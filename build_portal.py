#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
家族旅行手帳大廳 (Family Travel Vault) 與 2.5D 冬日南九州自駕島產生器
用法:
  - 開發與預覽模式 (預設): python3 build_portal.py
    產出 index.html 與 preview.html（載入 portal/*.js 獨立模組，方便即時除錯與預覽）
  - 正式發佈模式: python3 build_portal.py --release
    將 portal/ 下的資料與腳本內嵌至 index.html，並呼叫 obfuscate_and_protect.py 加固保護
"""

import os
import sys
import json
import shutil
import urllib.parse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORTAL_DIR = os.path.join(BASE_DIR, 'portal')


def build_script_block(release_mode: bool) -> str:
    """根據開發或發佈模式，產生外部 <script src> 或內嵌 <script> 區塊"""
    module_files = [
        'env.js',
        'terrain.js',
        'landmarks.js',
        'characters.js',
        'props.js',
        'island.js'
    ]
    if not release_mode:
        tags = [f'    <script src="./portal/{m}"></script>' for m in module_files]
        tags.append("""    <script>
        document.addEventListener('DOMContentLoaded', function() {
            if (window.KyushuIsland && window.KyushuIsland.Portal) {
                window.KyushuIsland.Portal.initPortalIsland('island-canvas-container');
            }
        });
    </script>""")
        return "\n".join(tags)

    # Release 模式：將 JSON 資料與所有 JS 模組合併為單一內嵌 <script>，供混淆器加密保護
    with open(os.path.join(PORTAL_DIR, 'data', 'kyushu_coast.json'), 'r', encoding='utf-8') as f:
        coast_json = f.read().strip()
    with open(os.path.join(PORTAL_DIR, 'data', 'route.json'), 'r', encoding='utf-8') as f:
        route_json = f.read().strip()

    js_chunks = [
        "window.KYUSHU_INLINE_DATA = {",
        f"  coast: {coast_json},",
        f"  route: {route_json}",
        "};"
    ]
    for m in module_files:
        p = os.path.join(PORTAL_DIR, m)
        with open(p, 'r', encoding='utf-8') as f:
            js_chunks.append(f"\n/* === {m} === */\n" + f.read())

    js_chunks.append("""
document.addEventListener('DOMContentLoaded', function() {
    if (window.KyushuIsland && window.KyushuIsland.Portal) {
        window.KyushuIsland.Portal.initPortalIsland('island-canvas-container');
    }
});
""")
    combined_js = "\n".join(js_chunks)
    return f"    <script>\n{combined_js}\n    </script>"


def build_portal(release_mode: bool = False):
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    scripts_html = build_script_block(release_mode)

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#dc2626">
    <title>❄️ 2026 南九州冬日自駕島 ｜ 家族旅行手帳大廳 ✈️</title>
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
    <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&family=Zen+Maru+Gothic:wght@400;500;700;900&display=swap" rel="stylesheet">

    <!-- Three.js r128 與 OrbitControls -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['"Zen Maru Gothic"', '"M PLUS Rounded 1c"', 'system-ui', 'sans-serif'],
                    }},
                    colors: {{
                        cute: {{
                            cream: '#FFFDF9',
                            paper: '#FDFBF7',
                            border: '#F1E9DA',
                            dark: '#3D342B',
                        }}
                    }}
                }}
            }}
        }};
    </script>

    <style>
        body {{
            background-color: #faf7f2;
            background-image:
                radial-gradient(#e5dec9 0.75px, transparent 0.75px),
                radial-gradient(#e5dec9 0.75px, #faf7f2 0.75px);
            background-size: 30px 30px;
            background-position: 0 0, 15px 15px;
            color: #3d342b;
        }}
        .vault-card {{
            border-radius: 1.75rem;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}
        .vault-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.08);
        }}
        .cute-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 800;
        }}
        .washi-tape {{
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%) rotate(-1deg);
            width: 110px;
            height: 24px;
            background: rgba(254, 226, 226, 0.85);
            border-left: 2px dashed rgba(239, 68, 68, 0.3);
            border-right: 2px dashed rgba(239, 68, 68, 0.3);
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            z-index: 10;
        }}

        /* 2.5D 南九州冬日自駕島容器 */
        #island-canvas-container {{
            width: 100%;
            height: 520px;
            position: relative;
            cursor: grab;
            touch-action: none;
            overflow: hidden;
            border-radius: 1.5rem;
        }}
        #island-canvas-container:active {{
            cursor: grabbing;
        }}
        @media (max-width: 640px) {{
            #island-canvas-container {{
                height: min(72vh, 560px);
                min-height: 430px;
                border-radius: 1.1rem;
            }}
            /* 行動版：對話框固定貼齊畫布底部、全寬、字體放大，不再遮擋角色與景點 */
            .island-speech-bubble {{
                left: 8px !important;
                right: 8px !important;
                top: auto !important;
                bottom: 8px;
                transform: none !important;
                max-width: none;
                padding: 10px 14px;
                font-size: 14px;
                border-radius: 16px;
            }}
            .island-speech-bubble::after {{ display: none; }}
            #bubble-speaker-text {{ font-size: 14px !important; line-height: 1.5 !important; }}
            #bubble-speaker-name {{ font-size: 13px !important; }}
            #bubble-spot-tag {{ font-size: 11px !important; }}
            /* 操作按鈕列：單行橫向滑動，節省垂直空間 */
            .island-ctrl-row {{
                flex-wrap: nowrap !important;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none;
                padding-bottom: 2px;
            }}
            .island-ctrl-row::-webkit-scrollbar {{ display: none; }}
            .island-ctrl-row > * {{ flex-shrink: 0; white-space: nowrap; }}
            .island-hint-desktop {{ display: none !important; }}
            .island-hint-mobile {{ display: flex !important; }}
        }}
        .island-hint-mobile {{
            display: none;
            animation: islandHintFade 7s ease forwards;
        }}
        @keyframes islandHintFade {{
            0%, 70% {{ opacity: 1; }}
            100% {{ opacity: 0; visibility: hidden; }}
        }}

        /* 3D 角色即時對話氣泡浮動層 */
        .island-speech-bubble {{
            position: absolute;
            transform: translate(-50%, -100%);
            background: rgba(255, 253, 249, 0.96);
            border: 2.5px solid #3d342b;
            padding: 8px 14px;
            border-radius: 18px;
            font-size: 12px;
            font-weight: 800;
            color: #3d342b;
            max-width: 260px;
            box-shadow: 0 12px 24px -4px rgba(0,0,0,0.22);
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
            z-index: 30;
        }}
        .island-speech-bubble::after {{
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border-width: 7px;
            border-style: solid;
            border-color: #3d342b transparent transparent transparent;
        }}
        .island-speech-bubble.active {{
            opacity: 1;
            transform: translate(-50%, -112%) scale(1);
        }}
    </style>
