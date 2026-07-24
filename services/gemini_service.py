import json
import logging
from typing import Optional, Dict, Any
from config import settings

logger = logging.getLogger(__name__)

def calculate_tdee_and_targets(
    gender: str = "male",
    age: int = 25,
    height: float = 170.0,
    weight: float = 70.0,
    body_fat: Optional[float] = None,
    activity_level: float = 1.375,
    goal: str = "cut"
) -> Dict[str, float]:
    """
    計算基礎代謝 (BMR)、每日總熱量消耗 (TDEE) 與目標三大營養素。
    """
    # 如果有體脂率，使用 Katch-McArdle 公式，否則使用 Mifflin-St Jeor 公式
    if body_fat and body_fat > 0:
        lean_mass = weight * (1 - body_fat / 100)
        bmr = 370 + (21.6 * lean_mass)
    else:
        if gender.lower() in ["male", "男", "m"]:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    tdee = bmr * activity_level

    # 依目標調整熱量攝取上限
    if goal == "cut":
        target_calories = max(bmr, tdee - 500.0) # 減脂：赤字 500 kcal，但不低於 BMR
    elif goal == "bulk":
        target_calories = tdee + 300.0            # 增肌：盈餘 300 kcal
    else:
        target_calories = tdee                    # 維持

    # 計算三大營養素分配（健身減重黃金比例）
    # 蛋白質：每公斤體重 2.0 克 (減脂/健身保護肌肉)
    target_protein = weight * 2.0
    protein_calories = target_protein * 4.0

    # 脂肪：總熱量的 25%
    fat_calories = target_calories * 0.25
    target_fat = fat_calories / 9.0

    # 碳水化合物：剩餘熱量
    carbs_calories = max(0, target_calories - protein_calories - fat_calories)
    target_carbs = carbs_calories / 4.0

    return {
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "target_calories": round(target_calories, 1),
        "target_protein": round(target_protein, 1),
        "target_carbs": round(target_carbs, 1),
        "target_fat": round(target_fat, 1)
    }

def estimate_food_dynamically(text: str) -> Dict[str, Any]:
    """
    智慧在地餐點動態估算器：當 Gemini API 遇到頻率限制 (429) 時，
    根據使用者輸入的關鍵字與份量，動態計算卡路里與三大營養素！
    """
    text_lower = text.lower() if text else ""
    
    # 份量倍數判斷
    portion = 1.0
    if any(k in text_lower for k in ["兩顆", "2顆", "雙份", "大份", "兩份", "2份", "大碗"]):
        portion = 1.8
    elif any(k in text_lower for k in ["半碗", "少飯", "小份", "半份", "微糖"]):
        portion = 0.6

    cal, p, c, f = 0.0, 0.0, 0.0, 0.0
    matched_items = []

    # 食物資料庫關鍵字與單位熱量
    db_items = [
        ("雞胸", 160, 30, 1, 4, "雞胸肉"),
        ("雞腿", 260, 24, 2, 16, "雞腿"),
        ("排骨", 340, 20, 12, 22, "排骨"),
        ("便當", 350, 10, 55, 12, "便當主食"),
        ("白飯", 280, 6, 60, 1, "白飯"),
        ("紫米", 240, 7, 50, 2, "紫米飯"),
        ("地瓜", 140, 2, 33, 1, "地瓜"),
        ("蛋", 75, 7, 1, 5, "雞蛋"),
        ("美式", 10, 1, 1, 0, "美式咖啡"),
        ("黑咖啡", 10, 1, 1, 0, "黑咖啡"),
        ("拿鐵", 160, 8, 13, 8, "拿鐵"),
        ("珍珠奶茶", 520, 4, 80, 20, "珍珠奶茶"),
        ("珍奶", 520, 4, 80, 20, "珍珠奶茶"),
        ("牛排", 480, 45, 2, 30, "牛排"),
        ("火鍋", 650, 42, 35, 32, "火鍋"),
        ("沙拉", 160, 6, 16, 8, "沙拉"),
        ("燕麥", 180, 6, 32, 3, "燕麥"),
        ("豆漿", 130, 10, 9, 5, "豆漿"),
        ("高蛋白", 150, 26, 3, 2, "高蛋白"),
        ("漢堡", 420, 18, 42, 20, "漢堡"),
        ("披薩", 300, 12, 35, 12, "披薩(單片)"),
        ("吐司", 140, 4, 26, 2, "吐司"),
        ("巧克力", 180, 2, 22, 9, "巧克力醬/抹醬")
    ]

    for kw, item_cal, item_p, item_c, item_f, name in db_items:
        if kw in text_lower:
            cal += item_cal
            p += item_p
            c += item_c
            f += item_f
            matched_items.append(name)

    # 若無匹配任何特定關鍵字，則進行基礎字數與一般餐點估算
    if cal == 0.0:
        cal, p, c, f = 450.0, 22.0, 50.0, 14.0
        food_name = text or "日常餐點"
    else:
        cal *= portion
        p *= portion
        c *= portion
        f *= portion
        food_name = " + ".join(matched_items) if matched_items else (text or "估算餐點")

    return {
        "type": "meal",
        "food_name": food_name,
        "calories": round(cal, 1),
        "protein": round(p, 1),
        "carbs": round(c, 1),
        "fat": round(f, 1),
        "advice": f"依據估算，這餐約提供 {round(p)}g 蛋白質！繼續保持健康飲食目標！"
    }

