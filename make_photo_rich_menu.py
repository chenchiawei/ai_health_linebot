import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 1. 讀取使用者上傳的新鮮健康食材照片
user_img_path = r"C:\Users\user\.gemini\antigravity\brain\12189836-d176-48a5-ae5d-5648c48e2e8b\.user_uploaded\media__1784874001311.png"

# LINE 官方標準尺寸 2500 x 1686
target_w, target_h = 2500, 1686

if os.path.exists(user_img_path):
    bg_img = Image.open(user_img_path).convert("RGBA")
    # 調整大小填滿 2500x1686
    bg_img = bg_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
else:
    # 備用底色
    bg_img = Image.new("RGBA", (target_w, target_h), (240, 247, 255, 255))

# 建立半透明玻璃質感 overlay
overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

col_w = target_w // 3
row_h = target_h // 2

# 6 格精緻高質感半透明膠囊卡片
panels = [
    {"icon": "📷", "title": "飲食拍照打卡", "sub": "AI 秒算熱量蛋白質", "x": 0, "y": 0},
    {"icon": "📊", "title": "個人健康數據", "sub": "7日體重趨勢與圖表", "x": col_w, "y": 0},
    {"icon": "🍳", "title": "智慧健康食譜", "sub": "AI 專屬烹飪指南", "x": col_w * 2, "y": 0},
    {"icon": "🏪", "title": "超商減脂攻略", "sub": "7-11/全家黃金組合", "x": 0, "y": row_h},
    {"icon": "🍲", "title": "火鍋便當避坑", "sub": "湯底醬汁聰明替換", "x": col_w, "y": row_h},
    {"icon": "📍", "title": "周邊外食地圖", "sub": "定位推薦低卡餐廳", "x": col_w * 2, "y": row_h},
]

# 字型設定
try:
    font_main = ImageFont.truetype("msjh.ttc", 62)
    font_sub = ImageFont.truetype("msjh.ttc", 34)
    font_icon = ImageFont.truetype("seguiemj.ttf", 100)
except:
    try:
        font_main = ImageFont.truetype("arial.ttf", 62)
        font_sub = ImageFont.truetype("arial.ttf", 34)
        font_icon = ImageFont.load_default()
    except:
        font_main = font_sub = font_icon = ImageFont.load_default()

margin = 22
radius = 40

for p in panels:
    x0, y0 = p["x"] + margin, p["y"] + margin
    x1, y1 = p["x"] + col_w - margin, p["y"] + row_h - margin
    
    # 畫半透明高質感白色玻璃卡片 (White Glassmorphism)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=(255, 255, 255, 205))
    # 畫極細精緻藍白色邊框
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=(255, 255, 255, 255), width=5)
    
    cx = p["x"] + col_w // 2
    cy = p["y"] + row_h // 2
    
    # 繪製 Icon、標題與次要說明
    draw.text((cx, cy - 90), p["icon"], fill=(30, 41, 59, 255), font=font_icon, anchor="mm")
    draw.text((cx, cy + 30), p["title"], fill=(15, 23, 42, 255), font=font_main, anchor="mm")
    draw.text((cx, cy + 100), p["sub"], fill=(51, 65, 85, 255), font=font_sub, anchor="mm")

# 組合背景與文字 Overlay
final_composite = Image.alpha_composite(bg_img, overlay).convert("RGB")

# 儲存
out_static = os.path.join("static", "rich_menu_photo_2500x1686.png")
final_composite.save(out_static, quality=98)
print(f"基於使用者照片之 6 格圖文選單已生成: {out_static}")
