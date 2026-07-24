import re
import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, MessagingApiBlob,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent, TextMessageContent, ImageMessageContent, LocationMessageContent
)

from config import settings
from database import engine, get_db, Base
import models
from services import gemini_service, maps_service, line_service

# 初始化日誌與資料庫表
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_health_bot")
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI 健康 & 減重外食 LINE Bot")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# 掛載靜態檔案 (LIFF Dashboard)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# LINE API 設定
configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

@app.get("/")
def read_root():
    return {"status": "online", "message": "AI 健康 LINE Bot 伺服器運作中！"}

@app.get("/liff")
def get_liff_page():
    """回傳 LINE LIFF 視覺化數據圖表網頁"""
    return FileResponse(os.path.join(STATIC_DIR, "liff.html"))

@app.get("/rich_menu.png")
def get_rich_menu_image():
    """回傳 2500x1686 圖文選單背景圖片"""
    return FileResponse(os.path.join(STATIC_DIR, "rich_menu_2500x1686.png"))

@app.get("/rich_menu_1040.png")
def get_rich_menu_1040_image():
    """回傳 1040x1040 精緻質感圖文選單背景圖片"""
    p1 = os.path.join(STATIC_DIR, "rich_menu_1040x1040.png")
    p2 = os.path.join(os.getcwd(), "static", "rich_menu_1040x1040.png")
    if os.path.exists(p1):
        return FileResponse(p1)
    elif os.path.exists(p2):
        return FileResponse(p2)
    return {"error": "file not found", "p1": p1, "p2": p2, "cwd": os.getcwd()}

@app.get("/api/user_stats/{user_id}")
def get_user_stats(user_id: str, db: Session = Depends(get_db)):
    """提供 LIFF 圖表使用之歷史體重與三大營養素統計資料"""
    user = db.query(models.User).filter(models.User.line_user_id == user_id).first()
    if not user:
        return {"status": "error", "message": "User not found"}

    # 取最近 7 天體重
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    logs = db.query(models.HealthLog).filter(
        models.HealthLog.line_user_id == user_id,
        models.HealthLog.logged_at >= seven_days_ago
    ).order_by(models.HealthLog.logged_at.asc()).all()

    today_summary = get_today_nutrition_summary(db, user_id)

    return {
        "weight": user.weight,
        "body_fat": user.body_fat or 0,
        "today_calories": today_summary["today_calories"],
        "today_protein": today_summary["today_protein"],
        "history": [{"weight": l.weight, "body_fat": l.body_fat, "date": l.logged_at.strftime("%m/%d")} for l in logs]
    }

