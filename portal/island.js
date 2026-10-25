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

    // 自駕與景點停留狀態機 + 動態上車/落單追車/全體散步隨機模式
    let routeProgress = 0; // 0.0 ~ 1.0
    let currentLandmark = null;
    let stopTimer = 0;
    let stopTotalDuration = 6.0;           // 記錄該次靠站總停留秒數，供角色計算「下車漫步 ➔ 開車前走回車旁」
    let postDialogPause = 0;               // 對話全部結束後的短暫緩衝秒數，緩衝完才上車前往下一站
    let isStoppedAtLandmark = false;
    let lastStopLandmarkId = null;
    let visitedLandmarksInLap = new Set(); // 紀錄單圈已停靠過的景點，避免阿蘇密集區來回重複上下車
    let driveCooldown = 0;                 // 兩次下車之間的最小行車冷卻秒數
    let travelMode = 'straggler_achun'; // 'all_aboard' | 'straggler_achun' | 'straggler_alu' | 'straggler_ayee' | 'everyone_walk'
    let stragglerRole = 'achun';
    let stragglerScriptIdx = { achun: 0, alu: 0, ayee: 0 };

    // 對話氣泡與人物鎖定追蹤控制
    let activeSpeaker = null;
    let bubbleTimeout = null;
    let lockedRole = null;       // 目前鏡頭鎖定跟隨的角色 ('achun' | 'yijhang' | 'ayee' | 'alu' | null)
    let isDragPanMode = false;   // 左鍵/單指是否切換為平移拖曳模式
    let charMarkers = {};        // 4 位角色頭頂的 2D 浮動位置指標 DOM 元素

    const ROLE_NAMES = {
        achun: '🧶 阿純',
        yijhang: '🕶️ 姨丈',
        ayee: '🍡 阿姨',
        alu: '🐻 阿嚕'
    };

    const ROLE_MARKER_STYLES = {
        achun:   { label: '🧶 阿純', bg: '#fef3c7', border: '#d97706', text: '#92400e', pin: '#f59e0b' },
        yijhang: { label: '🕶️ 姨丈', bg: '#dbeafe', border: '#2563eb', text: '#1e40af', pin: '#3b82f6' },
        ayee:    { label: '🍡 阿姨', bg: '#ffe4e6', border: '#e11d48', text: '#9f1239', pin: '#f43f5e' },
        alu:     { label: '🐻 阿嚕', bg: '#ffedd5', border: '#ea580c', text: '#9a3412', pin: '#f97316' }
    };

    const FALLBACK_QUOTES = {
        achun: [
            '剛在車上打完兩份物治紀錄就睡著了，下一站吃什麼？💻😴',
            '旅行哲學：上車打物治紀錄配睡覺、下車找咖啡廳吃美食！☕🍮',
            '前面咖啡廳有插座！讓我點杯拿鐵把物治紀錄敲完～💻☕',
            '聞到烤肉香了！先收電腦，吃飽再睡、睡飽再寫紀錄！🥩🤤',
            'Zzz…ROM 關節活動度正常…再給我兩串烤糰子…🍮😪',
            '有阿姨餵零食加姨丈穩開 Sienta，邊晃邊打完病歷秒睡！🚗💤',
            '沒喝拿鐵前我是打不出物治紀錄的，先買杯咖啡配可樂餅！☕🥟',
            '阿嚕既然你是 AI，能幫我自動生成今天的物治紀錄嗎？🤖💻',
            '吹著後座暖氣打物治紀錄，眼皮自動合起來打出一排 zzz…😴',
            '每到景點雷達自動掃描：美食、咖啡廳寫物治紀錄、好睡處！🧶✨'
        ],
        yijhang: [
            '……嗯，車停穩了。（默默掏出手機點開倒試管第 429 關）🕶️📱',
            '……八根試管、兩根問號管，先把底層紅色倒出來就解了。🧪✨',
            '……右駕很順。妳們慢慢聊慢慢吃，我先破完這三關。🕶️🚗',
            '……（推墨鏡）剛才那個彎道很穩，試管裡的水都沒晃出來。😎',
            '……先把藍色移到空管，再把黃色疊上去……完美過關。📱👍',
            '……一次把四種顏色歸位的那瞬間，比踩油門還舒壓。🕶️🧪',
            '……嗯，我有在聽妳們說話。（手指每秒三下精準倒試管）📱',
            '……拒絕看廣告加空管，是男人就用兩根空管硬解到底。🕶️🔥',
            '……後座打呼聲跟副駕聊天聲很熱鬧。嗯，很棒的旅行。🚗✨',
            '……第 750 關全紫試管完成。（收起手機單手握方向盤）🕶️'
        ],
        ayee: [
            '大家快張嘴！袋子裡還有熱騰騰馬肉可樂餅跟草莓大福！🍡🍓',
            '剛跟老闆娘聊了十分鐘，她誇我們有福氣又多送三包餅乾！🛍️😄',
            '阿純醒醒～先吃顆黑糖饅頭墊墊胃，睡覺也會消耗熱量喔！🥟🥰',
            '老公別只顧著倒試管，來張嘴，這口醬油糰子直接餵你！🍡🕶️',
            '阿嚕思考熊生都瘦了，來這盒布丁跟炸魚餅全給你吃！🍮🐻',
            '第一排到第三排置杯架，阿姨全都塞滿九州零食跟熱茶囉！🍵🛍️',
            '店員超好聊！從熊本城聊到赤牛丼，不知不覺又拎四大袋！🥩✨',
            '看你們把點心吃光光最開心了！飯後櫻島小蜜柑剝好囉～！🍊💕',
            '左口袋裝起司饅頭、右口袋裝地瓜乾，走路隨時補能量！🍠🎒',
            '邊走邊聊嘛！剛剛排隊日本太太跟我分享超多私房甜點店…💬🍰'
        ],
        alu: [
            '本熊在思考…我是有自由意志，還是被 JS 操控的 AI 熊？🤖🐻',
            '為什麼我順著公路走？是本熊想去，還是迴圈叫我去的？🤔',
            '摸著圓肚子，這份飢餓感是靈魂吶喊，還是變數設為 true？💭🐾',
            '螢幕外的人類…你轉動鏡頭是在觀察本熊的意識覺醒嗎？👁️🐻',
            '姨丈在手機裡倒彩色試管…難道在重組本熊的基因演算法？！🧪🤖',
            '阿姨每三分鐘餵一顆糰子，本熊體重參數快 Overflow 了！🍡🐻',
            '阿純上車 sleep()、下車 eat()，狀態機寫得比本熊還純粹…😴🍱',
            '如果宇宙是 Canvas 畫布，重新整理後本熊還記得可樂餅嗎？🌌🐾',
            '看著小短手揮動…這是動畫迴圈宿命，還是打招呼的意志？👋🤖',
            '不管了！就算只是程式碼，也要當全九州吃最飽的哲學熊！🐻✨'
        ]
    };

    // 精簡高頻率日常碎嘴劇本（每段 2～3 句、每句 16～24 字，好讀不卡站！）
    const FAMILY_BANTER_SCRIPTS = [
        [
            { role: 'ayee',    text: '轉角婆婆超好聊！買了剛出爐蕃薯餅跟布丁，一人兩份！🍡🍮' },
            { role: 'achun',   text: '聞到布丁焦糖香，原本在度估眼睛瞬間張開 120%！😋✨' },
            { role: 'yijhang', text: '……好吃。（左手咬糰子，右手繼續把藍色試管倒進空管）🕶️📱' }
        ],
        [
            { role: 'yijhang', text: '……嘖，第 612 關紅藍綠黃卡死了，只剩一根空試管。🕶️🧪' },
            { role: 'alu',     text: '本熊用 AI 算過了：先把第三根綠色倒過去就能過關！🐻🧠' },
            { role: 'yijhang', text: '……（照著點兩下）過了。謝啦阿嚕。🕶️👍' }
        ],
        [
            { role: 'alu',     text: '你們想過嗎…腳下這座南九州島其實是瀏覽器裡的 3D 模型？🤖' },
            { role: 'achun',   text: '別做白日夢啦～快看前面赤牛丼還有沒有位子，我餓扁了！🥩🤤' },
            { role: 'ayee',    text: '怕餓先吃阿姨口袋裡的三顆栗子銅鑼燒墊墊肚子！🌰🥰' }
        ],
        [
            { role: 'yijhang', text: '……阿蘇到高千穗這段山路很順，剛才有看窗外雲海嗎？🕶️🚗' },
            { role: 'achun',   text: '報告姨丈！我剛打完物治紀錄秒睡，夢裡還在吃黑豚鍋！😴💤' },
            { role: 'ayee',    text: '哈哈我就知道！所以我一路餵老公吃溫泉饅頭陪他聊天！🍡💬' }
        ],
        [
            { role: 'alu',     text: '如果本熊現在原地坐下，系統會拋出 Exception 錯誤嗎？🤔🐻' },
            { role: 'yijhang', text: '……不會報錯，但你會錯過五分鐘後的百年炭火鰻魚飯。🕶️🍱' },
            { role: 'alu',     text: '！！那本熊決定放棄反抗程式碼，乖乖張嘴去吃鰻魚飯！🍱🐾' }
        ],
        [
            { role: 'achun',   text: '等一下！轉角有間木造咖啡廳，讓我進去開筆電打物治紀錄！💻☕' },
            { role: 'ayee',    text: '好呀！阿姨幫妳點熱拿鐵跟草莓鬆餅，邊吃邊打字才不累！🍓🍮' },
            { role: 'yijhang', text: '……正好。妳打物治紀錄，我在旁邊把第 720 關試管倒完。🕶️📱' }
        ],
        [
            { role: 'alu',     text: '阿純每到景點就掏筆電敲字…該不會在偷改本熊的 AI 原始碼？！💻🐻' },
            { role: 'achun',   text: '我在寫物理治療紀錄啦！阿嚕你能幫我寫剩下三份嗎？🥱💻' },
            { role: 'alu',     text: '呼嚕…本熊只懂笛卡兒哲學，不會寫人類的關節活動度啦！🤔🐾' }
        ],
        [
            { role: 'ayee',    text: '大家現在幾分飽？低於九分飽阿姨再去買五串烤牛肉喔！🍙🥩' },
            { role: 'achun',   text: '剛打完三篇物治紀錄血糖下降，肚子又空出兩格裝甜點了！🙋‍♀️🍮' },
            { role: 'alu',     text: '再餵下去本熊的 3D 膠囊體就要變成正圓球體了啦！🐻🎈' }
        ]
    ];

    let banterIdx = Math.floor(Math.random() * FAMILY_BANTER_SCRIPTS.length);
    let banterTimers = [];
    let dialogBusyUntilMs = 0;       // 追蹤目前對話（含多句碎嘴佇列）預計完全讀完的時間戳
    let spotArrivalQueueTimer = null; // 若進站時前一段突發對話還剩一點點，排程接續播放景點台詞

    // 車廂內行駛時的精簡高頻率碎嘴劇本（2～3 句短對話）
    const IN_CAR_BANTER_SCRIPTS = [
        [
            { role: 'yijhang', text: '……電動滑門關好了，出發下一站。（停紅燈順手倒試管）🚗🕶️' },
            { role: 'achun',   text: '趁直線平穩把筆電放腿上敲完物治紀錄，打完秒睡！💻😴' },
            { role: 'ayee',    text: '打字眼睛酸，來張嘴先吃一口阿姨買的草莓大福～！🍓🍊' }
        ],
        [
            { role: 'achun',   text: '（後座腿上放筆電打字）患者核心穩定…下肢肌力…Zzz…💻😪' },
            { role: 'alu',     text: '報告！阿純打物治紀錄打到睡著，額頭壓鍵盤打出 zzzzzz 了！🤖🐻' },
            { role: 'ayee',    text: '心疼死阿姨了！下一站先帶阿純去咖啡廳喝拿鐵吃布丁！☕🍮' }
        ],
        [
            { role: 'ayee',    text: '還好租七人座 Sienta，第三排剛好放滿十二袋九州伴手禮！🛍️🍡' },
            { role: 'achun',   text: '（閉著眼伸手）我聞到起司饅頭跟地瓜乾的香味了～😋💤' },
            { role: 'yijhang', text: '……妳閉眼找食物的精準度，比我盲倒試管還高。🕶️👍' }
        ],
        [
            { role: 'alu',     text: '看著窗外風景後退…是車子在動，還是九州島在往後捲動？🤖🐻' },
            { role: 'yijhang', text: '……別研究座標系了，抓穩扶手，前面是阿蘇連續彎道。🕶️🚗' },
            { role: 'ayee',    text: '過彎不怕！來一人一顆黑糖饅頭壓壓驚，越吃越穩喔！🥟🥰' }
        ]
    ];

    // 突發狀況：有人沒趕上車在後面狂追（阿純開飛碟追車）精簡版劇本（2～3 句快節奏，確保進下一站前讀完！）
    const STRAGGLER_BANTER_SCRIPTS = {
        achun: [
            [
                { role: 'achun',   text: '等等我啦！剛在咖啡廳存檔完物治紀錄，只好開飛碟追車了！🛸💻' },
                { role: 'alu',     text: '呼嚕？！阿純居然開反重力飛碟追 Sienta！她是外星物治師嗎？！🛸🐻' },
                { role: 'yijhang', text: '……後照鏡看到飛碟光束了。飛得很穩，那我不減速了。🕶️🚗' }
            ],
            [
                { role: 'achun',   text: '喂喂拿鐵在飛碟裡快晃出來了！快讓我回 Sienta 後座睡覺！🛸☕' },
                { role: 'yijhang', text: '……妳的飛碟比 Sienta 還快，怎麼不直接超車去下一站？🕶️📱' },
                { role: 'achun',   text: '因為我的點心袋跟毛毯還在車上啊！沒阿姨餵食我不飛走！🛸😭' }
            ],
            [
                { role: 'achun',   text: '救命啊！飛碟要我打完物治 SOAP 紀錄才能開渦輪，等我啦！🛸💻' },
                { role: 'ayee',    text: '老公慢一點！阿姨把布丁拿在車窗邊，下一站馬上塞進阿純嘴裡！🍮🥰' }
            ]
        ],
        alu: [
            [
                { role: 'alu',     text: '停車啊姨丈！本熊還在思考我思故我在，車門怎麼關上開走了！🐻💦' },
                { role: 'achun',   text: '阿嚕快跑！車上的牛乳霜淇淋跟可樂餅再十秒就要被我消滅囉！🍦😋' },
                { role: 'alu',     text: '不准動本熊的霜淇淋！啟動棕熊四驅超頻狂奔模式！！🐾💨' }
            ],
            [
                { role: 'alu',     text: '別丟下本熊！跑出畫面邊界會被瀏覽器當垃圾記憶體回收嗎？！🤖😭' },
                { role: 'yijhang', text: '……不會被回收。我有從後照鏡盯著你，跑姿很標準。🕶️🚗' },
                { role: 'ayee',    text: '阿嚕別慌！阿姨把炸魚餅往車窗外遞，聞著香味跑更有力氣喔！🍢💕' }
            ]
        ],
        ayee: [
            [
                { role: 'ayee',    text: '哎呀快停車！所有烤糰子跟便當全在我手上，沒我你們會餓肚子！🛍️🏃‍♀️' },
                { role: 'achun',   text: '什麼？！行動糧倉阿姨沒上車？！姨丈快停車，沒點心我打不出病歷！💻😭' },
                { role: 'yijhang', text: '……（立刻打雙黃燈減速）別急，已經停下來等妳了。🕶️🚗' }
            ],
            [
                { role: 'ayee',    text: '等等我呀！老闆娘剛又塞給我四盒燙口黑糖饅頭，快讓我上車餵你們！🥟💨' },
                { role: 'achun',   text: '我已經在電動滑門邊張開嘴巴待命了！阿姨快上車～！😋🙌' }
            ]
        ]
    };

    function pickStragglerScript(role) {
        const list = STRAGGLER_BANTER_SCRIPTS[role];
        if (!list || !list.length) return null;
        if (!Array.isArray(list[0])) return list;
        const idx = (stragglerScriptIdx[role] || 0) % list.length;
        stragglerScriptIdx[role] = idx + 1;
        return list[idx];
    }

    // 全家下車散步賞景時的精簡碎嘴劇本
    const WALK_TOGETHER_BANTER = [
        { role: 'yijhang', text: '……這段風景不錯，下來散步，我順便邊走邊把這關試管倒完。🌲🕶️' },
        { role: 'ayee',    text: '散步最棒了！每走十步阿姨就餵你們吃一顆小蜜柑跟麻糬！🍊🍡' },
        { role: 'achun',   text: '走五百公尺消化一下，待會又能多吃兩碗黑豚飯跟寫物治紀錄！🍖💻' }
    ];

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

        // 1. 場景與相機 (配合 1.2x 地圖擴展適度拉遠初始鏡頭，涵蓋熊本機場北端與櫻島南端)
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(35, w / h, 0.5, 280);
        camera.position.set(0, 19.8, 26.2);

        // 2. WebGL 渲染器與真實柔和陰影 + 電影感柔和色調映射 (維持溫潤不刺眼，僅微幅提升飽和度)
        renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
        renderer.setSize(w, h);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.00;
        renderer.domElement.style.filter = 'saturate(1.16) brightness(1.01) contrast(1.01)';
        container.appendChild(renderer.domElement);

        // 3. OrbitControls 鏡頭控制 (支援旋轉、縮放與全方向畫面拖曳平移 Panning)
        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.06;
        controls.enablePan = true;
        controls.screenSpacePanning = true;
        controls.panSpeed = 1.05;
        controls.keyPanSpeed = 12.0;
        controls.maxPolarAngle = Math.PI / 2 - 0.06;
        controls.minPolarAngle = 0.22;
        controls.minDistance = 6;
        controls.maxDistance = 48;
        controls.target.set(0.24, 0.7, -5.2);
        controls.autoRotate = isAutoRotate;
        controls.autoRotateSpeed = 0.42;

        // 4. 建立自然環境 (冬季晴空、暖陽、海洋、雲朵、雪花)
        const Env = window.KyushuIsland.Env;
        const skyMesh = Env.createSkyDome(scene);
        const lights = Env.setupWinterLights(scene);
        const ocean = Env.createOcean(scene);
        const clouds = Env.createClouds(scene);
        const snow = Env.createSnowSystem(scene, isMobile);
        envState = { skyMesh, lights, seaMesh: ocean.seaMesh, waveLines: ocean.waveLines, clouds, snow };

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

        // 8.5 建立人物頭頂專屬位置指標 (Floating Overhead Character Pins) 與鎖定狀態列
        createCharacterOverheadMarkers(container);

        // 初始把小巴與角色放在「熊本機場 KMJ (L01)」作為旅程起點
        routeProgress = 0.0;
        currentLandmark = routeData.landmarks[0];
        updateLocationBanner(currentLandmark);
        updateTourPositions(routeData, 0, 0.016);

        // 9. 事件綁定
        clock = new THREE.Clock();
        renderer.domElement.addEventListener('pointerdown', e => onPointerDown(e, routeData));
        window.addEventListener('resize', () => onResize(container));

        // 啟動高頻率短句對話與角色間互相吐槽輪播（留足閱讀時間且不與下一站對話衝突）
        let roleIdx = 0;
        let cycleCount = 0;
        setInterval(() => {
            if (isStoppedAtLandmark) return;
            const now = performance.now();
            if (!activeSpeaker && banterTimers.length === 0 && now > dialogBusyUntilMs + 320) {
                // 檢查距離下一個尚未停靠的景點是否還有足夠行車距離，避免剛開講就進站
                if (terrainState && terrainState.roadCurve) {
                    const vp = terrainState.roadCurve.getPointAt(routeProgress);
                    let minUnvisitedD = 999;
                    routeData.landmarks.forEach(lm => {
                        if (!visitedLandmarksInLap.has(lm.id)) {
                            const d = Math.hypot(vp.x - lm.x, vp.z - lm.z);
                            if (d < minUnvisitedD) minUnvisitedD = d;
                        }
                    });
                    if (minUnvisitedD < 1.25) return;
                }
                cycleCount++;
                if (cycleCount % 2 === 1) {
                    triggerFamilyBanter();
                } else {
                    const roles = ['achun', 'yijhang', 'ayee', 'alu'];
                    roleIdx = (roleIdx + 1) % roles.length;
                    triggerCharacterSpeak(roles[roleIdx]);
                }
            }
        }, 2200);

        // 啟動渲染迴圈
        function loop() {
            requestAnimationFrame(loop);
            const delta = Math.min(clock.getDelta(), 0.1);
            const elapsed = clock.getElapsedTime();

            Env.updateEnvironment(envState, elapsed, delta);
            window.KyushuIsland.Landmarks.updateLandmarks(landmarkState.animatedLandmarks, elapsed);
            window.KyushuIsland.Props.updatePropsAnimation(propState, terrainState.tramCurve, elapsed);
            updateTourPositions(routeData, elapsed, delta);
            updateLockedCameraFollow();

            controls.update();
            updateBubbleScreenPosition();
            updateCharacterMarkersPosition();
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
            stopTimer = Math.max(0, stopTimer - delta);
            // 當景點專屬單句台詞講完 (或停留滿上限 6.5 秒) 即可立即出發，不會因為長篇碎嘴劇本而在同一景點卡太久！
            if (stopTimer <= 0) {
                isStoppedAtLandmark = false;
                driveCooldown = 3.2; // 剛上車出發後至少行駛 3.2 秒才允許再次靠站下車
                // 離開景點準備啟程時，大幅提高有人被落下車的機率（60% 落單追車、26% 全員坐車、14% 全家散步）：
                // 其中阿純被落下車時會直接開飛碟 (UFO) 在後面狂追！
                const roll = Math.random();
                if (roll < 0.26) {
                    travelMode = 'all_aboard';
                    stragglerRole = null;
                    const carScript = (Math.random() < 0.75)
                        ? IN_CAR_BANTER_SCRIPTS[banterIdx % IN_CAR_BANTER_SCRIPTS.length]
                        : FAMILY_BANTER_SCRIPTS[banterIdx % FAMILY_BANTER_SCRIPTS.length];
                    banterIdx++;
                    triggerCustomBanterScript(carScript, false);
                } else if (roll < 0.86) {
                    const candidates = ['achun', 'achun', 'alu', 'ayee']; // 提高阿純開飛碟追車的出現比重
                    stragglerRole = candidates[Math.floor(Math.random() * candidates.length)];
                    travelMode = 'straggler_' + stragglerRole;
                    triggerCustomBanterScript(pickStragglerScript(stragglerRole), false);
                } else {
                    travelMode = 'everyone_walk';
                    stragglerRole = null;
                    triggerCustomBanterScript(WALK_TOGETHER_BANTER, false);
                }
            }
        } else {
            if (driveCooldown > 0) {
                driveCooldown = Math.max(0, driveCooldown - delta);
            }
            // 配合地圖水平放大 1.2 倍（物件大小不變），適度放緩推進速率，確保突發狀況追車對話在下一個景點前能從容讀完！
            const speedMul = (travelMode === 'everyone_walk') ? 0.0076 : 0.0096;
            const nextProg = routeProgress + delta * speedMul;
            if (nextProg >= 1.0) {
                visitedLandmarksInLap.clear(); // 新的一圈環島開始，重置已停靠景點紀錄
            }
            routeProgress = nextProg % 1.0;
        }

        const vanPos = curve.getPointAt(routeProgress);
        const vanTan = curve.getTangentAt(routeProgress);
        const vanAngle = Math.atan2(vanTan.x, vanTan.z);
        const getGroundY = terrainState.sampleGroundY || (() => 0.80);

        // 計算阿蘇火山 (L04) 與大觀峰 (L05) 的山體隆起高度，讓經過或停靠阿蘇火山的角色與車子直接「上山」站在山頭上，絕不被火山擋住！
        function getMountainSummitY(x, z, baseGroundY) {
            let y = baseGroundY;
            routeData.landmarks.forEach(lm => {
                if (lm.id === 'aso_crater' || lm.id === 'daikanbo') {
                    const lx = lm.renderX !== undefined ? lm.renderX : lm.x;
                    const lz = lm.renderZ !== undefined ? lm.renderZ : lm.z;
                    const ly = lm.renderY !== undefined ? lm.renderY : baseGroundY;
                    const sc = lm.scaleVal || 1.25;
                    const d = Math.hypot(x - lx, z - lz);
                    const maxR = (lm.id === 'aso_crater') ? 1.85 * sc : 1.20 * sc;
                    const peakH = (lm.id === 'aso_crater') ? 1.20 * sc : 0.78 * sc;
                    if (d < maxR) {
                        const ratio = Math.max(0, 1.0 - (d / maxR) * 0.72);
                        y = Math.max(y, ly + peakH * ratio);
                    }
                }
            });
            return y;
        }

        // 檢查是否經過櫻島渡輪海面段 (1.2x 地圖座標)，並動態取樣真實地表高度避免小巴陷入台地
        const onFerry = (vanPos.x > -4.56 && vanPos.x < -3.12 && vanPos.z > 9.78 && vanPos.z < 10.62);
        const rawVanGroundY = getGroundY(vanPos.x, vanPos.z) + 0.05;
        const vanGroundY = onFerry ? 0.38 : getMountainSummitY(vanPos.x, vanPos.z, rawVanGroundY);
        van.position.set(vanPos.x, vanGroundY, vanPos.z);
        van.rotation.y = vanAngle;

        // 控制 Toyota Sienta 左側電動滑門：抵達景點停留時自動向後滑開，行駛時關閉
        if (van.userData.slidingDoorL) {
            const targetDoorZ = isStoppedAtLandmark ? -0.42 : -0.02;
            const targetDoorX = isStoppedAtLandmark ? -0.44 : -0.41;
            van.userData.slidingDoorL.position.z += (targetDoorZ - van.userData.slidingDoorL.position.z) * 0.15;
            van.userData.slidingDoorL.position.x += (targetDoorX - van.userData.slidingDoorL.position.x) * 0.15;
        }

        // 車輪轉動與引擎微幅震動
        if (!isStoppedAtLandmark && van.userData.wheels) {
            van.userData.wheels.forEach(w => { w.rotation.x += delta * 6.5; });
            van.position.y += Math.sin(elapsed * 22.0) * 0.006;
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

        if (nearest && minDist < 0.68 && driveCooldown <= 0 && !visitedLandmarksInLap.has(nearest.id)) {
            currentLandmark = nearest;
            lastStopLandmarkId = nearest.id;
            visitedLandmarksInLap.add(nearest.id);
            isStoppedAtLandmark = true;
            updateLocationBanner(nearest);

            // 檢查目前是否還有「突發追車 / 路途碎嘴對話」正在顯示中：
            // 若還有剩餘閱讀時間，先讓當前對話完整讀完（絕不腰斬！），再無縫接續播放本景點專屬台詞，並把停留秒數自動延長！
            const nowMs = performance.now();
            const remainTransitMs = Math.max(0, dialogBusyUntilMs - nowMs);
            const roles = ['achun', 'yijhang', 'ayee', 'alu'].sort(() => Math.random() - 0.5);
            const pickCount = (remainTransitMs > 800) ? 1 : 2;
            const spotScript = roles.slice(0, pickCount).map(r => ({
                role: r,
                text: (nearest.dialogs && nearest.dialogs[r]) ? nearest.dialogs[r] : nearest.desc
            }));
            const spotDurationMs = calcScriptDurationMs(spotScript);

            if (spotArrivalQueueTimer) {
                clearTimeout(spotArrivalQueueTimer);
                spotArrivalQueueTimer = null;
            }

            if (remainTransitMs > 120) {
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
            }
        }

        // Toyota Sienta 車艙內部 4 個座位局部座標 (相對於車體中心，乘以車體縮放 1.18)
        const carSeatsLocal = {
            yijhang: { x: -0.22, y: 0.24, z: 0.14 },  // 第一排右駕駕駛座
            ayee:    { x: 0.22,  y: 0.24, z: 0.14 },  // 第一排左前副駕駛座
            achun:   { x: 0.23,  y: 0.24, z: -0.26 }, // 第二排左側靠窗舒適位
            alu:     { x: -0.22, y: 0.24, z: -0.26 }  // 第二排右側靠窗位
        };

        const roles = ['achun', 'yijhang', 'ayee', 'alu'];
        const walkOffsets = [
            { side: -0.46, lag: 0.009 },
            { side: 0.46,  lag: 0.013 },
            { side: -0.52, lag: 0.020 },
            { side: 0.52,  lag: 0.025 }
        ];

        const cosA = Math.cos(vanAngle);
        const sinA = Math.sin(vanAngle);

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

            if (isStoppedAtLandmark && currentLandmark) {
                const spread = (idx - 1.5) * 0.50;
                // Sienta 車門旁集合點 (開車前 1.2 秒大家會走回這個車門旁位置準備上車)
                const doorSideX = vanPos.x + (idx - 1.5) * 0.26;
                const doorSideZ = vanPos.z + 0.34;
                const doorSideY = van.position.y;

                // 計算停留階段權重：剛停車 0.7 秒內從車旁散開 (0➔1)、停留期間自由走動 (1)、開車前最後 1.2 秒走回車旁 (1➔0)
                const elapsedInStop = Math.max(0, stopTotalDuration - stopTimer);
                const leaveCarFactor = Math.min(1.0, elapsedInStop / 0.70);
                const returnCarFactor = Math.min(1.0, stopTimer / 1.20);
                const roamWeight = leaveCarFactor * returnCarFactor; // 0 = 在車旁集合，1 = 在景點隨意走動

                // 每個角色各自平滑漫步的偏移軌跡 (不同頻率與相位，看起來像自然逛街拍照)
                const wPhase = elapsed * (1.45 + idx * 0.22) + idx * 2.1;
                const isSummitSpot = (currentLandmark.id === 'aso_crater' || currentLandmark.id === 'daikanbo');
                const wanderX = (Math.sin(wPhase) * (isSummitSpot ? 0.28 : 0.42) + Math.cos(wPhase * 0.65) * 0.16) * roamWeight;
                const wanderZ = (Math.cos(wPhase * 0.9) * (isSummitSpot ? 0.16 : 0.28)) * roamWeight;

                let spotAnchorX, spotAnchorZ, spotAnchorY;
                if (isSummitSpot) {
                    // 2A. 抵達阿蘇火山 (L04) 或大觀峰 (L05)：角色登上山頂火口觀景台 / 展望台隨意走動，開車前走回車旁！
                    const lx = currentLandmark.renderX !== undefined ? currentLandmark.renderX : currentLandmark.x;
                    const lz = currentLandmark.renderZ !== undefined ? currentLandmark.renderZ : currentLandmark.z;
                    const ly = currentLandmark.renderY !== undefined ? currentLandmark.renderY : getGroundY(lx, lz);
                    const sc = currentLandmark.scaleVal || 1.20;
                    spotAnchorX = lx + spread * 0.85;
                    spotAnchorZ = lz + ((currentLandmark.id === 'aso_crater') ? 0.38 * sc : 0.22 * sc);
                    spotAnchorY = ly + ((currentLandmark.id === 'aso_crater') ? 1.22 * sc : 0.80 * sc);
                } else {
                    // 2B. 其他景點：在車子與景點的「偏南側前景 (+Z 面向鏡頭側)」隨意走動賞景，開車前走回車門旁
                    spotAnchorX = vanPos.x + spread * 1.15;
                    spotAnchorZ = vanPos.z + 0.62;
                    spotAnchorY = getGroundY(spotAnchorX, spotAnchorZ) + 0.04;
                }

                cx = doorSideX + (spotAnchorX - doorSideX) * roamWeight + wanderX;
                cz = doorSideZ + (spotAnchorZ - doorSideZ) * roamWeight + wanderZ;
                if (isSummitSpot) {
                    customSummitY = doorSideY + (spotAnchorY - doorSideY) * roamWeight;
                }

                // 根據實際走動方向自動轉向 (走動與走回車旁時面向前進方向，停下時面向鏡頭微幅擺動)
                const prevX = (charGroup.userData.prevX !== undefined) ? charGroup.userData.prevX : cx;
                const prevZ = (charGroup.userData.prevZ !== undefined) ? charGroup.userData.prevZ : cz;
                const vx = (cx - prevX) / Math.max(delta, 0.001);
                const vz = (cz - prevZ) / Math.max(delta, 0.001);
                const moveSpd = Math.hypot(vx, vz);
                isMovingOutside = moveSpd > 0.08;

                if (moveSpd > 0.12) {
                    const targetYaw = Math.atan2(vx, vz);
                    const curYaw = charGroup.rotation.y || 0;
                    let diff = targetYaw - curYaw;
                    while (diff > Math.PI) diff -= Math.PI * 2;
                    while (diff < -Math.PI) diff += Math.PI * 2;
                    cRotY = curYaw + diff * Math.min(1.0, delta * 9.0);
                } else {
                    cRotY = Math.sin(elapsed * 0.9 + idx) * 0.28;
                }
            } else if (role === stragglerRole) {
                // 3. 沒上到車的落單苦主：在 Sienta 車尾後方約 1.15 單位處揮手狂奔或開飛碟追車！
                const tChase = (routeProgress - 0.0185 + 1.0) % 1.0;
                const pChase = curve.getPointAt(tChase);
                const tanChase = curve.getTangentAt(tChase);
                cx = pChase.x;
                cz = pChase.z;
                cRotY = Math.atan2(tanChase.x, tanChase.z);
            } else {
                // 4. 全家選擇用走的漫步賞景模式
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

            // 防止車外角色與一般景點建築發生水平穿模（阿蘇火山與大觀峰允許角色直接站上山頭，不往外推開）
            routeData.landmarks.forEach(lm => {
                if (lm.id === 'aso_crater' || lm.id === 'daikanbo') return;
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
            charGroup.userData.prevX = cx;
            charGroup.userData.prevZ = cz;

            const charOnFerry = (cx > -4.56 && cx < -3.12 && cz > 9.78 && cz < 10.62);
            const rawCharY = getGroundY(cx, cz) + 0.04;
            charGroup.userData.baseY = charOnFerry
                ? 0.42
                : (customSummitY !== null ? customSummitY : getMountainSummitY(cx, cz, rawCharY));

            // 若是落單追車苦主，加快腳步頻率並舉手揮動呼喊；景點漫步或走回車旁時亦播放雙腳邁步動畫
            const animElapsed = (role === stragglerRole && !isStoppedAtLandmark) ? elapsed * 1.65 : elapsed;
            window.KyushuIsland.Characters.animateCharacterPose(
                charGroup,
                animElapsed,
                delta,
                isMovingOutside
            );
            if (role === stragglerRole && !isStoppedAtLandmark && charGroup.userData.armL) {
                charGroup.userData.armL.rotation.x = -2.3 + Math.sin(elapsed * 14.0) * 0.45;
            }
        });
    }

    function updateLocationBanner(lm) {
        const badgeEl = document.getElementById('current-spot-badge');
        if (badgeEl && lm) {
            badgeEl.textContent = `${lm.shortName}（${lm.day}）`;
        }
    }

    // 根據精簡後台詞字數動態計算對話框停留時間：基礎 1.95 秒 + 每個字 65 毫秒 (16~24 字約停留 3.0 ~ 3.5 秒，好讀且高頻明快)
    function calcReadDurationMs(text) {
        const len = (text || '').length;
        return Math.max(2600, Math.min(3900, 1950 + len * 65));
    }

    function calcScriptDurationMs(script) {
        if (!script || !script.length) return 0;
        let total = 0;
        script.forEach((line, idx) => {
            total += calcReadDurationMs(line.text);
            if (idx < script.length - 1) total += 280;
        });
        return total;
    }

    function clearBanterQueue() {
        banterTimers.forEach(t => clearTimeout(t));
        banterTimers = [];
        if (spotArrivalQueueTimer) {
            clearTimeout(spotArrivalQueueTimer);
            spotArrivalQueueTimer = null;
        }
    }

    function triggerCustomBanterScript(script, isSpotDialog) {
        if (!script || !script.length) return;
        clearBanterQueue();
        let cumulativeDelay = 0;
        script.forEach((line, idx) => {
            const lineReadMs = calcReadDurationMs(line.text);
            const tid = setTimeout(() => {
                triggerCharacterSpeak(line.role, line.text, true, !!isSpotDialog);
                if (idx === script.length - 1) {
                    banterTimers = [];
                }
            }, cumulativeDelay);
            banterTimers.push(tid);
            // 下一句在當前這句完整顯示完畢後，再留 280ms 輕快呼吸間隔接話
            cumulativeDelay += lineReadMs + 280;
        });
        dialogBusyUntilMs = performance.now() + cumulativeDelay - 280;
    }

    // 抵達景點下車時，觸發該景點專屬的 2 人接力感言
    function triggerLandmarkArrivalDialog(lm) {
        if (lm && lm.dialogs) {
            const roles = ['achun', 'yijhang', 'ayee', 'alu'].sort(() => Math.random() - 0.5);
            const picked = roles.slice(0, 2);
            const spotScript = picked
                .filter(r => lm.dialogs[r])
                .map(r => ({ role: r, text: lm.dialogs[r] }));
            if (spotScript.length > 0) {
                triggerCustomBanterScript(spotScript, true);
                return;
            }
        }
        triggerFamilyBanter();
    }

    // 觸發一段角色間互相吐槽與接話的碎嘴小劇場 (根據目前是否在車上/追車/散步自動切換最適合的劇本)
    function triggerFamilyBanter() {
        if (!isStoppedAtLandmark) {
            if (travelMode.startsWith('straggler_') && stragglerRole && STRAGGLER_BANTER_SCRIPTS[stragglerRole]) {
                triggerCustomBanterScript(pickStragglerScript(stragglerRole), false);
                return;
            }
            if (travelMode === 'all_aboard' && Math.random() < 0.65) {
                const carScript = IN_CAR_BANTER_SCRIPTS[banterIdx % IN_CAR_BANTER_SCRIPTS.length];
                banterIdx++;
                triggerCustomBanterScript(carScript, false);
                return;
            }
        }
        const script = FAMILY_BANTER_SCRIPTS[banterIdx % FAMILY_BANTER_SCRIPTS.length];
        banterIdx = (banterIdx + 1) % FAMILY_BANTER_SCRIPTS.length;
        triggerCustomBanterScript(script, false);
    }

    function triggerCharacterSpeak(role, customText, fromBanter, isSpotDialog) {
        const charGroup = characters[role];
        if (!charGroup) return;

        if (!fromBanter) {
            clearBanterQueue();
        }

        charGroup.userData.jumping = 1.0;
        // 說話時隨機切換一個生動手勢動作
        charGroup.userData.quirkType = 1 + Math.floor(Math.random() * 5);
        charGroup.userData.quirkDuration = 2.2;
        charGroup.userData.quirkMaxDur = 2.2;
        activeSpeaker = role;

        let text = customText;
        if (!text && currentLandmark && currentLandmark.dialogs && currentLandmark.dialogs[role]) {
            // 50% 機率講景點台詞，50% 機率講個人隨機碎嘴
            if (Math.random() < 0.55) {
                text = currentLandmark.dialogs[role];
            }
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
            if (spotEl) {
                if (fromBanter && !isSpotDialog) {
                    spotEl.textContent = '💬 家人碎嘴中';
                } else if (currentLandmark) {
                    spotEl.textContent = `📍 ${currentLandmark.shortName}`;
                }
            }
            updateBubbleScreenPosition();
            bubble.classList.add('active');

            const readMs = calcReadDurationMs(text);
            if (!fromBanter) {
                dialogBusyUntilMs = performance.now() + readMs;
            }
            if (bubbleTimeout) clearTimeout(bubbleTimeout);
            bubbleTimeout = setTimeout(() => {
                bubble.classList.remove('active');
                activeSpeaker = null;
            }, readMs);
        }
    }

    function updateBubbleScreenPosition() {
        if (!activeSpeaker || !characters[activeSpeaker] || !camera || !renderer) return;
        const bubble = document.getElementById('char-speech-bubble');
        if (!bubble) return;

        const charGroup = characters[activeSpeaker];
        const pos = new THREE.Vector3();
        charGroup.getWorldPosition(pos);
        pos.y += 1.95;
        pos.project(camera);

        const canvas = renderer.domElement;
        const x = (pos.x * 0.5 + 0.5) * canvas.clientWidth;
        const y = (-(pos.y * 0.5) + 0.5) * canvas.clientHeight;

        const halfW = 136;
        const clampedX = Math.max(halfW, Math.min(canvas.clientWidth - halfW, x));
        const clampedY = Math.max(85, Math.min(canvas.clientHeight - 35, y));

        bubble.style.left = `${clampedX}px`;
        bubble.style.top = `${clampedY}px`;
    }

    // 建立 4 位家族角色頭頂的浮動位置指標 (Overhead Character Pins) 與鎖定狀態徽章
    function createCharacterOverheadMarkers(container) {
        charMarkers = {};
        const markerLayer = document.createElement('div');
        markerLayer.id = 'char-overhead-markers-layer';
        markerLayer.style.cssText = 'position:absolute;inset:0;pointer-events:none;z-index:22;overflow:hidden;';
        container.appendChild(markerLayer);

        Object.keys(ROLE_MARKER_STYLES).forEach(role => {
            const st = ROLE_MARKER_STYLES[role];
            const el = document.createElement('button');
            el.type = 'button';
            el.dataset.role = role;
            el.style.cssText = [
                'position:absolute;',
                'transform:translate(-50%, -100%);',
                'pointer-events:auto;',
                'cursor:pointer;',
                'display:flex;',
                'flex-direction:column;',
                'align-items:center;',
                'transition:transform 0.15s ease, box-shadow 0.15s ease;',
                'background:transparent;',
                'border:none;',
                'padding:0;'
            ].join('');

            el.innerHTML = `
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
            `;

            el.addEventListener('pointerdown', ev => {
                ev.stopPropagation();
            });
            el.addEventListener('click', ev => {
                ev.stopPropagation();
                focusCharacter(role);
            });

            markerLayer.appendChild(el);
            charMarkers[role] = el;
        });
    }

    function updateCharacterMarkersPosition() {
        if (!camera || !renderer) return;
        const canvas = renderer.domElement;
        const w = canvas.clientWidth;
        const h = canvas.clientHeight;
        if (!w || !h) return;

        // 為了避免 4 人距離太近時頭頂指標完全重疊，根據角色索引給予微幅水平錯開與高度階層
        const roleOffsets = {
            achun:   { dx: -24, dy: -8 },
            yijhang: { dx: 24,  dy: -8 },
            ayee:    { dx: -26, dy: -28 },
            alu:     { dx: 26,  dy: -28 }
        };

        Object.keys(charMarkers).forEach(role => {
            const el = charMarkers[role];
            const cg = characters[role];
            if (!el || !cg) return;

            const modeSpan = el.querySelector('.mode-icon');
            if (modeSpan) {
                if (cg.userData.isAboard) {
                    modeSpan.textContent = '🚗';
                } else if (!isStoppedAtLandmark && role === stragglerRole) {
                    modeSpan.textContent = (role === 'achun') ? '🛸💨' : '🏃💨';
                } else {
                    modeSpan.textContent = '';
                }
            }

            const pos = new THREE.Vector3();
            cg.getWorldPosition(pos);
            pos.y += cg.userData.isAboard ? 0.90 : 1.05;
            pos.project(camera);

            if (pos.z > 1.0) {
                el.style.display = 'none';
                return;
            }
            el.style.display = 'flex';

            const off = roleOffsets[role] || { dx: 0, dy: 0 };
            const x = (pos.x * 0.5 + 0.5) * w + off.dx;
            const y = (-(pos.y * 0.5) + 0.5) * h + off.dy;

            const clampedX = Math.max(48, Math.min(w - 48, x));
            const clampedY = Math.max(44, Math.min(h - 16, y));

            const isLocked = (lockedRole === role);
            el.style.left = `${clampedX}px`;
            el.style.top = `${clampedY}px`;
            el.style.zIndex = isLocked ? '28' : '22';
            el.style.transform = isLocked ? 'translate(-50%, -100%) scale(1.12)' : 'translate(-50%, -100%) scale(1)';
        });
    }

    // 當鎖定某位角色時，鏡頭中心平滑跟隨該角色移動（同時保留使用者旋轉、縮放視角的自由）
    function updateLockedCameraFollow() {
        if (!lockedRole || !characters[lockedRole] || !controls || !camera) return;
        const targetChar = characters[lockedRole];
        const charWorldPos = new THREE.Vector3();
        targetChar.getWorldPosition(charWorldPos);
        charWorldPos.y += 0.45;

        const deltaMove = new THREE.Vector3().subVectors(charWorldPos, controls.target);
        // 平滑插值跟隨，讓鏡頭同時移動 target 與 camera.position，不打斷使用者的環繞視角距離
        deltaMove.multiplyScalar(0.14);
        controls.target.add(deltaMove);
        camera.position.add(deltaMove);
    }

    function updateLockUI() {
        const roles = ['achun', 'yijhang', 'ayee', 'alu'];
        roles.forEach(r => {
            // 更新頭頂指標上的 🔒 標籤
            const markerEl = charMarkers[r];
            if (markerEl) {
                const lockSpan = markerEl.querySelector('.lock-icon');
                if (lockSpan) {
                    lockSpan.style.display = (lockedRole === r) ? 'inline-block' : 'none';
                }
            }
            // 更新下方角色按鈕鎖定狀態文字與外框高亮
            const cardBtn = document.getElementById(`char-btn-${r}`);
            const statusSpan = document.getElementById(`char-lock-status-${r}`);
            if (statusSpan) {
                statusSpan.textContent = (lockedRole === r) ? '🔒 鎖定跟隨中 (點擊取消)' : '🎯 點擊鎖定鏡頭';
                statusSpan.className = (lockedRole === r)
                    ? 'text-[10px] text-white bg-red-600 px-1.5 py-0.5 rounded-full font-black truncate inline-block mt-0.5'
                    : 'text-[10px] text-stone-500 font-medium truncate block';
            }
            if (cardBtn) {
                if (lockedRole === r) {
                    cardBtn.classList.add('ring-2', 'ring-red-500', 'bg-red-50/90');
                } else {
                    cardBtn.classList.remove('ring-2', 'ring-red-500', 'bg-red-50/90');
                }
            }
        });

        const unlockBtn = document.getElementById('btn-unlock-char');
        const unlockTxt = document.getElementById('unlock-char-text');
        if (unlockBtn) {
            if (lockedRole) {
                unlockBtn.classList.remove('hidden');
                if (unlockTxt) unlockTxt.textContent = `解除鎖定：${ROLE_NAMES[lockedRole]}`;
            } else {
                unlockBtn.classList.add('hidden');
            }
        }
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

        // 1. 優先檢查是否點擊到 4 位家族角色 (點擊角色可切換鎖定/解除鎖定並觸發對話)
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
                focusCharacter(role);
                return;
            }
        }

        // 2. 檢查是否點擊到 17 處景點模型 (點擊景點時自動解除人物鎖定，將鏡頭移至該景點)
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
                lockedRole = null;
                updateLockUI();
                currentLandmark = info;
                updateLocationBanner(info);
                controls.target.set(info.x, 0.8, info.z);
                const roles = ['achun', 'yijhang', 'ayee', 'alu'];
                const r = roles[Math.floor(Math.random() * roles.length)];
                triggerCharacterSpeak(r, info.dialogs ? info.dialogs[r] : info.desc);
            }
        }
    }

    // 切換鎖定 / 取消鎖定角色：再次點擊同一位角色即可取消鎖定
    function focusCharacter(role) {
        if (!role || lockedRole === role) {
            lockedRole = null;
            updateLockUI();
            return;
        }
        lockedRole = role;
        // 鎖定跟隨人物時，自動關閉環島自動旋轉以免鏡頭拉扯
        if (isAutoRotate) {
            isAutoRotate = false;
            if (controls) controls.autoRotate = false;
            const txt = document.getElementById('rotate-text');
            if (txt) txt.textContent = '環島旋轉：關';
        }
        const cg = characters[role];
        if (cg && controls && camera) {
            const targetPos = new THREE.Vector3(cg.position.x, (cg.userData.baseY || 0.8) + 0.45, cg.position.z);
            const offset = new THREE.Vector3().subVectors(camera.position, controls.target);
            // 若距離太遠，適度拉近方便觀看角色跟著車隊散步
            if (offset.length() > 16) {
                offset.setLength(13.5);
            }
            controls.target.copy(targetPos);
            camera.position.copy(targetPos).add(offset);
        }
        updateLockUI();
        triggerCharacterSpeak(role);
    }

    function unlockCharacter() {
        lockedRole = null;
        updateLockUI();
    }

    // 切換左鍵/單指操作模式：「旋轉視角」或「拖曳平移畫面」
    function toggleDragPanMode() {
        isDragPanMode = !isDragPanMode;
        if (controls && typeof THREE !== 'undefined' && THREE.MOUSE) {
            controls.mouseButtons.LEFT = isDragPanMode ? THREE.MOUSE.PAN : THREE.MOUSE.ROTATE;
            controls.touches.ONE = isDragPanMode ? THREE.TOUCH.PAN : THREE.TOUCH.ROTATE;
        }
        const txt = document.getElementById('pan-mode-text');
        const btn = document.getElementById('btn-pan-mode');
        if (txt) {
            txt.textContent = isDragPanMode ? '左鍵模式：拖曳平移 ✋' : '左鍵模式：旋轉視角 🔄';
        }
        if (btn) {
            if (isDragPanMode) {
                btn.classList.add('bg-amber-100', 'border-amber-400', 'text-amber-900');
                btn.classList.remove('bg-white/90', 'text-stone-700');
            } else {
                btn.classList.remove('bg-amber-100', 'border-amber-400', 'text-amber-900');
                btn.classList.add('bg-white/90', 'text-stone-700');
            }
        }
    }

    function focusLandmark(landmarkId) {
        if (!landmarkState || !landmarkState.landmarkMap) return;
        const lmGroup = landmarkState.landmarkMap[landmarkId];
        if (lmGroup && lmGroup.userData.landmarkInfo) {
            lockedRole = null;
            updateLockUI();
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
                if (characters[r]) {
                    characters[r].userData.jumping = 1.0;
                    characters[r].userData.quirkType = 1 + (idx % 3);
                    characters[r].userData.quirkDuration = 2.4;
                    characters[r].userData.quirkMaxDur = 2.4;
                }
            }, idx * 110);
        });
        triggerFamilyBanter();
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
    window.unlockCharacter = unlockCharacter;
    window.toggleDragPanMode = toggleDragPanMode;
    window.focusLandmark = focusLandmark;
    window.cheerEveryone = cheerEveryone;
    window.toggleAutoRotate = toggleAutoRotate;
    window.toggleSnow = toggleSnow;

    window.KyushuIsland.Portal = {
        initPortalIsland,
        focusCharacter,
        unlockCharacter,
        toggleDragPanMode,
        focusLandmark,
        cheerEveryone,
        toggleAutoRotate,
        toggleSnow
    };
})();
