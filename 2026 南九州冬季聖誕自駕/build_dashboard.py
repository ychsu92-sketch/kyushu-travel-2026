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
    total_spent_twd = expense_sum.get('total_spent_twd', 71250)
    per_person_avg = expense_sum.get('per_person_avg_twd', 17812.5)

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
                <div class="w-10 h-10 sm:w-11 sm:h-11 rounded-2xl shrink-0 bg-white border border-purple-200 flex items-center justify-center p-1 shadow-md shadow-purple-100 overflow-hidden">
                    <img src="./family_logo.png" alt="HSU Logo" class="w-full h-full object-contain">
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
            <button onclick="openTab('bookings')" id="tab-btn-bookings" class="xmas-tab-btn w-full sm:flex-1 min-w-0 px-1 py-2 sm:px-3 text-[11px] sm:text-xs">
                <span>📌</span> 預約
            </button>
            <button onclick="openTab('stays')" id="tab-btn-stays" class="xmas-tab-btn w-full sm:flex-1 min-w-0 px-1 py-2 sm:px-3 text-[11px] sm:text-xs">
                <span>🏡</span> 住宿
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

                        <!-- 今日美饌速查快捷列 -->
                        <div class="mt-4 pt-3.5 border-t border-red-100 flex flex-wrap items-center justify-between gap-2 bg-gradient-to-r from-amber-50/70 via-orange-50/50 to-purple-50/60 p-3 rounded-2xl border border-orange-200/70">
                            <div class="flex flex-wrap items-center gap-1.5 text-xs font-bold">
                                <span class="text-stone-600 text-[11px] font-black">🍽️ 今日美饌速覽：</span>
                                <button type="button" onclick="scrollToMeal('breakfast')" class="px-2.5 py-1 rounded-xl bg-white hover:bg-amber-100 text-amber-900 border border-amber-200 shadow-xs transition text-[11px]">🌅 早餐 3 選</button>
                                <button type="button" onclick="scrollToMeal('lunch')" class="px-2.5 py-1 rounded-xl bg-white hover:bg-orange-100 text-orange-900 border border-orange-200 shadow-xs transition text-[11px]">☀️ 午餐 3 選</button>
                                <button type="button" onclick="scrollToMeal('dinner')" class="px-2.5 py-1 rounded-xl bg-white hover:bg-rose-100 text-rose-900 border border-rose-200 shadow-xs transition text-[11px]">🌙 晚餐 3 選</button>
                                <button type="button" onclick="scrollToMeal('latenight')" id="quick-jump-latenight" class="px-2.5 py-1 rounded-xl bg-purple-600 hover:bg-purple-700 text-white shadow-xs transition text-[11px] font-black flex items-center gap-1">
                                    <span>🍸</span> 宵夜＆酒吧 3 選 ✨
                                </button>
                            </div>
                            <button type="button" onclick="openTab('restaurants')" class="px-3 py-1 rounded-xl bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-700 hover:to-amber-700 text-white font-black text-[11px] shadow-sm transition flex items-center gap-1">
                                <span>🍱</span> 前往 81 家美食總表 ↗
                            </button>
                        </div>

                        <!-- 臨時起意加點按鈕與抽屜 -->
                        <div class="mt-5 flex items-center justify-between pb-2 border-b border-stone-100">
                            <span class="text-xs font-black text-stone-700 flex items-center gap-1.5">
                                <span>⏱️</span> 行程時間軸
                            </span>
                            <button type="button" onclick="toggleCustomStopDrawer()" class="px-3 py-1.5 rounded-2xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-700 hover:to-rose-700 text-white font-black text-xs flex items-center gap-1.5 shadow-sm transition">
                                <span>➕</span> 臨時起意加點 / 順遊導航
                            </button>
                        </div>

                        <!-- 臨時加點表單抽屜 -->
                        <div id="custom-stop-form-drawer" class="hidden mt-3 bg-gradient-to-br from-amber-50 to-orange-50/50 p-4 rounded-2xl border-2 border-amber-300 space-y-3 text-xs shadow-sm">
                            <div class="flex items-center justify-between pb-1 border-b border-amber-200">
                                <span class="font-black text-amber-900 text-xs flex items-center gap-1">
                                    <span>✨</span> 臨時起意加點小便利貼 (自動生成 Google Maps 導航按鈕)
                                </span>
                                <button type="button" onclick="toggleCustomStopDrawer()" class="text-stone-400 hover:text-stone-600 text-xs font-bold">✕ 關閉</button>
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
                                    <button type="button" onclick="toggleCustomStopDrawer()" class="px-3 py-1.5 rounded-xl bg-stone-100 hover:bg-stone-200 text-stone-600 font-bold text-xs transition">取消</button>
                                    <button type="submit" class="px-4 py-1.5 rounded-xl bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 text-white font-black text-xs shadow-sm transition flex items-center gap-1">
                                        <span>➕</span> 加入今日行程並建立導航
                                    </button>
                                </div>
                            </form>
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
                                <path id="route-path-1" class="day-route-path transition-all duration-300" data-day="1" d="M 430 375 L 325 390" fill="none" stroke="#2563eb" stroke-width="4" stroke-dasharray="7 4" stroke-linecap="round"/>
                                <!-- Day 2: 熊本辛島町 (325 390) ➔ 草千里 (475 345) ➔ 大觀峰 (495 275) ➔ 黑川溫泉 (545 250) -->
                                <path id="route-path-2" class="day-route-path transition-all duration-300" data-day="2" d="M 325 390 Q 400 370, 475 345 T 495 275 T 545 250" fill="none" stroke="#dc2626" stroke-width="4.5" stroke-dasharray="8 4" stroke-linecap="round"/>
                                <!-- Day 3: 黑川溫泉 (545 250) ➔ 上色見 (505 400) ➔ 高千穗 (570 415) ➔ 宮崎海邊 (675 535) -->
                                <path id="route-path-3" class="day-route-path transition-all duration-300" data-day="3" d="M 545 250 Q 520 330, 505 400 T 570 415 Q 630 480, 675 535" fill="none" stroke="#7c3aed" stroke-width="4.5" stroke-dasharray="8 4" stroke-linecap="round"/>
                                <!-- Day 4: 宮崎 (675 535) ➔ 青島 (685 595) ➔ 摩艾 (675 645) ➔ 鵜戶神宮 (670 695) ➔ 鹿兒島 (365 685) -->
                                <path id="route-path-4" class="day-route-path transition-all duration-300" data-day="4" d="M 675 535 L 685 595 L 675 645 L 670 695 Q 520 720, 365 685" fill="none" stroke="#059669" stroke-width="4.5" stroke-dasharray="8 4" stroke-linecap="round"/>
                                <!-- Day 5: 鹿兒島 (365 685) ➔ 櫻島渡輪 (455 655) ➔ 仙巖園 (375 635) ➔ 天文館 (365 685) -->
                                <path id="route-path-5" class="day-route-path transition-all duration-300" data-day="5" d="M 365 685 Q 410 670, 455 655 Q 415 645, 375 635 L 365 685" fill="none" stroke="#ea580c" stroke-width="4.5" stroke-dasharray="6 3" stroke-linecap="round"/>
                                <!-- Day 6: 鹿兒島 (365 685) ➔ 霧島神宮 (470 570) ➔ 人吉鰻魚 (425 490) ➔ 熊本辛島町 (355 410) -->
                                <path id="route-path-6" class="day-route-path transition-all duration-300" data-day="6" d="M 365 685 Q 390 630, 470 570 Q 445 525, 425 490 Q 380 450, 355 410" fill="none" stroke="#d97706" stroke-width="4.5" stroke-dasharray="8 4" stroke-linecap="round"/>
                                <!-- Day 7: 熊本辛島町 (355 410) ➔ 熊本城 (345 340) ➔ 水前寺成趣園 (395 420) ➔ 熊本空港 (430 375) -->
                                <path id="route-path-7" class="day-route-path transition-all duration-300" data-day="7" d="M 355 410 L 345 340 L 395 420 L 430 375" fill="none" stroke="#be123c" stroke-width="4.5" stroke-dasharray="7 4" stroke-linecap="round"/>
                            </g>

                            <g id="map-pins-group"></g>
                        </svg>

                        <div class="absolute bottom-3 left-4 bg-white/90 backdrop-blur-sm p-3 rounded-2xl border border-stone-200 text-[11px] font-bold text-stone-600 space-y-1 shadow-sm pointer-events-none">
                            <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-red-600"></span> 🔴 熊本 / 黑川溫泉</div>
                            <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-purple-600"></span> 🟣 高千穗 / 宮崎日南</div>
                            <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span> 🟢 鹿兒島 / 櫻島火山</div>
                            <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> 🟡 霧島神宮 / 人吉鰻魚</div>
                            
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
                        <div class="flex items-center gap-2">
                            <span class="cute-pill bg-amber-100 text-amber-700">✨ 4人小家庭分帳</span>
                            <span class="text-xs text-stone-400">（阿純、阿嚕、阿姨、姨丈）</span>
                        </div>
                        <h3 class="text-xl font-black text-stone-800 mt-1">👛 旅費代墊與應付分攤結算看板</h3>
                        <p class="text-xs text-stone-500 mt-0.5">即時記帳自動分攤，支援網頁直接記帳與 Google 試算表雲端同步！</p>
                    </div>
                    <div class="bg-gradient-to-tr from-amber-100 to-amber-200/70 border border-amber-300 rounded-3xl px-5 py-3 text-right shadow-sm">
                        <div class="text-xs text-amber-800 font-bold">目前累計已記帳總花費</div>
                        <div class="text-2xl font-black text-stone-800 font-mono" id="cost-total-amount">NT$ 71,250</div>
                        <div class="text-[11px] text-stone-600" id="cost-per-person">平均每人應付 NT$ 17,813</div>
                    </div>
                </div>

                <!-- 4人個人結算卡片 (動態更新) -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="members-settlement-cards"></div>

                <!-- 平帳匯款小指引 (動態計算) -->
                <div class="sticky-note p-4 text-xs text-stone-800 leading-relaxed flex items-start gap-3" id="settlement-guide-box"></div>

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
                                    <option value="阿純">🌸 阿純 先墊付</option>
                                    <option value="阿嚕">🐻 阿嚕 先墊付</option>
                                    <option value="阿姨">🌼 阿姨 先墊付</option>
                                    <option value="姨丈">🎩 姨丈 先墊付</option>
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
                            <div class="flex items-center gap-3 text-xs font-bold text-stone-700">
                                <span class="text-stone-500">分攤成員：</span>
                                <label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" id="split-achun" checked class="rounded text-amber-600"> 阿純</label>
                                <label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" id="split-alu" checked class="rounded text-amber-600"> 阿嚕</label>
                                <label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" id="split-aunt" checked class="rounded text-amber-600"> 阿姨</label>
                                <label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" id="split-uncle" checked class="rounded text-amber-600"> 姨丈</label>
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
        <!-- TAB 4: 預約小便條 -->
        <section id="tab-content-bookings" class="tab-content hidden space-y-6">
            <div class="cute-card p-6 relative border-2 border-amber-200 space-y-6">
                <div class="washi-tape washi-tape-gold"></div>

                <div class="flex items-center justify-between pb-4 border-b-2 border-stone-100">
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

        <!-- TAB 5: 旅宿與機票 -->
        <section id="tab-content-stays" class="tab-content hidden space-y-6">
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
                            <span class="font-bold text-sky-600">機票費用：NT$ 33,150</span>
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

            <div>
                <h3 class="text-lg font-black text-stone-800 mb-3 flex items-center gap-2">
                    <span>🏡</span> 6 晚旅宿安排 (已確認訂房)
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="stays-grid"></div>
            </div>
        </section>

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
                        <span class="text-stone-500 text-[11px] font-black">📍 地區篩選：</span>
                        <button type="button" onclick="filterCoupons('all')" id="cfilter-all" class="cfilter-btn px-3 py-1 rounded-full bg-red-600 text-white shadow-xs transition text-[11px]">全部優惠 (6)</button>
                        <button type="button" onclick="filterCoupons('kumamoto')" id="cfilter-kumamoto" class="cfilter-btn px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">📍 熊本市區</button>
                        <button type="button" onclick="filterCoupons('kagoshima')" id="cfilter-kagoshima" class="cfilter-btn px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">📍 鹿兒島市區</button>
                        <button type="button" onclick="filterCoupons('miyazaki')" id="cfilter-miyazaki" class="cfilter-btn px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">📍 宮崎・日南</button>
                        <button type="button" onclick="filterCoupons('chain')" id="cfilter-chain" class="cfilter-btn px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]">🇯🇵 全九州連鎖免稅</button>
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
                renderAccommodations();
                initChecklist();
                initHandDrawnMap();
                initCosts();
                renderRestaurants();
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
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.xmas-tab-btn').forEach(btn => btn.classList.remove('active'));

            const targetContent = document.getElementById('tab-content-' + tabName);
            const targetBtn = document.getElementById('tab-btn-' + tabName);

            if (targetContent) targetContent.classList.remove('hidden');
            if (targetBtn) targetBtn.classList.add('active');
            if (tabName === 'costs') initCosts();
                renderRestaurants();
            if (tabName === 'restaurants') renderRestaurants();
            if (tabName === 'tools') renderCoupons();
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

            const container = document.getElementById('timeline-container');
            if (!container) return;
            container.innerHTML = '';
            const quickLinks = [];

            // 1. 原定計畫時間軸項目
            dayPlan.timeline.forEach(item => {{
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

                itemDiv.innerHTML = `
                    <div class="absolute -left-[31px] top-1.5 w-4 h-4 rounded-full bg-white border-2 border-red-500 flex items-center justify-center shadow-sm">
                        <div class="w-1.5 h-1.5 rounded-full bg-red-600"></div>
                    </div>
                    <div class="bg-white border-2 border-stone-200/80 rounded-2xl p-4 transition space-y-1.5 shadow-sm hover:border-red-300 hover:shadow-md">
                        <div class="flex flex-wrap items-center justify-between gap-2">
                            <span class="text-xs font-mono font-black text-red-600 bg-red-50 px-2.5 py-0.5 rounded-full border border-red-100">${{item.time}}</span>
                            <span class="cute-pill ${{tagClass}}">
                                <span>${{icon}}</span> ${{item.category.toUpperCase()}}
                            </span>
                        </div>
                        <h5 class="text-sm font-black text-stone-800 flex items-center justify-between">
                            <span>${{item.title}}</span>
                            <a href="${{mapSearchUrl}}" target="_blank" class="px-2 py-0.5 rounded-lg bg-sky-50 text-sky-600 hover:bg-sky-100 font-bold text-xs flex items-center gap-0.5 transition" title="在 Google Maps 查看">
                                <span>導航</span> ↗
                            </a>
                        </h5>
                        <p class="text-xs text-stone-600 leading-relaxed font-medium">${{item.desc}}</p>
                        ${{item.tips ? `
                            <div class="text-[11px] text-amber-800 bg-amber-50 border border-amber-200 rounded-xl p-2.5 flex items-start gap-1.5 mt-2">
                                <span>💡</span>
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
                const div = document.createElement('div');
                div.className = 'cute-card p-5 relative border-2 border-stone-200 space-y-3';
                div.innerHTML = `
                    <div class="flex items-start justify-between">
                        <div>
                            <span class="cute-pill bg-red-100 text-red-700">${{acc.night}}</span>
                            <h4 class="text-sm font-black text-stone-800 mt-1.5">${{acc.hotel_name}}</h4>
                            <p class="text-xs text-stone-400">${{acc.city}}</p>
                        </div>
                        <a href="${{acc.google_maps_url}}" target="_blank" class="px-2.5 py-1 rounded-full bg-sky-100 text-sky-700 hover:bg-sky-200 text-xs font-bold transition">
                            地圖 ↗
                        </a>
                    </div>
                    <div class="bg-stone-50 rounded-2xl p-3 space-y-1 text-xs border border-stone-200 font-medium">
                        <div class="flex justify-between"><span class="text-stone-400">房型配置：</span><span class="text-stone-800 font-bold">${{acc.room_type}}</span></div>
                        <div class="flex justify-between"><span class="text-stone-400">入住/退房：</span><span class="text-stone-600">${{acc.check_in.split(' ')[1] || acc.check_in}} / ${{acc.check_out.split(' ')[1] || acc.check_out}}</span></div>
                        <div class="flex justify-between"><span class="text-stone-400">訂房費用：</span><span class="text-emerald-700 font-bold">${{acc.booking_platform}}</span></div>
                    </div>
                    <div class="text-[11px] text-stone-500 leading-relaxed italic">
                        備註：${{acc.notes}}
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
            currentDayRoute = day;
            const routesGroup = document.getElementById('map-routes-group');
            if (routesGroup) routesGroup.style.display = 'block';
            showRoutes = true;

            const btnRoutes = document.getElementById('map-btn-routes');
            if (btnRoutes) {{
                btnRoutes.textContent = '🚗 7天全動線';
                btnRoutes.className = 'px-2.5 py-1 rounded-full bg-amber-600 text-white shadow-sm transition';
            }}

            // Update route buttons UI
            ['all', 1, 2, 3, 4, 5, 6, 7].forEach(d => {{
                const btn = document.getElementById(`btn-route-${{d}}`);
                if (btn) {{
                    if (String(d) === String(day)) {{
                        btn.className = 'btn-day-route px-3 py-1 rounded-full bg-amber-600 text-white shadow-xs transition text-[11px] font-black scale-105';
                    }} else {{
                        btn.className = 'btn-day-route px-2.5 py-1 rounded-full bg-white border border-stone-200 text-stone-600 hover:bg-amber-100 transition text-[11px]';
                    }}
                }}
            }});

            const banner = document.getElementById('route-summary-banner');
            const summaryText = document.getElementById('route-summary-text');
            const indicatorText = document.getElementById('route-indicator-text');

            if (day === 'all') {{
                document.querySelectorAll('.day-route-path').forEach(p => {{
                    p.style.opacity = '1';
                    p.style.strokeWidth = p.getAttribute('data-day') === '2' ? '4.5' : '4';
                    p.style.filter = 'none';
                    p.classList.remove('route-flowing');
                }});
                if (banner) banner.classList.add('hidden');
                if (indicatorText) indicatorText.textContent = '已顯示全 7 天自駕動線';
                renderMapPins('all');
            }} else {{
                const info = DAY_ROUTES_DATA[day];
                document.querySelectorAll('.day-route-path').forEach(p => {{
                    if (p.getAttribute('data-day') === String(day)) {{
                        p.style.opacity = '1';
                        p.style.strokeWidth = '6.5';
                        p.style.stroke = '#dc2626';
                        p.style.filter = 'drop-shadow(0 0 6px rgba(220, 38, 38, 0.7))';
                        p.classList.add('route-flowing');
                    }} else {{
                        p.style.opacity = '0.12';
                        p.style.strokeWidth = '2';
                        p.style.filter = 'none';
                        p.classList.remove('route-flowing');
                    }}
                }});

                if (banner && summaryText && info) {{
                    banner.classList.remove('hidden');
                    summaryText.innerHTML = `<span>🚗</span> <span><strong>${{info.title}}：</strong>${{info.desc}}</span>`;
                }}
                if (indicatorText && info) {{
                    indicatorText.textContent = `當前：${{info.title}}`;
                }}

                // Highlight only day landmarks
                if (info && info.landmarks) {{
                    const pinsGroup = document.getElementById('map-pins-group');
                    if (pinsGroup) {{
                        document.querySelectorAll('.map-pin').forEach(pin => {{
                            const pinId = pin.id.replace('pin-', '');
                            if (info.landmarks.includes(pinId)) {{
                                pin.style.opacity = '1';
                                pin.style.filter = 'drop-shadow(0 0 4px rgba(220, 38, 38, 0.5))';
                            }} else {{
                                pin.style.opacity = '0.35';
                                pin.style.filter = 'none';
                            }}
                        }});
                    }}
                }}
            }}
        }}

        // ======================= 優惠券與折價券資料系統 =======================
        const COUPONS_DATA = [
            {{
                id: "c_donki",
                title: "驚安殿堂 唐吉訶德 (Don Quijote)",
                title_jp: "ドン・キホーテ 免税＋特別優待",
                tag: "免稅 10% + 最高折 7%",
                discount: "10% 免稅 + 最高 7% 現折",
                condition: "滿 10,000 日圓折 5% ｜ 滿 30,000 日圓折 7%",
                barcode: "9900123456789",
                area: "kumamoto_kagoshima",
                area_tag: "kumamoto",
                area_name: "熊本市區・鹿兒島市區",
                stores: "熊本下通店、鹿兒島天文館店",
                google_maps: "https://www.google.com/maps/search/?api=1&query=ドン・キホーテ+熊本下通店",
                expiry: "2026/12/31 止",
                note: "結帳前務必主動出示護照與本條碼讓店員掃描"
            }},
            {{
                id: "c_bic",
                title: "Bic Camera / Kojima 電器綜合免稅",
                title_jp: "ビックカメラ / コジマ 特別割引",
                tag: "免稅 10% + 7% / 5% 折扣",
                discount: "10% 免稅 + 電器相機 7% / 藥妝 5%",
                condition: "相機電器玩具享額外 7% ｜ 保溫杯藥妝享額外 5%",
                barcode: "9900987654321",
                area: "kumamoto_kagoshima",
                area_tag: "kagoshima",
                area_name: "熊本・鹿兒島市區",
                stores: "Kojima x BicCamera 熊本店、Bic Camera 鹿兒島中央站店",
                google_maps: "https://www.google.com/maps/search/?api=1&query=ビックカメラ+鹿児島中央駅店",
                expiry: "2026/12/31 止",
                note: "出示手機條碼直接折抵，可刷台灣信用卡"
            }},
            {{
                id: "c_matsukiyo",
                title: "松本清藥妝 (Matsumoto Kiyoshi)",
                title_jp: "マツモトキヨシ 免税クーポン",
                tag: "免稅 10% + 最高折 7%",
                discount: "10% 免稅 + 滿額 3% / 5% / 7%",
                condition: "滿 1萬折 3% ｜ 滿 3萬折 5% ｜ 滿 5萬折 7%",
                barcode: "4901234567890",
                area: "all_kyushu",
                area_tag: "chain",
                area_name: "熊本・宮崎・鹿兒島連鎖",
                stores: "熊本下通店、宮崎橘通店、鹿兒島天文館店",
                google_maps: "https://www.google.com/maps/search/?api=1&query=マツモトキヨシ+熊本下通",
                expiry: "2026/12/31 止",
                note: "九州各大熱門商店街均有門市，買合利他命、面膜超划算"
            }},
            {{
                id: "c_daikoku",
                title: "大國藥妝 / 杉藥局 (Daikoku Drug)",
                title_jp: "ダイコクドラッグ 免税特別割引",
                tag: "免稅 10% + 最高折 7%",
                discount: "10% 免稅 + 現折 3% ~ 7%",
                condition: "熱門零食、常備感冒藥、痠痛貼布滿額現折",
                barcode: "4909876543210",
                area: "all_kyushu",
                area_tag: "chain",
                area_name: "熊本市區・鹿兒島市區",
                stores: "熊本新市街店、鹿兒島天文館店",
                google_maps: "https://www.google.com/maps/search/?api=1&query=ダイコクドラッグ+熊本",
                expiry: "2026/12/31 止",
                note: "常有店員講中文，價格透明親民"
            }},
            {{
                id: "c_tsuruya",
                title: "熊本鶴屋百貨 外國旅客 5% 貴賓券",
                title_jp: "鶴屋百貨店 外国人特別優待",
                tag: "外國旅客 5% 折扣 + 免稅",
                discount: "全館 5% 折扣 + 10% 免稅退稅",
                condition: "憑外國護照至本館退稅櫃台出示即可領取貴賓券",
                barcode: "2978849102401",
                area: "kumamoto",
                area_tag: "kumamoto",
                area_name: "熊本市區辛島町/通町筋",
                stores: "鶴屋百貨本館 (東館 1F 熊本熊廣場旁)",
                google_maps: "https://www.google.com/maps/search/?api=1&query=鶴屋百貨店+熊本",
                expiry: "2026/12/31 止",
                note: "買九州頂級銘菓、熊本熊限定商品與專櫃化妝品必備"
            }},
            {{
                id: "c_senganen",
                title: "仙巖園 ＆ 櫻島渡輪 觀光套票指引",
                title_jp: "仙巌園・桜島フェリー 共通チケット",
                tag: "套票優惠 85 折起",
                discount: "仙巖園＋尚古集成館門票優惠 ｜ 渡輪 CUTE 券",
                condition: "出示悠遊卡或護照至售票處購買共通券即享折扣",
                barcode: "8801234567891",
                area: "kagoshima",
                area_tag: "kagoshima",
                area_name: "鹿兒島・櫻島",
                stores: "鹿兒島中央站觀光所、櫻島渡輪碼頭售票口",
                google_maps: "https://www.google.com/maps/search/?api=1&query=仙巌園",
                expiry: "2026/12/31 止",
                note: "持 Welcome Cute 一日券可無限次搭乘櫻島渡輪與鹿兒島市營巴士"
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
            ['all', 'kumamoto', 'kagoshima', 'miyazaki', 'chain'].forEach(a => {{
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
                if (currentCouponFilter === 'chain' && (c.area_tag === 'chain' || c.area === 'all_kyushu')) return true;
                return c.area.includes(currentCouponFilter) || c.area_tag === currentCouponFilter;
            }});

            list.forEach(c => {{
                const card = document.createElement('div');
                card.className = 'bg-white rounded-3xl p-5 border-2 border-red-200 hover:border-red-400 space-y-3.5 shadow-sm hover:shadow-md transition flex flex-col justify-between';

                const barcodeSvg = renderBarcodeSvg(c.barcode, 200, 45);
                const qrSvg = renderQrSvg(c.barcode, 16);

                card.innerHTML = `
                    <div class="space-y-2.5">
                        <div class="flex items-center justify-between gap-1 flex-wrap">
                            <span class="cute-pill bg-red-100 text-red-700 font-black">${{c.tag}}</span>
                            <span class="text-[11px] font-bold text-stone-400">📍 ${{c.area_name}}</span>
                        </div>

                        <div>
                            <h4 class="text-sm font-black text-stone-800">${{c.title}}</h4>
                            <div class="text-[11px] text-stone-400 italic">${{c.title_jp}}</div>
                        </div>

                        <div class="bg-gradient-to-r from-red-50 to-orange-50 border border-red-200 rounded-2xl p-2.5 space-y-1 text-xs">
                            <div class="font-black text-red-700 flex items-center gap-1 text-[11px]">
                                <span>🎁 優惠詳情：</span>
                                <span>${{c.discount}}</span>
                            </div>
                            <div class="text-[11px] text-stone-600 font-bold">${{c.condition}}</div>
                        </div>

                        <!-- 條碼與 QRcode 掃描展示區 -->
                        <div class="p-3 bg-stone-50 rounded-2xl border-2 border-stone-200 space-y-2 text-center">
                            <div class="flex items-center justify-between gap-2">
                                <div class="flex-1 bg-white p-2 rounded-xl border border-stone-200 cursor-pointer" onclick="openBarcodeModal('${{c.id}}')" title="點擊放大條碼">
                                    ${{barcodeSvg}}
                                    <div class="font-mono text-xs font-bold text-stone-700 tracking-wider mt-1">${{c.barcode}}</div>
                                </div>
                                <div class="bg-white p-1.5 rounded-xl border border-stone-200 cursor-pointer shrink-0" onclick="openBarcodeModal('${{c.id}}')" title="點擊放大二維碼">
                                    ${{qrSvg}}
                                </div>
                            </div>
                            <div class="text-[10px] text-stone-400 font-medium">💡 結帳時點擊「條碼」可直接全螢幕放大讓店員掃描</div>
                        </div>

                        <div class="text-[11px] text-stone-500 bg-stone-50 p-2 rounded-xl border border-stone-100">
                            <strong>適用門市：</strong>${{c.stores}}
                        </div>
                    </div>

                    <div class="pt-2 border-t border-stone-100 flex items-center gap-2">
                        <button type="button" onclick="openBarcodeModal('${{c.id}}')" class="flex-1 py-2 px-3 rounded-xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-700 hover:to-rose-700 text-white font-black text-xs flex items-center justify-center gap-1 shadow-sm transition">
                            <span>🔍</span> 放大條碼供掃描
                        </button>
                        <a href="${{c.google_maps}}" target="_blank" class="py-2 px-3 rounded-xl bg-sky-50 hover:bg-sky-100 text-sky-700 border border-sky-200 font-bold text-xs flex items-center justify-center gap-1 transition" title="Google Maps 導航">
                            <span>🗺️</span> 導航
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

            if (titleEl) titleEl.textContent = c.title;
            if (barcodeSvgEl) barcodeSvgEl.innerHTML = renderBarcodeSvg(c.barcode, 260, 65);
            if (barcodeNumEl) barcodeNumEl.textContent = c.barcode;
            if (qrSvgEl) qrSvgEl.innerHTML = renderQrSvg(c.barcode, 24);
            if (condEl) condEl.textContent = `${{c.discount}} ｜ ${{c.condition}} ｜ 有效期至 ${{c.expiry}}`;

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
                    // 統一固定高度 h-[152px]，box-border 與 overflow-hidden 雙重鎖死，嚴格對齊且絕不超框
                    row.className = 'bg-white p-3 rounded-2xl border border-stone-200/90 shadow-2xs hover:shadow-md hover:border-orange-300 transition-all flex flex-col justify-between h-[152px] min-h-[152px] max-h-[152px] overflow-hidden box-border w-full';
                    
                    // 1. 精簡訂位標籤為 2~4 字，確保絕不溢出到隔壁欄位
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

                    // 2. 乾淨純粹的店名 (過濾所有括號備註、宣傳詞、日文副標題與菜品後綴)
                    let cleanName = (opt.name || '').trim();
                    cleanName = cleanName.replace(/\\s*[\\(（][^()（）]*[\\)）]/g, '').trim();
                    cleanName = cleanName.replace(/\\s*(炭焙手沖咖啡|手作泡芙與點心|晨光日式朝食|和洋朝食百匯|特選咖哩與在地小酌|夜間酒餚居酒時光|天然溫泉和洋朝食|展望赤牛漢堡排|元祖流水麵)$/g, '').trim();

                    // 3. 價格精簡乾淨
                    let cleanPrice = (opt.price || '').split('~')[0].split('/')[0].trim();
                    if (cleanPrice.includes('住宿內含')) cleanPrice = '住宿內含';
                    if (cleanPrice.includes('機票內含') || cleanPrice.includes('機票資格')) cleanPrice = '機票內含';

                    // 4. 地點精簡
                    const cleanArea = (opt.area || '').split(' ')[0].trim();

                    row.innerHTML = `
                        <div class="space-y-1.5 min-w-0">
                            <!-- 頂部獨立標籤列 (嚴格控制寬度，絕不溢出) -->
                            <div class="flex items-center justify-between gap-1 min-w-0">
                                <span class="inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-md border ${{badgeClass}} font-bold shrink-0 shadow-2xs">
                                    <span>${{badgeIcon}}</span>
                                    <span>${{badgeLabel}}</span>
                                </span>
                                ${{cleanArea ? `<span class="text-[10px] text-stone-400 font-bold truncate max-w-[65px] shrink-0">📍 ${{cleanArea}}</span>` : ''}}
                            </div>

                            <!-- 乾淨純粹店名 (單行截斷，字體清爽易讀) -->
                            <h5 class="font-black text-stone-800 text-xs sm:text-[13px] leading-snug tracking-tight hover:text-orange-600 transition cursor-pointer truncate" onclick="jumpToRestaurant('${{opt.id}}')" title="${{opt.name}}">
                                ${{cleanName}}
                            </h5>

                            <!-- 必吃特色推薦小卡 (招牌菜獨立呈現) -->
                            <div class="bg-stone-50 rounded-lg px-2 py-1 text-[11px] text-stone-600 font-medium line-clamp-1 border border-stone-100">
                                🍴 <span class="text-stone-700 font-bold">${{opt.must_eat}}</span>
                            </div>
                        </div>

                        <!-- 底部價格與操作區 (按鈕防超框專用結構：min-w-0 flex-1 彈性空間 + shrink-0 按鈕組) -->
                        <div class="flex items-center justify-between pt-1.5 border-t border-stone-100 text-[11px] gap-1.5 min-w-0 w-full mt-auto">
                            <span class="font-mono text-stone-800 font-black tracking-tight text-xs truncate min-w-0 flex-1">
                                ${{cleanPrice}}
                            </span>
                            <div class="flex items-center gap-1 shrink-0">
                                <button type="button" onclick="jumpToRestaurant('${{opt.id}}')" class="whitespace-nowrap px-2 py-0.5 rounded-md bg-orange-50 hover:bg-orange-100 text-orange-700 border border-orange-200 text-[10px] font-bold transition active:scale-95 shadow-2xs">
                                    攻略 ↗
                                </button>
                                <a href="https://www.google.com/maps/search/?api=1&query=${{encodeURIComponent(opt.name + ' ' + (opt.area || ''))}}" target="_blank" class="w-5 h-5 rounded-md bg-sky-50 hover:bg-sky-100 text-sky-700 border border-sky-200 flex items-center justify-center text-[10px] font-bold transition active:scale-95 shadow-2xs shrink-0" title="Google 地圖導航">
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
                activePin.parentNode.appendChild(activePin);
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
        const BASE_SETTLEMENT = {{
            '阿純': {{ basePaid: 47775, baseShould: 20575, color: 'text-red-600', icon: '🌸', note: '代墊華航機票 NT$ 33,150 ＋ 黑川山彥溫泉旅館 (含早餐)。' }},
            '阿嚕': {{ basePaid: 23475, baseShould: 9525, color: 'text-sky-600', icon: '🐻', note: '代墊熊本 Via Inn、宮崎海景公寓、鹿兒島 Perch 與熊本 AMANEK。' }},
            '阿姨': {{ basePaid: 0, baseShould: 20575, color: 'text-amber-600', icon: '🌼', note: '分攤華航機票 NT$ 11,050 ＋ 各晚特色旅宿。' }},
            '姨丈': {{ basePaid: 0, baseShould: 20575, color: 'text-purple-600', icon: '🎩', note: '分攤華航機票 NT$ 11,050 ＋ 各晚特色旅宿。' }}
        }};

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

            renderCosts();
        }}

        function renderCosts() {{
            const customList = getCustomExpenses();
            let baseTotalSpent = 71250;
            let customSpentTotal = 0;

            const membersCalc = {{
                '阿純': {{ paid: BASE_SETTLEMENT['阿純'].basePaid, should: BASE_SETTLEMENT['阿純'].baseShould }},
                '阿嚕': {{ paid: BASE_SETTLEMENT['阿嚕'].basePaid, should: BASE_SETTLEMENT['阿嚕'].baseShould }},
                '阿姨': {{ paid: BASE_SETTLEMENT['阿姨'].basePaid, should: BASE_SETTLEMENT['阿姨'].baseShould }},
                '姨丈': {{ paid: BASE_SETTLEMENT['姨丈'].basePaid, should: BASE_SETTLEMENT['姨丈'].baseShould }}
            }};

            customList.forEach(item => {{
                const twd = Number(item.amount_twd || 0);
                customSpentTotal += twd;

                if (membersCalc[item.payer]) {{
                    membersCalc[item.payer].paid += twd;
                }}

                const splitMembers = [];
                if (item.achun) splitMembers.push('阿純');
                if (item.alu) splitMembers.push('阿嚕');
                if (item.aunt) splitMembers.push('阿姨');
                if (item.uncle) splitMembers.push('姨丈');

                if (splitMembers.length > 0) {{
                    const share = Math.round(twd / splitMembers.length);
                    splitMembers.forEach(m => {{
                        if (membersCalc[m]) membersCalc[m].should += share;
                    }});
                }}
            }});

            const currentTotalSpent = baseTotalSpent + customSpentTotal;
            const currentPerPerson = Math.round(currentTotalSpent / 4);

            const totalEl = document.getElementById('cost-total-amount');
            if (totalEl) totalEl.textContent = `NT$ ${{currentTotalSpent.toLocaleString()}}`;
            const perEl = document.getElementById('cost-per-person');
            if (perEl) perEl.textContent = `平均每人應付 NT$ ${{currentPerPerson.toLocaleString()}}`;

            const cardsContainer = document.getElementById('members-settlement-cards');
            if (cardsContainer) {{
                cardsContainer.innerHTML = '';
                ['阿純', '阿嚕', '阿姨', '姨丈'].forEach(name => {{
                    const m = membersCalc[name];
                    const cfg = BASE_SETTLEMENT[name];
                    const diff = m.paid - m.should;
                    const isCredit = diff > 0;
                    const isBalanced = diff === 0;

                    const div = document.createElement('div');
                    div.className = 'polaroid-card space-y-3 bg-gradient-to-b from-white to-stone-50/50';
                    div.innerHTML = `
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <span class="text-2xl">${{cfg.icon}}</span>
                                <span class="text-base font-black text-stone-800">${{name}}</span>
                            </div>
                            <span class="cute-pill ${{isCredit ? 'bg-emerald-100 text-emerald-700' : (isBalanced ? 'bg-stone-100 text-stone-600' : 'bg-red-100 text-red-700')}}">
                                ${{isCredit ? '🟢 應收款' : (isBalanced ? '⚪ 平帳' : '🔴 應補款')}}
                            </span>
                        </div>
                        <div class="space-y-1 text-xs">
                            <div class="flex justify-between text-stone-500">
                                <span>累計已墊：</span>
                                <span class="font-bold text-stone-800 font-mono">NT$ ${{m.paid.toLocaleString()}}</span>
                            </div>
                            <div class="flex justify-between text-stone-500">
                                <span>個人應付：</span>
                                <span class="font-mono text-stone-600">NT$ ${{m.should.toLocaleString()}}</span>
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
                        <div class="text-[11px] text-stone-600 bg-white p-2.5 rounded-xl border border-stone-200 leading-relaxed">
                            💡 ${{cfg.note}}
                        </div>
                    `;
                    cardsContainer.appendChild(div);
                }});
            }}

            const guideBox = document.getElementById('settlement-guide-box');
            if (guideBox) {{
                const debtors = [];
                const creditors = [];
                ['阿純', '阿嚕', '阿姨', '姨丈'].forEach(name => {{
                    const diff = membersCalc[name].paid - membersCalc[name].should;
                    if (diff < -5) debtors.push({{ name, amount: Math.abs(diff) }});
                    else if (diff > 5) creditors.push({{ name, amount: diff }});
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
                    <span class="text-xl">💌</span>
                    <div>
                        <strong class="text-sm font-bold text-amber-800">一鍵搞定即時平帳匯款指引：</strong><br>
                        ${{steps.length > 0 ? steps.map((s, idx) => `${{idx + 1}}. ${{s}}。<br>`).join('') : '目前所有成員帳目完全平整，無需匯款！✨'}}<br>
                        ✨ 照著匯款，全家族帳目一秒歸零收支平衡！
                    </div>
                `;
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
                            item.achun ? '純' : '',
                            item.alu ? '嚕' : '',
                            item.aunt ? '姨' : '',
                            item.uncle ? '丈' : ''
                        ].filter(Boolean).join('/');

                        row.innerHTML = `
                            <div class="flex items-center gap-2">
                                <span class="cute-pill bg-amber-100 text-amber-700">${{item.date.split('-').slice(1).join('/')}}</span>
                                <span class="font-bold text-stone-800">${{item.item}}</span>
                                <span class="text-stone-400 text-[11px]">(${{item.category}})</span>
                                ${{item.note ? `<span class="text-stone-400 text-[11px] italic">"${{item.note}}"</span>` : ''}}
                            </div>
                            <div class="flex items-center gap-3">
                                <div class="text-right">
                                    <span class="font-mono font-bold text-stone-800">NT$ ${{Number(item.amount_twd).toLocaleString()}}</span>
                                    <div class="text-[10px] text-stone-400">${{item.payer}} 墊 ｜ 分攤: ${{splitText}}</div>
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
                        <div class="flex items-center gap-2">
                            <span class="${{isChecked ? 'text-emerald-600' : 'text-stone-300'}} text-sm">${{isChecked ? '❄️' : '⚪'}}</span>
                            <span>${{item.item}}</span>
                        </div>
                        ${{item.critical ? '<span class="cute-pill bg-red-100 text-red-700">必帶</span>' : ''}}
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
        <!-- 條碼全螢幕放大 Modal -->
        <div id="barcode-modal" class="hidden fixed inset-0 z-50 bg-black/85 flex items-center justify-center p-4 backdrop-blur-xs" onclick="closeBarcodeModal()">
            <div class="bg-white rounded-3xl p-6 max-w-sm w-full space-y-4 text-center shadow-2xl border-4 border-red-500" onclick="event.stopPropagation()">
                <div class="flex items-center justify-between border-b pb-2">
                    <span class="font-black text-sm text-stone-800" id="modal-coupon-title">優惠券條碼</span>
                    <button onclick="closeBarcodeModal()" class="text-stone-400 hover:text-stone-600 text-base font-bold">✕</button>
                </div>
                <div class="bg-amber-50 text-amber-900 text-xs font-bold p-2.5 rounded-xl border border-amber-200 leading-snug">
                    💡 請將手機螢幕亮度調至最大，直接出示給店員掃描
                </div>
                <div class="p-4 bg-white rounded-2xl border-2 border-stone-300 flex flex-col items-center justify-center space-y-2">
                    <div id="modal-barcode-svg" class="w-full flex justify-center"></div>
                    <div id="modal-barcode-num" class="font-mono font-black text-lg tracking-widest text-stone-900"></div>
                </div>
                <div id="modal-qr-svg" class="flex justify-center p-2 bg-stone-50 rounded-xl border border-stone-200"></div>
                <p class="text-[11px] text-stone-500 font-medium leading-relaxed" id="modal-coupon-condition"></p>
                <button onclick="closeBarcodeModal()" class="w-full py-2.5 rounded-2xl bg-stone-800 text-white font-bold text-xs hover:bg-stone-900 transition">
                    關閉放大視窗
                </button>
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
