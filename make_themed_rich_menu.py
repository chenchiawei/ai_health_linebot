import os
from PIL import Image, ImageDraw, ImageFont

# 2500 x 1686 官方標準尺寸
width, height = 2500, 1686

# 背景：極簡舒壓白底 (#F8FAF9)
img = Image.new("RGBA", (width, height), color=(248, 250, 249, 255))
draw = ImageDraw.Draw(img)

col_w = width // 3
row_h = height // 2

# 6 大特色主題繪圖卡片
panels = [
    {
        "icon": "🍱",
        "tag": "PHOTO MEAL LOG",
        "title": "飲食拍照打卡",
        "sub": "拍下餐點，AI秒算蛋白質與熱量",
        "card_bg": (236, 253, 245, 255),    # 清新綠
        "border_color": (167, 243, 208, 255),
        "text_color": (6, 78, 59, 255),
        "tag_bg": (52, 211, 153, 255),
        "x": 0, "y": 0
    },
    {
        "icon": "📊",
        "tag": "HEALTH DASHBOARD",
        "title": "個人健康數據",
        "sub": "7日體重趨勢與營養素分配圓餅圖",
        "card_bg": (240, 249, 255, 255),    # 天空藍
        "border_color": (186, 230, 253, 255),
        "text_color": (12, 74, 110, 255),
        "tag_bg": (56, 189, 248, 255),
        "x": col_w, "y": 0
    },
    {
        "icon": "📍",
        "tag": "MAP EXPLORER",
        "title": "周邊外食地圖",
        "sub": "一鍵定位搜尋附近低卡健康餐廳",
        "card_bg": (254, 243, 199, 255),    # 暖陽黃
        "border_color": (253, 230, 138, 255),
        "text_color": (120, 53, 15, 255),
        "tag_bg": (251, 191, 36, 255),
        "x": col_w * 2, "y": 0
    },
    {
        "icon": "🏪",
        "tag": "7-11 & CONVENIENCE",
        "title": "超商減脂攻略",
        "sub": "7-11與全家高蛋白原型食物黃金組合",
        "card_bg": (240, 253, 244, 255),    # 翡翠綠
        "border_color": (187, 247, 208, 255),
        "text_color": (20, 83, 45, 255),
        "tag_bg": (74, 222, 128, 255),
        "x": 0, "y": row_h
    },
    {
        "icon": "🍲",
        "tag": "HOTPOT & BENTO",
        "title": "火鍋便當避坑",
        "sub": "外食族湯底、醬汁與菜單聰明替換法",
        "card_bg": (254, 242, 242, 255),    # 暖心紅
        "border_color": (254, 202, 202, 255),
        "text_color": (127, 29, 29, 255),
        "tag_bg": (248, 113, 113, 255),
        "x": col_w, "y": row_h
    },
    {
        "icon": "⚖️",
        "tag": "TDEE & GOALS",
        "title": "設定體重目標",
        "sub": "隨時更新身高體重與增肌減脂目標",
        "card_bg": (245, 243, 255, 255),    # 夢幻紫
        "border_color": (221, 214, 254, 255),
        "text_color": (88, 28, 135, 255),
        "tag_bg": (167, 139, 250, 255),
        "x": col_w * 2, "y": row_h
    },
]

# 字型設定
try:
    font_main = ImageFont.truetype("msjh.ttc", 60)
    font_sub = ImageFont.truetype("msjh.ttc", 32)
    font_tag = ImageFont.truetype("arialbd.ttf", 26)
    font_icon = ImageFont.truetype("seguiemj.ttf", 100)
except:
    try:
        font_main = ImageFont.truetype("arial.ttf", 60)
        font_sub = ImageFont.truetype("arial.ttf", 32)
        font_tag = font_icon = ImageFont.load_default()
    except:
        font_main = font_sub = font_tag = font_icon = ImageFont.load_default()

margin = 24
radius = 38

for p in panels:
    x0, y0 = p["x"] + margin, p["y"] + margin
    x1, y1 = p["x"] + col_w - margin, p["y"] + row_h - margin
    
    # 輕柔陰影
    draw.rounded_rectangle([x0 + 4, y0 + 6, x1 + 4, y1 + 6], radius=radius, fill=(225, 230, 227, 120))
    # 主卡片
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=p["card_bg"])
    # 邊框
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=p["border_color"], width=4)
    
    cx = p["x"] + col_w // 2
    cy = p["y"] + row_h // 2
    
    # 小英文字主題標籤 Tag
    tag_w = 260
    tag_h = 42
    draw.rounded_rectangle(
        [cx - tag_w//2, y0 + 35, cx + tag_w//2, y0 + 35 + tag_h], 
        radius=14, 
        fill=p["tag_bg"]
    )
    draw.text((cx, y0 + 35 + tag_h//2), p["tag"], fill=(255, 255, 255), font=font_tag, anchor="mm")
    
    # 大主題圖示
    draw.text((cx, cy - 35), p["icon"], fill=(30, 41, 59, 255), font=font_icon, anchor="mm")
    
    # 標題與說明
    draw.text((cx, cy + 65), p["title"], fill=p["text_color"], font=font_main, anchor="mm")
    draw.text((cx, cy + 125), p["sub"], fill=(100, 116, 139), font=font_sub, anchor="mm")

# 轉 RGB
final_img = Image.new("RGB", (width, height), (248, 250, 249))
final_img.paste(img, (0, 0), mask=img)

# 儲存
out_path = os.path.join("static", "rich_menu_themed_2500x1686.png")
final_img.save(out_path, quality=98)
print(f"主題插畫風圖文選單已生成: {out_path}")
