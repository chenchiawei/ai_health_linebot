from typing import Dict, Any, List
from linebot.v3.messaging import (
    FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction, LocationAction
)

def get_quick_reply_buttons() -> QuickReply:
    """
    提供 LINE 訊息下方的快捷按鈕 (Quick Reply Buttons)
    """
    return QuickReply(
        items=[
            QuickReplyItem(action=MessageAction(label="📊 今日進度", text="查看狀態")),
            QuickReplyItem(action=MessageAction(label="🏪 7-11點餐指南", text="7-11攻略")),
            QuickReplyItem(action=MessageAction(label="🍲 火鍋避坑指南", text="火鍋攻略")),
            QuickReplyItem(action=MessageAction(label="🍱 便當挑選指南", text="便當攻略")),
            QuickReplyItem(action=LocationAction(label="📍 附近外食推薦"))
        ]
    )

def create_outing_guide_flex(category: str) -> FlexMessage:
    """
    建立外食情境避坑點餐指南 Flex Card。
    """
    guides = {
        "7-11": {
            "title": "🏪 7-ELEVEN / 全家 減脂點餐攻略",
            "bg": "#008000",
            "combos": [
                {"name": "主食選擇", "desc": "地瓜 (中) / 藜麥飯糰 / 溫泉蛋"},
                {"name": "高蛋白補充", "desc": "舒肥雞胸肉 / 零脂希臘優格 / 義式雞胸"},
                {"name": "飲品搭配", "desc": "無糖高纖豆漿 / 黑咖啡 / 原味氣泡水"}
            ],
            "tip": "避開微波義大利麵與重醬炒飯，選擇原型食物搭配高纖豆漿最保險！"
        },
        "火鍋": {
            "title": "🍲 火鍋 / 涮涮鍋 避坑點餐攻略",
            "bg": "#C0392B",
            "combos": [
                {"name": "湯底選擇", "desc": "昆布湯 / 蔬菜清湯（避開麻辣、牛奶湯）"},
                {"name": "主食與菜盤", "desc": "菜盤換全蔬菜 / 芋頭南瓜替代白飯"},
                {"name": "醬汁建議", "desc": "日式醬油 + 蔥花 + 蒜泥 + 辣椒 + 醋"}
            ],
            "tip": "避免火鍋料加工品（餃類/丸類），肉品選低脂牛/去皮雞肉/海鮮！"
        },
        "便當": {
            "title": "🍱 台式便當 / 自選便當 減脂攻略",
            "bg": "#D35400",
            "combos": [
                {"name": "主菜選擇", "desc": "清蒸魚 / 滷雞腿去皮 / 舒肥雞胸 (避開炸物)"},
                {"name": "飯量控制", "desc": "飯量要求半碗或紫米飯"},
                {"name": "配菜選擇", "desc": "選擇 3 種綠色蔬菜/蒸蛋/豆腐 (瀝乾醬汁)"}
            ],
            "tip": "要求店家『不要淋肉燥醬汁在飯上』，立減 150 kcal 隱形脂肪！"
        }
    }

    info = guides.get(category, guides["7-11"])
    combo_contents = []

    for item in info["combos"]:
        combo_contents.append({
            "type": "box",
            "layout": "vertical",
            "margin": "sm",
            "contents": [
                {"type": "text", "text": f"🔹 {item['name']}", "weight": "bold", "size": "xs", "color": "#2C3E50"},
                {"type": "text", "text": item["desc"], "size": "xs", "color": "#555555", "margin": "xs"}
            ]
        })

    flex_content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": info["bg"],
            "contents": [
                {"type": "text", "text": info["title"], "weight": "bold", "color": "#FFFFFF", "size": "sm"}
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": combo_contents + [
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "backgroundColor": "#F8F9FA",
                    "paddingAll": "md",
                    "cornerRadius": "md",
                    "contents": [
                        {"type": "text", "text": "💡 營養師避坑秘訣", "weight": "bold", "size": "xs", "color": "#E67E22"},
                        {"type": "text", "text": info["tip"], "wrap": True, "size": "xs", "color": "#666666", "margin": "xs"}
                    ]
                }
            ]
        }
    }

    return FlexMessage(alt_text=info["title"], contents=FlexContainer.from_dict(flex_content))

