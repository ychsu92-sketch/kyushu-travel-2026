# AGENTS.md - AI Agent 協作指南 (For Antigravity & AI Assistants)

歡迎來到本專案！這是一份專為 **Google Antigravity**、**Cursor**、**Claude Code** 等 AI 程式助理設計的專案運作指南。當你在本儲存庫中進行任何開發、維護或修改時，請嚴格遵守以下準則：

---

## 🧭 專案核心架構與職責分配

1. **入口大廳 (Travel Portal) - 2.5D 南九州冬日自駕浮空島**：
   - **生成腳本**：`build_portal.py`
   - **模組化 3D 引擎目錄**：`portal/`
     - `portal/data/kyushu_coast.json`：簡化自真實南九州地理邊界（含熊本、宮崎、鹿兒島薩摩與大隅半島、錦江灣、櫻島活火山與天草群島）。
     - `portal/data/route.json`：17 處真實地理位置景點 (`L01`~`L17`)、自駕巡遊路線與各景點角色專屬台詞。
     - `portal/env.js`：12 月冬季晴空漸層圓頂、冬日低角度暖陽與真實柔和長陰影、動態波浪海面、緩飄雲朵與可開關飄雪。
     - `portal/terrain.js`：2.5D 多層次低彩度冬季地貌（海岸浪花環、暖沙灘、檜木暖棕岩壁斷面、枯草抹茶綠草地、覆雪山脈、環島公路與市電軌道）。
     - `portal/landmarks.js`：17 處南九州景點 Low-poly 3D 模型與動態特效（火山白煙、黑川湯明竹燈與蒸氣、高千穗小舟、鹿兒島天文館聖誕樹等）。
     - `portal/characters.js`：4 位家族成員（`C1` 阿純、`C2` 姨丈、`C3` 阿姨、`C4` 阿嚕棕熊）精細模型與專屬動作狀態機。
     - `portal/props.js`：8 人座紅色自駕小巴、熊本路面電車、櫻島渡輪、屋台拉麵攤、溫泉商店、三毛貓、柴犬、散步路人與雪人（`P01`~`P09`）。
     - `portal/island.js`：場景組裝、自駕與景點停留動畫迴圈、Raycaster 點擊互動與 2D 對話氣泡投射。
     - `portal/preview.js`：本地專屬 `preview.html` 單項 360° 旋轉驗收畫廊控制器。
   - **產出檔案**：根目錄 `index.html`（GitHub Pages 首頁）與本地 `preview.html`（已列入 `.gitignore`）。
   - **修改原則**：
     - 開發與預覽時執行 `python3 build_portal.py`，產出未混淆的 `index.html` 與 `preview.html` 供瀏覽器除錯與使用者驗收。
     - 使用者確認無誤準備發佈前，執行 `python3 build_portal.py --release` 將所有模組與資料內嵌回 `index.html` 並自動執行 `obfuscate_and_protect.py` 混淆加固。

2. **特定年度旅行專案 - 2026 南九州冬季聖誕自駕**：
   - **存放路徑**：`2026 南九州冬季聖誕自駕/`
   - **生成腳本**：`2026 南九州冬季聖誕自駕/build_dashboard.py`
   - **產出檔案**：`2026 南九州冬季聖誕自駕/index.html`
   - **8 大模組**：`schedule`、`map`、`packing`、`tools`、`food`、`expenses`、`drive`、`memo`。
   - **修改原則**：修改行程細節、新增優惠券、調整美食清單時，**修改 `2026 南九州冬季聖誕自駕/build_dashboard.py` 後執行該 Python 腳本**，產出最新的手帳頁面。

---

## 🎨 設計與 UI/UX 規範

- **字體規範**：採用溫暖親切的日系圓體：`Zen Maru Gothic` 與 `M PLUS Rounded 1c`。
- **配色哲學**：
  - 主視覺以冬季聖誕、九州大地色（日式抹茶綠 `#799863`、聖誕暖紅 `#DC2626`、溫泉檜木暖棕 `#8C583A`、錦江灣海藍 `#3B82A6`）為主。
  - 避免刺眼霓虹色或死板的高對比純黑純白，採用柔和低彩度與自然陰影。
- **響應式支援 (RWD)**：所有按鈕、分頁選單、3D 畫布與卡片，必須在 iPhone / Android 直式小螢幕與電腦寬螢幕皆能完美操作。

---

## ⚙️ 常用終端機指令

```bash
# 1. 開發模式建置入口大廳與 preview.html 預覽畫廊
python3 build_portal.py

# 2. 正式發佈模式建置（內嵌 + JS 混淆與防拆解保護）
python3 build_portal.py --release

# 3. 重新建置 2026 南九州旅行手帳
python3 "2026 南九州冬季聖誕自駕/build_dashboard.py"

# 4. 本地啟動預覽伺服器
python3 -m http.server 8000
# 瀏覽器打開 http://localhost:8000/preview.html 或 http://localhost:8000 即可驗證
```

---

## 🛡️ Git 與發布準則

1. **嚴禁破壞性指令**：不可執行 `git push --force` 覆蓋其他協作者的提交；提交前請先 `git pull --rebase`。
2. **端對端驗證與預覽核可後才交付**：任何修改均須先在本地由 Agent 執行 Python 建置、檢查無任何 JavaScript 錯誤，並讓使用者透過預覽確認後才進行 Git commit 與 push。
3. **GitHub Pages 自動更新**：任何推送到 `main` 分支的變更，GitHub Pages 會在 30 秒內自動建置並發布到：
   `https://ychsu92-sketch.github.io/kyushu-travel-2026/`
