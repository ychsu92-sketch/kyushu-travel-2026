#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
from generate_portal_code import (
    FALLBACK_QUOTES,
    FAMILY_BANTER_SCRIPTS,
    IN_CAR_BANTER_SCRIPTS,
    STRAGGLER_BANTER_SCRIPTS,
    WALK_TOGETHER_BANTER_SCRIPTS
)

ISLAND_PATH = '/Users/reyhsu/.gemini/antigravity/scratch/kyushu-travel-2026/portal/island.js'

with open(ISLAND_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 產生新的對話區塊字串
def js_dump(obj, indent=4):
    return json.dumps(obj, ensure_ascii=False, indent=indent)

dialog_code = """    const FALLBACK_QUOTES = __FALLBACK__;

    // 精簡高頻率日常碎嘴劇本（每段 2～3 句、每句 16～24 字，好讀不卡站！）
    const FAMILY_BANTER_SCRIPTS = __FAMILY__;

    let banterIdx = Math.floor(Math.random() * FAMILY_BANTER_SCRIPTS.length);
    let banterTimers = [];
    let dialogBusyUntilMs = 0;       // 追蹤目前對話（含多句碎嘴佇列）預計完全讀完的時間戳
    let spotArrivalQueueTimer = null; // 若進站時前一段突發對話還剩一點點，排程接續播放景點台詞

    // 車廂內行駛時的精簡高頻率碎嘴劇本（2～3 句短對話）
    const IN_CAR_BANTER_SCRIPTS = __IN_CAR__;

    // 突發狀況：有人沒趕上車在後面狂追（阿純開飛碟追車）精簡版劇本（2～3 句快節奏，確保進下一站前讀完！）
    const STRAGGLER_BANTER_SCRIPTS = __STRAGGLER__;

    function pickStragglerScript(role) {
        const list = STRAGGLER_BANTER_SCRIPTS[role];
        if (!list || !list.length) return null;
        if (!Array.isArray(list[0])) return list;
        const idx = (stragglerScriptIdx[role] || 0) % list.length;
        stragglerScriptIdx[role] = idx + 1;
        return list[idx];
    }

    // 全家下車散步賞景時的精簡碎嘴劇本群（多款情境輪播）
    const WALK_TOGETHER_BANTER_SCRIPTS = __WALK__;
    let walkScriptIdx = Math.floor(Math.random() * WALK_TOGETHER_BANTER_SCRIPTS.length);

    function pickWalkTogetherScript() {
        const s = WALK_TOGETHER_BANTER_SCRIPTS[walkScriptIdx % WALK_TOGETHER_BANTER_SCRIPTS.length];
        walkScriptIdx++;
        return s;
    }"""

dialog_code = dialog_code.replace('__FALLBACK__', js_dump(FALLBACK_QUOTES, 8).strip())
dialog_code = dialog_code.replace('__FAMILY__', js_dump(FAMILY_BANTER_SCRIPTS, 8).strip())
dialog_code = dialog_code.replace('__IN_CAR__', js_dump(IN_CAR_BANTER_SCRIPTS, 8).strip())
dialog_code = dialog_code.replace('__STRAGGLER__', js_dump(STRAGGLER_BANTER_SCRIPTS, 8).strip())
dialog_code = dialog_code.replace('__WALK__', js_dump(WALK_TOGETHER_BANTER_SCRIPTS, 8).strip())

# 替換 FALLBACK_QUOTES 到 WALK_TOGETHER_BANTER 的區塊
idx1 = content.find('    const FALLBACK_QUOTES = {')
idx2 = content.find('    async function loadJsonData')
if idx1 == -1 or idx2 == -1:
    print("ERROR: indices not found in island.js")
    exit(1)

content = content[:idx1] + dialog_code + "\n\n" + content[idx2:]

# 替換散步對話觸發
content = content.replace(
    "triggerCustomBanterScript(WALK_TOGETHER_BANTER, false);",
    "triggerCustomBanterScript(pickWalkTogetherScript(), false);"
)

# 替換人物移動邏輯（加上說話站定與 isSpotBusy）
old_move_code = """                if (moveSpd > 0.12) {
                    const targetYaw = Math.atan2(vx, vz);
                    const curYaw = charGroup.rotation.y || 0;
                    let diff = targetYaw - curYaw;
                    while (diff > Math.PI) diff -= Math.PI * 2;
                    while (diff < -Math.PI) diff += Math.PI * 2;
                    cRotY = curYaw + diff * Math.min(1.0, delta * 9.0);
                } else {
                    cRotY = Math.sin(elapsed * 0.9 + idx) * 0.28;
                }"""

new_move_code = """                // 核心優化：若角色正在說話 (activeSpeaker === role)，原地停止走動，對話框不漂移，專注呈現肢體與表情
                const isSpeakingNow = (activeSpeaker === role);
                if (isSpeakingNow && charGroup.userData.prevX !== undefined) {
                    cx = charGroup.userData.prevX;
                    cz = charGroup.userData.prevZ;
                    isMovingOutside = false;
                }

                if (isMovingOutside && moveSpd > 0.12) {
                    const targetYaw = Math.atan2(vx, vz);
                    const curYaw = charGroup.rotation.y || 0;
                    let diff = targetYaw - curYaw;
                    while (diff > Math.PI) diff -= Math.PI * 2;
                    while (diff < -Math.PI) diff += Math.PI * 2;
                    cRotY = curYaw + diff * Math.min(1.0, delta * 9.0);
                } else {
                    cRotY = Math.sin(elapsed * 0.9 + idx) * 0.28;
                }

                // 景點專屬個性動作標記：在停留漫步階段 (roamWeight > 0.40) 且停步或說話時觸發各人代表性活動
                // 阿純席地打物理治療紀錄、阿嚕舉相機取景閃光、姨丈滑手機倒試管、阿姨四處熱情餵食
                charGroup.userData.isSpotBusy = (roamWeight > 0.40) && (!isMovingOutside || isSpeakingNow);"""

if old_move_code not in content:
    print("ERROR: old_move_code not found in island.js")
    exit(1)

content = content.replace(old_move_code, new_move_code)

with open(ISLAND_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("island.js successfully updated!")
