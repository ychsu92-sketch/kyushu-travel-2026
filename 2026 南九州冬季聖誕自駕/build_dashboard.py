#!/usr/bin/env python3
"""
生活小秘書 - 旅行儀表板 (Winter & Christmas Cozy Journal 風格)
用法: python3 build_dashboard.py
新增：九州手繪探索地圖分頁 (Map Tab)、修復行李檢查「全部重來」殘留刪除線錯誤
已修復：使用 json.dumps 注入 MAP_LANDMARKS，徹底杜絕單引號跳脫引發之 JS SyntaxError
"""

import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 19 處關鍵地標數據 (由 Python 管理並經 json.dumps 安全序列化，防範單引號衝突)
MAP_LANDMARKS = [
    {
        "id": "kmj_airport",
        "shortName": "🛫 熊本機場",
        "name": "熊本機場 KMJ (阿蘇空港)",
        "labelPos": "top",
        "category": "transit",
        "categoryName": "門戶機場",
        "day": "Day 1 & Day 7",
        "icon": "🛫",
        "x": 430,
        "y": 375,
        "color": "#2563eb",
        "desc": "2023全新落成航廈，木造質感溫馨，全九州名產與免稅店雲集，華航 CI194/195 直飛起降點！",
        "tips": "回程提早 2 小時抵達，免稅店採買時間充裕。"
    },
    {
        "id": "hotel_viainn",
        "shortName": "🏨 Via Inn",
        "name": "Via Inn Prime Kumamoto (辛島町)",
        "labelPos": "left",
        "category": "hotel",
        "categoryName": "第1晚住宿",
        "day": "Day 1 (12/22 二)",
        "icon": "🏡",
        "x": 325,
        "y": 390,
        "color": "#9333ea",
        "desc": "下樓即是新市街與下通熱鬧商圈，備有天然大浴場，舒緩第一天航程疲勞。",
        "tips": "鄰近辛島町路面電車站與機場利木津巴士站牌。"
    },
    {
        "id": "kumamoto_castle",
        "shortName": "🏯 熊本城",
        "name": "日本三大名城「熊本城」＆ 城彩苑",
        "labelPos": "top",
        "category": "sight",
        "categoryName": "歷史名勝＆小吃",
        "day": "Day 7 (12/28 一)",
        "icon": "🏯",
        "x": 345,
        "y": 340,
        "color": "#dc2626",
        "desc": "加藤清正建造之堅固名城，登上浴火重生天守閣俯瞰市區；城彩苑品嚐熱騰騰現炸馬肉可樂餅與芥末蓮藕。",
        "tips": "使用路面電車一日券即可輕鬆抵達。"
    },
    {
        "id": "suizenji",
        "shortName": "🍵 水前寺",
        "name": "水前寺成趣園 (江戶池泉回遊庭園)",
        "labelPos": "right",
        "category": "sight",
        "categoryName": "日式庭園",
        "day": "Day 7 (12/28 一)",
        "icon": "🍵",
        "x": 395,
        "y": 420,
        "color": "#16a34a",
        "desc": "仿富士山形狀的優美築山與清澈阿蘇伏流水湧泉池，可在古今傳授之間茶屋品嚐抹茶。",
        "tips": "清幽寧靜，適合全家漫步拍照。"
    },
    {
        "id": "aso_crater",
        "shortName": "🌋 阿蘇火山",
        "name": "阿蘇草千里之濱 ＆ 中岳火山口",
        "labelPos": "right",
        "category": "sight",
        "categoryName": "自然火山絕景",
        "day": "Day 2 (12/23 三)",
        "icon": "🌋",
        "x": 475,
        "y": 345,
        "color": "#ea580c",
        "desc": "遼闊草千里與阿蘇火山中岳火山口，白煙裊裊的大自然磅礡氣勢！",
        "tips": "山頂體感溫度接近零度，保暖防風厚外套必備。"
    },
    {
        "id": "daikanbo",
        "shortName": "🏔️ 大觀峰",
        "name": "大觀峰展望台 (阿蘇五嶽全景)",
        "labelPos": "top",
        "category": "sight",
        "categoryName": "遼闊展望景點",
        "day": "Day 2 (12/23 三)",
        "icon": "🏔️",
        "x": 495,
        "y": 275,
        "color": "#16a34a",
        "desc": "360度俯瞰阿蘇五嶽與巨大破火山口地形，被譽為宛如「釋迦涅槃像」的雄偉山景。",
        "tips": "停車場步行至展望台約 5 分鐘，步道平緩好走。"
    },
    {
        "id": "hotel_kurokawa",
        "shortName": "♨️ 黑川溫泉",
        "name": "黑川溫泉-山彥旅館 (やまびこ) 含早餐",
        "labelPos": "right",
        "category": "hotel",
        "categoryName": "第2晚黑川仙人風呂秘湯 (含朝食)",
        "day": "Day 2 (12/23 三)",
        "icon": "♨️",
        "x": 545,
        "y": 250,
        "color": "#9333ea",
        "desc": "沿著筑後川幽靜溪谷漫步，欣賞冬季限定竹燈祭「湯明」；入住仙人風呂享受日式晨光朝食。",
        "tips": "冬季山區道路可能有殘雪結冰，雪胎休旅車自駕最安心。"
    },
    {
        "id": "kamishikimi",
        "shortName": "🌲 上色見神社",
        "name": "上色見熊野座神社 (神隱之森)",
        "labelPos": "left",
        "category": "sight",
        "categoryName": "森林能量景點",
        "day": "Day 3 (12/24 四)",
        "icon": "🌲",
        "x": 505,
        "y": 400,
        "color": "#16a34a",
        "desc": "近百座長滿青苔的石燈籠與參天杉木參道，宛如踏進宮崎駿動畫神隱少女的世界。",
        "tips": "石階偶有濕滑，穿著防滑好走平底鞋。"
    },
    {
        "id": "takachiho_gorge",
        "shortName": "🚣 高千穗峽",
        "name": "高千穗峽谷划船 ＆ 真名井瀑布",
        "labelPos": "right",
        "category": "sight",
        "categoryName": "神話峽谷名勝",
        "day": "Day 3 (12/24 四)",
        "icon": "🚣",
        "x": 570,
        "y": 415,
        "color": "#0284c7",
        "desc": "泛舟於柱狀玄武岩絕壁之下仰望名瀑真名井瀑布；搭乘粉紅敞篷小火車行駛在百米高鐵道橋上吹泡泡！",
        "tips": "划船需提前 1 週於官網整點預約！"
    },
    {
        "id": "hotel_seagaia",
        "shortName": "🏖️ 宮崎公寓",
        "name": "宮崎 Seagaia Forest Condominiums",
        "labelPos": "left",
        "category": "hotel",
        "categoryName": "第3晚海景渡假公寓",
        "day": "Day 3 (12/24 四)",
        "icon": "🏖️",
        "x": 675,
        "y": 535,
        "color": "#9333ea",
        "desc": "寬敞海景渡假公寓，4人合住大客廳與廚房，平安夜享用入口即化宮崎牛鐵板燒！",
        "tips": "大幅分散車程，抵達溫暖的太平洋海濱。"
    },
    {
        "id": "aoshima",
        "shortName": "🌊 青島神社",
        "name": "青島神社 ＆ 鬼之洗衣板",
        "labelPos": "right",
        "category": "sight",
        "categoryName": "海蝕地質與結緣",
        "day": "Day 4 (12/25 五)",
        "icon": "🌊",
        "x": 685,
        "y": 595,
        "color": "#0284c7",
        "desc": "被大自然雕琢出如洗衣板般的奇岩圍繞之神聖小島，島上還有帶來好運的黃色幸福郵筒。",
        "tips": "聖誕節早晨沿著日南海岸散步格外清爽。"
    },
    {
        "id": "sun_messe",
        "shortName": "🗿 摩艾石像",
        "name": "Sun Messe 日南 (復活節島摩艾石像)",
        "labelPos": "left",
        "category": "sight",
        "categoryName": "授權摩艾巨石像",
        "day": "Day 4 (12/25 五)",
        "icon": "🗿",
        "x": 675,
        "y": 645,
        "color": "#d97706",
        "desc": "獲復活節島正式授權複製的 7 尊巨型摩艾石像，背靠蔚藍太平洋祈求好運！",
        "tips": "面朝海洋祈福，拍照極具異國情調。"
    },
    {
        "id": "udo_jingu",
        "shortName": "⛩️ 鵜戶神宮",
        "name": "鵜戶神宮 (絕壁海蝕洞穴奇景)",
        "labelPos": "right",
        "category": "sight",
        "categoryName": "海崖奇岩神宮",
        "day": "Day 4 (12/25 五)",
        "icon": "⛩️",
        "x": 670,
        "y": 695,
        "color": "#dc2626",
        "desc": "建於懸崖巨岩洞穴內的朱紅神宮，向海中靈石龜甲凹槽投擲「運玉」祈福！",
        "tips": "男生左手投擲、女生右手投擲。"
    },
    {
        "id": "hotel_perch",
        "shortName": "🏡 鹿兒島公寓",
        "name": "鹿兒島 Perch's Apartment 303 (連住2晚)",
        "labelPos": "left",
        "category": "hotel",
        "categoryName": "第4-5晚市區公寓",
        "day": "Day 4 & Day 5",
        "icon": "🏡",
        "x": 365,
        "y": 685,
        "color": "#9333ea",
        "desc": "市區舒適公寓連住兩晚免搬行李，下樓即達天文館商圈，品嚐壽庵黑豚涮涮鍋與吾愛人居酒屋。",
        "tips": "欣賞天文館冬季浪漫璀璨彩燈點燈。"
    },
    {
        "id": "sakurajima",
        "shortName": "🌋 櫻島火山",
        "name": "櫻島活火山 ＆ 櫻島渡輪 ＆ 溶岩足湯",
        "labelPos": "right",
        "category": "sight",
        "categoryName": "世界著名活火山",
        "day": "Day 5 (12/26 六)",
        "icon": "🌋",
        "x": 455,
        "y": 655,
        "color": "#ea580c",
        "desc": "開車直接開上渡輪（15分鐘船程），漫步溶岩渚遊步道享受天然火山足湯，登展望台感受火山氣勢！",
        "tips": "渡輪班次極多（每15-20分鐘一班），船上烏龍麵很有名。"
    },
    {
        "id": "senganen",
        "shortName": "🏯 仙巖園",
        "name": "大名庭園「仙巖園」＆ 城山展望台",
        "labelPos": "top",
        "category": "sight",
        "categoryName": "薩摩別墅與海灣夕照",
        "day": "Day 5 (12/26 六)",
        "icon": "🏯",
        "x": 375,
        "y": 635,
        "color": "#16a34a",
        "desc": "薩摩藩主島津氏別墅，將櫻島與錦江灣當作庭園山水的雄偉借景；登上城山俯瞰夕照。",
        "tips": "園內必吃現烤兩棒餅 (Jambo Mochi)。"
    },
    {
        "id": "kirishima_jingu",
        "shortName": "⛩️ 霧島神宮",
        "name": "南九州最大神宮「國寶 霧島神宮」",
        "labelPos": "top",
        "category": "sight",
        "categoryName": "南九州國寶神宮",
        "day": "Day 6 (12/27 日)",
        "icon": "⛩️",
        "x": 470,
        "y": 570,
        "color": "#dc2626",
        "desc": "祭祀日本神話天孫降臨之主角，朱紅色宏偉建築被譽為西之日光，神聖莊嚴。",
        "tips": "境內八百年巨大神木聳立，充滿靈氣。"
    },
    {
        "id": "hitoyoshi_unagi",
        "shortName": "🍱 人吉鰻魚",
        "name": "人吉百年炭火鰻魚名店「上村うなぎや」",
        "labelPos": "right",
        "category": "sight",
        "categoryName": "傳奇美食名店",
        "day": "Day 6 (12/27 日)",
        "icon": "🍱",
        "x": 425,
        "y": 490,
        "color": "#d97706",
        "desc": "百年老醬汁炭火現烤，外皮焦香微脆、肉質肥厚綿密，日本老饕讚不絕口的人吉必吃鰻魚飯！",
        "tips": "建議 12:00 前抵達排隊登記。"
    },
    {
        "id": "hotel_amanek",
        "shortName": "♨️ 熊本AMANEK",
        "name": "HOTEL AMANEK Kumamoto (辛島町)",
        "labelPos": "bottom",
        "category": "hotel",
        "categoryName": "第6晚市區溫泉飯店",
        "day": "Day 6 (12/27 日)",
        "icon": "♨️",
        "x": 355,
        "y": 410,
        "color": "#9333ea",
        "desc": "新市街核心商圈，頂樓有無邊際景觀露天溫泉大浴場，市區還車後享用勝烈亭黑豚炸豬排！",
        "tips": "整理 6 天戰利品行李，準備回國。"
    }
]

def load_data():
    current_trip_file = os.path.join(DATA_DIR, 'current_trip.json')
    history_file = os.path.join(DATA_DIR, 'trips_history.json')
    
    with open(current_trip_file, 'r', encoding='utf-8') as f:
        trip = json.load(f)
        
    with open(history_file, 'r', encoding='utf-8') as f:
        history = json.load(f)
        
    return trip, history

def build():
    trip, history = load_data()
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    expense_sum = trip.get('expense_summary', {})
    total_spent_twd = expense_sum.get('total_spent_twd', 91992.06)
    per_person_avg = expense_sum.get('per_person_avg_twd', round(total_spent_twd / 4, 1))
    flight_cost_twd = trip.get('flights', {}).get('outbound', {}).get('flight_cost_twd', 34515)

    packing = trip['packing_checklist']
    all_items = packing['documents'] + packing['carry_on'] + packing['checked_bag']
    total_items_count = len(all_items)
    checked_items_count = sum(1 for item in all_items if item.get('checked', False))
    packing_pct = round((checked_items_count / total_items_count) * 100) if total_items_count > 0 else 0

    # JSON 安全序列化
    trip_json_str = json.dumps(trip, ensure_ascii=False)
    history_json_str = json.dumps(history, ensure_ascii=False)
    landmarks_json_str = json.dumps(MAP_LANDMARKS, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="南九州手帳">
    <meta name="theme-color" content="#dc2626">
    <title>🎄 2026 南九州聖誕冬季自駕旅行手帳 ❄️</title>
    <!-- 家族專屬品牌識別 Favicon & App Icons -->
    <link rel="icon" type="image/x-icon" href="./favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="./favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="./favicon-16x16.png">
    <link rel="apple-touch-icon" sizes="180x180" href="./apple-touch-icon.png">
    <link rel="shortcut icon" href="./favicon.ico">
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Zen Maru Gothic + M PLUS Rounded 1c -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&family=Noto+Sans+TC:wght@400;500;700;900&family=Zen+Maru+Gothic:wght@400;500;700;900&display=swap" rel="stylesheet">
    <!-- Canvas Confetti -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['"Zen Maru Gothic"', '"M PLUS Rounded 1c"', '"Noto Sans TC"', 'sans-serif'],
                    }},
                    colors: {{
                        xmas: {{
                            red: '#c92a2a',
                            berry: '#a61e4d',
                            green: '#2b6cb0',
                            pine: '#1e5128',
                            forest: '#2d6a4f',
                            gold: '#f59f00',
                            snow: '#f8fafc',
                            cookie: '#d97706',
                            warmBg: '#fbf9f5'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{
            background-color: #fbf9f5;
            background-image: 
                radial-gradient(#e8dfd8 1.2px, transparent 1.2px),
                radial-gradient(#e8dfd8 1.2px, #fbf9f5 1.2px);
            background-size: 30px 30px;
            background-position: 0 0, 15px 15px;
            color: #3e322f;
            font-family: 'Zen Maru Gothic', 'M PLUS Rounded 1c', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }}

        #snow-canvas {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 40;
        }}

        .cute-card {{
            background: #ffffff;
            border: 2px solid #ede4dc;
            border-radius: 26px;
            box-shadow: 0 10px 24px -6px rgba(160, 120, 100, 0.12), 0 2px 6px rgba(160, 120, 100, 0.06);
            transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}
        .cute-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 14px 30px -6px rgba(160, 120, 100, 0.16);
        }}

        .washi-tape {{
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%) rotate(-1deg);
            width: 110px;
            height: 22px;
            background: rgba(201, 42, 42, 0.7);
            border-left: 3px dashed rgba(255, 255, 255, 0.85);
            border-right: 3px dashed rgba(255, 255, 255, 0.85);
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
            z-index: 20;
            pointer-events: none;
        }}
        .washi-tape-green {{
            background: rgba(45, 106, 79, 0.75);
            transform: translateX(-50%) rotate(1.5deg);
        }}
        .washi-tape-gold {{
            background: rgba(245, 159, 0, 0.75);
            transform: translateX(-50%) rotate(-1.5deg);
        }}

        .xmas-tab-btn {{
            background: #ffffff;
            border: 2px solid #ecdcd3;
            color: #6b5852;
            border-radius: 9999px;
            padding: 6px 12px;
            font-size: 13px;
            font-weight: 800;
            transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.03);
            white-space: nowrap;
        }}
        @media (max-width: 640px) {{
            .xmas-tab-btn {{
                padding: 6px 8px;
                font-size: 12px;
                gap: 2px;
            }}
        }}
        .xmas-tab-btn:hover {{
            background: #fff5f5;
            border-color: #ffc9c9;
            color: #c92a2a;
            transform: scale(1.02);
        }}
        .xmas-tab-btn.active {{
            background: linear-gradient(135deg, #c92a2a 0%, #a61e4d 100%);
            border-color: #c92a2a;
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(201, 42, 42, 0.3);
            transform: scale(1.02);
        }}

        .polaroid-card {{
            background: #ffffff;
            border: 1px solid #ebd9cc;
            padding: 14px 14px 20px 14px;
            border-radius: 20px;
            box-shadow: 0 6px 16px rgba(180, 140, 120, 0.12);
        }}

        .sticky-note {{
            background: #fffdf0;
            border: 2px dashed #fcd34d;
            border-radius: 22px;
            position: relative;
        }}

        .cute-pill {{
            border-radius: 9999px;
            padding: 3px 10px;
            font-size: 11px;
            font-weight: 800;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            white-space: nowrap;
            flex-shrink: 0;
        }}

        .soft-countdown {{
            background: #ffffff;
            border: 2px solid #fed7aa;
            border-radius: 16px;
            padding: 6px 12px;
            min-width: 54px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(251, 146, 60, 0.12);
        }}

                .map-pin {{
            cursor: pointer;
        }}
        .map-pin .pin-circle {{
            transition: r 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), stroke-width 0.25s ease, filter 0.25s ease, fill 0.25s ease;
        }}
        .map-pin .pin-icon {{
            transition: font-size 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            dominant-baseline: central;
            text-anchor: middle;
            pointer-events: none;
            user-select: none;
        }}
        /* 懸停回饋：輕微放大 */
        .map-pin:hover .pin-circle {{
            r: 18px;
            stroke-width: 3.5px;
            filter: drop-shadow(0 4px 10px rgba(220, 38, 38, 0.35));
        }}
        .map-pin:hover .pin-icon {{
            font-size: 15px;
        }}

        /* 點選選中：彈出放大 (顯著放大至 23px，圖標 17px，精緻白底紅圈與大陰影) */
        .map-pin.active .pin-circle {{
            r: 23px;
            stroke-width: 4.5px;
            fill: #fff5f5;
            filter: drop-shadow(0 8px 18px rgba(220, 38, 38, 0.55));
        }}
        .map-pin.active .pin-icon {{
            font-size: 17px;
        }}

        /* 選中時的雷達擴散光圈 */
        .map-pin .pin-ripple {{
            display: none;
            pointer-events: none;
        }}
        .map-pin.active .pin-ripple {{
            display: block;
            animation: pinRippleAnim 2s infinite cubic-bezier(0.1, 0.8, 0.3, 1);
        }}
        @keyframes pinRippleAnim {{
            0% {{
                r: 16px;
                opacity: 0.85;
                stroke-width: 3px;
            }}
            100% {{
                r: 38px;
                opacity: 0;
                stroke-width: 0.5px;
            }}
        }}

        /* 地名膠囊標籤：原本的字不要顯示 (預設完全隱藏) */
        .map-pin .pin-badge {{
            display: none;
            pointer-events: none;
            transform-box: fill-box;
            transform-origin: center;
        }}

        /* 點了圖示後：彈出放大動態 (Spring Bounce Pop-In) */
        .map-pin.active .pin-badge {{
            display: block;
            animation: popInBadge 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }}

        @keyframes popInBadge {{
            0% {{
                opacity: 0;
                transform: scale(0.3);
            }}
            70% {{
                opacity: 1;
                transform: scale(1.14);
            }}
            100% {{
                opacity: 1;
                transform: scale(1);
            }}
        }}

        /* 全顯模式 (若使用者需要一鍵全部展開) */
        #map-pins-group.show-all-labels .map-pin .pin-badge {{
            display: block;
            animation: none;
            opacity: 1;
            transform: scale(1);
        }}

        /* 路線動畫與條碼樣式 */
        @keyframes dash-flow {{
            to {{
                stroke-dashoffset: -30;
            }}
        }}
        .route-flowing {{
            animation: dash-flow 1.2s linear infinite;
        }}
        .barcode-container {{
            font-family: monospace;
            letter-spacing: 2px;
        }}

    </style>
</head>
<body class="antialiased flex flex-col min-h-screen">

    <canvas id="snow-canvas"></canvas>

    <header class="bg-white/90 backdrop-blur-md sticky top-0 z-50 border-b-2 border-red-100 px-3 sm:px-6 lg:px-8 py-2.5 sm:py-3 shadow-sm">
        <div class="max-w-7xl mx-auto flex items-center justify-between flex-wrap gap-2 sm:gap-3">
            <div class="flex items-center gap-2.5 sm:gap-3 min-w-0">
                <div class="w-10 h-10 sm:w-11 sm:h-11 rounded-2xl shrink-0 bg-white border border-stone-200 flex items-center justify-center p-1 shadow-md shadow-stone-100 overflow-hidden">
                    <img src="./family_logo.png" alt="Kyushu Travel Logo" class="w-full h-full object-contain">
                </div>
                <div class="min-w-0">
                    <div class="flex items-center gap-2">
                        <span class="cute-pill bg-red-100 text-red-700 border border-red-200 text-[10px] sm:text-xs">
                            🎅 冬日聖誕度假 · 家族自駕日記
                        </span>
                        <span class="text-xs text-stone-300 hidden sm:inline">|</span>
                        <span class="text-xs text-stone-500 font-medium hidden sm:inline" id="top-clock">🇯🇵 熊本即時時間</span>
                    </div>
                    <h1 class="text-xs sm:text-base md:text-lg font-black text-stone-800 flex flex-wrap items-center gap-1.5 sm:gap-2 mt-0.5 truncate sm:overflow-visible">
                        <span>{trip['title']}</span>
                        <span class="inline-flex items-center gap-1 text-[10px] sm:text-[11px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200 shrink-0 whitespace-nowrap">
                            <span class="text-xs">♨️</span>
                            <span>聖誕溫泉季</span>
                        </span>
                    </h1>
                </div>
            </div>

            <div class="flex items-center gap-1.5 sm:gap-2.5">
                <a href="../index.html" class="px-2 sm:px-3 py-1.5 rounded-full bg-stone-100 hover:bg-stone-200 text-stone-700 border border-stone-200 text-xs font-bold flex items-center gap-1 transition shadow-sm" title="回到旅程入口大廳">
                    <span>🏠</span>
                    <span class="hidden sm:inline">旅程大廳</span>
                </a>

                <button onclick="scrollToTabNav()" class="px-2.5 sm:px-3.5 py-1.5 rounded-full bg-gradient-to-r from-red-600 via-rose-600 to-red-500 hover:from-red-700 hover:to-rose-700 text-white font-black text-xs flex items-center gap-1.5 transition-all shadow-md shadow-red-300 ring-2 ring-red-200 hover:scale-105 active:scale-95" title="快速回到 8 大分頁選單">
                    <span>📋</span>
                    <span class="whitespace-nowrap">分頁選單</span>
                </button>

                <button onclick="toggleSnow()" id="snow-toggle-btn" class="px-2.5 sm:px-3.5 py-1.5 rounded-full bg-sky-100 hover:bg-sky-200 text-sky-700 border border-sky-200 text-xs font-bold flex items-center gap-1 transition shadow-sm">
                    <span>❄️</span>
                    <span id="snow-btn-text">下雪中</span>
                </button>

                <button onclick="fireChristmasCheer()" class="px-2.5 sm:px-3.5 py-1.5 rounded-full bg-red-100 hover:bg-red-200 text-red-700 border border-red-200 text-xs font-bold flex items-center gap-1 transition shadow-sm">
                    <span>🎁</span>
                    <span class="hidden sm:inline">聖誕驚喜！</span>
                    <span class="sm:hidden">驚喜</span>
                </button>

                <a href="https://docs.google.com/spreadsheets/d/1P4niaKfXpHnrlVkiexFmxa2Q0U7kwOvj6yUINn--WNo/edit?usp=sharing" target="_blank" class="px-2.5 sm:px-3.5 py-1.5 rounded-full bg-amber-100 hover:bg-amber-200 text-amber-700 border border-amber-200 text-xs font-bold flex items-center gap-1 transition shadow-sm">
                    <span>📊</span>
                    <span class="hidden sm:inline">試算表</span>
                </a>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 lg:px-8 py-6 flex-1 w-full space-y-6 relative z-10">

        <!-- HERO 看板 -->
        <div class="cute-card p-6 lg:p-8 relative overflow-hidden bg-gradient-to-br from-white via-red-50/30 to-amber-50/40 border-2 border-red-200 shadow-xl">
            <div class="washi-tape washi-tape-gold"></div>

            <div class="relative z-10 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
                <div class="space-y-3 max-w-2xl">
                    <div class="flex flex-wrap items-center gap-2">
                        <span class="cute-pill bg-red-100 text-red-700 border border-red-200">
                            🎄 聖誕自駕巡迴 (12/22 ~ 12/28)
                        </span>
                        <span class="cute-pill bg-emerald-100 text-emerald-700 border border-emerald-200">
                            ♨️ 阿蘇火山・黑川秘湯・霧島神宮
                        </span>
                        <span class="cute-pill bg-sky-100 text-sky-700 border border-sky-200">
                            ❄️ 8人座大空間休旅車・備妥雪胎
                        </span>
                    </div>

                    <h2 class="text-2xl sm:text-3xl lg:text-4xl font-black tracking-tight text-stone-800 flex items-center gap-2">
                        <span>🎅</span>
                        {trip['title']}
                    </h2>

                    <p class="text-stone-600 text-xs sm:text-sm leading-relaxed bg-white/80 p-3.5 rounded-2xl border border-red-100 shadow-sm">
                        📍 <strong>自駕路線：</strong>{trip['subtitle']}
                    </p>

                    <div class="text-xs text-stone-500 flex flex-wrap items-center gap-3 font-medium">
                        <span>📅 旅行日期：<strong class="text-stone-800">{trip['start_date']} 至 {trip['end_date']} (7 天 6 夜)</strong></span>
                        <span>•</span>
                        <span>✈️ 直飛航班：<strong class="text-red-600">華航 CI194 (14:30 桃機 T2 ➔ 17:30 熊本 KMJ) ⇄ CI195</strong></span>
                    </div>
                </div>

                <div class="w-full lg:w-auto bg-white/95 border-2 border-red-200 rounded-3xl p-5 flex flex-col items-center justify-center gap-3 shadow-lg shadow-red-100/60">
                    <div class="text-xs font-black tracking-wider text-red-600 uppercase flex items-center gap-1.5">
                        <span class="animate-bounce">🦌</span>
                        <span>聖誕啟程倒數計時！</span>
                    </div>

                    <div class="flex items-center gap-2 sm:gap-2.5" id="countdown-container">
                        <div class="soft-countdown bg-red-50 border-red-200">
                            <div class="text-2xl sm:text-3xl font-black text-red-600 font-mono" id="cd-days">--</div>
                            <div class="text-[10px] text-red-400 font-bold uppercase">天</div>
                        </div>
                        <div class="text-lg font-black text-stone-300">:</div>
                        <div class="soft-countdown bg-amber-50 border-amber-200">
                            <div class="text-2xl sm:text-3xl font-black text-amber-600 font-mono" id="cd-hours">--</div>
                            <div class="text-[10px] text-amber-500 font-bold uppercase">時</div>
                        </div>
                        <div class="text-lg font-black text-stone-300">:</div>
                        <div class="soft-countdown bg-emerald-50 border-emerald-200">
                            <div class="text-2xl sm:text-3xl font-black text-emerald-600 font-mono" id="cd-mins">--</div>
                            <div class="text-[10px] text-emerald-500 font-bold uppercase">分</div>
                        </div>
                        <div class="text-lg font-black text-stone-300">:</div>
                        <div class="soft-countdown bg-sky-50 border-sky-200">
                            <div class="text-2xl sm:text-3xl font-black text-sky-500 font-mono" id="cd-secs">--</div>
                            <div class="text-[10px] text-sky-400 font-bold uppercase">秒</div>
                        </div>
                    </div>

                    <div class="text-[11px] text-stone-500 font-medium text-center">
                        2026/12/22 (二) 14:30 華航 CI194 直飛熊本 🛫
                    </div>
                </div>
            </div>
        </div>

        <!-- 導航功能按鈕列 (手機版嚴格4x4兩排對齊・電腦版橫向整齊展開) -->
        <nav id="main-tab-nav" class="grid grid-cols-4 sm:flex sm:flex-wrap items-center justify-between gap-1.5 sm:gap-2 pb-2 border-b-2 border-red-100 scroll-mt-20">
            <button onclick="openTab('itinerary')" id="tab-btn-itinerary" class="xmas-tab-btn active w-full sm:flex-1 min-w-0 px-1 py-2 sm:px-3 text-[11px] sm:text-xs">
                <span>🗺️</span> 行程
            </button>
            <button onclick="openTab('map')" id="tab-btn-map" class="xmas-tab-btn w-full sm:flex-1 min-w-0 px-1 py-2 sm:px-3 text-[11px] sm:text-xs">
                <span>📍</span> 地圖
            </button>
            <button onclick="openTab('restaurants')" id="tab-btn-restaurants" class="xmas-tab-btn w-full sm:flex-1 min-w-0 px-1 py-2 sm:px-3 text-[11px] sm:text-xs">
                <span>🍱</span> 美食
            </button>
            <button onclick="openTab('costs')" id="tab-btn-costs" class="xmas-tab-btn w-full sm:flex-1 min-w-0 px-1 py-2 sm:px-3 text-[11px] sm:text-xs">
                <span>👛</span> 記帳
            </button>
            <button onclick="openTab('stays')" id="tab-btn-stays" class="xmas-tab-btn w-full sm:flex-1 min-w-0 px-1 py-2 sm:px-3 text-[11px] sm:text-xs">
                <span>🏨</span> 住宿/預約
            </button>
            <button onclick="openTab('stamps')" id="tab-btn-stamps" class="xmas-tab-btn w-full sm:flex-1 min-w-0 px-1 py-2 sm:px-3 text-[11px] sm:text-xs">
                <span>🎴</span> 集章巡禮
            </button>
            <button onclick="openTab('checklist')" id="tab-btn-checklist" class="xmas-tab-btn w-full sm:flex-1 min-w-0 px-1 py-2 sm:px-3 text-[11px] sm:text-xs">
                <span>🎒</span> 行李
            </button>
            <button onclick="openTab('tools')" id="tab-btn-tools" class="xmas-tab-btn w-full sm:flex-1 min-w-0 px-1 py-2 sm:px-3 text-[11px] sm:text-xs">
                <span>🎟️</span> 優惠/工具
            </button>
        </nav>

        <!-- TAB 1: 行程時間軸 -->
        <section id="tab-content-itinerary" class="tab-content space-y-6">
            <div class="flex items-center gap-2.5 overflow-x-auto pb-1" id="day-selector-bar"></div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 space-y-4">
                    <div class="cute-card p-6 relative border-2 border-red-100">
                        <div class="washi-tape washi-tape-gold"></div>

                        <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b-2 border-red-50 gap-3">
                            <div>
                                <div class="flex items-center gap-2">
                                    <span class="cute-pill bg-red-100 text-red-700" id="current-day-badge">DAY 1</span>
                                    <span class="cute-pill bg-emerald-100 text-emerald-700" id="current-day-feasibility">🟢 可行性絕佳</span>
                                </div>
                                <h3 class="text-xl font-black text-stone-800 mt-2" id="current-day-theme">當日主題</h3>
                                <p class="text-xs text-stone-500 mt-1 flex flex-wrap items-center gap-2 font-medium">
                                    <span id="current-day-date">📅 日期</span>
                                    <span>•</span>
                                    <span id="current-day-route">🗺️ 路線</span>
                                </p>
                            </div>
                            <div class="bg-amber-50 border border-amber-200 rounded-2xl px-3.5 py-2 text-xs text-amber-800 font-bold flex items-center gap-2 shadow-sm">
                                <span>🚗</span>
                                <span id="current-day-drive">預估車程</span>
                            </div>
                        </div>

                        <!-- 隨行資訊微型膠囊列 (方案B) ＆ 雙模式視圖切換 (方案A) -->
                        <div class="mt-4 pt-3 border-t border-stone-100 flex flex-wrap items-center justify-between gap-2.5">
                            <!-- 隨行膠囊按鈕群 (點擊開合對應面板) -->
                            <div class="flex flex-wrap items-center gap-1.5 text-xs font-bold" id="day-capsule-bar">
                                <!-- 膠囊 1: 天氣與穿搭 -->
                                <button type="button" onclick="toggleSubPanel('weather')" id="btn-capsule-weather" class="px-3 py-1.5 rounded-xl bg-white hover:bg-sky-50 text-slate-700 hover:text-sky-700 border border-stone-200 hover:border-sky-300 font-bold transition flex items-center gap-1.5 shadow-2xs">
                                    <span id="capsule-weather-icon">⛅</span>
                                    <span id="capsule-weather-text">5°C ~ 13°C</span>
                                    <span class="text-[10px] text-stone-400 font-mono" id="capsule-weather-arrow">▾</span>
                                </button>

                                <!-- 膠囊 2: 今日自駕停車 -->
                                <button type="button" onclick="toggleSubPanel('parking')" id="btn-capsule-parking" class="px-3 py-1.5 rounded-xl bg-white hover:bg-emerald-50 text-slate-700 hover:text-emerald-700 border border-stone-200 hover:border-emerald-300 font-bold transition flex items-center gap-1.5 shadow-2xs">
                                    <span>🅿️</span>
                                    <span>停車場 (<span id="capsule-parking-count">0</span>)</span>
                                    <span class="text-[10px] text-stone-400 font-mono" id="capsule-parking-arrow">▾</span>
                                </button>

                                <!-- 膠囊 3: 今日三餐與宵夜 -->
                                <button type="button" onclick="toggleSubPanel('meals')" id="btn-capsule-meals" class="px-3 py-1.5 rounded-xl bg-white hover:bg-amber-50 text-slate-700 hover:text-amber-700 border border-stone-200 hover:border-amber-300 font-bold transition flex items-center gap-1.5 shadow-2xs">
                                    <span>🍱</span>
                                    <span>美饌提案</span>
                                    <span class="text-[10px] text-stone-400 font-mono" id="capsule-meals-arrow">▾</span>
                                </button>

                                <!-- 膠囊 4: 臨時加點 -->
                                <button type="button" onclick="toggleSubPanel('custom')" id="btn-capsule-custom" class="px-3 py-1.5 rounded-xl bg-white hover:bg-rose-50 text-slate-700 hover:text-rose-700 border border-stone-200 hover:border-rose-300 font-bold transition flex items-center gap-1.5 shadow-2xs">
                                    <span>➕</span>
                                    <span>臨時加點</span>
                                    <span class="text-[10px] text-stone-400 font-mono" id="capsule-custom-arrow">▾</span>
                                </button>
                            </div>

                            <!-- 模式切換按鈕：長輩清爽 vs 自駕全配 (方案A) -->
                            <div class="flex items-center gap-1 bg-stone-100 p-1 rounded-2xl border border-stone-200 text-xs font-black shrink-0">
                                <button type="button" onclick="setDashboardViewMode('clean')" id="btn-mode-clean" class="px-2.5 py-1 rounded-xl transition flex items-center gap-1 bg-white text-stone-800 shadow-2xs">
                                    <span>🌿</span> 清爽閱讀
                                </button>
                                <button type="button" onclick="setDashboardViewMode('driver')" id="btn-mode-driver" class="px-2.5 py-1 rounded-xl transition flex items-center gap-1 text-stone-500 hover:text-stone-800">
                                    <span>🚗</span> 自駕全配
                                </button>
                            </div>
                        </div>

                        <!-- 隨選收納面板區 (預設乾淨收合，點擊對應膠囊平滑展開) -->
                        <div id="subpanels-wrapper" class="space-y-2 mt-2">
                            <!-- 面板 1: 天氣與穿搭 -->
                            <div id="panel-weather" class="hidden p-4 rounded-2xl bg-gradient-to-r from-sky-50/90 via-blue-50/50 to-indigo-50/60 border border-sky-200/90 shadow-2xs space-y-2.5 text-xs">
                                <div class="flex flex-wrap items-center justify-between gap-2">
                                    <div class="flex items-center gap-2.5">
                                        <span id="day-weather-icon" class="text-2xl drop-shadow-xs">⛅</span>
                                        <div>
                                            <div class="flex items-center gap-2">
                                                <span id="day-weather-city" class="text-xs font-black text-slate-800">熊本市區</span>
                                                <span id="day-weather-condition" class="cute-pill bg-sky-100 text-sky-800 font-bold text-[11px]">晴時多雲</span>
                                                <span id="day-weather-temp" class="text-xs font-mono font-black text-rose-600 bg-white px-2 py-0.5 rounded-md border border-rose-200 shadow-2xs">5°C ~ 13°C</span>
                                            </div>
                                            <div class="text-[11px] text-slate-500 font-medium mt-0.5" id="day-weather-feeling">涼冷乾爽・早晚溫差大 ｜ 降水機率：10%</div>
                                        </div>
                                    </div>
                                    <button type="button" onclick="openTab('checklist')" class="px-2.5 py-1 rounded-xl bg-white hover:bg-sky-100 text-sky-700 border border-sky-200 text-[11px] font-bold transition flex items-center gap-1 shadow-2xs">
                                        <span>🧳</span> 7 天天氣穿搭指南 ↗
                                    </button>
                                </div>
                                <div class="text-[11px] text-slate-700 bg-white/85 p-2.5 rounded-xl border border-sky-100/80 flex items-start gap-1.5 shadow-2xs">
                                    <span class="shrink-0 text-sm">🧥</span>
                                    <span><strong>穿著建議：</strong><span id="day-weather-clothing">長袖發熱衣 + 針織毛衣 + 防風防寒夾克，配舒適長褲。</span></span>
                                </div>
                            </div>

                            <!-- 面板 2: 今日自駕停車場速查 -->
                            <div id="panel-parking" class="hidden p-3.5 rounded-2xl bg-gradient-to-r from-emerald-50/90 to-teal-50/60 border border-emerald-200/90 shadow-2xs space-y-2 text-xs">
                                <div class="flex items-center justify-between pb-1 border-b border-emerald-200/60">
                                    <span class="font-black text-emerald-950 flex items-center gap-1">
                                        <span>🅿️</span> 今日自駕景點推薦停車場（點擊直達導航）：
                                    </span>
                                </div>
                                <div id="day-parking-chips" class="flex flex-wrap items-center gap-2"></div>
                            </div>

                            <!-- 面板 3: 今日美饌速覽 -->
                            <div id="panel-meals" class="hidden p-3.5 rounded-2xl bg-gradient-to-r from-amber-50/80 via-orange-50/50 to-purple-50/50 border border-amber-200/90 shadow-2xs space-y-2 text-xs">
                                <div class="flex flex-wrap items-center justify-between gap-2 pb-1 border-b border-amber-200/60">
                                    <span class="font-black text-amber-950 flex items-center gap-1">
                                        <span>🍽️</span> 今日精選三餐提案：
                                    </span>
                                    <button type="button" onclick="openTab('restaurants')" class="px-2.5 py-1 rounded-xl bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-700 hover:to-amber-700 text-white font-black text-[11px] shadow-2xs transition flex items-center gap-1">
                                        <span>🍱</span> 前往 81 家美食總表 ↗
                                    </button>
                                </div>
                                <div class="flex flex-wrap items-center gap-1.5 text-xs font-bold">
                                    <button type="button" onclick="scrollToMeal('breakfast')" class="px-2.5 py-1 rounded-xl bg-white hover:bg-amber-100 text-amber-900 border border-amber-200 shadow-2xs transition text-[11px]">🌅 早餐 3 選</button>
                                    <button type="button" onclick="scrollToMeal('lunch')" class="px-2.5 py-1 rounded-xl bg-white hover:bg-orange-100 text-orange-900 border border-orange-200 shadow-2xs transition text-[11px]">☀️ 午餐 3 選</button>
                                    <button type="button" onclick="scrollToMeal('dinner')" class="px-2.5 py-1 rounded-xl bg-white hover:bg-rose-100 text-rose-900 border border-rose-200 shadow-2xs transition text-[11px]">🌙 晚餐 3 選</button>
                                    <button type="button" onclick="scrollToMeal('latenight')" id="quick-jump-latenight" class="px-2.5 py-1 rounded-xl bg-purple-600 hover:bg-purple-700 text-white shadow-2xs transition text-[11px] font-black flex items-center gap-1">
                                        <span>🍸</span> 宵夜＆酒吧 3 選 ✨
                                    </button>
                                </div>
                            </div>

                            <!-- 面板 4: 臨時加點表單抽屜 -->
                            <div id="custom-stop-form-drawer" class="hidden bg-gradient-to-br from-stone-50 to-amber-50/40 p-4 rounded-2xl border-2 border-amber-200 space-y-3 text-xs shadow-2xs">
                                <div class="flex items-center justify-between pb-1 border-b border-amber-200">
                                    <span class="font-black text-amber-900 text-xs flex items-center gap-1">
                                        <span>✨</span> 臨時起意加點小便利貼 (自動生成 Google Maps 導航按鈕)
                                    </span>
                                    <button type="button" onclick="toggleSubPanel('custom')" class="text-stone-400 hover:text-stone-600 text-xs font-bold">✕ 關閉</button>
                                </div>
                                <form onsubmit="handleNewCustomStopSubmit(event)" class="space-y-2.5">
                                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                                        <div>
                                            <label class="block font-bold text-stone-700 mb-1">📍 想去的地點 / 店名 / 景點名稱：</label>
                                            <input type="text" id="cstop-title" placeholder="例如：道の駅 阿蘇 / 南阿蘇採草莓 / 驚安殿堂" required class="w-full bg-white border border-stone-200 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none focus:border-amber-400">
                                        </div>
                                        <div>
                                            <label class="block font-bold text-stone-700 mb-1">⏰ 預估時間（選填）：</label>
                                            <input type="text" id="cstop-time" placeholder="例如：14:30、下午順遊、或晚餐後" class="w-full bg-white border border-stone-200 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none focus:border-amber-400">
                                        </div>
                                    </div>
                                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                                        <div>
                                            <label class="block font-bold text-stone-700 mb-1">🏷️ 類別：</label>
                                            <select id="cstop-category" class="w-full bg-white border border-stone-200 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none focus:border-amber-400">
                                                <option value="sight">⛩️ 順遊名勝 / 探險景點</option>
                                                <option value="food">🍽️ 美食小吃 / 特色餐廳</option>
                                                <option value="shopping">🛍️ 購物採買 / 超市名產</option>
                                                <option value="transit">☕ 休息站 / 道の駅 / 加油</option>
                                                <option value="onsen">♨️ 臨時泡湯 / 日歸溫泉</option>
                                                <option value="farm">🍓 採果農園 / 觀光牧場</option>
                                            </select>
                                        </div>
                                        <div>
                                            <label class="block font-bold text-stone-700 mb-1">📝 備忘筆記 / 必買提醒（選填）：</label>
                                            <input type="text" id="cstop-desc" placeholder="例如：附免費停車場、買新鮮草莓一盒" class="w-full bg-white border border-stone-200 rounded-xl px-3 py-2 text-xs font-medium text-stone-800 focus:outline-none focus:border-amber-400">
                                        </div>
                                    </div>
                                    <div class="flex justify-end gap-2 pt-1">
                                        <button type="button" onclick="toggleSubPanel('custom')" class="px-3 py-1.5 rounded-xl bg-stone-100 hover:bg-stone-200 text-stone-600 font-bold text-xs transition">取消</button>
                                        <button type="submit" class="px-4 py-1.5 rounded-xl bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 text-white font-black text-xs shadow-sm transition flex items-center gap-1">
                                            <span>➕</span> 加入今日行程並建立導航
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>

                        <!-- 時間軸標題列 -->
                        <div class="mt-5 flex items-center justify-between pb-2 border-b border-stone-100">
                            <span class="text-xs font-black text-stone-700 flex items-center gap-1.5">
                                <span>⏱️</span> 行程時間軸
                            </span>
                            <span class="text-[11px] text-stone-400 font-medium" id="mode-status-hint">🌿 清爽閱讀中・點擊項目可展開自駕細節</span>
                        </div>

                        <div class="mt-6 relative pl-6 border-l-2 border-dashed border-red-300 space-y-5" id="timeline-container"></div>
                    </div>
                </div>

                <div class="space-y-4">
                    <div class="cute-card p-5 relative border-2 border-red-100">
                        <div class="washi-tape !w-20 !top-[-8px]"></div>
                        <h4 class="text-sm font-black text-red-600 flex items-center gap-2 mb-2">
                            <span>🏡</span> 今晚住哪裡～
                        </h4>
                        <div class="bg-red-50/60 border border-red-200 rounded-2xl p-3.5 space-y-1 text-xs">
                            <div class="font-bold text-stone-800 text-sm" id="day-hotel-name">載入中...</div>
                            <div class="text-stone-500 font-medium" id="day-hotel-desc">下樓即是熱鬧商店街，走路好逛又方便！</div>
                        </div>
                    </div>

                    <div class="cute-card p-5 relative border-2 border-amber-100">
                        <div class="washi-tape washi-tape-gold !w-20 !top-[-8px]"></div>
                        <h4 class="text-sm font-black text-amber-700 flex items-center gap-2 mb-2">
                            <span>🎁</span> 今日推薦名產與好料
                        </h4>
                        <div class="bg-amber-50/70 border border-amber-200 rounded-2xl p-3.5 text-xs text-stone-700 leading-relaxed font-medium" id="day-souvenir-box">
                            載入中...
                        </div>
                    </div>

                    <div class="cute-card p-5 relative border-2 border-stone-200 space-y-3">
                        <div class="flex items-center justify-between pb-1 border-b border-stone-100">
                            <h4 class="text-sm font-black text-stone-800 flex items-center gap-1.5">
                                <span>🗺️</span> 景點導航傳送門
                            </h4>
                            <span class="cute-pill bg-sky-100 text-sky-700 text-[10px]">Google Maps 直達</span>
                        </div>

                        <!-- 臨時即時導航搜尋框 -->
                        <div class="space-y-1.5 bg-stone-50 p-2.5 rounded-2xl border border-stone-200">
                            <label class="text-[11px] font-bold text-stone-600 flex items-center gap-1">
                                <span>🔍</span> 臨時自訂地點直達導航：
                            </label>
                            <div class="flex gap-1.5">
                                <input type="text" id="quick-nav-input" placeholder="輸入任何店名 / 地點 / 電話" class="flex-1 bg-white border border-stone-200 rounded-xl px-2.5 py-1.5 text-xs font-bold text-stone-800 focus:outline-none focus:border-sky-400">
                                <button type="button" onclick="launchQuickNav()" class="px-3 py-1.5 rounded-xl bg-sky-600 hover:bg-sky-700 text-white font-black text-xs shadow-sm transition">導航</button>
                            </div>
                            <div class="flex flex-wrap gap-1 pt-0.5">
                                <button type="button" onclick="quickNavSearch('採草莓 農園')" class="px-2 py-0.5 rounded-lg bg-pink-50 text-pink-700 border border-pink-200 text-[10px] font-bold hover:bg-pink-100">🍓 採草莓</button>
                                <button type="button" onclick="quickNavSearch('日歸溫泉 家族風呂')" class="px-2 py-0.5 rounded-lg bg-rose-50 text-rose-700 border border-rose-200 text-[10px] font-bold hover:bg-rose-100">♨️ 溫泉</button>
                                <button type="button" onclick="quickNavSearch('道の駅')" class="px-2 py-0.5 rounded-lg bg-amber-50 text-amber-700 border border-amber-200 text-[10px] font-bold hover:bg-amber-100">☕ 道の駅</button>
                                <button type="button" onclick="quickNavSearch('唐吉訶德')" class="px-2 py-0.5 rounded-lg bg-yellow-50 text-yellow-800 border border-yellow-200 text-[10px] font-bold hover:bg-yellow-100">🛒 唐吉訶德</button>
                                <button type="button" onclick="quickNavSearch('業務超市')" class="px-2 py-0.5 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold hover:bg-emerald-100">🥬 業務超市</button>
                            </div>
                        </div>

                        <!-- 當日推薦景點快捷導航清單 -->
                        <div class="space-y-1.5" id="quick-links-box"></div>
                    </div>
                </div>
            </div>

            <!-- 全寬獨立切割美食專區 (橫向延伸至右側空白，不跟行程時間軸擠在同一排版匡內) -->
            <div id="day-meals-container" class="cute-card p-5 sm:p-6 border-2 border-orange-200 bg-white relative space-y-5 shadow-sm w-full overflow-hidden mt-6"></div>
        </section>

        <!-- TAB 2: 九州手繪探索地圖 -->
        <section id="tab-content-map" class="tab-content hidden space-y-6">
            <div class="cute-card p-6 relative border-2 border-emerald-200 space-y-6">
                <div class="washi-tape washi-tape-green"></div>

                <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b-2 border-stone-100 gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="cute-pill bg-emerald-100 text-emerald-800">🗺️ 聖誕自駕手繪探索地圖</span>
                            <span class="text-xs text-stone-400">完整收錄機場、5 處旅宿與所有代表性名勝</span>
                        </div>
                        <h3 class="text-xl font-black text-stone-800 mt-1">📍 2026 南九州 7天6夜冒險地圖</h3>
                        <p class="text-xs text-stone-500 mt-0.5">點擊地圖上的任意圖釘 📍，即可查看該地點的天數、遊玩亮點與一鍵 Google Maps 導航！</p>
                    </div>

                    <div class="flex flex-wrap items-center gap-1.5 sm:gap-2 text-xs font-bold">
                        <button onclick="filterMap('all')" id="map-btn-all" class="px-2.5 py-1 rounded-full bg-emerald-700 text-white shadow-sm transition">
                            全部
                        </button>
                        <button onclick="filterMap('hotel')" id="map-btn-hotel" class="px-2.5 py-1 rounded-full bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                            🏡 旅宿
                        </button>
                        <button onclick="filterMap('sight')" id="map-btn-sight" class="px-2.5 py-1 rounded-full bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                            ⛩️ 景點
                        </button>
                        <button onclick="filterMap('transit')" id="map-btn-transit" class="px-2.5 py-1 rounded-full bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                            🛫 機場
                        </button>
                        <button onclick="toggleMapRoutes()" id="map-btn-routes" class="px-2.5 py-1 rounded-full bg-amber-100 text-amber-800 hover:bg-amber-200 transition">
                            🚗 7天全動線
                        </button>
                        <button onclick="toggleMapLabels()" id="map-btn-labels" class="px-2.5 py-1 rounded-full bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                            🏷️ 地名標籤
                        </button>
                    </div>
                </div>

                <!-- 每日移動路線快速切換器 (Day 1 至 Day 7 依序呈現) -->
                <div class="bg-amber-50/70 p-3.5 rounded-2xl border border-amber-200 space-y-2">
                    <div class="flex flex-wrap items-center justify-between gap-2">
                        <span class="text-xs font-black text-amber-950 flex items-center gap-1.5">
                            <span>🚗</span> 每日移動路線檢視 (點選切換當日自駕軌跡)：
                        </span>
                        <span class="text-[11px] text-amber-700 font-bold" id="route-indicator-text">已顯示全 7 天自駕動線</span>
                    </div>
                    <div class="flex flex-wrap items-center gap-1.5 text-xs font-bold">
                        <button type="button" onclick="selectDayRoute('all')" id="btn-route-all" class="btn-day-route px-3 py-1 rounded-full bg-amber-600 text-white shadow-xs transition text-[11px]">全部動線 (7天)</button>
                        <button type="button" onclick="selectDayRoute(1)" id="btn-route-1" class="btn-day-route px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">Day 1 熊本入境 ➔</button>
                        <button type="button" onclick="selectDayRoute(2)" id="btn-route-2" class="btn-day-route px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">Day 2 熊本 ➔ 阿蘇黑川 ➔</button>
                        <button type="button" onclick="selectDayRoute(3)" id="btn-route-3" class="btn-day-route px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">Day 3 黑川 ➔ 高千穗宮崎 ➔</button>
                        <button type="button" onclick="selectDayRoute(4)" id="btn-route-4" class="btn-day-route px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">Day 4 宮崎 ➔ 日南鹿兒島 ➔</button>
                        <button type="button" onclick="selectDayRoute(5)" id="btn-route-5" class="btn-day-route px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">Day 5 鹿兒島 ➔ 櫻島仙巖園 ➔</button>
                        <button type="button" onclick="selectDayRoute(6)" id="btn-route-6" class="btn-day-route px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">Day 6 鹿兒島 ➔ 霧島人吉 ➔ 熊本 ➔</button>
                        <button type="button" onclick="selectDayRoute(7)" id="btn-route-7" class="btn-day-route px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">Day 7 熊本市區 ➔ 機場 ➔ 台灣 ➔</button>
                    </div>
                    <!-- 當日詳細路線動態小黃籤 -->
                    <div id="route-summary-banner" class="hidden mt-2 p-2.5 bg-white rounded-xl border border-amber-300 text-xs text-amber-900 font-bold flex flex-wrap items-center justify-between gap-2 shadow-xs">
                        <div id="route-summary-text" class="flex items-center gap-1.5"></div>
                        <button type="button" onclick="selectDayRoute('all')" class="text-[11px] text-amber-700 underline font-bold hover:text-amber-900">重設顯示全部 ↺</button>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 cute-card p-4 bg-[#f4f7f2] border-2 border-emerald-100 relative overflow-hidden flex items-center justify-center min-h-[580px]">
                        <svg id="kyushu-svg" viewBox="200 60 550 730" class="w-full h-auto max-h-[660px] select-none" xmlns="http://www.w3.org/2000/svg">
                            <defs>
                                <filter id="cute-shadow" x="-10%" y="-10%" width="120%" height="120%">
                                    <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#a39080" flood-opacity="0.25"/>
                                </filter>
                                <pattern id="sea-waves" width="40" height="20" patternUnits="userSpaceOnUse">
                                    <path d="M 5 10 Q 15 5, 25 10 T 45 10" fill="none" stroke="#d5e3da" stroke-width="1.5" stroke-linecap="round"/>
                                </pattern>
                            </defs>

                            <rect width="920" height="820" fill="#e9f3ec" rx="20"/>
                            <rect width="920" height="820" fill="url(#sea-waves)" rx="20"/>

                            <text x="240" y="310" fill="#88a896" font-size="13" font-weight="bold" letter-spacing="2">有 明 海</text>
                            <text x="715" y="450" fill="#88a896" font-size="15" font-weight="bold" letter-spacing="3">太 平 洋</text>
                            <text x="325" y="740" fill="#88a896" font-size="13" font-weight="bold" letter-spacing="2">錦 江 灣</text>

                            <path d="
                                M 330 110 
                                C 380 90, 480 80, 530 130 
                                C 580 170, 640 210, 660 270 
                                C 680 320, 680 400, 710 470 
                                C 730 520, 730 600, 710 680 
                                C 690 730, 660 760, 610 760 
                                C 570 760, 530 730, 500 700 
                                C 470 700, 440 760, 410 760 
                                C 360 760, 340 700, 360 640 
                                C 340 590, 320 540, 300 480 
                                C 270 450, 240 430, 260 380 
                                C 280 340, 260 300, 280 250 
                                C 300 200, 310 150, 330 110 Z" 
                                fill="#fffef7" stroke="#9bbd9e" stroke-width="3.5" filter="url(#cute-shadow)"/>

                            <ellipse cx="445" cy="660" rx="26" ry="20" fill="#fed7aa" stroke="#f97316" stroke-width="2.5"/>
                            <text x="445" y="665" font-size="11" font-weight="bold" fill="#c2410c" text-anchor="middle">櫻島 🌋</text>

                            <text x="350" y="270" font-size="15" font-weight="900" fill="#cbd5e1" text-anchor="middle">熊 本 縣</text>
                            <text x="610" y="520" font-size="15" font-weight="900" fill="#cbd5e1" text-anchor="middle">宮 崎 縣</text>
                            <text x="450" y="720" font-size="15" font-weight="900" fill="#cbd5e1" text-anchor="middle">鹿 兒 島 縣</text>

                            <g id="map-routes-group">
                                <!-- Day 1: 桃機 ➔ 熊本空港 (430 375) ➔ 熊本辛島町 (325 390) -->
                                <g class="route-group cursor-pointer" onclick="toggleMapRoute(1)" id="route-group-1">
                                    <path d="M 430 375 L 325 390" fill="none" stroke="transparent" stroke-width="26" stroke-linecap="round"/>
                                    <path id="route-path-1" class="day-route-path transition-all duration-300" data-day="1" d="M 430 375 L 325 390" fill="none" stroke="#2563eb" stroke-width="4" stroke-dasharray="7 4" stroke-linecap="round"/>
                                </g>
                                <!-- Day 2: 熊本辛島町 (325 390) ➔ 草千里 (475 345) ➔ 大觀峰 (495 275) ➔ 黑川溫泉 (545 250) -->
                                <g class="route-group cursor-pointer" onclick="toggleMapRoute(2)" id="route-group-2">
                                    <path d="M 325 390 Q 400 370, 475 345 T 495 275 T 545 250" fill="none" stroke="transparent" stroke-width="26" stroke-linecap="round"/>
                                    <path id="route-path-2" class="day-route-path transition-all duration-300" data-day="2" d="M 325 390 Q 400 370, 475 345 T 495 275 T 545 250" fill="none" stroke="#dc2626" stroke-width="4.5" stroke-dasharray="8 4" stroke-linecap="round"/>
                                </g>
                                <!-- Day 3: 黑川溫泉 (545 250) ➔ 上色見 (505 400) ➔ 高千穗 (570 415) ➔ 宮崎海邊 (675 535) -->
                                <g class="route-group cursor-pointer" onclick="toggleMapRoute(3)" id="route-group-3">
                                    <path d="M 545 250 Q 520 330, 505 400 T 570 415 Q 630 480, 675 535" fill="none" stroke="transparent" stroke-width="26" stroke-linecap="round"/>
                                    <path id="route-path-3" class="day-route-path transition-all duration-300" data-day="3" d="M 545 250 Q 520 330, 505 400 T 570 415 Q 630 480, 675 535" fill="none" stroke="#7c3aed" stroke-width="4.5" stroke-dasharray="8 4" stroke-linecap="round"/>
                                </g>
                                <!-- Day 4: 宮崎 (675 535) ➔ 青島 (685 595) ➔ 摩艾 (675 645) ➔ 鵜戶神宮 (670 695) ➔ 鹿兒島 (365 685) -->
                                <g class="route-group cursor-pointer" onclick="toggleMapRoute(4)" id="route-group-4">
                                    <path d="M 675 535 L 685 595 L 675 645 L 670 695 Q 520 720, 365 685" fill="none" stroke="transparent" stroke-width="26" stroke-linecap="round"/>
                                    <path id="route-path-4" class="day-route-path transition-all duration-300" data-day="4" d="M 675 535 L 685 595 L 675 645 L 670 695 Q 520 720, 365 685" fill="none" stroke="#059669" stroke-width="4.5" stroke-dasharray="8 4" stroke-linecap="round"/>
                                </g>
                                <!-- Day 5: 鹿兒島 (365 685) ➔ 櫻島渡輪 (455 655) ➔ 仙巖園 (375 635) ➔ 天文館 (365 685) -->
                                <g class="route-group cursor-pointer" onclick="toggleMapRoute(5)" id="route-group-5">
                                    <path d="M 365 685 Q 410 670, 455 655 Q 415 645, 375 635 L 365 685" fill="none" stroke="transparent" stroke-width="26" stroke-linecap="round"/>
                                    <path id="route-path-5" class="day-route-path transition-all duration-300" data-day="5" d="M 365 685 Q 410 670, 455 655 Q 415 645, 375 635 L 365 685" fill="none" stroke="#ea580c" stroke-width="4.5" stroke-dasharray="6 3" stroke-linecap="round"/>
                                </g>
                                <!-- Day 6: 鹿兒島 (365 685) ➔ 霧島神宮 (470 570) ➔ 人吉鰻魚 (425 490) ➔ 熊本辛島町 (355 410) -->
                                <g class="route-group cursor-pointer" onclick="toggleMapRoute(6)" id="route-group-6">
                                    <path d="M 365 685 Q 390 630, 470 570 Q 445 525, 425 490 Q 380 450, 355 410" fill="none" stroke="transparent" stroke-width="26" stroke-linecap="round"/>
                                    <path id="route-path-6" class="day-route-path transition-all duration-300" data-day="6" d="M 365 685 Q 390 630, 470 570 Q 445 525, 425 490 Q 380 450, 355 410" fill="none" stroke="#d97706" stroke-width="4.5" stroke-dasharray="8 4" stroke-linecap="round"/>
                                </g>
                                <!-- Day 7: 熊本辛島町 (355 410) ➔ 熊本城 (345 340) ➔ 水前寺成趣園 (395 420) ➔ 熊本空港 (430 375) -->
                                <g class="route-group cursor-pointer" onclick="toggleMapRoute(7)" id="route-group-7">
                                    <path d="M 355 410 L 345 340 L 395 420 L 430 375" fill="none" stroke="transparent" stroke-width="26" stroke-linecap="round"/>
                                    <path id="route-path-7" class="day-route-path transition-all duration-300" data-day="7" d="M 355 410 L 345 340 L 395 420 L 430 375" fill="none" stroke="#be123c" stroke-width="4.5" stroke-dasharray="7 4" stroke-linecap="round"/>
                                </g>
                            </g>

                            <g id="map-pins-group"></g>
                        </svg>

                        <div class="absolute bottom-3 left-4 bg-white/95 backdrop-blur-sm p-3 rounded-2xl border-2 border-stone-200 text-[11px] font-bold text-stone-600 space-y-1.5 shadow-md">
                            <div class="flex items-center justify-between gap-3 pb-1 border-b border-stone-200">
                                <span class="text-xs font-black text-stone-800 flex items-center gap-1"><span>✨</span> 路線篩選模式</span>
                                <button type="button" onclick="resetMapRoutes()" id="map-reset-routes-btn" class="text-[10px] text-stone-500 hover:text-red-600 font-black underline transition cursor-pointer">顯示全部路線</button>
                            </div>
                            <div class="text-[10px] text-amber-800 font-bold" id="map-route-status-tip">💡 點擊地圖任意虛線，可單獨留下該日自駕路線</div>
                            <div class="flex flex-wrap gap-1.5 pt-0.5 pointer-events-auto">
                                <button type="button" onclick="toggleMapRoute(1)" id="route-btn-1" class="px-2 py-0.5 rounded-full text-[10px] font-bold border border-blue-200 bg-blue-50 text-blue-700 hover:bg-blue-100 transition">D1</button>
                                <button type="button" onclick="toggleMapRoute(2)" id="route-btn-2" class="px-2 py-0.5 rounded-full text-[10px] font-bold border border-red-200 bg-red-50 text-red-700 hover:bg-red-100 transition">D2</button>
                                <button type="button" onclick="toggleMapRoute(3)" id="route-btn-3" class="px-2 py-0.5 rounded-full text-[10px] font-bold border border-purple-200 bg-purple-50 text-purple-700 hover:bg-purple-100 transition">D3</button>
                                <button type="button" onclick="toggleMapRoute(4)" id="route-btn-4" class="px-2 py-0.5 rounded-full text-[10px] font-bold border border-emerald-200 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 transition">D4</button>
                                <button type="button" onclick="toggleMapRoute(5)" id="route-btn-5" class="px-2 py-0.5 rounded-full text-[10px] font-bold border border-orange-200 bg-orange-50 text-orange-700 hover:bg-orange-100 transition">D5</button>
                                <button type="button" onclick="toggleMapRoute(6)" id="route-btn-6" class="px-2 py-0.5 rounded-full text-[10px] font-bold border border-amber-200 bg-amber-50 text-amber-700 hover:bg-amber-100 transition">D6</button>
                                <button type="button" onclick="toggleMapRoute(7)" id="route-btn-7" class="px-2 py-0.5 rounded-full text-[10px] font-bold border border-rose-200 bg-rose-50 text-rose-700 hover:bg-rose-100 transition">D7</button>
                            </div>
                        </div>
                    </div>

                    <div class="space-y-4">
                        <div class="polaroid-card space-y-3 bg-gradient-to-b from-white to-red-50/20 border-2 border-red-200 relative" id="map-detail-card">
                            <div class="washi-tape washi-tape-gold !w-20 !top-[-8px]"></div>

                            <div class="flex items-start justify-between gap-2 pt-1">
                                <div>
                                    <span class="cute-pill bg-red-100 text-red-700" id="card-day">點擊地圖圖釘</span>
                                    <h4 class="text-base font-black text-stone-800 mt-1" id="card-title">阿蘇草千里之濱 ＆ 火山口</h4>
                                    <span class="text-xs text-stone-400 font-bold" id="card-category">自然火山絕景</span>
                                </div>
                                <span class="text-3xl p-2 rounded-2xl bg-white border border-stone-200 shadow-sm" id="card-icon">🌋</span>
                            </div>

                            <p class="text-xs text-stone-600 leading-relaxed font-medium bg-stone-50 p-3 rounded-xl border border-stone-200" id="card-desc">
                                遼闊草原與高聳火山湖，近距離眺望不斷冒出白色煙霧的中岳活火山口，場面壯闊震撼無比！
                            </p>

                            <div class="text-[11px] text-amber-800 bg-amber-50 border border-amber-200 rounded-xl p-2.5 flex items-start gap-1.5" id="card-tips-box">
                                <span>💡</span>
                                <span id="card-tips"><strong>貼心叮嚀：</strong>山頂風大體感溫度低，穿著保暖防風厚外套與毛帽！</span>
                            </div>

                            <div class="pt-2">
                                <a id="card-map-link" href="https://www.google.com/maps/search/?api=1&query=阿蘇草千里" target="_blank" class="w-full py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white font-black text-xs flex items-center justify-center gap-1.5 shadow-md shadow-red-200 transition">
                                    <span>🗺️</span>
                                    <span>在 Google Maps 中開啟導航</span>
                                    <span>↗</span>
                                </a>
                            </div>
                        </div>

                        <div class="cute-card p-4 border-2 border-stone-200 space-y-3">
                            <div class="flex items-center justify-between pb-2 border-b border-stone-100">
                                <h5 class="text-xs font-black text-stone-700 flex items-center gap-1.5">
                                    <span>⚡</span> 焦點快速定位：
                                </h5>
                                <div class="flex gap-1.5" id="quick-pick-tabs">
                                    <button onclick="switchQuickPickTab('hotels')" id="qtab-hotels" class="px-3 py-1 rounded-xl text-xs font-black bg-purple-100 text-purple-700 transition">🏨 6晚旅宿</button>
                                    <button onclick="switchQuickPickTab('sights')" id="qtab-sights" class="px-3 py-1 rounded-xl text-xs font-black bg-stone-100 text-stone-600 hover:bg-stone-200 transition">🏔️ 經典景點</button>
                                </div>
                            </div>
                            
                            <!-- 快捷按鈕列表 -->
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-bold" id="map-quick-buttons"></div>

                            <!-- 一鍵找身邊加油站按鈕 -->
                            <div class="pt-2 border-t border-stone-100">
                                <a href="https://www.google.com/maps/search/?api=1&query=加油站+Gas+Station+ガソリンスタンド" target="_blank" class="w-full py-2.5 px-3 rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-black text-xs flex items-center justify-center gap-1.5 shadow-md shadow-amber-200 transition">
                                    <span>⛽</span>
                                    <span>一鍵呼叫目前位置最近的加油站 (Google Maps)</span>
                                    <span>↗</span>
                                </a>
                            </div>
                        </div>

                        <!-- 自駕加油防呆口訣 -->
                        <div class="sticky-note p-3.5 space-y-1.5 text-xs text-stone-800">
                            <div class="font-black text-amber-900 flex items-center gap-1">
                                <span>🚗</span> 日本自駕加油 4 大防呆口訣：
                            </div>
                            <ul class="space-y-1 text-[11px] text-stone-700 list-disc list-inside font-medium">
                                <li><strong>認明紅槍 (レギュラー)</strong>：休旅車請加 Regular 紅色油槍，切勿加錯綠槍柴油！</li>
                                <li><strong>選「満タン (加滿)」</strong>：螢幕選「満タン」，跳槍即停。</li>
                                <li><strong>滿油還車留收據</strong>：租車還車前需在市區 5km 內加滿，並出示「給油レシート」。</li>
                                <li><strong>現金找零去精算機</strong>：現金付款若有找零，持收據條碼到旁邊精算機刷碼找零錢。</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <!-- TOYOTA 租車官方核心重要事項大補帖 (全自駕安全與合約重要須知) -->
            <div class="cute-card p-6 relative border-2 border-amber-200/90 bg-gradient-to-br from-white via-amber-50/20 to-orange-50/20 space-y-5 shadow-xs">
                <div class="washi-tape washi-tape-gold"></div>

                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b-2 border-amber-100 gap-3">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="cute-pill bg-amber-100 text-amber-900 font-bold">🚗 TOYOTA 租車官方合約說明</span>
                            <span class="cute-pill bg-red-100 text-red-700 font-bold">自駕行前必讀</span>
                        </div>
                        <h4 class="text-base sm:text-lg font-black text-stone-800 mt-1 flex items-center gap-2">
                            <span>📋</span> TOYOTA 租車重要事項說明＆自駕安全實戰手冊
                        </h4>
                        <p class="text-xs text-stone-500 mt-0.5">整理自 TOYOTA 日本官方「重要事項説明」與海外旅客合約規範，涵蓋櫃台取車證件、保險W方案、事故處置、違停與加油須知。</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <a href="https://rent.toyota.co.jp/global_zh-tw/guide/importantitems.html" target="_blank" class="px-3 py-1.5 rounded-xl bg-white hover:bg-amber-100 text-amber-900 border border-amber-200 font-bold text-xs flex items-center gap-1.5 shadow-2xs transition shrink-0">
                            <span>🌐</span> TOYOTA 官方合約原文 ↗
                        </a>
                    </div>
                </div>

                <!-- 6 大核心卡片 Grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
                    <!-- 卡片 1: 取車必備證件與付款政策 -->
                    <div class="bg-white/95 p-4 rounded-2xl border border-stone-200/90 shadow-2xs space-y-2.5">
                        <div class="flex items-center justify-between font-black pb-1.5 border-b border-stone-100">
                            <span class="text-stone-800 flex items-center gap-1.5">
                                <span>📄</span> 1. 櫃台取車必備 4 大件
                            </span>
                            <span class="text-[10px] bg-red-50 text-red-600 px-2 py-0.5 rounded-full font-bold">缺一不可</span>
                        </div>
                        <ul class="space-y-1.5 text-[11px] text-stone-700 font-medium">
                            <li class="flex items-start gap-1.5">
                                <span class="text-red-500 shrink-0">●</span>
                                <span><strong>台灣護照正本</strong>：有效期限須在 6 個月以上。</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-red-500 shrink-0">●</span>
                                <span><strong>台灣駕照正本</strong>：務必在<strong>有效期限內</strong>（過期請先至台灣監理站換發最新版）。</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-red-500 shrink-0">●</span>
                                <span><strong>台灣駕照日文譯本正本</strong>：由監理站核發之 A4 規格譯本（<strong>日本不承認台灣國際駕照</strong>）。</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-red-500 shrink-0">●</span>
                                <span><strong>實體信用卡</strong>：<strong>官方全面停用金融卡 (Debit Card) 與預付卡</strong>，不支援行動支付，現場刷卡扣除預估費用。</span>
                            </li>
                        </ul>
                        <div class="text-[10px] text-amber-800 bg-amber-50 p-2 rounded-xl border border-amber-200 leading-tight">
                            ⚠️ <strong>多人輪流開車提醒</strong>：若有第二位駕駛，取車時所有人必須同時在櫃台出示駕照與譯本登記，未登記駕駛人肇事「保險一律不理賠」！
                        </div>
                    </div>

                    <!-- 卡片 2: 保險賠償與安心 W 方案 -->
                    <div class="bg-white/95 p-4 rounded-2xl border border-stone-200/90 shadow-2xs space-y-2.5">
                        <div class="flex items-center justify-between font-black pb-1.5 border-b border-stone-100">
                            <span class="text-stone-800 flex items-center gap-1.5">
                                <span>🛡️</span> 2. 保險賠償與安心 W 方案
                            </span>
                            <span class="text-[10px] bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded-full font-bold">強烈推薦</span>
                        </div>
                        <ul class="space-y-1.5 text-[11px] text-stone-700 font-medium">
                            <li class="flex items-start gap-1.5">
                                <span class="text-emerald-600 shrink-0">●</span>
                                <span><strong>基本費用內含</strong>：對人無限額、對物無限額（自負額 ¥50,000）、車輛時價（自負額 ¥50,000）、乘客傷害每人最高 3,000 萬日圓。</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-emerald-600 shrink-0">●</span>
                                <span><strong>營業損失賠償 (NOC)</strong>：車輛能開回店鋪需付 ¥20,000；拋錨無法開回需付 ¥50,000。</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-emerald-600 shrink-0">●</span>
                                <span><strong>安心 W 方案 (¥1,650/天)</strong>：
                                    <br>✅ <strong>免除對物與車輛自負額（現省 10 萬日圓）</strong>
                                    <br>✅ <strong>免除營業損失賠償 NOC（現省 2~5 萬日圓）</strong>
                                    <br>✅ <strong>免除爆胎修補、換新輪胎與輪圈受損費用</strong>
                                </span>
                            </li>
                        </ul>
                        <div class="text-[10px] text-emerald-800 bg-emerald-50 p-2 rounded-xl border border-emerald-200 leading-tight">
                            💡 日本道路救援與換胎工資極貴，加購安心 W 方案全家自駕安心無憂！
                        </div>
                    </div>

                    <!-- 卡片 3: 保險絕對不理賠的 6 大禁忌 -->
                    <div class="bg-white/95 p-4 rounded-2xl border border-red-200 shadow-2xs space-y-2.5">
                        <div class="flex items-center justify-between font-black pb-1.5 border-b border-red-100">
                            <span class="text-red-800 flex items-center gap-1.5">
                                <span>🚫</span> 3. 保險 6 大絕不理賠禁忌
                            </span>
                            <span class="text-[10px] bg-red-100 text-red-800 px-2 py-0.5 rounded-full font-bold">千萬注意</span>
                        </div>
                        <ul class="space-y-1.5 text-[11px] text-stone-700 font-medium">
                            <li class="flex items-start gap-1.5">
                                <span class="text-red-600 shrink-0">✖</span>
                                <span><strong>未向警察報案</strong>：自撞、擦撞山壁或無人受傷小刮痕，<strong>沒叫警察開立事故證明，保險 100% 不理賠</strong>！</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-red-600 shrink-0">✖</span>
                                <span><strong>非出發時登記之駕駛人肇事</strong>。</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-red-600 shrink-0">✖</span>
                                <span><strong>無照駕駛、酒後駕駛</strong>（日本酒駕連坐同車乘客，處罰極嚴）。</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-red-600 shrink-0">✖</span>
                                <span><strong>逾時還車未提前聯絡</strong>期間發生之任何事故。</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-red-600 shrink-0">✖</span>
                                <span><strong>鑰匙留在車內導致失竊</strong>、禁菸車內抽菸污損。</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-red-600 shrink-0">✖</span>
                                <span><strong>加錯燃油造成引擎損壞</strong>（汽油車誤加柴油屬人為疏失需全額自賠）。</span>
                            </li>
                        </ul>
                    </div>

                    <!-- 卡片 4: 事故與拋錨 4 步驟 SOP -->
                    <div class="bg-white/95 p-4 rounded-2xl border border-stone-200/90 shadow-2xs space-y-2.5">
                        <div class="flex items-center justify-between font-black pb-1.5 border-b border-stone-100">
                            <span class="text-stone-800 flex items-center gap-1.5">
                                <span>🚨</span> 4. 發生事故 / 拋錨應變 SOP
                            </span>
                            <span class="text-[10px] bg-sky-50 text-sky-700 px-2 py-0.5 rounded-full font-bold">冷靜處理</span>
                        </div>
                        <ol class="space-y-1.5 text-[11px] text-stone-700 font-medium list-decimal list-inside">
                            <li><strong>第一步：救護傷患</strong><br>若有人受傷，立即撥打 <span class="text-red-600 font-bold font-mono">119</span> 叫救護車，將車輛移至安全處。</li>
                            <li><strong>第二步：向警察報案備案</strong><br>立即撥打 <span class="text-red-600 font-bold font-mono">110</span> 報警，向警方取得交通事故案號。</li>
                            <li><strong>第三步：現場留證（切勿私了）</strong><br>記錄對方姓名、電話、車牌，拍照錄影保留現場跡證。</li>
                            <li><strong>第四步：聯絡 TOYOTA 專線</strong><br>撥打店鋪電話或 TOYOTA 24小時中文專線 <span class="text-sky-700 font-bold font-mono">0800-7000-815</span> 通報派車。</li>
                        </ol>
                    </div>

                    <!-- 卡片 5: 違規停車被貼黃單處理流程 -->
                    <div class="bg-white/95 p-4 rounded-2xl border border-stone-200/90 shadow-2xs space-y-2.5">
                        <div class="flex items-center justify-between font-black pb-1.5 border-b border-stone-100">
                            <span class="text-stone-800 flex items-center gap-1.5">
                                <span>🅿️</span> 5. 違規停車被貼單之處理
                            </span>
                            <span class="text-[10px] bg-amber-50 text-amber-700 px-2 py-0.5 rounded-full font-bold">還車前繳清</span>
                        </div>
                        <ul class="space-y-1.5 text-[11px] text-stone-700 font-medium">
                            <li>若擋風玻璃被貼「違規停車確認標章」：</li>
                            <li>① <strong>務必在還車前前往該轄區警察署</strong>辦理繳納罰款手續。</li>
                            <li>② 至金融機構或便利店繳清罰款後，<strong>妥善保管收據</strong>。</li>
                            <li>③ 還車時出示警察開立的證明與罰款收據。</li>
                        </ul>
                        <div class="text-[10px] text-red-800 bg-red-50 p-2 rounded-xl border border-red-200 leading-tight">
                            ⚠️ <strong>未繳清後果嚴重</strong>：還車前若未繳，TOYOTA 將加收違約金（<strong>普通車 ¥25,000 / 中大型車 ¥30,000</strong>），並通報全日本租車協會列入拒絕租車黑名單！
                        </div>
                    </div>

                    <!-- 卡片 6: 還車加油與油電混合結算 -->
                    <div class="bg-white/95 p-4 rounded-2xl border border-stone-200/90 shadow-2xs space-y-2.5">
                        <div class="flex items-center justify-between font-black pb-1.5 border-b border-stone-100">
                            <span class="text-stone-800 flex items-center gap-1.5">
                                <span>⛽</span> 6. 還車加油與油電結算
                            </span>
                            <span class="text-[10px] bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full font-bold">還車小秘訣</span>
                        </div>
                        <ul class="space-y-1.5 text-[11px] text-stone-700 font-medium">
                            <li class="flex items-start gap-1.5">
                                <span class="text-indigo-600 shrink-0">●</span>
                                <span><strong>傳統油車滿油還車</strong>：還車前需在還車店鋪 <strong>5km 內的加油站加滿</strong>（選 Regular 紅色油槍「満タン」），並保留加油發票供查驗。</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-indigo-600 shrink-0">●</span>
                                <span><strong>油電混合車 (Hybrid) 便利結算</strong>：TOYOTA 獨家提供「混合動力車燃油結算」！歸還時無須先加滿油，店員直接根據儀表板「平均油耗」計算里程油資，免去市區找加油站排隊的麻煩。</span>
                            </li>
                            <li class="flex items-start gap-1.5">
                                <span class="text-indigo-600 shrink-0">●</span>
                                <span><strong>若需延長租借時間</strong>：請於原訂還車時間前致電店鋪，未聯絡超時將收取高額違約金。</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- 緊急聯絡備忘列 -->
                <div class="p-3.5 bg-gradient-to-r from-red-50/90 via-rose-50/70 to-amber-50/80 border border-red-200/80 rounded-2xl flex flex-wrap items-center justify-between gap-3 text-xs shadow-2xs">
                    <div class="flex flex-wrap items-center gap-3">
                        <span class="font-black text-red-950 flex items-center gap-1">
                            <span>📞</span> <strong>自駕在途緊急求助電話備忘：</strong>
                        </span>
                        <div class="flex flex-wrap items-center gap-2">
                            <span class="bg-white px-2.5 py-1 rounded-xl border border-red-200 text-red-700 font-mono font-black">🚔 警察：110</span>
                            <span class="bg-white px-2.5 py-1 rounded-xl border border-red-200 text-red-700 font-mono font-black">🚑 救護車：119</span>
                            <span class="bg-white px-2.5 py-1 rounded-xl border border-amber-200 text-amber-900 font-mono font-black">🏢 TOYOTA 免費專線：0800-7000-815</span>
                            <span class="bg-white px-2.5 py-1 rounded-xl border border-stone-200 text-stone-700 font-mono font-black">📱 國際/手機：+81-92-577-0091</span>
                        </div>
                    </div>
                    <span class="text-[11px] text-stone-500 font-medium">服務時間：每日 8:00 ~ 20:00（提供中文、英文多語對應）</span>
                </div>
            </div>
        </section>

        <!-- TAB: 餐廳與美食總整理 -->
        <section id="tab-content-restaurants" class="tab-content hidden space-y-6">
            <div class="cute-card p-6 relative border-2 border-orange-200 space-y-6">
                <div class="washi-tape washi-tape-gold"></div>

                <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b-2 border-orange-100 gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="cute-pill bg-orange-100 text-orange-800">🍱 全九州 63 家嚴選美食・訂位總整理</span>
                            <span class="text-xs text-stone-400">早・午・晚 三餐完整攻略</span>
                        </div>
                        <h3 class="text-xl font-black text-stone-800 mt-1">🍽️ 2026 南九州 7天6夜美饌手帳＆線上訂位傳送門</h3>
                        <p class="text-xs text-stone-500 mt-0.5">完整收錄阿蘇赤牛、黑川溫泉會席、高千穗牛、宮崎牛、日南海鮮、鹿兒島六白黑豚與人吉百年烤鰻，支援一鍵線上訂位、電話代訂與 Google Maps 導航！</p>
                    </div>

                    <!-- 搜尋框 -->
                    <div class="w-full md:w-72">
                        <div class="relative">
                            <input type="text" id="rest-search-input" oninput="filterRestaurants()" placeholder="🔍 搜尋餐廳、料理、地區或店名..." class="w-full bg-white border border-stone-200 rounded-2xl pl-3 pr-8 py-2 text-xs font-bold text-stone-800 focus:outline-none focus:border-orange-400 shadow-sm">
                            <button type="button" onclick="clearRestSearch()" class="absolute right-2.5 top-2 text-stone-400 hover:text-stone-600 text-xs font-bold">✕</button>
                        </div>
                    </div>
                </div>

                <!-- 篩選標籤列 -->
                <div class="space-y-2 bg-orange-50/50 p-4 rounded-3xl border border-orange-200 text-xs font-bold">
                    <div class="flex flex-wrap items-center gap-2">
                        <span class="text-stone-500 text-[11px] font-bold">🍴 餐別篩選：</span>
                        <button type="button" onclick="setRestFilter('meal', 'all')" id="rf-meal-all" class="rf-meal-btn px-3 py-1 rounded-full bg-orange-600 text-white shadow-sm transition">全部餐別 (81)</button>
                        <button type="button" onclick="setRestFilter('meal', 'breakfast')" id="rf-meal-breakfast" class="rf-meal-btn px-3 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition">🌅 早餐 (21)</button>
                        <button type="button" onclick="setRestFilter('meal', 'lunch')" id="rf-meal-lunch" class="rf-meal-btn px-3 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition">☀️ 午餐 (21)</button>
                        <button type="button" onclick="setRestFilter('meal', 'dinner')" id="rf-meal-dinner" class="rf-meal-btn px-3 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition">🌙 晚餐 (21)</button>
                        <button type="button" onclick="setRestFilter('meal', 'latenight')" id="rf-meal-latenight" class="rf-meal-btn px-3 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition">🍸 宵夜＆酒吧 (18)</button>
                    </div>

                    <div class="flex flex-wrap items-center gap-2 pt-1 border-t border-orange-200/60">
                        <span class="text-stone-500 text-[11px] font-bold">📅 行程天數：</span>
                        <button type="button" onclick="setRestFilter('day', 'all')" id="rf-day-all" class="rf-day-btn px-2.5 py-0.5 rounded-full bg-orange-600 text-white shadow-sm transition text-[11px]">全部天數</button>
                        <button type="button" onclick="setRestFilter('day', '1')" id="rf-day-1" class="rf-day-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]">Day 1 熊本</button>
                        <button type="button" onclick="setRestFilter('day', '2')" id="rf-day-2" class="rf-day-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]">Day 2 阿蘇黑川</button>
                        <button type="button" onclick="setRestFilter('day', '3')" id="rf-day-3" class="rf-day-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]">Day 3 高千穗宮崎</button>
                        <button type="button" onclick="setRestFilter('day', '4')" id="rf-day-4" class="rf-day-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]">Day 4 日南鹿兒島</button>
                        <button type="button" onclick="setRestFilter('day', '5')" id="rf-day-5" class="rf-day-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]">Day 5 櫻島仙巖園</button>
                        <button type="button" onclick="setRestFilter('day', '6')" id="rf-day-6" class="rf-day-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]">Day 6 霧島人吉</button>
                        <button type="button" onclick="setRestFilter('day', '7')" id="rf-day-7" class="rf-day-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]">Day 7 熊本古城</button>
                    </div>

                    <div class="flex flex-wrap items-center gap-2 pt-1 border-t border-orange-200/60">
                        <span class="text-stone-500 text-[11px] font-bold">🔥 必吃主題：</span>
                        <button type="button" onclick="setRestFilter('theme', 'all')" id="rf-theme-all" class="rf-theme-btn px-2.5 py-0.5 rounded-full bg-orange-600 text-white shadow-sm transition text-[11px]">全部美食</button>
                        <button type="button" onclick="setRestFilter('theme', 'shortlist')" id="rf-theme-shortlist" class="rf-theme-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">⭐ 我的候選名單 (<span id="shortlist-count-badge">0</span>)</button>
                        <button type="button" onclick="setRestFilter('theme', 'meat')" id="rf-theme-meat" class="rf-theme-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]">🐮 頂級肉品 (和牛/黑豚/鰻魚)</button>
                        <button type="button" onclick="setRestFilter('theme', 'reserve')" id="rf-theme-reserve" class="rf-theme-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]">🎫 建議線上提早訂位名店</button>
                        <button type="button" onclick="setRestFilter('theme', 'bar')" id="rf-theme-bar" class="rf-theme-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]">🍸 微醺酒吧與特色酒館</button>
                    </div>
                </div>

                <!-- 餐廳卡片列表 Grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5" id="restaurants-grid"></div>
            </div>
        </section>

                <!-- TAB 3: 分帳看板 ＆ 即時記帳 -->
        <section id="tab-content-costs" class="tab-content hidden space-y-6">
            <div class="cute-card p-6 relative border-2 border-amber-200 space-y-6">
                <div class="washi-tape washi-tape-gold"></div>

                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b-2 border-stone-100 gap-4">
                    <div>
                        <div class="flex flex-wrap items-center gap-2">
                            <span class="cute-pill bg-amber-100 text-amber-700 font-bold">✨ 4人探險隊分帳</span>
                            <span class="text-xs text-stone-400" id="members-subtitle-names">（首席導遊、總務大臣、美食評鑑官、榮譽總指揮）</span>
                            <button type="button" onclick="openMemberNamesModal()" class="px-2 py-0.5 rounded-lg bg-amber-100/90 hover:bg-amber-200 text-amber-900 border border-amber-300 text-[11px] font-bold transition active:scale-95 flex items-center gap-1 shadow-2xs">
                                <span>✏️</span> <span>自訂名稱</span>
                            </button>
                        </div>
                        <h3 class="text-xl font-black text-stone-800 mt-1">👛 旅費代墊與應付分攤結算看板</h3>
                        <p class="text-xs text-stone-500 mt-0.5">即時記帳自動分攤，支援網頁直接記帳與 Google 試算表雲端同步！</p>
                    </div>
                    <div class="bg-gradient-to-tr from-amber-100 to-amber-200/70 border border-amber-300 rounded-3xl px-5 py-3 text-right shadow-sm">
                        <div class="text-xs text-amber-800 font-bold">目前累計已記帳總花費</div>
                        <div class="text-2xl font-black text-stone-800 font-mono" id="cost-total-amount">NT$ {total_spent_twd:,.0f}</div>
                        <div class="text-[11px] text-stone-600" id="cost-per-person">平均每人應付 NT$ {per_person_avg:,.0f}</div>
                    </div>
                </div>

                <!-- 4人個人結算卡片 (動態更新) -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="members-settlement-cards"></div>

                <!-- 平帳匯款小指引 (動態計算) -->
                <div class="sticky-note p-4 text-xs text-stone-800 leading-relaxed flex items-start gap-3" id="settlement-guide-box"></div>

                <!-- 📊 Google 試算表已登記公費項目 (動態列表) -->
                <div class="cute-card p-5 border-2 border-stone-200 space-y-3 bg-white/95">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-stone-100 gap-2">
                        <div class="flex items-center gap-2">
                            <span class="text-base">📋</span>
                            <h4 class="text-sm font-black text-stone-800">Google 試算表已登記公費支出明細</h4>
                            <span class="cute-pill bg-emerald-100 text-emerald-800 text-[10px]" id="base-expenses-count-badge">7 筆</span>
                        </div>
                        <a href="https://docs.google.com/spreadsheets/d/1P4niaKfXpHnrlVkiexFmxa2Q0U7kwOvj6yUINn--WNo/edit" target="_blank" class="text-xs text-amber-800 hover:text-amber-900 font-bold flex items-center gap-1 self-start sm:self-auto">
                            <span>開啟 2026家族🇯🇵南九州 雲端試算表 ↗</span>
                        </a>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-xs text-left text-stone-700">
                            <thead class="text-[11px] text-stone-500 bg-stone-50 font-black border-b border-stone-200">
                                <tr>
                                    <th class="px-3 py-2">日期 / 天數</th>
                                    <th class="px-3 py-2">消費項目與內容</th>
                                    <th class="px-3 py-2">類別</th>
                                    <th class="px-3 py-2">付款人</th>
                                    <th class="px-3 py-2 text-right">原幣金額</th>
                                    <th class="px-3 py-2 text-right">折合台幣</th>
                                    <th class="px-3 py-2 text-center">分攤名單</th>
                                </tr>
                            </thead>
                            <tbody id="base-expenses-table-body" class="divide-y divide-stone-100">
                                <!-- JS 動態渲染公費明細 -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- 📝 旅途快速記帳小助手 -->
                <div class="bg-amber-50/50 border-2 border-amber-200 rounded-3xl p-5 space-y-4">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-amber-200">
                        <div class="flex items-center gap-2">
                            <span class="text-xl">📝</span>
                            <h4 class="text-base font-black text-stone-800">旅途即時記帳小助手</h4>
                            <span class="cute-pill bg-amber-200 text-amber-800 text-[10px]">免切換 App・即刻算平</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span id="sync-status-indicator" class="text-xs font-bold text-stone-500 flex items-center gap-1">
                                <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> <span>🟡 直寫通道未綁定（綁定後直接自動寫入試算表，免複製貼上）</span>
                            </span>
                            <button type="button" onclick="toggleWebhookSettings()" class="text-xs font-bold text-amber-800 hover:text-amber-900 underline flex items-center gap-1">
                                <span>⚙️</span> Google 試算表串接設定
                            </button>
                        </div>
                    </div>

                    <!-- 串接設定抽屜 -->
                    <div id="webhook-settings-drawer" class="hidden bg-white p-4 rounded-2xl border-2 border-amber-300 space-y-3 text-xs">
                        <div class="flex items-start justify-between">
                            <div>
                                <div class="font-black text-stone-800 text-sm">🔗 Google 試算表全自動同步 Webhook</div>
                                <p class="text-stone-500 mt-0.5">在您的 Google Sheet 部署 Apps Script 後貼上網址，網頁記帳將自動秒速新增至試算表！</p>
                            </div>
                            <span class="cute-pill bg-sky-100 text-sky-700">雲端免手動</span>
                        </div>
                        <div class="space-y-1">
                            <label class="text-stone-600 font-bold">Google Apps Script Webhook 網址：</label>
                            <div class="flex gap-2">
                                <input type="url" id="webhook-url-input" placeholder="https://script.google.com/macros/s/.../exec" class="flex-1 bg-stone-50 border border-stone-200 rounded-xl px-3 py-2 text-xs font-mono text-stone-800 focus:outline-none focus:border-amber-400">
                                <button type="button" onclick="saveGoogleWebhookUrl()" class="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold transition">儲存網址</button>
                            </div>
                        </div>
                        <div class="bg-stone-50 p-3 rounded-xl border border-stone-200 space-y-1.5 text-[11px] text-stone-600">
                            <div class="font-bold text-stone-800 flex items-center justify-between">
                                <span>💡 30 秒啟用教學：</span>
                                <button type="button" onclick="copyAppsScriptCode()" class="text-amber-700 hover:underline font-bold">📋 複製 Apps Script 程式碼</button>
                            </div>
                            <ol class="list-decimal list-inside space-y-1">
                                <li>打開您的 Google 試算表 ➔ 點選頂端【擴充功能】➔【Apps Script】。</li>
                                <li>點擊右上角【📋 複製 Apps Script 程式碼】，完整貼上到編輯器並存檔。</li>
                                <li>點擊右上角【部署】➔【新增部署】➔ 選擇【網頁應用程式】，存取權限選【所有人】後部署。</li>
                                <li>複製取得的「網頁應用程式網址」貼入上方輸入框並點擊「儲存網址」即連線成功！</li>
                            </ol>
                        </div>
                    </div>

                    <!-- 記帳表單 -->
                    <form onsubmit="handleNewExpenseSubmit(event)" class="space-y-3">
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
                            <div>
                                <label class="font-bold text-stone-600 block mb-1">📅 消費日期：</label>
                                <select id="exp-date" class="w-full bg-white border border-stone-200 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none focus:border-amber-400">
                                    <option value="2026-12-22">12/22 (二) Day 1 抵達熊本</option>
                                    <option value="2026-12-23">12/23 (三) Day 2 阿蘇黑川</option>
                                    <option value="2026-12-24">12/24 (四) Day 3 高千穗宮崎</option>
                                    <option value="2026-12-25">12/25 (五) Day 4 日南鹿兒島</option>
                                    <option value="2026-12-26">12/26 (六) Day 5 櫻島仙巖園</option>
                                    <option value="2026-12-27">12/27 (日) Day 6 霧島人吉</option>
                                    <option value="2026-12-28">12/28 (一) Day 7 熊本返台</option>
                                </select>
                            </div>

                            <div>
                                <label class="font-bold text-stone-600 block mb-1">🏷️ 消費項目名稱：</label>
                                <input type="text" id="exp-item" placeholder="例如：黑亭拉麵 / 阿蘇加油 / 門票" required class="w-full bg-white border border-stone-200 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none focus:border-amber-400">
                            </div>

                            <div>
                                <label class="font-bold text-stone-600 block mb-1">📂 消費類別：</label>
                                <select id="exp-category" class="w-full bg-white border border-stone-200 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none focus:border-amber-400">
                                    <option value="餐飲美食">🍽️ 餐飲美食</option>
                                    <option value="交通加油">🚗 交通加油 (租車/油錢/過路費)</option>
                                    <option value="門票活動">🎟️ 門票活動 (划船/纜車/門票)</option>
                                    <option value="購物採買">🛍️ 購物採買 (伴手禮/超市宵夜)</option>
                                    <option value="旅宿費用">🏡 旅宿費用</option>
                                    <option value="其他雜支">📦 其他雜支</option>
                                </select>
                            </div>

                            <div>
                                <label class="font-bold text-stone-600 block mb-1">💳 誰先墊付：</label>
                                <select id="exp-payer" class="w-full bg-white border border-stone-200 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none focus:border-amber-400">
                                    <option value="achun">🌸 首席導遊 阿純 先墊付</option>
                                    <option value="alu">🐻 總務大臣 阿嚕 先墊付</option>
                                    <option value="ayee">🌼 美食評鑑官 阿姨 先墊付</option>
                                    <option value="yijhang">🎩 榮譽總指揮 姨丈 先墊付</option>
                                </select>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs items-end">
                            <div>
                                <label class="font-bold text-stone-600 block mb-1">💴 金額 (可輸入 JPY 或 TWD)：</label>
                                <div class="flex gap-2">
                                    <input type="number" id="exp-amount" placeholder="金額" required min="1" oninput="syncExpenseCurrencyCalc()" class="flex-1 bg-white border border-stone-200 rounded-xl px-3 py-2 text-sm font-black font-mono text-stone-800 focus:outline-none focus:border-amber-400">
                                    <select id="exp-currency" onchange="syncExpenseCurrencyCalc()" class="bg-white border border-stone-200 rounded-xl px-2 py-2 text-xs font-bold text-stone-700">
                                        <option value="JPY">¥ JPY</option>
                                        <option value="TWD">NT$ TWD</option>
                                    </select>
                                </div>
                            </div>

                            <div class="bg-white p-2.5 rounded-xl border border-stone-200 flex items-center justify-between">
                                <span class="text-stone-400 font-bold">換算折合：</span>
                                <span class="font-mono font-black text-amber-800 text-sm" id="exp-converted-preview">NT$ 0</span>
                            </div>

                            <div>
                                <label class="font-bold text-stone-600 block mb-1">📝 備註 (選填)：</label>
                                <input type="text" id="exp-note" placeholder="例如：超商宵夜草莓" class="w-full bg-white border border-stone-200 rounded-xl px-3 py-2 text-xs font-medium text-stone-800 focus:outline-none focus:border-amber-400">
                            </div>
                        </div>

                        <!-- 誰分攤 -->
                        <div class="flex flex-wrap items-center justify-between gap-3 pt-2">
                            <div class="flex flex-wrap items-center gap-3 text-xs font-bold text-stone-700">
                                <span class="text-stone-500">分攤成員：</span>
                                <label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" id="split-achun" checked class="rounded text-amber-600"> <span id="label-split-achun">首席導遊 阿純</span></label>
                                <label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" id="split-alu" checked class="rounded text-amber-600"> <span id="label-split-alu">總務大臣 阿嚕</span></label>
                                <label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" id="split-aunt" checked class="rounded text-amber-600"> <span id="label-split-ayee">美食評鑑官 阿姨</span></label>
                                <label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" id="split-uncle" checked class="rounded text-amber-600"> <span id="label-split-yijhang">榮譽總指揮 姨丈</span></label>
                            </div>

                            <button type="submit" class="px-5 py-2.5 rounded-2xl bg-amber-600 hover:bg-amber-700 text-white font-black text-xs flex items-center gap-1.5 shadow-md shadow-amber-200 transition">
                                <span>➕</span> 儲存這筆花費並重算分帳
                            </button>
                        </div>
                    </form>

                    <!-- 新增記帳列表清單 -->
                    <div class="pt-3 border-t border-amber-200 space-y-2">
                        <div class="flex items-center justify-between">
                            <h5 class="text-xs font-black text-stone-700 flex items-center gap-1.5">
                                <span>📋</span> 本次旅途新增記帳明細 (<span id="custom-expense-count">0</span> 筆)：
                            </h5>
                            <button type="button" onclick="copyAllExpensesTsv()" class="text-xs text-amber-800 hover:text-amber-900 font-bold flex items-center gap-1">
                                <span>📋</span> 📤 匯出純文字備份 (TSV)
                            </button>
                        </div>
                        <div id="custom-expenses-list" class="space-y-1.5 max-h-60 overflow-y-auto pr-1"></div>
                    </div>
                </div>
            </div>
        </section>
        <!-- TAB 4: 🎴 南九州自駕集章巡禮 ＆ 家族微電影靈感 -->
        <section id="tab-content-stamps" class="tab-content hidden space-y-6">
            <div class="cute-card p-6 relative border-2 border-red-200 bg-white space-y-6">
                <div class="washi-tape washi-tape-gold"></div>

                <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b-2 border-red-50 gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="cute-pill bg-red-100 text-red-800 font-black">🏮 御朱印風觀光巡禮</span>
                            <span class="cute-pill bg-amber-100 text-amber-800 font-bold">🎬 家族微電影鏡頭建議</span>
                            <span class="text-xs text-stone-400">溫馨自然留影・留下一生珍藏的家庭回憶</span>
                        </div>
                        <h3 class="text-xl font-black text-stone-800 mt-2 flex items-center gap-2">
                            <span>🎴</span> 南九州自駕集章巡禮 ＆ 家族回憶底片
                        </h3>
                        <p class="text-xs text-stone-500 mt-1">
                            收集 12 處日式觀光印記・自然捕捉全家人最真實開心的電影感鏡頭・解鎖家族榮譽大師勳章！
                        </p>
                    </div>

                    <!-- 快速操作按鈕 -->
                    <div class="flex items-center gap-2 self-start md:self-auto shrink-0">
                        <button type="button" onclick="unlockAllStamps()" class="px-3.5 py-1.5 rounded-full bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-300 text-xs font-bold transition active:scale-95 shadow-2xs">
                            ✨ 一鍵全亮 (預覽)
                        </button>
                        <button type="button" onclick="resetAllStamps()" class="px-3.5 py-1.5 rounded-full bg-stone-100 hover:bg-stone-200 text-stone-600 text-xs font-bold transition active:scale-95">
                            🔄 重設進度
                        </button>
                    </div>
                </div>

                <!-- 全家探索進度條 -->
                <div class="bg-gradient-to-r from-red-50 via-amber-50 to-orange-50 rounded-2xl p-4 border border-red-200 space-y-2.5">
                    <div class="flex items-center justify-between text-xs font-bold">
                        <span class="text-stone-800 flex items-center gap-1.5">
                            <span class="text-base">⛩️</span>
                            <span>全家南九州探索進度：</span>
                            <span id="stamps-count-label" class="font-mono text-red-700 font-black text-sm">0 / 12</span>
                        </span>
                        <span id="stamps-percent-label" class="font-mono text-red-600 font-black text-sm">0%</span>
                    </div>
                    <div class="w-full bg-white/80 rounded-full h-3.5 p-0.5 border border-red-200 shadow-inner overflow-hidden">
                        <div id="stamps-progress-bar" class="h-full rounded-full bg-gradient-to-r from-red-500 via-amber-500 to-emerald-500 transition-all duration-500 shadow-sm" style="width: 0%;"></div>
                    </div>
                    <div class="text-[11px] text-stone-500 flex items-center justify-between">
                        <span>💡 每抵達一個景點，點擊右側日式印章即可蓋印記錄！</span>
                        <span class="font-bold text-amber-700" id="stamps-status-hint">準備啟程出發 ❄️</span>
                    </div>
                </div>

                <!-- 12 大日式集章卡片清單 -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="stamps-grid-container"></div>

                <!-- 家族榮譽大師成就榜 -->
                <div class="pt-6 border-t-2 border-stone-100 space-y-4">
                    <div class="flex items-center justify-between">
                        <div>
                            <h4 class="text-base font-black text-stone-800 flex items-center gap-2">
                                <span>🎖️</span> 家族專屬榮譽大師成就榜
                            </h4>
                            <p class="text-xs text-stone-500 mt-0.5">晚餐居酒屋小酌時秀給全家人看，榮譽感爆棚的專屬頭銜！</p>
                        </div>
                        <span class="cute-pill bg-purple-100 text-purple-800 font-bold text-xs" id="badges-unlocked-count">已解鎖 0 / 6</span>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5" id="badges-grid-container"></div>
                </div>

                <!-- 家族旅行心情留言板 ＆ 拍立得時光牆 -->
                <div class="pt-6 border-t-2 border-stone-100 space-y-4">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div>
                            <h4 class="text-base font-black text-stone-800 flex items-center gap-2">
                                <span>💌</span> 家族旅行心情留言板 ＆ 拍立得時光牆
                            </h4>
                            <p class="text-xs text-stone-500 mt-0.5">隨手寫下一句話、紀錄溫馨當下・全家人隨時都能回味感動！</p>
                        </div>
                        <span class="cute-pill bg-rose-100 text-rose-800 font-bold text-xs self-start sm:self-auto" id="family-notes-count">0 則心情紀錄</span>
                    </div>

                    <!-- 自由心情小便利貼發布區 -->
                    <div class="bg-gradient-to-r from-amber-50/70 via-rose-50/50 to-orange-50/70 rounded-2xl p-4 border border-amber-200/80 space-y-3">
                        <div class="flex flex-wrap items-center justify-between gap-2">
                            <div class="flex items-center gap-2">
                                <span class="text-xs font-bold text-stone-700">✍️ 留言身分：</span>
                                <select id="family-msg-sender" onchange="toggleCustomSender(this.value)" class="bg-white border border-stone-200 rounded-xl px-2.5 py-1 text-xs font-bold text-stone-700 focus:outline-none focus:border-amber-400">
                                    <option value="全家大家庭 🏠">全家大家庭 🏠</option>
                                    <option value="司機兼導遊 🚗">司機兼導遊 🚗</option>
                                    <option value="隨行攝影師 📷">隨行攝影師 📷</option>
                                    <option value="美食部長 🍜">美食部長 🍜</option>
                                    <option value="總務財務長 💰">總務財務長 💰</option>
                                    <option value="開心果代表 🍓">開心果代表 🍓</option>
                                    <option value="自訂稱呼 ✍️">自訂稱呼...</option>
                                </select>
                                <input type="text" id="family-msg-custom-sender" class="hidden bg-white border border-stone-200 rounded-xl px-2.5 py-1 text-xs text-stone-700 focus:outline-none focus:border-amber-400 w-28" placeholder="輸入您的稱呼">
                            </div>

                            <!-- 心情表情快捷選擇 -->
                            <div class="flex items-center gap-1 bg-white/80 p-1 rounded-xl border border-stone-200">
                                <button type="button" onclick="selectFamilyMood('😊')" data-emoji="😊" class="mood-emoji-btn text-sm px-1.5 py-0.5 rounded-lg transition active:scale-90 ring-2 ring-amber-400 bg-amber-100" title="開心感動">😊</button>
                                <button type="button" onclick="selectFamilyMood('😋')" data-emoji="😋" class="mood-emoji-btn text-sm px-1.5 py-0.5 rounded-lg transition active:scale-90" title="大飽口福">😋</button>
                                <button type="button" onclick="selectFamilyMood('♨️')" data-emoji="♨️" class="mood-emoji-btn text-sm px-1.5 py-0.5 rounded-lg transition active:scale-90" title="放鬆溫泉">♨️</button>
                                <button type="button" onclick="selectFamilyMood('✨')" data-emoji="✨" class="mood-emoji-btn text-sm px-1.5 py-0.5 rounded-lg transition active:scale-90" title="美景震撼">✨</button>
                                <button type="button" onclick="selectFamilyMood('🚗')" data-emoji="🚗" class="mood-emoji-btn text-sm px-1.5 py-0.5 rounded-lg transition active:scale-90" title="自駕順暢">🚗</button>
                            </div>
                        </div>

                        <div class="flex flex-col sm:flex-row gap-2">
                            <input type="text" id="family-msg-text" onkeydown="if(event.key==='Enter') addFamilyMessage()" class="flex-1 bg-white border border-stone-200 focus:border-amber-400 rounded-xl px-3 py-2 text-xs text-stone-800 placeholder-stone-400 focus:outline-none transition shadow-2xs" placeholder="寫下一句話、想對全家說的暖心叮嚀或當下的心情（選填，長輩不寫也完全沒關係～）">
                            <button type="button" onclick="addFamilyMessage()" class="px-4 py-2 bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-700 hover:to-rose-700 text-white font-black text-xs rounded-xl shadow-2xs active:scale-95 transition shrink-0 flex items-center justify-center gap-1.5">
                                <span>📌</span> <span>貼上留言</span>
                            </button>
                        </div>
                    </div>

                    <!-- 留言貼紙與拍立得回憶牆雙分頁/整合呈現 -->
                    <div class="space-y-3">
                        <div class="flex items-center justify-between pb-1">
                            <span class="text-xs font-bold text-stone-600 flex items-center gap-1.5">
                                <span>📌</span> <span>家族便利貼 ＆ 各站回憶手記牆</span>
                            </span>
                            <span class="text-[11px] text-stone-400">點擊拍立得可查看大圖</span>
                        </div>
                        <div id="family-board-container" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3"></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 5: 旅宿與預約 -->
        <section id="tab-content-stays" class="tab-content hidden space-y-6">
            <!-- 機票 -->
            <div>
                <h3 class="text-lg font-black text-stone-800 mb-3 flex items-center gap-2">
                    <span>✈️</span> 中華航空直飛來回機票
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="cute-card p-5 relative border-2 border-sky-200 bg-gradient-to-b from-white to-sky-50">
                        <div class="flex items-center justify-between pb-2 border-b border-sky-100">
                            <span class="cute-pill bg-sky-100 text-sky-700">去程 12/22 (二)</span>
                            <span class="font-mono font-bold text-sky-700">華航 CI194 直飛</span>
                        </div>
                        <div class="flex items-center justify-between py-3">
                            <div>
                                <div class="text-2xl font-black text-stone-800">TPE</div>
                                <div class="text-xs text-stone-400">台北桃園 (T2)</div>
                                <div class="text-sm font-black text-sky-600 mt-0.5">14:30</div>
                            </div>
                            <div class="flex flex-col items-center">
                                <div class="text-xs text-stone-400">2 小時航程</div>
                                <div class="text-sky-500 text-base">✈️💨</div>
                            </div>
                            <div class="text-right">
                                <div class="text-2xl font-black text-stone-800">KMJ</div>
                                <div class="text-xs text-stone-400">熊本機場</div>
                                <div class="text-sm font-black text-sky-600 mt-0.5">17:30</div>
                            </div>
                        </div>
                        <div class="text-xs text-stone-500 pt-2 border-t border-sky-100 flex justify-between">
                            <span>4人同行 ｜ 托運 23kg + 隨身 7kg</span>
                            <span class="font-bold text-sky-600">機票費用：NT$ {flight_cost_twd:,.0f}</span>
                        </div>
                    </div>

                    <div class="cute-card p-5 relative border-2 border-amber-200 bg-gradient-to-b from-white to-amber-50">
                        <div class="flex items-center justify-between pb-2 border-b border-amber-100">
                            <span class="cute-pill bg-amber-100 text-amber-700">回程 12/28 (一)</span>
                            <span class="font-mono font-bold text-amber-700">華航 CI195 直飛</span>
                        </div>
                        <div class="flex items-center justify-between py-3">
                            <div>
                                <div class="text-2xl font-black text-stone-800">KMJ</div>
                                <div class="text-xs text-stone-400">熊本新航廈</div>
                                <div class="text-sm font-black text-amber-600 mt-0.5">18:35</div>
                            </div>
                            <div class="flex flex-col items-center">
                                <div class="text-xs text-stone-400">2.5 小時航程</div>
                                <div class="text-amber-500 text-base">✈️💨</div>
                            </div>
                            <div class="text-right">
                                <div class="text-2xl font-black text-stone-800">TPE</div>
                                <div class="text-xs text-stone-400">台北桃園 (T2)</div>
                                <div class="text-sm font-black text-amber-600 mt-0.5">20:10</div>
                            </div>
                        </div>
                        <div class="text-xs text-stone-500 pt-2 border-t border-amber-100 flex justify-between">
                            <span>提早 2 小時抵達熊本新航廈採買伴手禮</span>
                            <span class="font-bold text-emerald-700">平安返台</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 住宿安排 -->
            <div>
                <h3 class="text-lg font-black text-stone-800 mb-3 flex items-center gap-2">
                    <span>🏡</span> 6 晚旅宿安排 (已確認訂房)
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="stays-grid"></div>
            </div>

            <!-- 出發前重點預約便利貼 -->
            <div class="cute-card p-6 relative border-2 border-amber-200 space-y-4">
                <div class="washi-tape washi-tape-gold"></div>
                <div class="flex items-center justify-between pb-3 border-b-2 border-stone-100">
                    <div>
                        <h3 class="text-lg font-black text-stone-800 flex items-center gap-2">
                            <span>📌</span> 出發前重點預約便利貼 (共 5 項)
                        </h3>
                        <p class="text-xs text-stone-500 mt-1">划船、雪胎自駕、溫泉與日文駕照譯本～照著打勾勾！</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div class="sticky-note p-4 space-y-2 transform -rotate-1 hover:rotate-0 transition">
                        <div class="flex items-center justify-between">
                            <span class="font-black text-stone-800 text-sm">🚗 租車 (雪胎指定)</span>
                            <span class="cute-pill bg-amber-200 text-amber-800">⏳ 待確認</span>
                        </div>
                        <div class="text-[11px] font-bold text-amber-700">出發前 2～3 個月 ｜ Toyota / Times</div>
                        <p class="text-xs text-stone-700 leading-relaxed">
                            務必備註「スタッドレスタイヤ (雪胎)」，阿蘇黑川冬季必備；確認含 ETC 機與免責保險。
                        </p>
                    </div>

                    <div class="sticky-note p-4 space-y-2 !bg-pink-50 !border-pink-200 transform rotate-1 hover:rotate-0 transition">
                        <div class="flex items-center justify-between">
                            <span class="font-black text-stone-800 text-sm">🚣 高千穗峽租船</span>
                            <span class="cute-pill bg-pink-200 text-pink-700">⏳ 1週前09:00搶</span>
                        </div>
                        <div class="text-[11px] font-bold text-pink-600">搭乘日前 1 週 09:00 ｜ 觀光協會官網</div>
                        <p class="text-xs text-stone-700 leading-relaxed">
                            一艘船限乘 3 人，線上刷卡預約，搶熱門下午時段，穿過真名井瀑布超美！
                        </p>
                    </div>

                    <div class="sticky-note p-4 space-y-2 !bg-emerald-50 !border-emerald-200 transform -rotate-1 hover:rotate-0 transition">
                        <div class="flex items-center justify-between">
                            <span class="font-black text-stone-800 text-sm">♨️ 黑川溫泉山彥旅館</span>
                            <span class="cute-pill bg-emerald-200 text-emerald-800">✅ 已下訂！</span>
                        </div>
                        <div class="text-[11px] font-bold text-emerald-700">費用 JPY 70,400 (約 NT$ 14,625)</div>
                        <p class="text-xs text-stone-700 leading-relaxed">
                            冬季黑川竹燈祭超熱門，山彥旅館日式和室朝食方案與仙人露天風呂都訂好囉！晚餐可於黑川老街漫步享用在地居酒鄉土料理。
                        </p>
                    </div>

                    <div class="sticky-note p-4 space-y-2 !bg-sky-50 !border-sky-200 transform rotate-1 hover:rotate-0 transition">
                        <div class="flex items-center justify-between">
                            <span class="font-black text-stone-800 text-sm">📄 VJW ＆ 日文駕照譯本</span>
                            <span class="cute-pill bg-sky-200 text-sky-700">⏳ 出發前1~2週</span>
                        </div>
                        <div class="text-[11px] font-bold text-sky-600">Visit Japan Web ＆ 台灣監理站</div>
                        <p class="text-xs text-stone-700 leading-relaxed">
                            填寫入境與海關申報 QR；記得帶<strong>「台灣駕照正本」＋「日文譯本正本」</strong>（非國際駕照）。
                        </p>
                    </div>

                    <div class="sticky-note p-4 space-y-2 transform -rotate-1 hover:rotate-0 transition">
                        <div class="flex items-center justify-between">
                            <span class="font-black text-stone-800 text-sm">🍱 人吉鰻魚 / 壽庵黑豚</span>
                            <span class="cute-pill bg-amber-200 text-amber-800">⏳ 當日提早排</span>
                        </div>
                        <div class="text-[11px] font-bold text-amber-700">百年碳火香氣 / 線上訂位</div>
                        <p class="text-xs text-stone-700 leading-relaxed">
                            人吉百年老店「上村うなぎや」建議 11:00 前抵達排隊；鹿兒島「壽庵」提前官網訂位！
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 兼容空標籤 -->
        <div id="tab-content-bookings" class="hidden"></div>

        <!-- TAB 6: 行李檢查表 (徹底修復重來錯誤) -->
        <section id="tab-content-checklist" class="tab-content hidden space-y-6">
            <div class="cute-card p-6 relative border-2 border-emerald-200 space-y-6">
                <div class="washi-tape washi-tape-green"></div>

                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b-2 border-stone-100 gap-4">
                    <div>
                        <h3 class="text-lg font-black text-stone-800 flex items-center gap-2">
                            <span>🎒</span> 南九州自駕行李打包檢核清單
                        </h3>
                        <p class="text-xs text-stone-500 mt-1">點一下小圓圈打勾勾，會自動記錄在瀏覽器裡唷！</p>
                    </div>
                    <div class="flex items-center gap-2.5">
                        <button onclick="resetPackingChecklist()" id="btn-reset-packing" class="px-3.5 py-1.5 rounded-full bg-stone-100 text-stone-600 hover:bg-red-50 hover:text-red-600 text-xs font-bold transition">
                            全部重來 (清空)
                        </button>
                        <button onclick="checkAllPacking()" id="btn-all-packed" class="px-3.5 py-1.5 rounded-full bg-stone-100 text-stone-500 border border-stone-200 hover:bg-emerald-50 hover:text-emerald-700 text-xs font-bold transition">
                            一鍵全部打包 🎉
                        </button>
                    </div>
                </div>

                <!-- ❄️ 2026 南九州 7 天冬季氣候分析與防寒打包對照指南 -->
                <div class="bg-gradient-to-br from-sky-50 via-blue-50/40 to-indigo-50/50 p-5 rounded-2xl border-2 border-sky-200 space-y-4">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-sky-200/70 gap-2">
                        <div class="flex items-center gap-2">
                            <span class="text-2xl drop-shadow-xs">❄️</span>
                            <div>
                                <h4 class="text-sm font-black text-slate-800">2026 南九州 7 天冬季氣候分析與防寒打包指南</h4>
                                <p class="text-xs text-slate-500 font-medium">出發日期：2026/12/22 ~ 12/28 ｜ 熊本・阿蘇・黑川・高千穗・宮崎・鹿兒島</p>
                            </div>
                        </div>
                        <span class="cute-pill bg-sky-100 text-sky-800 font-bold text-xs">洋蔥式穿法最舒適</span>
                    </div>

                    <!-- 7 天逐日天氣橫向對照卡片 -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
                        <!-- Day 1 -->
                        <div class="bg-white/95 p-3 rounded-xl border border-sky-100 shadow-2xs space-y-1">
                            <div class="flex items-center justify-between font-black">
                                <span class="text-red-600 font-mono">DAY 1 (12/22)</span>
                                <span>⛅ 晴時多雲</span>
                            </div>
                            <div class="text-slate-800 font-bold">熊本市區 (辛島町/下通)</div>
                            <div class="text-rose-600 font-mono font-black text-sm">5°C ~ 13°C</div>
                            <div class="text-[11px] text-slate-500 leading-tight">涼冷乾爽，早晚溫差大。發熱衣+針織衫+防風外套。</div>
                        </div>
                        <!-- Day 2 -->
                        <div class="bg-gradient-to-b from-sky-100/50 to-white p-3 rounded-xl border-2 border-sky-300 shadow-2xs space-y-1 relative">
                            <span class="absolute -top-2 right-2 text-[10px] bg-sky-600 text-white font-black px-1.5 py-0.5 rounded-full shadow-2xs">全趟最冷 ⚠️</span>
                            <div class="flex items-center justify-between font-black">
                                <span class="text-red-600 font-mono">DAY 2 (12/23)</span>
                                <span>❄️ 初雪結霜警戒</span>
                            </div>
                            <div class="text-slate-800 font-bold">阿蘇草千里・黑川溫泉</div>
                            <div class="text-sky-700 font-mono font-black text-sm">-1°C ~ 6°C (火口 -3°C)</div>
                            <div class="text-[11px] text-slate-600 leading-tight">山區風強！長版厚羽絨、毛帽、厚手套、防滑保暖鞋必備。</div>
                        </div>
                        <!-- Day 3 -->
                        <div class="bg-white/95 p-3 rounded-xl border border-sky-100 shadow-2xs space-y-1">
                            <div class="flex items-center justify-between font-black">
                                <span class="text-red-600 font-mono">DAY 3 (12/24)</span>
                                <span>🌤️ 山谷轉晴</span>
                            </div>
                            <div class="text-slate-800 font-bold">高千穗峽 ➔ 宮崎日向灘</div>
                            <div class="text-emerald-700 font-mono font-black text-sm">2°C ~ 12°C</div>
                            <div class="text-[11px] text-slate-500 leading-tight">高千穗峽谷涼意濃，抵達宮崎溫暖如春，外套可開襟。</div>
                        </div>
                        <!-- Day 4 -->
                        <div class="bg-white/95 p-3 rounded-xl border border-sky-100 shadow-2xs space-y-1">
                            <div class="flex items-center justify-between font-black">
                                <span class="text-red-600 font-mono">DAY 4 (12/25)</span>
                                <span>☀️ 冬日暖陽</span>
                            </div>
                            <div class="text-slate-800 font-bold">宮崎日南海岸 ➔ 鹿兒島</div>
                            <div class="text-amber-700 font-mono font-black text-sm">7°C ~ 15°C</div>
                            <div class="text-[11px] text-slate-500 leading-tight">海濱紫外線強，青島與摩艾石像需多步行，輕便好走。</div>
                        </div>
                        <!-- Day 5 -->
                        <div class="bg-white/95 p-3 rounded-xl border border-sky-100 shadow-2xs space-y-1">
                            <div class="flex items-center justify-between font-black">
                                <span class="text-red-600 font-mono">DAY 5 (12/26)</span>
                                <span>🌤️ 晴・海風</span>
                            </div>
                            <div class="text-slate-800 font-bold">櫻島火山・鹿兒島市區</div>
                            <div class="text-rose-600 font-mono font-black text-sm">6°C ~ 14°C</div>
                            <div class="text-[11px] text-slate-500 leading-tight">渡輪甲板風大需防風帽/連帽外套，仙巖園室內暖氣足。</div>
                        </div>
                        <!-- Day 6 -->
                        <div class="bg-white/95 p-3 rounded-xl border border-sky-100 shadow-2xs space-y-1">
                            <div class="flex items-center justify-between font-black">
                                <span class="text-red-600 font-mono">DAY 6 (12/27)</span>
                                <span>⛅ 高原微涼</span>
                            </div>
                            <div class="text-slate-800 font-bold">霧島神宮・人吉 ➔ 熊本</div>
                            <div class="text-indigo-700 font-mono font-black text-sm">2°C ~ 11°C</div>
                            <div class="text-[11px] text-slate-500 leading-tight">高原參拜神宮與牧場戶外開闊，建議備好毛帽與圍巾。</div>
                        </div>
                        <!-- Day 7 -->
                        <div class="bg-white/95 p-3 rounded-xl border border-sky-100 shadow-2xs space-y-1">
                            <div class="flex items-center justify-between font-black">
                                <span class="text-red-600 font-mono">DAY 7 (12/28)</span>
                                <span>☀️ 舒適返台</span>
                            </div>
                            <div class="text-slate-800 font-bold">熊本城・成趣園 ➔ 機場</div>
                            <div class="text-rose-600 font-mono font-black text-sm">4°C ~ 12°C</div>
                            <div class="text-[11px] text-slate-500 leading-tight">登天守閣梯級多，穿透氣內搭+好收納輕羽絨，回台方便脫下。</div>
                        </div>
                        <!-- 穿搭核心叮嚀卡 -->
                        <div class="bg-gradient-to-br from-amber-50 to-orange-50 p-3 rounded-xl border border-amber-200 shadow-2xs space-y-1">
                            <div class="font-black text-amber-900 flex items-center gap-1">
                                <span>💡</span> 洋蔥式穿搭秘訣
                            </div>
                            <div class="text-[11px] text-amber-800 leading-tight">
                                日本<strong>室內與自駕車內暖氣極強 (22~24°C)</strong>，務必選擇<strong>開襟拉鍊毛衣/輕羽絨外套</strong>，上車即脫、下車即穿，長輩最不易感冒！
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="space-y-3">
                        <div class="flex items-center justify-between pb-2 border-b-2 border-sky-100">
                            <h4 class="text-sm font-black text-sky-600 flex items-center gap-1.5">
                                <span>📄</span> 重要證件＆駕照譯本
                            </h4>
                            <span class="cute-pill bg-sky-100 text-sky-600" id="doc-count">0/6</span>
                        </div>
                        <div class="space-y-2" id="list-documents"></div>
                    </div>

                    <div class="space-y-3">
                        <div class="flex items-center justify-between pb-2 border-b-2 border-amber-100">
                            <h4 class="text-sm font-black text-amber-600 flex items-center gap-1.5">
                                <span>👜</span> 隨身上機 (車用設備/保暖)
                            </h4>
                            <span class="cute-pill bg-amber-100 text-amber-600" id="car-count">0/6</span>
                        </div>
                        <div class="space-y-2" id="list-carry-on"></div>
                    </div>

                    <div class="space-y-3">
                        <div class="flex items-center justify-between pb-2 border-b-2 border-emerald-100">
                            <h4 class="text-sm font-black text-emerald-600 flex items-center gap-1.5">
                                <span>🧳</span> 托運行李 (衣物/溫泉用品)
                            </h4>
                            <span class="cute-pill bg-emerald-100 text-emerald-600" id="bag-count">0/6</span>
                        </div>
                        <div class="space-y-2" id="list-checked-bag"></div>
                    </div>
                </div>

                <div class="sticky-note p-3.5 text-xs text-amber-800 leading-relaxed">
                    ⚠️ <strong>自駕駕駛特別叮嚀：</strong><br>
                    • 請務必將<strong>「台灣駕照正本」＋「監理站日文譯本正本」</strong>放在隨身包包，缺一不可！<br>
                    • 行動電源（充電寶）<strong>絕對不可以放進托運行李箱</strong>，一定要隨身帶上飛機唷！
                </div>
            </div>
        </section>

        <!-- TAB 7: 工具箱與優惠券專區 -->
        <section id="tab-content-tools" class="tab-content hidden space-y-6">
            <!-- 🎟️ 折價券、優惠券專區 (可即時出示條碼與 QRcode) -->
            <div class="cute-card p-6 relative border-2 border-red-200 space-y-5">
                <div class="washi-tape washi-tape-gold"></div>

                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b-2 border-red-100 gap-3">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="cute-pill bg-red-100 text-red-700 font-black">🎟️ 旅日必備・即掃即用</span>
                            <span class="text-xs text-stone-500">免稅 10% ＋ 最高現折 7%</span>
                        </div>
                        <h4 class="text-lg font-black text-stone-800 mt-1">🎁 南九州景點・購物・藥妝・百貨折價券專區</h4>
                        <p class="text-xs text-stone-500 mt-0.5">點擊條碼可「全螢幕放大」供店員掃描！亦可按所在城市篩選，或一鍵 GPS 定位篩選身邊可用的優惠券。</p>
                    </div>

                    <button type="button" onclick="detectUserLocationForCoupons()" class="px-4 py-2 rounded-2xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-700 hover:to-rose-700 text-white font-black text-xs flex items-center justify-center gap-1.5 shadow-sm transition">
                        <span>🧭</span> 一鍵定位篩選周邊優惠券
                    </button>
                </div>

                <!-- 優惠券地區篩選列 -->
                <div class="flex flex-wrap items-center justify-between gap-2 bg-amber-50/60 p-3 rounded-2xl border border-amber-200 text-xs font-bold">
                    <div class="flex flex-wrap items-center gap-1.5">
                        <span class="text-stone-500 text-[11px] font-black">📍 分類篩選：</span>
                        <button type="button" onclick="filterCoupons('all')" id="cfilter-all" class="cfilter-btn px-3 py-1 rounded-full bg-red-600 text-white shadow-xs transition text-[11px] font-bold">全部精選 (9)</button>
                        <button type="button" onclick="filterCoupons('chain')" id="cfilter-chain" class="cfilter-btn px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">🇯🇵 連鎖購物・免稅 (6)</button>
                        <button type="button" onclick="filterCoupons('drive_local')" id="cfilter-drive_local" class="cfilter-btn px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">🚗 自駕省錢＆溫泉情報 (3)</button>
                        <button type="button" onclick="filterCoupons('kumamoto')" id="cfilter-kumamoto" class="cfilter-btn px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">📍 熊本</button>
                        <button type="button" onclick="filterCoupons('kagoshima')" id="cfilter-kagoshima" class="cfilter-btn px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">📍 鹿兒島</button>
                        <button type="button" onclick="filterCoupons('miyazaki')" id="cfilter-miyazaki" class="cfilter-btn px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">📍 宮崎・日南</button>
                    </div>
                    <span id="coupon-location-status" class="text-[11px] text-amber-800 font-bold"></span>
                </div>

                <!-- 優惠券卡片列表 Grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5" id="coupons-grid"></div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="cute-card p-6 relative border-2 border-red-200 space-y-4">
                    <div class="washi-tape"></div>
                    <div class="flex items-center justify-between">
                        <h4 class="text-base font-black text-stone-800 flex items-center gap-2">
                            <span>💱</span> 日圓 ⇄ 台幣可愛小算盤
                        </h4>
                        <span class="cute-pill bg-red-100 text-red-700">匯率約 0.2078</span>
                    </div>

                    <div class="bg-red-50/50 rounded-2xl p-4 border border-red-100 space-y-3">
                        <div>
                            <label class="text-xs text-stone-500 font-bold">日圓金額 (JPY)：</label>
                            <div class="relative mt-1">
                                <input type="number" id="calc-jpy" value="10000" oninput="calcFromJpy(this.value)" class="w-full bg-white border-2 border-stone-200 rounded-xl px-3.5 py-2 text-base font-black font-mono text-stone-800 focus:outline-none focus:border-red-400">
                                <span class="absolute right-3.5 top-2.5 text-sm font-black text-stone-400">¥ 日圓</span>
                            </div>
                        </div>

                        <div class="flex justify-center text-stone-400 text-lg">⇅</div>

                        <div>
                            <label class="text-xs text-stone-500 font-bold">折合台幣 (TWD)：</label>
                            <div class="relative mt-1">
                                <input type="number" id="calc-twd" value="2078" oninput="calcFromTwd(this.value)" class="w-full bg-white border-2 border-stone-200 rounded-xl px-3.5 py-2 text-base font-black font-mono text-red-600 focus:outline-none focus:border-red-400">
                                <span class="absolute right-3.5 top-2.5 text-sm font-black text-red-600">NT$ 台幣</span>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-4 gap-2 text-center text-xs">
                        <div class="p-2 rounded-xl bg-white border border-stone-200">
                            <div class="text-stone-400">¥ 1,000</div>
                            <div class="font-black text-stone-800 mt-0.5">≈ NT$ 208</div>
                        </div>
                        <div class="p-2 rounded-xl bg-white border border-stone-200">
                            <div class="text-stone-400">¥ 5,000</div>
                            <div class="font-black text-stone-800 mt-0.5">≈ NT$ 1,039</div>
                        </div>
                        <div class="p-2 rounded-xl bg-white border border-stone-200">
                            <div class="text-stone-400">¥ 10,000</div>
                            <div class="font-black text-stone-800 mt-0.5">≈ NT$ 2,078</div>
                        </div>
                        <div class="p-2 rounded-xl bg-white border border-stone-200">
                            <div class="text-stone-400">¥ 30,000</div>
                            <div class="font-black text-stone-800 mt-0.5">≈ NT$ 6,234</div>
                        </div>
                    </div>
                </div>

                <div class="cute-card p-6 relative border-2 border-sky-200 space-y-4">
                    <div class="washi-tape washi-tape-blue"></div>
                    <h4 class="text-base font-black text-stone-800 flex items-center gap-2">
                        <span>🚨</span> 九州急難救助＆道路救援通訊錄
                    </h4>
                    <div class="space-y-2.5 text-xs font-medium">
                        <div class="p-3 rounded-2xl bg-red-50 border border-red-200 flex justify-between items-center">
                            <div>
                                <div class="font-black text-red-700">駐福岡辦事處 (急難專線)</div>
                                <div class="text-stone-400 text-[11px]">九州全區護照遺失或危急求助</div>
                            </div>
                            <a href="tel:+819019229740" class="font-mono font-bold text-white bg-red-600 px-3 py-1 rounded-full hover:bg-red-700 shadow-sm">+81-90-1922-9740</a>
                        </div>

                        <div class="p-3 rounded-2xl bg-stone-50 border border-stone-200 flex justify-between items-center">
                            <div>
                                <div class="font-bold text-stone-800">外交部海外急難救助 24hr</div>
                                <div class="text-stone-400 text-[11px]">全球免付費專線</div>
                            </div>
                            <a href="tel:+886800085095" class="font-mono font-bold text-stone-700 bg-white px-3 py-1 rounded-full border border-stone-200 hover:bg-stone-50">+886-800-085-095</a>
                        </div>

                        <div class="p-3 rounded-2xl bg-stone-50 border border-stone-200 flex justify-between items-center">
                            <div>
                                <div class="font-bold text-stone-800">JAF 日本道路救援 (爆胎/拋錨)</div>
                                <div class="text-stone-400 text-[11px]">自駕突發狀況求助</div>
                            </div>
                            <a href="tel:0570008139" class="font-mono font-bold text-stone-700 bg-white px-3 py-1 rounded-full border border-stone-200 hover:bg-stone-50">#8139 / 0570-00-8139</a>
                        </div>

                        <div class="p-3 rounded-2xl bg-emerald-50 border border-emerald-200 flex justify-between items-center">
                            <div>
                                <div class="font-bold text-emerald-800">日本警察局 (110) ｜ 救護車 (119)</div>
                                <div class="text-stone-400 text-[11px]">事故報案 (110) ｜ 急病送醫 (119)</div>
                            </div>
                            <span class="font-mono font-black text-emerald-700">撥打 110 / 119</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <footer class="bg-white/80 border-t-2 border-stone-100 py-4 px-4 text-center text-xs text-stone-400 mt-8 font-medium">
        🎄 2026 南九州聖誕冬季自駕旅行手帳 ｜ 建立時間：{now_str} ｜ 祝大家聖誕假期平安快樂！❄️✨
    </footer>

    <div id="toast" class="fixed bottom-6 right-6 z-50 bg-white border-2 border-red-300 text-stone-800 px-4 py-2.5 rounded-2xl shadow-xl text-xs font-bold transform translate-y-16 opacity-0 transition-all duration-300 flex items-center gap-2">
        <span>🎄</span>
        <span id="toast-msg">已完成操作！</span>
    </div>

    <!-- 核心互動邏輯與飄雪動效 (使用 JSON 安全注入，杜絕語法錯誤) -->
    <script>
        const TRIP_DATA = {trip_json_str};
        const MAP_LANDMARKS = {landmarks_json_str};

        let isSnowing = true;
        let snowAnimationId = null;
        let showRoutes = true;
        let selectedPinId = null;

        document.addEventListener('DOMContentLoaded', () => {{
            try {{
                initSnow();
                initCountdown();
                initTimelineDays();
                renderDayDetails(0);
                setDashboardViewMode(dashboardViewMode);
                renderAccommodations();
                initChecklist();
                initHandDrawnMap();
                initCosts();
                renderRestaurants();
                initStamps();
                updateTopClock();
                setInterval(updateTopClock, 1000);
            }} catch (err) {{
                console.error("Initialization error:", err);
            }}
        }});

        function fireChristmasCheer() {{
            confetti({{
                particleCount: 70,
                spread: 60,
                origin: {{ y: 0.6 }},
                colors: ['#c92a2a', '#2d6a4f', '#f59f00', '#ffffff', '#74c0fc']
            }});
        }}

        function initSnow() {{
            const canvas = document.getElementById('snow-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');

            function resize() {{
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }}
            window.addEventListener('resize', resize);
            resize();

            const snowflakes = [];
            const count = 45;

            for (let i = 0; i < count; i++) {{
                snowflakes.push({{
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    radius: Math.random() * 3 + 1,
                    density: Math.random() * count,
                    speed: Math.random() * 0.8 + 0.4,
                    wind: Math.random() * 0.5 - 0.25
                }});
            }}

            function draw() {{
                if (!isSnowing) return;
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = 'rgba(255, 255, 255, 0.75)';
                ctx.beginPath();
                for (let i = 0; i < count; i++) {{
                    const f = snowflakes[i];
                    ctx.moveTo(f.x, f.y);
                    ctx.arc(f.x, f.y, f.radius, 0, Math.PI * 2, true);
                }}
                ctx.fill();

                for (let i = 0; i < count; i++) {{
                    const f = snowflakes[i];
                    f.y += f.speed;
                    f.x += f.wind;
                    if (f.y > canvas.height) {{
                        f.y = -5;
                        f.x = Math.random() * canvas.width;
                    }}
                }}
                snowAnimationId = requestAnimationFrame(draw);
            }}

            draw();
        }}

        function toggleSnow() {{
            isSnowing = !isSnowing;
            const btn = document.getElementById('snow-btn-text');
            const canvas = document.getElementById('snow-canvas');
            if (isSnowing) {{
                btn.textContent = '下雪中';
                canvas.style.display = 'block';
                initSnow();
                showToast('已開啟浪漫飄雪效果 ❄️');
            }} else {{
                btn.textContent = '飄雪暫停';
                canvas.style.display = 'none';
                cancelAnimationFrame(snowAnimationId);
                showToast('已暫停飄雪效果');
            }}
        }}

        function initCountdown() {{
            const targetDateStr = TRIP_DATA.start_date + 'T14:30:00';
            const targetTime = new Date(targetDateStr).getTime();

            function update() {{
                const now = new Date().getTime();
                const diff = targetTime - now;

                if (diff <= 0) {{
                    document.getElementById('cd-days').textContent = '00';
                    document.getElementById('cd-hours').textContent = '00';
                    document.getElementById('cd-mins').textContent = '00';
                    document.getElementById('cd-secs').textContent = '00';
                    return;
                }}

                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                const secs = Math.floor((diff % (1000 * 60)) / 1000);

                document.getElementById('cd-days').textContent = String(days).padStart(2, '0');
                document.getElementById('cd-hours').textContent = String(hours).padStart(2, '0');
                document.getElementById('cd-mins').textContent = String(mins).padStart(2, '0');
                document.getElementById('cd-secs').textContent = String(secs).padStart(2, '0');
            }}

            update();
            setInterval(update, 1000);
        }}

        function updateTopClock() {{
            const now = new Date();
            const jpnTime = new Date(now.toLocaleString("en-US", {{ timeZone: "Asia/Tokyo" }}));
            const timeStr = jpnTime.toLocaleTimeString('zh-TW', {{ hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }});
            const el = document.getElementById('top-clock');
            if (el) el.textContent = `🇯🇵 熊本即時時間 ${{timeStr}} (GMT+9) ❄️`;
        }}

        function openTab(tabName) {{
            if (tabName === 'bookings') tabName = 'stays';
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.xmas-tab-btn').forEach(btn => btn.classList.remove('active'));

            const targetContent = document.getElementById('tab-content-' + tabName);
            const targetBtn = document.getElementById('tab-btn-' + tabName);

            if (targetContent) targetContent.classList.remove('hidden');
            if (targetBtn) targetBtn.classList.add('active');
            if (tabName === 'costs') initCosts();
            if (tabName === 'restaurants') renderRestaurants();
            if (tabName === 'tools') renderCoupons();
            if (tabName === 'stamps') initStamps();
        }}

        function initTimelineDays() {{
            const bar = document.getElementById('day-selector-bar');
            if (!bar) return;
            bar.innerHTML = '';
            TRIP_DATA.daily_itinerary.forEach((dayPlan, idx) => {{
                const btn = document.createElement('button');
                btn.className = `xmas-day-btn px-4 py-2 rounded-2xl text-xs font-black border-2 transition flex flex-col items-center min-w-[95px] ${{idx === 0 ? 'bg-red-600 text-white border-red-600 shadow-md shadow-red-200' : 'bg-white border-stone-200 text-stone-500 hover:border-red-300 hover:text-red-600'}}`;
                btn.id = `day-btn-${{idx}}`;
                btn.onclick = () => renderDayDetails(idx);

                const shortDate = dayPlan.weekday_title.split(' ')[0];
                const weekDay = dayPlan.weekday_title.split(' ')[1] || '';

                btn.innerHTML = `
                    <span class="text-[10px] tracking-wider uppercase">DAY ${{dayPlan.day}}</span>
                    <span class="text-xs font-black mt-0.5">${{shortDate}} ${{weekDay}}</span>
                `;
                bar.appendChild(btn);
            }});
        }}

        let currentDayIndex = 0;

        function getCustomStops(dayIdx) {{
            try {{
                return JSON.parse(localStorage.getItem(`kyushu_custom_stops_day_${{dayIdx}}`) || '[]');
            }} catch (e) {{
                return [];
            }}
        }}

        function setCustomStops(dayIdx, items) {{
            localStorage.setItem(`kyushu_custom_stops_day_${{dayIdx}}`, JSON.stringify(items));
        }}

        let dashboardViewMode = localStorage.getItem('dashboard_view_mode') || 'clean';

        function setDashboardViewMode(mode) {{
            dashboardViewMode = mode;
            localStorage.setItem('dashboard_view_mode', mode);

            const btnClean = document.getElementById('btn-mode-clean');
            const btnDriver = document.getElementById('btn-mode-driver');
            const statusHint = document.getElementById('mode-status-hint');

            if (mode === 'driver') {{
                if (btnDriver) btnDriver.className = 'px-2.5 py-1 rounded-xl transition flex items-center gap-1 bg-white text-stone-800 shadow-2xs font-black';
                if (btnClean) btnClean.className = 'px-2.5 py-1 rounded-xl transition flex items-center gap-1 text-stone-500 hover:text-stone-800 font-bold';
                if (statusHint) statusHint.textContent = '🚗 自駕全配中・已展開全站停車場與參觀撇步';
                document.querySelectorAll('.timeline-detail-box').forEach(el => el.classList.remove('hidden'));
                document.querySelectorAll('[id^="arrow-tl-"]').forEach(el => el.textContent = '▴');
                showToast('已切換為「自駕全配模式」🚗');
            }} else {{
                if (btnClean) btnClean.className = 'px-2.5 py-1 rounded-xl transition flex items-center gap-1 bg-white text-stone-800 shadow-2xs font-black';
                if (btnDriver) btnDriver.className = 'px-2.5 py-1 rounded-xl transition flex items-center gap-1 text-stone-500 hover:text-stone-800 font-bold';
                if (statusHint) statusHint.textContent = '🌿 清爽簡潔中・點擊小標籤可展開自駕細節';
                document.querySelectorAll('.timeline-detail-box').forEach(el => el.classList.add('hidden'));
                document.querySelectorAll('[id^="arrow-tl-"]').forEach(el => el.textContent = '▾');
                showToast('已切換為「清爽簡潔模式」🌿');
            }}
        }}

        function toggleTimelineDetail(id) {{
            const box = document.getElementById('box-' + id);
            const arrow = document.getElementById('arrow-' + id);
            if (!box) return;
            if (box.classList.contains('hidden')) {{
                box.classList.remove('hidden');
                if (arrow) arrow.textContent = '▴';
            }} else {{
                box.classList.add('hidden');
                if (arrow) arrow.textContent = '▾';
            }}
        }}

        function toggleSubPanel(panelName) {{
            const panels = ['weather', 'parking', 'meals', 'custom'];
            panels.forEach(p => {{
                const panelEl = (p === 'custom') ? document.getElementById('custom-stop-form-drawer') : document.getElementById('panel-' + p);
                const arrowEl = document.getElementById('capsule-' + p + '-arrow');
                const btnEl = document.getElementById('btn-capsule-' + p);

                if (p === panelName) {{
                    if (panelEl) {{
                        const isHidden = panelEl.classList.contains('hidden');
                        if (isHidden) {{
                            panelEl.classList.remove('hidden');
                            if (arrowEl) arrowEl.textContent = '▴';
                            if (btnEl) {{
                                btnEl.classList.add('bg-stone-100', 'border-stone-400');
                            }}
                        }} else {{
                            panelEl.classList.add('hidden');
                            if (arrowEl) arrowEl.textContent = '▾';
                            if (btnEl) {{
                                btnEl.classList.remove('bg-stone-100', 'border-stone-400');
                            }}
                        }}
                    }}
                }} else {{
                    if (panelEl) panelEl.classList.add('hidden');
                    if (arrowEl) arrowEl.textContent = '▾';
                    if (btnEl) {{
                        btnEl.classList.remove('bg-stone-100', 'border-stone-400');
                    }}
                }}
            }});
        }}

        function toggleCustomStopDrawer() {{
            const drawer = document.getElementById('custom-stop-form-drawer');
            if (drawer) {{
                drawer.classList.toggle('hidden');
                if (!drawer.classList.contains('hidden')) {{
                    const input = document.getElementById('cstop-title');
                    if (input) input.focus();
                }}
            }}
        }}

        function handleNewCustomStopSubmit(e) {{
            e.preventDefault();
            const titleInput = document.getElementById('cstop-title');
            const timeInput = document.getElementById('cstop-time');
            const catSelect = document.getElementById('cstop-category');
            const descInput = document.getElementById('cstop-desc');

            const title = titleInput.value.trim();
            if (!title) return;

            const time = timeInput.value.trim() || '⏰ 隨性順遊';
            const category = catSelect.value;
            const desc = descInput.value.trim() || '自訂順遊地點，出發探索趣！';

            const newStop = {{
                id: 'cstop_' + Date.now(),
                title,
                time,
                category,
                desc,
                isCustom: true
            }};

            const list = getCustomStops(currentDayIndex);
            list.push(newStop);
            setCustomStops(currentDayIndex, list);

            titleInput.value = '';
            timeInput.value = '';
            descInput.value = '';
            toggleCustomStopDrawer();

            renderDayDetails(currentDayIndex);
            showToast(`✨ 已成功新增「${{title}}」至 Day ${{currentDayIndex + 1}} 行程時間軸！`);
        }}

        function deleteCustomStop(dayIdx, stopId) {{
            let list = getCustomStops(dayIdx);
            list = list.filter(item => item.id !== stopId);
            setCustomStops(dayIdx, list);
            renderDayDetails(dayIdx);
            showToast('已移除該筆臨時加點！');
        }}

        function launchQuickNav() {{
            const input = document.getElementById('quick-nav-input');
            if (!input || !input.value.trim()) {{
                showToast('請輸入想前往的地點或店名！');
                return;
            }}
            const query = input.value.trim();
            window.open(`https://www.google.com/maps/search/?api=1&query=${{encodeURIComponent(query)}}`, '_blank');
        }}

        function quickNavSearch(keyword) {{
            const dayPlan = TRIP_DATA.daily_itinerary[currentDayIndex || 0];
            let region = '南九州';
            if (dayPlan) {{
                if (dayPlan.theme.includes('熊本') || dayPlan.route.includes('熊本')) region = '熊本';
                else if (dayPlan.theme.includes('阿蘇') || dayPlan.route.includes('阿蘇')) region = '阿蘇';
                else if (dayPlan.theme.includes('黑川') || dayPlan.route.includes('黑川')) region = '黑川溫泉';
                else if (dayPlan.theme.includes('高千穗') || dayPlan.route.includes('高千穗')) region = '高千穗';
                else if (dayPlan.theme.includes('宮崎') || dayPlan.route.includes('宮崎')) region = '宮崎';
                else if (dayPlan.theme.includes('日南') || dayPlan.route.includes('日南')) region = '宮崎日南';
                else if (dayPlan.theme.includes('鹿兒島') || dayPlan.route.includes('鹿兒島')) region = '鹿兒島';
                else if (dayPlan.theme.includes('櫻島') || dayPlan.route.includes('櫻島')) region = '櫻島';
                else if (dayPlan.theme.includes('霧島') || dayPlan.route.includes('霧島')) region = '霧島';
            }}
            const fullQuery = `${{region}} ${{keyword}}`;
            window.open(`https://www.google.com/maps/search/?api=1&query=${{encodeURIComponent(fullQuery)}}`, '_blank');
        }}

        function renderDayDetails(idx) {{
            currentDayIndex = idx;
            const dayPlan = TRIP_DATA.daily_itinerary[idx];
            if (!dayPlan) return;

            document.querySelectorAll('.xmas-day-btn').forEach((btn, i) => {{
                if (i === idx) {{
                    btn.className = 'xmas-day-btn px-4 py-2 rounded-2xl text-xs font-black border-2 transition flex flex-col items-center min-w-[95px] bg-red-600 text-white border-red-600 shadow-md shadow-red-200';
                }} else {{
                    btn.className = 'xmas-day-btn px-4 py-2 rounded-2xl text-xs font-black border-2 transition flex flex-col items-center min-w-[95px] bg-white border-stone-200 text-stone-500 hover:border-red-300 hover:text-red-600';
                }}
            }});

            const badge = document.getElementById('current-day-badge');
            if (badge) badge.textContent = `DAY ${{dayPlan.day}} / 7 DAYS`;
            const feas = document.getElementById('current-day-feasibility');
            if (feas) feas.textContent = dayPlan.feasibility || '🟢 可行性絕佳';
            const theme = document.getElementById('current-day-theme');
            if (theme) theme.textContent = dayPlan.theme;
            const dateEl = document.getElementById('current-day-date');
            if (dateEl) dateEl.textContent = `📅 ${{dayPlan.weekday_title}}`;
            const routeEl = document.getElementById('current-day-route');
            if (routeEl) routeEl.textContent = `🗺️ ${{dayPlan.route}}`;
            const driveEl = document.getElementById('current-day-drive');
            if (driveEl) driveEl.textContent = dayPlan.drive_time;

            const hotelEl = document.getElementById('day-hotel-name');
            if (hotelEl) hotelEl.textContent = dayPlan.hotel || '溫暖的家';
            const souvEl = document.getElementById('day-souvenir-box');
            if (souvEl) souvEl.textContent = dayPlan.souvenir || '享受日本當令新鮮草莓與特色名物！';

            // 隨行膠囊列與子面板更新
            const weather = dayPlan.weather;
            const weatherCapText = document.getElementById('capsule-weather-text');
            const weatherCapIcon = document.getElementById('capsule-weather-icon');
            if (weather) {{
                if (weatherCapText) weatherCapText.textContent = `${{weather.temp_min}}°C ~ ${{weather.temp_max}}°C ${{weather.condition}}`;
                if (weatherCapIcon) weatherCapIcon.textContent = weather.icon || '⛅';
                const cityEl = document.getElementById('day-weather-city');
                if (cityEl) cityEl.textContent = weather.city || '';
                const condEl = document.getElementById('day-weather-condition');
                if (condEl) condEl.textContent = weather.condition || '';
                const tempEl = document.getElementById('day-weather-temp');
                if (tempEl) tempEl.textContent = weather.temp_display || `${{weather.temp_min}}°C ~ ${{weather.temp_max}}°C`;
                const feelEl = document.getElementById('day-weather-feeling');
                if (feelEl) feelEl.textContent = `${{weather.feeling}} ｜ 降水機率：${{weather.pop}}`;
                const clothEl = document.getElementById('day-weather-clothing');
                if (clothEl) clothEl.textContent = weather.clothing || '';
            }}

            const parkings = (dayPlan.timeline || []).filter(t => t.parking);
            const parkingCountEl = document.getElementById('capsule-parking-count');
            if (parkingCountEl) parkingCountEl.textContent = parkings.length;
            const parkingChipsContainer = document.getElementById('day-parking-chips');
            if (parkingChipsContainer) {{
                if (parkings.length > 0) {{
                    parkingChipsContainer.innerHTML = parkings.map(p => `
                        <a href="${{p.parking.url}}" target="_blank" class="px-2.5 py-1 rounded-xl bg-white hover:bg-emerald-100 text-emerald-900 border border-emerald-200 shadow-2xs font-bold text-[11px] flex items-center gap-1 transition" title="${{p.parking.name}} (${{p.parking.fee}})">
                            <span>🅿️</span> ${{p.parking.name.split(' ')[0]}} ↗
                        </a>
                    `).join('');
                }} else {{
                    parkingChipsContainer.innerHTML = `<span class="text-stone-400 text-xs">本日以飯店或景點免費臨停為主，無需額外尋找大型收費場。</span>`;
                }}
            }}

            // 自動收合所有展開的次面板（換日乾淨體驗）
            ['weather', 'parking', 'meals', 'custom'].forEach(p => {{
                const panelEl = (p === 'custom') ? document.getElementById('custom-stop-form-drawer') : document.getElementById('panel-' + p);
                const arrowEl = document.getElementById('capsule-' + p + '-arrow');
                const btnEl = document.getElementById('btn-capsule-' + p);
                if (panelEl) panelEl.classList.add('hidden');
                if (arrowEl) arrowEl.textContent = '▾';
                if (btnEl) btnEl.classList.remove('bg-stone-100', 'border-stone-400');
            }});

            const container = document.getElementById('timeline-container');
            if (!container) return;
            container.innerHTML = '';
            const quickLinks = [];
            const isDriver = (dashboardViewMode === 'driver');

            // 1. 原定計畫時間軸項目 (支援方案C手風琴折疊與雙模式)
            dayPlan.timeline.forEach((item, itemIdx) => {{
                const itemDiv = document.createElement('div');
                itemDiv.className = 'relative group';

                let icon = '📍';
                let tagClass = 'bg-stone-100 text-stone-600 border border-stone-200';
                if (item.category === 'flight') {{ icon = '✈️'; tagClass = 'bg-sky-100 text-sky-700 border border-sky-200'; }}
                else if (item.category === 'transit') {{ icon = '🚗'; tagClass = 'bg-amber-100 text-amber-700 border border-amber-200'; }}
                else if (item.category === 'hotel') {{ icon = '🏡'; tagClass = 'bg-red-100 text-red-700 border border-red-200'; }}
                else if (item.category === 'food') {{ icon = '🍱'; tagClass = 'bg-rose-100 text-rose-700 border border-rose-200'; }}
                else if (item.category === 'sight') {{ icon = '⛩️'; tagClass = 'bg-emerald-100 text-emerald-800 border border-emerald-200'; }}

                quickLinks.push(item.title);
                const mapSearchUrl = `https://www.google.com/maps/search/?api=1&query=${{encodeURIComponent(item.title)}}`;
                const itemKey = `tl-${{idx}}-${{itemIdx}}`;
                const hasDetails = (item.parking || item.tips);

                itemDiv.innerHTML = `
                    <div class="absolute -left-[31px] top-1.5 w-4 h-4 rounded-full bg-white border-2 border-red-500 flex items-center justify-center shadow-2xs">
                        <div class="w-1.5 h-1.5 rounded-full bg-red-600"></div>
                    </div>
                    <div class="bg-white border border-stone-200/90 rounded-2xl p-4 transition space-y-1.5 shadow-2xs hover:border-red-300 hover:shadow-xs">
                        <div class="flex flex-wrap items-center justify-between gap-2">
                            <span class="text-xs font-mono font-black text-red-600 bg-red-50 px-2.5 py-0.5 rounded-full border border-red-100">${{item.time}}</span>
                            <span class="cute-pill ${{tagClass}}">
                                <span>${{icon}}</span> ${{item.category.toUpperCase()}}
                            </span>
                        </div>
                        <h5 class="text-sm font-black text-stone-800 flex items-center justify-between">
                            <span>${{item.title}}</span>
                            <div class="flex items-center gap-1.5 shrink-0">
                                ${{item.parking ? `
                                    <a href="${{item.parking.url}}" target="_blank" class="px-2 py-0.5 rounded-lg bg-emerald-50 text-emerald-800 hover:bg-emerald-100 border border-emerald-200/70 font-bold text-xs flex items-center gap-0.5 transition" title="${{item.parking.name}} (${{item.parking.fee}})">
                                        <span>🅿️ 停車</span> ↗
                                    </a>
                                ` : ''}}
                                <a href="${{mapSearchUrl}}" target="_blank" class="px-2 py-0.5 rounded-lg bg-sky-50 text-sky-600 hover:bg-sky-100 border border-sky-200/70 font-bold text-xs flex items-center gap-0.5 transition" title="在 Google Maps 查看">
                                    <span>導航</span> ↗
                                </a>
                            </div>
                        </h5>
                        <p class="text-xs text-stone-600 leading-relaxed font-medium">${{item.desc}}</p>

                        ${{hasDetails ? `
                            <div class="flex flex-wrap items-center gap-1.5 pt-1.5 mt-1 border-t border-stone-100">
                                ${{item.parking ? `
                                    <button type="button" onclick="toggleTimelineDetail('${{itemKey}}-pkg')" class="px-2 py-0.5 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200/80 text-[10px] font-bold transition flex items-center gap-1">
                                        <span>🅿️ 停車指引</span>
                                        <span id="arrow-${{itemKey}}-pkg" class="text-[9px] text-emerald-600 font-mono">${{isDriver ? '▴' : '▾'}}</span>
                                    </button>
                                ` : ''}}
                                ${{item.tips ? `
                                    <button type="button" onclick="toggleTimelineDetail('${{itemKey}}-tips')" class="px-2 py-0.5 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200/80 text-[10px] font-bold transition flex items-center gap-1">
                                        <span>💡 參觀撇步</span>
                                        <span id="arrow-${{itemKey}}-tips" class="text-[9px] text-amber-600 font-mono">${{isDriver ? '▴' : '▾'}}</span>
                                    </button>
                                ` : ''}}
                            </div>
                        ` : ''}}

                        ${{item.parking ? `
                            <div id="box-${{itemKey}}-pkg" class="timeline-detail-box ${{isDriver ? '' : 'hidden'}} text-[11px] text-emerald-900 bg-emerald-50/80 border border-emerald-200/80 rounded-xl p-2.5 flex flex-col gap-1 mt-1.5 shadow-2xs">
                                <div class="flex flex-wrap items-center justify-between gap-1 font-black">
                                    <span class="flex items-center gap-1"><span>🅿️ 推薦：</span><span>${{item.parking.name}}</span></span>
                                    <span class="text-emerald-800 font-mono text-[10px] bg-white px-1.5 py-0.5 rounded-md border border-emerald-200 shadow-2xs">${{item.parking.fee}}</span>
                                </div>
                                <div class="text-[10px] text-emerald-800 leading-tight">
                                    🚗 車位：${{item.parking.capacity}} ｜ 💡 叮嚀：${{item.parking.tips}}
                                </div>
                            </div>
                        ` : ''}}
                        ${{item.tips ? `
                            <div id="box-${{itemKey}}-tips" class="timeline-detail-box ${{isDriver ? '' : 'hidden'}} text-[11px] text-amber-800 bg-amber-50/80 border border-amber-200/80 rounded-xl p-2.5 flex items-start gap-1.5 mt-1.5 shadow-2xs">
                                <span class="shrink-0 text-xs">💡</span>
                                <span><strong>小撇步：</strong>${{item.tips}}</span>
                            </div>
                        ` : ''}}
                    </div>
                `;
                container.appendChild(itemDiv);
            }});

            // 2. 當日臨時起意自訂加點項目 (保存在本機，隨時可增刪並一鍵導航)
            const customStops = getCustomStops(idx);
            if (customStops.length > 0) {{
                customStops.forEach(cstop => {{
                    const itemDiv = document.createElement('div');
                    itemDiv.className = 'relative group';

                    let icon = '⭐';
                    let tagClass = 'bg-amber-100 text-amber-800 border border-amber-200';
                    if (cstop.category === 'food') {{ icon = '🍽️'; }}
                    else if (cstop.category === 'sight') {{ icon = '⛩️'; }}
                    else if (cstop.category === 'shopping') {{ icon = '🛍️'; }}
                    else if (cstop.category === 'transit') {{ icon = '☕'; }}
                    else if (cstop.category === 'onsen') {{ icon = '♨️'; }}
                    else if (cstop.category === 'farm') {{ icon = '🍓'; }}

                    const mapSearchUrl = `https://www.google.com/maps/search/?api=1&query=${{encodeURIComponent(cstop.title)}}`;

                    itemDiv.innerHTML = `
                        <div class="absolute -left-[31px] top-1.5 w-4 h-4 rounded-full bg-amber-400 border-2 border-amber-600 flex items-center justify-center shadow-sm">
                            <div class="w-1.5 h-1.5 rounded-full bg-amber-700 animate-pulse"></div>
                        </div>
                        <div class="bg-gradient-to-r from-amber-50/70 to-orange-50/40 border-2 border-amber-300 rounded-2xl p-4 transition space-y-2 shadow-sm hover:shadow-md">
                            <div class="flex flex-wrap items-center justify-between gap-2">
                                <span class="text-xs font-mono font-black text-amber-900 bg-amber-100 px-2.5 py-0.5 rounded-full border border-amber-200">${{cstop.time}}</span>
                                <div class="flex items-center gap-1.5">
                                    <span class="cute-pill bg-amber-200 text-amber-900 border border-amber-300 font-bold">
                                        <span>${{icon}}</span> 臨時起意加點
                                    </span>
                                    <button type="button" onclick="deleteCustomStop(${{idx}}, '${{cstop.id}}')" class="p-1 text-stone-400 hover:text-red-600 transition" title="移除此臨時加點">🗑️</button>
                                </div>
                            </div>
                            <h5 class="text-sm font-black text-stone-800 flex items-center justify-between">
                                <span class="flex items-center gap-1.5">
                                    <span>${{icon}}</span>
                                    <span>${{cstop.title}}</span>
                                </span>
                                <a href="${{mapSearchUrl}}" target="_blank" class="px-3 py-1 rounded-xl bg-gradient-to-r from-sky-600 to-blue-600 hover:from-sky-700 hover:to-blue-700 text-white font-black text-xs flex items-center gap-1 shadow-sm transition">
                                    <span>🗺️</span> 立即導航 ↗
                                </a>
                            </h5>
                            <p class="text-xs text-stone-600 leading-relaxed font-medium bg-white/70 p-2.5 rounded-xl border border-amber-200">${{cstop.desc}}</p>
                        </div>
                    `;
                    container.appendChild(itemDiv);
                }});
            }}

            // 2.5 當日宵夜＆酒吧時間軸卡片 (直覺醒目，在時間軸最後一眼可見)
            if (dayPlan.meals && dayPlan.meals.latenight && dayPlan.meals.latenight.length > 0) {{
                const lateDiv = document.createElement('div');
                lateDiv.className = 'relative group';

                const optsHtml = dayPlan.meals.latenight.map((opt, i) => `
                    <div class="bg-white/95 p-3 rounded-xl border border-purple-200 flex items-center justify-between gap-2 shadow-xs hover:border-purple-300 transition">
                        <div class="min-w-0">
                            <div class="font-black text-xs text-purple-950 truncate">${{i + 1}}. ${{opt.name}}</div>
                            <div class="text-[11px] text-stone-500 truncate mt-0.5">🍴 ${{opt.must_eat}} <span class="font-mono text-purple-900 font-bold ml-1">(${{opt.price.split('~')[0].trim()}})</span></div>
                        </div>
                        <div class="flex items-center gap-1.5 shrink-0">
                            <button type="button" onclick="jumpToRestaurant('${{opt.id}}')" class="px-2.5 py-1 rounded-xl bg-purple-100 hover:bg-purple-200 text-purple-800 text-[11px] font-black transition">
                                訂位/詳情 ↗
                            </button>
                            <a href="https://www.google.com/maps/search/?api=1&query=${{encodeURIComponent(opt.name + ' ' + opt.area)}}" target="_blank" class="px-2.5 py-1 rounded-xl bg-sky-50 hover:bg-sky-100 text-sky-700 text-[11px] font-black transition">
                                導航 ↗
                            </a>
                        </div>
                    </div>
                `).join('');

                lateDiv.innerHTML = `
                    <div class="absolute -left-[31px] top-1.5 w-4 h-4 rounded-full bg-purple-600 border-2 border-purple-300 flex items-center justify-center shadow-sm">
                        <div class="w-1.5 h-1.5 rounded-full bg-white animate-ping"></div>
                    </div>
                    <div class="bg-gradient-to-br from-purple-50 via-indigo-50/60 to-pink-50/50 border-2 border-purple-300 rounded-2xl p-4 transition space-y-2.5 shadow-sm hover:shadow-md">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-mono font-black text-purple-900 bg-purple-100 px-2.5 py-0.5 rounded-full border border-purple-200">21:30 ~ 深夜</span>
                            <span class="cute-pill bg-purple-200 text-purple-900 border border-purple-300 font-bold">
                                <span>🍸</span> 宵夜＆酒吧 3 選
                            </span>
                        </div>
                        <h5 class="text-sm font-black text-stone-900 flex items-center justify-between">
                            <span class="flex items-center gap-1.5">
                                <span>🌙</span> 今晚宵夜・微醺小酌提案
                            </span>
                            <button type="button" onclick="scrollToMeal('latenight')" class="text-[11px] text-purple-700 hover:underline font-bold">
                                查看全餐總表 ⬇
                            </button>
                        </h5>
                        <div class="space-y-2">
                            ${{optsHtml}}
                        </div>
                    </div>
                `;
                container.appendChild(lateDiv);
            }}

            const qlBtn = document.getElementById('quick-jump-latenight');
            if (qlBtn) {{
                if (dayPlan.meals && dayPlan.meals.latenight && dayPlan.meals.latenight.length > 0) {{
                    qlBtn.classList.remove('hidden');
                }} else {{
                    qlBtn.classList.add('hidden');
                }}
            }}

            const linksBox = document.getElementById('quick-links-box');
            if (linksBox) {{
                linksBox.innerHTML = '';
                quickLinks.slice(0, 4).forEach(name => {{
                    const cleanName = name.replace(/（.*）|\(.*\)|•/g, '').trim();
                    const a = document.createElement('a');
                    a.href = `https://www.google.com/maps/search/?api=1&query=${{encodeURIComponent(cleanName)}}`;
                    a.target = '_blank';
                    a.className = 'block p-2 rounded-xl bg-stone-50 hover:bg-red-50 border border-stone-200 text-stone-800 text-xs font-bold truncate transition flex items-center justify-between';
                    a.innerHTML = `<span>📍 ${{cleanName}}</span><span class="text-stone-400">↗</span>`;
                    linksBox.appendChild(a);
                }});
            }}

            // 3. 渲染當日三餐精選推薦 (早、午、晚 各 3 選)
            renderDayMealsSection(dayPlan, idx);
        }}

        function renderAccommodations() {{
            const grid = document.getElementById('stays-grid');
            if (!grid) return;
            grid.innerHTML = '';

            TRIP_DATA.accommodations.forEach(acc => {{
                // 判斷訂房平台標籤與主題色彩
                let platformBadge = '';
                const pStr = acc.booking_platform || '';
                if (pStr.includes('Booking.com')) {{
                    platformBadge = '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-800 border border-blue-200 font-black text-[11px] shadow-2xs"><span class="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse"></span>Booking.com 預訂</span>';
                }} else if (pStr.includes('Airbnb')) {{
                    platformBadge = '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-800 border border-rose-200 font-black text-[11px] shadow-2xs"><span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse"></span>Airbnb 民宿預訂</span>';
                }} else if (pStr.includes('官網')) {{
                    platformBadge = '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-900 border border-amber-200 font-black text-[11px] shadow-2xs"><span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>♨️ 旅館官網直訂</span>';
                }} else {{
                    platformBadge = '<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-stone-100 text-stone-700 font-bold text-[11px]">已預約</span>';
                }}

                const div = document.createElement('div');
                div.className = 'cute-card p-5 relative border-2 border-stone-200 space-y-3.5 hover:border-red-200 transition-all';
                div.innerHTML = `
                    <div class="flex items-start justify-between gap-2">
                        <div>
                            <div class="flex flex-wrap items-center gap-1.5 mb-1.5">
                                <span class="cute-pill bg-red-100 text-red-700">${{acc.night}}</span>
                                ${{platformBadge}}
                            </div>
                            <h4 class="text-base font-black text-stone-800 tracking-tight leading-snug">${{acc.hotel_name}}</h4>
                            <p class="text-xs text-stone-400 font-medium flex items-center gap-1 mt-0.5">
                                <span>📍</span>${{acc.city}}
                            </p>
                        </div>
                        <a href="${{acc.google_maps_url}}" target="_blank" class="shrink-0 px-3 py-1 rounded-full bg-sky-100 text-sky-700 hover:bg-sky-200 text-xs font-black transition flex items-center gap-1">
                            地圖 ↗
                        </a>
                    </div>

                    <div class="bg-stone-50 rounded-2xl p-3.5 space-y-2 text-xs border border-stone-200 font-medium">
                        <div class="flex justify-between items-center">
                            <span class="text-stone-400">房型配置：</span>
                            <span class="text-stone-800 font-bold">${{acc.room_type}}</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-stone-400">入住/退房：</span>
                            <span class="text-stone-700 font-semibold">${{acc.check_in.split(' ')[1] || acc.check_in}} / ${{acc.check_out.split(' ')[1] || acc.check_out}}</span>
                        </div>
                        <div class="flex justify-between items-center pt-1 border-t border-stone-200/60">
                            <span class="text-stone-400">訂購管道 / 費用：</span>
                            <span class="text-emerald-700 font-black">${{acc.booking_platform}}</span>
                        </div>
                    </div>

                    <div class="text-[11px] text-stone-500 leading-relaxed bg-amber-50/60 rounded-xl p-2.5 border border-amber-200/50">
                        <span class="font-bold text-amber-800">💡 旅宿亮點：</span>${{acc.notes}}
                    </div>
                `;
                grid.appendChild(div);
            }});
        }}

        
        // ======================= 餐廳美饌與訂位系統 =======================
        let currentRestFilter = {{
            meal: 'all',
            day: 'all',
            theme: 'all',
            search: ''
        }};

        function setRestFilter(type, value) {{
            currentRestFilter[type] = value;
            updateRestFilterUI();
            renderRestaurants();
        }}

        function filterRestaurants() {{
            const input = document.getElementById('rest-search-input');
            currentRestFilter.search = input ? input.value.trim().toLowerCase() : '';
            renderRestaurants();
        }}

        function clearRestSearch() {{
            const input = document.getElementById('rest-search-input');
            if (input) input.value = '';
            currentRestFilter.search = '';
            renderRestaurants();
        }}

        function updateRestFilterUI() {{
            // Meal buttons (4 大餐別專屬鮮明色彩)
            ['all', 'breakfast', 'lunch', 'dinner', 'latenight'].forEach(m => {{
                const btn = document.getElementById(`rf-meal-${{m}}`);
                if (btn) {{
                    const isActive = m === currentRestFilter.meal;
                    if (isActive) {{
                        if (m === 'breakfast') btn.className = 'rf-meal-btn px-3 py-1 rounded-full bg-amber-500 text-white shadow-sm font-black transition';
                        else if (m === 'lunch') btn.className = 'rf-meal-btn px-3 py-1 rounded-full bg-emerald-600 text-white shadow-sm font-black transition';
                        else if (m === 'dinner') btn.className = 'rf-meal-btn px-3 py-1 rounded-full bg-rose-600 text-white shadow-sm font-black transition';
                        else if (m === 'latenight') btn.className = 'rf-meal-btn px-3 py-1 rounded-full bg-purple-600 text-white shadow-sm font-black transition';
                        else btn.className = 'rf-meal-btn px-3 py-1 rounded-full bg-stone-800 text-white shadow-sm font-black transition';
                    }} else {{
                        if (m === 'breakfast') btn.className = 'rf-meal-btn px-3 py-1 rounded-full bg-white border border-amber-200 text-amber-800 hover:bg-amber-50 transition';
                        else if (m === 'lunch') btn.className = 'rf-meal-btn px-3 py-1 rounded-full bg-white border border-emerald-200 text-emerald-800 hover:bg-emerald-50 transition';
                        else if (m === 'dinner') btn.className = 'rf-meal-btn px-3 py-1 rounded-full bg-white border border-rose-200 text-rose-800 hover:bg-rose-50 transition';
                        else if (m === 'latenight') btn.className = 'rf-meal-btn px-3 py-1 rounded-full bg-white border border-purple-200 text-purple-800 hover:bg-purple-50 transition';
                        else btn.className = 'rf-meal-btn px-3 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-stone-100 transition';
                    }}
                }}
            }});

            // Day buttons
            ['all', '1', '2', '3', '4', '5', '6', '7'].forEach(d => {{
                const btn = document.getElementById(`rf-day-${{d}}`);
                if (btn) {{
                    if (d === currentRestFilter.day) {{
                        btn.className = 'rf-day-btn px-2.5 py-0.5 rounded-full bg-orange-600 text-white shadow-sm transition text-[11px] font-black';
                    }} else {{
                        btn.className = 'rf-day-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]';
                    }}
                }}
            }});

            // Theme buttons (含個人候選清單)
            ['all', 'shortlist', 'meat', 'reserve', 'bar'].forEach(t => {{
                const btn = document.getElementById(`rf-theme-${{t}}`);
                if (btn) {{
                    if (t === currentRestFilter.theme) {{
                        if (t === 'shortlist') btn.className = 'rf-theme-btn px-2.5 py-0.5 rounded-full bg-amber-500 text-white shadow-sm font-black transition text-[11px] ring-2 ring-amber-300';
                        else btn.className = 'rf-theme-btn px-2.5 py-0.5 rounded-full bg-orange-600 text-white shadow-sm transition text-[11px] font-black';
                    }} else {{
                        btn.className = 'rf-theme-btn px-2.5 py-0.5 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-orange-100 transition text-[11px]';
                    }}
                }}
            }});
            updateShortlistBadge();
        }}


        // 回到分頁導覽選單功能 (動態偵測置頂高度，確保 8 個分頁兩排 100% 完整露出)
        function scrollToTabNav() {{
            const nav = document.getElementById('main-tab-nav');
            if (nav) {{
                const header = document.querySelector('header');
                const headerH = header ? header.offsetHeight : 80;
                // 多預留 20px 緩衝空間，讓上排 4 個與下排 4 個按鈕都能完整出現在畫面中
                const navTop = nav.getBoundingClientRect().top + window.pageYOffset - headerH - 20;
                window.scrollTo({{ top: Math.max(0, navTop), behavior: 'smooth' }});
            }}
        }}

        // ======================= 每日移動路線系統 =======================
        const DAY_ROUTES_DATA = {{
            1: {{
                title: "Day 1 啟程抵達",
                desc: "桃機 CI194 ➔ 熊本空港 KMJ (取車出發) ➔ 熊本辛島町飯店 (約 20km / 40分)",
                landmarks: ["kmj_airport", "hotel_viainn"]
            }},
            2: {{
                title: "Day 2 阿蘇火山 ➔ 黑川秘湯",
                desc: "熊本辛島町 ➔ 草千里之濱・中岳火山口 ➔ 大觀峰展望台 ➔ 黑川溫泉山彥旅館 (約 95km / 2小時30分)",
                landmarks: ["hotel_viainn", "aso_crater", "daikanbo", "hotel_kurokawa"]
            }},
            3: {{
                title: "Day 3 高千穗神話 ➔ 宮崎日向",
                desc: "黑川溫泉 ➔ 上色見熊野座神社 ➔ 高千穗峽谷划船 ➔ 宮崎喜來登海景公寓 (約 145km / 3小時)",
                landmarks: ["hotel_kurokawa", "kamishikimi", "takachiho_gorge", "hotel_seagaia"]
            }},
            4: {{
                title: "Day 4 日南海岸 ➔ 鹿兒島",
                desc: "宮崎 ➔ 青島神社 ➔ 摩艾石像 ➔ 鵜戶神宮 ➔ 鹿兒島中央公寓 (約 155km / 3小時15分)",
                landmarks: ["hotel_seagaia", "aoshima", "sun_messe", "udo_jingu", "hotel_perch"]
            }},
            5: {{
                title: "Day 5 櫻島火山 ➔ 仙巖園",
                desc: "鹿兒島 ➔ 櫻島渡輪 ➔ 櫻島活火山足湯 ➔ 仙巖園庭園 ➔ 天文館商圈 (約 35km / 渡輪15分)",
                landmarks: ["hotel_perch", "sakurajima", "senganen"]
            }},
            6: {{
                title: "Day 6 鹿兒島 ➔ 霧島人吉 ➔ 熊本",
                desc: "鹿兒島出發 ➔ 國寶霧島神宮 ➔ 人吉古城碳火鰻魚 ➔ 熊本辛島町飯店 (約 180km / 3小時)",
                landmarks: ["hotel_perch", "kirishima_jingu", "hitoyoshi_unagi", "hotel_amanek"]
            }},
            7: {{
                title: "Day 7 熊本市區 ➔ 機場 ➔ 台灣",
                desc: "辛島町飯店 ➔ 熊本城天守閣・城彩苑 ➔ 水前寺成趣園 ➔ 熊本機場 KMJ (搭乘 CI195 直飛返台)",
                landmarks: ["hotel_amanek", "kumamoto_castle", "suizenji", "kmj_airport"]
            }}
        }};

        let currentDayRoute = 'all';

        function selectDayRoute(day) {{
            // 點選同天自動反轉為全部動線
            if (currentDayRoute === String(day) && day !== 'all') {{
                day = 'all';
            }}
            currentDayRoute = String(day);
            showRoutes = true;

            const routesGroup = document.getElementById('map-routes-group');
            if (routesGroup) routesGroup.style.display = 'inline';

            const btnRoutes = document.getElementById('map-btn-routes');
            if (btnRoutes) {{
                btnRoutes.textContent = '🚗 7天全動線';
                btnRoutes.className = 'px-2.5 py-1 rounded-full bg-amber-600 text-white shadow-sm transition';
            }}

            // 1. 同步上排與下排的所有按鈕高亮狀態
            ['all', 1, 2, 3, 4, 5, 6, 7].forEach(d => {{
                const btnTop = document.getElementById(`btn-route-${{d}}`);
                const isSel = String(d) === currentDayRoute;
                if (btnTop) {{
                    if (isSel) {{
                        btnTop.className = 'btn-day-route px-3 py-1 rounded-full bg-amber-600 text-white shadow-xs transition text-[11px] font-black scale-105';
                    }} else {{
                        btnTop.className = 'btn-day-route px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]';
                    }}
                }}
            }});

            for (let d = 1; d <= 7; d++) {{
                const btnBottom = document.getElementById(`route-btn-${{d}}`);
                const isSel = String(d) === currentDayRoute;
                if (btnBottom) {{
                    if (isSel) {{
                        btnBottom.className = 'px-2 py-0.5 rounded-full text-[10px] font-black border border-stone-800 bg-stone-900 text-white shadow-xs scale-105 transition';
                    }} else {{
                        btnBottom.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold border border-stone-200 bg-white text-stone-600 hover:bg-amber-100 transition';
                    }}
                }}
            }}

            const banner = document.getElementById('route-summary-banner');
            const summaryText = document.getElementById('route-summary-text');
            const indicatorText = document.getElementById('route-indicator-text');
            const statusTip = document.getElementById('map-route-status-tip');

            // 2. 切換 SVG 虛線顯示狀態
            if (currentDayRoute === 'all') {{
                for (let d = 1; d <= 7; d++) {{
                    const grp = document.getElementById(`route-group-${{d}}`);
                    const path = document.getElementById(`route-path-${{d}}`);
                    if (grp) grp.style.display = 'inline';
                    if (path) {{
                        path.style.opacity = '1';
                        path.style.display = 'inline';
                        path.setAttribute('stroke-width', d === 1 || d === 5 ? '4' : '4.5');
                        path.removeAttribute('filter');
                        path.classList.remove('route-flowing');
                    }}
                }}
                if (banner) banner.classList.add('hidden');
                if (indicatorText) indicatorText.textContent = '已顯示全 7 天自駕動線';
                if (statusTip) statusTip.textContent = '💡 點擊地圖任意虛線或上方按鈕，可單獨留下該日自駕路線';
                renderMapPins('all');
                showToast('已恢復顯示全九州完整自駕路線 🗺️');
            }} else {{
                const targetDay = Number(currentDayRoute);
                for (let d = 1; d <= 7; d++) {{
                    const grp = document.getElementById(`route-group-${{d}}`);
                    const path = document.getElementById(`route-path-${{d}}`);
                    if (d === targetDay) {{
                        if (grp) grp.style.display = 'inline';
                        if (path) {{
                            path.style.opacity = '1';
                            path.style.display = 'inline';
                            path.setAttribute('stroke-width', '7');
                            path.setAttribute('stroke', '#dc2626');
                            path.setAttribute('filter', 'drop-shadow(0 0 6px rgba(220, 38, 38, 0.7))');
                            path.classList.add('route-flowing');
                        }}
                    }} else {{
                        // 隱藏非目標天數路線
                        if (grp) grp.style.display = 'none';
                        if (path) {{
                            path.style.opacity = '0';
                            path.style.display = 'none';
                            path.setAttribute('stroke-width', '4');
                            path.removeAttribute('filter');
                            path.classList.remove('route-flowing');
                        }}
                    }}
                }}

                const info = DAY_ROUTES_DATA[targetDay];
                if (banner && summaryText && info) {{
                    banner.classList.remove('hidden');
                    summaryText.innerHTML = `<span>🚗</span> <span><strong>${{info.title}}：</strong>${{info.desc}}</span>`;
                }}
                if (indicatorText && info) {{
                    indicatorText.textContent = `當前：${{info.title}}`;
                }}
                if (statusTip && info) {{
                    statusTip.innerHTML = `📍 <span class="text-red-700 font-black">已聚焦：${{info.title}}</span>`;
                }}

                // 連動地圖圖釘與右側景點卡片
                if (info && info.landmarks) {{
                    document.querySelectorAll('.map-pin').forEach(pin => {{
                        const pinId = pin.id.replace('pin-', '');
                        if (info.landmarks.includes(pinId)) {{
                            pin.style.opacity = '1';
                            pin.style.filter = 'drop-shadow(0 0 4px rgba(220, 38, 38, 0.5))';
                        }} else {{
                            pin.style.opacity = '0.25';
                            pin.style.filter = 'none';
                        }}
                    }});
                }}

                if (info && info.landmarks && info.landmarks.length > 0) {{
                    selectLandmark(info.landmarks[0]);
                }}

                showToast(`已留下 Day ${{targetDay}} 自駕路線！其餘路線已隱藏 🚗✨`);
            }}
        }}

        // ======================= 優惠券與折價券資料系統 =======================
        const COUPONS_DATA = [
            // ── 1. 商業綜合通路與藥妝免稅 (100% 官方真實核銷連結) ──
            {{
                id: "c_donki",
                title: "驚安殿堂 唐吉訶德 (Don Quijote)",
                title_jp: "ドン・キホーテ 免税＋特別優待電子クーポン",
                category: "shopping",
                tag: "免稅 10% + 最高折 7%",
                discount: "10% 免稅 + 最高 7% 現折 (官方電子券)",
                condition: "滿 10,000 日圓折 5% ｜ 滿 30,000 日圓折 7%",
                barcode: "9900123456789",
                official_url: "https://japanportal.donki-global.com/coupon/?ptcd=0076000703",
                official_name: "唐吉訶德官方電子折價券",
                usage_guide: "⚠️ 唐吉訶德門市結帳時，店員須在手機開啟的官方網頁上點擊金額核銷，靜態截圖不被接受，請點擊上方按鈕出示官方網頁！",
                area: "kumamoto_kagoshima_chain",
                area_tag: "chain",
                area_name: "熊本下通・鹿兒島天文館",
                stores: "熊本下通店、鹿兒島天文館店",
                google_maps: "https://www.google.com/maps/search/?api=1&query=ドン・キホーテ+熊本下通店",
                expiry: "長期有效 (2026/12 聖誕適用)",
                note: "結帳前務必開啟官方網頁並出示護照由店員核銷點擊"
            }},
            {{
                id: "c_bic",
                title: "Bic Camera / Kojima 電器綜合免稅",
                title_jp: "ビックカメラ / コジマ 特別割引クーポン",
                category: "shopping",
                tag: "免稅 10% + 7% / 5% 折扣",
                discount: "10% 免稅 + 電器相機 7% / 藥妝保溫瓶 5% / 日本酒 3%",
                condition: "相機、電器、保溫瓶出示條碼即享免稅外加折抵優惠",
                barcode: "9900987654321",
                official_url: "https://tourist-info.biccamera.com/",
                official_name: "Bic Camera 官方外國旅客服務專區",
                usage_guide: "結帳時直接由店員掃描本卡片條碼或開啟官方網頁條碼即可折抵，可刷台灣信用卡。",
                area: "kumamoto_kagoshima",
                area_tag: "chain",
                area_name: "熊本市區・鹿兒島中央站",
                stores: "Kojima x BicCamera 熊本店、Bic Camera 鹿兒島中央站店",
                google_maps: "https://www.google.com/maps/search/?api=1&query=ビックカメラ+鹿児島中央駅店",
                expiry: "2026/12/31 止",
                note: "相機鏡頭、大容量保溫杯、刮鬍刀、Dyson 吹風機超划算"
            }},
            {{
                id: "c_matsukiyo",
                title: "松本清藥妝 (Matsumoto Kiyoshi)",
                title_jp: "マツモトキヨシ 外国人限定 免税クーポン",
                category: "shopping",
                tag: "免稅 10% + 最高折 7%",
                discount: "10% 免稅 + 滿額加碼折 3% ~ 7%",
                condition: "滿 1萬折 3% ｜ 滿 3萬折 5% ｜ 滿 5萬折 7%",
                barcode: "4901234567890",
                official_url: "https://www.matsumotokiyoshi-tw.com/",
                official_name: "松本清官方繁體中文網站",
                usage_guide: "出示條碼由收銀台掃描，全九州各大主要商店街皆有門市。",
                area: "all_kyushu",
                area_tag: "chain",
                area_name: "熊本・宮崎・鹿兒島連鎖",
                stores: "熊本下通店、宮崎橘通店、鹿兒島天文館店",
                google_maps: "https://www.google.com/maps/search/?api=1&query=マツモトキヨシ+熊本下通",
                expiry: "2026/12/31 止",
                note: "合利他命、EVE止痛藥、WAKAMOTO、雪肌精常備藥補貨首選"
            }},
            {{
                id: "c_sugi",
                title: "SUGI 杉藥局 (Sugi Pharmacy)",
                title_jp: "スギ薬局 免税＋インバウンド限定割引",
                category: "shopping",
                tag: "免稅 10% + 滿額折 3%~8%",
                discount: "10% 免稅 + 滿額最高現折 8%",
                condition: "滿 1 萬折 3% ｜ 滿 3 萬折 5% ｜ 滿 5 萬折 8%",
                barcode: "4908821901234",
                official_url: "https://www.sugi-net.jp/",
                official_name: "SUGI 杉藥局官方網站",
                usage_guide: "結帳時出示條碼及外國護照，即可享免稅加上額外折抵。",
                area: "all_kyushu",
                area_tag: "chain",
                area_name: "熊本市區・鹿兒島市區",
                stores: "熊本櫻町店、鹿兒島市區門市",
                google_maps: "https://www.google.com/maps/search/?api=1&query=スギ薬局+熊本",
                expiry: "2026/12/31 止",
                note: "藥品齊全且化妝水保養品常有獨家組合"
            }},
            {{
                id: "c_daikoku",
                title: "大國藥妝 (Daikoku Drug)",
                title_jp: "ダイコクドラッグ 免税特別割引",
                category: "shopping",
                tag: "免稅 10% + 現折 3%~7%",
                discount: "10% 免稅 + 滿額現折 3% ~ 7%",
                condition: "熱門零食、常備感冒藥、痠痛貼布滿額現折",
                barcode: "4909876543210",
                official_url: "https://daikokudrug.com/",
                official_name: "大國藥妝官方免稅指引",
                usage_guide: "出示條碼由收銀人員掃描，常駐中文服務人員。",
                area: "all_kyushu",
                area_tag: "chain",
                area_name: "熊本市區・鹿兒島市區",
                stores: "熊本新市街店、鹿兒島天文館店",
                google_maps: "https://www.google.com/maps/search/?api=1&query=ダイコクドラッグ+熊本",
                expiry: "2026/12/31 止",
                note: "DHC維他命、休足時間、ROIHI鎮痛貼片價格親民"
            }},
            {{
                id: "c_tsuruya",
                title: "熊本鶴屋百貨 外國旅客 5% 貴賓券",
                title_jp: "鶴屋百貨店 外国人特別優待クーポン",
                category: "shopping",
                tag: "5% 貴賓券 + 10% 免稅",
                discount: "全館 5% 折扣 + 10% 免稅退稅",
                condition: "憑外國護照至本館退稅櫃台出示即可領取 5% 貴賓券",
                barcode: "2978849102401",
                official_url: "https://www.tsuruya-dept.co.jp/",
                official_name: "熊本鶴屋百貨官方網站",
                usage_guide: "至本館退稅櫃台出示護照領取 5% 實體券，結帳即折，東館 1F 旁為熊本熊部長辦公室！",
                area: "kumamoto",
                area_tag: "kumamoto",
                area_name: "熊本市區辛島町/通町筋",
                stores: "鶴屋百貨本館 (熊本熊廣場旁)",
                google_maps: "https://www.google.com/maps/search/?api=1&query=鶴屋百貨店+熊本",
                expiry: "長期有效 (2026 全年適用)",
                note: "買九州頂級銘菓（陣太鼓、武者返）、頂級伴手禮與專櫃精品必逛"
            }},

            // ── 2. 自駕專用：ETC 省錢指南與地方精準情報 ──
            {{
                id: "c_etc_guide",
                title: "🚗【自駕省錢實測】ETC 按實計費 vs KEP 吃到飽精算指南",
                title_jp: "九州自駕高速 ETC 省錢攻略 (比買 KEP 現省 ¥8,570！)",
                category: "drive_local",
                tag: "💡 省錢必看・不買吃到飽更划算",
                discount: "Toyota 加租 ETC 卡只需 ¥330 ｜ 全程實算過路費僅約 ¥8,630",
                condition: "南九州山海國道風景線免過路費！KEP 7日券 ¥17,200 反而多付 ¥8,570",
                barcode: "9908882026120",
                official_url: "https://search.w-nexco.co.jp/",
                official_name: "NEXCO 西日本官方高速過路費即時試算網",
                usage_guide: "取車時在 Toyota 櫃台說「ETCカードをレンタルしたいです (加租ETC卡，租金¥330)」，取車插上卡片，過收費站減速走藍色【ETC專用道】，最後一天還車印明細刷卡結清即可！",
                area: "drive_local_all",
                area_tag: "drive_local",
                area_name: "全九州自駕公路網 (阿蘇/高千穗/宮崎/鹿兒島)",
                stores: "熊本機場 Toyota Rent a Car 取車櫃檯",
                google_maps: "https://www.google.com/maps/search/?api=1&query=トヨタレンタカー+熊本空港店",
                expiry: "2026/12/22 ~ 12/28 自駕適用",
                note: "實測費用：宮崎->鹿兒島約 ¥3,650，溝邊鹿兒島空港->熊本約 ¥3,480，其餘走景觀國道免收費！"
            }},
            {{
                id: "c_kurokawa_pass",
                title: "♨️【黑川溫泉秘湯】黑川溫泉 入湯手形 (入浴巡禮券)",
                title_jp: "黒川温泉 入湯手形 (黒川温泉観光旅館協同組合)",
                category: "drive_local",
                tag: "♨️ 溫泉協會官方・省 40%",
                discount: "¥1,500 任選 3 家秘湯露天風呂 或 2 湯 + 1 美食伴手禮",
                condition: "單泡一家露天風呂原價 ¥600~800，買手形泡 3 家現省近半，更可兌換特約甜點伴手禮",
                barcode: "9908882026121",
                official_url: "https://www.kurokawaonsen.or.jp/tegata/",
                official_name: "黑川溫泉觀光旅館協同組合 (風の舎)",
                usage_guide: "於黑川溫泉「風の舎」旅客服務中心或任一旅館櫃檯購買，附有精緻天然杉木圓牌，泡完可帶回家當紀念！",
                area: "kumamoto",
                area_tag: "drive_local",
                area_name: "熊本阿蘇・黑川溫泉街",
                stores: "黑川溫泉觀光中心「風の舎」、各特約溫泉旅館",
                google_maps: "https://www.google.com/maps/search/?api=1&query=黒川温泉+風の舎",
                expiry: "購入日起半年內有效 (Day 2-3 適用)",
                note: "推薦巡禮：新明館「穴風呂」、山之宿「新平山」或黑川街區人氣甜點店"
            }},
            {{
                id: "c_kyushu_tourism",
                title: "🎌【即時路況/火山情報】九州觀光機構 Welcome Kyushu",
                title_jp: "一般社団法人 九州観光機構 (WELCOME KYUSHU 官方繁中網)",
                category: "drive_local",
                tag: "❄️ 阿蘇火山警戒・冬季降雪即時通報",
                discount: "官方第一手路況管制、火山氣體安全警報、冬季自駕指引",
                condition: "自駕上阿蘇火山口或黑川山區必查！掌握即時通行開放狀態",
                barcode: "9908882026125",
                official_url: "https://www.welcomekyushu.travel/tw/",
                official_name: "九州觀光機構 (Welcome Kyushu) 繁中官方網站",
                usage_guide: "出發前或旅途中點擊官方專頁，即可查詢最新各縣冬季降雪路況、輪胎防滑鏈要求與阿蘇火山噴氣即時管制！",
                area: "all_kyushu",
                area_tag: "drive_local",
                area_name: "全九州 (熊本・阿蘇・黑川・鹿兒島)",
                stores: "九州觀光機構官方平台線上即時更新",
                google_maps: "https://www.google.com/maps/search/?api=1&query=阿蘇中岳火口",
                expiry: "2026 冬季最新官方情報",
                note: "提供最權威的阿蘇火山管制警戒等級與冬季高山道路防滑管制即時通報"
            }}
        ];

        let currentCouponFilter = 'all';

        function renderBarcodeSvg(codeStr, width, height) {{
            // Generate clean vector code-128 SVG bars
            const bars = [];
            let pos = 10;
            for (let i = 0; i < codeStr.length; i++) {{
                const charCode = codeStr.charCodeAt(i);
                const w1 = ((charCode % 3) + 1) * 2;
                const w2 = ((charCode % 2) + 1) * 2;
                bars.push(`<rect x="${{pos}}" y="0" width="${{w1}}" height="${{height}}" fill="#111827"/>`);
                pos += w1 + w2;
                bars.push(`<rect x="${{pos}}" y="0" width="${{w2}}" height="${{height}}" fill="#111827"/>`);
                pos += w2 + 3;
            }}
            return `<svg viewBox="0 0 ${{pos + 10}} ${{height}}" class="w-full h-${{height > 50 ? '16' : '10'}}" xmlns="http://www.w3.org/2000/svg">${{bars.join('')}}</svg>`;
        }}

        function renderQrSvg(codeStr, size) {{
            // Generate crisp vector QR pattern
            return `
                <svg viewBox="0 0 100 100" class="w-${{size}} h-${{size}}" xmlns="http://www.w3.org/2000/svg">
                    <rect width="100" height="100" fill="#ffffff" rx="6"/>
                    <!-- Corner Pos 1 -->
                    <rect x="10" y="10" width="24" height="24" fill="#111827" rx="3"/>
                    <rect x="15" y="15" width="14" height="14" fill="#ffffff"/>
                    <rect x="18" y="18" width="8" height="8" fill="#111827"/>
                    <!-- Corner Pos 2 -->
                    <rect x="66" y="10" width="24" height="24" fill="#111827" rx="3"/>
                    <rect x="71" y="15" width="14" height="14" fill="#ffffff"/>
                    <rect x="74" y="18" width="8" height="8" fill="#111827"/>
                    <!-- Corner Pos 3 -->
                    <rect x="10" y="66" width="24" height="24" fill="#111827" rx="3"/>
                    <rect x="15" y="71" width="14" height="14" fill="#ffffff"/>
                    <rect x="18" y="74" width="8" height="8" fill="#111827"/>
                    <!-- Inner Grid Data Points -->
                    <rect x="42" y="12" width="6" height="6" fill="#111827"/>
                    <rect x="52" y="18" width="6" height="6" fill="#111827"/>
                    <rect x="42" y="28" width="12" height="6" fill="#111827"/>
                    <rect x="12" y="42" width="8" height="6" fill="#111827"/>
                    <rect x="26" y="48" width="8" height="6" fill="#111827"/>
                    <rect x="40" y="42" width="20" height="18" fill="#dc2626" rx="2"/>
                    <rect x="68" y="42" width="8" height="8" fill="#111827"/>
                    <rect x="80" y="52" width="10" height="6" fill="#111827"/>
                    <rect x="42" y="68" width="8" height="12" fill="#111827"/>
                    <rect x="56" y="74" width="12" height="6" fill="#111827"/>
                    <rect x="72" y="68" width="16" height="16" fill="#111827"/>
                </svg>
            `;
        }}

        function filterCoupons(area) {{
            currentCouponFilter = area;
            ['all', 'chain', 'drive_local', 'kumamoto', 'kagoshima', 'miyazaki'].forEach(a => {{
                const btn = document.getElementById(`cfilter-${{a}}`);
                if (btn) {{
                    if (a === area) {{
                        btn.className = 'cfilter-btn px-3 py-1 rounded-full bg-red-600 text-white shadow-xs transition text-[11px] font-bold';
                    }} else {{
                        btn.className = 'cfilter-btn px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]';
                    }}
                }}
            }});
            renderCoupons();
        }}

        function renderCoupons() {{
            const grid = document.getElementById('coupons-grid');
            if (!grid) return;
            grid.innerHTML = '';

            const list = COUPONS_DATA.filter(c => {{
                if (currentCouponFilter === 'all') return true;
                if (currentCouponFilter === 'chain') return c.category === 'shopping' || c.area_tag === 'chain' || c.area.includes('chain');
                if (currentCouponFilter === 'drive_local') return c.category === 'drive_local' || c.area_tag === 'drive_local';
                return c.area.includes(currentCouponFilter) || c.area_tag === currentCouponFilter;
            }});

            list.forEach(c => {{
                const card = document.createElement('div');
                const isDrive = c.category === 'drive_local';
                // 嚴格統一卡片高度 h-full，flex flex-col justify-between，外框整齊劃一
                card.className = `bg-white rounded-3xl p-5 border-2 ${{isDrive ? 'border-amber-300 hover:border-amber-500 bg-gradient-to-b from-white to-amber-50/20' : 'border-red-200 hover:border-red-400 bg-white'}} shadow-sm hover:shadow-md transition flex flex-col justify-between h-full box-border space-y-3.5`;

                const barcodeSvg = renderBarcodeSvg(c.barcode, 200, 42);
                const qrSvg = renderQrSvg(c.barcode, 14);

                card.innerHTML = `
                    <div class="space-y-3 flex-1 flex flex-col">
                        <!-- 1. 頂部標籤列 (固定高度 24px) -->
                        <div class="flex items-center justify-between gap-1 h-6">
                            <span class="cute-pill ${{isDrive ? 'bg-amber-100 text-amber-800 border border-amber-300' : 'bg-red-100 text-red-700'}} font-black text-[10px] shrink-0">${{c.tag}}</span>
                            <span class="text-[11px] font-bold text-stone-400 truncate max-w-[150px]">📍 ${{c.area_name}}</span>
                        </div>

                        <!-- 2. 標題區塊 (固定高度 44px，垂直置中) -->
                        <div class="h-[44px] flex flex-col justify-center">
                            <h4 class="text-sm font-black text-stone-800 leading-tight line-clamp-1" title="${{c.title}}">${{c.title}}</h4>
                            <div class="text-[11px] text-stone-400 italic line-clamp-1 mt-0.5" title="${{c.title_jp}}">${{c.title_jp}}</div>
                        </div>

                        <!-- 3. 優惠詳情 (固定高度 94px，點擊導跳官方電子券/官網) -->
                        <div class="${{isDrive ? 'bg-gradient-to-r from-amber-50 to-orange-50 border-amber-200 hover:border-amber-400' : 'bg-gradient-to-r from-red-50 to-orange-50 border-red-200 hover:border-red-400'}} border rounded-2xl p-2.5 h-[94px] flex flex-col justify-between text-xs cursor-pointer hover:shadow-xs transition group select-none" onclick="window.open('${{c.official_url}}', '_blank')" title="點擊直接開啟官方優惠券網頁">
                            <div>
                                <div class="font-black text-red-700 flex items-center justify-between gap-1 text-[11px]">
                                    <div class="flex items-center gap-1 truncate">
                                        <span class="shrink-0">🎁 優惠：</span>
                                        <span class="truncate">${{c.discount}}</span>
                                    </div>
                                    <span class="text-[10px] text-red-600 font-black group-hover:underline flex items-center gap-0.5 shrink-0">
                                        <span>開啟</span> <span>↗</span>
                                    </span>
                                </div>
                                <div class="text-[11px] text-stone-600 font-bold line-clamp-1 mt-1">${{c.condition}}</div>
                            </div>
                            <div class="text-[10px] text-amber-800 bg-white/80 px-2 py-0.5 rounded-lg border border-amber-200/70 font-medium truncate">
                                💡 點此框跳轉至【${{c.official_name || '官方核銷專頁'}}】
                            </div>
                        </div>

                        <!-- 4. 條碼與 QRcode 掃描展示區 (固定高度 148px) -->
                        <div class="p-2.5 bg-stone-50 rounded-2xl border-2 border-stone-200 h-[148px] flex flex-col justify-between text-center">
                            <div class="flex items-center justify-between gap-2 flex-1">
                                <div class="flex-1 bg-white p-2 rounded-xl border border-stone-200 cursor-pointer hover:border-red-300 transition h-full flex flex-col justify-center items-center" onclick="openBarcodeModal('${{c.id}}')" title="點擊全螢幕放大條碼">
                                    <div class="w-full flex justify-center">${{barcodeSvg}}</div>
                                    <div class="font-mono text-xs font-bold text-stone-700 tracking-wider mt-1">${{c.barcode}}</div>
                                </div>
                                <div class="bg-white p-1.5 rounded-xl border border-stone-200 cursor-pointer hover:border-red-300 transition shrink-0 h-full flex items-center justify-center" onclick="openBarcodeModal('${{c.id}}')" title="點擊全螢幕放大二維碼">
                                    ${{qrSvg}}
                                </div>
                            </div>
                            <div class="text-[10px] text-stone-500 font-medium line-clamp-1 mt-1.5 pt-1 border-t border-stone-200/60" title="${{c.usage_guide ? c.usage_guide : '結帳時點擊「條碼」可直接全螢幕放大讓店員掃描'}}">
                                ${{c.usage_guide ? c.usage_guide : '💡 點擊「條碼」可全螢幕放大讓店員掃描'}}
                            </div>
                        </div>

                        <!-- 5. 適用地點 (固定高度 36px) -->
                        <div class="text-[11px] text-stone-500 bg-stone-50 px-2.5 py-1.5 rounded-xl border border-stone-100 h-[36px] flex items-center truncate" title="${{c.stores}}">
                            <span class="shrink-0 font-bold text-stone-600">適用：</span>
                            <span class="truncate">${{c.stores}}</span>
                        </div>
                    </div>

                    <!-- 6. 底部等寬等高按鈕 Grid (固定 3 欄等寬，每顆高 36px，整整齊齊) -->
                    <div class="pt-2 border-t border-stone-100 grid grid-cols-3 gap-1.5 w-full">
                        <button type="button" onclick="openBarcodeModal('${{c.id}}')" class="h-9 rounded-xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-700 hover:to-rose-700 text-white font-black text-[11px] flex items-center justify-center gap-1 shadow-2xs active:scale-95 transition" title="放大條碼供店員掃描">
                            <span>🔍</span> <span class="truncate">放大條碼</span>
                        </button>
                        <a href="${{c.official_url}}" target="_blank" class="h-9 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 font-bold text-[11px] flex items-center justify-center gap-1 active:scale-95 transition" title="開啟官方網址">
                            <span>🌐</span> <span class="truncate">官方網頁 ↗</span>
                        </a>
                        <a href="${{c.google_maps}}" target="_blank" class="h-9 rounded-xl bg-sky-50 hover:bg-sky-100 text-sky-700 border border-sky-200 font-bold text-[11px] flex items-center justify-center gap-1 active:scale-95 transition" title="Google Maps 導航">
                            <span>🗺️</span> <span class="truncate">地圖導航</span>
                        </a>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        function openBarcodeModal(couponId) {{
            const c = COUPONS_DATA.find(item => item.id === couponId);
            if (!c) return;
            const modal = document.getElementById('barcode-modal');
            const titleEl = document.getElementById('modal-coupon-title');
            const barcodeSvgEl = document.getElementById('modal-barcode-svg');
            const barcodeNumEl = document.getElementById('modal-barcode-num');
            const qrSvgEl = document.getElementById('modal-qr-svg');
            const condEl = document.getElementById('modal-coupon-condition');
            const officialBtn = document.getElementById('modal-official-link-btn');
            const alertEl = document.getElementById('modal-coupon-alert');

            if (titleEl) titleEl.textContent = c.title;
            if (barcodeSvgEl) barcodeSvgEl.innerHTML = renderBarcodeSvg(c.barcode, 260, 65);
            if (barcodeNumEl) barcodeNumEl.textContent = c.barcode;
            if (qrSvgEl) qrSvgEl.innerHTML = renderQrSvg(c.barcode, 24);
            if (condEl) condEl.textContent = `${{c.discount}} ｜ ${{c.condition}} ｜ 有效期：${{c.expiry}}`;

            if (officialBtn) {{
                officialBtn.href = c.official_url;
                officialBtn.textContent = `🌐 開啟官方頁面 (${{c.official_name || '官方專區'}}) ↗`;
            }}

            if (alertEl) {{
                if (c.usage_guide) {{
                    alertEl.textContent = c.usage_guide;
                    alertEl.classList.remove('hidden');
                }} else {{
                    alertEl.textContent = '💡 請將手機螢幕亮度調至最大，直接出示給店員掃描；若店員要求點擊折價券，請點擊下方「開啟官方電子券網頁」！';
                    alertEl.classList.remove('hidden');
                }}
            }}

            if (modal) modal.classList.remove('hidden');
        }}

        function closeBarcodeModal() {{
            const modal = document.getElementById('barcode-modal');
            if (modal) modal.classList.add('hidden');
        }}

        function detectUserLocationForCoupons() {{
            const statusEl = document.getElementById('coupon-location-status');
            if (!navigator.geolocation) {{
                showToast("您的瀏覽器暫不支援自動定位，請直接點選上方城市標籤！");
                return;
            }}
            if (statusEl) statusEl.textContent = "🧭 正在取得您的位置...";
            showToast("🧭 正在定位中，將為您篩選周邊最近的優惠券...");

            navigator.geolocation.getCurrentPosition(
                (pos) => {{
                    const lat = pos.coords.latitude;
                    const lon = pos.coords.longitude;
                    // Distances to hubs
                    const dKuma = Math.hypot(lat - 32.80, lon - 130.70);
                    const dMiya = Math.hypot(lat - 31.91, lon - 131.42);
                    const dKago = Math.hypot(lat - 31.59, lon - 130.55);
                    
                    let detected = 'chain';
                    let locName = '全九州連鎖免稅';
                    if (dKuma <= dMiya && dKuma <= dKago) {{
                        detected = 'kumamoto';
                        locName = '熊本市區';
                    }} else if (dKago <= dKuma && dKago <= dMiya) {{
                        detected = 'kagoshima';
                        locName = '鹿兒島市區';
                    }} else {{
                        detected = 'miyazaki';
                        locName = '宮崎日南';
                    }}
                    
                    filterCoupons(detected);
                    if (statusEl) statusEl.textContent = `📍 已自動為您切換至【${{locName}}】專屬優惠`;
                    showToast(`🧭 定位成功！已篩選【${{locName}}】優惠券！`);
                }},
                (err) => {{
                    if (statusEl) statusEl.textContent = "";
                    showToast("定位權限未開啟或超時，已為您顯示全區優惠券！");
                    filterCoupons('all');
                }},
                {{ timeout: 7000 }}
            );
        }}

        // ======================= 美食候選清單系統 =======================
        let shortlistedRestaurants = new Set(JSON.parse(localStorage.getItem('kyushu_shortlist_restaurants') || '[]'));

        function toggleShortlist(restId) {{
            if (shortlistedRestaurants.has(restId)) {{
                shortlistedRestaurants.delete(restId);
                showToast("已從美食候選清單中移除 ⚪");
            }} else {{
                shortlistedRestaurants.add(restId);
                showToast("⭐ 已加入我的美食候選清單！");
            }}
            localStorage.setItem('kyushu_shortlist_restaurants', JSON.stringify(Array.from(shortlistedRestaurants)));
            updateShortlistBadge();
            renderRestaurants();
        }}

        function updateShortlistBadge() {{
            const badge = document.getElementById('shortlist-count-badge');
            if (badge) badge.textContent = shortlistedRestaurants.size;
        }}

        function renderRestaurants() {{
            const container = document.getElementById('restaurants-grid');
            if (!container) return;
            container.innerHTML = '';

            const list = TRIP_DATA.restaurants_directory || [];

            const filtered = list.filter(r => {{
                if (currentRestFilter.meal !== 'all' && r.meal_type !== currentRestFilter.meal) return false;
                if (currentRestFilter.day !== 'all' && String(r.day) !== currentRestFilter.day) return false;
                if (currentRestFilter.theme === 'shortlist') {{
                    if (!shortlistedRestaurants.has(r.id)) return false;
                }}
                if (currentRestFilter.theme === 'meat') {{
                    const text = (r.name + r.must_eat + r.tag).toLowerCase();
                    if (!text.includes('牛') && !text.includes('豚') && !text.includes('鰻') && !text.includes('肉')) return false;
                }}
                if (currentRestFilter.theme === 'reserve') {{
                    if (!r.reserve_type.includes('預約') && !r.reserve_type.includes('訂位')) return false;
                }}
                if (currentRestFilter.theme === 'bar') {{
                    const isBar = r.meal_type === 'latenight' || (r.name + r.tag + r.must_eat).toLowerCase().includes('bar') || (r.name + r.tag).includes('酒');
                    if (!isBar) return false;
                }}
                if (currentRestFilter.search) {{
                    const q = currentRestFilter.search;
                    const combined = (r.name + r.name_jp + r.area + r.must_eat + r.desc + r.tag).toLowerCase();
                    if (!combined.includes(q)) return false;
                }}
                return true;
            }});

            if (filtered.length === 0) {{
                container.innerHTML = `
                    <div class="col-span-full py-12 text-center text-stone-400 text-xs font-bold space-y-2">
                        <div class="text-3xl">🔍🍽️</div>
                        <p>查無符合的美食推薦，請調整上方篩選條件或清除搜尋關鍵字。</p>
                        <button onclick="clearAllRestFilters()" class="px-3 py-1.5 rounded-xl bg-orange-100 text-orange-800 hover:bg-orange-200 transition">重設所有篩選</button>
                    </div>
                `;
                return;
            }}

            filtered.forEach(r => {{
                const card = document.createElement('div');
                card.id = `rest-card-${{r.id}}`;

                const isShortlisted = shortlistedRestaurants.has(r.id);
                const mapSearchUrl = `https://www.google.com/maps/search/?api=1&query=${{encodeURIComponent(r.name + ' ' + r.area)}}`;
                const isReserveRecommended = r.reserve_type.includes('預約') || r.reserve_type.includes('訂位');

                // 4 大餐別專屬鮮明底色與主題徽章
                let cardThemeClass = 'bg-white border-2 border-stone-200 hover:border-orange-300';
                let mealBadgeClass = 'bg-orange-100 text-orange-800 border-orange-200';
                let mustEatBgClass = 'bg-amber-50/80 border-amber-200 text-amber-900';

                if (r.meal_type === 'breakfast') {{
                    cardThemeClass = 'bg-gradient-to-b from-amber-50/80 via-white to-white border-2 border-amber-300/80 hover:border-amber-400';
                    mealBadgeClass = 'bg-amber-100 text-amber-900 border border-amber-300 font-black';
                    mustEatBgClass = 'bg-amber-100/60 border border-amber-200 text-amber-950';
                }} else if (r.meal_type === 'lunch') {{
                    cardThemeClass = 'bg-gradient-to-b from-emerald-50/80 via-white to-white border-2 border-emerald-300/80 hover:border-emerald-400';
                    mealBadgeClass = 'bg-emerald-100 text-emerald-900 border border-emerald-300 font-black';
                    mustEatBgClass = 'bg-emerald-100/60 border border-emerald-200 text-emerald-950';
                }} else if (r.meal_type === 'dinner') {{
                    cardThemeClass = 'bg-gradient-to-b from-rose-50/80 via-white to-white border-2 border-rose-300/80 hover:border-rose-400';
                    mealBadgeClass = 'bg-rose-100 text-rose-900 border border-rose-300 font-black';
                    mustEatBgClass = 'bg-rose-100/60 border border-rose-200 text-rose-950';
                }} else if (r.meal_type === 'latenight') {{
                    cardThemeClass = 'bg-gradient-to-b from-purple-50/80 via-white to-white border-2 border-purple-300/80 hover:border-purple-400';
                    mealBadgeClass = 'bg-purple-100 text-purple-900 border border-purple-300 font-black';
                    mustEatBgClass = 'bg-purple-100/60 border border-purple-200 text-purple-950';
                }}

                // 選取圖卡時立即改變底色與邊框光圈！
                if (isShortlisted) {{
                    cardThemeClass = '!bg-amber-50 !border-2 !border-amber-500 shadow-md ring-4 ring-amber-300/80 scale-[1.01]';
                }}

                card.className = `${{cardThemeClass}} rounded-3xl p-5 transition-all duration-300 space-y-3.5 shadow-sm hover:shadow-md flex flex-col justify-between`;

                card.innerHTML = `
                    <div class="space-y-2.5">
                        <div class="flex items-center justify-between gap-1 flex-wrap">
                            <div class="flex items-center gap-1.5">
                                <span class="cute-pill ${{mealBadgeClass}} font-black">${{r.meal_name}}</span>
                                <span class="cute-pill bg-white border border-stone-200 text-stone-600 font-bold">Day ${{r.day}}</span>
                                ${{isShortlisted ? '<span class="cute-pill bg-amber-500 text-white font-black text-[10px] shadow-xs">⭐ 候選中</span>' : ''}}
                            </div>
                            <div class="flex items-center gap-1.5">
                                <button type="button" onclick="toggleShortlist('${{r.id}}')" class="px-2 py-0.5 rounded-full ${{isShortlisted ? 'bg-amber-500 text-white font-black shadow-xs' : 'bg-white border border-stone-200 text-stone-500 hover:bg-stone-50'}} text-[11px] font-bold transition">
                                    ${{isShortlisted ? '⭐ 鎖定' : '☆ 候選'}}
                                </button>
                                <span class="text-[11px] font-bold text-stone-400">📍 ${{r.area}}</span>
                            </div>
                        </div>

                        <div>
                            <h4 class="text-sm font-black text-stone-800 flex items-center justify-between">
                                <span>${{r.name}}</span>
                            </h4>
                            <div class="text-[11px] text-stone-400 font-medium italic mt-0.5">${{r.name_jp}}</div>
                        </div>

                        <!-- 必吃招牌菜 -->
                        <div class="${{mustEatBgClass}} rounded-2xl p-2.5 text-xs leading-snug">
                            <div class="font-black flex items-center gap-1 mb-0.5 text-[11px]">
                                <span>🍴 必吃招牌：</span>
                            </div>
                            <div class="font-bold">${{r.must_eat}}</div>
                        </div>

                        <!-- 價位與預約指引 -->
                        <div class="space-y-1.5 text-xs text-stone-600">
                            <div class="flex items-center justify-between text-[11px]">
                                <span class="font-bold text-stone-400">預估價位：</span>
                                <span class="font-mono font-bold text-stone-700">${{r.price}}</span>
                            </div>
                            <div class="flex items-start justify-between gap-2 text-[11px]">
                                <span class="font-bold text-stone-400 shrink-0">訂位指引：</span>
                                <span class="font-bold ${{isReserveRecommended ? 'text-rose-600' : 'text-emerald-700'}} text-right">${{r.reserve_type}}</span>
                            </div>
                            <div class="text-[11px] text-stone-500 bg-white/70 p-2 rounded-xl border border-stone-200/80 leading-normal">
                                💡 ${{r.reserve_guide}}
                            </div>
                            ${{r.tips ? `
                                <div class="text-[11px] text-orange-900 bg-orange-50/70 p-2 rounded-xl border border-orange-200 leading-normal">
                                    ✨ <strong>老饕叮嚀：</strong>${{r.tips}}
                                </div>
                            ` : ''}}
                        </div>
                    </div>

                    <!-- 動作按鈕：線上訂位 + 導航 + 電話 -->
                    <div class="pt-2 border-t border-stone-100 flex items-center gap-2">
                        <a href="${{r.reserve_url}}" target="_blank" class="flex-1 py-2 px-3 rounded-xl ${{isReserveRecommended ? 'bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-700 hover:to-rose-700 text-white' : 'bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-700 hover:to-amber-700 text-white'}} font-black text-xs flex items-center justify-center gap-1 shadow-sm transition text-center">
                            <span>🎫</span>
                            <span>${{isReserveRecommended ? '前往線上預約 ↗' : '查看店家詳情 ↗'}}</span>
                        </a>
                        <a href="${{mapSearchUrl}}" target="_blank" class="py-2 px-3 rounded-xl bg-sky-50 hover:bg-sky-100 text-sky-700 border border-sky-200 font-bold text-xs flex items-center justify-center gap-1 transition" title="Google Maps 導航">
                            <span>🗺️</span>
                        </a>
                        ${{r.phone && r.phone !== '-' ? `
                            <a href="tel:${{r.phone}}" class="py-2 px-3 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 font-bold text-xs flex items-center justify-center gap-1 transition" title="撥打電話 (代訂預約)">
                                <span>📞</span>
                            </a>
                        ` : ''}}
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function clearAllRestFilters() {{
            currentRestFilter = {{ meal: 'all', day: 'all', theme: 'all', search: '' }};
            const input = document.getElementById('rest-search-input');
            if (input) input.value = '';
            updateRestFilterUI();
            renderRestaurants();
        }}

        function jumpToRestaurant(restId) {{
            openTab('restaurants');
            currentRestFilter = {{ meal: 'all', day: 'all', theme: 'all', search: '' }};
            const input = document.getElementById('rest-search-input');
            if (input) input.value = '';
            updateRestFilterUI();
            renderRestaurants();

            setTimeout(() => {{
                const card = document.getElementById(`rest-card-${{restId}}`);
                if (card) {{
                    card.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    card.classList.add('ring-4', 'ring-orange-500', 'ring-offset-2', 'scale-[1.02]');
                    setTimeout(() => {{
                        card.classList.remove('ring-4', 'ring-orange-500', 'ring-offset-2', 'scale-[1.02]');
                    }}, 3000);
                }}
            }}, 200);
        }}

        function jumpToDayRestaurants(dayNum) {{
            openTab('restaurants');
            currentRestFilter.day = String(dayNum);
            currentRestFilter.meal = 'all';
            currentRestFilter.theme = 'all';
            currentRestFilter.search = '';
            const input = document.getElementById('rest-search-input');
            if (input) input.value = '';
            updateRestFilterUI();
            renderRestaurants();
        }}

        function scrollToMeal(mType) {{
            const el = document.getElementById(`day-meals-${{mType}}-list`);
            if (el) {{
                el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                const card = el.closest('.rounded-2xl');
                if (card) {{
                    card.classList.add('ring-4', 'ring-purple-400', 'transition-all');
                    setTimeout(() => card.classList.remove('ring-4', 'ring-purple-400'), 1800);
                }}
            }} else {{
                const container = document.getElementById('day-meals-container');
                if (container) container.scrollIntoView({{ behavior: 'smooth' }});
            }}
        }}

        function renderDayMealsSection(dayPlan, idx) {{
            let mealsContainer = document.getElementById('day-meals-container');
            if (!mealsContainer) {{
                const itineraryTab = document.getElementById('tab-content-itinerary');
                mealsContainer = document.createElement('div');
                mealsContainer.id = 'day-meals-container';
                mealsContainer.className = 'cute-card p-5 sm:p-6 border-2 border-orange-200 bg-white relative space-y-5 shadow-sm w-full overflow-hidden mt-6';
                itineraryTab.appendChild(mealsContainer);
            }}
            mealsContainer.innerHTML = '';

            const meals = dayPlan.meals;
            if (!meals) return;

            const hasLateNight = !!meals.latenight && meals.latenight.length > 0;
            // 響應式優化：在桌面 (>=1024px) 一字排開 4 欄；平板 2 欄；手機 1 欄，確保每張卡片皆有充足寬度
            const gridColsClass = hasLateNight ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4' : 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3';

            mealsContainer.innerHTML = `
                <div class="washi-tape washi-tape-gold"></div>
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b-2 border-orange-100">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="cute-pill bg-orange-100 text-orange-800 font-black">🍽️ 當日美饌與微醺提案</span>
                            <span class="text-xs text-stone-500 font-medium">${{hasLateNight ? '早・午・晚・宵夜酒吧 各 3 選（共 12 選）' : '早・午・晚 各 3 選（共 9 選）'}}</span>
                        </div>
                        <h4 class="text-base sm:text-lg font-black text-stone-800 mt-1 flex items-center gap-2">
                            <span>🍱</span> Day ${{idx + 1}} 專屬美饌特搜清單
                        </h4>
                    </div>
                    <button type="button" onclick="jumpToDayRestaurants(${{idx + 1}})" class="px-4 py-2 rounded-2xl bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-black text-xs flex items-center gap-1.5 shadow-sm transition active:scale-95 shrink-0 self-start sm:self-auto">
                        <span>🍱</span> 前往餐廳總整理做訂位 ↗
                    </button>
                </div>

                <div class="grid ${{gridColsClass}} gap-3.5 sm:gap-4 text-xs">
                    <!-- 早餐 -->
                    <div class="bg-amber-50/50 rounded-2xl p-3 sm:p-3.5 border border-amber-200/90 space-y-2.5 flex flex-col justify-between">
                        <div>
                            <div class="font-black text-stone-800 flex items-center justify-between pb-1.5 border-b border-amber-200">
                                <span class="flex items-center gap-1"><span>🌅</span> 早餐 3 選</span>
                                <span class="text-[10px] text-amber-800 font-bold">活力朝食</span>
                            </div>
                            <div class="space-y-2 mt-2.5" id="day-meals-breakfast-list"></div>
                        </div>
                    </div>

                    <!-- 午餐 -->
                    <div class="bg-orange-50/50 rounded-2xl p-3 sm:p-3.5 border border-orange-200/90 space-y-2.5 flex flex-col justify-between">
                        <div>
                            <div class="font-black text-stone-800 flex items-center justify-between pb-1.5 border-b border-orange-200">
                                <span class="flex items-center gap-1"><span>☀️</span> 午餐 3 選</span>
                                <span class="text-[10px] text-orange-800 font-bold">在地名物</span>
                            </div>
                            <div class="space-y-2 mt-2.5" id="day-meals-lunch-list"></div>
                        </div>
                    </div>

                    <!-- 晚餐 -->
                    <div class="bg-rose-50/50 rounded-2xl p-3 sm:p-3.5 border border-rose-200/90 space-y-2.5 flex flex-col justify-between">
                        <div>
                            <div class="font-black text-stone-800 flex items-center justify-between pb-1.5 border-b border-rose-200">
                                <span class="flex items-center gap-1"><span>🌙</span> 晚餐 3 選</span>
                                <span class="text-[10px] text-rose-800 font-bold">夜間饗宴</span>
                            </div>
                            <div class="space-y-2 mt-2.5" id="day-meals-dinner-list"></div>
                        </div>
                    </div>

                    ${{hasLateNight ? `
                    <!-- 宵夜＆酒吧 -->
                    <div class="bg-purple-50/50 rounded-2xl p-3 sm:p-3.5 border border-purple-200/90 space-y-2.5 flex flex-col justify-between">
                        <div>
                            <div class="font-black text-stone-800 flex items-center justify-between pb-1.5 border-b border-purple-200">
                                <span class="flex items-center gap-1"><span>🍸</span> 宵夜＆酒吧 3 選</span>
                                <span class="text-[10px] text-purple-800 font-bold">微醺夜食</span>
                            </div>
                            <div class="space-y-2 mt-2.5" id="day-meals-latenight-list"></div>
                        </div>
                    </div>
                    ` : ''}}
                </div>
            `;

            ['breakfast', 'lunch', 'dinner', 'latenight'].forEach(mType => {{
                const container = document.getElementById(`day-meals-${{mType}}-list`);
                if (!container || !meals[mType]) return;

                meals[mType].forEach(opt => {{
                    const row = document.createElement('div');
                    // 增強 Hover 特效：光暈外框 ring-4、平滑上浮 -translate-y-1.5、強烈投影 shadow-xl、指針 cursor-pointer、金黃微光漸變
                    row.className = 'group relative bg-white hover:bg-gradient-to-br hover:from-white hover:to-orange-50/70 p-3 rounded-2xl border-2 border-stone-200/90 hover:border-orange-400 hover:ring-4 hover:ring-orange-200/60 shadow-2xs hover:shadow-xl transition-all duration-200 flex flex-col justify-between h-[152px] min-h-[152px] max-h-[152px] overflow-hidden box-border w-full cursor-pointer select-none';
                    row.title = '點擊查看餐廳詳細訂位攻略 ↗';
                    row.onclick = (e) => {{
                        if (e.target.closest('a')) return;
                        jumpToRestaurant(opt.id);
                    }};
                    
                    // 1. 精簡訂位標籤為 2~4 字
                    const rawRes = (opt.reserve_type || '').toLowerCase();
                    let badgeLabel = '現場入座';
                    let badgeClass = 'bg-emerald-50 text-emerald-800 border-emerald-200';
                    let badgeIcon = '⚡';
                    
                    if (rawRes.includes('房客') || rawRes.includes('住宿') || rawRes.includes('朝食')) {{
                        badgeLabel = '房客專享';
                        badgeClass = 'bg-purple-50 text-purple-800 border-purple-200';
                        badgeIcon = '🏨';
                    }} else if (rawRes.includes('免預約') || rawRes.includes('無需預約')) {{
                        badgeLabel = '免預約';
                        badgeClass = 'bg-emerald-50 text-emerald-800 border-emerald-200';
                        badgeIcon = '⚡';
                    }} else if (rawRes.includes('現場排隊') || rawRes.includes('現場候位') || rawRes.includes('取號')) {{
                        badgeLabel = '現場候位';
                        badgeClass = 'bg-teal-50 text-teal-800 border-teal-200';
                        badgeIcon = '⏳';
                    }} else if (rawRes.includes('線上預約') || rawRes.includes('官網預約')) {{
                        badgeLabel = '線上預約';
                        badgeClass = 'bg-rose-50 text-rose-800 border-rose-200';
                        badgeIcon = '📅';
                    }} else if (rawRes.includes('電話預約')) {{
                        badgeLabel = '電話預約';
                        badgeClass = 'bg-rose-50 text-rose-800 border-rose-200';
                        badgeIcon = '📞';
                    }} else if (rawRes.includes('預約') || rawRes.includes('訂位') || rawRes.includes('洽詢')) {{
                        badgeLabel = '需預約';
                        badgeClass = 'bg-rose-50 text-rose-800 border-rose-200';
                        badgeIcon = '📅';
                    }}

                    // 2. 乾淨純粹的店名
                    let cleanName = (opt.name || '').trim();
                    cleanName = cleanName.replace(/\s*[\(（][^()（）]*[\)）]/g, '').trim();
                    cleanName = cleanName.replace(/\s*(炭焙手沖咖啡|手作泡芙與點心|晨光日式朝食|和洋朝食百匯|特選咖哩與在地小酌|夜間酒餚居酒時光|天然溫泉和洋朝食|展望赤牛漢堡排|元祖流水麵)$/g, '').trim();

                    // 3. 價格精簡乾淨
                    let cleanPrice = (opt.price || '').split('~')[0].split('/')[0].trim();
                    if (cleanPrice.includes('住宿內含')) cleanPrice = '住宿內含';
                    if (cleanPrice.includes('機票內含') || cleanPrice.includes('機票資格')) cleanPrice = '機票內含';

                    // 4. 地點精簡
                    const cleanArea = (opt.area || '').split(' ')[0].trim();

                    row.innerHTML = `
                        <div class="space-y-1.5 min-w-0 pointer-events-none">
                            <!-- 頂部獨立標籤列 (含 hover 提示) -->
                            <div class="flex items-center justify-between gap-1 min-w-0">
                                <span class="inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-md border ${{badgeClass}} font-bold shrink-0 shadow-2xs">
                                    <span>${{badgeIcon}}</span>
                                    <span>${{badgeLabel}}</span>
                                </span>
                                <div class="flex items-center gap-1 shrink-0">
                                    ${{cleanArea ? `<span class="text-[10px] text-stone-400 font-bold truncate max-w-[65px]">📍 ${{cleanArea}}</span>` : ''}}
                                    <span class="text-[10px] text-orange-600 font-black opacity-0 group-hover:opacity-100 transition-opacity">點擊攻略 ↗</span>
                                </div>
                            </div>

                            <!-- 乾淨純粹店名 (hover 強烈變色) -->
                            <h5 class="font-black text-stone-800 group-hover:text-orange-600 text-xs sm:text-[13px] leading-snug tracking-tight transition truncate" title="${{opt.name}}">
                                ${{cleanName}}
                            </h5>

                            <!-- 必吃特色推薦小卡 -->
                            <div class="bg-stone-50 group-hover:bg-white rounded-lg px-2 py-1 text-[11px] text-stone-600 font-medium line-clamp-1 border border-stone-100 group-hover:border-orange-200 transition">
                                🍴 <span class="text-stone-700 font-bold">${{opt.must_eat}}</span>
                            </div>
                        </div>

                        <!-- 底部價格與操作區 -->
                        <div class="flex items-center justify-between pt-1.5 border-t border-stone-100 text-[11px] gap-1.5 min-w-0 w-full mt-auto">
                            <span class="font-mono text-stone-800 font-black tracking-tight text-xs truncate min-w-0 flex-1 pointer-events-none">
                                ${{cleanPrice}}
                            </span>
                            <div class="flex items-center gap-1 shrink-0">
                                <span class="whitespace-nowrap px-2 py-0.5 rounded-md bg-orange-50 group-hover:bg-orange-500 text-orange-700 group-hover:text-white border border-orange-200 group-hover:border-orange-500 text-[10px] font-black transition active:scale-95 shadow-2xs pointer-events-none">
                                    攻略 ↗
                                </span>
                                <a href="https://www.google.com/maps/search/?api=1&query=${{encodeURIComponent(opt.name + ' ' + (opt.area || ''))}}" target="_blank" onclick="event.stopPropagation()" class="w-5 h-5 rounded-md bg-sky-50 hover:bg-sky-100 text-sky-700 border border-sky-200 flex items-center justify-center text-[10px] font-bold transition active:scale-95 shadow-2xs shrink-0 pointer-events-auto" title="Google 地圖導航">
                                    🗺️
                                </a>
                            </div>
                        </div>
                    `;
                    container.appendChild(row);
                }});
            }});
        }}


        // ======================= 九州手繪地圖互動邏輯 =======================
        function initHandDrawnMap() {{
            renderMapPins('all');
            switchQuickPickTab('hotels');
            resetMapDetailCard();
        }}

        function resetMapDetailCard() {{
            selectedPinId = null;
            document.querySelectorAll('.map-pin').forEach(pin => pin.classList.remove('active'));

            const dayEl = document.getElementById('card-day');
            if (dayEl) dayEl.textContent = '✨ 點選地圖圖釘';
            const titleEl = document.getElementById('card-title');
            if (titleEl) titleEl.textContent = '南九州手繪地圖';
            const catEl = document.getElementById('card-category');
            if (catEl) catEl.textContent = '點擊圖示展開亮點';
            const iconEl = document.getElementById('card-icon');
            if (iconEl) iconEl.textContent = '📍';
            const descEl = document.getElementById('card-desc');
            if (descEl) descEl.textContent = '點選左側手繪地圖上的任意圖釘圖示，地標將會「彈出放大」並在此呈現完整遊玩情報、避坑叮嚀與一鍵 Google Maps 導航！';
            const tipsEl = document.getElementById('card-tips');
            if (tipsEl) tipsEl.innerHTML = '<strong>自駕小提示：</strong>南九州山路與沿海風景絕美，點選景點圖釘可直接導航，出發前記得檢查油量喔！';
            const mapLink = document.getElementById('card-map-link');
            if (mapLink) {{
                mapLink.href = 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent('南九州自駕');
            }}
        }}

        let showAllMapLabels = false;

        function toggleMapLabels() {{
            showAllMapLabels = !showAllMapLabels;
            const pinsGroup = document.getElementById('map-pins-group');
            const btn = document.getElementById('map-btn-labels');
            if (pinsGroup) {{
                if (showAllMapLabels) pinsGroup.classList.add('show-all-labels');
                else pinsGroup.classList.remove('show-all-labels');
            }}
            if (btn) {{
                btn.textContent = showAllMapLabels ? '🏷️ 地名：全顯示中' : '🏷️ 地名：點選才彈出';
                btn.className = showAllMapLabels 
                    ? 'px-2.5 py-1 rounded-full bg-stone-800 text-white shadow-sm transition' 
                    : 'px-2.5 py-1 rounded-full bg-stone-100 text-stone-600 hover:bg-stone-200 transition';
            }}
        }}

        let currentMapFilter = 'all';

        function filterMap(category) {{
            currentMapFilter = category;
            ['all', 'hotel', 'sight', 'transit'].forEach(cat => {{
                const btn = document.getElementById(`map-btn-${{cat}}`);
                if (btn) {{
                    if (cat === category) {{
                        btn.className = 'px-2.5 py-1 rounded-full bg-emerald-700 text-white shadow-sm transition';
                    }} else {{
                        btn.className = 'px-2.5 py-1 rounded-full bg-stone-100 text-stone-600 hover:bg-stone-200 transition';
                    }}
                }}
            }});
            renderMapPins(category);
        }}

        function toggleMapRoute(day) {{
            selectDayRoute(day);
        }}

        function resetMapRoutes() {{
            selectDayRoute('all');
        }}

        function renderMapPins(filterCategory) {{
            const pinsGroup = document.getElementById('map-pins-group');
            if (!pinsGroup) return;
            pinsGroup.innerHTML = '';

            MAP_LANDMARKS.forEach(lm => {{
                if (filterCategory !== 'all' && lm.category !== filterCategory) return;

                const isSelected = lm.id === selectedPinId;
                const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                g.setAttribute('class', `map-pin ${{isSelected ? 'active' : ''}}`);
                g.setAttribute('id', `pin-${{lm.id}}`);
                g.onclick = (e) => {{
                    e.stopPropagation();
                    selectLandmark(lm.id);
                }};

                // 柔和陰影
                const circleShadow = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                circleShadow.setAttribute('cx', lm.x);
                circleShadow.setAttribute('cy', lm.y + 3);
                circleShadow.setAttribute('r', '14');
                circleShadow.setAttribute('fill', 'rgba(0,0,0,0.15)');
                circleShadow.setAttribute('class', 'pointer-events-none');
                g.appendChild(circleShadow);

                // 水波雷達漣漪 (選中時彈出擴散)
                const rippleCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                rippleCircle.setAttribute('class', 'pin-ripple');
                rippleCircle.setAttribute('cx', lm.x);
                rippleCircle.setAttribute('cy', lm.y);
                rippleCircle.setAttribute('r', '16');
                rippleCircle.setAttribute('fill', 'none');
                rippleCircle.setAttribute('stroke', lm.color || '#dc2626');
                rippleCircle.setAttribute('stroke-width', '2.5');
                g.appendChild(rippleCircle);

                // 核心圖釘圓圈
                const bgCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                bgCircle.setAttribute('class', 'pin-circle');
                bgCircle.setAttribute('cx', lm.x);
                bgCircle.setAttribute('cy', lm.y);
                bgCircle.setAttribute('r', isSelected ? '23' : '15');
                bgCircle.setAttribute('fill', isSelected ? '#fff5f5' : '#ffffff');
                bgCircle.setAttribute('stroke', isSelected ? '#c92a2a' : (lm.color || '#dc2626'));
                bgCircle.setAttribute('stroke-width', isSelected ? '4.5' : '2.5');
                g.appendChild(bgCircle);

                // 圖釘內可愛 Emoji (完美居中對齊)
                const textIcon = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                textIcon.setAttribute('class', 'pin-icon pointer-events-none select-none');
                textIcon.setAttribute('x', lm.x);
                textIcon.setAttribute('y', lm.y);
                textIcon.setAttribute('dominant-baseline', 'central');
                textIcon.setAttribute('text-anchor', 'middle');
                textIcon.setAttribute('font-size', isSelected ? '17' : '13');
                textIcon.textContent = lm.icon;
                g.appendChild(textIcon);

                // 浮動日系膠囊標籤 (預設隱藏，點擊圖釘後彈出放大！)
                const labelText = lm.shortName || lm.name;
                const labelWidth = Math.max(70, labelText.length * 13 + 16);
                const labelHeight = 26;
                const pos = lm.labelPos || 'top';

                let rectX = lm.x - labelWidth / 2;
                let rectY = lm.y - 45;

                if (pos === 'bottom') {{
                    rectX = lm.x - labelWidth / 2;
                    rectY = lm.y + 24;
                }} else if (pos === 'left') {{
                    rectX = lm.x - labelWidth - 18;
                    rectY = lm.y - 13;
                }} else if (pos === 'right') {{
                    rectX = lm.x + 18;
                    rectY = lm.y - 13;
                }}

                const badgeG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                badgeG.setAttribute('class', `pin-badge pointer-events-none select-none ${{isSelected ? 'active' : ''}}`);

                // 膠囊白底
                const bgRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                bgRect.setAttribute('x', rectX);
                bgRect.setAttribute('y', rectY);
                bgRect.setAttribute('width', labelWidth);
                bgRect.setAttribute('height', labelHeight);
                bgRect.setAttribute('rx', '13');
                bgRect.setAttribute('fill', '#ffffff');
                bgRect.setAttribute('stroke', '#c92a2a');
                bgRect.setAttribute('stroke-width', '2');
                bgRect.setAttribute('filter', 'url(#cute-shadow)');
                badgeG.appendChild(bgRect);

                // 醒目標籤文字 (大字號 13px，加粗紅字)
                const labelT = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                labelT.setAttribute('x', rectX + labelWidth / 2);
                labelT.setAttribute('y', rectY + 13);
                labelT.setAttribute('dominant-baseline', 'central');
                labelT.setAttribute('text-anchor', 'middle');
                labelT.setAttribute('font-size', '13');
                labelT.setAttribute('font-weight', '900');
                labelT.setAttribute('fill', '#c92a2a');
                labelT.textContent = labelText;
                badgeG.appendChild(labelT);

                g.appendChild(badgeG);
                pinsGroup.appendChild(g);
            }});

            if (showAllMapLabels) {{
                pinsGroup.classList.add('show-all-labels');
            }}
        }}

        function selectLandmark(landmarkId) {{
            selectedPinId = landmarkId;
            const lm = MAP_LANDMARKS.find(item => item.id === landmarkId);
            if (!lm) return;

            // 移除其他圖釘 active
            document.querySelectorAll('.map-pin').forEach(pin => pin.classList.remove('active'));

            // 將被選中的圖釘加上 active 並移到 SVG 最頂層，觸發彈出放大動畫！
            const activePin = document.getElementById(`pin-${{landmarkId}}`);
            if (activePin) {{
                activePin.classList.add('active');
                if (activePin.parentNode) {{
                    activePin.parentNode.appendChild(activePin);
                }}
            }}

            // 更新右側拍立得卡片資訊
            const dayEl = document.getElementById('card-day');
            if (dayEl) dayEl.textContent = lm.day;
            const titleEl = document.getElementById('card-title');
            if (titleEl) titleEl.textContent = lm.name;
            const catEl = document.getElementById('card-category');
            if (catEl) catEl.textContent = lm.categoryName;
            const iconEl = document.getElementById('card-icon');
            if (iconEl) iconEl.textContent = lm.icon;
            const descEl = document.getElementById('card-desc');
            if (descEl) descEl.textContent = lm.desc;
            const tipsEl = document.getElementById('card-tips');
            if (tipsEl) tipsEl.innerHTML = `<strong>貼心叮嚀：</strong>${{lm.tips}}`;
            const mapLink = document.getElementById('card-map-link');
            if (mapLink) mapLink.href = `https://www.google.com/maps/search/?api=1&query=${{encodeURIComponent(lm.name.split(' ')[0])}}`;

            // 同步更新下方快速定位清單高亮
            renderMapQuickButtons();
        }}

        function toggleMapRoutes() {{
            showRoutes = !showRoutes;
            const routesGroup = document.getElementById('map-routes-group');
            const btn = document.getElementById('map-btn-routes');
            if (routesGroup) routesGroup.style.display = showRoutes ? 'block' : 'none';
            if (btn) {{
                btn.textContent = showRoutes ? '🚗 7天行車動線：開啟中' : '🚗 7天行車動線：隱藏中';
                btn.className = showRoutes ? 'px-3 py-1.5 rounded-full bg-amber-100 text-amber-800 hover:bg-amber-200 transition' : 'px-3 py-1.5 rounded-full bg-stone-100 text-stone-500 hover:bg-stone-200 transition';
            }}
        }}

        let currentQuickPickTab = 'hotels';

        function switchQuickPickTab(tab) {{
            currentQuickPickTab = tab;
            ['hotels', 'sights'].forEach(t => {{
                const btn = document.getElementById(`qtab-${{t}}`);
                if (btn) {{
                    if (t === tab) {{
                        if (t === 'hotels') btn.className = 'px-3 py-1 rounded-xl text-xs font-black bg-purple-100 text-purple-700 transition';
                        else if (t === 'sights') btn.className = 'px-3 py-1 rounded-xl text-xs font-black bg-emerald-100 text-emerald-800 transition';
                    }} else {{
                        btn.className = 'px-3 py-1 rounded-xl text-xs font-black bg-stone-100 text-stone-600 hover:bg-stone-200 transition';
                    }}
                }}
            }});
            renderMapQuickButtons();
        }}

        function renderMapQuickButtons() {{
            const container = document.getElementById('map-quick-buttons');
            if (!container) return;
            container.innerHTML = '';

            let list = [];
            if (currentQuickPickTab === 'hotels') {{
                list = [
                    {{ id: 'hotel_viainn', label: 'Day 1 Via Inn 辛島町' }},
                    {{ id: 'hotel_kurokawa', label: 'Day 2 黑川山彥旅館' }},
                    {{ id: 'hotel_seagaia', label: 'Day 3 宮崎 Seagaia' }},
                    {{ id: 'hotel_perch', label: 'Day 4-5 鹿兒島 Perch' }},
                    {{ id: 'hotel_amanek', label: 'Day 6 熊本 AMANEK' }}
                ];
            }} else {{
                list = [
                    {{ id: 'kmj_airport', label: '🛫 熊本機場' }},
                    {{ id: 'aso_crater', label: '🌋 阿蘇火山口' }},
                    {{ id: 'kamishikimi', label: '🌲 上色見神社' }},
                    {{ id: 'takachiho_gorge', label: '🚣 高千穗峽谷' }},
                    {{ id: 'aoshima', label: '🌊 青島洗衣板' }},
                    {{ id: 'sun_messe', label: '🗿 日南摩艾像' }},
                    {{ id: 'sakurajima', label: '🌋 櫻島火山渡輪' }},
                    {{ id: 'kirishima_jingu', label: '⛩️ 國寶霧島神宮' }},
                    {{ id: 'hitoyoshi_unagi', label: '🍱 人吉鰻魚飯' }},
                    {{ id: 'kumamoto_castle', label: '🏯 熊本城天守閣' }}
                ];
            }}

            list.forEach(p => {{
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = `p-2 rounded-xl text-left transition truncate border text-xs font-bold ${{
                    selectedPinId === p.id 
                        ? 'bg-red-50 text-red-700 border-red-300 shadow-sm' 
                        : 'bg-stone-50 hover:bg-stone-100 text-stone-700 border-stone-200'
                }}`;
                btn.textContent = p.label;
                btn.onclick = () => {{
                    selectLandmark(p.id);
                }};
                container.appendChild(btn);
            }});
        }}

        // ======================= 費用明細 ＆ 即時記帳與 Google Sheet 串接 =======================
        const DEFAULT_MEMBER_NAMES = {{
            achun: '首席導遊 阿純',
            alu: '總務大臣 阿嚕',
            ayee: '美食評鑑官 阿姨',
            yijhang: '榮譽總指揮 姨丈'
        }};

        const MEMBER_CONFIG = {{
            achun: {{ key: 'achun', icon: '🌸', color: 'text-red-600' }},
            alu: {{ key: 'alu', icon: '🐻', color: 'text-sky-600' }},
            ayee: {{ key: 'ayee', icon: '🌼', color: 'text-amber-600' }},
            yijhang: {{ key: 'yijhang', icon: '🎩', color: 'text-purple-600' }}
        }};

        function getMemberNames() {{
            try {{
                const stored = localStorage.getItem('kyushu_member_names_v2');
                if (stored) {{
                    const parsed = JSON.parse(stored);
                    return {{
                        achun: (parsed.achun || '').trim() || DEFAULT_MEMBER_NAMES.achun,
                        alu: (parsed.alu || '').trim() || DEFAULT_MEMBER_NAMES.alu,
                        ayee: (parsed.ayee || '').trim() || DEFAULT_MEMBER_NAMES.ayee,
                        yijhang: (parsed.yijhang || '').trim() || DEFAULT_MEMBER_NAMES.yijhang
                    }};
                }}
            }} catch(e) {{}}
            return Object.assign({{}}, DEFAULT_MEMBER_NAMES);
        }}

        function resolveMemberKey(payer) {{
            if (!payer) return 'achun';
            if (payer === 'achun' || payer === '阿純' || payer.includes('阿純') || payer.includes('導遊')) return 'achun';
            if (payer === 'alu' || payer === '阿嚕' || payer.includes('阿嚕') || payer.includes('總務')) return 'alu';
            if (payer === 'ayee' || payer === '阿姨' || payer.includes('阿姨') || payer.includes('美食')) return 'ayee';
            if (payer === 'yijhang' || payer === '姨丈' || payer.includes('姨丈') || payer.includes('指揮')) return 'yijhang';
            const names = getMemberNames();
            if (payer === names.achun) return 'achun';
            if (payer === names.alu) return 'alu';
            if (payer === names.ayee) return 'ayee';
            if (payer === names.yijhang) return 'yijhang';
            return 'achun';
        }}

        function updatePayerAndSplitOptions() {{
            const names = getMemberNames();
            const payerSelect = document.getElementById('exp-payer');
            if (payerSelect) {{
                const curVal = payerSelect.value;
                payerSelect.innerHTML = `
                    <option value="achun">🌸 ${{escapeHtml(names.achun)}} 先墊付</option>
                    <option value="alu">🐻 ${{escapeHtml(names.alu)}} 先墊付</option>
                    <option value="ayee">🌼 ${{escapeHtml(names.ayee)}} 先墊付</option>
                    <option value="yijhang">🎩 ${{escapeHtml(names.yijhang)}} 先墊付</option>
                `;
                if (curVal) payerSelect.value = curVal;
            }}

            const lblAchun = document.getElementById('label-split-achun');
            const lblAlu = document.getElementById('label-split-alu');
            const lblAyee = document.getElementById('label-split-ayee');
            const lblYijhang = document.getElementById('label-split-yijhang');
            const subTitle = document.getElementById('members-subtitle-names');

            if (lblAchun) lblAchun.textContent = names.achun;
            if (lblAlu) lblAlu.textContent = names.alu;
            if (lblAyee) lblAyee.textContent = names.ayee;
            if (lblYijhang) lblYijhang.textContent = names.yijhang;
            if (subTitle) subTitle.textContent = `（${{names.achun}}、${{names.alu}}、${{names.ayee}}、${{names.yijhang}}）`;
        }}

        function openMemberNamesModal() {{
            const names = getMemberNames();
            const inAchun = document.getElementById('member-input-achun');
            const inAlu = document.getElementById('member-input-alu');
            const inAyee = document.getElementById('member-input-ayee');
            const inYijhang = document.getElementById('member-input-yijhang');

            if (inAchun) inAchun.value = names.achun;
            if (inAlu) inAlu.value = names.alu;
            if (inAyee) inAyee.value = names.ayee;
            if (inYijhang) inYijhang.value = names.yijhang;

            const modal = document.getElementById('member-names-modal');
            if (modal) modal.classList.remove('hidden');
        }}

        function closeMemberNamesModal() {{
            const modal = document.getElementById('member-names-modal');
            if (modal) modal.classList.add('hidden');
        }}

        function saveCustomMemberNames() {{
            const inAchun = document.getElementById('member-input-achun');
            const inAlu = document.getElementById('member-input-alu');
            const inAyee = document.getElementById('member-input-ayee');
            const inYijhang = document.getElementById('member-input-yijhang');

            const newNames = {{
                achun: (inAchun ? inAchun.value.trim() : '') || DEFAULT_MEMBER_NAMES.achun,
                alu: (inAlu ? inAlu.value.trim() : '') || DEFAULT_MEMBER_NAMES.alu,
                ayee: (inAyee ? inAyee.value.trim() : '') || DEFAULT_MEMBER_NAMES.ayee,
                yijhang: (inYijhang ? inYijhang.value.trim() : '') || DEFAULT_MEMBER_NAMES.yijhang
            }};

            localStorage.setItem('kyushu_member_names_v2', JSON.stringify(newNames));
            closeMemberNamesModal();
            updatePayerAndSplitOptions();
            renderCosts();
            showToast('✨ 4 位成員分帳稱號已成功更新並同步！');
        }}

        function resetMemberNamesToSchemeA() {{
            localStorage.removeItem('kyushu_member_names_v2');
            const inAchun = document.getElementById('member-input-achun');
            const inAlu = document.getElementById('member-input-alu');
            const inAyee = document.getElementById('member-input-ayee');
            const inYijhang = document.getElementById('member-input-yijhang');

            if (inAchun) inAchun.value = DEFAULT_MEMBER_NAMES.achun;
            if (inAlu) inAlu.value = DEFAULT_MEMBER_NAMES.alu;
            if (inAyee) inAyee.value = DEFAULT_MEMBER_NAMES.ayee;
            if (inYijhang) inYijhang.value = DEFAULT_MEMBER_NAMES.yijhang;

            updatePayerAndSplitOptions();
            renderCosts();
            showToast('已恢復方案 A 探險隊專屬職責預設名稱！');
        }}

        function getCustomExpenses() {{
            try {{
                return JSON.parse(localStorage.getItem('kyushu_custom_expenses') || '[]');
            }} catch (e) {{
                return [];
            }}
        }}

        function setCustomExpenses(list) {{
            localStorage.setItem('kyushu_custom_expenses', JSON.stringify(list));
        }}

        function syncExpenseCurrencyCalc() {{
            const amountInput = document.getElementById('exp-amount');
            const currSelect = document.getElementById('exp-currency');
            const preview = document.getElementById('exp-converted-preview');
            if (!amountInput || !preview) return;

            const val = parseFloat(amountInput.value) || 0;
            const curr = currSelect ? currSelect.value : 'JPY';
            const rate = TRIP_DATA.rate_to_twd || 0.2078;

            if (curr === 'JPY') {{
                const twd = Math.round(val * rate);
                preview.textContent = `NT$ ${{twd.toLocaleString()}} (依匯率 ${{rate}})`;
            }} else {{
                const jpy = Math.round(val / rate);
                preview.textContent = `約 ¥ ${{jpy.toLocaleString()}} 日圓`;
            }}
        }}

        function initCosts() {{
            const webhookUrl = localStorage.getItem('kyushu_google_sheet_webhook') || '';
            const webhookInput = document.getElementById('webhook-url-input');
            if (webhookInput) webhookInput.value = webhookUrl;

            const indicator = document.getElementById('sync-status-indicator');
            const drawer = document.getElementById('webhook-settings-drawer');
            if (indicator) {{
                if (webhookUrl) {{
                    indicator.innerHTML = '<span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span> <span class="text-emerald-800 font-black">🟢 Google 試算表雲端直寫：已連線（記帳自動秒寫入）</span>';
                    if (drawer) drawer.classList.add('hidden');
                }} else {{
                    indicator.innerHTML = '<span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> <span class="text-amber-800 font-bold">🟡 直寫通道未綁定（綁定後直接自動寫入試算表，免複製貼上）</span>';
                }}
            }}

            updatePayerAndSplitOptions();
            renderCosts();
        }}

        function renderCosts() {{
            const customList = getCustomExpenses();
            const names = getMemberNames();
            const baseList = (TRIP_DATA && Array.isArray(TRIP_DATA.expenses_list)) ? TRIP_DATA.expenses_list : [];

            let baseTotalSpent = 0;
            let customSpentTotal = 0;

            const membersCalc = {{
                achun: {{ paid: 0, should: 0, paidItems: [] }},
                alu: {{ paid: 0, should: 0, paidItems: [] }},
                ayee: {{ paid: 0, should: 0, paidItems: [] }},
                yijhang: {{ paid: 0, should: 0, paidItems: [] }}
            }};

            // 1. 動態計算 Google 試算表同步下來的公費支出
            baseList.forEach(item => {{
                const twd = Number(item.amount_twd || 0);
                baseTotalSpent += twd;

                const payerKey = resolveMemberKey(item.payer);
                if (membersCalc[payerKey]) {{
                    membersCalc[payerKey].paid += twd;
                    membersCalc[payerKey].paidItems.push(item.item);
                }}

                const splitMembers = [];
                if (item.split) {{
                    if (item.split.achun) splitMembers.push('achun');
                    if (item.split.alu) splitMembers.push('alu');
                    if (item.split.ayee) splitMembers.push('ayee');
                    if (item.split.yijhang) splitMembers.push('yijhang');
                }}

                if (splitMembers.length > 0) {{
                    const share = twd / splitMembers.length;
                    splitMembers.forEach(k => {{
                        if (membersCalc[k]) membersCalc[k].should += share;
                    }});
                }}
            }});

            // 2. 累加本地即時記帳的小項目 (尚未回寫或額外暫存者)
            customList.forEach(item => {{
                const twd = Number(item.amount_twd || 0);
                customSpentTotal += twd;

                const payerKey = resolveMemberKey(item.payer);
                if (membersCalc[payerKey]) {{
                    membersCalc[payerKey].paid += twd;
                    membersCalc[payerKey].paidItems.push(item.item);
                }}

                const splitMembers = [];
                if (item.achun) splitMembers.push('achun');
                if (item.alu) splitMembers.push('alu');
                if (item.aunt) splitMembers.push('ayee');
                if (item.uncle) splitMembers.push('yijhang');

                if (splitMembers.length > 0) {{
                    const share = twd / splitMembers.length;
                    splitMembers.forEach(k => {{
                        if (membersCalc[k]) membersCalc[k].should += share;
                    }});
                }}
            }});

            const currentTotalSpent = baseTotalSpent + customSpentTotal;
            const currentPerPerson = Math.round(currentTotalSpent / 4);

            const totalEl = document.getElementById('cost-total-amount');
            if (totalEl) totalEl.textContent = `NT$ ${{Math.round(currentTotalSpent).toLocaleString()}}`;
            const perEl = document.getElementById('cost-per-person');
            if (perEl) perEl.textContent = `平均每人應付 NT$ ${{currentPerPerson.toLocaleString()}}`;

            // 渲染 4 位成員的結算看板卡片
            const cardsContainer = document.getElementById('members-settlement-cards');
            if (cardsContainer) {{
                cardsContainer.innerHTML = '';
                ['achun', 'alu', 'ayee', 'yijhang'].forEach(k => {{
                    const m = membersCalc[k];
                    const cfg = MEMBER_CONFIG[k];
                    const displayName = names[k];
                    const diff = Math.round(m.paid - m.should);
                    const isCredit = diff > 0;
                    const isBalanced = diff === 0;

                    let noteText = '';
                    if (m.paidItems.length > 0) {{
                        noteText = `代墊：${{m.paidItems.join('、')}}`;
                    }} else {{
                        noteText = `分攤家族機票、自駕租車與特色旅宿公費`;
                    }}

                    const div = document.createElement('div');
                    div.className = 'polaroid-card space-y-3 bg-gradient-to-b from-white to-stone-50/50 relative group';
                    div.innerHTML = `
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2 min-w-0">
                                <span class="text-2xl shrink-0">${{cfg.icon}}</span>
                                <span class="text-base font-black text-stone-800 truncate" title="${{escapeHtml(displayName)}}">${{escapeHtml(displayName)}}</span>
                            </div>
                            <span class="cute-pill shrink-0 ${{isCredit ? 'bg-emerald-100 text-emerald-700' : (isBalanced ? 'bg-stone-100 text-stone-600' : 'bg-red-100 text-red-700')}}">
                                ${{isCredit ? '🟢 應收款' : (isBalanced ? '⚪ 平帳' : '🔴 應補款')}}
                            </span>
                        </div>
                        <div class="space-y-1 text-xs">
                            <div class="flex justify-between text-stone-500">
                                <span>累計已墊：</span>
                                <span class="font-bold text-stone-800 font-mono">NT$ ${{Math.round(m.paid).toLocaleString()}}</span>
                            </div>
                            <div class="flex justify-between text-stone-500">
                                <span>個人應付：</span>
                                <span class="font-mono text-stone-600">NT$ ${{Math.round(m.should).toLocaleString()}}</span>
                            </div>
                            <div class="flex justify-between pt-2 border-t border-stone-200 text-sm">
                                <span class="${{isCredit ? 'text-emerald-700' : (isBalanced ? 'text-stone-600' : 'text-red-600')}} font-black">
                                    ${{isCredit ? '結算應收：' : (isBalanced ? '收支平衡：' : '結算應付：')}}
                                </span>
                                <span class="${{isCredit ? 'text-emerald-700' : (isBalanced ? 'text-stone-600' : 'text-red-600')}} font-mono font-black">
                                    ${{isCredit ? '+ NT$ ' + diff.toLocaleString() : (isBalanced ? 'NT$ 0' : '- NT$ ' + Math.abs(diff).toLocaleString())}}
                                </span>
                            </div>
                        </div>
                        <div class="text-[11px] text-stone-600 bg-white p-2.5 rounded-xl border border-stone-200 leading-relaxed truncate" title="${{escapeHtml(noteText)}}">
                            💡 ${{escapeHtml(noteText)}}
                        </div>
                    `;
                    cardsContainer.appendChild(div);
                }});
            }}

            // 渲染平帳指引
            const guideBox = document.getElementById('settlement-guide-box');
            if (guideBox) {{
                const debtors = [];
                const creditors = [];
                ['achun', 'alu', 'ayee', 'yijhang'].forEach(k => {{
                    const diff = Math.round(membersCalc[k].paid - membersCalc[k].should);
                    if (diff < -5) debtors.push({{ key: k, name: names[k], amount: Math.abs(diff) }});
                    else if (diff > 5) creditors.push({{ key: k, name: names[k], amount: diff }});
                }});

                let steps = [];
                let dIdx = 0;
                let cIdx = 0;
                while (dIdx < debtors.length && cIdx < creditors.length) {{
                    const d = debtors[dIdx];
                    const c = creditors[cIdx];
                    const payAmount = Math.min(d.amount, c.amount);

                    steps.push(`<strong>${{d.name}}</strong> 匯款補給 <strong>${{c.name}}</strong> <span class="text-amber-800 font-bold font-mono">NT$ ${{Math.round(payAmount).toLocaleString()}}</span>`);

                    d.amount -= payAmount;
                    c.amount -= payAmount;
                    if (d.amount <= 5) dIdx++;
                    if (c.amount <= 5) cIdx++;
                }}

                guideBox.innerHTML = `
                    <span class="text-xl shrink-0">💌</span>
                    <div class="space-y-1">
                        <strong class="text-sm font-bold text-amber-800">一鍵搞定即時平帳匯款指引：</strong><br>
                        ${{steps.length > 0 ? steps.map((s, idx) => `${{idx + 1}}. ${{s}}。<br>`).join('') : '目前所有成員帳目完全平整，無需匯款！✨'}}<br>
                        <span class="text-stone-500 text-[11px]">✨ 照著匯款，全家族公費帳目一秒歸零收支平衡！</span>
                    </div>
                `;
            }}

            // 渲染 Google 試算表已登記公費項目表格
            const tableBody = document.getElementById('base-expenses-table-body');
            const countBadge = document.getElementById('base-expenses-count-badge');
            if (countBadge) countBadge.textContent = `${{baseList.length}} 筆`;

            if (tableBody) {{
                tableBody.innerHTML = '';
                baseList.forEach(item => {{
                    const tr = document.createElement('tr');
                    tr.className = 'hover:bg-amber-50/40 transition';

                    const splitList = [];
                    if (item.split?.achun) splitList.push('阿純');
                    if (item.split?.alu) splitList.push('阿嚕');
                    if (item.split?.ayee) splitList.push('阿姨');
                    if (item.split?.yijhang) splitList.push('姨丈');
                    const splitStr = splitList.length === 4 ? '<span class="cute-pill bg-sky-50 text-sky-700 text-[10px]">4人全員</span>' : splitList.join('、');

                    tr.innerHTML = `
                        <td class="px-3 py-2.5 font-medium text-stone-500 whitespace-nowrap">${{escapeHtml(item.day || '-')}}</td>
                        <td class="px-3 py-2.5 font-bold text-stone-800">${{escapeHtml(item.item || '-')}}</td>
                        <td class="px-3 py-2.5"><span class="cute-pill bg-stone-100 text-stone-600 text-[10px]">${{escapeHtml(item.category || '-')}}</span></td>
                        <td class="px-3 py-2.5 font-bold text-amber-800">${{escapeHtml(item.payer || '-')}}</td>
                        <td class="px-3 py-2.5 text-right font-mono text-stone-500 whitespace-nowrap">${{item.currency}} ${{Number(item.amount_orig || item.amount_twd).toLocaleString()}}</td>
                        <td class="px-3 py-2.5 text-right font-mono font-bold text-emerald-700 whitespace-nowrap">NT$ ${{Math.round(Number(item.amount_twd || 0)).toLocaleString()}}</td>
                        <td class="px-3 py-2.5 text-center whitespace-nowrap">${{splitStr}}</td>
                    `;
                    tableBody.appendChild(tr);
                }});
            }}

            const countEl = document.getElementById('custom-expense-count');
            if (countEl) countEl.textContent = customList.length;

            const listContainer = document.getElementById('custom-expenses-list');
            if (listContainer) {{
                if (customList.length === 0) {{
                    listContainer.innerHTML = '<div class="text-xs text-stone-400 italic py-2 text-center">尚無新增的花費記錄，輸入上方表單即可隨時記帳～</div>';
                }} else {{
                    listContainer.innerHTML = '';
                    customList.slice().reverse().forEach(item => {{
                        const row = document.createElement('div');
                        row.className = 'bg-white p-3 rounded-2xl border border-stone-200 flex flex-wrap items-center justify-between text-xs gap-2 shadow-sm';
                        
                        const splitText = [
                            item.achun ? names.achun.slice(0, 4) : '',
                            item.alu ? names.alu.slice(0, 4) : '',
                            item.aunt ? names.ayee.slice(0, 4) : '',
                            item.uncle ? names.yijhang.slice(0, 4) : ''
                        ].filter(Boolean).join('/');

                        const payerKey = resolveMemberKey(item.payer);
                        const payerDisplayName = names[payerKey] || item.payer;

                        row.innerHTML = `
                            <div class="flex items-center gap-2">
                                <span class="cute-pill bg-amber-100 text-amber-700">${{item.date.split('-').slice(1).join('/')}}</span>
                                <span class="font-bold text-stone-800">${{escapeHtml(item.item)}}</span>
                                <span class="text-stone-400 text-[11px]">(${{escapeHtml(item.category)}})</span>
                                ${{item.note ? `<span class="text-stone-400 text-[11px] italic">"${{escapeHtml(item.note)}}"</span>` : ''}}
                            </div>
                            <div class="flex items-center gap-3">
                                <div class="text-right">
                                    <span class="font-mono font-bold text-stone-800">NT$ ${{Number(item.amount_twd).toLocaleString()}}</span>
                                    <div class="text-[10px] text-stone-400">${{escapeHtml(payerDisplayName)}} 墊 ｜ 分攤: ${{splitText}}</div>
                                </div>
                                <button type="button" onclick="copySingleExpenseTsv('${{item.id}}')" class="p-1 text-stone-400 hover:text-stone-600" title="複製此列">📋</button>
                                <button type="button" onclick="deleteCustomExpense('${{item.id}}')" class="p-1 text-red-400 hover:text-red-600" title="刪除">🗑️</button>
                            </div>
                        `;
                        listContainer.appendChild(row);
                    }});
                }}
            }}
        }}

        function handleNewExpenseSubmit(e) {{
            e.preventDefault();
            const date = document.getElementById('exp-date').value;
            const item = document.getElementById('exp-item').value.trim();
            const category = document.getElementById('exp-category').value;
            const payer = document.getElementById('exp-payer').value;
            const amountOriginal = parseFloat(document.getElementById('exp-amount').value) || 0;
            const currency = document.getElementById('exp-currency').value;
            const note = document.getElementById('exp-note').value.trim();

            if (!item || amountOriginal <= 0) {{
                showToast('請填寫有效的消費項目與金額！');
                return;
            }}

            const achun = document.getElementById('split-achun').checked;
            const alu = document.getElementById('split-alu').checked;
            const aunt = document.getElementById('split-aunt').checked;
            const uncle = document.getElementById('split-uncle').checked;

            let headcount = (achun ? 1 : 0) + (alu ? 1 : 0) + (aunt ? 1 : 0) + (uncle ? 1 : 0);
            if (headcount === 0) headcount = 4;

            const rate = TRIP_DATA.rate_to_twd || 0.2078;
            const amountTwd = currency === 'JPY' ? Math.round(amountOriginal * rate) : Math.round(amountOriginal);
            const perPersonTwd = Math.round(amountTwd / headcount);

            const newRecord = {{
                id: 'exp_' + Date.now(),
                date,
                item,
                category,
                payer,
                currency,
                amount_original: amountOriginal,
                amount_twd: amountTwd,
                achun,
                alu,
                aunt,
                uncle,
                headcount,
                per_person_twd: perPersonTwd,
                note,
                synced: false
            }};

            const list = getCustomExpenses();
            list.push(newRecord);
            setCustomExpenses(list);

            document.getElementById('exp-item').value = '';
            document.getElementById('exp-amount').value = '';
            document.getElementById('exp-note').value = '';
            document.getElementById('exp-converted-preview').textContent = 'NT$ 0';

            renderCosts();

            const webhookUrl = localStorage.getItem('kyushu_google_sheet_webhook');
            if (webhookUrl) {{
                showToast(`已記帳 NT$ ${{amountTwd.toLocaleString()}}！正在傳送至 Google 試算表...`);
                fetch(webhookUrl, {{
                    method: 'POST',
                    mode: 'no-cors',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(newRecord)
                }}).then(() => {{
                    newRecord.synced = true;
                    setCustomExpenses(list);
                    showToast(`✨ 記帳成功！已同步新增至 Google 試算表！`);
                }}).catch(err => {{
                    console.error('Webhook sync failed:', err);
                    showToast(`本機記帳成功！(試算表連線逾時，可隨時手動貼上)`);
                }});
            }} else {{
                showToast(`已記錄至本手帳！若需自動寫入 Google 試算表，請在上方綁定 Webhook 網址。`);
            }}
        }}

        function deleteCustomExpense(id) {{
            let list = getCustomExpenses();
            list = list.filter(item => item.id !== id);
            setCustomExpenses(list);
            renderCosts();
            showToast('已刪除此筆記錄並重新結算！');
        }}

        function copySingleExpenseTsv(id) {{
            const item = getCustomExpenses().find(x => x.id === id);
            if (!item) return;
            const tsv = `${{item.date}}	${{item.item}}	${{item.category}}	${{item.payer}}	${{item.currency}}	${{item.amount_original}}	${{item.amount_twd}}	${{item.achun ? 'TRUE' : 'FALSE'}}	${{item.alu ? 'TRUE' : 'FALSE'}}	${{item.aunt ? 'TRUE' : 'FALSE'}}	${{item.uncle ? 'TRUE' : 'FALSE'}}	${{item.headcount}}	${{item.per_person_twd}}	${{item.note || ''}}`;
            copyToClipboard(tsv, '已複製該筆記帳（直接在 Google 試算表按 Ctrl+V 貼上）！📋');
        }}

        function copyAllExpensesTsv() {{
            const list = getCustomExpenses();
            if (list.length === 0) {{
                showToast('目前尚無新增記錄可供複製！');
                return;
            }}
            const rows = list.map(item => {{
                return `${{item.date}}	${{item.item}}	${{item.category}}	${{item.payer}}	${{item.currency}}	${{item.amount_original}}	${{item.amount_twd}}	${{item.achun ? 'TRUE' : 'FALSE'}}	${{item.alu ? 'TRUE' : 'FALSE'}}	${{item.aunt ? 'TRUE' : 'FALSE'}}	${{item.uncle ? 'TRUE' : 'FALSE'}}	${{item.headcount}}	${{item.per_person_twd}}	${{item.note || ''}}`;
            }});
            copyToClipboard(rows.join(String.fromCharCode(10)), `已複製全部 ${{list.length}} 筆記錄！請在 Google 試算表【費用】工作表按 Ctrl+V 貼上！📋`);
        }}

        function toggleWebhookSettings() {{
            const drawer = document.getElementById('webhook-settings-drawer');
            if (drawer) drawer.classList.toggle('hidden');
        }}

        function saveGoogleWebhookUrl() {{
            const input = document.getElementById('webhook-url-input');
            if (!input) return;
            const url = input.value.trim();
            localStorage.setItem('kyushu_google_sheet_webhook', url);
            initCosts();
                renderRestaurants();
            showToast(url ? '已成功儲存 Google 試算表 Webhook 網址！🎉' : '已清除 Webhook 網址，恢復為純本機記帳。');
        }}

                function copyAppsScriptCode() {{
            const code = `/**
 * 2026 南九州旅行手帳 - Google 試算表自動記帳 Webhook (全自動直接寫入版)
 * 試算表：https://docs.google.com/spreadsheets/d/1P4niaKfXpHnrlVkiexFmxa2Q0U7kwOvj6yUINn--WNo
 * 
 * 【功能說明】：
 * - 支援儀表板網頁或手機「一鍵儲存 ➔ 直接寫入試算表」，全程 0 手動複製貼上！
 * - 自動鎖定【費用】工作表中的空白列 (從第 24 列開始自動填入)。
 * - 自動寫入日期、項目、類別、代墊人、雙幣金額與 4 人勾選分攤。
 * - 自動連動試算表公式與上方結算看板！
 */

function doPost(e) {{
  try {{
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName("費用") || ss.getActiveSheet();
    
    var data = JSON.parse(e.postData.contents);
    
    var date = data.date || Utilities.formatDate(new Date(), "GMT+9", "yyyy-MM-dd");
    var item = data.item || "";
    var category = data.category || "其他雜支";
    var payer = data.payer || "阿純";
    var currency = data.currency || "JPY";
    var amountOriginal = Number(data.amount_original || 0);
    
    // 分攤成員布林值
    var achun = (data.achun !== undefined) ? !!data.achun : true;
    var alu = (data.alu !== undefined) ? !!data.alu : true;
    var aunt = (data.aunt !== undefined) ? !!data.aunt : true;
    var uncle = (data.uncle !== undefined) ? !!data.uncle : true;
    var note = data.note || "";

    // 尋找第 18 列以後第一個「消費項目 (Column C, 第3欄)」為空的列
    var targetRow = -1;
    for (var r = 18; r <= 41; r++) {{
      var val = sheet.getRange(r, 3).getValue();
      if (!val || val.toString().trim() === "") {{
        targetRow = r;
        break;
      }}
    }}
    
    // 若 18~41 列已滿，則在合計列 (原第 42 列) 上方插入新列
    if (targetRow === -1) {{
      targetRow = 42;
      sheet.insertRowBefore(42);
    }}

    // 寫入欄位至對應欄位 (Column B 至 O)
    // B: 日期, C: 項目, D: 類別, E: 付款人, F: 幣別, G: 原幣金額
    sheet.getRange(targetRow, 2).setValue(date);
    sheet.getRange(targetRow, 3).setValue(item);
    sheet.getRange(targetRow, 4).setValue(category);
    sheet.getRange(targetRow, 5).setValue(payer);
    sheet.getRange(targetRow, 6).setValue(currency);
    sheet.getRange(targetRow, 7).setValue(amountOriginal);
    
    // H: 折合台幣公式
    sheet.getRange(targetRow, 8).setFormula('=IF(F' + targetRow + '="JPY", ROUND(G' + targetRow + '*$K$2, 0), IF(F' + targetRow + '="TWD", G' + targetRow + ', 0))');
    
    // I, J, K, L: 4人分攤 (TRUE / FALSE)
    sheet.getRange(targetRow, 9).setValue(achun);
    sheet.getRange(targetRow, 10).setValue(alu);
    sheet.getRange(targetRow, 11).setValue(aunt);
    sheet.getRange(targetRow, 12).setValue(uncle);
    
    // M: 分攤人數公式, N: 每人應付公式, O: 備註
    sheet.getRange(targetRow, 13).setFormula('=COUNTIF(I' + targetRow + ':L' + targetRow + ', TRUE)');
    sheet.getRange(targetRow, 14).setFormula('=IF(M' + targetRow + '>0, H' + targetRow + '/M' + targetRow + ', 0)');
    sheet.getRange(targetRow, 15).setValue(note);

    return ContentService.createTextOutput(JSON.stringify({{
      status: "success",
      message: "成功直接寫入 Google 試算表第 " + targetRow + " 列！",
      targetRow: targetRow,
      item: item,
      payer: payer
    }})).setMimeType(ContentService.MimeType.JSON);

  }} catch (err) {{
    return ContentService.createTextOutput(JSON.stringify({{
      status: "error",
      message: err.toString()
    }})).setMimeType(ContentService.MimeType.JSON);
  }}
}}

function doGet(e) {{
  return ContentService.createTextOutput("2026 南九州旅行記帳 Webhook 直寫連線正常！❄️").setMimeType(ContentService.MimeType.TEXT);
}}
`;
            copyToClipboard(code, '已複製全自動直寫 Google Apps Script 程式碼！請在試算表的【擴充功能 ➔ Apps Script】貼上並部署！📋');
        }}

        // ======================= 行李檢查表 (徹底修復重來錯誤) =======================
        function initChecklist() {{
            const savedState = JSON.parse(localStorage.getItem('kyushu_xmas_checklist') || '{{}}');

            ['documents', 'carry_on', 'checked_bag'].forEach(groupKey => {{
                const containerId = groupKey === 'documents' ? 'list-documents' : (groupKey === 'carry_on' ? 'list-carry-on' : 'list-checked-bag');
                const container = document.getElementById(containerId);
                if (!container) return;
                container.innerHTML = '';

                TRIP_DATA.packing_checklist[groupKey].forEach(item => {{
                    const isChecked = savedState.hasOwnProperty(item.id) ? !!savedState[item.id] : false;
                    const div = document.createElement('div');
                    div.className = `p-2.5 rounded-2xl border-2 transition cursor-pointer flex items-center justify-between text-xs font-bold ${{isChecked ? 'bg-stone-50 border-stone-200 text-stone-400 line-through' : 'bg-white border-stone-200 text-stone-800 hover:border-red-300'}}`;
                    div.id = `item-row-${{item.id}}`;
                    div.onclick = () => toggleChecklistItem(item.id, groupKey);

                    div.innerHTML = `
                        <div class="flex items-center gap-2 min-w-0 flex-1 pr-2">
                            <span class="${{isChecked ? 'text-emerald-600' : 'text-stone-300'}} text-sm shrink-0">${{isChecked ? '❄️' : '⚪'}}</span>
                            <span class="truncate sm:overflow-visible sm:whitespace-normal font-bold">${{item.item}}</span>
                        </div>
                        ${{item.critical ? '<span class="cute-pill bg-red-100 text-red-700 shrink-0 whitespace-nowrap text-[10px] font-black">必帶</span>' : ''}}
                    `;
                    container.appendChild(div);
                }});
            }});

            updateChecklistStats();
        }}

        function toggleChecklistItem(itemId, groupKey) {{
            const savedState = JSON.parse(localStorage.getItem('kyushu_xmas_checklist') || '{{}}');
            const currentState = savedState.hasOwnProperty(itemId) ? savedState[itemId] : false;
            const newState = !currentState;
            savedState[itemId] = newState;
            localStorage.setItem('kyushu_xmas_checklist', JSON.stringify(savedState));

            initChecklist();
            if (newState) showToast('已完成一項！❄️✨');
        }}

        function updateChecklistStats() {{
            const savedState = JSON.parse(localStorage.getItem('kyushu_xmas_checklist') || '{{}}');
            let totalAll = 0;
            let totalCheckedAll = 0;
            ['documents', 'carry_on', 'checked_bag'].forEach(groupKey => {{
                let gTotal = 0;
                let gChecked = 0;
                TRIP_DATA.packing_checklist[groupKey].forEach(item => {{
                    gTotal++;
                    totalAll++;
                    const isChecked = savedState.hasOwnProperty(item.id) ? !!savedState[item.id] : false;
                    if (isChecked) {{
                        gChecked++;
                        totalCheckedAll++;
                    }}
                }});
                const counterId = groupKey === 'documents' ? 'doc-count' : (groupKey === 'carry_on' ? 'car-count' : 'bag-count');
                const el = document.getElementById(counterId);
                if (el) el.textContent = `${{gChecked}}/${{gTotal}}`;
            }});

            // 動態更新全部打包按鈕顏色與文字狀態，絕不卡死在深綠色！
            const btnAll = document.getElementById('btn-all-packed');
            const btnReset = document.getElementById('btn-reset-packing');
            if (btnAll) {{
                if (totalCheckedAll === totalAll && totalAll > 0) {{
                    btnAll.className = 'px-3.5 py-1.5 rounded-full bg-emerald-600 text-white hover:bg-emerald-700 text-xs font-black transition shadow-sm ring-2 ring-emerald-300';
                    btnAll.innerHTML = '全部打包好啦！🎉';
                }} else if (totalCheckedAll === 0) {{
                    btnAll.className = 'px-3.5 py-1.5 rounded-full bg-stone-100 text-stone-500 border border-stone-200 hover:bg-emerald-50 hover:text-emerald-700 text-xs font-bold transition';
                    btnAll.innerHTML = '一鍵全部打包 🎉';
                }} else {{
                    btnAll.className = 'px-3.5 py-1.5 rounded-full bg-amber-500 text-white hover:bg-amber-600 text-xs font-bold transition shadow-xs';
                    btnAll.innerHTML = `打包中 (${{totalCheckedAll}}/${{totalAll}}) ➔ 一鍵完成 🎉`;
                }}
            }}
            if (btnReset) {{
                if (totalCheckedAll === 0) {{
                    btnReset.className = 'px-3.5 py-1.5 rounded-full bg-red-50 text-red-700 border border-red-200 text-xs font-bold transition';
                }} else {{
                    btnReset.className = 'px-3.5 py-1.5 rounded-full bg-stone-100 text-stone-600 hover:bg-red-50 hover:text-red-600 text-xs font-bold transition';
                }}
            }}
        }}

        function resetPackingChecklist() {{
            const emptyState = {{}};
            ['documents', 'carry_on', 'checked_bag'].forEach(groupKey => {{
                TRIP_DATA.packing_checklist[groupKey].forEach(item => {{
                    emptyState[item.id] = false;
                }});
            }});
            localStorage.setItem('kyushu_xmas_checklist', JSON.stringify(emptyState));
            initChecklist();
            showToast('已將所有檢查項目重設清空，刪除線全消！⚪');
        }}

        function checkAllPacking() {{
            const fullState = {{}};
            ['documents', 'carry_on', 'checked_bag'].forEach(groupKey => {{
                TRIP_DATA.packing_checklist[groupKey].forEach(item => {{
                    fullState[item.id] = true;
                }});
            }});
            localStorage.setItem('kyushu_xmas_checklist', JSON.stringify(fullState));
            initChecklist();
            fireChristmasCheer();
            showToast('全數打包完畢！準備出發！🎉');
        }}

        function calcFromJpy(val) {{
            const rate = TRIP_DATA.rate_to_twd || 0.2078;
            const twdInput = document.getElementById('calc-twd');
            if (!twdInput) return;
            if (val === '') {{ twdInput.value = ''; return; }}
            twdInput.value = Math.round(parseFloat(val) * rate);
        }}

        function calcFromTwd(val) {{
            const rate = TRIP_DATA.rate_to_twd || 0.2078;
            const jpyInput = document.getElementById('calc-jpy');
            if (!jpyInput) return;
            if (val === '') {{ jpyInput.value = ''; return; }}
            jpyInput.value = Math.round(parseFloat(val) / rate);
        }}

        // ======================= 🎴 南九州自駕集章巡禮 ＆ 家族微電影靈感 (實境雙軌解鎖) =======================
        const STAMPS_DATA = [
            {{
                id: 'kumamoto_castle',
                day: 'Day 7',
                name: '熊本城 ＆ 櫻之馬場城彩苑',
                area: '熊本市中央區',
                icon: '🏯',
                category: '歷史名城',
                stamp_title: '銀杏名城',
                stamp_sub: '熊本城天守',
                film_tip: '捕捉長輩漫步城彩苑老街，咬下第一口熱呼呼芥末蓮藕餅的驚奇笑容（自然側拍 5 秒）。',
                photo_spot: '天守閣仰角大合照、城彩苑古風燈籠前',
                badge_tag: 'history',
                quiz: {{
                    question: '熊本城別名為「銀杏城」，相傳是因為當年加藤清正親手在天守閣前種下了哪種象徵樹木？',
                    options: ['金黃大銀杏樹 (親手種植)', '百年垂枝櫻花樹', '京都大紅槭樹'],
                    answer: 0,
                    explain: '答對了！加藤清正建城時親手種下大銀杏，故熊本城又稱銀杏城！'
                }}
            }},
            {{
                id: 'aso_volcano',
                day: 'Day 2',
                name: '阿蘇中岳火口 ＆ 草千里之濱',
                area: '阿蘇市火山群',
                icon: '🌋',
                category: '活火山高原',
                stamp_title: '雄大中岳',
                stamp_sub: '阿蘇大火口',
                film_tip: '長輩手捧熱呼呼咖啡，站在草千里遠眺冒著白煙的活火山，海風吹過頭髮的悠閒側影。',
                photo_spot: '草千里大草原背影、阿蘇火山口冒煙同框',
                badge_tag: 'drive',
                quiz: {{
                    question: '在阿蘇中岳第一火口觀景步道旁，現場設立了許多防範火山突發噴發的堅固圓形避難建築叫什麼？',
                    options: ['退避壕 (堅固混凝土碉堡)', '地下防空坑道', '火山觀測木屋'],
                    answer: 0,
                    explain: '答對了！火口步道周圍的圓形厚實退避壕，是阿蘇火山獨特的安全象徵！'
                }}
            }},
            {{
                id: 'daikanbo',
                day: 'Day 2',
                name: '大觀峰展望台 ＆ 牛奶之路',
                area: '阿蘇市山田',
                icon: '⛰️',
                category: '絕景展望',
                stamp_title: '阿蘇雄姿',
                stamp_sub: '大觀峰頂',
                film_tip: '全員走在通往大觀峰頂端石碑的突出山岬上，360度大景環繞，長輩張開雙手的豪氣側錄。',
                photo_spot: '展望台最高石碑、遠眺阿蘇五岳「釋迦涅槃佛」全景',
                badge_tag: 'drive',
                quiz: {{
                    question: '從大觀峰向南遠眺阿蘇五岳，其起伏連綿的山巒輪廓在當地傳說中看起來最像什麼神聖形態？',
                    options: ['安祥仰臥的「釋迦涅槃佛」', '奔馳的草原神駒', '展翅的金色鳳凰'],
                    answer: 0,
                    explain: '答對了！阿蘇五岳遠望宛如一位仰臥朝天的釋迦佛陀，被譽為涅槃釋迦像！'
                }}
            }},
            {{
                id: 'kurokawa_onsen',
                day: 'Day 2',
                name: '黑川溫泉街 ＆ 冬季竹燈祭',
                area: '南小國町黑川',
                icon: '♨️',
                category: '秘湯街町',
                stamp_title: '秘湯黑川',
                stamp_sub: '湯明竹燈祭',
                film_tip: '黃昏時長輩穿著日式花浴衣、踩著木屐漫步在竹燈籠點綴的石板斜坡上，提燈漫步的背影步態。',
                photo_spot: '丸鈴橋竹燈祭（湯あかり）、山彥旅館仙人風呂',
                badge_tag: 'onsen',
                quiz: {{
                    question: '黑川溫泉冬季每晚於溪流與川端通點亮的夢幻「湯明 (湯あかり)」祭典，主要的透光燈球是用什麼天然材料手工編織？',
                    options: ['在地竹子 (鏤空竹球與竹筒)', '日本石州和紙', '彩色吹製玻璃'],
                    answer: 0,
                    explain: '答對了！黑川居民利用當地疏伐的竹子手工編織成鏤空竹球，在溪面上散發溫暖幽光！'
                }}
            }},
            {{
                id: 'kamishikimi',
                day: 'Day 3',
                name: '上色見熊野座神社',
                area: '高森町上色見',
                icon: '⛩️',
                category: '神隱之森',
                stamp_title: '神隱之森',
                stamp_sub: '上色見熊野',
                film_tip: '穿梭在長滿青苔的百座石燈籠參道之間，晨光穿透杉樹林灑在長輩緩步向上的幽靜鏡頭。',
                photo_spot: '青苔石燈籠深邃參道、穿磐岩巨大被踢破的岩洞',
                badge_tag: 'shrine',
                quiz: {{
                    question: '沿著神社石階穿過本殿後方，會看到傳說被鬼八法師一腳踢穿的巨大破岩風洞叫什麼？',
                    options: ['穿磐岩 (穿戸岩)', '風穴天石', '天狗神窟'],
                    answer: 0,
                    explain: '答對了！巨大岩洞「穿磐岩」象徵打破一切障礙、必勝祈願，是這裡最震撼的能量景點！'
                }}
            }},
            {{
                id: 'takachiho_gorge',
                day: 'Day 3',
                name: '高千穗峽 ＆ 真名井瀑布',
                area: '宮崎縣高千穗',
                icon: '🚣',
                category: '神話峽谷',
                stamp_title: '神話飛瀑',
                stamp_sub: '真名井泛舟',
                film_tip: '划船破水前行時，從船尾低角度抓拍長輩仰望 17 公尺飛瀑水氣飄過臉龐的震撼讚嘆神情。',
                photo_spot: '小船穿過瀑布旁、峽谷御橋向下俯瞰視角',
                badge_tag: 'shrine',
                quiz: {{
                    question: '划木船穿行於柱狀節理玄武岩峭壁之間，最著名的這座落差 17 公尺日本百選名瀑叫什麼名字？',
                    options: ['真名井瀑布', '白絲飛瀑', '音無之瀧'],
                    answer: 0,
                    explain: '答對了！真名井瀑布相傳是天孫降臨神明引水所形成，是高千穗最經典的代表性地標！'
                }}
            }},
            {{
                id: 'aoshima_shrine',
                day: 'Day 4',
                name: '青島神社 ＆ 鬼之洗濯板',
                area: '宮崎市青島',
                icon: '🌊',
                category: '海洋奇岩',
                stamp_title: '鬼之洗濯',
                stamp_sub: '青島海神宮',
                film_tip: '走過青島彌生橋，長輩低頭好奇觀察腳下一層一層整齊如洗衣板奇岩海蝕地貌的驚嘆神情。',
                photo_spot: '鬼之洗濯板天然波浪石階、島內熱帶蒲葵樹林中的朱紅鳥居',
                badge_tag: 'shrine',
                quiz: {{
                    question: '青島周圍退潮時，砂岩與泥岩互層經數百萬年海浪侵蝕，形成一圈一圈整齊宛如洗衣板的天然奇景被稱為什麼？',
                    options: ['鬼之洗濯板 (鬼の洗濯板)', '龍宮仙階', '海神浪階'],
                    answer: 0,
                    explain: '答對了！國家天然紀念物「鬼之洗濯板」，幾何條紋從空中看宛如大自然神奇的洗衣板！'
                }}
            }},
            {{
                id: 'sunmesse_nichinan',
                day: 'Day 4',
                name: 'Sun Messe 日南（摩艾石像）',
                area: '宮崎縣日南市',
                icon: '🗿',
                category: '太平洋岸',
                stamp_title: '日南摩艾',
                stamp_sub: '復活節巨石',
                film_tip: '以 7 尊巨大摩艾石像為背景，全員戴上墨鏡或遮陽帽並肩站立、吹著太平洋海風的公路巨星感背影！',
                photo_spot: '7 尊巨大摩艾石像合照、面向太平洋斜坡上的鮮豔打卡長椅',
                badge_tag: 'drive',
                quiz: {{
                    question: '日南山坡上面向浩瀚太平洋的 7 尊巨大摩艾石像，是世界上唯一獲得哪裡官方授權完全復刻的？',
                    options: ['智利 復活節島 (Easter Island)', '夏威夷歐胡島', '南太平洋大溪地'],
                    answer: 0,
                    explain: '答對了！日本團隊曾協助修復智利復活節島石像，特獲長老會全球唯一授權復刻！'
                }}
            }},
            {{
                id: 'udo_shrine',
                day: 'Day 4',
                name: '鵜戶神宮 ＆ 龜石運玉投擲',
                area: '宮崎縣日南市',
                icon: '⛩️',
                category: '海崖洞穴',
                stamp_title: '開運神玉',
                stamp_sub: '鵜戶海蝕洞',
                film_tip: '長輩站在崖邊，左手拿著小陶球『運玉』，全神貫注揮臂丟向海中龜石凹洞的熱血神情（必開慢動作！）。',
                photo_spot: '巨大海蝕洞窟內的朱紅本殿、崖邊驚濤拍岸投運玉處',
                badge_tag: 'udo',
                quiz: {{
                    question: '在鵜戶神宮懸崖邊，男生用左手、女生用右手將黏土燒製的「運玉」投向海中哪種形狀的奇石背上凹槽以祈求好運？',
                    options: ['靈龜石 (神龜背上的凹槽)', '錦鯉石', '海豚奇岩'],
                    answer: 0,
                    explain: '答對了！將運玉精準丟進海中「靈龜石」背上的黃色方繩圈凹洞中，象徵心願必能成真！'
                }}
            }},
            {{
                id: 'sakurajima_ferry',
                day: 'Day 5',
                name: '櫻島渡輪 ＆ 溶岩海濱足湯',
                area: '鹿兒島港～櫻島',
                icon: '⛴️',
                category: '航海火山',
                stamp_title: '航海足湯',
                stamp_sub: '櫻島渡輪',
                film_tip: '在渡輪頂層甲板上，一邊吹著海風吃熱騰騰的藪金烏龍麵，看海鷗飛過海面的滿足吃相。',
                photo_spot: '錦江灣甲板海風吹拂照、櫻島熔岩海濱公園日本最長足湯',
                badge_tag: 'drive',
                quiz: {{
                    question: '搭乘櫻島渡輪 15 分鐘的航程中，甲板上全日本饕客口耳相傳、即使再趕也一定要搶吃一碗的靈魂美食是什麼？',
                    options: ['藪金 (やぶ金) 天婦羅烏龍麵', '黑豚濃湯拉麵', '薩摩甜甜圈'],
                    answer: 0,
                    explain: '答對了！「やぶ金」烏龍麵是櫻島渡輪傳奇美味，上船第一件事就是衝去點一碗！'
                }}
            }},
            {{
                id: 'senganen',
                day: 'Day 5',
                name: '薩摩大名庭園 仙巖園',
                area: '鹿兒島市吉野町',
                icon: '🏯',
                category: '薩摩名園',
                stamp_title: '薩摩名園',
                stamp_sub: '仙巖園借景',
                film_tip: '信步在仙巖園御殿迴廊前，以櫻島火山為背景，抓拍長輩一邊品嚐現烤兩棒餅 (ぢゃんぼ餅) 一邊談笑的溫馨鏡頭。',
                photo_spot: '借景櫻島的池泉回遊式庭園全景、望嶽樓、兩棒餅茶屋',
                badge_tag: 'history',
                quiz: {{
                    question: '仙巖園是薩摩藩主島津氏的別邸，其最精妙的日本傳統「借景」造園手法，是將哪一座大自然奇景借來當作庭園假山？',
                    options: ['櫻島活火山 (錦江灣當作水池)', '薩摩富士 開聞岳', '富士山'],
                    answer: 0,
                    explain: '答對了！仙巖園以雄偉的櫻島火山為假山、錦江灣為池塘，構成了全日本最氣勢磅礴的世界文化遺產大名庭園！'
                }}
            }},
            {{
                id: 'kirishima_shrine',
                day: 'Day 6',
                name: '國寶 霧島神宮 ＆ 千年神木',
                area: '鹿兒島縣霧島市',
                icon: '⛩️',
                category: '國寶神殿',
                stamp_title: '天孫降臨',
                stamp_sub: '國寶霧島神宮',
                film_tip: '穿梭在參天古杉林蔭參道中，冬日陽光穿過樹稍灑在長輩肩頭，長輩漫步欣賞朱紅國寶雕樑畫棟的悠閒鏡頭。',
                photo_spot: '鮮紅大鳥居階梯、800年巨杉神木前仰望合影',
                badge_tag: 'shrine',
                quiz: {{
                    question: '霧島神宮祭祀著日本神話中天孫降臨的主角「瓊瓊杵尊」，殿前參道旁矗立著一棵象徵長壽平安的神木是什麼樹？',
                    options: ['樹齡 800 年的挺拔巨大古杉 (杉木)', '千年樟樹名木', '古銀杏神木'],
                    answer: 0,
                    explain: '答對了！霧島神宮御神木是一株高達 38 公尺、樹齡 800 年的挺拔古杉，是南九州極具靈氣的國寶神木！'
                }}
            }}
        ];

        const BADGES_DATA = [
            {{
                id: 'driver',
                name: '九州自駕首席掌舵官',
                icon: '🚗',
                tag: 'drive',
                desc: '無論山路彎道或濱海公路，穩健帶領全家平安暢遊九州！',
                req: '解鎖阿蘇火山、大觀峰、櫻島渡輪或日南摩艾 (滿 2 處解鎖)'
            }},
            {{
                id: 'onsen',
                name: '黑川仙人秘湯鑒定師',
                icon: '♨️',
                tag: 'onsen',
                desc: '漫步黑川溫泉街與冬季竹燈祭，精通南九州頂級名湯與旅宿美學！',
                req: '解鎖黑川溫泉街與竹燈祭'
            }},
            {{
                id: 'shrine',
                name: '神話大地全方位庇佑者',
                icon: '⛩️',
                tag: 'shrine',
                desc: '走遍八百萬神明聚會所，天孫降臨神宮與幽靜神隱古社福氣招好招滿！',
                req: '解鎖上色見熊野座、高千穗峽、青島神社或霧島神宮 (滿 2 處解鎖)'
            }},
            {{
                id: 'luck',
                name: '鵜戶龜石開運神射手',
                icon: '🎯',
                tag: 'udo',
                desc: '一擲入洞！象徵 2027 全年運勢爆棚、身體安康、大吉大利！',
                req: '解鎖鵜戶神宮運玉投擲印章'
            }},
            {{
                id: 'food',
                name: '薩摩大名與熊本古城巡禮者',
                icon: '🏯',
                tag: 'history',
                desc: '登熊本天守閣、賞仙巖園借景櫻島，沉浸於最深厚迷人的九州歷史風華！',
                req: '解鎖熊本城與仙巖園大名庭園'
            }},
            {{
                id: 'movie',
                name: '2026 家族微電影奧斯卡最佳劇組',
                icon: '🎬',
                tag: 'all',
                desc: '這趟旅程不是普通的旅行，而是一部值得世代相傳的精彩紀錄片！',
                req: '全數收集 12 枚南九州自駕印記'
            }}
        ];

        function playStampSound() {{
            try {{
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(140, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(40, ctx.currentTime + 0.12);
                gain.gain.setValueAtTime(0.35, ctx.currentTime);
                gain.gain.linearRampToValueAtTime(0.01, ctx.currentTime + 0.12);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.13);
            }} catch(e) {{}}
        }}

        function getStampsProgress() {{
            try {{
                return JSON.parse(localStorage.getItem('kyushu_trip_stamps_v1') || '{{}}');
            }} catch(e) {{
                return {{}};
            }}
        }}

        function saveStampsProgress(data) {{
            try {{
                localStorage.setItem('kyushu_trip_stamps_v1', JSON.stringify(data));
            }} catch(e) {{}}
        }}

        function initStamps() {{
            renderStamps();
            renderFamilyBoard();
        }}

        function renderStamps() {{
            const container = document.getElementById('stamps-grid-container');
            if (!container) return;
            const progress = getStampsProgress();
            container.innerHTML = '';

            let stampedCount = 0;

            STAMPS_DATA.forEach(item => {{
                const stampInfo = progress[item.id] || null;
                const isStamped = !!(stampInfo && stampInfo.stamped);
                if (isStamped) stampedCount++;

                const card = document.createElement('div');
                card.className = `cute-card p-4 sm:p-5 relative border-2 ${{isStamped ? 'border-red-300 bg-red-50/20' : 'border-stone-200 bg-white'}} hover:border-red-300 transition-all flex flex-col justify-between space-y-3.5 shadow-2xs`;

                const unlockMethodText = stampInfo?.method === 'photo' ? '📸 照片驗證蓋印' : stampInfo?.method === 'quiz' ? '🧩 實地訪查答對' : '✅ 蓋印完成';

                card.innerHTML = `
                    <div class="space-y-3">
                        <!-- 頂部標籤與天數 -->
                        <div class="flex items-center justify-between pb-2 border-b border-stone-100">
                            <span class="cute-pill bg-red-50 text-red-700 font-bold text-[10px] border border-red-200">
                                ${{item.day}} ｜ ${{item.category}}
                            </span>
                            <span class="text-[10px] text-stone-400 font-bold truncate max-w-[120px]">
                                📍 ${{item.area}}
                            </span>
                        </div>

                        <!-- 景點名稱與日式戳印區 -->
                        <div class="flex items-center justify-between gap-3">
                            <div class="flex-1 min-w-0">
                                <h4 class="font-black text-stone-800 text-sm sm:text-base leading-snug truncate" title="${{item.name}}">
                                    ${{item.icon}} ${{item.name}}
                                </h4>
                                <p class="text-[11px] text-stone-500 font-medium mt-1 line-clamp-1" title="${{item.photo_spot}}">
                                    📸 推薦：${{item.photo_spot}}
                                </p>
                                ${{isStamped ? `
                                    <div class="inline-flex items-center gap-1 mt-2 text-[10px] text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded-full font-bold border border-emerald-200 shadow-2xs">
                                        <span>${{unlockMethodText}}</span>
                                        <span>•</span>
                                        <span>${{stampInfo.time || '2026/12'}}</span>
                                    </div>
                                ` : `
                                    <div class="text-[10px] text-amber-700 bg-amber-50 px-2 py-0.5 rounded-md border border-amber-200 mt-2 font-bold inline-flex items-center gap-1">
                                        <span>🔒</span> 拍照片 或 答對問題 解鎖蓋印
                                    </div>
                                `}}
                            </div>

                            <!-- 戳印本體 -->
                            <div class="shrink-0">
                                ${{isStamped ? `
                                    <div class="w-20 h-20 sm:w-22 sm:h-22 rounded-full border-3 border-double border-red-600 bg-red-50 text-red-700 flex flex-col items-center justify-center p-1 shadow-md rotate-[-8deg] hover:rotate-0 transition-transform cursor-pointer" onclick="showStampPhotoPreview('${{item.id}}')" title="已蓋印！點擊查看大圖">
                                        <span class="text-[9px] font-black tracking-widest text-red-600 border-b border-red-400 pb-0.5 leading-none">${{item.stamp_title}}</span>
                                        <span class="text-[11px] font-black tracking-tighter my-0.5 text-red-700 leading-tight">${{item.stamp_sub}}</span>
                                        <span class="text-[8px] font-mono font-bold text-red-500 scale-90">2026 XMAS</span>
                                    </div>
                                ` : `
                                    <div class="w-20 h-20 sm:w-22 sm:h-22 rounded-full border-2 border-dashed border-stone-300 bg-stone-50/70 text-stone-400 flex flex-col items-center justify-center p-1 shadow-2xs">
                                        <span class="text-xl">🏮</span>
                                        <span class="text-[9px] font-bold mt-1 text-stone-400">待解鎖</span>
                                    </div>
                                `}}
                            </div>
                        </div>

                        <!-- 🎥 給掌鏡者的電影感短片鏡頭建議 -->
                        <div class="bg-amber-50/80 border border-amber-200/90 rounded-2xl p-2.5 sm:p-3 text-xs text-stone-700 space-y-1">
                            <div class="font-black text-amber-800 flex items-center gap-1.5 text-[11px]">
                                <span>🎥</span>
                                <span>家族微電影・自然抓拍靈感（捕捉最動人的瞬間）</span>
                            </div>
                            <p class="text-[11px] text-stone-600 leading-relaxed font-medium">
                                ${{item.film_tip}}
                            </p>
                        </div>

                        <!-- ✍️ 這站的心情短語 / 家族金句 (選填) -->
                        <div class="bg-stone-50/70 border border-stone-200/80 rounded-2xl p-2.5 space-y-1.5">
                            <div class="flex items-center justify-between text-[11px]">
                                <span class="font-bold text-stone-700 flex items-center gap-1">
                                    <span>✍️</span> <span>這刻的心情短語 / 家族金句 (選填)</span>
                                </span>
                                ${{stampInfo?.note ? `
                                    <span class="text-[10px] text-emerald-700 font-bold bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
                                        ✓ 已記錄
                                    </span>
                                ` : `
                                    <span class="text-[10px] text-stone-400">長輩不想寫也沒關係～</span>
                                `}}
                            </div>
                            <div class="flex items-center gap-1.5">
                                <input type="text"
                                    class="flex-1 bg-white border border-stone-200 focus:border-amber-400 rounded-xl px-2.5 py-1 text-xs text-stone-800 placeholder-stone-400 focus:outline-none transition shadow-2xs"
                                    placeholder="寫下一句當下的心情、爆笑金句或溫暖感動..."
                                    value="${{escapeHtml(stampInfo?.note || '')}}"
                                    id="stamp-note-input-${{item.id}}"
                                    onchange="saveStampNote('${{item.id}}', this.value)"
                                    onkeydown="if(event.key==='Enter') saveStampNote('${{item.id}}', this.value, true)"
                                />
                                <button type="button" onclick="saveStampNote('${{item.id}}', document.getElementById('stamp-note-input-${{item.id}}').value, true)" class="px-2.5 py-1 rounded-xl bg-amber-100 hover:bg-amber-200 text-amber-900 border border-amber-300 font-bold text-xs shrink-0 transition active:scale-95 shadow-2xs" title="保存文字">
                                    儲存
                                </button>
                            </div>
                            ${{stampInfo?.note ? `
                                <div class="text-[11px] text-amber-950 bg-amber-50/80 border border-amber-200/80 rounded-xl px-2.5 py-1.5 italic font-medium flex items-start gap-1.5 shadow-2xs">
                                    <span class="text-xs shrink-0">💬</span>
                                    <span class="leading-relaxed whitespace-pre-wrap">${{escapeHtml(stampInfo.note)}}</span>
                                </div>
                            ` : ''}}
                        </div>
                    </div>

                    <!-- 解鎖按鈕區 (實境雙軌驗證：拍照驗證 OR 實地小問答) -->
                    <div class="pt-2 border-t border-stone-100">
                        ${{isStamped ? `
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-2">
                                    ${{stampInfo && stampInfo.photo ? `
                                        <img src="${{stampInfo.photo}}" class="w-9 h-9 rounded-lg object-cover border border-stone-200 shadow-2xs cursor-pointer" onclick="showStampPhotoPreview('${{item.id}}')" title="點擊放大相片">
                                        <span class="text-[10px] text-emerald-700 font-bold">已保存現場照 ✨</span>
                                    ` : `
                                        <label class="cursor-pointer text-[10px] font-bold text-stone-600 hover:text-red-600 flex items-center gap-1">
                                            <span>📷 補存現場照片</span>
                                            <input type="file" accept="image/*" class="hidden" onchange="handleStampPhotoUpload('${{item.id}}', event)">
                                        </label>
                                    `}}
                                </div>
                                <button type="button" onclick="resetSingleStamp('${{item.id}}')" class="text-[10px] text-stone-400 hover:text-red-500 font-medium transition" title="重新解鎖挑戰">
                                    重置此站 ↺
                                </button>
                            </div>
                        ` : `
                            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
                                <!-- 方式 1: 拍照驗證解鎖 -->
                                <label class="flex-1 cursor-pointer py-1.5 px-2.5 rounded-xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-700 hover:to-rose-700 text-white font-bold text-xs flex items-center justify-center gap-1 shadow-2xs active:scale-95 transition">
                                    <span>📸</span>
                                    <span>拍照驗證解鎖</span>
                                    <input type="file" accept="image/*" class="hidden" onchange="handleStampPhotoUpload('${{item.id}}', event)">
                                </label>

                                <!-- 方式 2: 實地訪查小問答解鎖 -->
                                <button type="button" onclick="openStampQuizModal('${{item.id}}')" class="flex-1 py-1.5 px-2.5 rounded-xl bg-amber-100 hover:bg-amber-200 text-amber-900 border border-amber-300 font-bold text-xs flex items-center justify-center gap-1 shadow-2xs active:scale-95 transition">
                                    <span>🧩</span>
                                    <span>實地訪查解鎖</span>
                                </button>
                            </div>
                        `}}
                    </div>
                `;
                container.appendChild(card);
            }});

            // 更新探索進度條
            const total = STAMPS_DATA.length;
            const pct = Math.round((stampedCount / total) * 100);
            const countLabel = document.getElementById('stamps-count-label');
            const pctLabel = document.getElementById('stamps-percent-label');
            const bar = document.getElementById('stamps-progress-bar');
            const hint = document.getElementById('stamps-status-hint');

            if (countLabel) countLabel.textContent = `${{stampedCount}} / ${{total}}`;
            if (pctLabel) pctLabel.textContent = `${{pct}}%`;
            if (bar) bar.style.width = `${{pct}}%`;
            if (hint) {{
                if (stampedCount === 0) hint.textContent = '拍照片或回答現場題目即可蓋印 ❄️';
                else if (stampedCount < 6) hint.textContent = `實境探索中（已認證解鎖 ${{stampedCount}} 處）✨`;
                else if (stampedCount < 12) hint.textContent = `集章進度過半！家族回憶大豐收（${{stampedCount}}/12）🎉`;
                else hint.textContent = '🎊 12 處名勝全數制霸！家族微電影大圓滿！';
            }}

            // 更新家族榮譽大師成就榜與心情留言板
            renderBadges(progress, stampedCount);
            renderFamilyBoard();
        }}

        function renderBadges(progress, stampedCount) {{
            const badgeContainer = document.getElementById('badges-grid-container');
            const countBadge = document.getElementById('badges-unlocked-count');
            if (!badgeContainer) return;
            badgeContainer.innerHTML = '';

            let unlockedCount = 0;

            BADGES_DATA.forEach(badge => {{
                let isUnlocked = false;
                if (badge.id === 'driver') {{
                    isUnlocked = !!(progress['aso_volcano']?.stamped || progress['daikanbo']?.stamped || progress['sakurajima_ferry']?.stamped);
                }} else if (badge.id === 'onsen') {{
                    isUnlocked = !!(progress['kurokawa_onsen']?.stamped);
                }} else if (badge.id === 'shrine') {{
                    isUnlocked = !!((progress['kamishikimi']?.stamped ? 1 : 0) + (progress['takachiho_gorge']?.stamped ? 1 : 0) + (progress['aoshima_shrine']?.stamped ? 1 : 0) + (progress['kirishima_shrine']?.stamped ? 1 : 0) >= 2);
                }} else if (badge.id === 'luck') {{
                    isUnlocked = !!(progress['udo_shrine']?.stamped);
                }} else if (badge.id === 'food') {{
                    isUnlocked = !!(progress['kumamoto_castle']?.stamped || progress['senganen']?.stamped);
                }} else if (badge.id === 'movie') {{
                    isUnlocked = stampedCount === STAMPS_DATA.length;
                }}

                if (isUnlocked) unlockedCount++;

                const div = document.createElement('div');
                div.className = `p-3.5 rounded-2xl border transition-all ${{isUnlocked ? 'bg-gradient-to-br from-amber-50 to-orange-50 border-amber-300 shadow-sm ring-2 ring-amber-200' : 'bg-stone-50/60 border-stone-200 text-stone-400'}}`;

                div.innerHTML = `
                    <div class="flex items-center justify-between pb-1.5 border-b ${{isUnlocked ? 'border-amber-200' : 'border-stone-200'}}">
                        <span class="font-black text-xs ${{isUnlocked ? 'text-amber-900' : 'text-stone-500'}} flex items-center gap-1.5">
                            <span class="text-base">${{badge.icon}}</span>
                            <span>${{badge.name}}</span>
                        </span>
                        ${{isUnlocked ? `
                            <span class="cute-pill bg-amber-200 text-amber-900 font-black text-[10px] shadow-2xs">✨ 榮譽解鎖</span>
                        ` : `
                            <span class="text-[10px] text-stone-400 font-bold">進行中</span>
                        `}}
                    </div>
                    <p class="text-[11px] ${{isUnlocked ? 'text-stone-700 font-bold' : 'text-stone-400'}} mt-1.5 leading-snug">
                        ${{badge.desc}}
                    </p>
                    <div class="text-[10px] ${{isUnlocked ? 'text-amber-700 font-bold' : 'text-stone-400'}} mt-1">
                        🎯 條件：${{badge.req}}
                    </div>
                `;
                badgeContainer.appendChild(div);
            }});

            if (countBadge) countBadge.textContent = `已解鎖 ${{unlockedCount}} / ${{BADGES_DATA.length}}`;
        }}

        // ======================= 實地訪查小問答 Modal 互動邏輯 =======================
        let activeQuizStampId = null;

        function openStampQuizModal(stampId) {{
            const item = STAMPS_DATA.find(s => s.id === stampId);
            if (!item || !item.quiz) return;
            activeQuizStampId = stampId;

            const modal = document.getElementById('stamp-quiz-modal');
            const spotNameEl = document.getElementById('quiz-modal-spot-name');
            const questionEl = document.getElementById('quiz-modal-question');
            const hintEl = document.getElementById('quiz-modal-hint');
            const optionsEl = document.getElementById('quiz-modal-options');
            const feedbackEl = document.getElementById('quiz-modal-feedback');

            if (spotNameEl) spotNameEl.textContent = `${{item.icon}} ${{item.name}} 實地訪查`;
            if (questionEl) questionEl.textContent = item.quiz.question;
            if (hintEl) hintEl.textContent = '💡 答案就在現場招牌、景點說明或眼前景致中！';
            if (feedbackEl) {{
                feedbackEl.className = 'hidden text-xs font-bold py-2 px-3 rounded-xl';
                feedbackEl.textContent = '';
            }}

            if (optionsEl) {{
                optionsEl.innerHTML = '';
                item.quiz.options.forEach((optText, optIdx) => {{
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = 'w-full p-3 rounded-2xl bg-white hover:bg-amber-50 border-2 border-stone-200 hover:border-amber-400 text-stone-800 font-bold text-xs text-left transition flex items-center justify-between group active:scale-98';
                    btn.innerHTML = `
                        <span class="flex items-center gap-2">
                            <span class="w-6 h-6 rounded-full bg-amber-100 text-amber-800 flex items-center justify-center text-xs font-black group-hover:bg-amber-200 shrink-0">
                                ${{String.fromCharCode(65 + optIdx)}}
                            </span>
                            <span>${{optText}}</span>
                        </span>
                        <span class="text-stone-300 group-hover:text-amber-500 font-bold">➔</span>
                    `;
                    btn.onclick = () => submitStampQuiz(stampId, optIdx);
                    optionsEl.appendChild(btn);
                }});
            }}

            if (modal) modal.classList.remove('hidden');
        }}

        function closeStampQuizModal() {{
            const modal = document.getElementById('stamp-quiz-modal');
            if (modal) modal.classList.add('hidden');
            activeQuizStampId = null;
        }}

        function submitStampQuiz(stampId, chosenIdx) {{
            const item = STAMPS_DATA.find(s => s.id === stampId);
            if (!item || !item.quiz) return;

            const feedbackEl = document.getElementById('quiz-modal-feedback');

            if (chosenIdx === item.quiz.answer) {{
                // 答對了！
                playStampSound();
                const progress = getStampsProgress();
                if (!progress[stampId]) progress[stampId] = {{}};
                progress[stampId].stamped = true;
                progress[stampId].method = 'quiz';
                const now = new Date();
                progress[stampId].time = `${{now.getFullYear()}}/${{now.getMonth() + 1}}/${{now.getDate()}} ${{String(now.getHours()).padStart(2, '0')}}:${{String(now.getMinutes()).padStart(2, '0')}}`;
                saveStampsProgress(progress);

                if (feedbackEl) {{
                    feedbackEl.className = 'block text-xs font-bold py-2.5 px-3.5 rounded-xl bg-emerald-100 text-emerald-800 border border-emerald-300';
                    feedbackEl.innerHTML = `🎉 ${{item.quiz.explain}}`;
                }}

                setTimeout(() => {{
                    closeStampQuizModal();
                    renderStamps();
                    showToast(`🎉 答對了！恭喜成功解鎖【${{item.stamp_title}}】紀念印章！🏮`);
                    const allDone = STAMPS_DATA.every(s => progress[s.id] && progress[s.id].stamped);
                    if (allDone) fireChristmasCheer();
                }}, 1100);
            }} else {{
                // 答錯
                if (feedbackEl) {{
                    feedbackEl.className = 'block text-xs font-bold py-2 px-3 rounded-xl bg-rose-100 text-rose-800 border border-rose-300';
                    feedbackEl.textContent = '哎呀差一點點！仔細看一下現場景觀或再猜一次看看～💡';
                }}
            }}
        }}

        function handleStampPhotoUpload(stampId, event) {{
            const file = event.target.files && event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {{
                const img = new Image();
                img.onload = function() {{
                    const maxSide = 480;
                    let w = img.width;
                    let h = img.height;
                    if (w > h && w > maxSide) {{
                        h = Math.round((h * maxSide) / w);
                        w = maxSide;
                    }} else if (h > maxSide) {{
                        w = Math.round((w * maxSide) / h);
                        h = maxSide;
                    }}

                    const canvas = document.createElement('canvas');
                    canvas.width = w;
                    canvas.height = h;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, w, h);
                    const compressedDataUrl = canvas.toDataURL('image/jpeg', 0.82);

                    playStampSound();
                    const progress = getStampsProgress();
                    if (!progress[stampId]) progress[stampId] = {{}};
                    progress[stampId].stamped = true;
                    progress[stampId].method = 'photo';
                    progress[stampId].photo = compressedDataUrl;
                    const now = new Date();
                    progress[stampId].time = `${{now.getFullYear()}}/${{now.getMonth() + 1}}/${{now.getDate()}} ${{String(now.getHours()).padStart(2, '0')}}:${{String(now.getMinutes()).padStart(2, '0')}}`;

                    saveStampsProgress(progress);
                    renderStamps();
                    const item = STAMPS_DATA.find(s => s.id === stampId);
                    showToast(`📷 拍照認證成功！已蓋上【${{item ? item.stamp_title : '景點'}}】日式紀念戳章！🏮✨`);

                    const allDone = STAMPS_DATA.every(s => progress[s.id] && progress[s.id].stamped);
                    if (allDone) fireChristmasCheer();
                }};
                img.src = e.target.result;
            }};
            reader.readAsDataURL(file);
        }}

        function resetSingleStamp(stampId) {{
            const progress = getStampsProgress();
            if (progress[stampId]) {{
                delete progress[stampId];
                saveStampsProgress(progress);
                renderStamps();
                showToast('已重設此站進度，可隨時重新拍照或答題！⚪');
            }}
        }}

        function unlockAllStamps() {{
            playStampSound();
            const progress = getStampsProgress();
            const now = new Date();
            const timeStr = `${{now.getFullYear()}}/${{now.getMonth() + 1}}/${{now.getDate()}} ${{String(now.getHours()).padStart(2, '0')}}:${{String(now.getMinutes()).padStart(2, '0')}}`;
            STAMPS_DATA.forEach(item => {{
                if (!progress[item.id]) progress[item.id] = {{}};
                progress[item.id].stamped = true;
                progress[item.id].method = progress[item.id].method || 'photo';
                progress[item.id].time = timeStr;
            }});
            saveStampsProgress(progress);
            renderStamps();
            fireChristmasCheer();
            showToast('已為您一鍵點亮全部 12 枚南九州日式紀念戳章！🎉');
        }}

        function resetAllStamps() {{
            localStorage.removeItem('kyushu_trip_stamps_v1');
            renderStamps();
            showToast('已重設集章進度，歡迎隨時重新蓋印！⚪');
        }}

        function escapeHtml(str) {{
            if (!str) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
        }}

        function saveStampNote(stampId, text, showFeedback) {{
            const progress = getStampsProgress();
            if (!progress[stampId]) progress[stampId] = {{ stamped: false }};
            progress[stampId].note = (text || '').trim();
            saveStampsProgress(progress);
            renderStamps();
            renderFamilyBoard();
            if (showFeedback) {{
                showToast('已保存旅途心情手記！✍️✨');
            }}
        }}

        function saveStampNoteFromModal(stampId) {{
            const input = document.getElementById('modal-note-input');
            if (!input) return;
            saveStampNote(stampId, input.value, true);
            showStampPhotoPreview(stampId);
        }}

        function getFamilyMessages() {{
            try {{
                const stored = localStorage.getItem('kyushu_trip_family_messages_v1');
                if (stored) return JSON.parse(stored);
            }} catch(e) {{}}
            return [
                {{
                    id: 'msg_welcome',
                    sender: '主辦導遊 🚗',
                    text: '2026 南九州冬季聖誕自駕之旅出發！大家盡情拍照、享受溫泉與美食，隨時在這裡分享心情喔！❄️✨',
                    mood: '😊',
                    time: '2026/12/22 09:00',
                    likes: 3
                }}
            ];
        }}

        function saveFamilyMessages(msgs) {{
            try {{
                localStorage.setItem('kyushu_trip_family_messages_v1', JSON.stringify(msgs));
            }} catch(e) {{}}
        }}

        let activeFamilyMood = '😊';
        function selectFamilyMood(emoji) {{
            activeFamilyMood = emoji;
            document.querySelectorAll('.mood-emoji-btn').forEach(btn => {{
                if (btn.dataset.emoji === emoji) {{
                    btn.classList.add('ring-2', 'ring-amber-400', 'bg-amber-100');
                }} else {{
                    btn.classList.remove('ring-2', 'ring-amber-400', 'bg-amber-100');
                }}
            }});
        }}

        function toggleCustomSender(val) {{
            const input = document.getElementById('family-msg-custom-sender');
            if (!input) return;
            if (val === '自訂稱呼 ✍️') {{
                input.classList.remove('hidden');
                input.focus();
            }} else {{
                input.classList.add('hidden');
            }}
        }}

        function addFamilyMessage() {{
            const senderSelect = document.getElementById('family-msg-sender');
            const customSender = document.getElementById('family-msg-custom-sender');
            const textInput = document.getElementById('family-msg-text');
            if (!textInput) return;
            
            const text = textInput.value.trim();
            if (!text) {{
                showToast('請先輸入想分享的心情小語喔！✍️');
                return;
            }}
            
            let sender = senderSelect ? senderSelect.value : '全家大家庭 🏠';
            if (sender === '自訂稱呼 ✍️' && customSender && customSender.value.trim()) {{
                sender = customSender.value.trim();
            }}
            
            const now = new Date();
            const timeStr = `${{now.getMonth() + 1}}/${{now.getDate()}} ${{String(now.getHours()).padStart(2, '0')}}:${{String(now.getMinutes()).padStart(2, '0')}}`;
            
            const msgs = getFamilyMessages();
            msgs.unshift({{
                id: 'msg_' + Date.now(),
                sender: sender,
                text: text,
                mood: activeFamilyMood,
                time: timeStr,
                likes: 0
            }});
            
            saveFamilyMessages(msgs);
            textInput.value = '';
            renderFamilyBoard();
            showToast('已成功貼上心情留言！💌✨');
        }}

        function likeFamilyMessage(msgId) {{
            const msgs = getFamilyMessages();
            const target = msgs.find(m => m.id === msgId);
            if (target) {{
                target.likes = (target.likes || 0) + 1;
                saveFamilyMessages(msgs);
                renderFamilyBoard();
            }}
        }}

        function deleteFamilyMessage(msgId) {{
            let msgs = getFamilyMessages();
            msgs = msgs.filter(m => m.id !== msgId);
            saveFamilyMessages(msgs);
            renderFamilyBoard();
            showToast('已移除該則留言。');
        }}

        function renderFamilyBoard() {{
            const container = document.getElementById('family-board-container');
            const countLabel = document.getElementById('family-notes-count');
            if (!container) return;
            container.innerHTML = '';

            const msgs = getFamilyMessages();
            const progress = getStampsProgress();

            const stampMemories = [];
            STAMPS_DATA.forEach(item => {{
                const sp = progress[item.id];
                if (sp && (sp.note || sp.photo)) {{
                    stampMemories.push({{
                        item: item,
                        note: sp.note,
                        photo: sp.photo,
                        time: sp.time || '2026/12'
                    }});
                }}
            }});

            const totalCount = msgs.length + stampMemories.length;
            if (countLabel) countLabel.textContent = `${{totalCount}} 則心情紀錄`;

            if (totalCount === 0) {{
                container.innerHTML = `
                    <div class="col-span-full py-8 text-center text-stone-400 bg-stone-50 rounded-2xl border-2 border-dashed border-stone-200 text-xs">
                        尚無心情留言或景點手記，出發後在各站打卡或輸入一句話，這裡就會自動編成一本專屬相簿手札！🌸
                    </div>
                `;
                return;
            }}

            msgs.forEach(msg => {{
                const card = document.createElement('div');
                card.className = 'p-3.5 rounded-2xl border border-amber-200/90 bg-amber-50/60 shadow-2xs flex flex-col justify-between space-y-2 relative transition hover:border-amber-300';
                card.innerHTML = `
                    <div class="space-y-1.5">
                        <div class="flex items-center justify-between pb-1 border-b border-amber-200/60">
                            <span class="text-xs font-black text-amber-900 flex items-center gap-1">
                                <span>${{msg.mood || '📌'}}</span>
                                <span>${{escapeHtml(msg.sender)}}</span>
                            </span>
                            <span class="text-[10px] text-stone-400 font-mono">${{msg.time}}</span>
                        </div>
                        <p class="text-xs text-stone-800 leading-relaxed font-medium whitespace-pre-wrap">${{escapeHtml(msg.text)}}</p>
                    </div>
                    <div class="flex items-center justify-between pt-1 text-[10px] text-stone-400">
                        <button type="button" onclick="likeFamilyMessage('${{msg.id}}')" class="flex items-center gap-1 text-rose-600 font-bold hover:scale-105 active:scale-95 transition">
                            <span>❤️</span>
                            <span>${{msg.likes || 0}}</span>
                        </button>
                        <button type="button" onclick="deleteFamilyMessage('${{msg.id}}')" class="hover:text-red-500 transition" title="刪除">
                            ✕
                        </button>
                    </div>
                `;
                container.appendChild(card);
            }});

            stampMemories.forEach(mem => {{
                const card = document.createElement('div');
                card.className = 'p-3 rounded-2xl border border-red-200 bg-white shadow-2xs flex flex-col justify-between space-y-2 relative transition hover:border-red-300 hover:shadow-sm cursor-pointer';
                card.onclick = () => showStampPhotoPreview(mem.item.id);
                card.innerHTML = `
                    <div class="space-y-2">
                        <div class="flex items-center justify-between pb-1 border-b border-stone-100">
                            <span class="text-[10px] text-red-700 bg-red-50 px-2 py-0.5 rounded-md font-black border border-red-200">
                                ${{mem.item.icon}} ${{mem.item.name}}
                            </span>
                            <span class="text-[10px] text-stone-400 font-mono">${{mem.time}}</span>
                        </div>
                        ${{mem.photo ? `
                            <div class="relative w-full h-28 bg-stone-100 rounded-xl overflow-hidden border border-stone-200">
                                <img src="${{mem.photo}}" class="w-full h-full object-cover">
                                <div class="absolute bottom-1 right-1 bg-black/60 backdrop-blur-xs text-white text-[9px] px-1.5 py-0.5 rounded font-mono">
                                    📸 點擊放大
                                </div>
                            </div>
                        ` : ''}}
                        ${{mem.note ? `
                            <div class="bg-amber-50/70 border border-amber-200/80 rounded-xl p-2 text-[11px] text-stone-800 italic leading-snug">
                                “${{escapeHtml(mem.note)}}”
                            </div>
                        ` : `
                            <div class="text-[11px] text-stone-400 italic">已拍照蓋印留念 ✨</div>
                        `}}
                    </div>
                    <div class="text-[10px] text-stone-400 text-right flex items-center justify-between pt-1 border-t border-stone-50">
                        <span class="text-red-600 font-bold">🏮 ${{mem.item.stamp_title}}</span>
                        <span class="text-amber-700 font-bold">查看拍立得 ➔</span>
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function showStampPhotoPreview(stampId) {{
            const progress = getStampsProgress();
            const stampInfo = progress[stampId] || {{}};
            const photoUrl = stampInfo.photo;
            const note = stampInfo.note || '';
            const item = STAMPS_DATA.find(s => s.id === stampId);

            let modal = document.getElementById('stamp-photo-modal');
            if (!modal) {{
                modal = document.createElement('div');
                modal.id = 'stamp-photo-modal';
                modal.className = 'fixed inset-0 z-50 bg-black/85 flex items-center justify-center p-4 backdrop-blur-xs';
                modal.onclick = function() {{ modal.classList.add('hidden'); }};
                document.body.appendChild(modal);
            }}

            modal.innerHTML = `
                <div class="bg-white rounded-3xl p-5 max-w-md w-full space-y-3.5 text-center shadow-2xl border-4 border-amber-300 relative max-h-[92vh] overflow-y-auto" onclick="event.stopPropagation()">
                    <div class="flex items-center justify-between pb-2 border-b">
                        <div class="flex items-center gap-1.5 text-stone-800 font-black text-sm">
                            <span>📸</span>
                            <span>${{item ? item.name : '景點'}} 專屬拍立得</span>
                        </div>
                        <button onclick="document.getElementById('stamp-photo-modal').classList.add('hidden')" class="text-stone-400 hover:text-stone-600 text-lg font-bold">✕</button>
                    </div>

                    ${{photoUrl ? `
                        <div class="relative bg-stone-900 rounded-2xl overflow-hidden shadow-inner flex items-center justify-center">
                            <img src="${{photoUrl}}" class="w-full max-h-[50vh] object-contain rounded-2xl">
                            <div class="absolute bottom-2 right-2 px-2.5 py-1 bg-black/60 backdrop-blur-xs text-white text-[10px] rounded-full font-mono">
                                ${{stampInfo.time || '2026/12'}}
                            </div>
                        </div>
                    ` : `
                        <div class="py-8 bg-stone-50 rounded-2xl border-2 border-dashed border-stone-200 text-stone-400 text-xs">
                            尚未上傳相片，可點擊卡片上的「📷 補存現場照片」隨時添加！
                        </div>
                    `}}

                    <!-- 景點與紀念印章名稱 -->
                    <div class="flex items-center justify-between px-1 text-xs text-stone-500 font-medium">
                        <span>📍 ${{item ? item.area : ''}}</span>
                        <span class="font-bold text-red-600">🏮 ${{item ? item.stamp_title : ''}}</span>
                    </div>

                    <!-- 心情筆記 / 金句 -->
                    <div class="bg-amber-50/80 border border-amber-200 rounded-2xl p-3 text-left space-y-2">
                        <div class="flex items-center justify-between text-[11px] font-bold text-amber-900">
                            <span class="flex items-center gap-1">
                                <span>✍️</span> <span>這刻的心情手記 / 家族金句：</span>
                            </span>
                        </div>
                        ${{note ? `
                            <p class="text-xs text-stone-800 font-medium italic leading-relaxed whitespace-pre-wrap">“${{escapeHtml(note)}}”</p>
                        ` : `
                            <p class="text-xs text-stone-400 italic">尚無心情文字（完全選填，沒有文字也沒關係）</p>
                        `}}
                        <div class="pt-2 border-t border-amber-200/60 flex items-center gap-1.5">
                            <input type="text" id="modal-note-input" class="flex-1 bg-white border border-stone-200 rounded-xl px-2.5 py-1 text-xs text-stone-800 placeholder-stone-400 focus:outline-none focus:border-amber-400" placeholder="補充或修改這站的心情短語..." value="${{escapeHtml(note)}}">
                            <button type="button" onclick="saveStampNoteFromModal('${{stampId}}')" class="px-3 py-1 bg-amber-200 hover:bg-amber-300 text-amber-900 font-bold text-xs rounded-xl shadow-2xs transition active:scale-95">
                                儲存
                            </button>
                        </div>
                    </div>
                </div>
            `;
            modal.classList.remove('hidden');
        }}

        function copyToClipboard(text, msg) {{
            navigator.clipboard.writeText(text).then(() => {{
                showToast(msg || '已複製到剪貼簿！');
            }});
        }}

        function showToast(msg) {{
            const toast = document.getElementById('toast');
            const toastMsg = document.getElementById('toast-msg');
            if (!toast || !toastMsg) return;
            toastMsg.textContent = msg;
            toast.classList.remove('translate-y-16', 'opacity-0');
            toast.classList.add('translate-y-0', 'opacity-100');

            setTimeout(() => {{
                toast.classList.remove('translate-y-0', 'opacity-100');
                toast.classList.add('translate-y-16', 'opacity-0');
            }}, 2800);
        }}
    </script>

        <!-- 實地訪查小問答 Modal (實境解鎖) -->
        <div id="stamp-quiz-modal" class="hidden fixed inset-0 z-50 bg-black/85 flex items-center justify-center p-4 backdrop-blur-xs" onclick="closeStampQuizModal()">
            <div class="bg-white rounded-3xl p-5 sm:p-6 max-w-md w-full space-y-4 text-center shadow-2xl border-4 border-amber-400 relative" onclick="event.stopPropagation()">
                <div class="flex items-center justify-between border-b pb-2.5">
                    <div class="flex items-center gap-1.5 text-amber-800 font-black text-sm">
                        <span class="text-base">🧩</span>
                        <span id="quiz-modal-spot-name">景點現場訪查</span>
                    </div>
                    <button onclick="closeStampQuizModal()" class="text-stone-400 hover:text-stone-600 text-lg font-bold">✕</button>
                </div>
                <div class="bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200 rounded-2xl p-4 text-left space-y-2">
                    <span class="cute-pill bg-amber-200 text-amber-900 font-bold text-[10px]">現場觀察任務</span>
                    <h4 class="font-black text-stone-800 text-sm leading-snug" id="quiz-modal-question">題目載入中...</h4>
                    <p class="text-[11px] text-amber-700 font-medium" id="quiz-modal-hint">💡 答案就在現場招牌、景點說明或眼前景致中！</p>
                </div>
                <div class="space-y-2.5 text-left" id="quiz-modal-options"></div>
                <div id="quiz-modal-feedback" class="hidden text-xs font-bold py-2.5 px-3.5 rounded-xl"></div>
                <button onclick="closeStampQuizModal()" class="w-full py-2.5 rounded-2xl bg-stone-100 text-stone-600 font-bold text-xs hover:bg-stone-200 transition">
                    先去現場看一眼～稍後再答
                </button>
            </div>
        </div>

        <!-- 條碼全螢幕放大 Modal -->
        <div id="barcode-modal" class="hidden fixed inset-0 z-50 bg-black/85 flex items-center justify-center p-4 backdrop-blur-xs" onclick="closeBarcodeModal()">
            <div class="bg-white rounded-3xl p-6 max-w-md w-full space-y-4 text-center shadow-2xl border-4 border-red-500" onclick="event.stopPropagation()">
                <div class="flex items-center justify-between border-b pb-2">
                    <span class="font-black text-sm text-stone-800" id="modal-coupon-title">優惠券條碼</span>
                    <button type="button" onclick="closeBarcodeModal()" class="text-stone-400 hover:text-stone-600 text-base font-bold">✕</button>
                </div>
                <div id="modal-coupon-alert" class="bg-amber-50 text-amber-900 text-xs font-bold p-2.5 rounded-xl border border-amber-200 leading-snug text-left">
                    💡 請將手機螢幕亮度調至最大，直接出示給店員掃描
                </div>
                <div class="p-4 bg-white rounded-2xl border-2 border-stone-300 flex flex-col items-center justify-center space-y-2">
                    <div id="modal-barcode-svg" class="w-full flex justify-center"></div>
                    <div id="modal-barcode-num" class="font-mono font-black text-lg tracking-widest text-stone-900"></div>
                </div>
                <div id="modal-qr-svg" class="flex justify-center p-2 bg-stone-50 rounded-xl border border-stone-200"></div>
                <p class="text-[11px] text-stone-500 font-medium leading-relaxed" id="modal-coupon-condition"></p>
                
                <div class="space-y-2 pt-1">
                    <a id="modal-official-link-btn" href="#" target="_blank" class="w-full py-2.5 px-3 rounded-2xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-700 hover:to-rose-700 text-white font-black text-xs flex items-center justify-center gap-1.5 shadow-md transition">
                        <span>🌐</span> 開啟官方電子券網頁 (現場核銷專用) ↗
                    </a>
                    <button type="button" onclick="closeBarcodeModal()" class="w-full py-2.5 rounded-2xl bg-stone-100 text-stone-700 font-bold text-xs hover:bg-stone-200 transition">
                        關閉放大視窗
                    </button>
                </div>
            </div>
        </div>

        <!-- ✏️ 自訂成員名稱 Modal -->
        <div id="member-names-modal" class="hidden fixed inset-0 z-50 bg-black/85 flex items-center justify-center p-4 backdrop-blur-xs" onclick="closeMemberNamesModal()">
            <div class="bg-white rounded-3xl p-5 sm:p-6 max-w-md w-full space-y-4 shadow-2xl border-4 border-amber-400 relative" onclick="event.stopPropagation()">
                <div class="flex items-center justify-between border-b pb-2.5">
                    <div class="flex items-center gap-2 text-amber-900 font-black text-sm">
                        <span class="text-base">✏️</span>
                        <span>自訂 4 位成員分帳稱號 / 姓名</span>
                    </div>
                    <button type="button" onclick="closeMemberNamesModal()" class="text-stone-400 hover:text-stone-600 text-lg font-bold">✕</button>
                </div>
                <p class="text-xs text-stone-500 leading-relaxed">
                    您可以自由修改每位成員在分帳看板中顯示的稱呼或姓名，修改後將即時同步更新至結算卡片、墊付選單與匯款指引！
                </p>

                <div class="space-y-3 text-left">
                    <div>
                        <label class="text-xs font-bold text-stone-700 block mb-1 flex items-center gap-1.5">
                            <span>🌸</span> <span>第 1 位成員 (原阿純)：</span>
                        </label>
                        <input type="text" id="member-input-achun" class="w-full bg-stone-50 border border-stone-200 focus:bg-white focus:border-amber-400 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none transition" placeholder="例如：首席導遊 阿純">
                    </div>
                    <div>
                        <label class="text-xs font-bold text-stone-700 block mb-1 flex items-center gap-1.5">
                            <span>🐻</span> <span>第 2 位成員 (原阿嚕)：</span>
                        </label>
                        <input type="text" id="member-input-alu" class="w-full bg-stone-50 border border-stone-200 focus:bg-white focus:border-amber-400 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none transition" placeholder="例如：總務大臣 阿嚕">
                    </div>
                    <div>
                        <label class="text-xs font-bold text-stone-700 block mb-1 flex items-center gap-1.5">
                            <span>🌼</span> <span>第 3 位成員 (原阿姨)：</span>
                        </label>
                        <input type="text" id="member-input-ayee" class="w-full bg-stone-50 border border-stone-200 focus:bg-white focus:border-amber-400 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none transition" placeholder="例如：美食評鑑官 阿姨">
                    </div>
                    <div>
                        <label class="text-xs font-bold text-stone-700 block mb-1 flex items-center gap-1.5">
                            <span>🎩</span> <span>第 4 位成員 (原姨丈)：</span>
                        </label>
                        <input type="text" id="member-input-yijhang" class="w-full bg-stone-50 border border-stone-200 focus:bg-white focus:border-amber-400 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none transition" placeholder="例如：榮譽總指揮 姨丈">
                    </div>
                </div>

                <div class="flex items-center justify-between pt-2 border-t border-stone-100 gap-2">
                    <button type="button" onclick="resetMemberNamesToSchemeA()" class="px-3 py-2 rounded-xl bg-stone-100 hover:bg-stone-200 text-stone-600 font-bold text-xs transition">
                        🔄 恢復方案A職責
                    </button>
                    <div class="flex items-center gap-2">
                        <button type="button" onclick="closeMemberNamesModal()" class="px-3 py-2 rounded-xl border border-stone-200 text-stone-500 font-bold text-xs hover:bg-stone-50 transition">
                            取消
                        </button>
                        <button type="button" onclick="saveCustomMemberNames()" class="px-4 py-2 rounded-xl bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-700 hover:to-amber-800 text-white font-black text-xs shadow-md transition active:scale-95">
                            💾 儲存並套用
                        </button>
                    </div>
                </div>
            </div>
        </div>

</body>
</html>'''

    output_path = os.path.join(BASE_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"🗺️ 九州手繪地圖版旅行儀表板建立成功：{output_path}")

if __name__ == '__main__':
    build()
