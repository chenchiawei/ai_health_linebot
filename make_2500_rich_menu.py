import os
from PIL import Image, ImageDraw, ImageFont

# 官方大型圖文選單精確規範尺寸: 2500 x 1686 像素
width, height = 2500, 1686
img = Image.new("RGBA", (width, height), color=(15, 23, 42, 255)) # 時尚深色背景 #0F172A
draw = ImageDraw.Draw(img)

# 2 列 3 欄 網格計算
col_w = width // 3
row_h = height // 2

panels = [
    {"icon": "🍱", "title": "飲食拍照打卡", "sub": "AI 估算熱量", "bg": (16, 185, 129, 230), "x": 0, "y": 0},
    {"icon": "📊", "title": "個人健康數據", "sub": "7日體重趨勢", "bg": (14, 165, 233, 230), "x": col_w, "y": 0},
    {"icon": "📍", "title": "周邊外食地圖", "sub": "定位推薦美食", "bg": (245, 158, 11, 230), "x": col_w * 2, "y": 0},
    {"icon": "🏪", "title": "超商減脂攻略", "sub": "7-11/全家組合", "bg": (34, 197, 94, 230), "x": 0, "y": row_h},
    {"icon": "🍲", "title": "火鍋便當避坑", "sub": "聰明替換醬汁", "bg": (239, 68, 68, 230), "x": col_w, "y": row_h},
    {"icon": "⚖️", "title": "設定體重目標", "sub": "更新 TDEE", "bg": (139, 92, 246, 230), "x": col_w * 2, "y": row_h},
]

# 字型設定
try:
    font_main = ImageFont.truetype("msjh.ttc", 65)
    font_sub = ImageFont.truetype("msjh.ttc", 38)
    font_icon = ImageFont.truetype("seguiemj.ttf", 110)
except:
    try:
        font_main = ImageFont.truetype("arial.ttf", 65)
        font_sub = ImageFont.truetype("arial.ttf", 38)
        font_icon = ImageFont.load_default()
    except:
        font_main = font_sub = font_icon = ImageFont.load_default()

margin = 20
for p in panels:
    x0, y0 = p["x"] + margin, p["y"] + margin
    x1, y1 = p["x"] + col_w - margin, p["y"] + row_h - margin
    
    # 繪製圓角卡片
    draw.rounded_rectangle([x0, y0, x1, y1], radius=36, fill=p["bg"])
    
    cx = p["x"] + col_w // 2
    cy = p["y"] + row_h // 2
    
    # 圖示與標題文字繪製
    draw.text((cx, cy - 100), p["icon"], fill=(255, 255, 255, 255), font=font_icon, anchor="mm")
    draw.text((cx, cy + 30), p["title"], fill=(255, 255, 255, 255), font=font_main, anchor="mm")
    draw.text((cx, cy + 105), p["sub"], fill=(241, 245, 249, 210), font=font_sub, anchor="mm")

# 轉回 RGB
final_img = Image.new("RGB", (width, height), (15, 23, 42))
final_img.paste(img, (0, 0), mask=img)

# 同時存到 static 與使用者桌面 (Desktop)
path_static = os.path.join("static", "rich_menu_2500x1686.png")
path_desktop = r"C:\Users\user\Desktop\rich_menu_2500x1686.png"

final_img.save(path_static, quality=95)
try:
    final_img.save(path_desktop, quality=95)
    print(f"圖片已成功生成並儲存到桌面: {path_desktop}")
except Exception as e:
    print(f"靜態檔已儲存: {path_static}")
