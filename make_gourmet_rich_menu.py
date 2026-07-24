import os
from PIL import Image, ImageDraw, ImageFont

# 2500 x 1686 官方標準尺寸
width, height = 2500, 1686

# 讀取使用者照片
user_img_path = r"C:\Users\user\.gemini\antigravity\brain\12189836-d176-48a5-ae5d-5648c48e2e8b\.user_uploaded\media__1784874001311.png"

# 底色：清新水藍與微晨光乳白 (#F0F7FF)
canvas = Image.new("RGBA", (width, height), color=(240, 247, 255, 255))

if os.path.exists(user_img_path):
    food_photo = Image.open(user_img_path).convert("RGBA")
    # 將照片高品質縮放並淡化作為極致優雅背景
    food_photo = food_photo.resize((width, height), Image.Resampling.LANCZOS)
    # 微微降暗度與加強彩度，使前景卡片浮現
    dimmer = Image.new("RGBA", (width, height), (240, 247, 255, 140))
    bg_img = Image.alpha_composite(food_photo, dimmer)
else:
    bg_img = canvas

draw = ImageDraw.Draw(bg_img)

col_w = width // 3
row_h = height // 2

# 6 個獨立精緻莫蘭迪色系卡片 (完全不遮蓋、不發白、高質感)
panels = [
    {
        "icon": "📷",
        "title": "飲食拍照打卡",
        "sub": "拍照或輸入餐點，AI 秒算熱量",
        "bg": (255, 255, 255, 240),
        "border": (37, 99, 235, 255),
        "title_color": (30, 58, 138, 255),
        "sub_color": (71, 85, 105, 255),
        "btn_bg": (37, 99, 235, 255),
        "btn_text": "開始打卡",
        "x": 0, "y": 0
    },
    {
        "icon": "📊",
        "title": "個人健康數據",
        "sub": "7日體重趨勢圖與三大營養素",
        "bg": (255, 255, 255, 240),
        "border": (56, 189, 248, 255),
        "title_color": (12, 74, 110, 255),
        "sub_color": (71, 85, 105, 255),
        "btn_bg": (224, 242, 254, 255),
        "btn_text": "查看圖表",
        "x": col_w, "y": 0
    },
    {
        "icon": "🍳",
        "title": "智慧健康食譜",
        "sub": "想吃什麼，AI 教你輕鬆煮",
        "bg": (255, 255, 255, 240),
        "border": (251, 146, 60, 255),
        "title_color": (124, 45, 18, 255),
        "sub_color": (71, 85, 105, 255),
        "btn_bg": (254, 237, 213, 255),
        "btn_text": "食譜指南",
        "x": col_w * 2, "y": 0
    },
    {
        "icon": "🏪",
        "title": "超商減脂攻略",
        "sub": "7-11/全家健身原型食物組合",
        "bg": (255, 255, 255, 240),
        "border": (74, 222, 128, 255),
        "title_color": (20, 83, 45, 255),
        "sub_color": (71, 85, 105, 255),
        "btn_bg": (220, 252, 231, 255),
        "btn_text": "超商推薦",
        "x": 0, "y": row_h
    },
    {
        "icon": "🍲",
        "title": "火鍋便當避坑",
        "sub": "外食湯底醬汁聰明替換秘訣",
        "bg": (255, 255, 255, 240),
        "border": (248, 113, 113, 255),
        "title_color": (127, 29, 29, 255),
        "sub_color": (71, 85, 105, 255),
        "btn_bg": (254, 226, 226, 255),
        "btn_text": "外食點餐",
        "x": col_w, "y": row_h
    },
    {
        "icon": "📍",
        "title": "周邊健康外食",
        "sub": "一鍵定位搜尋附近低卡餐廳",
        "bg": (255, 255, 255, 240),
        "border": (167, 139, 250, 255),
        "title_color": (88, 28, 135, 255),
        "sub_color": (71, 85, 105, 255),
        "btn_bg": (237, 233, 254, 255),
        "btn_text": "地圖搜尋",
        "x": col_w * 2, "y": row_h
    },
]

# 字型設定
try:
    font_main = ImageFont.truetype("msjh.ttc", 58)
    font_sub = ImageFont.truetype("msjh.ttc", 32)
    font_btn = ImageFont.truetype("msjh.ttc", 32)
    font_icon = ImageFont.truetype("seguiemj.ttf", 110)
except:
    try:
        font_main = ImageFont.truetype("arial.ttf", 58)
        font_sub = font_btn = ImageFont.truetype("arial.ttf", 32)
        font_icon = ImageFont.load_default()
    except:
        font_main = font_sub = font_btn = font_icon = ImageFont.load_default()

margin = 24
radius = 42

for p in panels:
    x0, y0 = p["x"] + margin, p["y"] + margin
    x1, y1 = p["x"] + col_w - margin, p["y"] + row_h - margin
    
    # 柔和立體下沉陰影
    draw.rounded_rectangle([x0 + 4, y0 + 6, x1 + 4, y1 + 6], radius=radius, fill=(15, 23, 42, 40))
    # 純白卡片底色 (微透明度高質感)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=p["bg"])
    # 質感鮮明邊框
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=p["border"], width=4)
    
    cx = p["x"] + col_w // 2
    cy = p["y"] + row_h // 2
    
    # 圖示
    draw.text((cx, cy - 100), p["icon"], fill=(30, 41, 59, 255), font=font_icon, anchor="mm")
    
    # 標題與說明
    draw.text((cx, cy + 25), p["title"], fill=p["title_color"], font=font_main, anchor="mm")
    draw.text((cx, cy + 85), p["sub"], fill=p["sub_color"], font=font_sub, anchor="mm")
    
    # 底部精品 Pill 按鈕
    btn_w, btn_h = 320, 68
    by = y1 - 95
    btn_text_color = (255, 255, 255, 255) if p["btn_bg"] == (37, 99, 235, 255) else p["title_color"]
    draw.rounded_rectangle([cx - btn_w//2, by, cx + btn_w//2, by + btn_h], radius=34, fill=p["btn_bg"])
    draw.text((cx, by + btn_h//2), p["btn_text"], fill=btn_text_color, font=font_btn, anchor="mm")

# 轉 RGB
final_composite = bg_img.convert("RGB")

out_static = os.path.join("static", "rich_menu_gourmet_2500x1686.png")
final_composite.save(out_static, quality=98)
print(f"超精美圖文選單已生成: {out_static}")
