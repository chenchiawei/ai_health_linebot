import os
from PIL import Image, ImageDraw, ImageFont

# 2500 x 1686 官方標準尺寸
width, height = 2500, 1686

# 極簡舒壓背景：溫馨明亮暖白/極簡日系高質感 (#F8FAF9)
img = Image.new("RGBA", (width, height), color=(248, 250, 249, 255))
draw = ImageDraw.Draw(img)

col_w = width // 3
row_h = height // 2

# 6 大極簡低視覺壓力卡片配色與內容
panels = [
    {
        "icon": "🥗", 
        "title": "飲食拍照打卡", 
        "sub": "照片 / 文字熱量估算", 
        "card_bg": (230, 244, 234, 255),  # 薄荷柔綠
        "border_color": (166, 218, 185, 255),
        "text_color": (22, 101, 52, 255),
        "sub_color": (74, 122, 94, 255),
        "x": 0, "y": 0
    },
    {
        "icon": "📊", 
        "title": "個人健康數據", 
        "sub": "7日體重趨勢圖表", 
        "card_bg": (232, 242, 252, 255),  # 晴空柔藍
        "border_color": (180, 212, 242, 255),
        "text_color": (26, 86, 138, 255),
        "sub_color": (70, 114, 153, 255),
        "x": col_w, "y": 0
    },
    {
        "icon": "📍", 
        "title": "周邊外食地圖", 
        "sub": "傳送定位推薦健康餐廳", 
        "card_bg": (254, 243, 226, 255),  # 暖杏柔橙
        "border_color": (247, 216, 170, 255),
        "text_color": (170, 90, 18, 255),
        "sub_color": (160, 110, 60, 255),
        "x": col_w * 2, "y": 0
    },
    {
        "icon": "🏪", 
        "title": "超商減脂攻略", 
        "sub": "7-11 / 全家原型食物組合", 
        "card_bg": (234, 245, 237, 255),  # 森林柔綠
        "border_color": (175, 220, 190, 255),
        "text_color": (30, 100, 55, 255),
        "sub_color": (80, 125, 95, 255),
        "x": 0, "y": row_h
    },
    {
        "icon": "🍲", 
        "title": "火鍋便當避坑", 
        "sub": "湯底與醬汁熱量替換秘訣", 
        "card_bg": (252, 232, 232, 255),  # 珊瑚柔紅
        "border_color": (245, 185, 185, 255),
        "text_color": (170, 45, 45, 255),
        "sub_color": (155, 85, 85, 255),
        "x": col_w, "y": row_h
    },
    {
        "icon": "⚖️", 
        "title": "設定體重目標", 
        "sub": "更新 BMR / TDEE 數據", 
        "card_bg": (240, 235, 250, 255),  # 薰衣草紫
        "border_color": (205, 190, 235, 255),
        "text_color": (95, 50, 160, 255),
        "sub_color": (115, 85, 165, 255),
        "x": col_w * 2, "y": row_h
    },
]

# 字型大小與樣式
try:
    font_main = ImageFont.truetype("msjh.ttc", 62)
    font_sub = ImageFont.truetype("msjh.ttc", 36)
    font_icon = ImageFont.truetype("seguiemj.ttf", 100)
except:
    try:
        font_main = ImageFont.truetype("arial.ttf", 62)
        font_sub = ImageFont.truetype("arial.ttf", 36)
        font_icon = ImageFont.load_default()
    except:
        font_main = font_sub = font_icon = ImageFont.load_default()

# 較大卡片間距 (30px)，有效降低視覺壓迫感
margin = 28
radius = 42

for p in panels:
    x0, y0 = p["x"] + margin, p["y"] + margin
    x1, y1 = p["x"] + col_w - margin, p["y"] + row_h - margin
    
    # 1. 畫圓角微陰影 (降低硬質感)
    shadow_offset = 6
    draw.rounded_rectangle(
        [x0 + shadow_offset, y0 + shadow_offset, x1 + shadow_offset, y1 + shadow_offset], 
        radius=radius, 
        fill=(220, 225, 222, 120)
    )
    
    # 2. 畫主卡片 (柔和清新馬卡龍底色)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=p["card_bg"])
    
    # 3. 畫微精緻邊框
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=p["border_color"], width=4)
    
    cx = p["x"] + col_w // 2
    cy = p["y"] + row_h // 2
    
    # 文字與 Icon 對齊
    draw.text((cx, cy - 95), p["icon"], fill=(30, 41, 59, 255), font=font_icon, anchor="mm")
    draw.text((cx, cy + 30), p["title"], fill=p["text_color"], font=font_main, anchor="mm")
    draw.text((cx, cy + 100), p["sub"], fill=p["sub_color"], font=font_sub, anchor="mm")

# 轉 RGB
final_img = Image.new("RGB", (width, height), (248, 250, 249))
final_img.paste(img, (0, 0), mask=img)

# 儲存
out_path = os.path.join("static", "rich_menu_minimal_2500x1686.png")
final_img.save(out_path, quality=98)
print(f"清新低視覺壓力圖文選單已生成: {out_path}")
