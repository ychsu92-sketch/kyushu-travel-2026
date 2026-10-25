#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_status_bar.py
Adds overhead action status bars for characters performing landmark actions:
- Shows persona actions (laptop typing, camera taking photos, phone tube puzzle, dango feeding)
- Hides for the currently speaking character (except speaker)
- Updates dynamically with smooth rotation of lively descriptions
"""
import os

ISLAND_PATH = '/Users/reyhsu/.gemini/antigravity/scratch/kyushu-travel-2026/portal/island.js'

with open(ISLAND_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add ROLE_SPOT_STATUSES after ROLE_MARKER_STYLES
spot_statuses_def = """
    const ROLE_SPOT_STATUSES = {
        achun: [
            '💻 席地打物治紀錄中…',
            '💻 飛快敲筆電寫 SOAP 病歷…',
            '☕ 邊喝拿鐵邊打復健報告…',
            '💻 鍵盤狂敲整理個案中…'
        ],
        yijhang: [
            '📱 專注破倒試管第 750 關…',
            '🧪 冷靜計算水管倒水順序…',
            '📱 沉浸彩色試管手遊中…',
            '🧪 連闖三關試管破解中…'
        ],
        ayee: [
            '🍡 熱情分送剛烤好糰子…',
            '🥟 遞上熱騰騰黑糖饅頭…',
            '🍊 剝多汁小蜜柑餵食全家…',
            '🛍️ 掏出九州伴手禮分食中…'
        ],
        alu: [
            '📷 舉復古相機取景拍照中…',
            '📸 閃光燈閃爍捕捉全家福…',
            '📷 調整光圈紀錄九州美景…',
            '📸 尋找最佳角度構圖中…'
        ]
    };
"""

marker_styles_marker = "    };\n\n    const FALLBACK_QUOTES ="
if marker_styles_marker not in content:
    print("ERROR: marker_styles_marker not found")
    exit(1)

content = content.replace(
    marker_styles_marker,
    "    };" + spot_statuses_def + "\n    const FALLBACK_QUOTES ="
)

# 2. Add char-action-status element in createCharacterOverheadMarkers
old_inner_html = """            el.innerHTML = `
                <div class="char-pin-badge" style="
                    background:${st.bg};
                    border:2px solid ${st.border};
                    color:${st.text};
                    padding:2px 7px;
                    border-radius:9999px;
                    font-size:10.5px;
                    font-weight:900;
                    white-space:nowrap;
                    box-shadow:0 3px 8px rgba(0,0,0,0.16);
                    display:flex;
                    align-items:center;
                    gap:3px;
                    line-height:1.2;
                ">
                    <span>${st.label}</span>
                    <span class="mode-icon" style="font-size:9px;opacity:0.85;"></span>
                    <span class="lock-icon" style="display:none;font-size:9px;background:${st.border};color:#fff;padding:0 4px;border-radius:999px;">🔒跟隨中</span>
                </div>
                <div style="
                    width:0;height:0;
                    border-left:5px solid transparent;
                    border-right:5px solid transparent;
                    border-top:6px solid ${st.border};
                    margin-top:-1px;
                "></div>
            `;"""

new_inner_html = """            el.innerHTML = `
                <div class="char-action-status" style="
                    display:none;
                    background:rgba(15, 23, 42, 0.92);
                    backdrop-filter:blur(8px);
                    -webkit-backdrop-filter:blur(8px);
                    border:1.5px solid ${st.border};
                    color:#ffffff;
                    font-size:9.5px;
                    font-weight:800;
                    padding:2px 8px;
                    border-radius:9999px;
                    white-space:nowrap;
                    box-shadow:0 3px 10px rgba(0,0,0,0.32);
                    margin-bottom:3px;
                    align-items:center;
                    gap:4px;
                    line-height:1.2;
                    letter-spacing:0.02em;
                    pointer-events:none;
                ">
                    <span class="action-dot" style="
                        width:6px;
                        height:6px;
                        border-radius:999px;
                        background:${st.pin};
                        box-shadow:0 0 6px ${st.pin};
                        display:inline-block;
                        flex-shrink:0;
                    "></span>
                    <span class="action-text"></span>
                </div>
                <div class="char-pin-badge" style="
                    background:${st.bg};
                    border:2px solid ${st.border};
                    color:${st.text};
                    padding:2px 7px;
                    border-radius:9999px;
                    font-size:10.5px;
                    font-weight:900;
                    white-space:nowrap;
                    box-shadow:0 3px 8px rgba(0,0,0,0.16);
                    display:flex;
                    align-items:center;
                    gap:3px;
                    line-height:1.2;
                ">
                    <span>${st.label}</span>
                    <span class="mode-icon" style="font-size:9px;opacity:0.85;"></span>
                    <span class="lock-icon" style="display:none;font-size:9px;background:${st.border};color:#fff;padding:0 4px;border-radius:999px;">🔒跟隨中</span>
                </div>
                <div style="
                    width:0;height:0;
                    border-left:5px solid transparent;
                    border-right:5px solid transparent;
                    border-top:6px solid ${st.border};
                    margin-top:-1px;
                "></div>
            `;"""

if old_inner_html not in content:
    print("ERROR: old_inner_html not found")
    exit(1)

content = content.replace(old_inner_html, new_inner_html)

# 3. Update updateCharacterMarkersPosition to update status text and toggle display
old_marker_update = """            const modeSpan = el.querySelector('.mode-icon');
            if (modeSpan) {
                if (cg.userData.isAboard) {
                    modeSpan.textContent = '🚗';
                } else if (!isStoppedAtLandmark && role === stragglerRole) {
                    modeSpan.textContent = (role === 'achun') ? '🛸💨' : '🏃💨';
                } else {
                    modeSpan.textContent = '';
                }
            }"""

new_marker_update = """            const modeSpan = el.querySelector('.mode-icon');
            if (modeSpan) {
                if (cg.userData.isAboard) {
                    modeSpan.textContent = '🚗';
                } else if (!isStoppedAtLandmark && role === stragglerRole) {
                    modeSpan.textContent = (role === 'achun') ? '🛸💨' : '🏃💨';
                } else {
                    modeSpan.textContent = '';
                }
            }

            // 景點專屬個性動作頭頂狀態列（除發言者外，做動作的人頭頂顯示正在做什麼）
            const isBusy = isStoppedAtLandmark && (cg.userData.isSpotBusy === true);
            const isSpeaking = (activeSpeaker === role);
            const actionEl = el.querySelector('.char-action-status');
            const actionText = el.querySelector('.action-text');

            if (actionEl && actionText) {
                if (isBusy && !isSpeaking) {
                    actionEl.style.display = 'inline-flex';
                    const list = ROLE_SPOT_STATUSES[role] || [];
                    const sIdx = Math.floor(elapsed * 0.35) % (list.length || 1);
                    actionText.textContent = list[sIdx] || '';
                } else {
                    actionEl.style.display = 'none';
                }
            }"""

if old_marker_update not in content:
    print("ERROR: old_marker_update not found")
    exit(1)

content = content.replace(old_marker_update, new_marker_update)

with open(ISLAND_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("portal/island.js successfully updated with character action status bars!")
