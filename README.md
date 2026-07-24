# 🥗 AI 健康 & 減重外食 LINE Bot

專為**健身與減重外食族**打造的 AI LINE 官方帳號！
結合 **FastAPI + LINE Messaging API + Gemini 2.5 多模態 AI + Google Places API**，自動試算 BMR/TDEE、拍照辨識飲食熱量、記錄體重體脂變動，並在您沒時間下廚時，結合 Google 地圖搜尋周邊健康餐點並提供 AI 點餐攻略！

---

## 📁 專案架構概覽

```text
ai_health_linebot/
├── main.py                  # FastAPI 主程式與 LINE Webhook 事件處理
├── config.py                # 環境變數與 API 密鑰管理
├── database.py              # SQLite 資料庫連線
├── models.py                # User, HealthLog, MealLog 資料表定義
├── test_local.py            # 本地獨立測試腳本 (免連 LINE 即可測試邏輯)
├── services/
│   ├── gemini_service.py    # Gemini AI 核心：BMR/TDEE 計算、飲食辨識、點餐建議
│   ├── maps_service.py      # Google Maps 搜尋周邊健康外食
│   └── line_service.py      # LINE Flex Message 卡片繪製與 Quick Reply
├── .env.example             # 環境變數設定範本
└── requirements.txt         # 依賴套件清單
```

---

## 🚀 快速開始指南

### 第一步：安裝 Python 依賴套件
請開啟終端機 (Terminal / PowerShell)，進入本專案目錄並執行：
```bash
pip install -r requirements.txt
```

### 第二步：快速驗證本地邏輯 (無需設定 LINE)
直接執行測試腳本，驗證 BMR/TDEE 計算、Gemini 模擬與餐廳搜尋：
```bash
python test_local.py
```

---

## 📲 連接 LINE 官方帳號與手機測試

### 1. 複製設定檔 `.env`
將 `.env.example` 複製一份並重新命名為 `.env`：
在 `.env` 中填入您的金鑰：
* `LINE_CHANNEL_SECRET`: 來自 LINE Developers Console
* `LINE_CHANNEL_ACCESS_TOKEN`: 來自 LINE Developers Console
* `GEMINI_API_KEY`: 來自 [Google AI Studio](https://aistudio.google.com/)

### 2. 啟動本機伺服器
```bash
python main.py
```
伺服器將在 `http://127.0.0.1:8000` 啟動。

### 3. 使用 ngrok 開啟外網 HTTPS 通道
在另一個終端機視窗執行：
```bash
ngrok http 8000
```
取得 ngrok 產生的 HTTPS 網址（例如：`https://xxxx.ngrok-free.app`）。

### 4. 設定 LINE Webhook
1. 進入 [LINE Developers Console](https://developers.line.biz/)。
2. 找到您的 Messaging API Channel。
3. 將 **Webhook URL** 設為：`https://xxxx.ngrok-free.app/webhook`
4. 開啟 **Use Webhook** 開關。

---

## 💬 常用指令與體驗

1. **基本資料設定與熱量目標試算**
   - 傳送：`設定 175cm 72kg 16% 減脂`
   - 機器人自動計算 BMR/TDEE，並回傳建議熱量與蛋白質上限！

2. **飲食拍照打卡 / 文字記錄**
   - 直接**拍照上傳餐點**（如便當或火鍋照片），或輸入 `吃了雞腿便當`
   - 機器人自動解析卡路里、三大營養素，並給予營養師評語！

3. **周邊健康外食推薦 (Google Maps)**
   - 在 LINE 聊天室點擊「**傳送位置**」
   - 機器人自動搜尋家/公司附近的健康店家，並根據今日剩餘熱量給予專屬**點餐攻略**！

4. **查詢健康狀態**
   - 傳送：`查看狀態` 或 `我的資料`
   - 機器人回傳當前熱量與蛋白質進度卡片！
