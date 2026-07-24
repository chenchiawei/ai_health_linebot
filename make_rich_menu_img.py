import os
from PIL import Image, ImageDraw, ImageFont

# LINE 官方規定大型 6 格圖文選單尺寸：2500 x 1686 像素
width, height = 2500, 1686
img = Image.new("RGB", (width, height), color="#F4F6F7")
draw = ImageDraw.Draw(img)

# 2 列 3 欄 網格計算
col_w = width // 3
row_h = height // 2

panels = [
    {"title": "🍱 飲食打卡", "bg": "#1DB446", "text_color": "#FFFFFF", "x": 0, "y": 0},
    {"title": "📊 健康數據", "bg": "#2C3E50", "text_color": "#FFFFFF", "x": col_w, "y": 0},
    {"title": "📍 附近外食", "bg": "#E67E22", "text_color": "#FFFFFF", "x": col_w * 2, "y": 0},
    {"title": "🏪 7-11攻略", "bg": "#27AE60", "text_color": "#FFFFFF", "x": 0, "y": row_h},
    {"title": "🍲 火鍋便當", "bg": "#C0392B", "text_color": "#FFFFFF", "x": col_w, "y": row_h},
    {"title": "⚖️ 設定體重", "bg": "#2980B9", "text_color": "#FFFFFF", "x": col_w * 2, "y": row_h},
]

# 試著載入中文字型
try:
    font = ImageFont.truetype("msjh.ttc", 90) # 微軟正黑體
except:
    try:
        font = ImageFont.truetype("arial.ttf", 90)
    except:
        font = ImageFont.load_default()

for p in panels:
    x0, y0 = p["x"], p["y"]
    x1, y1 = x0 + col_w, y0 + row_h
    
    # 畫出底色區塊 (留 6px 邊框分隔)
    draw.rectangle([x0 + 4, y0 + 4, x1 - 4, y1 - 4], fill=p["bg"])
    
    # 繪製文字標籤
    text = p["title"]
    # 使用 draw.text (對齊中心)
    draw.text((x0 + col_w // 2, y0 + row_h // 2), text, fill=p["text_color"], font=font, anchor="mm")

# 儲存至 static 目錄
out_path = os.path.join("static", "rich_menu_2500x1686.png")
img.save(out_path)
print(f"Rich Menu 圖片已生成: {out_path}")
