import os
from PIL import Image, ImageDraw, ImageFont

# LINE 大型 4 格圖文選單標準規範尺寸: 2500 x 1686 像素
width, height = 2500, 1686

# 清新明亮日系極簡底色 (#F8FAF9)
img = Image.new("RGBA", (width, height), color=(248, 250, 249, 255))
draw = ImageDraw.Draw(img)

# 2 列 2 欄 網格計算
col_w = width // 2
row_h = height // 2

panels = [
    {
        "icon": "📷",
        "tag": "AI PHOTO & TEXT LOG",
        "title": "飲食拍照打卡",
        "sub": "拍照上傳或文字輸入，AI 秒算熱量與蛋白質",
        "card_bg": (236, 253, 245, 255),    # 柔和清新綠
        "border_color": (167, 243, 208, 255),
        "text_color": (6, 78, 59, 255),
        "sub_color": (74, 122, 94, 255),
        "tag_bg": (52, 211, 153, 255),
        "x": 0, "y": 0
    },
    {
        "icon": "📊",
        "tag": "HEALTH DASHBOARD",
        "title": "個人健康數據看板",
        "sub": "7日體重下降趨勢圖與三大營養素圓餅圖",
        "card_bg": (240, 249, 255, 255),    # 柔和晴空藍
        "border_color": (186, 230, 253, 255),
        "text_color": (12, 74, 110, 255),
        "sub_color": (70, 114, 153, 255),
        "tag_bg": (56, 189, 248, 255),
        "x": col_w, "y": 0
    },
    {
        "icon": "🍱",
        "tag": "OUTING DINING GUIDE",
        "title": "外食點餐避坑指南",
        "sub": "7-11、火鍋、便當與 SUBWAY 健身低卡組合",
        "card_bg": (254, 243, 199, 255),    # 柔和暖杏黃
        "border_color": (253, 230, 138, 255),
        "text_color": (120, 53, 15, 255),
        "sub_color": (160, 110, 60, 255),
        "tag_bg": (251, 191, 36, 255),
        "x": 0, "y": row_h
    },
    {
        "icon": "📍",
        "tag": "NEARBY RESTAURANTS",
        "title": "附近健康外食地圖",
        "sub": "一鍵傳送目前定位，精準推薦周邊健康餐廳",
        "card_bg": (240, 253, 244, 255),    # 柔和翡翠綠
        "border_color": (187, 247, 208, 255),
        "text_color": (20, 83, 45, 255),
        "sub_color": (80, 125, 95, 255),
        "tag_bg": (74, 222, 128, 255),
        "x": col_w, "y": row_h
    },
]

# 字型設定
try:
    font_main = ImageFont.truetype("msjh.ttc", 68)
    font_sub = ImageFont.truetype("msjh.ttc", 36)
    font_tag = ImageFont.truetype("arialbd.ttf", 28)
    font_icon = ImageFont.truetype("seguiemj.ttf", 130)
except:
    try:
        font_main = ImageFont.truetype("arial.ttf", 68)
        font_sub = ImageFont.truetype("arial.ttf", 36)
        font_tag = font_icon = ImageFont.load_default()
    except:
        font_main = font_sub = font_tag = font_icon = ImageFont.load_default()

# 寬敞的大邊距 (32px)，創造極佳呼吸感
margin = 32
radius = 48

for p in panels:
    x0, y0 = p["x"] + margin, p["y"] + margin
    x1, y1 = p["x"] + col_w - margin, p["y"] + row_h - margin
    
    # 柔和立體陰影
    draw.rounded_rectangle([x0 + 6, y0 + 8, x1 + 6, y1 + 8], radius=radius, fill=(225, 230, 227, 130))
    # 卡片底色
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=p["card_bg"])
    # 卡片細邊框
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=p["border_color"], width=5)
    
    cx = p["x"] + col_w // 2
    cy = p["y"] + row_h // 2
    
    # 小英文 Tag 標籤
    tag_w = 320
    tag_h = 48
    draw.rounded_rectangle(
        [cx - tag_w//2, y0 + 45, cx + tag_w//2, y0 + 45 + tag_h], 
        radius=16, 
        fill=p["tag_bg"]
    )
    draw.text((cx, y0 + 45 + tag_h//2), p["tag"], fill=(255, 255, 255), font=font_tag, anchor="mm")
    
    # 圖示繪製
    draw.text((cx, cy - 40), p["icon"], fill=(30, 41, 59, 255), font=font_icon, anchor="mm")
    
    # 標題與說明文字
    draw.text((cx, cy + 75), p["title"], fill=p["text_color"], font=font_main, anchor="mm")
    draw.text((cx, cy + 145), p["sub"], fill=p["sub_color"], font=font_sub, anchor="mm")

# 轉 RGB
final_img = Image.new("RGB", (width, height), (248, 250, 249))
final_img.paste(img, (0, 0), mask=img)

# 同時存到 static 與桌面
path_static = os.path.join("static", "rich_menu_4grid_2500x1686.png")
final_img.save(path_static, quality=98)
print(f"黃金 4 格極簡圖文選單已生成: {path_static}")