def create_meal_flex_message(meal_data: Dict[str, Any], user_summary: Dict[str, Any]) -> FlexMessage:
    """
    建立飲食打卡/照片辨識結果的 Flex Message 卡片。
    """
    rem_cal = max(0, user_summary.get("target_calories", 2000) - user_summary.get("today_calories", 0))
    rem_p = max(0, user_summary.get("target_protein", 140) - user_summary.get("today_protein", 0))

    flex_content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#1DB446",
            "contents": [
                {
                    "type": "text",
                    "text": "🍱 AI 飲食分析報告",
                    "weight": "bold",
                    "color": "#FFFFFF",
                    "size": "lg"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": meal_data.get("food_name", "餐點分析"),
                    "weight": "bold",
                    "size": "xl",
                    "color": "#111111"
                },
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {"type": "text", "text": "🔥 預估熱量", "color": "#aaaaaa", "size": "sm", "flex": 2},
                                {"type": "text", "text": f"{meal_data.get('calories', 0)} kcal", "weight": "bold", "size": "sm", "color": "#e74c3c", "flex": 3}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {"type": "text", "text": "🥩 蛋白質", "color": "#aaaaaa", "size": "sm", "flex": 2},
                                {"type": "text", "text": f"{meal_data.get('protein', 0)} g", "weight": "bold", "size": "sm", "color": "#3498db", "flex": 3}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {"type": "text", "text": "🍚 碳水化合物", "color": "#aaaaaa", "size": "sm", "flex": 2},
                                {"type": "text", "text": f"{meal_data.get('carbs', 0)} g", "weight": "bold", "size": "sm", "color": "#f39c12", "flex": 3}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {"type": "text", "text": "🥑 脂肪", "color": "#aaaaaa", "size": "sm", "flex": 2},
                                {"type": "text", "text": f"{meal_data.get('fat', 0)} g", "weight": "bold", "size": "sm", "color": "#9b59b6", "flex": 3}
                            ]
                        }
                    ]
                },
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [
                        {"type": "text", "text": "💡 營養師評語", "weight": "bold", "size": "sm", "color": "#27ae60"},
                        {"type": "text", "text": meal_data.get("advice", "營養均衡！"), "wrap": True, "size": "xs", "color": "#555555", "margin": "xs"}
                    ]
                },
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [
                        {"type": "text", "text": f"📊 今日剩餘額度：{round(rem_cal)} kcal | 補蛋白質 {round(rem_p)}g", "size": "xs", "color": "#888888", "align": "center"}
                    ]
                }
            ]
        }
    }
    return FlexMessage(alt_text="🍱 AI 飲食分析報告", contents=FlexContainer.from_dict(flex_content))

