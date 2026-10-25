/**
 * portal/preview.js
 * 發佈前專屬 3D 預覽與驗收畫廊引擎 (Preview Gallery Inspector)：
 * - 支援切換「S 完整南九州冬日自駕島」、「C1~C4 家族角色檢視」、「L01~L17 景點模型檢視」、「P01~P09 動態物件與街景檢視」
 * - 每個項目皆提供編號、名稱、特徵說明與 360° 獨立旋轉放大檢視台，方便使用者以文字回饋微調。
 */
(function () {
    window.KyushuIsland = window.KyushuIsland || {};

    let inspectorScene, inspectorCamera, inspectorRenderer, inspectorControls, inspectorClock;
    let currentShowcaseRoot = null;
    let currentCategory = 'character';
    let currentCode = 'C1';
    let charPoseIdx = 0; // 0: 景點專屬動作, 1: 走路擺臂動作, 2: 開飛碟追車(C1專屬)
    let routeDataCache = null;

    async function initPreviewGallery() {
        try {
            if (window.KYUSHU_INLINE_DATA && window.KYUSHU_INLINE_DATA.route) {
                routeDataCache = window.KYUSHU_INLINE_DATA.route;
            } else {
                const resp = await fetch('./portal/data/route.json');
                routeDataCache = await resp.json();
            }
        } catch (e) {
            console.warn('⚠️ 載入 route.json 失敗，嘗試使用預設路徑資料', e);
            if (window.KYUSHU_INLINE_DATA && window.KYUSHU_INLINE_DATA.route) {
                routeDataCache = window.KYUSHU_INLINE_DATA.route;
            }
        }

        // 1. 初始化完整南九州島預覽區
        if (window.KyushuIsland && window.KyushuIsland.Portal && window.KyushuIsland.Portal.initPortalIsland) {
            try {
                await window.KyushuIsland.Portal.initPortalIsland('full-island-container');
            } catch (err) {
                console.error('❌ 初始化 3D 完整大島失敗:', err);
            }
        }

        // 2. 初始化右側單項 360° 放大檢視台 (3D Turntable Inspector)
        const stage = document.getElementById('turntable-canvas-container');
        if (!stage) return;

        const w = stage.clientWidth || 500;
        const h = stage.clientHeight || 420;

        inspectorScene = new THREE.Scene();
        inspectorScene.background = new THREE.Color(0xf1f5f9);

        inspectorCamera = new THREE.PerspectiveCamera(34, w / h, 0.1, 100);
        inspectorCamera.position.set(0, 1.8, 3.6);

        inspectorRenderer = new THREE.WebGLRenderer({ antialias: true });
        inspectorRenderer.setSize(w, h);
        inspectorRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        inspectorRenderer.shadowMap.enabled = true;
        inspectorRenderer.shadowMap.type = THREE.PCFSoftShadowMap;
        inspectorRenderer.toneMapping = THREE.ACESFilmicToneMapping;
        inspectorRenderer.toneMappingExposure = 1.14;
        stage.appendChild(inspectorRenderer.domElement);

        inspectorControls = new THREE.OrbitControls(inspectorCamera, inspectorRenderer.domElement);
        inspectorControls.enableDamping = true;
        inspectorControls.target.set(0, 0.55, 0);
        inspectorControls.autoRotate = true;
        inspectorControls.autoRotateSpeed = 1.6;

        // 檢視台燈光與圓形木質展示底座 (提升立體陰影與暖陽輪廓光)
        const amb = new THREE.AmbientLight(0xfff5ea, 0.50);
        inspectorScene.add(amb);
        const hemi = new THREE.HemisphereLight(0xdbeafe, 0xd6c7b2, 0.38);
        inspectorScene.add(hemi);
        const dir = new THREE.DirectionalLight(0xffecd2, 1.25);
        dir.position.set(5, 8, 6);
        dir.castShadow = true;
        dir.shadow.mapSize.width = 1024;
        dir.shadow.mapSize.height = 1024;
        dir.shadow.radius = 2.0;
        dir.shadow.bias = -0.0005;
        inspectorScene.add(dir);
        const rimLight = new THREE.DirectionalLight(0xfff6e6, 0.35);
        rimLight.position.set(-5, 6, -5);
        inspectorScene.add(rimLight);

        const pedestal = new THREE.Mesh(
            new THREE.CylinderGeometry(1.15, 1.25, 0.14, 32),
            new THREE.MeshLambertMaterial({ color: 0x799863 })
        );
        pedestal.position.y = -0.07;
        pedestal.receiveShadow = true;
        inspectorScene.add(pedestal);

        const rim = new THREE.Mesh(
            new THREE.CylinderGeometry(1.26, 1.32, 0.18, 32),
            new THREE.MeshLambertMaterial({ color: 0x8c583a })
        );
        rim.position.y = -0.18;
        inspectorScene.add(rim);

        inspectorClock = new THREE.Clock();

        // 渲染目錄清單並預設選中 C1 阿純
        renderCatalogButtons();
        selectCatalogItem('character', 'C1');

        window.addEventListener('resize', () => {
            const nw = stage.clientWidth;
            const nh = stage.clientHeight;
            inspectorCamera.aspect = nw / nh;
            inspectorCamera.updateProjectionMatrix();
            inspectorRenderer.setSize(nw, nh);
        });

        function loopInspector() {
            requestAnimationFrame(loopInspector);
            const delta = Math.min(inspectorClock.getDelta(), 0.1);
            const elapsed = inspectorClock.getElapsedTime();

            if (currentShowcaseRoot) {
                if (currentCategory === 'character') {
                    currentShowcaseRoot.userData.baseY = 0;
                    currentShowcaseRoot.userData.isSpotBusy = (charPoseIdx === 0);
                    currentShowcaseRoot.userData.isUfoChasing = (currentCode === 'C1' && charPoseIdx === 2);
                    currentShowcaseRoot.userData.isBroomChasing = (currentCode === 'C3' && charPoseIdx === 2);
                    currentShowcaseRoot.userData.isDragonChasing = (currentCode === 'C4' && charPoseIdx === 2);
                    window.KyushuIsland.Characters.animateCharacterPose(currentShowcaseRoot, elapsed, delta, charPoseIdx === 1);
                } else if (currentCategory === 'landmark') {
                    window.KyushuIsland.Landmarks.updateLandmarks([currentShowcaseRoot], elapsed);
                } else if (currentCategory === 'prop') {
                    if (currentShowcaseRoot.userData.wheels) {
                        currentShowcaseRoot.userData.wheels.forEach(w => { w.rotation.x += delta * 5.0; });
                    }
                    if (currentShowcaseRoot.userData.tail) {
                        currentShowcaseRoot.userData.tail.rotation.z = Math.sin(elapsed * 9.0) * 0.35;
                    }
                }
            }

            inspectorControls.update();
            inspectorRenderer.render(inspectorScene, inspectorCamera);
        }
        loopInspector();
    }

    function renderCatalogButtons() {
        // 1. 角色 C1~C4
        const charBox = document.getElementById('catalog-characters');
        if (charBox) {
            charBox.innerHTML = window.KyushuIsland.Characters.CHARACTER_SPECS.map(c => `
                <button onclick="window.selectPreviewItem('character', '${c.code}')" id="btn-item-${c.code}"
                    class="catalog-btn text-left p-2.5 rounded-2xl border-2 border-stone-200 hover:border-red-400 bg-white transition flex flex-col gap-0.5">
                    <div class="flex items-center justify-between">
                        <span class="px-2 py-0.5 rounded-md bg-red-100 text-red-800 font-black text-[11px]">${c.code}</span>
                        <span class="text-[11px] font-bold text-stone-500">${c.badge}</span>
                    </div>
                    <div class="font-black text-sm text-stone-800 mt-0.5">${c.name} <span class="text-xs font-bold text-stone-500">｜ ${c.title}</span></div>
                </button>
            `).join('');
        }

        // 2. 景點 L01~L17
        const lmBox = document.getElementById('catalog-landmarks');
        if (lmBox && routeDataCache) {
            lmBox.innerHTML = routeDataCache.landmarks.map(l => `
                <button onclick="window.selectPreviewItem('landmark', '${l.code}')" id="btn-item-${l.code}"
                    class="catalog-btn text-left p-2 rounded-xl border-2 border-stone-200 hover:border-emerald-500 bg-white transition flex items-center justify-between gap-2">
                    <div class="flex items-center gap-2 min-w-0">
                        <span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-black text-[11px] shrink-0">${l.code}</span>
                        <span class="font-black text-xs text-stone-800 truncate">${l.shortName}</span>
                    </div>
                    <span class="text-[10px] font-bold text-stone-400 shrink-0">${l.day}</span>
                </button>
            `).join('');
        }

        // 3. 動態物件與街景 P01~P09
        const propBox = document.getElementById('catalog-props');
        if (propBox) {
            propBox.innerHTML = window.KyushuIsland.Props.PROP_SPECS.map(p => `
                <button onclick="window.selectPreviewItem('prop', '${p.code}')" id="btn-item-${p.code}"
                    class="catalog-btn text-left p-2 rounded-xl border-2 border-stone-200 hover:border-amber-500 bg-white transition flex items-center justify-between gap-2">
                    <div class="flex items-center gap-2 min-w-0">
                        <span class="px-1.5 py-0.5 rounded bg-amber-100 text-amber-900 font-black text-[11px] shrink-0">${p.code}</span>
                        <span class="font-black text-xs text-stone-800 truncate">${p.name}</span>
                    </div>
                    <span class="text-[10px] font-bold text-stone-500 shrink-0">${p.badge}</span>
                </button>
            `).join('');
        }
    }

    function selectCatalogItem(category, code) {
        currentCategory = category;
        currentCode = code;

        document.querySelectorAll('.catalog-btn').forEach(b => {
            b.classList.remove('ring-2', 'ring-red-500', 'bg-red-50/60', 'border-red-500');
        });
        const activeBtn = document.getElementById(`btn-item-${code}`);
        if (activeBtn) {
            activeBtn.classList.add('ring-2', 'ring-red-500', 'bg-red-50/60', 'border-red-500');
        }

        if (currentShowcaseRoot) {
            inspectorScene.remove(currentShowcaseRoot);
            currentShowcaseRoot = null;
        }

        const codeBadge = document.getElementById('inspector-code');
        const titleEl = document.getElementById('inspector-title');
        const subEl = document.getElementById('inspector-subtitle');
        const descEl = document.getElementById('inspector-desc');
        const poseBtn = document.getElementById('btn-toggle-pose');

        if (category === 'character') {
            charPoseIdx = 0;
            const txt = document.getElementById('pose-mode-text');
            if (txt) txt.textContent = '目前：景點專屬動作 (點擊切換)';

            const spec = window.KyushuIsland.Characters.CHARACTER_SPECS.find(c => c.code === code);
            currentShowcaseRoot = window.KyushuIsland.Characters.createCharacter(code);
            currentShowcaseRoot.scale.setScalar(0.95);
            currentShowcaseRoot.userData.baseY = 0;
            currentShowcaseRoot.position.y = 0;
            inspectorScene.add(currentShowcaseRoot);
            inspectorCamera.position.set(0, 1.15, 3.65);
            inspectorControls.target.set(0, 0.65, 0);
            inspectorControls.update();

            if (spec) {
                codeBadge.textContent = spec.code;
                titleEl.textContent = `${spec.name}（${spec.title}）`;
                subEl.textContent = spec.badge;
                descEl.textContent = spec.desc;
            }
            if (poseBtn) poseBtn.classList.remove('hidden');
        } else if (category === 'landmark') {
            const lm = routeDataCache.landmarks.find(l => l.code === code);
            currentShowcaseRoot = window.KyushuIsland.Landmarks.createLandmarkByCode(code);
            currentShowcaseRoot.scale.setScalar(1.0);
            inspectorScene.add(currentShowcaseRoot);
            inspectorCamera.position.set(0, 1.85, 3.85);
            inspectorControls.target.set(0, 0.55, 0);
            inspectorControls.update();

            if (lm) {
                codeBadge.textContent = lm.code;
                titleEl.textContent = lm.name;
                subEl.textContent = `${lm.shortName} ｜ ${lm.day}`;
                descEl.textContent = lm.desc;
                // 同步讓左側大島鏡頭聚焦到該景點
                window.KyushuIsland.Portal.focusLandmark(lm.id);
            }
            if (poseBtn) poseBtn.classList.add('hidden');
        } else if (category === 'prop') {
            const p = window.KyushuIsland.Props.PROP_SPECS.find(x => x.code === code);
            currentShowcaseRoot = window.KyushuIsland.Props.createPropByCode(code);
            currentShowcaseRoot.scale.setScalar(1.18);
            inspectorScene.add(currentShowcaseRoot);
            inspectorCamera.position.set(0, 1.50, 3.45);
            inspectorControls.target.set(0, 0.45, 0);
            inspectorControls.update();

            if (p) {
                codeBadge.textContent = p.code;
                titleEl.textContent = p.name;
                subEl.textContent = p.badge;
                descEl.textContent = p.desc;
            }
            if (poseBtn) poseBtn.classList.add('hidden');
        }
    }

    function toggleCharPoseMode() {
        const maxModes = (currentCode === 'C1' || currentCode === 'C3' || currentCode === 'C4') ? 3 : 2;
        charPoseIdx = (charPoseIdx + 1) % maxModes;
        const txt = document.getElementById('pose-mode-text');
        if (txt) {
            if (charPoseIdx === 0) txt.textContent = '目前：景點專屬動作 (點擊切換)';
            else if (charPoseIdx === 1) {
                if (currentCode === 'C1') txt.textContent = '目前：走路動作 (再點看飛碟🛸)';
                else if (currentCode === 'C3') txt.textContent = '目前：走路動作 (再點看魔法掃帚🧹)';
                else if (currentCode === 'C4') txt.textContent = '目前：走路動作 (再點看祥龍騰雲🐉)';
                else txt.textContent = '目前：走路擺臂動作 (點擊切換)';
            } else {
                if (currentCode === 'C1') txt.textContent = '目前：🛸 阿純開飛碟追車模式！';
                else if (currentCode === 'C3') txt.textContent = '目前：🧹 阿姨騎魔法掃帚追車模式！';
                else if (currentCode === 'C4') txt.textContent = '目前：🐉 阿嚕騎祥龍騰雲追車模式！';
            }
        }
    }

    window.selectPreviewItem = selectCatalogItem;
    window.toggleCharPoseMode = toggleCharPoseMode;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPreviewGallery);
    } else {
        initPreviewGallery();
    }
})();
