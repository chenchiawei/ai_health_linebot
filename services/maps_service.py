import logging
import requests
from typing import List, Dict, Any
from config import settings

logger = logging.getLogger(__name__)

def search_nearby_healthy_restaurants(latitude: float, longitude: float, radius_meters: int = 1000) -> List[Dict[str, Any]]:
    """
    搜尋使用者周邊的健康/減脂/低卡/健身外食店家。
    使用 Google Places API (Nearby Search)。若未設定 API Key，則回傳模擬推薦清單。
    """
    if not settings.GOOGLE_MAPS_API_KEY or settings.GOOGLE_MAPS_API_KEY == "your_google_maps_api_key_here":
        # 示範模擬店家清單（當無 API Key 時供開發測試）
        return [
            {
                "name": "極光健康少油餐盒 (示範推薦)",
                "type": "健康便當 / 舒肥雞胸",
                "rating": 4.7,
                "address": "您當前位置 300 公尺內",
                "distance_text": "步行約 4 分鐘"
            },
            {
                "name": "7-ELEVEN / 全家便利商店",
                "type": "超商低卡組合 (雞胸肉+豆漿)",
                "rating": 4.5,
                "address": "附近 150 公尺",
                "distance_text": "步行約 2 分鐘"
            },
            {
                "name": "鮮涮小火鍋 (昆布清湯底)",
                "type": "原型食物 / 小火鍋",
                "rating": 4.4,
                "address": "附近 500 公尺",
                "distance_text": "步行約 6 分鐘"
            }
        ]

    try:
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        keywords = "健康便當 OR 健身餐 OR 低卡 OR 舒肥 OR 小火鍋 OR SUBWAY"
        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius_meters,
            "keyword": keywords,
            "language": "zh-TW",
            "key": settings.GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        results = []
        if data.get("status") == "OK":
            for place in data.get("results", [])[:4]: # 取前 4 家評分優良者
                results.append({
                    "name": place.get("name", "健康餐廳"),
                    "type": "外食餐廳",
                    "rating": place.get("rating", 4.0),
                    "address": place.get("vicinity", "附近區域"),
                    "distance_text": "距離極近"
                })
            return results
        else:
            logger.warning(f"Google Places API 回傳狀態: {data.get('status')}")
            return search_nearby_healthy_restaurants(latitude, longitude) # 降級至預設模組

    except Exception as e:
        logger.error(f"Google Maps API 呼叫失敗: {e}")
        return search_nearby_healthy_restaurants(latitude, longitude)