def create_health_summary_flex_message(user_data: Dict[str, Any], today_logs: Dict[str, Any]) -> FlexMessage:
    """
    建立個人健康檔案與今日數據總覽 Flex Message。
    """
    tdee = user_data.get("tdee", 2000)
    target_cal = user_data.get("target_calories", 1800)
    today_cal = today_logs.get("today_calories", 0)
    rem_cal = max(0, target_cal - today_cal)

    target_p = user_data.get("target_protein", 140)
    today_p = today_logs.get("today_protein", 0)
    rem_p = max(0, target_p - today_p)

    flex_content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#34495E",
            "contents": [
                {"type": "text", "text": "📊 個人健康與熱量概況", "weight": "bold", "color": "#FFFFFF", "size": "lg"}
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": f"⚖️ 體重: {user_data.get('weight', 70)} kg", "weight": "bold", "size": "sm"},
                        {"type": "text", "text": f"📉 體脂: {user_data.get('body_fat', '未填')}%", "weight": "bold", "size": "sm", "align": "end"}
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xs",
                    "contents": [
                        {"type": "text", "text": f"🔥 TDEE: {tdee} kcal", "size": "xs", "color": "#7f8c8d"},
                        {"type": "text", "text": f"🎯 目標熱量: {target_cal} kcal", "size": "xs", "color": "#27ae60", "align": "end"}
                    ]
                },
                {"type": "separator", "margin": "md"},
                {
                    "type": "text",
                    "text": "📅 今日熱量與營養進度",
                    "weight": "bold",
                    "margin": "md",
                    "size": "sm"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "sm",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {"type": "text", "text": "已攝取熱量", "size": "xs", "color": "#666666", "flex": 3},
                                {"type": "text", "text": f"{round(today_cal)} / {round(target_cal)} kcal", "size": "xs", "weight": "bold", "flex": 4}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {"type": "text", "text": "已攝取蛋白質", "size": "xs", "color": "#666666", "flex": 3},
                                {"type": "text", "text": f"{round(today_p)} / {round(target_p)} g", "size": "xs", "weight": "bold", "color": "#2980b9", "flex": 4}
                            ]
                        }
                    ]
                },
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "backgroundColor": "#ECF0F1",
                    "cornerRadius": "md",
                    "paddingAll": "md",
                    "contents": [
                        {"type": "text", "text": "💡 下餐推薦額度", "weight": "bold", "size": "xs", "color": "#2c3e50"},
                        {"type": "text", "text": f"熱量剩餘: {round(rem_cal)} kcal", "size": "xs", "color": "#e67e22"},
                        {"type": "text", "text": f"蛋白質尚缺: {round(rem_p)} g", "size": "xs", "color": "#2980b9"}
                    ]
                }
            ]
        }
    }
    return FlexMessage(alt_text="📊 個人健康與熱量概況", contents=FlexContainer.from_dict(flex_content))

def create_dine_out_flex_carousel(restaurants: List[Dict[str, Any]], tips: str) -> FlexMessage:
    """
    建立 Google Maps 外食推薦與點餐攻略卡片輪播 (Carousel)。
    """
    bubbles = []
    for spot in restaurants:
        bubble = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#E67E22",
                "contents": [
                    {"type": "text", "text": "🗺️ 周邊健康外食推薦", "color": "#FFFFFF", "size": "xs", "weight": "bold"},
                    {"type": "text", "text": spot.get("name", "健康餐廳"), "color": "#FFFFFF", "size": "md", "weight": "bold", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                            {"type": "text", "text": "🏷️ 類型", "size": "xs", "color": "#7f8c8d", "flex": 2},
                            {"type": "text", "text": spot.get("type", "外食"), "size": "xs", "weight": "bold", "flex": 4}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "xs",
                        "contents": [
                            {"type": "text", "text": "⭐ 評分", "size": "xs", "color": "#7f8c8d", "flex": 2},
                            {"type": "text", "text": f"{spot.get('rating', 4.5)} / 5.0", "size": "xs", "color": "#f39c12", "weight": "bold", "flex": 4}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "xs",
                        "contents": [
                            {"type": "text", "text": "📍 位置", "size": "xs", "color": "#7f8c8d", "flex": 2},
                            {"type": "text", "text": spot.get("address", "附近"), "size": "xs", "color": "#333333", "flex": 4}
                        ]
                    },
                    {"type": "separator", "margin": "md"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {"type": "text", "text": "👨‍🍳 AI 建議點餐組合", "weight": "bold", "size": "xs", "color": "#d35400"},
                            {"type": "text", "text": tips, "wrap": True, "size": "xs", "color": "#555555", "margin": "xs"}
                        ]
                    }
                ]
            }
        }
        bubbles.append(bubble)

    carousel_content = {
        "type": "carousel",
        "contents": bubbles
    }
    return FlexMessage(alt_text="🗺️ 周邊健康外食推薦", contents=FlexContainer.from_dict(carousel_content))
