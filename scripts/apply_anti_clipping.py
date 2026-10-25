#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_anti_clipping.py
Updates portal/island.js character loop to implement:
1. Character-to-Character mutual collision avoidance
2. Character-to-Car OBB collision avoidance
3. Character-to-Landmark collision avoidance
4. Character-to-Obstacle collision avoidance (using window.KyushuIsland.Obstacles)
5. Aligned door-side and wandering anchors in van local orientation
"""
import os

ISLAND_PATH = '/Users/reyhsu/.gemini/antigravity/scratch/kyushu-travel-2026/portal/island.js'

with open(ISLAND_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the beginning of the roles loop and the end of character animation
old_loop_start = "        roles.forEach((role, idx) => {"
old_loop_end = "            if (role === stragglerRole && !isStoppedAtLandmark && charGroup.userData.armL) {\n                charGroup.userData.armL.rotation.x = -2.3 + Math.sin(elapsed * 14.0) * 0.45;\n            }\n        });"

start_idx = content.find(old_loop_start)
end_idx = content.find(old_loop_end)

if start_idx == -1 or end_idx == -1:
    print(f"ERROR: loop markers not found: start_idx={start_idx}, end_idx={end_idx}")
    exit(1)

new_loop_code = """        // 第一階段：計算每位角色的基礎目標座標（在車內坐定，或在車外候車/漫步/追車）
        const outsideChars = [];

        roles.forEach((role, idx) => {
            const charGroup = characters[role];
            if (!charGroup) return;
            const off = walkOffsets[idx];

            // 判斷這位家人現在是否坐在 Toyota Sienta 車廂內
            const isAboard = !isStoppedAtLandmark && (
                travelMode === 'all_aboard' ||
                (travelMode.startsWith('straggler_') && role !== stragglerRole) ||
                onFerry
            );

            charGroup.userData.isAboard = isAboard;
            charGroup.userData.isUfoChasing = (role === 'achun' && role === stragglerRole && !isStoppedAtLandmark && !isAboard);

            if (isAboard) {
                // 1. 真的坐在 Sienta 七人座車艙座椅上（透過車窗玻璃清晰可見，隨車一起前進）
                const seat = carSeatsLocal[role];
                const worldX = van.position.x + seat.x * cosA + seat.z * sinA;
                const worldZ = van.position.z - seat.x * sinA + seat.z * cosA;
                const jumpBoost = (charGroup.userData.jumping > 0) ? Math.sin(charGroup.userData.jumping * Math.PI) * 0.18 : 0;

                charGroup.scale.setScalar(0.68);
                charGroup.position.set(worldX, van.position.y + seat.y + jumpBoost, worldZ);
                charGroup.rotation.y = vanAngle;
                charGroup.userData.baseY = van.position.y + seat.y;

                window.KyushuIsland.Characters.animateCharacterPose(
                    charGroup,
                    elapsed,
                    delta,
                    'seated'
                );
                return;
            }

            // 在車外時恢復標準 0.96x 飽滿比例
            charGroup.scale.setScalar(0.96);
            let cx, cz, cRotY;
            let customSummitY = null;
            let isMovingOutside = !isStoppedAtLandmark;
            const isSummitSpot = isStoppedAtLandmark && currentLandmark && (currentLandmark.id === 'aso_crater' || currentLandmark.id === 'daikanbo');
            let roamWeight = 0;

            if (isStoppedAtLandmark && currentLandmark) {
                // 計算停留階段權重：剛停車 0.7 秒內從車旁散開 (0➔1)、停留期間自由走動 (1)、開車前最後 1.2 秒走回車旁 (1➔0)
                const elapsedInStop = Math.max(0, stopTotalDuration - stopTimer);
                const leaveCarFactor = Math.min(1.0, elapsedInStop / 0.70);
                const returnCarFactor = Math.min(1.0, stopTimer / 1.20);
                roamWeight = leaveCarFactor * returnCarFactor; // 0 = 在車旁集合，1 = 在景點隨意走動

                // Sienta 左側電動滑門旁集合點 (車身外側 0.82m，沿車身長度均勻間隔 0.48m，完全避免人物與車身及相互穿模)
                const doorLocalX = -0.82;
                const doorLocalZ = (idx - 1.5) * 0.48;
                const doorSideX = vanPos.x + (doorLocalX * cosA + doorLocalZ * sinA);
                const doorSideZ = vanPos.z + (-doorLocalX * sinA + doorLocalZ * cosA);
                const doorSideY = van.position.y;

                let spotAnchorX, spotAnchorZ, spotAnchorY;
                if (isSummitSpot) {
                    // 抵達阿蘇火山 (L04) 或大觀峰 (L05)：登上山頂火口觀景台 / 展望台隨意走動
                    const lx = currentLandmark.renderX !== undefined ? currentLandmark.renderX : currentLandmark.x;
                    const lz = currentLandmark.renderZ !== undefined ? currentLandmark.renderZ : currentLandmark.z;
                    const ly = currentLandmark.renderY !== undefined ? currentLandmark.renderY : getGroundY(lx, lz);
                    const sc = currentLandmark.scaleVal || 1.20;
                    const summitSpread = (idx - 1.5) * 0.65;
                    spotAnchorX = lx + summitSpread * 0.85;
                    spotAnchorZ = lz + ((currentLandmark.id === 'aso_crater') ? 0.38 * sc : 0.22 * sc);
                    spotAnchorY = ly + ((currentLandmark.id === 'aso_crater') ? 1.22 * sc : 0.80 * sc);
                } else {
                    // 其他景點：四位家人各自有獨立的賞景扇區錨點（完全錯開彼此初始區域）
                    const roamAnchorsLocal = [
                        { x: -1.15, z: 1.10 }, // 阿純：車前左側開筆電席地打物治紀錄區
                        { x:  0.85, z: 0.95 }, // 姨丈：車前右側路旁專心玩試管手遊區
                        { x: -0.35, z: 1.55 }, // 阿姨：前方中央散步採買餵食區
                        { x:  0.95, z: 1.65 }  // 阿嚕：遠端高視角相機取景拍照區
                    ];
                    const ra = roamAnchorsLocal[idx];
                    spotAnchorX = vanPos.x + (ra.x * cosA + ra.z * sinA);
                    spotAnchorZ = vanPos.z + (-ra.x * sinA + ra.z * cosA);
                    spotAnchorY = getGroundY(spotAnchorX, spotAnchorZ) + 0.04;
                }

                // 每個角色各自平滑漫步的偏移軌跡 (不同頻率與相位，微幅自然晃動)
                const wPhase = elapsed * (1.35 + idx * 0.25) + idx * 2.1;
                const wanderAmp = isSummitSpot ? 0.18 : 0.22;
                const wanderX = (Math.sin(wPhase) * wanderAmp + Math.cos(wPhase * 0.65) * 0.08) * roamWeight;
                const wanderZ = (Math.cos(wPhase * 0.85) * (wanderAmp * 0.75)) * roamWeight;

                cx = doorSideX + (spotAnchorX - doorSideX) * roamWeight + wanderX;
                cz = doorSideZ + (spotAnchorZ - doorSideZ) * roamWeight + wanderZ;
                if (isSummitSpot) {
                    customSummitY = doorSideY + (spotAnchorY - doorSideY) * roamWeight;
                }
            } else if (role === stragglerRole) {
                // 落單苦主：在 Sienta 車尾後方追車（阿純開飛碟，阿嚕/阿姨奔跑）
                const tChase = (routeProgress - 0.0185 + 1.0) % 1.0;
                const pChase = curve.getPointAt(tChase);
                const tanChase = curve.getTangentAt(tChase);
                cx = pChase.x;
                cz = pChase.z;
                cRotY = Math.atan2(tanChase.x, tanChase.z);
            } else {
                // 全家下車散步賞景模式
                const tChar = (routeProgress - off.lag + 1.0) % 1.0;
                const pChar = curve.getPointAt(tChar);
                const tanChar = curve.getTangentAt(tChar);
                const rVecX = tanChar.z;
                const rVecZ = -tanChar.x;
                const rLen = Math.hypot(rVecX, rVecZ) || 1;
                cx = pChar.x + (rVecX / rLen) * off.side;
                cz = pChar.z + (rVecZ / rLen) * off.side;
                cRotY = Math.atan2(tanChar.x, tanChar.z);
            }

            // 核心優化：若角色正在說話 (activeSpeaker === role)，原地停止走動，對話框不漂移，專注呈現肢體與表情
            const isSpeakingNow = (activeSpeaker === role);
            if (isSpeakingNow && charGroup.userData.prevX !== undefined) {
                cx = charGroup.userData.prevX;
                cz = charGroup.userData.prevZ;
                isMovingOutside = false;
            }

            outsideChars.push({
                role,
                idx,
                charGroup,
                cx,
                cz,
                cRotY: cRotY || 0,
                customSummitY,
                isSpeakingNow,
                isMovingOutside,
                isStoppedAtLandmark,
                isSummitSpot: !!isSummitSpot,
                roamWeight
            });
        });

        // 第二階段：嚴格防穿模碰撞解析管線 (Multi-pass Anti-Clipping Resolution)
        // 解決 1: 人物與人物互撞  2: 人物與 Sienta 車身互穿  3: 人物與景點建築互穿  4: 人物與街景道具互穿
        const obstacles = window.KyushuIsland.Obstacles || [];
        const MIN_CHAR_DIST = 0.52; // 人物全身安全直徑（含冬季大衣與肢體動作安全緩衝）
        const VAN_HALF_W = 0.65;    // Sienta 局部座標寬度半徑 (含人體半徑)
        const VAN_HALF_L = 1.15;    // Sienta 局部座標長度半徑 (含人體半徑)

        for (let iter = 0; iter < 3; iter++) {
            // 1. 人物與人物之間互相推開，永不穿模
            for (let i = 0; i < outsideChars.length; i++) {
                for (let j = i + 1; j < outsideChars.length; j++) {
                    const c1 = outsideChars[i];
                    const c2 = outsideChars[j];
                    let dx = c2.cx - c1.cx;
                    let dz = c2.cz - c1.cz;
                    let dist = Math.hypot(dx, dz);
                    if (dist < MIN_CHAR_DIST) {
                        if (dist < 0.001) {
                            dx = (c2.idx - c1.idx) * 0.1 || 0.1;
                            dz = 0.1;
                            dist = Math.hypot(dx, dz);
                        }
                        const overlap = MIN_CHAR_DIST - dist;
                        const nx = dx / dist;
                        const nz = dz / dist;
                        if (c1.isSpeakingNow && !c2.isSpeakingNow) {
                            // 發言者定格不動，另一名漫步者退開
                            c2.cx += nx * overlap;
                            c2.cz += nz * overlap;
                        } else if (!c1.isSpeakingNow && c2.isSpeakingNow) {
                            c1.cx -= nx * overlap;
                            c1.cz -= nz * overlap;
                        } else {
                            // 雙方對稱推開
                            c1.cx -= nx * overlap * 0.5;
                            c1.cz -= nz * overlap * 0.5;
                            c2.cx += nx * overlap * 0.5;
                            c2.cz += nz * overlap * 0.5;
                        }
                    }
                }
            }

            // 2. 人物與 Toyota Sienta 休旅車之間 OBB 碰撞盒嚴格避讓，永不穿透車身
            outsideChars.forEach(c => {
                if (c.isSummitSpot && c.roamWeight > 0.40) return; // 山頂平台遠離停車場小巴
                const distToVan = Math.hypot(c.cx - vanPos.x, c.cz - vanPos.z);
                if (distToVan > 3.0) return;

                // 投影至小巴車體局部座標系 (Local Frame)
                const dx = c.cx - vanPos.x;
                const dz = c.cz - vanPos.z;
                const lx = dx * cosA - dz * sinA;
                const lz = dx * sinA + dz * cosA;

                if (Math.abs(lx) < VAN_HALF_W && Math.abs(lz) < VAN_HALF_L) {
                    const penX = VAN_HALF_W - Math.abs(lx);
                    const penZ = VAN_HALF_L - Math.abs(lz);
                    if (penX < penZ) {
                        const pushLx = (lx >= 0 ? VAN_HALF_W : -VAN_HALF_W);
                        c.cx = vanPos.x + (pushLx * cosA + lz * sinA);
                        c.cz = vanPos.z + (-pushLx * sinA + lz * cosA);
                    } else {
                        const pushLz = (lz >= 0 ? VAN_HALF_L : -VAN_HALF_L);
                        c.cx = vanPos.x + (lx * cosA + pushLz * sinA);
                        c.cz = vanPos.z + (-lx * sinA + pushLz * cosA);
                    }
                }
            });

            // 3. 人物與一般景點建築物避讓 (Kumamoto 城郭、機場航廈、神社鳥居)
            outsideChars.forEach(c => {
                routeData.landmarks.forEach(lm => {
                    if (lm.id === 'aso_crater' || lm.id === 'daikanbo') return;
                    const lx = lm.renderX !== undefined ? lm.renderX : lm.x;
                    const lz = lm.renderZ !== undefined ? lm.renderZ : lm.z;
                    const safeR = (lm.id === 'kumamoto_castle' || lm.id === 'kumamoto_airport') ? 1.55 : 1.25;
                    const d = Math.hypot(c.cx - lx, c.cz - lz);
                    if (d < safeR && d > 0.001) {
                        c.cx = lx + ((c.cx - lx) / d) * safeR;
                        c.cz = lz + ((c.cz - lz) / d) * safeR;
                    }
                });
            });

            // 4. 人物與島嶼街景背景物件避讓 (屋台拉麵、町家聚落、自販機、杉木、鳥居、巴士站牌、石燈籠)
            outsideChars.forEach(c => {
                obstacles.forEach(obs => {
                    const d = Math.hypot(c.cx - obs.x, c.cz - obs.z);
                    const minD = obs.r + 0.24;
                    if (d < minD && d > 0.001) {
                        c.cx = obs.x + ((c.cx - obs.x) / d) * minD;
                        c.cz = obs.z + ((c.cz - obs.z) / d) * minD;
                    }
                });
            });
        }

        // 第三階段：套用最終安全座標、平滑朝向、物理高度與專屬姿態動畫
        outsideChars.forEach(c => {
            const charGroup = c.charGroup;
            const prevX = (charGroup.userData.prevX !== undefined) ? charGroup.userData.prevX : c.cx;
            const prevZ = (charGroup.userData.prevZ !== undefined) ? charGroup.userData.prevZ : c.cz;
            const vx = (c.cx - prevX) / Math.max(delta, 0.001);
            const vz = (c.cz - prevZ) / Math.max(delta, 0.001);
            const moveSpd = Math.hypot(vx, vz);
            let moving = moveSpd > 0.08;

            if (c.isSpeakingNow) {
                moving = false;
                c.cRotY = Math.sin(elapsed * 0.9 + c.idx) * 0.25;
            } else if (c.isStoppedAtLandmark) {
                if (moving && moveSpd > 0.12) {
                    const targetYaw = Math.atan2(vx, vz);
                    const curYaw = charGroup.rotation.y || 0;
                    let diff = targetYaw - curYaw;
                    while (diff > Math.PI) diff -= Math.PI * 2;
                    while (diff < -Math.PI) diff += Math.PI * 2;
                    c.cRotY = curYaw + diff * Math.min(1.0, delta * 9.0);
                } else {
                    c.cRotY = Math.sin(elapsed * 0.9 + c.idx) * 0.28;
                }
            }

            charGroup.position.x = c.cx;
            charGroup.position.z = c.cz;
            charGroup.rotation.y = c.cRotY;
            charGroup.userData.prevX = c.cx;
            charGroup.userData.prevZ = c.cz;

            const charOnFerry = (c.cx > -4.56 && c.cx < -3.12 && c.cz > 9.78 && c.cz < 10.62);
            const rawCharY = getGroundY(c.cx, c.cz) + 0.04;
            charGroup.userData.baseY = charOnFerry
                ? 0.42
                : (c.customSummitY !== null ? c.customSummitY : getMountainSummitY(c.cx, c.cz, rawCharY));

            // 景點專屬個性動作標記：在停留漫步階段 (roamWeight > 0.40) 且停步或說話時觸發各人代表性活動
            // 阿純席地打物理治療紀錄、阿嚕舉相機取景閃光、姨丈滑手機倒試管、阿姨四處熱情餵食
            charGroup.userData.isSpotBusy = c.isStoppedAtLandmark && (c.roamWeight > 0.40) && (!moving || c.isSpeakingNow);

            // 若是落單追車苦主，加快腳步頻率並舉手揮動呼喊；景點漫步或走回車旁時亦播放雙腳邁步動畫
            const animElapsed = (c.role === stragglerRole && !c.isStoppedAtLandmark) ? elapsed * 1.65 : elapsed;
            window.KyushuIsland.Characters.animateCharacterPose(
                charGroup,
                animElapsed,
                delta,
                moving
            );
            if (c.role === stragglerRole && !c.isStoppedAtLandmark && charGroup.userData.armL) {
                charGroup.userData.armL.rotation.x = -2.3 + Math.sin(elapsed * 14.0) * 0.45;
            }
        });"""

content = content[:start_idx] + new_loop_code + content[end_idx + len(old_loop_end):]

with open(ISLAND_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("portal/island.js successfully upgraded with full anti-clipping pipeline!")
