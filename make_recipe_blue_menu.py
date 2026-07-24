import os
from PIL import Image, ImageDraw, ImageFont

# LINE 官方標準 2500 x 1686 像素
width, height = 2500, 1686

# 全圖淡藍色清新醫療/健康高質感底色 (#F0F7FF)
img = Image.new("RGBA", (width, height), color=(240, 247, 255, 255))
draw = ImageDraw.Draw(img)

w_left = 833
w_right = 833
h_half = 843

NAVY_TEXT = (30, 58, 138, 255)
SLATE_SUB = (71, 85, 105, 255)
BORDER_BLUE = (191, 219, 254, 255)

panels = [
    # 1. 左側大卡片 (高 1686) - 核心照片打卡
    {
        "is_left_main": True,
        "icon": "📷",
        "title": "飲食拍照打卡",
        "sub": "拍照上傳或輸入餐點\nAI 秒算熱量與蛋白質",
        "pill": "📷 拍照 / 文字打卡",
        "card_bg": (219, 234, 254, 255),   # 淡寶藍色
        "pill_bg": (37, 99, 235, 255),     # 皇家藍 Pill 按鈕
        "pill_text": (255, 255, 255, 255),
        "x0": 0, "y0": 0, "x1": w_left, "y1": height
    },
    # 2. 右上左 - 個人健康數據
    {
        "is_left_main": False,
        "icon": "📊",
        "title": "個人健康數據",
        "sub": "7日體重趨勢與營養比例",
        "pill": "健康數據看板",
        "card_bg": (239, 246, 255, 255),   # 天空冰藍
        "pill_bg": (219, 234, 254, 255),
        "pill_text": (30, 64, 175, 255),
        "x0": w_left, "y0": 0, "x1": w_left + w_right, "y1": h_half
    },
    # 3. 右上右 - 智慧健康食譜 (全新強大 AI 食譜功能!)
    {
        "is_left_main": False,
        "icon": "🍳",
        "title": "智慧健康食譜",
        "sub": "想吃什麼，AI 教你輕鬆煮",
        "pill": "🍳 AI 智慧食譜",
        "card_bg": (224, 242, 254, 255),   # 水藍色
        "pill_bg": (186, 230, 253, 255),
        "pill_text": (3, 105, 161, 255),
        "x0": w_left + w_right, "y0": 0, "x1": width, "y1": h_half
    },
    # 4. 右下左 - 外食點餐避坑
    {
        "is_left_main": False,
        "icon": "🍱",
        "title": "外食點餐指南",
        "sub": "7-11、火鍋、便當避坑指南",
        "pill": "外食點餐指南",
        "card_bg": (236, 254, 255, 255),   # 清涼湖水藍
        "pill_bg": (207, 250, 254, 255),
        "pill_text": (14, 116, 144, 255),
        "x0": w_left, "y0": h_half, "x1": w_left + w_right, "y1": height
    },
    # 5. 右下右 - 附近健康外食
    {
        "is_left_main": False,
        "icon": "📍",
        "title": "附近健康外食",
        "sub": "傳送定位推薦周邊低卡餐廳",
        "pill": "地圖定位搜尋",
        "card_bg": (238, 242, 255, 255),   # 輕淡紫藍色
        "pill_bg": (224, 231, 255, 255),
        "pill_text": (67, 56, 202, 255),
        "x0": w_left + w_right, "y0": h_half, "x1": width, "y1": height
    },
]

# 字型設定
try:
    font_main_lg = ImageFont.truetype("msjh.ttc", 68)
    font_main = ImageFont.truetype("msjh.ttc", 54)
    font_sub = ImageFont.truetype("msjh.ttc", 32)
    font_pill = ImageFont.truetype("msjh.ttc", 36)
    font_icon_lg = ImageFont.truetype("seguiemj.ttf", 160)
    font_icon = ImageFont.truetype("seguiemj.ttf", 110)
except:
    try:
        font_main_lg = font_main = ImageFont.truetype("arial.ttf", 54)
        font_sub = font_pill = ImageFont.truetype("arial.ttf", 32)
        font_icon_lg = font_icon = ImageFont.load_default()
    except:
        font_main_lg = font_main = font_sub = font_pill = font_icon_lg = font_icon = ImageFont.load_default()

margin = 16
radius = 32

for p in panels:
    x0, y0 = p["x0"] + margin, p["y0"] + margin
    x1, y1 = p["x1"] - margin, p["y1"] - margin
    
    # 卡片底色
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=p["card_bg"])
    # 質感細邊框
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=BORDER_BLUE, width=3)
    
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    
    if p.get("is_left_main"):
        draw.text((cx, cy - 240), p["icon"], fill=(30, 41, 59, 255), font=font_icon_lg, anchor="mm")
        draw.text((cx, cy - 20), p["title"], fill=NAVY_TEXT, font=font_main_lg, anchor="mm")
        
        lines = p["sub"].split("\n")
        draw.text((cx, cy + 90), lines[0], fill=SLATE_SUB, font=font_sub, anchor="mm")
        draw.text((cx, cy + 140), lines[1], fill=SLATE_SUB, font=font_sub, anchor="mm")
        
        pill_w, pill_h = 580, 100
        py = y1 - 160
        draw.rounded_rectangle([cx - pill_w//2, py, cx + pill_w//2, py + pill_h], radius=50, fill=p["pill_bg"])
        draw.text((cx, py + pill_h//2), p["pill"], fill=p["pill_text"], font=font_pill, anchor="mm")
        
    else:
        draw.text((cx, cy - 110), p["icon"], fill=(30, 41, 59, 255), font=font_icon, anchor="mm")
        draw.text((cx, cy + 25), p["title"], fill=NAVY_TEXT, font=font_main, anchor="mm")
        draw.text((cx, cy + 90), p["sub"], fill=SLATE_SUB, font=font_sub, anchor="mm")
        
        pill_w, pill_h = 360, 68
        py = y1 - 100
        draw.rounded_rectangle([cx - pill_w//2, py, cx + pill_w//2, py + pill_h], radius=34, fill=p["pill_bg"])
        draw.text((cx, py + pill_h//2), p["pill"], fill=p["pill_text"], font=font_pill, anchor="mm")

# 轉 RGB
final_img = Image.new("RGB", (width, height), (240, 247, 255))
final_img.paste(img, (0, 0), mask=img)

# 儲存
out_path = os.path.join("static", "rich_menu_recipe_blue_2500x1686.png")
final_img.save(out_path, quality=98)
print(f"含智慧食譜之淡藍色極致質感圖文選單已生成: {out_path}")
