/**
 * portal/island.js
 * 南九州 2.5D 冬日自駕浮空島主控制器：
 * - 載入真實海岸線 JSON 與 17 處行程景點座標
 * - 組裝環境（天空圓頂、冬日暖陽長陰影、錦江灣波浪海面、雲朵、可開關飄雪）
 * - 驅動紅色小巴沿真实自駕路線行駛，並在各景點停留讓 4 位家人（阿純、姨丈、阿姨、阿嚕）下車散步、做專屬動作與顯示對應景點台詞
 * - 支援點擊角色/景點互動、鏡頭聚焦、自動旋轉開關、飄雪開關
 */
(function () {
    window.KyushuIsland = window.KyushuIsland || {};

    let scene, camera, renderer, controls, clock;
    let islandRoot;
    let envState, terrainState, landmarkState, propState;
    let characters = {};
    let isAutoRotate = true;
    let isSnowEnabled = true;

    // 自駕與景點停留狀態機
    let routeProgress = 0; // 0.0 ~ 1.0
    let currentLandmark = null;
    let stopTimer = 0;
    let isStoppedAtLandmark = false;
    let lastStopLandmarkId = null;

    // 對話氣泡控制
    let activeSpeaker = null;
    let bubbleTimeout = null;

    const ROLE_NAMES = {
        achun: '🧶 阿純',
        yijhang: '🕶️ 姨丈',
        ayee: '🍡 阿姨',
        alu: '🐻 阿嚕'
    };

    const FALLBACK_QUOTES = {
        achun: [
            '耶！2026 南九州冬季聖誕自駕出發囉～📸',
            '我的黃色毛球針織帽是不是超適合冬天的九州！✨',
            '從阿蘇火山到日南摩艾，每天都有超棒風景！🎄'
        ],
        yijhang: [
            '墨鏡戴好、雪胎檢查完畢，全家人安心交給我開！🕶️',
            '這台紅色 8 人座小巴開在九州山路太舒適了！🚗',
            '大家坐穩囉，下一站風景更漂亮！👍'
        ],
        ayee: [
            '這趟九州美食太多了！馬肉可樂餅、赤牛丼、黑豚跟鰻魚飯～😍',
            '手上的三色烤糰子跟黑川溫泉饅頭都好香甜喔！🍡',
            '伴手禮袋已經裝滿一半了，太好買了！🛍️'
        ],
        alu: [
            '呼嚕～本熊不是熊本熊，我是愛吃美食的焦糖棕熊阿嚕！🐻',
            '摸摸圓肚子，什麼時候可以開飯跟泡黑川溫泉呀？♨️',
            '九州的冬天涼涼的，圍著紅圍巾剛剛好！🐾'
        ]
    };

    async function loadJsonData(url, inlineKey) {
        if (window.KYUSHU_INLINE_DATA && window.KYUSHU_INLINE_DATA[inlineKey]) {
            return window.KYUSHU_INLINE_DATA[inlineKey];
        }
        const resp = await fetch(url);
        return await resp.json();
    }

    async function initPortalIsland(containerId) {
        const container = document.getElementById(containerId || 'island-canvas-container');
        if (!container || typeof THREE === 'undefined') return;

        const coastData = await loadJsonData('./portal/data/kyushu_coast.json', 'coast');
        const routeData = await loadJsonData('./portal/data/route.json', 'route');

        const w = container.clientWidth || 800;
        const h = container.clientHeight || 520;
        const isMobile = window.innerWidth < 768;

        // 1. 場景與相機 (拉近初始鏡頭讓微縮模型與地貌層次更飽滿)
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(34, w / h, 0.5, 260);
        camera.position.set(0, 16.5, 21.5);

        // 2. WebGL 渲染器與真實柔和陰影
        renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
        renderer.setSize(w, h);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(renderer.domElement);

        // 3. OrbitControls 鏡頭控制
        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.06;
        controls.maxPolarAngle = Math.PI / 2 - 0.06;
        controls.minPolarAngle = 0.25;
        controls.minDistance = 8;
        controls.maxDistance = 42;
        controls.target.set(0.5, 0.6, -2.5);
        controls.autoRotate = isAutoRotate;
        controls.autoRotateSpeed = 0.45;

        // 4. 建立自然環境 (冬季晴空、暖陽、海洋、雲朵、雪花)
        const Env = window.KyushuIsland.Env;
        const skyMesh = Env.createSkyDome(scene);
        const lights = Env.setupWinterLights(scene);
        const ocean = Env.createOcean(scene);
        const clouds = Env.createClouds(scene);
        const snow = Env.createSnowSystem(scene, isMobile);
        envState = { skyMesh, lights, seaMesh: ocean.seaMesh, waveCrests: ocean.waveCrests, clouds, snow };

        // 5. 建立南九州真實海岸線浮空島與自駕道路
        islandRoot = new THREE.Group();
        scene.add(islandRoot);

        terrainState = window.KyushuIsland.Terrain.buildSouthKyushuTerrain(islandRoot, coastData, routeData);
        if (terrainState.foamMeshes) {
            envState.foamMeshes = terrainState.foamMeshes;
        }

        // 6. 建立 17 處真實地理位置景點 (自動貼合等高線台地表面並避讓車道中心線)
        landmarkState = window.KyushuIsland.Landmarks.buildAllLandmarks(
            islandRoot,
            routeData.landmarks,
            terrainState.sampleGroundY,
            terrainState.roadCurve
        );

        // 7. 建立小巴、熊本市電、櫻島渡輪、屋台、商店、貓狗、路人 (貼合地面並避讓車道與地標)
        propState = window.KyushuIsland.Props.populateIslandProps(
            islandRoot,
            terrainState.tramCurve,
            isMobile,
            terrainState.sampleGroundY,
            terrainState.roadCurve,
            routeData.landmarks
        );

        // 8. 建立 4 位家族角色 (阿純、姨丈、阿姨、阿嚕) - 放大至 0.96x 讓人物表情與道具一目了然
        const Chars = window.KyushuIsland.Characters;
        ['achun', 'yijhang', 'ayee', 'alu'].forEach(role => {
            const c = Chars.createCharacter(role);
            c.scale.setScalar(0.96);
            c.userData.baseY = 0.84;
            islandRoot.add(c);
            characters[role] = c;
        });

        // 初始把小巴與角色放到熊本城/阿蘇一帶
        routeProgress = 0.14;
        currentLandmark = routeData.landmarks[1];
        updateTourPositions(routeData, 0, 0.016);

        // 9. 事件綁定
        clock = new THREE.Clock();
        renderer.domElement.addEventListener('pointerdown', e => onPointerDown(e, routeData));
        window.addEventListener('resize', () => onResize(container));

        // 啟動自動對話輪播
        let roleIdx = 0;
        setInterval(() => {
            if (!activeSpeaker) {
                const roles = ['achun', 'yijhang', 'ayee', 'alu'];
                roleIdx = (roleIdx + 1) % roles.length;
                triggerCharacterSpeak(roles[roleIdx]);
            }
        }, 6800);

        setTimeout(() => triggerCharacterSpeak('achun'), 1000);

        // 啟動渲染迴圈
        function loop() {
            requestAnimationFrame(loop);
            const delta = Math.min(clock.getDelta(), 0.1);
            const elapsed = clock.getElapsedTime();

            Env.updateEnvironment(envState, elapsed, delta);
            window.KyushuIsland.Landmarks.updateLandmarks(landmarkState.animatedLandmarks, elapsed);
            window.KyushuIsland.Props.updatePropsAnimation(propState, terrainState.tramCurve, elapsed);
            updateTourPositions(routeData, elapsed, delta);

            controls.update();
            updateBubbleScreenPosition();
            renderer.render(scene, camera);
        }
        loop();
    }

    // 驅動自駕小巴與 4 位家人沿南九州路線巡遊 + 抵達景點時下車散步互動
    function updateTourPositions(routeData, elapsed, delta) {
        if (!terrainState || !terrainState.roadCurve || !propState || !propState.minivan) return;
        const curve = terrainState.roadCurve;
        const van = propState.minivan;

        if (isStoppedAtLandmark) {
            stopTimer -= delta;
            if (stopTimer <= 0) {
                isStoppedAtLandmark = false;
            }
        } else {
            routeProgress = (routeProgress + delta * 0.016) % 1.0;
        }

        const vanPos = curve.getPointAt(routeProgress);
        const vanTan = curve.getTangentAt(routeProgress);
        const vanAngle = Math.atan2(vanTan.x, vanTan.z);
        const getGroundY = terrainState.sampleGroundY || (() => 0.80);

        // 檢查是否經過櫻島渡輪海面段，並動態取樣真實地表高度避免小巴陷入台地
        const onFerry = (vanPos.x > -3.80 && vanPos.x < -2.60 && vanPos.z > 8.15 && vanPos.z < 8.85);
        const vanGroundY = onFerry ? 0.38 : (getGroundY(vanPos.x, vanPos.z) + 0.05);
        van.position.set(vanPos.x, vanGroundY, vanPos.z);
        van.rotation.y = vanAngle;

        // 車輪轉動與引擎微幅震動
        if (!isStoppedAtLandmark && van.userData.wheels) {
            van.userData.wheels.forEach(w => { w.rotation.x += delta * 6.0; });
            van.position.y += Math.sin(elapsed * 22.0) * 0.008;
        }

        // 偵測距離最近的景點
        let nearest = null;
        let minDist = 999;
        routeData.landmarks.forEach(lm => {
            const d = Math.hypot(vanPos.x - lm.x, vanPos.z - lm.z);
            if (d < minDist) {
                minDist = d;
                nearest = lm;
            }
        });

        if (nearest && minDist < 1.15 && lastStopLandmarkId !== nearest.id) {
            currentLandmark = nearest;
            lastStopLandmarkId = nearest.id;
            isStoppedAtLandmark = true;
            stopTimer = 4.2; // 在景點停留 4.2 秒讓家人下車做專屬動作與對話
            updateLocationBanner(nearest);
        }

        // 排列 4 位家族角色在已淨空的車道兩側散步或駐足欣賞景點（縮小橫向偏移並避開地標建築，徹底防止穿模）
        const roles = ['achun', 'yijhang', 'ayee', 'alu'];
        const offsets = [
            { side: -0.46, lag: 0.011 },
            { side: 0.46,  lag: 0.016 },
            { side: -0.52, lag: 0.024 },
            { side: 0.52,  lag: 0.030 }
        ];

        roles.forEach((role, idx) => {
            const charGroup = characters[role];
            if (!charGroup) return;
            const off = offsets[idx];
            let cx, cz, cRotY;

            if (isStoppedAtLandmark && currentLandmark) {
                // 在小巴與景點前方的安全淨空帶一字弧形排開做專屬動作（面朝景點或鏡頭，不踩進景點模型內）
                const lmX = currentLandmark.renderX !== undefined ? currentLandmark.renderX : currentLandmark.x;
                const lmZ = currentLandmark.renderZ !== undefined ? currentLandmark.renderZ : currentLandmark.z;
                const toLmX = lmX - vanPos.x;
                const toLmZ = lmZ - vanPos.z;
                const toLmAngle = Math.atan2(toLmX, toLmZ);
                const perpX = Math.cos(toLmAngle);
                const perpZ = -Math.sin(toLmAngle);
                const spread = (idx - 1.5) * 0.48;

                // 站在車道中心往景點方向微偏 0.28 處，並確保與景點中心保持 >= 1.05 安全距離
                cx = vanPos.x + Math.sin(toLmAngle) * 0.28 + perpX * spread;
                cz = vanPos.z + Math.cos(toLmAngle) * 0.28 + perpZ * spread;
                cRotY = toLmAngle + Math.PI * 0.15 + Math.sin(elapsed * 0.8 + idx) * 0.15;
            } else {
                // 沿著路線跟隨小巴在淨空路肩散步前進
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

            // 防止角色與任何景點建築發生水平穿模：若距離任一景點中心 < 0.98，自動往外推開
            routeData.landmarks.forEach(lm => {
                const lx = lm.renderX !== undefined ? lm.renderX : lm.x;
                const lz = lm.renderZ !== undefined ? lm.renderZ : lm.z;
                const d = Math.hypot(cx - lx, cz - lz);
                const safeR = 0.98;
                if (d < safeR && d > 0.001) {
                    cx = lx + ((cx - lx) / d) * safeR;
                    cz = lz + ((cz - lz) / d) * safeR;
                }
            });

            charGroup.position.x = cx;
            charGroup.position.z = cz;
            charGroup.rotation.y = cRotY;

            // 每幀透過 Raycaster 動態更新角色腳底所在階梯台地高度，徹底消除陷入高地或懸空問題
            const charOnFerry = (cx > -3.80 && cx < -2.60 && cz > 8.15 && cz < 8.85);
            charGroup.userData.baseY = charOnFerry ? 0.42 : (getGroundY(cx, cz) + 0.04);

            window.KyushuIsland.Characters.animateCharacterPose(
                charGroup,
                elapsed,
                delta,
                !isStoppedAtLandmark
            );
        });
    }

    function updateLocationBanner(lm) {
        const badgeEl = document.getElementById('current-spot-badge');
        if (badgeEl && lm) {
            badgeEl.textContent = `${lm.shortName}（${lm.day}）`;
        }
    }

    function triggerCharacterSpeak(role, customText) {
        const charGroup = characters[role];
        if (!charGroup) return;

        charGroup.userData.jumping = 1.0;
        activeSpeaker = role;

        let text = customText;
        if (!text && currentLandmark && currentLandmark.dialogs && currentLandmark.dialogs[role]) {
            text = currentLandmark.dialogs[role];
        }
        if (!text) {
            const pool = FALLBACK_QUOTES[role] || FALLBACK_QUOTES.achun;
            text = pool[Math.floor(Math.random() * pool.length)];
        }

        const bubble = document.getElementById('char-speech-bubble');
        const nameEl = document.getElementById('bubble-speaker-name');
        const textEl = document.getElementById('bubble-speaker-text');
        const spotEl = document.getElementById('bubble-spot-tag');

        if (bubble && nameEl && textEl) {
            nameEl.textContent = ROLE_NAMES[role] || role;
            textEl.textContent = text;
            if (spotEl && currentLandmark) {
                spotEl.textContent = `📍 ${currentLandmark.shortName}`;
            }
            updateBubbleScreenPosition();
            bubble.classList.add('active');

            if (bubbleTimeout) clearTimeout(bubbleTimeout);
            bubbleTimeout = setTimeout(() => {
                bubble.classList.remove('active');
                activeSpeaker = null;
            }, 4600);
        }
    }

    function updateBubbleScreenPosition() {
        if (!activeSpeaker || !characters[activeSpeaker] || !camera || !renderer) return;
        const bubble = document.getElementById('char-speech-bubble');
        if (!bubble) return;

        const charGroup = characters[activeSpeaker];
        const pos = new THREE.Vector3();
        charGroup.getWorldPosition(pos);
        pos.y += 1.45;
        pos.project(camera);

        const canvas = renderer.domElement;
        const x = (pos.x * 0.5 + 0.5) * canvas.clientWidth;
        const y = (-(pos.y * 0.5) + 0.5) * canvas.clientHeight;

        const clampedX = Math.max(115, Math.min(canvas.clientWidth - 115, x));
        const clampedY = Math.max(65, Math.min(canvas.clientHeight - 35, y));

        bubble.style.left = `${clampedX}px`;
        bubble.style.top = `${clampedY}px`;
    }

    function onPointerDown(e, routeData) {
        if (!renderer || !camera) return;
        const rect = renderer.domElement.getBoundingClientRect();
        const mouse = new THREE.Vector2(
            ((e.clientX - rect.left) / rect.width) * 2 - 1,
            -((e.clientY - rect.top) / rect.height) * 2 + 1
        );
        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, camera);

        // 1. 優先檢查是否點擊到 4 位家族角色
        const charMeshes = [];
        Object.values(characters).forEach(cg => {
            cg.traverse(ch => {
                if (ch.isMesh) {
                    ch.userData.parentRole = cg.userData.role;
                    charMeshes.push(ch);
                }
            });
        });
        const hitChar = raycaster.intersectObjects(charMeshes, false);
        if (hitChar.length > 0) {
            const role = hitChar[0].object.userData.parentRole;
            if (role) {
                triggerCharacterSpeak(role);
                return;
            }
        }

        // 2. 檢查是否點擊到 17 處景點模型
        if (landmarkState && landmarkState.animatedLandmarks) {
            const lmMeshes = [];
            landmarkState.animatedLandmarks.forEach(lmGroup => {
                lmGroup.traverse(ch => {
                    if (ch.isMesh) {
                        ch.userData.landmarkInfo = lmGroup.userData.landmarkInfo;
                        lmMeshes.push(ch);
                    }
                });
            });
            const hitLm = raycaster.intersectObjects(lmMeshes, false);
            if (hitLm.length > 0 && hitLm[0].object.userData.landmarkInfo) {
                const info = hitLm[0].object.userData.landmarkInfo;
                currentLandmark = info;
                updateLocationBanner(info);
                controls.target.set(info.x, 0.8, info.z);
                const roles = ['achun', 'yijhang', 'ayee', 'alu'];
                const r = roles[Math.floor(Math.random() * roles.length)];
                triggerCharacterSpeak(r, info.dialogs ? info.dialogs[r] : info.desc);
            }
        }
    }

    function focusCharacter(role) {
        const cg = characters[role];
        if (cg && controls) {
            controls.target.set(cg.position.x, 0.8, cg.position.z);
        }
        triggerCharacterSpeak(role);
    }

    function focusLandmark(landmarkId) {
        if (!landmarkState || !landmarkState.landmarkMap) return;
        const lmGroup = landmarkState.landmarkMap[landmarkId];
        if (lmGroup && lmGroup.userData.landmarkInfo) {
            const info = lmGroup.userData.landmarkInfo;
            currentLandmark = info;
            updateLocationBanner(info);
            if (controls) {
                controls.target.set(info.x, 0.8, info.z);
            }
            triggerCharacterSpeak('achun', info.dialogs ? info.dialogs.achun : info.desc);
        }
    }

    function cheerEveryone() {
        const roles = ['achun', 'yijhang', 'ayee', 'alu'];
        roles.forEach((r, idx) => {
            setTimeout(() => {
                if (characters[r]) characters[r].userData.jumping = 1.0;
            }, idx * 110);
        });
        const lucky = roles[Math.floor(Math.random() * roles.length)];
        triggerCharacterSpeak(lucky);
    }

    function toggleAutoRotate() {
        isAutoRotate = !isAutoRotate;
        if (controls) controls.autoRotate = isAutoRotate;
        const txt = document.getElementById('rotate-text');
        if (txt) txt.textContent = `環島旋轉：${isAutoRotate ? '開' : '關'}`;
    }

    function toggleSnow() {
        isSnowEnabled = !isSnowEnabled;
        if (envState && envState.snow) {
            envState.snow.visible = isSnowEnabled;
        }
        const txt = document.getElementById('snow-text');
        if (txt) txt.textContent = `冬日飄雪：${isSnowEnabled ? '開' : '關'}`;
    }

    function onResize(container) {
        if (!container || !camera || !renderer) return;
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
    }

    // 匯出全域控制函式供 HTML 按鈕呼叫
    window.focusCharacter = focusCharacter;
    window.focusLandmark = focusLandmark;
    window.cheerEveryone = cheerEveryone;
    window.toggleAutoRotate = toggleAutoRotate;
    window.toggleSnow = toggleSnow;

    window.KyushuIsland.Portal = {
        initPortalIsland,
        focusCharacter,
        focusLandmark,
        cheerEveryone,
        toggleAutoRotate,
        toggleSnow
    };
})();
