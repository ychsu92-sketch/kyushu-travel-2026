# AGENTS.md - AI Agent 協作指南 (For Antigravity & AI Assistants)

歡迎來到本專案！這是一份專為 **Google Antigravity**、**Cursor**、**Claude Code** 等 AI 程式助理設計的專案運作指南。當你在本儲存庫中進行任何開發、維護或修改時，請嚴格遵守以下準則：

---

## 🧭 專案核心架構與職責分配

1. **入口大廳 (Travel Portal) - 3D 浮空政策島**：
   - **生成腳本**：`build_portal.py`
   - **產出檔案**：根目錄 `index.html`（同時也是 GitHub Pages 的 Landing Page）
   - **視覺架構**：
     - 基於 **Three.js r128** + **OrbitControls**。
     - 參考 `https://puma.taipei/heart-island`（沈伯洋政策島）風格：Low-poly 抹茶綠島嶼地表、幾何岩壁、阿蘇火山、黑川溫泉、神社鳥居、櫻島渡輪、8 人座紅色自駕小巴。
     - **Catmull-Rom 3D 曲線巡遊**：4 位角色（阿純、姨丈、阿姨、阿嚕）使用階層式群組模型，沿著 `roadCurve` 散步巡遊，擁有平滑交替擺動的四肢與上下起伏動態。
     - **對話氣泡投射**：使用 `vector.project(camera)` 計算 3D 座標在螢幕上的 2D 像素位置，呈現即時對話框。
   - **修改原則**：當需要調整 3D 島嶼、更換小人物外型/台詞、或新增年度旅行入口時，**必須修改 `build_portal.py` 並執行 `python3 build_portal.py`**，嚴禁直接手動改寫龐大的 `index.html`。

2. **特定年度旅行專案 - 2026 南九州冬季聖誕自駕**：
   - **存放路徑**：`2026 南九州冬季聖誕自駕/`
   - **生成腳本**：`2026 南九州冬季聖誕自駕/build_dashboard.py`
   - **產出檔案**：`2026 南九州冬季聖誕自駕/index.html`
   - **8 大模組**：
     - `schedule`：每日行程時間軸、景點細節、MapCode。
     - `map`：每日移動路線圖、自駕區間地圖。
     - `packing`：行李打包清單、進度條、重設狀態。
     - `tools`：即時折價券與條碼、定位導航、實用工具。
     - `food`：美食推薦、早中晚與宵夜酒吧分類卡片、高亮選取底色。
     - `expenses`：日幣/台幣即時記帳與換算。
     - `drive`：日本雪地自駕安全手冊、交通號誌、事故應急。
     - `memo`：個人離線備忘筆記。
   - **修改原則**：修改行程細節、新增優惠券、調整美食清單時，**修改 `2026 南九州冬季聖誕自駕/build_dashboard.py` 後執行該 Python 腳本**，產出最新的手帳頁面。

---

## 🎨 設計與 UI/UX 規範

- **字體規範**：採用溫暖親切的日系圓體：`Zen Maru Gothic` 與 `M PLUS Rounded 1c`。
- **配色哲學**：
  - 主視覺以冬季聖誕、九州大地色（日式抹茶綠 `#799863`、聖誕暖紅 `#DC2626`、溫泉檜木暖棕 `#7C2D12`、錦江灣海藍 `#0284C7`）為主。
  - 避免刺眼霓虹色或死板的高對比純黑純白，採用柔和低彩度與自然陰影。
- **響應式支援 (RWD)**：所有按鈕、分頁選單、3D 畫布與卡片，必須在 iPhone / Android 直式小螢幕與電腦寬螢幕皆能完美操作。

---

## ⚙️ 常用終端機指令

```bash
# 1. 重新建置入口大廳 (Portal)
python3 build_portal.py

# 2. 重新建置 2026 南九州旅行手帳
python3 "2026 南九州冬季聖誕自駕/build_dashboard.py"

# 3. 本地啟動預覽伺服器
python3 -m http.server 8000
# 瀏覽器打開 http://localhost:8000 即可驗證
```

---

## 🛡️ Git 與發布準則

1. **嚴禁破壞性指令**：不可執行 `git push --force` 覆蓋其他協作者的提交；提交前請先 `git pull --rebase`。
2. **端對端驗證後才交付**：任何修改均須先在本地由 Agent 執行 Python 建置並檢查產出檔案完整性，確認無任何 JavaScript 錯誤後才進行 Git commit。
3. **GitHub Pages 自動更新**：任何推送到 `main` 分支的變更，GitHub Pages 會在 30 秒內自動建置並發布到：
   `https://ychsu92-sketch.github.io/kyushu-travel-2026/`