</head>
<body class="antialiased min-h-screen flex flex-col justify-between">

    <!-- 置頂 Header -->
    <header class="bg-white/90 backdrop-blur-md sticky top-0 z-40 border-b-2 border-stone-200/80 px-4 sm:px-8 py-3.5 shadow-xs">
        <div class="max-w-6xl mx-auto flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-11 h-11 rounded-2xl bg-white border border-purple-200 shadow-md shadow-purple-100 flex items-center justify-center p-1 shrink-0 overflow-hidden">
                    <img src="./family_logo.png" alt="HSU Logo" class="w-full h-full object-contain">
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <span class="text-[10px] font-black uppercase tracking-wider text-red-600 bg-red-50 border border-red-200 px-2 py-0.2 rounded-full">
                            2026 KYUSHU WINTER DRIVE
                        </span>
                        <span class="text-xs text-stone-300 hidden sm:inline">|</span>
                        <span class="text-xs text-stone-500 font-bold hidden sm:inline">熊本・阿蘇・黑川・高千穗・宮崎日南・鹿兒島櫻島</span>
                    </div>
                    <h1 class="text-base sm:text-lg font-black text-stone-800">
                        2026 南九州冬季聖誕自駕・家族旅行大廳
                    </h1>
                </div>
            </div>

            <div class="flex items-center gap-2">
                <button onclick="cheerEveryone()" class="px-3.5 py-1.5 rounded-full bg-red-100 hover:bg-red-200 text-red-700 border border-red-200 text-xs font-black flex items-center gap-1.5 transition shadow-xs">
                    <span>🎉</span>
                    <span class="hidden sm:inline">全員集合歡呼！</span>
                    <span class="sm:hidden">歡呼</span>
                </button>
                <a href="https://docs.google.com/spreadsheets/d/1P4niaKfXpHnrlVkiexFmxa2Q0U7kwOvj6yUINn--WNo/edit?usp=sharing" target="_blank" class="px-3 py-1.5 rounded-full bg-amber-100 hover:bg-amber-200 text-amber-800 border border-amber-300 text-xs font-bold flex items-center gap-1.5 transition shadow-xs">
                    <span>📊</span>
                    <span class="hidden sm:inline">記帳試算表</span>
                </a>
            </div>
        </div>
    </header>

    <!-- 主體內容 -->
    <main class="max-w-6xl mx-auto px-4 sm:px-8 py-6 w-full flex-1 space-y-8">

        <!-- ================= 2.5D 南九州真實輪廓・冬日自駕冒險島 ================= -->
        <div class="relative bg-gradient-to-b from-sky-100/90 via-sky-50 to-amber-50/40 rounded-3xl p-4 sm:p-6 border-2 border-stone-200 shadow-xl overflow-hidden">

            <!-- 標題與控制器列 -->
            <div class="relative z-20 flex flex-col lg:flex-row lg:items-center justify-between gap-3 pb-3 border-b border-sky-200/70">
                <div>
                    <div class="flex flex-wrap items-center gap-2">
                        <span class="inline-flex items-center gap-1.5 text-xs font-black text-red-800 bg-red-100/90 px-2.5 py-0.5 rounded-full border border-red-300">
                            <span class="w-2 h-2 rounded-full bg-red-600 animate-ping"></span>
                            <span>❄️ 2026/12/22 ~ 12/28 冬季聖誕自駕巡禮</span>
                        </span>
                        <span class="inline-flex items-center gap-1 text-xs font-black text-emerald-900 bg-emerald-100/90 px-2.5 py-0.5 rounded-full border border-emerald-300">
                            <span>📍 目前抵達：</span>
                            <span id="current-spot-badge">🏯 熊本城（Day 1 & 7）</span>
                        </span>
                    </div>
                    <h2 class="text-xl sm:text-2xl font-black text-stone-800 mt-1.5 flex items-center gap-2">
                        <span>🗾</span> 2026 南九州冬日自駕島・阿純一家的聖誕冒險
                    </h2>
                </div>
                <div class="island-ctrl-row flex flex-wrap items-center gap-2">
                    <button id="btn-unlock-char" onclick="unlockCharacter()" class="hidden px-3 py-1.5 rounded-full bg-red-600 hover:bg-red-700 text-white border border-red-700 text-xs font-black flex items-center gap-1 shadow-sm transition animate-pulse">
                        <span>🔓</span>
                        <span id="unlock-char-text">解除鎖定</span>
                    </button>
                    <button id="btn-pan-mode" onclick="toggleDragPanMode()" class="px-3 py-1.5 rounded-full bg-amber-100 hover:bg-amber-200 text-amber-900 border border-amber-400 text-xs font-bold flex items-center gap-1 shadow-xs transition" title="預設拖曳平移畫面；按住 Shift + 拖曳或點此切換為旋轉視角">
                        <span>✋</span>
                        <span id="pan-mode-text">左鍵模式：拖曳平移 ✋（Shift 旋轉）</span>
                    </button>
                    <button onclick="toggleSnow()" class="px-3 py-1.5 rounded-full bg-white/90 hover:bg-white text-stone-700 border border-stone-300 text-xs font-bold flex items-center gap-1 shadow-xs transition">
                        <span>❄️</span>
                        <span id="snow-text">冬日飄雪：開</span>
                    </button>
                    <button onclick="toggleAutoRotate()" id="btn-auto-rotate" class="px-3 py-1.5 rounded-full bg-white/90 hover:bg-white text-stone-700 border border-stone-300 text-xs font-bold flex items-center gap-1 shadow-xs transition">
                        <span>🔄</span>
                        <span id="rotate-text">環島旋轉：開</span>
                    </button>
                    <button onclick="cheerEveryone()" class="px-3 py-1.5 rounded-full bg-white/90 hover:bg-white text-stone-700 border border-stone-300 text-xs font-bold flex items-center gap-1 shadow-xs transition">
                        <span>🤾</span>
                        <span>全員歡呼！</span>
                    </button>
                    <a href="./2026%20南九州冬季聖誕自駕/index.html" class="px-4 py-2 rounded-full bg-red-600 hover:bg-red-700 text-white font-black text-xs shadow-md shadow-red-200 flex items-center gap-1.5 transition transform hover:scale-105 active:scale-95">
                        <span>進入 2026 南九州手帳</span>
                        <span>➔</span>
                    </a>
                </div>
            </div>

            <!-- 3D WebGL 畫布容器 -->
            <div id="island-canvas-container" class="relative mt-3 bg-gradient-to-b from-[#cbd5e1] via-[#e2e8f0] to-[#f5ebe1]/40">
                <!-- 動態跟隨角色的對話氣泡 -->
                <div id="char-speech-bubble" class="island-speech-bubble">
                    <div class="flex items-center justify-between gap-2 border-b border-stone-200 pb-0.5 mb-1">
                        <span id="bubble-speaker-name" class="text-[11px] font-black text-red-600">🧶 阿純</span>
                        <span id="bubble-spot-tag" class="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-1.5 rounded">📍 熊本城</span>
                    </div>
                    <div id="bubble-speaker-text" class="text-xs font-bold text-stone-800 leading-snug whitespace-normal">
                        耶！2026 南九州冬季聖誕自駕出發囉～📸
                    </div>
                </div>

                <!-- 浮動在畫布角落的引導提示 -->
                <div class="island-hint-mobile absolute top-2 right-2 bg-white/90 backdrop-blur-sm px-2.5 py-1 rounded-xl border border-stone-200/80 text-[11px] font-bold text-stone-700 shadow-xs pointer-events-none items-center gap-1 z-25">
                    <span>👆 單指拖曳平移・雙指縮放・點頭像看狀態</span>
                </div>
                <div class="island-hint-desktop absolute bottom-3 left-3 bg-white/85 backdrop-blur-sm px-3 py-1.5 rounded-xl border border-stone-200/80 text-[11px] font-bold text-stone-700 shadow-xs pointer-events-none flex items-center gap-2 z-25">
                    <span>✋ 拖曳平移畫面 / 按住 Shift (或右鍵) 拖曳旋轉視角 ｜ 點擊頭頂指標或下方名牌可「鎖定/取消鎖定」鏡頭跟隨角色！</span>
                </div>
            </div>

            <!-- 下方 4 位家族角色名牌列 (點擊鎖定跟隨 / 再次點擊取消鎖定) -->
            <div class="relative z-20 grid grid-cols-2 sm:grid-cols-4 gap-2.5 mt-3 pt-3 border-t border-sky-200/70 text-xs">
                <button id="char-btn-achun" onclick="focusCharacter('achun')" class="p-2.5 rounded-2xl bg-white/90 hover:bg-white border-2 border-amber-200 font-black text-stone-800 flex items-center gap-2.5 transition hover:border-amber-400 shadow-xs text-left">
                    <span class="w-7 h-7 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center text-base shrink-0">🧭</span>
                    <div class="min-w-0">
                        <div class="truncate">首席導遊 <span class="text-[10px] text-amber-700 font-bold">｜阿純</span></div>
                        <span id="char-lock-status-achun" class="text-[10px] text-stone-500 font-medium truncate block">🎯 點擊鎖定鏡頭</span>
                    </div>
                </button>
                <button id="char-btn-yijhang" onclick="focusCharacter('yijhang')" class="p-2.5 rounded-2xl bg-white/90 hover:bg-white border-2 border-blue-200 font-black text-stone-800 flex items-center gap-2.5 transition hover:border-blue-400 shadow-xs text-left">
                    <span class="w-7 h-7 rounded-xl bg-blue-100 text-blue-800 flex items-center justify-center text-base shrink-0">🎩</span>
                    <div class="min-w-0">
                        <div class="truncate">榮譽總指揮 <span class="text-[10px] text-blue-700 font-bold">｜姨丈</span></div>
                        <span id="char-lock-status-yijhang" class="text-[10px] text-stone-500 font-medium truncate block">🎯 點擊鎖定鏡頭</span>
                    </div>
                </button>
                <button id="char-btn-ayee" onclick="focusCharacter('ayee')" class="p-2.5 rounded-2xl bg-white/90 hover:bg-white border-2 border-rose-200 font-black text-stone-800 flex items-center gap-2.5 transition hover:border-rose-400 shadow-xs text-left">
                    <span class="w-7 h-7 rounded-xl bg-rose-100 text-rose-800 flex items-center justify-center text-base shrink-0">⭐</span>
                    <div class="min-w-0">
                        <div class="truncate">美食評鑑官 <span class="text-[10px] text-rose-700 font-bold">｜阿姨</span></div>
                        <span id="char-lock-status-ayee" class="text-[10px] text-stone-500 font-medium truncate block">🎯 點擊鎖定鏡頭</span>
                    </div>
                </button>
                <button id="char-btn-alu" onclick="focusCharacter('alu')" class="p-2.5 rounded-2xl bg-white/90 hover:bg-white border-2 border-orange-200 font-black text-stone-800 flex items-center gap-2.5 transition hover:border-orange-400 shadow-xs text-left">
                    <span class="w-7 h-7 rounded-xl bg-orange-100 text-orange-900 flex items-center justify-center text-base shrink-0">💰</span>
                    <div class="min-w-0">
                        <div class="truncate">總務大臣 <span class="text-[10px] text-orange-800 font-bold">｜阿嚕</span></div>
                        <span id="char-lock-status-alu" class="text-[10px] text-stone-500 font-medium truncate block">🎯 點擊鎖定鏡頭</span>
                    </div>
                </button>
            </div>

            <!-- 7 日自駕重點景點快速跳轉列 -->
            <div class="relative z-20 flex items-center gap-1.5 overflow-x-auto pt-2.5 pb-1 text-[11px] font-bold">
                <span class="text-stone-500 shrink-0 mr-1">🗺️ 景點鏡頭巡禮：</span>
                <button onclick="focusLandmark('kmj_airport')" class="px-2.5 py-1 rounded-full bg-white/80 hover:bg-white border border-stone-200 text-stone-700 shrink-0 transition">🛫 熊本機場</button>
                <button onclick="focusLandmark('kumamoto_castle')" class="px-2.5 py-1 rounded-full bg-white/80 hover:bg-white border border-stone-200 text-stone-700 shrink-0 transition">🏯 熊本城</button>
                <button onclick="focusLandmark('aso_crater')" class="px-2.5 py-1 rounded-full bg-white/80 hover:bg-white border border-stone-200 text-stone-700 shrink-0 transition">🌋 阿蘇火山</button>
                <button onclick="focusLandmark('kurokawa_onsen')" class="px-2.5 py-1 rounded-full bg-white/80 hover:bg-white border border-stone-200 text-stone-700 shrink-0 transition">♨️ 黑川溫泉</button>
                <button onclick="focusLandmark('takachiho_gorge')" class="px-2.5 py-1 rounded-full bg-white/80 hover:bg-white border border-stone-200 text-stone-700 shrink-0 transition">🚣 高千穗峽</button>
                <button onclick="focusLandmark('sun_messe_moai')" class="px-2.5 py-1 rounded-full bg-white/80 hover:bg-white border border-stone-200 text-stone-700 shrink-0 transition">🗿 日南摩艾</button>
                <button onclick="focusLandmark('tenmonkan')" class="px-2.5 py-1 rounded-full bg-white/80 hover:bg-white border border-stone-200 text-stone-700 shrink-0 transition">🎄 鹿兒島天文館</button>
                <button onclick="focusLandmark('sakurajima')" class="px-2.5 py-1 rounded-full bg-white/80 hover:bg-white border border-stone-200 text-stone-700 shrink-0 transition">🚢 櫻島活火山</button>
                <button onclick="focusLandmark('kirishima_jingu')" class="px-2.5 py-1 rounded-full bg-white/80 hover:bg-white border border-stone-200 text-stone-700 shrink-0 transition">⛩️ 霧島神宮</button>
                <button onclick="focusLandmark('hitoyoshi_unagi')" class="px-2.5 py-1 rounded-full bg-white/80 hover:bg-white border border-stone-200 text-stone-700 shrink-0 transition">🍱 人吉鰻魚</button>
            </div>

        </div>

        <!-- 旅程清單列表 -->
        <section class="space-y-4">
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <span class="text-xl">🧳</span>
                    <h3 class="text-lg font-black text-stone-800">所有旅行手帳清單</h3>
                </div>
                <span class="text-xs text-stone-500 font-bold">依時間與狀態排列</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

                <!-- 旅程卡片 1: 2026 南九州 (目前啟動中) -->
                <div class="vault-card bg-white border-2 border-red-200 p-6 sm:p-7 relative flex flex-col justify-between shadow-md shadow-red-100/50">
                    <div class="washi-tape"></div>

                    <div class="space-y-4">
                        <div class="flex items-center justify-between gap-2">
                            <span class="cute-pill bg-emerald-100 text-emerald-800 border border-emerald-300">
                                <span class="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
                                🎄 倒數啟程中・焦點旅程
                            </span>
                            <span class="text-xs font-bold text-stone-400 font-mono">2026 冬季</span>
                        </div>

                        <div>
                            <h4 class="text-xl font-black text-stone-800 hover:text-red-600 transition flex items-center gap-2">
                                <span>🎅</span> 2026 南九州冬季聖誕自駕
                            </h4>
                            <p class="text-xs text-stone-500 mt-1 font-bold">
                                📅 2026/12/22 (二) ~ 12/28 (一) ｜ 7 天 6 夜自駕
                            </p>
                        </div>

                        <div class="p-3 bg-red-50/50 border border-red-100 rounded-2xl space-y-1.5 text-xs">
                            <div class="flex items-center gap-1.5 text-stone-700">
                                <span>✈️</span> <strong>直飛航班：</strong>華航 CI194 (桃機 T2 ➔ 熊本 KMJ) ⇄ CI195
                            </div>
                            <div class="flex items-center gap-1.5 text-stone-700">
                                <span>📍</span> <strong>自駕路線：</strong>熊本 ➔ 阿蘇草千里 ➔ 黑川溫泉 ➔ 高千穗 ➔ 宮崎日南 ➔ 鹿兒島 ➔ 霧島人吉 ➔ 熊本城
                            </div>
                            <div class="flex items-center gap-1.5 text-stone-700">
                                <span>👛</span> <strong>目前記帳：</strong>NT$ 71,250 (4人家族平均 $17,813)
                            </div>
                        </div>

                        <div class="flex flex-wrap gap-1.5">
                            <span class="text-[11px] px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 border border-amber-200 font-bold">🌋 阿蘇中岳火山口</span>
                            <span class="text-[11px] px-2.5 py-0.5 rounded-full bg-purple-50 text-purple-800 border border-purple-200 font-bold">♨️ 黑川山彥仙人風呂 (含早餐)</span>
                            <span class="text-[11px] px-2.5 py-0.5 rounded-full bg-sky-50 text-sky-800 border border-sky-200 font-bold">🚣 高千穗峽划船</span>
                            <span class="text-[11px] px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold">🍱 人吉百年碳火鰻魚</span>
                            <span class="text-[11px] px-2.5 py-0.5 rounded-full bg-rose-50 text-rose-800 border border-rose-200 font-bold">🌋 櫻島活火山渡輪</span>
                        </div>
                    </div>

                    <div class="pt-6 mt-6 border-t border-stone-100 flex items-center justify-between gap-3">
                        <div class="text-[11px] text-stone-400 font-bold">
                            📂 專屬資料夾：<code>2026 南九州冬季聖誕自駕/</code>
                        </div>
                        <a href="./2026%20南九州冬季聖誕自駕/index.html" class="px-5 py-2.5 rounded-full bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-700 hover:to-rose-700 text-white font-black text-xs shadow-md shadow-red-200 flex items-center gap-1.5 transition transform hover:scale-105 active:scale-95">
                            <span>打開手帳</span>
                            <span>➔</span>
                        </a>
                    </div>
                </div>

                <!-- 建立新旅程卡片 -->
                <div class="vault-card bg-stone-50 border-2 border-dashed border-stone-300 p-6 sm:p-7 flex flex-col items-center justify-center text-center space-y-3 hover:border-red-400 transition cursor-pointer">
                    <div class="w-12 h-12 rounded-2xl bg-white border border-stone-200 shadow-xs flex items-center justify-center text-2xl text-stone-400">
                        ✨
                    </div>
                    <div>
                        <h4 class="text-base font-black text-stone-800">
                            想要籌備下一趟全新旅程嗎？
                        </h4>
                        <p class="text-xs text-stone-500 mt-1 max-w-lg leading-relaxed">
                            未來只要在專案底下以「年份＋地點」建立新資料夾（例如：<code>2027 北海道夏季薰衣草自駕</code>），複製模板資料後執行編譯，就會自動在入口大廳點亮全新旅程卡片！
                        </p>
                    </div>
                    <div class="inline-flex items-center gap-1.5 text-xs text-red-600 font-bold">
                        <span>💡 完全獨立模組化・輕鬆帶著走的家族數位記憶</span>
                    </div>
                </div>

            </div>
        </section>

        <!-- 常用實用外連與家族百寶箱 -->
        <section class="bg-white rounded-3xl p-6 border-2 border-stone-200 space-y-4">
            <div class="flex items-center gap-2">
                <span class="text-lg">🧰</span>
                <h3 class="text-sm font-black text-stone-800">家族旅行必備百寶箱</h3>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <a href="https://www.vjw.digital.go.jp/" target="_blank" class="p-3 rounded-2xl bg-stone-50 hover:bg-stone-100 border border-stone-200 transition font-bold text-stone-700 flex flex-col gap-1">
                    <span class="text-base">🇯🇵</span>
                    <span>Visit Japan Web</span>
                    <span class="text-[10px] text-stone-400 font-normal">日本快速入境審查申報</span>
                </a>
                <a href="https://docs.google.com/spreadsheets/d/1P4niaKfXpHnrlVkiexFmxa2Q0U7kwOvj6yUINn--WNo/edit?usp=sharing" target="_blank" class="p-3 rounded-2xl bg-amber-50 hover:bg-amber-100 border border-amber-200 transition font-bold text-amber-800 flex flex-col gap-1">
                    <span class="text-base">📊</span>
                    <span>家族旅行雲端帳本</span>
                    <span class="text-[10px] text-amber-600 font-normal">即時記錄匯款與分攤</span>
                </a>
                <a href="https://www.taoyuan-airport.com/" target="_blank" class="p-3 rounded-2xl bg-sky-50 hover:bg-sky-100 border border-sky-200 transition font-bold text-sky-800 flex flex-col gap-1">
                    <span class="text-base">🛫</span>
                    <span>桃園機場航班即時表</span>
                    <span class="text-[10px] text-sky-600 font-normal">第一/第二航廈起降狀況</span>
                </a>
                <a href="https://rate.bot.com.tw/xrt?Lang=zh-TW" target="_blank" class="p-3 rounded-2xl bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 transition font-bold text-emerald-800 flex flex-col gap-1">
                    <span class="text-base">💴</span>
                    <span>台灣銀行即時牌告匯率</span>
                    <span class="text-[10px] text-emerald-600 font-normal">日圓現鈔換匯參考</span>
                </a>
            </div>
        </section>

    </main>

    <!-- 頁尾宣告 -->
    <footer class="bg-white border-t-2 border-stone-200 py-6 px-4 text-center text-xs text-stone-400 font-medium">
        ❄️ 2026 南九州冬季聖誕自駕・家族旅行手帳大廳 ｜ 更新時間：{now_str} ｜ 祝全家人每一次出發都平安滿載！✨
    </footer>