def analyze_food_with_gemini(image_bytes: Optional[bytes] = None, text_description: Optional[str] = None) -> Dict[str, Any]:
    """
    呼叫 Gemini API 智慧區分「一般聊天問答」與「飲食紀錄打卡」。
    """
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
        if text_description and any(kw in text_description.lower() for kw in ["你好", "哈囉", "嗨", "你是誰", "安安"]):
            return {
                "type": "chat",
                "reply": "你好呀！我是你的專屬 AI 健康與減重外食特助 🥗！今天過得如何？隨時可以跟我分享今天的餐點照片、輸入文字打卡（如：『吃了雞胸便當』），或是點擊傳送地點讓我推薦周邊健康外食喔！"
            }
        return estimate_food_dynamically(text_description or "")

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        prompt = """你是 AI 健康教練。分析輸入（圖片/文字）。
1. 若是一般招呼/聊天問答(如你好、你是誰、減脂觀念):
   輸出 JSON: {"type": "chat", "reply": "簡短回答(50字內)"}
2. 若是飲食打卡(如吃了雞胸便當、黑咖啡):
   輸出 JSON: {"type": "meal", "food_name": "餐點名", "calories": 熱量, "protein": 蛋白質, "carbs": 碳水, "fat": 脂肪, "advice": "評語(30字內)"}
僅輸出 JSON。"""

        contents = []
        if image_bytes:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"))
        if text_description:
            contents.append(text_description)
        contents.append(prompt)

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=contents,
        )

        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        data = json.loads(raw_text.strip())
        return data

    except Exception as e:
        logger.error(f"Gemini API 呼叫失敗: {e}")
        # 當 Gemini API 遇到限制或網路問題時，開啟動態估算器
        if text_description and any(kw in text_description.lower() for kw in ["你好", "哈囉", "嗨", "你是誰", "安安", "早安", "午安", "晚安"]):
            return {
                "type": "chat",
                "reply": "你好呀！我是你的專屬 AI 健康與減重外食特助 🥗！有什麼我可以幫忙的嗎？可以隨時拍餐點照片或輸入『吃了什麼』進行熱量打卡喔！"
            }
        return estimate_food_dynamically(text_description or "")

def generate_dine_out_tips(restaurant_name: str, restaurant_type: str, remaining_cal: float, remaining_protein: float) -> str:
    """
    結合使用者剩餘熱量與店家類型，生成專屬外食點餐攻略。
    """
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
        return f"💡 點餐攻略：前往『{restaurant_name}』，目前您今日還剩 {remaining_cal} kcal、需補 {remaining_protein}g 蛋白質。建議選擇主食減半、雙份蛋白質（如去皮雞腿/豆腐），並避免重油醬汁！"

    try:
        from google import genai
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        prompt = f"""使用者正在『{restaurant_name}』（類型：{restaurant_type}）準備用餐。
使用者今天的剩餘目標：
- 還可攝取熱量：{remaining_cal} kcal
- 還需補充蛋白質：{remaining_protein} g

請以專業減重健身營養師的口吻，給予 3 條具體、可操作的點餐與搭配建議（例如：如何點菜、飯量控制、醬汁選擇）。
字數控制在 120 字以內，用語簡潔親切。"""

        response = client.models.generate_content(
            model="gemini-1.5-flash-8b",
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        return f"💡 點餐建議：建議選澤高蛋白質主菜（如清蒸/舒肥雞胸肉/魚肉），白飯減半，並搭配無糖飲料以防熱量超標。"
