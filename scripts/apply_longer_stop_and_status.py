#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_longer_stop_and_status.py
1. Lengthen landmark stop duration by +7.5s (dialog + ~8s free activity time).
2. Ensure overhead action status bar is reliably displayed for all non-speaking characters throughout the stop.
3. Show '🚗 走回車旁準備出發…' during the return-to-car phase.
4. Ensure isSpotBusy is reliably active during the entire roaming phase (roamWeight > 0.20).
"""
import os

ISLAND_PATH = '/Users/reyhsu/.gemini/antigravity/scratch/kyushu-travel-2026/portal/island.js'

with open(ISLAND_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Lengthen stopTimer
old_timer_block = """            if (remainTransitMs > 120) {
                const handoffDelayMs = remainTransitMs + 300;
                stopTimer = ((handoffDelayMs + spotDurationMs) / 1000) + 1.15;
                stopTotalDuration = stopTimer;
                dialogBusyUntilMs = nowMs + handoffDelayMs + spotDurationMs;
                spotArrivalQueueTimer = setTimeout(() => {
                    spotArrivalQueueTimer = null;
                    triggerCustomBanterScript(spotScript, true);
                }, handoffDelayMs);
            } else {
                stopTimer = (spotDurationMs / 1000) + 1.15;
                stopTotalDuration = stopTimer;
                triggerCustomBanterScript(spotScript, true);
            }"""

new_timer_block = """            if (remainTransitMs > 120) {
                const handoffDelayMs = remainTransitMs + 300;
                // 停留秒數充裕延長：景點對話結束後額外保留 7.5 秒自由漫步與專屬動作時間
                stopTimer = ((handoffDelayMs + spotDurationMs) / 1000) + 7.5;
                stopTotalDuration = stopTimer;
                dialogBusyUntilMs = nowMs + handoffDelayMs + spotDurationMs;
                spotArrivalQueueTimer = setTimeout(() => {
                    spotArrivalQueueTimer = null;
                    triggerCustomBanterScript(spotScript, true);
                }, handoffDelayMs);
            } else {
                stopTimer = (spotDurationMs / 1000) + 7.5;
                stopTotalDuration = stopTimer;
                triggerCustomBanterScript(spotScript, true);
            }"""

if old_timer_block not in content:
    print("ERROR: old_timer_block not found in island.js")
    exit(1)

content = content.replace(old_timer_block, new_timer_block)

# 2. Update returnCarFactor to 1.50s buffer
old_factors = """                const elapsedInStop = Math.max(0, stopTotalDuration - stopTimer);
                const leaveCarFactor = Math.min(1.0, elapsedInStop / 0.70);
                const returnCarFactor = Math.min(1.0, stopTimer / 1.20);
                roamWeight = leaveCarFactor * returnCarFactor; // 0 = 在車旁集合，1 = 在景點隨意走動"""

new_factors = """                const elapsedInStop = Math.max(0, stopTotalDuration - stopTimer);
                const leaveCarFactor = Math.min(1.0, elapsedInStop / 0.80);
                const returnCarFactor = Math.min(1.0, stopTimer / 1.50);
                roamWeight = leaveCarFactor * returnCarFactor; // 0 = 在車旁集合，1 = 在景點隨意走動"""

if old_factors in content:
    content = content.replace(old_factors, new_factors)

# 3. Update isSpotBusy condition to roamWeight > 0.20 (active during entire roaming phase)
old_spot_busy = "charGroup.userData.isSpotBusy = c.isStoppedAtLandmark && (c.roamWeight > 0.40) && (!moving || c.isSpeakingNow);"
new_spot_busy = "charGroup.userData.isSpotBusy = c.isStoppedAtLandmark && (c.roamWeight > 0.20);"

if old_spot_busy not in content:
    print("ERROR: old_spot_busy not found in island.js")
    exit(1)

content = content.replace(old_spot_busy, new_spot_busy)

# 4. Update status bar update logic in updateCharacterMarkersPosition
old_status_logic = """            // 景點專屬個性動作頭頂狀態列（除發言者外，做動作的人頭頂顯示正在做什麼）
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

new_status_logic = """            // 景點專屬個性動作頭頂狀態列（除當前發言者顯示大氣泡外，其餘作動作的家人頭頂一律清晰顯示正在做什麼）
            const isSpeaking = (activeSpeaker === role);
            const actionEl = el.querySelector('.char-action-status');
            const actionText = el.querySelector('.action-text');

            if (actionEl && actionText) {
                if (isStoppedAtLandmark && !isSpeaking) {
                    actionEl.style.display = 'inline-flex';
                    if (stopTimer < 1.50) {
                        // 開車前 1.5 秒走回車門旁準備出發
                        actionText.textContent = '🚗 走回車旁準備出發…';
                    } else {
                        // 景點自由活動階段：輪播各自的專屬活動描寫
                        const list = ROLE_SPOT_STATUSES[role] || [];
                        const sIdx = Math.floor(elapsed * 0.30) % (list.length || 1);
                        actionText.textContent = list[sIdx] || '';
                    }
                } else {
                    actionEl.style.display = 'none';
                }
            }"""

if old_status_logic not in content:
    print("ERROR: old_status_logic not found in island.js")
    exit(1)

content = content.replace(old_status_logic, new_status_logic)

with open(ISLAND_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("portal/island.js successfully updated with longer stop duration and guaranteed status bar display!")