{scripts_html}

</body>
</html>"""

    output_path = os.path.join(BASE_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # 同步更新 旅行/index.html 鏡像
    mirror_dir = os.path.join(BASE_DIR, '旅行')
    if os.path.isdir(mirror_dir):
        shutil.copyfile(output_path, os.path.join(mirror_dir, 'index.html'))

    print(f"🎉 2026 南九州冬日自駕島入口大廳建立成功：{output_path} (release={release_mode})")


def build_preview_page():
    """產生本地專屬的 preview.html 預覽與單項驗收畫廊（.gitignore 不上傳）"""
    preview_html = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔍 3D 模型與場景預覽驗收畫廊 ｜ 2026 南九州冬日自駕島</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@500;700;800&family=Zen+Maru+Gothic:wght@500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        body {
            font-family: "Zen Maru Gothic", "M PLUS Rounded 1c", sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
        }
        #full-island-container {
            width: 100%;
            height: 460px;
            position: relative;
            border-radius: 1.25rem;
            overflow: hidden;
            cursor: grab;
        }
        #turntable-canvas-container {
            width: 100%;
            height: 340px;
            position: relative;
            border-radius: 1.25rem;
            overflow: hidden;
            cursor: grab;
        }
        .island-speech-bubble {
            position: absolute;
            transform: translate(-50%, -100%);
            background: rgba(255, 253, 249, 0.96);
            border: 2px solid #3d342b;
            padding: 6px 12px;
            border-radius: 14px;
            font-size: 11px;
            font-weight: 800;
            color: #3d342b;
            max-width: 240px;
            pointer-events: none;
            opacity: 0;
            transition: all 0.2s;
            z-index: 30;
        }
        .island-speech-bubble.active {
            opacity: 1;
            transform: translate(-50%, -110%);
        }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <header class="bg-stone-900 text-white px-6 py-3.5 sticky top-0 z-50 flex flex-wrap items-center justify-between gap-3 shadow-md">
        <div class="flex items-center gap-3">
            <span class="px-2.5 py-1 rounded-lg bg-red-600 font-black text-xs">LOCAL PREVIEW ONLY</span>
            <h1 class="font-black text-base sm:text-lg">2026 南九州冬日自駕島・發佈前預覽與單項驗收畫廊</h1>
        </div>
        <div class="flex items-center gap-3 text-xs font-bold">
            <span class="text-stone-300">💬 請記下要調整的編號（如 <code class="text-amber-300">C1</code>、<code class="text-emerald-300">L06</code>、<code class="text-sky-300">P02</code> 或 <code class="text-rose-300">S</code>）直接用文字告訴我！</span>
            <a href="./index.html" target="_blank" class="px-3.5 py-1.5 rounded-full bg-white text-stone-900 font-black hover:bg-stone-200 transition">打開完整首頁 index.html ➔</a>
        </div>
    </header>

    <main class="max-w-7xl mx-auto w-full px-4 sm:px-6 py-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

        <!-- 左側 7 欄：S 完整南九州冬日自駕島場景 -->
        <section class="lg:col-span-7 bg-white rounded-3xl p-5 border-2 border-stone-200 shadow-sm flex flex-col justify-between space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-black text-xs">代號 S</span>
                        <h2 class="font-black text-lg text-stone-800">完整場景：南九州真實輪廓冬日自駕島</h2>
                    </div>
                    <p class="text-xs text-stone-500 font-medium mt-0.5">含錦江灣、櫻島活火山、冬季暖陽長陰影、波浪海面、雲朵飄雪與環島自駕路線</p>
                </div>
                <div class="flex flex-wrap items-center gap-1.5 text-xs font-bold">
                    <button id="btn-unlock-char" onclick="unlockCharacter()" class="hidden px-2.5 py-1 rounded-full bg-red-600 hover:bg-red-700 text-white font-black"><span id="unlock-char-text">🔓 解除鎖定</span></button>
                    <button id="btn-pan-mode" onclick="toggleDragPanMode()" class="px-2.5 py-1 rounded-full bg-amber-100 hover:bg-amber-200 text-amber-900 text-xs font-bold" title="預設拖曳平移；按住 Shift + 拖曳旋轉"><span id="pan-mode-text">左鍵模式：拖曳平移 ✋（Shift 旋轉）</span></button>
                    <span id="current-spot-badge" class="px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200">🏯 熊本城</span>
                    <button onclick="toggleSnow()" class="px-2.5 py-1 rounded-full bg-stone-100 hover:bg-stone-200 text-stone-700"><span id="snow-text">冬日飄雪：開</span></button>
                    <button onclick="toggleAutoRotate()" class="px-2.5 py-1 rounded-full bg-stone-100 hover:bg-stone-200 text-stone-700"><span id="rotate-text">環島旋轉：開</span></button>
                    <button onclick="cheerEveryone()" class="px-2.5 py-1 rounded-full bg-red-100 hover:bg-red-200 text-red-700 font-black">🎉 歡呼</button>
                </div>
            </div>

            <div id="full-island-container" class="bg-stone-200">
                <div id="char-speech-bubble" class="island-speech-bubble">
                    <div class="flex items-center justify-between gap-2 border-b border-stone-200 pb-0.5 mb-0.5">
                        <span id="bubble-speaker-name" class="text-[10px] font-black text-red-600">🧶 阿純</span>
                        <span id="bubble-spot-tag" class="text-[9px] font-bold text-emerald-700">📍 熊本城</span>
                    </div>
                    <div id="bubble-speaker-text" class="text-[11px] font-bold text-stone-800"></div>
                </div>
            </div>

            <div class="grid grid-cols-4 gap-2 text-xs">
                <button id="char-btn-achun" onclick="focusCharacter('achun')" class="py-1.5 px-2 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 font-black border border-amber-200">鎖定/取消 C1 首席導遊 阿純</button>
                <button id="char-btn-yijhang" onclick="focusCharacter('yijhang')" class="py-1.5 px-2 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-900 font-black border border-blue-200">鎖定/取消 C2 榮譽總指揮 姨丈</button>
                <button id="char-btn-ayee" onclick="focusCharacter('ayee')" class="py-1.5 px-2 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-900 font-black border border-rose-200">鎖定/取消 C3 美食評鑑官 阿姨</button>
                <button id="char-btn-alu" onclick="focusCharacter('alu')" class="py-1.5 px-2 rounded-xl bg-orange-50 hover:bg-orange-100 text-orange-900 font-black border border-orange-200">鎖定/取消 C4 總務大臣 阿嚕</button>
            </div>
        </section>

        <!-- 右側 5 欄：360° 單項放大旋轉檢視台 (Turntable Inspector) -->
        <section class="lg:col-span-5 bg-white rounded-3xl p-5 border-2 border-stone-200 shadow-sm flex flex-col justify-between space-y-3">
            <div class="flex items-start justify-between gap-2">
                <div>
                    <div class="flex items-center gap-2">
                        <span id="inspector-code" class="px-2.5 py-0.5 rounded-md bg-red-600 text-white font-black text-xs">C1</span>
                        <h3 id="inspector-title" class="font-black text-base text-stone-800">首席導遊 阿純（全行程總召）</h3>
                    </div>
                    <p id="inspector-subtitle" class="text-xs font-bold text-amber-700 mt-0.5">🧶 黃色毛帽・自拍達人</p>
                </div>
                <button id="btn-toggle-pose" onclick="window.toggleCharPoseMode()" class="px-3 py-1 rounded-full bg-amber-100 hover:bg-amber-200 text-amber-900 font-black text-xs border border-amber-300 shrink-0">
                    <span id="pose-mode-text">切換為：走路擺臂動作</span>
                </button>
            </div>

            <div id="turntable-canvas-container" class="border border-stone-200"></div>

            <div class="p-3 rounded-2xl bg-stone-50 border border-stone-200 text-xs text-stone-600 font-medium leading-relaxed" id="inspector-desc">
                戴著招牌黃色毛球針織帽與溫暖圍巾，負責規劃全家人南九州行程與沿途自拍紀錄！
            </div>
        </section>

        <!-- 下方全寬：所有可點選檢視的編號目錄 (Characters / Landmarks / Props) -->
        <section class="lg:col-span-12 grid grid-cols-1 md:grid-cols-3 gap-6">

            <!-- 1. 角色清單 C1~C4 -->
            <div class="bg-white rounded-3xl p-5 border-2 border-stone-200 space-y-3">
                <div class="flex items-center justify-between">
                    <h4 class="font-black text-sm text-stone-800 flex items-center gap-1.5"><span>👥</span> 家族成員角色（C1 ~ C4）</h4>
                    <span class="text-[11px] font-bold text-stone-400">點選右側放大檢視</span>
                </div>
                <div id="catalog-characters" class="grid grid-cols-1 gap-2"></div>
            </div>

            <!-- 2. 17 處景點清單 L01~L17 -->
            <div class="bg-white rounded-3xl p-5 border-2 border-stone-200 space-y-3">
                <div class="flex items-center justify-between">
                    <h4 class="font-black text-sm text-stone-800 flex items-center gap-1.5"><span>🏯</span> 南九州 17 處景點模型（L01 ~ L17）</h4>
                    <span class="text-[11px] font-bold text-stone-400">點選同步聚焦大島位置</span>
                </div>
                <div id="catalog-landmarks" class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 max-h-80 overflow-y-auto pr-1"></div>
            </div>

            <!-- 3. 動態物件與街景道具 P01~P14 -->
            <div class="bg-white rounded-3xl p-5 border-2 border-stone-200 space-y-3">
                <div class="flex items-center justify-between">
                    <h4 class="font-black text-sm text-stone-800 flex items-center gap-1.5"><span>🚋</span> 載具、聚落、牧場與街景（P01 ~ P14）</h4>
                    <span class="text-[11px] font-bold text-stone-400">點選右側放大檢視</span>
                </div>
                <div id="catalog-props" class="grid grid-cols-1 gap-1.5 max-h-80 overflow-y-auto pr-1"></div>
            </div>

        </section>

    </main>

    <script src="./portal/env.js"></script>
    <script src="./portal/terrain.js"></script>
    <script src="./portal/landmarks.js"></script>
    <script src="./portal/characters.js"></script>
    <script src="./portal/props.js"></script>
    <script src="./portal/island.js"></script>
    <script src="./portal/preview.js"></script>
</body>
</html>"""
    preview_path = os.path.join(BASE_DIR, 'preview.html')
    with open(preview_path, 'w', encoding='utf-8') as f:
        f.write(preview_html)
    print(f"🔍 3D 預覽與單項驗收畫廊建立成功：{preview_path}")


if __name__ == '__main__':
    is_release = ('--release' in sys.argv)
    build_portal(release_mode=is_release)
    build_preview_page()
    if is_release:
        import obfuscate_and_protect
        obfuscate_and_protect.protect_html_file(os.path.join(BASE_DIR, 'index.html'))
        mirror_index = os.path.join(BASE_DIR, '旅行', 'index.html')
        if os.path.exists(mirror_index):
            shutil.copyfile(os.path.join(BASE_DIR, 'index.html'), mirror_index)
