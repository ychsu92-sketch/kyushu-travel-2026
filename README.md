# 家族旅行互動手帳與 3D 入口大廳 (Travel Portal & Dashboard)

這是一個以現代 Web 技術打造的家族旅行數位手帳與 3D 互動入口大廳專案。專為自駕旅行與親友協作設計，具備沈伯洋政策島風格的 3D 浮空島、小人物巡遊動畫，以及全功能旅行手帳。

🌐 **線上公開體驗網址：** [https://ychsu92-sketch.github.io/kyushu-travel-2026/](https://ychsu92-sketch.github.io/kyushu-travel-2026/)

---

## 🌟 專案特色

1. **🏛️ 3D 政策島風格家族大廳 (`index.html`)**：
   - 採用 **Three.js WebGL** 打造 low-poly 浮空冒險島（阿蘇火山、黑川溫泉桶、櫻島渡輪、神社鳥居與 8 人座紅色自駕小巴）。
   - **4 位 Q 版家族成員沿著環島路徑真實散步巡遊**（手腳自然擺動、上下起伏、轉向面朝行進方向）。
   - 支援手機與桌機 360° 拖曳旋轉、縮放，點擊人物即時彈跳並浮現對話氣泡。
   - 快速跳轉至各年度專屬旅行手帳。

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

## 🚀 如何使用 Google Antigravity 共同編輯？

本專案完全支援 **Google Antigravity**（以及 Cursor、VS Code、Claude Code 等 AI IDE）。

### 1. 取得專案原始碼
```bash
git clone https://github.com/ychsu92-sketch/kyushu-travel-2026.git
cd kyushu-travel-2026
```

### 2. 在 Antigravity 中開啟專案
- 點選 Antigravity 選單 **File ➔ Open Folder**，選擇本專案目錄。
- 專案根目錄已備妥 `AGENTS.md`，你的 AI Agent 會自動閱讀專案規範與編譯腳本，一秒進入狀況！

### 3. 用自然語言指揮 AI 修改
你可以直接在 Antigravity 聊天視窗中輸入自然語言指令：
- 💡 *「我想在 Day 2 晚上新增黑川溫泉街的烤糰子散步行程。」*
- 💡 *「幫我在 3D 島嶼的大廳上新增一個燈塔模型與雪花效果。」*
- 💡 *「美食分頁幫我新增由布院著名的 B-Speak 生乳捲，並放上 Google Maps 連結。」*

### 4. 重新編譯與本地預覽
專案採用 Python 模組化自動生成器，修改後可透過以下指令重新生成 HTML：
```bash
# 重新建置 3D 入口大廳
python3 build_portal.py

# 重新建置南九州旅行手帳
python3 "2026 南九州冬季聖誕自駕/build_dashboard.py"
```
直接點擊生成的 `index.html` 或使用瀏覽器打開即可離線預覽。

### 5. Push 同步上線 (GitHub Pages)
驗證完成後，推送到 `main` 分支即可自動更新線上網站：
```bash
git add .
git commit -m "feat: 更新旅行行程與景點資訊"
git push origin main
```
約 30 秒至 1 分鐘後，GitHub Pages 便會自動同步更新至線上網站！

---

## 📂 專案結構地圖

```text
kyushu-travel-2026/
├── AGENTS.md                  # 給 AI Agent (Antigravity) 的專案開發規範手冊
├── README.md                  # 本文件（專案介紹與協作指南）
├── build_portal.py            # 3D 政策島大廳生成腳本 (Three.js 核心引擎)
├── index.html                 # 3D 政策島大廳主頁面 (GitHub Pages 首頁)
└── 2026 南九州冬季聖誕自駕/     # 2026 九州專案資料夾
    ├── build_dashboard.py     # 九州手帳 HTML 生成腳本 (Tailwind + JS)
    ├── index.html             # 九州手帳完成品
    ├── travel_data_import.xlsx# 行程原始資料表
    ├── sync_from_sheets.py    # Google Sheets 同步腳本
    └── google_sheets_sync_webhook.gs # Google Apps Script Webhook
```

---

## 🤝 參與貢獻與協作規範
- 提交變更前請確保在本地瀏覽器端對端預覽無誤。
- 遵循色彩規範與圓體字型風格（Zen Maru Gothic / M PLUS Rounded 1c）。
- 歡迎透過 Pull Request 或直接 Commit 共同完善家族旅行手帳！
