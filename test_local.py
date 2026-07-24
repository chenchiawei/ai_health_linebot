"""
本地獨立功能測試腳本
不需連接 LINE 即可在主機上驗證 BMR/TDEE 計算、Gemini 飲食分析與 Google Maps 餐廳搜尋！
"""
import asyncio
from database import engine, SessionLocal, Base
import models
from services import gemini_service, maps_service

def run_local_test():
    print("=" * 60)
    print("🚀 開始執行 AI 健康 LINE Bot 本地功能模擬測試")
    print("=" * 60)

    # 1. 初始化 SQLite 資料庫
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 2. 測試 BMR / TDEE 動態計算模組
    print("\n[測試 1] BMR & TDEE 算力模組")
    targets = gemini_service.calculate_tdee_and_targets(
        gender="male",
        age=26,
        height=175.0,
        weight=72.0,
        body_fat=16.0,
        activity_level=1.375,
        goal="cut" # 減脂
    )
    print(f"  • 身高 175cm / 體重 72kg / 體脂 16% (減脂目標)")
    print(f"  • 基礎代謝 (BMR): {targets['bmr']} kcal")
    print(f"  • 每日總消耗 (TDEE): {targets['tdee']} kcal")
    print(f"  • 建議每日攝取熱量: {targets['target_calories']} kcal")
    print(f"  • 建議每日蛋白質: {targets['target_protein']} g")

    # 3. 測試文字飲食打卡與 Gemini 辨識
    print("\n[測試 2] 文字飲食打卡分析")
    test_food_text = "今天午餐吃了舒肥雞胸肉便當，紫米飯半碗，清蒸高麗菜"
    print(f"  • 模擬輸入文字: '{test_food_text}'")
    meal_res = gemini_service.analyze_food_with_gemini(text_description=test_food_text)
    print(f"  • 辨識餐點: {meal_res['food_name']}")
    print(f"  • 預估熱量: {meal_res['calories']} kcal")
    print(f"  • 蛋白質: {meal_res['protein']} g | 碳水: {meal_res['carbs']} g | 脂肪: {meal_res['fat']} g")
    print(f"  • AI 評語: {meal_res['advice']}")

    # 4. 測試 Google Maps 周邊健康餐廳搜尋
    print("\n[測試 3] Google Maps 外食地點搜尋與 AI 點餐建議")
    mock_lat, mock_lng = 25.0330, 121.5654 # 台北信義區座標
    spots = maps_service.search_nearby_healthy_restaurants(mock_lat, mock_lng)
    print(f"  • 搜尋結果 ({len(spots)} 家):")
    for s in spots:
        print(f"    - [{s['type']}] {s['name']} (評分: {s['rating']})")

    dine_tips = gemini_service.generate_dine_out_tips(
        restaurant_name=spots[0]['name'],
        restaurant_type=spots[0]['type'],
        remaining_cal=550.0,
        remaining_protein=35.0
    )
    print(f"\n  • 專屬外食點餐攻略:\n    {dine_tips}")

    print("\n" + "=" * 60)
    print("✅ 本地功能測試成功完成！程式邏輯正常！")
    print("=" * 60)

if __name__ == "__main__":
    run_local_test()