@app.post("/webhook")
async def callback(request: Request):
    """
    LINE Webhook 進入點
    """
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        logger.error("Invalid LINE signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
    return "OK"

# ------------------------------------------------------------------
# LINE 事件處理器
# ------------------------------------------------------------------

@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    """
    處理使用者傳送的文字訊息 (設定個人資料、外食攻略、文字飲食打卡、查詢狀態)
    """
    user_id = event.source.user_id
    user_text = event.message.text.strip()
    db = next(get_db())

    # 1. 取得或建立使用者資料
    user = db.query(models.User).filter(models.User.line_user_id == user_id).first()
    if not user:
        user = models.User(line_user_id=user_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    # 2. 指令解析：外食情境避坑指南
    if "7-11" in user_text or "超商" in user_text:
        flex_msg = line_service.create_outing_guide_flex("7-11")
        send_line_reply(event.reply_token, flex_msg)
        return
    elif "火鍋" in user_text:
        flex_msg = line_service.create_outing_guide_flex("火鍋")
        send_line_reply(event.reply_token, flex_msg)
        return
    elif "便當" in user_text and not any(k in user_text for k in ["吃了", "吃個", "紀錄"]):
        flex_msg = line_service.create_outing_guide_flex("便當")
        send_line_reply(event.reply_token, flex_msg)
        return

    # 3. 指令解析：查看狀態 / 說明
    if user_text in ["查看狀態", "我的資料", "健康概況", "打卡總覽", "選單"]:
        reply_msg = get_user_summary_flex(db, user)
        send_line_reply(event.reply_token, reply_msg)
        return

    # 4. 指令解析：設定基本資料 (例如: "設定 175cm 70kg 15% 減脂" 或 "體重 68kg")
    if "設定" in user_text or "體重" in user_text or "體脂" in user_text:
        reply_text = parse_and_update_user_profile(db, user, user_text)
        send_line_reply(event.reply_token, TextMessage(text=reply_text, quick_reply=line_service.get_quick_reply_buttons()))
        return

    # 5. 預設：智慧判斷日常聊天 vs 飲食打卡
    process_text_meal_log(event, db, user, user_text)

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    """
    處理使用者上傳的食物照片
    """
    user_id = event.source.user_id
    db = next(get_db())
    user = db.query(models.User).filter(models.User.line_user_id == user_id).first()
    if not user:
        user = models.User(line_user_id=user_id)
        db.add(user)
        db.commit()

    try:
        with ApiClient(configuration) as api_client:
            line_bot_blob_api = MessagingApiBlob(api_client)
            image_bytes = line_bot_blob_api.get_message_content(message_id=event.message.id)

        meal_data = gemini_service.analyze_food_with_gemini(image_bytes=image_bytes)
        save_meal_log(db, user_id, meal_data)

        today_summary = get_today_nutrition_summary(db, user_id)
        user_summary = {
            "target_calories": user.target_calories,
            "target_protein": user.target_protein,
            "today_calories": today_summary["today_calories"],
            "today_protein": today_summary["today_protein"]
        }

        flex_msg = line_service.create_meal_flex_message(meal_data, user_summary)
        send_line_reply(event.reply_token, flex_msg)

    except Exception as e:
        logger.error(f"處理圖片失敗: {e}")
        send_line_reply(event.reply_token, TextMessage(text="⚠️ 圖片分析時發生錯誤，請稍後重試！", quick_reply=line_service.get_quick_reply_buttons()))

@handler.add(MessageEvent, message=LocationMessageContent)
def handle_location_message(event):
    """
    處理使用者傳送的 LINE 位置訊息，推薦周邊健康外食並給予 AI 點餐建議
    """
    user_id = event.source.user_id
    lat = event.message.latitude
    lng = event.message.longitude

    db = next(get_db())
    user = db.query(models.User).filter(models.User.line_user_id == user_id).first()
    if not user:
        user = models.User(line_user_id=user_id)

    today_summary = get_today_nutrition_summary(db, user_id)
    rem_cal = max(0, user.target_calories - today_summary["today_calories"])
    rem_p = max(0, user.target_protein - today_summary["today_protein"])

    restaurants = maps_service.search_nearby_healthy_restaurants(lat, lng)

    first_spot = restaurants[0] if restaurants else {"name": "健康餐廳", "type": "低卡便當"}
    tips = gemini_service.generate_dine_out_tips(
        restaurant_name=first_spot["name"],
        restaurant_type=first_spot["type"],
        remaining_cal=round(rem_cal),
        remaining_protein=round(rem_p)
    )

    carousel_msg = line_service.create_dine_out_flex_carousel(restaurants, tips)
    send_line_reply(event.reply_token, carousel_msg)

# ------------------------------------------------------------------
# 輔助函式
# ------------------------------------------------------------------

def send_line_reply(reply_token: str, message):
    if hasattr(message, 'quick_reply') and message.quick_reply is None:
        message.quick_reply = line_service.get_quick_reply_buttons()

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[message]
            )
        )

def process_text_meal_log(event, db: Session, user: models.User, user_text: str):
    """處理文字輸入：自動區分一般聊天與飲食打卡"""
    ai_res = gemini_service.analyze_food_with_gemini(text_description=user_text)

    if ai_res.get("type") == "chat" or "reply" in ai_res:
        reply_text = ai_res.get("reply", "你好呀！我是你的專屬 AI 健康與減重外食特助 🥗！有什麼我可以幫忙的嗎？")
        send_line_reply(event.reply_token, TextMessage(text=reply_text, quick_reply=line_service.get_quick_reply_buttons()))
        return

    save_meal_log(db, user.line_user_id, ai_res)

    today_summary = get_today_nutrition_summary(db, user.line_user_id)
    user_summary = {
        "target_calories": user.target_calories,
        "target_protein": user.target_protein,
        "today_calories": today_summary["today_calories"],
        "today_protein": today_summary["today_protein"]
    }
    flex_msg = line_service.create_meal_flex_message(ai_res, user_summary)
    send_line_reply(event.reply_token, flex_msg)

