import os
from PIL import Image, ImageDraw, ImageFont

# LINE 官方 6 格圖文選單精確規範總尺寸: 2500 x 1686 像素
width, height = 2500, 1686

# 讀取使用者鮮美健康食材照片
user_img_path = r"C:\Users\user\.gemini\antigravity\brain\12189836-d176-48a5-ae5d-5648c48e2e8b\.user_uploaded\media__1784874001311.png"

# 底圖
canvas = Image.new("RGBA", (width, height), color=(240, 247, 255, 255))
if os.path.exists(user_img_path):
    food_photo = Image.open(user_img_path).convert("RGBA")
    food_photo = food_photo.resize((width, height), Image.Resampling.LANCZOS)
    dimmer = Image.new("RGBA", (width, height), (240, 247, 255, 120))
    bg_img = Image.alpha_composite(food_photo, dimmer)
else:
    bg_img = canvas

draw = ImageDraw.Draw(bg_img)

# 精確計算 LINE 官方 6 格紅線對齊邊界
# 欄寬 = 833.33 px，列高 = 843 px
col_w = width // 3     # 833
row_h = height // 2    # 843

panels = [
    {
        "icon": "📷",
        "title": "飲食拍照打卡",
        "sub": "拍照或輸入餐點，AI 秒算熱量與蛋白質",
        "pill": "📷 開始打卡",
        "card_bg": (255, 255, 255, 245),
        "border": (37, 99, 235, 255),
        "title_color": (30, 58, 138, 255),
        "sub_color": (71, 85, 105, 255),
        "pill_bg": (37, 99, 235, 255),
        "pill_text": (255, 255, 255, 255),
        "col": 0, "row": 0
    },
    {
        "icon": "📊",
        "title": "個人健康數據",
        "sub": "7日體重趨勢圖與三大營養素分配",
        "pill": "健康數據看板",
        "card_bg": (255, 255, 255, 245),
        "border": (56, 189, 248, 255),
        "title_color": (12, 74, 110, 255),
        "sub_color": (71, 85, 105, 255),
        "pill_bg": (224, 242, 254, 255),
        "pill_text": (30, 64, 175, 255),
        "col": 1, "row": 0
    },
    {
        "icon": "🍳",
        "title": "智慧健康食譜",
        "sub": "想吃什麼，AI 教你輕鬆上手煮",
        "pill": "🍳 食譜指南",
        "card_bg": (255, 255, 255, 245),
        "border": (251, 146, 60, 255),
        "title_color": (124, 45, 18, 255),
        "sub_color": (71, 85, 105, 255),
        "pill_bg": (254, 237, 213, 255),
        "pill_text": (194, 65, 12, 255),
        "col": 2, "row": 0
    },
    {
        "icon": "🏪",
        "title": "超商減脂攻略",
        "sub": "7-11 / 全家健身原型食物組合",
        "pill": "超商避坑推薦",
        "card_bg": (255, 255, 255, 245),
        "border": (74, 222, 128, 255),
        "title_color": (20, 83, 45, 255),
        "sub_color": (71, 85, 105, 255),
        "pill_bg": (220, 252, 231, 255),
        "pill_text": (21, 128, 61, 255),
        "col": 0, "row": 1
    },
    {
        "icon": "🍲",
        "title": "火鍋便當避坑",
        "sub": "外食湯底醬汁與主食聰明替換",
        "pill": "外食點餐攻略",
        "card_bg": (255, 255, 255, 245),
        "border": (248, 113, 113, 255),
        "title_color": (127, 29, 29, 255),
        "sub_color": (71, 85, 105, 255),
        "pill_bg": (254, 226, 226, 255),
        "pill_text": (185, 28, 28, 255),
        "col": 1, "row": 1
    },
    {
        "icon": "📍",
        "title": "周邊健康外食",
        "sub": "一鍵定位搜尋周邊低卡健康餐廳",
        "pill": "地圖定位搜尋",
        "card_bg": (255, 255, 255, 245),
        "border": (167, 139, 250, 255),
        "title_color": (88, 28, 135, 255),
        "sub_color": (71, 85, 105, 255),
        "pill_bg": (237, 233, 254, 255),
        "pill_text": (126, 34, 206, 255),
        "col": 2, "row": 1
    },
]

# 字型設定
try:
    font_main = ImageFont.truetype("msjh.ttc", 64)
    font_sub = ImageFont.truetype("msjh.ttc", 34)
    font_pill = ImageFont.truetype("msjh.ttc", 36)
    font_icon = ImageFont.truetype("seguiemj.ttf", 120)
except:
    try:
        font_main = ImageFont.truetype("arial.ttf", 64)
        font_sub = font_pill = ImageFont.truetype("arial.ttf", 34)
        font_icon = ImageFont.load_default()
    except:
        font_main = font_sub = font_pill = font_icon = ImageFont.load_default()

# 緊密填滿每格 (邊距僅 6px)，100% 精準對齊 LINE 官方劃分紅線！
margin = 6
radius = 24

for p in panels:
    col = p["col"]
    row = p["row"]
    
    # 計算每格精確座標
    x0 = col * col_w + margin
    y0 = row * row_h + margin
    
    # 最右欄填滿剩餘像素 (確保 2500 滿版)
    x1 = (col + 1) * col_w - margin if col < 2 else width - margin
    y1 = (row + 1) * row_h - margin if row < 1 else height - margin
    
    # 卡片底色與精細邊框
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=p["card_bg"])
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=p["border"], width=4)
    
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    
    # 圖示繪製
    draw.text((cx, cy - 120), p["icon"], fill=(30, 41, 59, 255), font=font_icon, anchor="mm")
    
    # 標題與說明文字
    draw.text((cx, cy + 20), p["title"], fill=p["title_color"], font=font_main, anchor="mm")
    draw.text((cx, cy + 90), p["sub"], fill=p["sub_color"], font=font_sub, anchor="mm")
    
    # 底部 Pill 膠囊按鈕 (適當放大更易辨識)
    pill_w, pill_h = 420, 78
    py = y1 - 110
    draw.rounded_rectangle([cx - pill_w//2, py, cx + pill_w//2, py + pill_h], radius=39, fill=p["pill_bg"])
    draw.text((cx, py + pill_h//2), p["pill"], fill=p["pill_text"], font=font_pill, anchor="mm")

# 轉 RGB 並高品質儲存
final_composite = bg_img.convert("RGB")
out_path = os.path.join("static", "rich_menu_exact_fit_2500x1686.png")
final_composite.save(out_path, quality=98)
print(f"100% 精確對齊 LINE 劃分線之 6 格圖文選單已生成: {out_path}")
