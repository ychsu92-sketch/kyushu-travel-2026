# 2026 南九州冬季聖誕自駕・家族旅行互動手帳與 3D 入口大廳

這是一個以現代 Web 技術打造的家族旅行數位手帳與 2.5D 互動入口大廳專案。專為自駕旅行與親友協作設計，具備依南九州真實海岸線打造的 2.5D 冬季浮空島、4 位家族成員巡遊動畫，以及全功能旅行手帳。

🌐 **線上公開體驗網址：** [https://ychsu92-sketch.github.io/kyushu-travel-2026/](https://ychsu92-sketch.github.io/kyushu-travel-2026/)

---

## 🌟 專案特色

1. **🗾 2.5D 南九州冬日自駕浮空島大廳 (`index.html`)**：
   - 採用 **Three.js WebGL** 依據南九州真實海岸線（熊本、阿蘇、黑川、高千穗、宮崎日南、鹿兒島錦江灣、櫻島活火山與天草群島）打造 2.5D 冬季浮空冒險島。
   - **17 處真實地理位置景點 (`L01`~`L17`)** 與 **9 種動態街景物件 (`P01`~`P09`)**：包含 8 人座紅色雪胎自駕小巴、熊本懷舊路面電車、櫻島渡輪、屋台拉麵攤、溫泉街商店、三毛貓、柴犬與散步路人。
   - **4 位家族成員 (`C1` 阿純、`C2` 姨丈、`C3` 阿姨、`C4` 阿嚕棕熊)** 沿著真實自駕路線巡遊，抵達景點時會下車散步並展現專屬動作（阿純黃毛帽自拍揮手、姨丈戴墨鏡握方向盤、阿姨吃三色烤糰子冒愛心、阿嚕棕熊摸肚子）與各景點專屬對話氣泡。
   - 支援手機與桌機 360° 拖曳旋轉、縮放、冬日飄雪開關，以及點擊人物或景點即時互動。

2. **🚗 2026 南九州冬季聖誕自駕專題手帳 (`2026 南九州冬季聖誕自駕/`)**：
   - **8 大完整功能模組**：
     - 📅 **每日詳細行程**：時間軸、景點資訊、MapCode、導航連結。
     - 🗺️ **每日自駕移動路線地圖**：清楚標記當日自駕路徑與停留點。
     - 🎒 **互動行李清單**：分類勾選、即時打包進度、重置功能。
     - 🎟️ **工具與票券定位**：各種折價券、優惠條碼/QRcode，即點即用。
     - 🍱 **美食與餐廳清單**：早午晚餐與宵夜酒吧色標區隔、點選卡片高亮底色。
     - 💰 **分帳與外幣即時換算**：日圓/台幣快速試算、公費記錄。
     - 🛑 **日本冬季自駕須知**：雪鏈、號誌、加油站與應急電話手冊。
     - 📝 **個人旅行備忘錄**：離線儲存私房筆記。

---

## 🚀 如何使用 Google Antigravity 共同編輯與預覽？

### 1. 取得專案原始碼
```bash
git clone https://github.com/ychsu92-sketch/kyushu-travel-2026.git
cd kyushu-travel-2026
```

### 2. 重新編譯與本地預覽畫廊
專案採用模組化生成器，修改後可透過以下指令重新生成 HTML：
```bash
# 開發與預覽模式（產出 index.html 與單項驗收畫廊 preview.html）
python3 build_portal.py

# 啟動本地預覽伺服器
python3 -m http.server 8000
# 打開 http://localhost:8000/preview.html 可逐一檢視 C1~C4 角色、L01~L17 景點與 P01~P09 物件
```

### 3. 正式發佈與 Push 同步上線 (GitHub Pages)
驗證完成後，執行 `--release` 內嵌並加固保護，推送到 `main` 分支即可自動更新線上網站：
```bash
python3 build_portal.py --release
git add .
git commit -m "feat: 更新南九州 3D 冬日自駕島與旅行手帳"
git push origin main
```

---

## 📂 專案結構地圖

```text
kyushu-travel-2026/
├── AGENTS.md                  # 給 AI Agent (Antigravity) 的專案開發規範手冊
├── README.md                  # 本文件（專案介紹與協作指南）
├── build_portal.py            # 入口大廳與預覽畫廊生成腳本
├── obfuscate_and_protect.py   # 發佈版 JS 混淆與防拆解保護腳本
├── index.html                 # 3D 大廳主頁面 (GitHub Pages 首頁)
├── portal/                    # 3D 島嶼模組化引擎與地理資料
│   ├── data/                  # 南九州真實海岸線與 17 處景點路線 JSON
│   ├── env.js                 # 冬季天空、暖陽陰影、波浪海面、雲朵與飄雪
│   ├── terrain.js             # 2.5D 南九州地形、積雪山脈、道路與市電軌道
│   ├── landmarks.js           # L01~L17 景點 3D 模型與動態特效
│   ├── characters.js          # C1~C4 家族成員模型與專屬動作
│   ├── props.js               # P01~P09 小巴、市電、渡輪、屋台、貓狗與路人
│   ├── island.js              # 大廳主場景組裝與互動控制
│   └── preview.js             # 本地預覽畫廊單項 360° 檢視台
└── 2026 南九州冬季聖誕自駕/     # 2026 九州專案資料夾
    ├── build_dashboard.py     # 九州手帳 HTML 生成腳本 (Tailwind + JS)
    ├── index.html             # 九州手帳完成品
    ├── travel_data_import.xlsx# 行程原始資料表
    ├── sync_from_sheets.py    # Google Sheets 同步腳本
    └── google_sheets_sync_webhook.gs # Google Apps Script Webhook
```