def save_meal_log(db: Session, user_id: str, meal_data: dict):
    log = models.MealLog(
        line_user_id=user_id,
        meal_name=meal_data.get("food_name", "餐點記錄"),
        calories=meal_data.get("calories", 0),
        protein=meal_data.get("protein", 0),
        carbs=meal_data.get("carbs", 0),
        fat=meal_data.get("fat", 0),
        notes=meal_data.get("advice", "")
    )
    db.add(log)
    db.commit()

def get_today_nutrition_summary(db: Session, user_id: str) -> dict:
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    logs = db.query(models.MealLog).filter(
        models.MealLog.line_user_id == user_id,
        models.MealLog.logged_at >= today_start
    ).all()

    today_cal = sum(l.calories for l in logs)
    today_p = sum(l.protein for l in logs)
    return {"today_calories": today_cal, "today_protein": today_p}

def get_user_summary_flex(db: Session, user: models.User):
    today_summary = get_today_nutrition_summary(db, user.line_user_id)
    user_dict = {
        "weight": user.weight,
        "body_fat": user.body_fat or "未填",
        "tdee": round(user.tdee),
        "target_calories": round(user.target_calories),
        "target_protein": round(user.target_protein)
    }
    return line_service.create_health_summary_flex_message(user_dict, today_summary)

def parse_and_update_user_profile(db: Session, user: models.User, text: str) -> str:
    """解析使用者設定字串並更新 BMR/TDEE 及目標"""
    h_match = re.search(r"(\d+(\.\d+)?)\s*(cm|公分)", text, re.IGNORECASE)
    if h_match:
        user.height = float(h_match.group(1))

    w_match = re.search(r"(\d+(\.\d+)?)\s*(kg|公斤|體重)", text, re.IGNORECASE)
    if w_match:
        user.weight = float(w_match.group(1))
        # 新增至體重歷史紀錄
        h_log = models.HealthLog(line_user_id=user.line_user_id, weight=user.weight, body_fat=user.body_fat)
        db.add(h_log)

    bf_match = re.search(r"(\d+(\.\d+)?)\s*(%|體脂)", text, re.IGNORECASE)
    if bf_match:
        user.body_fat = float(bf_match.group(1))

    if "增肌" in text:
        user.goal = "bulk"
    elif "維持" in text:
        user.goal = "maintain"
    elif "減脂" in text or "減肥" in text:
        user.goal = "cut"

    targets = gemini_service.calculate_tdee_and_targets(
        gender=user.gender,
        age=user.age,
        height=user.height,
        weight=user.weight,
        body_fat=user.body_fat,
        activity_level=user.activity_level,
        goal=user.goal
    )

    user.bmr = targets["bmr"]
    user.tdee = targets["tdee"]
    user.target_calories = targets["target_calories"]
    user.target_protein = targets["target_protein"]
    user.target_carbs = targets["target_carbs"]
    user.target_fat = targets["target_fat"]

    db.commit()

    return (
        f"✅ 個人檔案與目標已更新！\n"
        f"📏 身高: {user.height} cm | 體重: {user.weight} kg | 體脂: {user.body_fat or '未填'}%\n"
        f"🎯 目標: {'減脂' if user.goal=='cut' else '增肌' if user.goal=='bulk' else '維持'}\n"
        f"🔥 基礎代謝 (BMR): {round(user.bmr)} kcal\n"
        f"⚡ 每日總消耗 (TDEE): {round(user.tdee)} kcal\n"
        f"📌 建議每日攝取上限: {round(user.target_calories)} kcal (蛋白質 {round(user.target_protein)}g)"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
