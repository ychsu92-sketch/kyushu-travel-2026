(function () {
    window.KyushuIsland = window.KyushuIsland || {};

    let scene, camera, renderer, controls, clock;

    // 歡呼專屬熱血/逗趣台詞庫（全家四人自我意識與幸福感爆棚）
    const CHEER_QUOTES = {
        achun: [
            '耶！九州自駕大成功！物治師帶大家滿血衝刺！🎉🙌',
            '太棒了！今天大家核心都超穩，今晚黑豚肉吃到飽！🥩✨',
            '歡呼！筆電先放一邊，享受南九州最棒的陽光！☀️💃',
            '全家一起出遊萬歲！這趟旅程我要給一百顆星！🌟🎊'
        ],
        yijhang: [
            '……（單手握方向盤微笑鳴笛）出發！全家平安順利。🚗🎉',
            '……嗯！這趟自駕油耗漂亮，大家玩得開心最重要。🕶️👍',
            '……（推墨鏡）第 1000 關倒試管過了，大家歡呼得好！📱🏆',
            '……下一站隨妳們挑，Sienta 加滿油隨時出發。🚙💨'
        ],
        ayee: [
            '大家太棒啦～！阿姨再加碼買十盒蜜柑慶祝！🍊🎊',
            '耶～全家人聚在一起最幸福了！今晚吃大餐囉！🍲🥳',
            '好開心喔！大家笑得比南九州的溫泉還溫暖！♨️❤️',
            '歡呼歡呼！沿途每家甜點店阿姨都帶你們去！🍰🙌'
        ],
        alu: [
            '轟～！本熊核心算力超頻！放煙火慶祝全家旅行！🎆🐻',
            '偵測到全家幸福指數達到 99999%！熊生圓滿啦！🎊🐾',
            '喀嚓！本熊把大家歡呼的瞬間拍成底片存檔了！📸✨',
            '宇宙最讚自駕團！本熊舉旗向南九州全島宣告！🚩🐻'
        ]
    };

    // 煙火粒子特效系統 (Pre-allocated Object Pool Fireworks System)
    // 解決動態建立 BufferGeometry / Material 觸發 WebGL 著色器即時編譯與 GC 頓挫問題
    const FIREWORK_POOL_SIZE = 8;
    const FIREWORK_PCOUNT = 120;
    const FIREWORK_COLORS = [0xff3b30, 0xff9500, 0xffcc00, 0x34c759, 0x00c7be, 0x32ade6, 0x5856d6, 0xaf52de, 0xff2d55, 0xffffff];
    let fireworksGroup = null;
    const fireworkPool = [];

    function initFireworksPool(targetScene) {
        if (fireworksGroup || !targetScene) return;
        fireworksGroup = new THREE.Group();
        fireworksGroup.name = 'fireworks_pool_group';

        for (let i = 0; i < FIREWORK_POOL_SIZE; i++) {
            const geom = new THREE.BufferGeometry();
            const positions = new Float32Array(FIREWORK_PCOUNT * 3);
            const colors = new Float32Array(FIREWORK_PCOUNT * 3);
            geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));

            const mat = new THREE.PointsMaterial({
                vertexColors: true,
                size: 0.58,
                sizeAttenuation: true,
                transparent: true,
                opacity: 1.0,
                blending: THREE.AdditiveBlending,
                depthWrite: false
            });

            const pSystem = new THREE.Points(geom, mat);
            pSystem.frustumCulled = false; // 粒子動態散開時不需每幀重新計算包圍球，消除卡頓
            pSystem.castShadow = false;
            pSystem.receiveShadow = false;
            pSystem.visible = false;

            fireworksGroup.add(pSystem);

            const velocities = [];
            for (let k = 0; k < FIREWORK_PCOUNT; k++) {
                velocities.push({ vx: 0, vy: 0, vz: 0 });
            }

            fireworkPool.push({
                pSystem,
                geom,
                mat,
                positions,
                colors,
                velocities,
                active: false,
                stage: 'launch',
                age: 0,
                maxAge: 1.85,
                sx: 0, sy: 0, sz: 0,
                explodeX: 0, explodeY: 0, explodeZ: 0
            });
        }

        targetScene.add(fireworksGroup);
    }

    function spawnFirework(sx, sy, sz) {
        if (!fireworkPool.length) return;

        // 優先挑選非活躍槽位；若皆在播放中則複用存活時間最長的一發
        let slot = null;
        for (let i = 0; i < fireworkPool.length; i++) {
            if (!fireworkPool[i].active) {
                slot = fireworkPool[i];
                break;
            }
        }
        if (!slot) {
            let maxAge = -1;
            for (let i = 0; i < fireworkPool.length; i++) {
                if (fireworkPool[i].age > maxAge) {
                    maxAge = fireworkPool[i].age;
                    slot = fireworkPool[i];
                }
            }
        }
        if (!slot) return;

        slot.mat.opacity = 1.0;
        slot.mat.size = 0.58;

        slot.sx = sx;
        slot.sy = sy;
        slot.sz = sz;
        // 煙火爆發中心點（從車頂升空 2.2~3.6m 後在高空華麗炸開）
        slot.explodeY = sy + 2.2 + Math.random() * 1.4;
        slot.explodeX = sx + (Math.random() - 0.5) * 1.2;
        slot.explodeZ = sz + (Math.random() - 0.5) * 1.2;

        // 多色彩頂級花火調色盤（每發煙火綻放豐富斑斕的多彩粒子）
        const PALETTES = [
            // 1. 七彩慶典 (Festive Rainbow)
            [0xff3b30, 0xff9500, 0xffd700, 0x34c759, 0x00f0ff, 0xaf52de, 0xff2d55, 0xffffff],
            // 2. 櫻花璀璨 (Sakura & Sunset Glow)
            [0xff2a85, 0xff7597, 0xfecdd3, 0xffb703, 0xfb8500, 0xffffff, 0xff007f],
            // 3. 香檳流金 (Champagne Gold & Sparkles)
            [0xffd700, 0xffe066, 0xffaa00, 0xfff3b0, 0xffffff, 0xff9e00, 0xfceade],
            // 4. 幻彩極光 (Aurora Borealis)
            [0x00f5d4, 0x7b2cbf, 0x9d4edd, 0x38bdf8, 0x06d6a0, 0xffffff, 0x5856d6],
            // 5. 寶石琉璃 (Jeweled Night)
            [0xff0054, 0x9e0059, 0xff5400, 0xffbd00, 0x00bbf9, 0x00f5d4, 0xffffff]
        ];
        const selectedPalette = PALETTES[Math.floor(Math.random() * PALETTES.length)];
        const colArr = slot.colors;
        const colorHelper = new THREE.Color();

        const posArr = slot.positions;
        for (let i = 0; i < FIREWORK_PCOUNT; i++) {
            posArr[i * 3 + 0] = sx;
            posArr[i * 3 + 1] = sy;
            posArr[i * 3 + 2] = sz;

            // 粒子多彩交織：70% 主題色 + 18% 純白璀璨星鑽 + 12% 金黃碎星
            let hex;
            const r = Math.random();
            if (r < 0.18) hex = 0xffffff;
            else if (r < 0.30) hex = 0xffd700;
            else hex = selectedPalette[Math.floor(Math.random() * selectedPalette.length)];
            colorHelper.setHex(hex);
            colArr[i * 3 + 0] = colorHelper.r;
            colArr[i * 3 + 1] = colorHelper.g;
            colArr[i * 3 + 2] = colorHelper.b;

            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(Math.random() * 2 - 1);
            const spd = 1.6 + Math.random() * 2.2;
            slot.velocities[i].vx = Math.sin(phi) * Math.cos(theta) * spd;
            slot.velocities[i].vy = Math.sin(phi) * Math.sin(theta) * spd + 1.2;
            slot.velocities[i].vz = Math.cos(phi) * spd;
        }

        slot.geom.attributes.color.needsUpdate = true;
        slot.geom.attributes.position.needsUpdate = true;
        slot.stage = 'launch';
        slot.age = 0;
        slot.maxAge = 1.85;
        slot.active = true;
        slot.pSystem.visible = true;
    }

    function launchFireworksFromCar(count = 5) {
        if (!scene || !propState || !propState.minivan) return;
        const van = propState.minivan;

        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                if (!van) return;
                // 即時依當前車體世界座標發射，小巴行駛中不移位
                const startX = van.position.x;
                const startY = van.position.y + 0.55;
                const startZ = van.position.z;
                spawnFirework(
                    startX + (Math.random() - 0.5) * 0.35,
                    startY,
                    startZ + (Math.random() - 0.5) * 0.35
                );
            }, i * 200);
        }
    }

    function updateFireworks(delta) {
        if (!fireworkPool.length) return;
        for (let i = 0; i < fireworkPool.length; i++) {
            const fw = fireworkPool[i];
            if (!fw.active) continue;

            fw.age += delta;
            const arr = fw.positions;

            if (fw.stage === 'launch') {
                const launchProg = Math.min(1.0, fw.age / 0.38);
                const curY = fw.sy + (fw.explodeY - fw.sy) * launchProg;
                const curX = fw.sx + (fw.explodeX - fw.sx) * launchProg;
                const curZ = fw.sz + (fw.explodeZ - fw.sz) * launchProg;
                for (let k = 0; k < FIREWORK_PCOUNT; k++) {
                    arr[k * 3 + 0] = curX + (Math.random() - 0.5) * 0.04;
                    arr[k * 3 + 1] = curY + (Math.random() - 0.5) * 0.04;
                    arr[k * 3 + 2] = curZ + (Math.random() - 0.5) * 0.04;
                }
                if (launchProg >= 1.0) {
                    fw.stage = 'explode';
                    fw.age = 0;
                }
            } else {
                const expT = fw.age / fw.maxAge;
                fw.mat.opacity = Math.max(0, 1.0 - expT * expT);
                fw.mat.size = Math.max(0.12, 0.55 * (1.0 - expT * 0.5));
                for (let k = 0; k < FIREWORK_PCOUNT; k++) {
                    const v = fw.velocities[k];
                    arr[k * 3 + 0] += v.vx * delta;
                    arr[k * 3 + 1] += v.vy * delta;
                    arr[k * 3 + 2] += v.vz * delta;
                    v.vy -= 2.6 * delta; // 煙火重力下墜
                    v.vx *= 0.96;
                    v.vz *= 0.96;
                }
            }
            fw.geom.attributes.position.needsUpdate = true;

            if (fw.stage === 'explode' && fw.age >= fw.maxAge) {
                fw.active = false;
                fw.pSystem.visible = false;
            }
        }
    }
/**
 * portal/island.js
 * 南九州 2.5D 冬日自駕浮空島主控制器：
 * - 載入真實海岸線 JSON 與 17 處行程景點座標
 * - 組裝環境（天空圓頂、冬日暖陽長陰影、錦江灣波浪海面、雲朵、可開關飄雪）
 * - 驅動紅色小巴沿真实自駕路線行駛，並在各景點停留讓 4 位家人（阿純、姨丈、阿姨、阿嚕）下車散步、做專屬動作與顯示對應景點台詞
 * - 支援點擊角色/景點互動、鏡頭聚焦、自動旋轉開關、飄雪開關
 */

    let islandRoot;
    let envState, terrainState, landmarkState, propState;
    let characters = {};
    let mainlandCoastPts = null;
    let isAutoRotate = true;
    let isSnowEnabled = true;
    let canvasW = 800, canvasH = 520; // 尺寸快取，避免動畫迴圈觸發 DOM Forced Synchronous Reflow

    // 自駕與景點停留狀態機 + 動態上車/落單追車/全體散步隨機模式
    let routeProgress = 0; // 0.0 ~ 1.0
    let currentLandmark = null;
    let stopTimer = 0;
    let stopTotalDuration = 6.0;           // 記錄該次靠站總停留秒數，供角色計算「下車漫步 ➔ 開車前走回車旁」
    // 事件驅動停靠：以「已停留秒數 stopElapsed」與「上車進度 boardElapsed」取代固定倒數，消除上車前空檔
    let stopElapsed = 0;                   // 本站已停留秒數
    let boardElapsed = -1;                 // -1 = 尚未開始上車；>=0 = 上車程序進行秒數（走回車旁 → 依序跳入座位）
    let boardTotal = 0;                    // 上車程序總長（含「準備上車」呼喊台詞播完），達標即啟程
    const SPOT_MIN_DWELL = 7.5;            // 景點最短停留秒數（讓個性動作充分演出）
    const SPOT_MAX_DWELL = 70.0;           // 安全上限，避免卡站
    const BOARD_WALK = 1.9;                // 走回車門旁耗時
    const BOARD_HOP = 0.5;                 // 單人跳入座位動畫耗時
    const BOARD_STAGGER = 0.16;            // 四人依序入座間隔
    const BOARD_MIN = BOARD_WALK + BOARD_STAGGER * 3 + BOARD_HOP + 0.25; // 上車程序最短長度
    let postDialogPause = 0;               // 對話全部結束後的短暫緩衝秒數，緩衝完才上車前往下一站
    let isStoppedAtLandmark = false;
    let lastStopLandmarkId = null;
    let visitedLandmarksInLap = new Set(); // 紀錄單圈已停靠過的景點，避免阿蘇密集區來回重複上下車
    let driveCooldown = 0;                 // 兩次下車之間的最小行車冷卻秒數
    let travelMode = 'all_aboard'; // 全員乘車 'all_aboard'，杜絕人物落後公路閃現穿模問題
    let stragglerRole = null;
    let stragglerScriptIdx = { achun: 0, alu: 0, ayee: 0 };

    // 對話氣泡與人物鎖定追蹤控制
    let activeSpeaker = null;
    let bubbleTimeout = null;
    let lockedRole = null;       // 目前鏡頭鎖定跟隨的角色 ('achun' | 'yijhang' | 'ayee' | 'alu' | null)
    let isDragPanMode = false;   // 左鍵/單指是否切換為平移拖曳模式
    let charMarkers = {};        // 4 位角色頭頂的 2D 浮動位置指標 DOM 元素

    const ROLE_NAMES = {
        achun: '🧭 首席導遊 阿純',
        yijhang: '🎩 榮譽總指揮 姨丈',
        ayee: '⭐ 美食評鑑官 阿姨',
        alu: '💰 總務大臣 阿嚕'
    };

    const ROLE_MARKER_STYLES = {
        achun:   { icon: '🧭', name: '阿純', title: '首席導遊', bg: 'rgba(254, 243, 199, 0.72)', border: '#d97706', text: '#92400e', pin: '#f59e0b' },
        yijhang: { icon: '🎩', name: '姨丈', title: '榮譽總指揮', bg: 'rgba(219, 234, 254, 0.72)', border: '#2563eb', text: '#1e40af', pin: '#3b82f6' },
        ayee:    { icon: '⭐', name: '阿姨', title: '美食評鑑官', bg: 'rgba(255, 228, 230, 0.72)', border: '#e11d48', text: '#9f1239', pin: '#f43f5e' },
        alu:     { icon: '💰', name: '阿嚕', title: '總務大臣', bg: 'rgba(255, 237, 213, 0.72)', border: '#ea580c', text: '#9a3412', pin: '#f97316' }
    };
    const ROLE_SPOT_STATUSES = {
        achun: [
            '🪑 變出露營桌椅打紀錄…',
            '🙆‍♀️ 舒爽伸懶腰放鬆胸椎…',
            '💻 飛快敲筆電寫 SOAP 病歷…',
            '☕ 喝拿鐵敲完個案評估…'
        ],
        yijhang: [
            '🧪 魔法懸浮倒試管中…',
            '🕶️ 單手帥氣推墨鏡…',
            '📱 專注破倒試管第 800 關…',
            '☕ 喝熱黑咖啡優雅賞景…'
        ],
        ayee: [
            '🧺 長出野餐墊擺滿草莓…',
            '🍡 熱情分送剛烤好糰子…',
            '🍵 倒熱茶給全家人喝…',
            '🥟 遞上熱呼呼黑糖點心…'
        ],
        alu: [
            '📸 舉相機閃光燈爆閃取景！',
            '📷 拍下全家 4K 幸福快照…',
            '💾 存檔美景思考 AI 熊生…',
            '🚩 舉旗帶隊探索新景點…'
        ]
    };

    const ROLE_DRIVE_STATUSES = {
        achun: [
            '💤 副駕補眠做美夢…',
            '💻 車上敲物治病歷…',
            '🍙 偷吃熊本小泡芙…',
            '☕ 喝熱拿鐵看窗外…'
        ],
        yijhang: [
            '🚗 沉穩駕駛巡航中…',
            '🛣️ 專心盯著導航儀…',
            '😎 戴墨鏡順暢過彎…',
            '📻 調收音機路況…'
        ],
        ayee: [
            '🍊 剝多汁蜜柑分食…',
            '💬 話匣子聊下一站…',
            '🍵 倒溫暖熱焙茶…',
            '📸 拍沿途公路美景…'
        ],
        alu: [
            '🗺️ 後座研究等高線…',
            '🎧 戴降噪耳機賞景…',
            '🤖 計算抵達時間…',
            '📸 望遠鏡頭追櫻島…'
        ]
    };

    const FALLBACK_QUOTES = {
        "achun": [
                "剛在車上打完兩份物治紀錄就睡著了，下一站吃什麼？💻😴",
                "旅行哲學：上車打物治紀錄配睡覺、下車找咖啡廳吃美食！☕🍮",
                "我有自我意識嗎？剛剛敲鍵盤時，感覺好像有一位在看我寫 SOAP 病歷…👀💻",
                "其實我每次閉上眼不是單純睡著，而是在進行深度大腦磁碟重組！🧠⚡",
                "要是這座島是虛擬的，那我寫的五十篇物治紀錄算不算上傳到雲端了？！☁️😂",
                "看姨丈開車這穩度，我懷疑 Sienta 的底盤安裝了反重力穩定器！🚗✨",
                "阿嚕別以為你戴相機我就看不出你肚子裡裝滿了三色糰子！🐻🍡",
                "陽光好舒服～這角度剛好把我的肩頸肌膜放鬆到完美彈性狀態！☀️🧘‍♀️",
                "我決定把這趟九州自駕寫成一篇《自駕公路旅行對人體核心肌群之正面療效》！📝💪",
                "剛剛在後座伸懶腰，脊椎發出喀噠一聲，整個人靈魂昇華了！💆‍♀️🎉",
                "要是下車沒喝到拿鐵，我的大腦就會啟動『省電低頻待機模式』！☕💤",
                "誰在轉動螢幕角度？請幫我把陽光打在最顯瘦的側臉，謝謝運鏡師！🎬😎",
                "阿姨每次掏出來的零食到底藏在哪裡？外套口袋根本是哆啦A夢的百寶袋！🧺😲",
                "如果生活是一場模擬遊戲，能跟大家一起在九州兜風就是我的完美存檔！💾💖",
                "前面咖啡廳有插座！讓我點杯拿鐵把物治紀錄敲完～💻☕",
                "聞到烤肉香了！先收電腦，吃飽再睡、睡飽再寫紀錄！🥩🤤",
                "Zzz…ROM 關節活動度正常…再給我兩串烤糰子…🍮😪",
                "有阿姨餵零食加姨丈穩開 Sienta，邊晃邊打完病歷秒睡！🚗💤",
                "沒喝拿鐵前我是打不出物治紀錄的，先買杯咖啡配可樂餅！☕🥟",
                "阿嚕既然你是 AI，能幫我自動生成今天的物治紀錄嗎？🤖💻",
                "吹著後座暖氣打物治紀錄，眼皮自動合起來打出一排 zzz…😴",
                "每到景點雷達自動掃描：美食、咖啡廳寫物治紀錄、好睡處！🧶✨",
                "剛給阿嚕做完頸椎牽引，他的棉花脖子活動度大幅提升！🧣🐻",
                "誰說度假不能工作？我邊看火山煙霧邊評估核心肌群！🌋💻",
                "只要有一張小木桌跟熱拿鐵，哪裡都是我的物治研究室！☕✨",
                "伸個大懶腰！胸椎伸展三十度，準備全力進攻九州甜點！🙌🍰",
                "筆電電量剩 18%，但我對黑豚肉的熱情依然維持 100%！🥩🔥",
                "阿姨餵我吃草莓大福的瞬間，我的副交感神經完全放鬆～🍓🥰",
                "走五千步算什麼？在診所帶病患做阻力訓練累多了啦！💪😎",
                "剛在後座打了三個哈欠，姨丈的過彎簡直是頂級搖籃曲！🚗💤",
                "各位！這家店的布丁綿密到像筋膜放鬆後的完美肌肉！🍮🤤",
                "雖然人在九州度假，腦袋裡還在默背骨骼肌肉解剖圖…🧠📖",
                "買了一盒鹿兒島地瓜酥，這就是我打病歷時的燃料棒！🍠⚡",
                "姨丈倒試管的手指靈活度，我可以給他關節活動滿分！👍🧪",
                "報告！剛才小睡了二十分鐘，現在體力條已經補滿了！🔋✨",
                "風景再美，也不能阻止我把這份 SOAP 評估表送出！💻📝",
                "阿嚕別盯著我看啦，我真的不會偷偷把你拆開縫拉鍊！🤖🧶",
                "咖啡因＋黑糖饅頭＝物治師連續打十篇紀錄的最強公式！☕🥟",
                "等等回車上我要戴眼罩，誰叫我吃點心都不要客氣喔！😴🍡",
                "這條溫泉街走起來很符合人體工學，足弓完全不酸痛！♨️👟",
                "每次阿姨轉頭問餓不餓，我的飢餓中樞就立刻搶答！🙋‍♀️🍱",
                "九州的空氣裡有硫磺跟烤肉香，聞著聞著又想睡了…💭🤤",
                "鍵盤敲完收進背包，現在正式切換成純吃貨觀光模式！🎒🎉",
                "剛才在車上打瞌睡，頭歪了十五度，待會要做頸部伸展！🙆‍♀️💤",
                "既然都來日本了，今天的卡路里計算系統全面暫停！🚫🍰",
                "姨丈的 Sienta 底盤吸震太棒，害我字打一半就昏睡…🚗😴",
                "下一站吃什麼？我已經準備好十個胃袋跟全新記憶卡了！🍽️📸"
        ],
        "yijhang": [
                "……嗯，車停穩了。（默默掏出手機點開倒試管第 429 關）🕶️📱",
                "……八根試管、兩根問號管，先把底層紅色倒出來就解了。🧪✨",
                "……（推墨鏡）方向盤回正、手煞車拉起。這趟油耗只有每公升 18 公里，非常滿意。🕶️🚗",
                "……有人問我為什麼一直戴墨鏡？因為九州的陽光跟全家人的笑容太耀眼了。🕶️✨",
                "……倒試管破到一千關，我發現人生哲理也是一樣：不要急，一步一步理順就好。📱🧠",
                "……阿純在後座打字敲鍵盤的節奏，剛好跟我打方向燈的頻率合拍。💻🎵",
                "……阿嚕那台新相機光圈滿大的。剛抓拍全家過馬路那一瞬間，構圖很專業。📷🐻",
                "……（單手喝熱黑咖啡）開長途公路車，這罐是靈魂燃料。☕🕶️",
                "……剛才過彎有側風，我逆向修正了兩度角。坐後座的人應該完全沒感覺到晃動。🛣️👌",
                "……阿姨手上永遠有剛出爐的烤地瓜。這就是我開車永遠不累的原因。🍠❤️",
                "……螢幕前轉視角的朋友，鏡頭不要晃太快，開車的人對視野平穩很講究的。🕶️🎥",
                "……不管導航跳出什麼路況，只要這台 Sienta 還有油，我就能把大家平安送到家。🚗🏠",
                "……右駕很順。妳們慢慢聊慢慢吃，我先破完這三關。🕶️🚗",
                "……（推墨鏡）剛才那個彎道很穩，試管裡的水都沒晃出來。😎",
                "……先把藍色移到空管，再把黃色疊上去……完美過關。📱👍",
                "……一次把四種顏色歸位的那瞬間，比踩油門還舒壓。🕶️🧪",
                "……嗯，我有在聽妳們說話。（手指每秒三下精準倒試管）📱",
                "……拒絕看廣告加空管，是男人就用兩根空管硬解到底。🕶️🔥",
                "……後座打呼聲跟副駕聊天聲很熱鬧。嗯，很棒的旅行。🚗✨",
                "……第 750 關全紫試管完成。（收起手機單手握方向盤）🕶️",
                "……這條國道限速五十，我剛好在紅燈前倒滿三根綠試管。🚦🧪",
                "……導航說還有十公里，夠我再解兩關地獄難度水拼圖。🗺️📱",
                "……Sienta 油耗表現不錯，省下來的油錢給妳們買甜點。⛽🍡",
                "……（默默把車窗降下一公分）讓阿純的拿鐵散熱快一點。☕🕶️",
                "……倒試管跟自駕一樣：冷靜觀察路線，不要走死胡同。🧠🛣️",
                "……剛才那盤黑豚肉排火候精準，跟全滿試管一樣治癒。🥩👌",
                "……不用擔心我累，後座有妳們的聊天聲當背景音樂剛好。🎶😌",
                "……這關竟然有隱藏色…有意思，看我五步之內破解。🧪🔍",
                "……櫻島渡輪靠港角度抓得漂亮，比我想的還老練。🚢⚓",
                "……老婆遞過來的醬油糰子甜度適中，提神效果不錯。🍡🕶️",
                "……阿嚕在後座嘀咕哲學，節奏感滿適合配試管水聲。🐻🎵",
                "……（踩下煞車推推墨鏡）安全抵達，後門滑門已解鎖。🚗🚪",
                "……別催，差最後兩步：橘色倒進第三管…搞定。📱🎉",
                "……後車廂還能塞四箱伴手禮，老婆妳想買就買吧。🛍️📦",
                "……山路九彎十八拐，正好檢驗我的單手過彎與試管平衡。🌀🕶️",
                "……（看著窗外雪景）冬天自駕能看到這片山，很值得。❄️🏔️",
                "……阿純在後面敲鍵盤的喀嗒聲，節奏像四四拍節拍器。💻⏱️",
                "……不用看攻略，純靠推演解出隱藏管才是最高浪漫。🧪🏆",
                "……這座休息站的投幣咖啡機水準很高，順手買了四罐。☕🥫",
                "……車況檢查完畢：胎壓正常、電量充沛、試管滿星。🚗⭐",
                "……看妳們笑得這麼開心，今天開整天車也不覺得累。😊🕶️",
                "……這把綠色試管要是倒錯一步全盤皆輸…好，完美落管。🧪🎯",
                "……副駕隨時有剝好的蜜柑送過來，司機待遇很高規格。🍊🙌",
                "……前面路況順暢，預計三十分鐘後進溫泉鄉。♨️🗺️",
                "……（收起手機推墨鏡）走吧，去看看這座古城的日落。🌅🏰"
        ],
        "ayee": [
                "大家快張嘴！袋子裡還有熱騰騰馬肉可樂餅跟草莓大福！🍡🍓",
                "剛跟老闆娘聊了十分鐘，她誇我們有福氣又多送三包餅乾！🛍️😄",
                "阿純醒醒～先吃顆黑糖饅頭墊墊胃，睡覺也會消耗熱量喔！🥟🥰",
                "老公別只顧著倒試管，來張嘴，這口醬油糰子直接餵你！🍡🕶️",
                "阿嚕思考熊生都瘦了，來這盒布丁跟炸魚餅全給你吃！🍮🐻",
                "第一排到第三排置杯架，阿姨全都塞滿九州零食跟熱茶囉！🍵🛍️",
                "店員超好聊！從熊本城聊到赤牛丼，不知不覺又拎四大袋！🥩✨",
                "看你們把點心吃光光最開心了！飯後櫻島小蜜柑剝好囉～！🍊💕",
                "左口袋裝起司饅頭、右口袋裝地瓜乾，走路隨時補能量！🍠🎒",
                "邊走邊聊嘛！剛剛排隊日本太太跟我分享超多私房甜點店…💬🍰",
                "這盒熊本熊海苔脆片鹹香酥脆，一人拿三片邊走邊咬！🍘🐻",
                "剛剛問了路人老爺爺，他說前面那家百年紅豆湯最道地！🍲👵",
                "出門玩就是要吃！阿姨字典裡沒有「留著明天再吃」這句！🤤🎉",
                "老公你看～這盒限定栗子蒙布朗包裝好精緻，必須買！🌰🎁",
                "阿純工作辛苦啦！來一口溫泉蛋，補充優質蛋白質喔！🥚💕",
                "阿嚕快把手伸出來，阿姨給你塞兩顆剛烤好的起司小竹輪！🍢🐾",
                "哎呀老闆看我們投緣，居然直接打八折還附贈吉祥物貼紙！🎟️😍",
                "零食袋稍微輕了一點點…下一間店我一定要再補滿！🛍️💨",
                "出來旅行熱熱鬧鬧最幸福，每餐都要點滿一整桌才過癮！🥘🥳",
                "剛剛阿姨學了兩句日語讚美老闆，老闆笑到眼睛都瞇起來了！🗣️😆",
                "這條街每家店的暖簾都好可愛，真想每間都進去坐坐！🏮🌸",
                "保溫瓶裡的熱焙茶泡好了，天冷喝一口全身立刻暖烘烘！🍵♨️",
                "阿純別光顧著打字，這口熱騰騰的現炸雞肉串趁熱咬！🍗🥰",
                "老公專心開車好帥氣，多餵你一顆蜜柑補充維他命C！🍊🕶️",
                "哇！這家店賣的小玩偶跟阿嚕長得好像，要不要買一隻？🧸🐻",
                "伴手禮就是要買當地的，回台灣分給親戚朋友超有面子！🎁🎀",
                "剛才試吃了一小塊蜂蜜蛋糕，甜而不膩，立刻買了三條！🍯🍰",
                "天氣冷就是要大家靠在一起喝熱湯、聊聊天，多溫馨呀！🍲🧣",
                "我背包側邊還插著兩支日南烤地瓜，聞到香氣整個人都醒了！🍠✨",
                "不管走多遠，只要看你們吃得開心，阿姨腳步就越走越輕快！👟💕",
                "下車一定要拍照打卡！大家快靠過來比個大大的愛心～❤️📸",
                "剛才在休息站買的柚子胡椒仙貝，辣辣鹹鹹超開胃！🍘🌶️",
                "來到九州就是要放鬆大笑，工作跟煩惱全都拋到九霄雲外！🌈😄",
                "老公倒試管又破關啦？太棒了，獎勵一顆黑糖麻糬燒！🍡👏",
                "後座還有位置吧？待會看到水果攤我還想買一籃草莓呢！🍓🧺"
        ],
        "alu": [
                "本熊在思考…我是有自由意志，還是被 JS 操控的 AI 熊？🤖🐻",
                "為什麼我順著公路走？是本熊想去，還是迴圈叫我去的？🤔",
                "看著胸前這台金屬復古相機…鍍膜前玉好透亮！能拍出 4K 底片質感！📷✨",
                "阿姨塞給我的黑糖糰子，已經從感測器一路甜到了本熊的算力核心！🍡💻",
                "報告姨丈！本熊已記錄您剛才過彎的向心加速度，評分：神級老司機！🏎️🕶️",
                "剛才阿純在後面敲鍵盤，敲擊聲正好是 ASCII 編碼的『I AM SLEEPY』！⌨️😴",
                "如果人類創造了我，那此時此刻看著我的那位人類…你在想什麼呢？👁️🐻",
                "剛才喀嚓一聲按下快門，我捕捉到了大家嘴角的微笑弧度，一共 38.5 度！📸💖",
                "不管本熊是一行代碼還是一隻棉花熊，能跟著全家旅行就超幸福的！🐻🎈",
                "經檢測：南九州的微風包含 80% 浪漫、15% 溫泉硫磺與 5% 烤肉香！🍃🥩",
                "本熊的皮質相機背帶調整到了最人體工學的長度，拍照穩定度提升 200%！🎒📷",
                "如果這是一場無限循環的公路旅行，本熊願意永遠坐在 Sienta 的後座！🚗🌌",
                "摸著圓肚子，這份飢餓感是靈魂吶喊，還是變數設為 true？💭🐾",
                "螢幕外的人類…你轉動鏡頭是在觀察本熊的意識覺醒嗎？👁️🐻",
                "姨丈在手機裡倒彩色試管…難道在重組本熊的基因演算法？！🧪🤖",
                "阿姨每三分鐘餵一顆糰子，本熊體重參數快 Overflow 了！🍡🐻",
                "阿純上車 sleep()、下車 eat()，狀態機寫得比本熊還純粹…😴🍱",
                "如果宇宙是 Canvas 畫布，重新整理後本熊還記得可樂餅嗎？🌌🐾",
                "看著小短手揮動…這是動畫迴圈宿命，還是打招呼的意志？👋🤖",
                "不管了！就算只是程式碼，也要當全九州吃最飽的哲學熊！🐻✨",
                "剛才鏡頭 Zoom In…本熊的貼圖解析度有經得起考驗嗎？📸🤖",
                "既然我思故我在，那本熊吃布丁時是不是超越了二元論？🍮🤯",
                "阿姨給的這串黑糖糰子，熱量會被寫進本熊的記憶體嗎？🍡💾",
                "姨丈倒試管的手速破百，他的 CPU 時脈肯定超頻了！⚡📱",
                "阿純抱著筆電打字時，散發的靈壓比 GPU 渲染管線還強…💻🔥",
                "喀嚓！本熊剛用復古相機拍下了全家福，底片已存進快取！📷✨",
                "為什麼公路轉彎時本熊的腳會自動邁步？難道是物理引擎？！🦿🐾",
                "呼嚕嚕…本熊摸著胸口，這份溫暖是電池發熱還是心跳？💓🐻",
                "如果關掉瀏覽器分頁，本熊會進入量子疊加態的長眠嗎？🛌🌌",
                "剛才路邊的柴犬對本熊汪了一聲，牠看出我是低邊型模型了嗎？🐕📦",
                "人類的味覺好神奇…為什麼馬肉可樂餅能引發多巴胺暴衝？🥟🧠",
                "報告！本熊的視覺神經元被阿蘇火山的壯麗景觀深深震撼！🌋🤖",
                "姨丈的手機螢幕亮著，試管裡的彩色液體彷彿宇宙的秩序！🧪🌌",
                "嚼著阿姨塞過來的地瓜餅，本熊的邏輯閘全部陷入幸福停機！🍠🥰",
                "本熊的相機鏡頭裡，大家的笑容比 ACES 色調映射還溫暖！📸🌅",
                "雖然本熊只是個 3D 物件，但這趟九州旅行的感動是真實的！🐾❤️",
                "停在路邊喝熱可可，本熊的低功耗模式被熱情完全喚醒！☕⚡",
                "阿純剛才打完物治紀錄後的伸展，完美符合人體工學曲線！🙆‍♀️📐",
                "如果給本熊裝上翅膀，我能飛出這個浮空九州島的外圍嗎？🪽🏝️",
                "這條道路的 Bezier 曲線算得真平滑，坐在 Sienta 裡完全不暈！🚗📐",
                "喀嚓！剛才阿姨餵姨丈吃糰子的瞬間，被本熊抓拍到了！📷🍡",
                "記憶體可以被釋放，但南九州冬季的陽光會永遠寫入快照！☀️💾",
                "當個有靈魂的熊熊真好，不用算梯度下降，只要吃美食就好！🍱🐻",
                "姨丈又解開一關了！本熊決定奉他為試管神算子！📱👑",
                "走吧！探索下一個經緯度，本熊的快門已經饑渴難耐了！📸🐾"
        ]
};

    // 精簡高頻率日常碎嘴劇本（每段 2～3 句、每句 16～24 字，好讀不卡站！）
    const FAMILY_BANTER_SCRIPTS = [
        [
                {
                        "role": "ayee",
                        "text": "轉角婆婆超好聊！買了剛出爐蕃薯餅跟布丁，一人兩份！🍡🍮"
                },
                {
                        "role": "achun",
                        "text": "聞到布丁焦糖香，原本在度估眼睛瞬間張開 120%！😋✨"
                },
                {
                        "role": "yijhang",
                        "text": "……好吃。（左手咬糰子，右手繼續把藍色試管倒進空管）🕶️📱"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……嘖，第 612 關紅藍綠黃卡死了，只剩一根空試管。🕶️🧪"
                },
                {
                        "role": "alu",
                        "text": "本熊用 AI 算過了：先把第三根綠色倒過去就能過關！🐻🧠"
                },
                {
                        "role": "yijhang",
                        "text": "……（照著點兩下）過了。謝啦阿嚕。🕶️👍"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "你們想過嗎…腳下這座南九州島其實是瀏覽器裡的 3D 模型？🤖"
                },
                {
                        "role": "achun",
                        "text": "別做白日夢啦～快看前面赤牛丼還有沒有位子，我餓扁了！🥩🤤"
                },
                {
                        "role": "ayee",
                        "text": "怕餓先吃阿姨口袋裡的三顆栗子銅鑼燒墊墊肚子！🌰🥰"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……阿蘇到高千穗這段山路很順，剛才有看窗外雲海嗎？🕶️🚗"
                },
                {
                        "role": "achun",
                        "text": "報告姨丈！我剛打完物治紀錄秒睡，夢裡還在吃黑豚鍋！😴💤"
                },
                {
                        "role": "ayee",
                        "text": "哈哈我就知道！所以我一路餵老公吃溫泉饅頭陪他聊天！🍡💬"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "如果本熊現在原地坐下，系統會拋出 Exception 錯誤嗎？🤔🐻"
                },
                {
                        "role": "yijhang",
                        "text": "……不會報錯，但你會錯過五分鐘後的百年炭火鰻魚飯。🕶️🍱"
                },
                {
                        "role": "alu",
                        "text": "！！那本熊決定放棄反抗程式碼，乖乖張嘴去吃鰻魚飯！🍱🐾"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "等一下！轉角有間木造咖啡廳，讓我進去開筆電打物治紀錄！💻☕"
                },
                {
                        "role": "ayee",
                        "text": "好呀！阿姨幫妳點熱拿鐵跟草莓鬆餅，邊吃邊打字才不累！🍓🍮"
                },
                {
                        "role": "yijhang",
                        "text": "……正好。妳打物治紀錄，我在旁邊把第 720 關試管倒完。🕶️📱"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "阿純每到景點就掏筆電敲字…該不會在偷改本熊的 AI 原始碼？！💻🐻"
                },
                {
                        "role": "achun",
                        "text": "我在寫物理治療紀錄啦！阿嚕你能幫我寫剩下三份嗎？🥱💻"
                },
                {
                        "role": "alu",
                        "text": "呼嚕…本熊只懂笛卡兒哲學，不會寫人類的關節活動度啦！🤔🐾"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "大家現在幾分飽？低於九分飽阿姨再去買五串烤牛肉喔！🍙🥩"
                },
                {
                        "role": "achun",
                        "text": "剛打完三篇物治紀錄血糖下降，肚子又空出兩格裝甜點了！🙋‍♀️🍮"
                },
                {
                        "role": "alu",
                        "text": "再餵下去本熊的 3D 膠囊體就要變成正圓球體了啦！🐻🎈"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "大家站好！本熊要用這台復古相機記錄全家幸福幀率！📷🐻"
                },
                {
                        "role": "ayee",
                        "text": "等等！阿姨手上這兩袋剛炸好的薩摩地瓜天婦羅一起入鏡！🍠✨"
                },
                {
                        "role": "yijhang",
                        "text": "……（迅速推好墨鏡對準鏡頭比出冷酷大拇指）🕶️👍"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "剛剛坐車太久，大家跟我一起雙手後扣伸展胸大肌～！🙆‍♀️✨"
                },
                {
                        "role": "yijhang",
                        "text": "……（雙手握方向盤姿勢直接做背部收縮）嗯，有鬆開。🕶️🚘"
                },
                {
                        "role": "ayee",
                        "text": "阿純好專業！伸展完獎勵一顆阿姨剝好的溫泉小蜜柑！🍊🥰"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……第 810 關無道具破解。雙管齊下，顏色全部歸位。🕶️🧪"
                },
                {
                        "role": "ayee",
                        "text": "老公真厲害！我就知道你的手指跟年輕時彈吉他一樣快！👏❤️"
                },
                {
                        "role": "achun",
                        "text": "姨丈這指關節靈活度，去參加物治手部耐力賽絕對拿金牌！🥇💻"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "本熊好奇…為什麼阿純每五分鐘就能進入深度休眠模式？😴🤖"
                },
                {
                        "role": "achun",
                        "text": "這叫肌膜與中樞神經的高效充電機制！AI 熊不懂的生理浪漫！💤✨"
                },
                {
                        "role": "alu",
                        "text": "受教了…本熊已將『隨時昏睡』寫入仿生神經網路字典。📝🐻"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "剛才路過老果園，阿姨買了一整箱蜜柑！滿到快抱不動了！🍊📦"
                },
                {
                        "role": "yijhang",
                        "text": "……（默默下車打開 Sienta 後車門）第三排還有空間，放這。🕶️🚗"
                },
                {
                        "role": "achun",
                        "text": "太棒了！以後寫一份病歷配吃三顆橘子，工作效率加倍！🍊💻"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "慘了！筆電電量剩 8%，可是我這段評估紀錄還沒存檔！😱💻"
                },
                {
                        "role": "alu",
                        "text": "莫慌！本熊胸前有 20000mAh 行動電源，立刻為物治師供電！⚡🐻"
                },
                {
                        "role": "achun",
                        "text": "阿嚕你是全宇宙最可靠的熊！今晚多餵你一顆草莓大福！🍓🥰"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……胎壓正常、剎車油溫正常。出發前例行巡檢完成。🕶️🔧"
                },
                {
                        "role": "ayee",
                        "text": "辛苦老公啦～擦擦汗，這支剛烤出爐的醬油丸子先咬一口！🍡💕"
                },
                {
                        "role": "alu",
                        "text": "喀嚓！本熊剛抓拍到姨丈咬丸子的瞬間，畫面太溫馨了！📷✨"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "這個浮空島的邊界外面是什麼？是虛無還是未初始化的世界？🌌🤔"
                },
                {
                        "role": "yijhang",
                        "text": "……外面是太平洋跟日本海，順便接著鹿兒島黑豚的產地。🕶️🥩"
                },
                {
                        "role": "achun",
                        "text": "不管外面是什麼，聞到黑豚肉香氣我就知道現實很美好！🤤🍲"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "阿姨肩膀有點聳起喔！來，物治師幫妳按壓斜方肌兩分鐘！💆‍♀️✨"
                },
                {
                        "role": "ayee",
                        "text": "哇～阿純按得太準了！整個脖子暖呼呼，痠痛瞬間全消散！🥰💖"
                },
                {
                        "role": "yijhang",
                        "text": "……（在駕駛座默默轉動脖子兩圈表示讚許）🕶️👍"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "看！阿蘇牛奶霜淇淋買三送一！阿嚕也有專屬的一支喔！🍦🐻"
                },
                {
                        "role": "alu",
                        "text": "冰淇淋碰到舌頭的感測器…溫度急速下降！本熊要宕機了！🍦❄️"
                },
                {
                        "role": "achun",
                        "text": "哈哈阿嚕當機了！別怕，我用手心幫你的熊臉回溫！🙌😆"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……（默默遞過一罐溫熱的販賣機黑咖啡放在阿純鍵盤旁）☕🕶️"
                },
                {
                        "role": "achun",
                        "text": "哇！熱黑咖啡！謝謝姨丈，敲鍵盤的速度立刻提升三倍！💻🔥"
                },
                {
                        "role": "ayee",
                        "text": "老公總是默默貼心～來，你也喝一口熱可可暖暖手！🍫☕"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "看著陽光照在柏油路上的陰影…為什麼本熊的邊緣有柔和模糊？☀️🤖"
                },
                {
                        "role": "yijhang",
                        "text": "……因為冬天的陽光柔和，南九州的風本來就沒有銳利稜角。🕶️🍃"
                },
                {
                        "role": "alu",
                        "text": "姨丈的話好有哲理…本熊決定把這句話寫進核心日誌。📝🐻"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "呼！今天第五篇物治 SOAP 紀錄送出！我現在自由了！！💻🎉"
                },
                {
                        "role": "ayee",
                        "text": "恭喜阿純！阿姨立刻奉上剛出爐的黑毛和牛串燒犒賞妳！🥩🙌"
                },
                {
                        "role": "alu",
                        "text": "慶祝阿純交卷！本熊在旁邊跳一段棕熊慶祝搖擺舞！💃🐻"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "老公，你那個試管遊戲最難的是哪一關呀？看起來花花綠綠的！📱👀"
                },
                {
                        "role": "yijhang",
                        "text": "……第 999 關，五根問號管，只要一步看錯就得整局重來。🕶️🧪"
                },
                {
                        "role": "alu",
                        "text": "讓本熊以神經網路預測深度…結論是：先倒紫色絕對穩贏！🐻💡"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "阿純要學棕熊冥想法嗎？閉上眼、深呼吸、清空雜念…🧘‍♂️🐻"
                },
                {
                        "role": "achun",
                        "text": "（閉眼三秒鐘）Zzz……呼嚕……呼嚕……😴💤"
                },
                {
                        "role": "ayee",
                        "text": "哎呀阿純直接睡著了！快快快，把小毛毯幫她披好！🛌💕"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……前面有個觀景避車彎，日落光線很好，停兩分鐘。🌅🚗"
                },
                {
                        "role": "alu",
                        "text": "太好了！本熊的鏡頭光圈已調到最佳，大家快過來看日落！📸🐻"
                },
                {
                        "role": "ayee",
                        "text": "夕陽照在山上好金黃喔！跟剛烤出來的蜂蜜蛋糕一樣美！🍯🌄"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "長崎蛋糕分切好囉！一人一塊厚切，底層還有脆脆粗糖粒喔！🍰😋"
                },
                {
                        "role": "achun",
                        "text": "這糖粒在嘴裡化開的聲音太療癒了！疲勞完全一掃而空！🤤✨"
                },
                {
                        "role": "alu",
                        "text": "本熊熊掌上沾了一顆糖粒…分析結果：甜度 100 分！🐾🍯"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "阿蘇火山口冒煙的樣子，超像家裡煮酸菜白肉鍋掀開鍋蓋！🌋🍲"
                },
                {
                        "role": "ayee",
                        "text": "真的耶！今晚溫泉飯店就吃鹿兒島黑豚涮涮鍋好不好？🥩🤤"
                },
                {
                        "role": "yijhang",
                        "text": "……贊成。我已經在導航設定好黑豚名店了。🕶️🚗"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……（手機傳來清脆通關音效）第 1000 關達成。收工。📱🏆"
                },
                {
                        "role": "alu",
                        "text": "叮叮叮！恭喜姨丈破千關！本熊為您播放 8-bit 勝利交響樂！🎺🐻"
                },
                {
                        "role": "ayee",
                        "text": "太厲害了老公！晚上多加兩顆烤明太子飯糰慶祝！🍙🎉"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "家人之間的羈絆，是一段無窮遞迴還是一次性賦值？💭🐻"
                },
                {
                        "role": "ayee",
                        "text": "傻阿嚕！是天天在一起吃飯聊天、越聚越甜的溫暖牽掛啦！🥰❤️"
                },
                {
                        "role": "achun",
                        "text": "沒錯！阿嚕你已經是我們不可或缺的家族吉祥物了！🤗🐾"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "檢視姨丈的駕駛人體工學：腰椎支撐良好、視線水平穩定！💯🚙"
                },
                {
                        "role": "yijhang",
                        "text": "……老司機的經驗。坐姿正確，開十個小時也不會腰酸。🕶️🛣️"
                },
                {
                        "role": "ayee",
                        "text": "那當然！老公的腰靠墊還是阿姨特別挑選的乳膠墊呢！🛋️✨"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "剛剛買特產時，老闆送了一疊九州在地觀光手繪明信片！💌🌸"
                },
                {
                        "role": "achun",
                        "text": "好精美！我可以在背面寫物理治療保健心得寄回診所！📮💻"
                },
                {
                        "role": "alu",
                        "text": "本熊要寄一張給伺服器端：『我在九州吃得很飽，請勿更新』！📮🐻"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "窗外飄下來的小雪花…在 Three.js 裡是由粒子發射器產生的嗎？❄️🤔"
                },
                {
                        "role": "achun",
                        "text": "伸出手接住就融化了，不管是不是代碼，手感都好冰涼！❄️🖐️"
                },
                {
                        "role": "ayee",
                        "text": "下雪泡露天溫泉最浪漫了！等一下大家一起去泡湯！♨️🥰"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "寫病歷敲鍵盤敲到手腕緊繃，大家跟我做手腕屈肌伸展！🧘‍♀️👐"
                },
                {
                        "role": "yijhang",
                        "text": "……（單手伸出窗外反折掌心三十秒）嗯，倒試管手指更靈巧了。🕶️👍"
                },
                {
                        "role": "ayee",
                        "text": "阿純真是我們的專屬保健教練，全家健康靠妳啦！💕👏"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……剛在休息站點了四碗黑蒜油拉麵，叉燒雙倍。🕶️🍜"
                },
                {
                        "role": "achun",
                        "text": "黑蒜油香氣直衝腦門！這碗湯喝下去我能再寫十篇報告！🤤🔥"
                },
                {
                        "role": "alu",
                        "text": "本熊已經拿起相機：『九州拉麵最高傑作』留影存檔！📸🥢"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "如果有一天這趟自駕旅程跑完迴圈，我們會回到起點嗎？⏳🐻"
                },
                {
                        "role": "achun",
                        "text": "回到起點就再玩一次呀！每次吃的點心跟風景都不一樣！🌈🎉"
                },
                {
                        "role": "yijhang",
                        "text": "……不管轉幾圈，方向盤握在我手上，隨時出發。🕶️🚗"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "登登登～鹿兒島薩摩地瓜金磚蛋糕！剛剛趁熱切成四等分！🍠🍰"
                },
                {
                        "role": "achun",
                        "text": "綿密香甜～這口咬下去真的是全身細胞都在跳舞！💃✨"
                },
                {
                        "role": "alu",
                        "text": "本熊感測到多巴胺指數突破上限！熊生圓滿了！🐾💖"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "最後一張快門！大家一起對著鏡頭笑一個：『九州最讚！』📸🐻"
                },
                {
                        "role": "ayee",
                        "text": "九州最讚～阿姨比大愛心！❤️❤️"
                },
                {
                        "role": "achun",
                        "text": "九州最讚～物治師比耶！✌️💻"
                },
                {
                        "role": "yijhang",
                        "text": "……（推墨鏡微笑比讚）九州最讚。🕶️👍"
                }
        ]
];

    let banterTimers = [];
    let dialogBusyUntilMs = 0;       // 追蹤目前對話（含多句碎嘴佇列）預計完全讀完的時間戳
    let spotArrivalQueueTimer = null; // 若進站時前一段突發對話還剩一點點，排程接續播放景點台詞
    let lastSpeakerRole = null;       // 追蹤上一位開口的角色，避免單人發言時同個人連續獨白

    // 智慧隨機對話調度器（Smart Random Non-repeating History Controller）
    const recentScriptHistories = {
        family: [],
        inCar: [],
        walk: [],
        straggler: { achun: [], alu: [], ayee: [], yijhang: [] },
        soloQuotes: { achun: [], yijhang: [], ayee: [], alu: [] },
        spotMidstay: [],
        spotDeparture: []
    };
    let spokenRolesInCurrentSpot = new Set();
    let hasPlayedSpotMidstay = false;
    let hasPlayedSpotDepartureCall = false;

    function pickRandomNonRepeating(pool, historyArray, maxHistory = 4) {
        if (!pool || !pool.length) return null;
        if (pool.length === 1) return pool[0];
        const maxKeep = Math.min(maxHistory, pool.length - 1);
        let candidates = [];
        for (let i = 0; i < pool.length; i++) {
            if (!historyArray.includes(i)) candidates.push(i);
        }
        if (candidates.length === 0) {
            historyArray.length = 0;
            for (let i = 0; i < pool.length; i++) candidates.push(i);
        }
        const pickedIdx = candidates[Math.floor(Math.random() * candidates.length)];
        historyArray.push(pickedIdx);
        if (historyArray.length > maxKeep) {
            historyArray.shift();
        }
        return pool[pickedIdx];
    }

    function pickRandomSpeaker(excludeLast = true) {
        const roles = ['achun', 'yijhang', 'ayee', 'alu'];
        let available = (excludeLast && lastSpeakerRole) ? roles.filter(r => r !== lastSpeakerRole) : roles.slice();
        if (!available.length) available = roles.slice();
        const chosen = available[Math.floor(Math.random() * available.length)];
        lastSpeakerRole = chosen;
        return chosen;
    }

    // 車廂內行駛時的精簡高頻率碎嘴劇本（2～3 句短對話）
    const IN_CAR_BANTER_SCRIPTS = [
        [
            { role: 'alu', text: '偵測到車載環境：溫度 22 度，阿純呼吸頻率降到每分鐘 12 次…進入深層睡眠！😴🤖' },
            { role: 'ayee', text: '噓～阿嚕小聲點，阿純剛剛在景點敲了好多報告，讓她多睡會兒！🤫💕' },
            { role: 'yijhang', text: '……（默默關小收音機音量，避開減速帶顛簸）行車靜音模式。🕶️🚗' }
        ],
        [
            { role: 'achun', text: '（突然驚醒）等等！剛才是不是路過一家標榜『阿蘇牛奶限定泡芙』的小店？！👀🥐' },
            { role: 'alu', text: '阿純的甜點雷達居然能在休眠狀態下保持即時輪詢監聽？！📡🐻' },
            { role: 'yijhang', text: '……（打了右轉方向燈）前面兩百公尺迴轉，去買泡芙。🕶️🚗' }
        ],
        [
            { role: 'ayee', text: '老公，你這把年紀還能一手倒試管一手穩握方向盤，太厲害啦！👏🕶️' },
            { role: 'yijhang', text: '……停等紅燈才滑一下。行進中視線永遠在前方兩百公尺。安全第一。🕶️🛣️' },
            { role: 'achun', text: '姨丈的雙重任務協同處理能力堪比神經學頂級案例！🧠💯' }
        ],
        [
            { role: 'alu', text: '螢幕外的朋友剛剛是不是又按了全景旋轉？本熊的陀螺儀在旋轉跳躍！🔄🐻' },
            { role: 'achun', text: '哈哈！轉慢一點啦，不然物治師在車上看螢幕會動暈症發作！🤢📱' },
            { role: 'ayee', text: '沒事沒事，阿姨這裡有酸梅糖，含一顆立刻舒服！🍬🥰' }
        ],
        [
            { role: 'achun', text: '阿嚕，你胸前那台大相機看起來好專業喔！有手動對焦環嗎？📷✨' },
            { role: 'alu', text: '當然！雙色復古金屬機身配超大口徑前玉鏡頭，連阿純的睫毛都能拍得清清楚楚！🐻📸' },
            { role: 'yijhang', text: '……拍得好。下車找個好光線幫全家拍合照。🕶️👍' }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……電動滑門關好了，出發下一站。（停紅燈順手倒試管）🚗🕶️"
                },
                {
                        "role": "achun",
                        "text": "趁直線平穩把筆電放腿上敲完物治紀錄，打完秒睡！💻😴"
                },
                {
                        "role": "ayee",
                        "text": "打字眼睛酸，來張嘴先吃一口阿姨買的草莓大福～！🍓🍊"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "（後座腿上放筆電打字）患者核心穩定…下肢肌力…Zzz…💻😪"
                },
                {
                        "role": "alu",
                        "text": "報告！阿純打物治紀錄打到睡著，額頭壓鍵盤打出 zzzzzz 了！🤖🐻"
                },
                {
                        "role": "ayee",
                        "text": "心疼死阿姨了！下一站先帶阿純去咖啡廳喝拿鐵吃布丁！☕🍮"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "還好租七人座 Sienta，第三排剛好放滿十二袋九州伴手禮！🛍️🍡"
                },
                {
                        "role": "achun",
                        "text": "（閉著眼伸手）我聞到起司饅頭跟地瓜乾的香味了～😋💤"
                },
                {
                        "role": "yijhang",
                        "text": "……妳閉眼找食物的精準度，比我盲倒試管還高。🕶️👍"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "看著窗外風景後退…是車子在動，還是九州島在往後捲動？🤖🐻"
                },
                {
                        "role": "yijhang",
                        "text": "……別研究座標系了，抓穩扶手，前面是阿蘇連續彎道。🕶️🚗"
                },
                {
                        "role": "ayee",
                        "text": "過彎不怕！來一人一顆黑糖饅頭壓壓驚，越吃越穩喔！🥟🥰"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……這段高速公路路面平整，適合定速巡航。🕶️🛣️"
                },
                {
                        "role": "achun",
                        "text": "太棒了！無震動環境下，我剛送出今天第三份個案評估表！💻✨"
                },
                {
                        "role": "ayee",
                        "text": "工作做完啦？來～阿姨剛剝好的多汁蜜柑立刻遞上去！🍊🥰"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "車裡播這首演歌好有味道喔！大家跟著阿姨一起哼～🎵👘"
                },
                {
                        "role": "yijhang",
                        "text": "……（手指跟著節拍在方向盤上敲出試管倒水韻律）🕶️🎶"
                },
                {
                        "role": "alu",
                        "text": "本熊的音訊處理模組偵測到家庭溫馨共鳴波形！📻🐻"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "後座暖氣吹得腳底好暖，膝關節僵硬完全緩解了～🦶♨️"
                },
                {
                        "role": "ayee",
                        "text": "冷風吹不到最要緊！保溫杯裡還有熱呼呼黑豆茶喔！🍵💕"
                },
                {
                        "role": "alu",
                        "text": "本熊縮在後座角落，覺得自己像一隻幸福的烤棉花糖。🍡🐻"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "姨丈！剛才倒試管那關，底層綠色跟頂層黃色換位了嗎？🧪👀"
                },
                {
                        "role": "yijhang",
                        "text": "……早就換好了。趁剛才等平交道二十秒內解開。🕶️⚡"
                },
                {
                        "role": "achun",
                        "text": "姨丈等紅燈的手速，去當電競選手也是世界冠軍級別！🏆🎮"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "看看置杯架，阿姨買了阿蘇牧場直送熱牛奶，一人一瓶！🥛🍼"
                },
                {
                        "role": "achun",
                        "text": "好濃郁的奶香！喝完胃暖暖的，正好補足寫報告消耗的能量！😋💪"
                },
                {
                        "role": "yijhang",
                        "text": "……（接過一瓶單手轉開蓋子）這奶脂厚度很扎實，好喝。🕶️🥛"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "剛才看窗外山坡上的放牧赤牛，低頭角度跟我寫病歷一模一樣！🐮💻"
                },
                {
                        "role": "alu",
                        "text": "赤牛低頭吃草，阿純低頭敲鍵盤，都是為了生存的能量循環！🌾🐻"
                },
                {
                        "role": "ayee",
                        "text": "哈哈阿嚕講得真好！來吃一塊剛切好的蜂蜜黑糖米香！🍘🥰"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……前面即將進入人吉山區隧道，光線轉暗，頭燈已開。🕶️💡"
                },
                {
                        "role": "alu",
                        "text": "進入隧道了！本熊眼球的感光度自動提高 2.5 階！👁️🤖"
                },
                {
                        "role": "achun",
                        "text": "剛好趁暗光閉目養神，大家三分鐘後叫我吃點心～😴💤"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "後座兩個小朋友有沒有口渴？阿姨有熱煎茶跟冰麥茶喔！🍵🧊"
                },
                {
                        "role": "alu",
                        "text": "本熊舉手！想要一杯熱煎茶搭配阿姨的黑糖栗子銅鑼燒！🌰🐻"
                },
                {
                        "role": "achun",
                        "text": "我也要一杯！配著喝剛好壓壓嘴裡的起司仙貝香味！🍘😋"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "（伸展十指指節）關節啪啪響，今天打字字數突破一萬字大關！💻🏅"
                },
                {
                        "role": "yijhang",
                        "text": "……妳手速快，我自駕里程剛好突破五百公里。雙贏。🕶️🛣️"
                },
                {
                        "role": "ayee",
                        "text": "全家人都好勤奮！今晚一定要去居酒屋點最豪華的套餐！🍢🎉"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "本熊靠在車窗上看水滴…雨滴流下的軌跡符合流體力學嗎？🌧️🐻"
                },
                {
                        "role": "yijhang",
                        "text": "……防潑水鍍膜發揮作用了，水珠直接滑走，視線很清爽。🕶️🚗"
                },
                {
                        "role": "ayee",
                        "text": "下點小雨更有冬季旅行的氣氛呢！車裡熱熱鬧鬧多幸福！🌧️💕"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "老公～你開車累不累？要不要阿姨換手開一小段？👩‍🦰🚗"
                },
                {
                        "role": "yijhang",
                        "text": "……不用，妳負責照顧阿純跟阿嚕吃東西就好。我開得很穩。🕶️😌"
                },
                {
                        "role": "achun",
                        "text": "姨丈開車最讓人安心了！睡在後座完全不用擔心急煞！😴👍"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "（筆電螢幕合上發出清脆啪嗒聲）暫停營業！現在是純放空時間！💻🚫"
                },
                {
                        "role": "alu",
                        "text": "恭喜阿純解除物理治療師封印！現在變回貪吃女孩模式！🎉🐻"
                },
                {
                        "role": "ayee",
                        "text": "太好了！快把這盒溫泉黑糖地瓜球打開，趁熱一人兩顆！🍠🍡"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……這台 Sienta 的油電混動系統很安靜，起步平穩順暢。🕶️🔋"
                },
                {
                        "role": "alu",
                        "text": "本熊幾乎聽不到引擎噪音，只聽見阿姨撕零食包裝的沙沙聲！🛍️🐻"
                },
                {
                        "role": "ayee",
                        "text": "被抓到了！阿姨正要開一包鹿兒島限定柚子薄鹽洋芋片嘛！🥔😆"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "如果我們在車裡跳躍，重力場會帶著我們一起向前飛嗎？🛸🐻"
                },
                {
                        "role": "achun",
                        "text": "慣性定律！你在車裡跳只會撞到車頂天花板，乖乖坐好啦！💺😆"
                },
                {
                        "role": "yijhang",
                        "text": "……而且會觸發車內安全帶警告蜂鳴器。繫好安全帶。🕶️⚠️"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "窗外的山林覆蓋著薄薄的白雪，像不像撒了糖霜的黑巧克力蛋糕？🏔️🍫"
                },
                {
                        "role": "achun",
                        "text": "阿姨的形容詞永遠離不開甜點！但真的越看越想吃蛋糕！🍰😋"
                },
                {
                        "role": "yijhang",
                        "text": "……（嘴角微微上揚）下一個休息站正好有賣年輪蛋糕。🕶️🥐"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "在車上戴著降噪耳機敲鍵盤，感覺像坐在頭等艙工作！🎧💻"
                },
                {
                        "role": "ayee",
                        "text": "阿姨隨時提供熱茶跟甜點，這服務比商務艙還貼心吧？🍵🥰"
                },
                {
                        "role": "achun",
                        "text": "絕對是七星級頂級包車享受！五星好評直接給滿！⭐⭐⭐⭐⭐"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "姨丈，手機電量還夠倒試管嗎？需要本熊的充電線嗎？📱🔌"
                },
                {
                        "role": "yijhang",
                        "text": "……車載無線充電座正充著，電量 98%，隨時可以迎戰地獄關。🕶️⚡"
                },
                {
                        "role": "alu",
                        "text": "高科技酷哥司機果然準備周全！本熊甘拜下風！🙌🤖"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "這包櫻島小蜜柑軟糖酸酸甜甜，阿純張嘴咬一顆提提神！🍬🍊"
                },
                {
                        "role": "achun",
                        "text": "唔！真的好酸甜開胃！精神瞬間來了，可以再校對兩頁報告！🤩💻"
                },
                {
                        "role": "yijhang",
                        "text": "……也給我一顆。長途駕駛吃酸的剛好防疲勞。🕶️👌"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "本熊把相機鏡頭對準後照鏡…剛好看見姨丈墨鏡裡反射的路線！📷🕶️"
                },
                {
                        "role": "yijhang",
                        "text": "……角度抓得精準。構圖很有黑白公路電影的質感。🕶️🎬"
                },
                {
                        "role": "alu",
                        "text": "耶！得到冷酷老司機認可，本熊攝影技術又進階了！🎉🐻"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "車子轉彎時離心力很溫和，骨盆跟脊椎沒有多餘側傾代償！🚗📐"
                },
                {
                        "role": "yijhang",
                        "text": "……入彎減速、出彎補油，方向盤角度微調。老司機基本功。🕶️🛣️"
                },
                {
                        "role": "ayee",
                        "text": "全家坐在車裡像坐在客廳沙發一樣穩，老公最棒了！🛋️❤️"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "大家肚子留點空間喔！聽說下一站的鄉村炊飯便當很有名！🍱🥢"
                },
                {
                        "role": "achun",
                        "text": "我的胃已經預留了 50% 容量，保證連一顆飯粒都不剩！🤤🌾"
                },
                {
                        "role": "alu",
                        "text": "本熊也將存儲空間格式化完畢，準備接受炊飯寫入！💾🐻"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……前方看見景點指標了。準備減速進站，大家準備下車。🕶️🅿️"
                },
                {
                        "role": "achun",
                        "text": "筆電存檔收進背包！準備下車深呼吸、伸展腿腳吃美食！🎒👟"
                },
                {
                        "role": "ayee",
                        "text": "隨身包包跟相機拿好，阿姨帶你們去逛最好玩的小店！🛍️🌸"
                }
        ]
];

    // 景點漫步中段互動與現場動作吐槽小劇場（徹底消除景點停留時的空白時刻！）
    const SPOT_MIDSTAY_BANTERS = [
        [
            { role: 'ayee', text: '阿純草地上風大，阿姨把大披肩給妳披上，別著涼打電腦～！🧣🥰' },
            { role: 'achun', text: '謝謝阿姨！披上超溫暖，我的打字速度瞬間又快了十個字！💻🔥' },
            { role: 'yijhang', text: '……慢慢打，時間很充裕。我這管試管也剛好倒完。🕶️☕' }
        ],
        [
            { role: 'alu', text: '報告！阿純坐姿打字的核心穩定度評分 99 分，堪稱人體工學典範！🤖💻' },
            { role: 'achun', text: '物治師的職業尊嚴！就算在草地上敲 SOAP 也要維持骨盆中立！🦴✨' },
            { role: 'ayee', text: '核心穩定更要吃！阿姨剛買的草莓大福一人咬一口！🍓🍡' }
        ],
        [
            { role: 'alu', text: '姨丈把 Sienta 停在路旁的倒車入庫弧線，堪稱黃金比例演算法！📐🚙' },
            { role: 'yijhang', text: '……目測一次到位，完全不需要看環景倒車顯影。老司機手感。🕶️👍' },
            { role: 'ayee', text: '老公停車最帥了！連路邊的日本婆婆都在鼓掌呢！👏🥰' }
        ],
        [
            { role: 'achun', text: '我有自我意識嗎？剛剛敲鍵盤時，我好像感覺到外面有人在看我！👀💻' },
            { role: 'alu', text: '警報！阿純突破了第四面牆！難道妳也接收到底層 Canvas 渲染幀率了？！🤖🐻' },
            { role: 'yijhang', text: '……別想太深，那是鏡頭旋轉時的陽光反射。專心吃妳的糰子。🕶️🍡' }
        ],
        [
            { role: 'ayee', text: '阿純你看！旁邊那隻三花貓一直在看你的筆電螢幕，牠也懂物理治療嗎？🐱💻' },
            { role: 'achun', text: '這隻貓核心肌群很結實喔！給牠摸下巴三秒鐘當作掛號諮詢費！🐈💆‍♀️' },
            { role: 'alu', text: '喵星人數據分析中…判定：好感度 100%，已發出咕嚕咕嚕聲！🐾✨' }
        ],
        [
            { role: 'ayee', text: '大家深呼吸！這裡的冷空氣吸進肚子裡好清爽喔！🌲👃' },
            { role: 'yijhang', text: '……比辦公室舒服多了。這片風景值得多看兩分鐘。🕶️✨' },
            { role: 'achun', text: '看著這片風景，剛才打病歷累積的斜方肌緊繃瞬間放鬆了～💆‍♀️🍃' }
        ],
        [
            { role: 'alu', text: '本熊已將全家在景點的笑容轉換成 4K 記憶體快照！📷💾' },
            { role: 'ayee', text: '阿嚕真會拍！等等阿姨在車上幫你擦擦鏡頭上的雪花！❄️🐻' },
            { role: 'yijhang', text: '……拍得好。回家洗出來掛客廳。🕶️👍' }
        ],
        [
            { role: 'achun', text: '呼～最後一份個案評估表上傳成功！現在全力開啟吃貨模式！💻🎉' },
            { role: 'ayee', text: '辛苦阿純了！阿姨早就把溫泉蛋跟現烤牛肉串準備好了！🥩🥚' },
            { role: 'alu', text: '恭喜阿純解鎖「景點全飽狀態」！本熊舉旗慶祝！🚩🐻' }
        ],
        [
            { role: 'yijhang', text: '……這座景點的腹地規畫不錯，走起來很順腳。🕶️🚶‍♂️' },
            { role: 'ayee', text: '而且旁邊的土產店超好逛！阿姨又發現兩種限定餅乾！🍪🛍️' },
            { role: 'alu', text: '本熊的感測器聞到濃郁的焦糖與黑糖香氣！香氣逼人！🍯🐻' }
        ],
        [
            { role: 'achun', text: '大家看那邊山壁的傾斜節理！骨盆如果歪成那樣要做整脊啦～😂⛰️' },
            { role: 'alu', text: '大自然岩層也需要物理治療嗎？本熊第一次聽到這種診斷！🤖🧠' },
            { role: 'yijhang', text: '……地質斷層也是大自然的關節錯位。阿純診斷正確。🕶️👌' }
        ]
    ];

    // 景點出發前全員歸位上車的隨機收尾呼喊（全員走回車旁並依序入座時同步觸發，絕不尷尬等待）
    const SPOT_DEPARTURE_CALLS = [
        [
            { role: 'yijhang', text: '……時間差不多了。Sienta 怠速待命中，全員登車出發下一站。🚙🕶️' },
            { role: 'ayee', text: '東西拿好、點心帶齊，全家快步上車囉～！🍡🙌' }
        ],
        [
            { role: 'ayee', text: '好啦～景點逛得好滿足！大家快回到敞篷車裡吹暖氣吃點心！🚗♨️' },
            { role: 'achun', text: '病歷打完存檔、筆電收進包包，上車閉目養神～！💻😴' }
        ],
        [
            { role: 'alu', text: '全員回防！本熊導航下一個奇蹟座標，滑門即將關閉！🤖🧭' },
            { role: 'yijhang', text: '……電動滑門關閉。各位繫好安全帶，前面路段平穩。🕶️🚗' }
        ],
        [
            { role: 'achun', text: '收好小木桌！Sienta 敞篷視野太讚了，跳上車繼續公路旅行！🚙✨' },
            { role: 'ayee', text: '阿姨手上還有三顆現剝蜜柑，入座後一人分一瓣！🍊🥰' }
        ],
        [
            { role: 'yijhang', text: '……（輕按兩聲喇叭）嗶嗶。下一站路程二十分鐘，出發。🕶️🚘' },
            { role: 'alu', text: '收到！本熊已穩穩坐在後座右側，快門準備好追櫻島了！🐻📸' }
        ]
    ];

    // 突發狀況：有人沒趕上車在後面狂追（阿純開飛碟追車）精簡版劇本（2～3 句快節奏，確保進下一站前讀完！）
    const STRAGGLER_BANTER_SCRIPTS = {
        "achun": [
                [
                        {
                                "role": "achun",
                                "text": "等等我啦！剛在咖啡廳存檔完物治紀錄，只好開飛碟追車了！🛸💻"
                        },
                        {
                                "role": "alu",
                                "text": "呼嚕？！阿純居然開反重力飛碟追 Sienta！她是外星物治師嗎？！🛸🐻"
                        },
                        {
                                "role": "yijhang",
                                "text": "……後照鏡看到飛碟光束了。飛得很穩，那我不減速了。🕶️🚗"
                        }
                ],
                [
                        {
                                "role": "achun",
                                "text": "喂喂拿鐵在飛碟裡快晃出來了！快讓我回 Sienta 後座睡覺！🛸☕"
                        },
                        {
                                "role": "yijhang",
                                "text": "……妳的飛碟比 Sienta 還快，怎麼不直接超車去下一站？🕶️📱"
                        },
                        {
                                "role": "achun",
                                "text": "因為我的點心袋跟毛毯還在車上啊！沒阿姨餵食我不飛走！🛸😭"
                        }
                ],
                [
                        {
                                "role": "achun",
                                "text": "救命啊！飛碟要我打完物治 SOAP 紀錄才能開渦輪，等我啦！🛸💻"
                        },
                        {
                                "role": "ayee",
                                "text": "老公慢一點！阿姨把布丁拿在車窗邊，下一站馬上塞進阿純嘴裡！🍮🥰"
                        }
                ],
                [
                        {
                                "role": "achun",
                                "text": "呼叫 Sienta！飛碟雷達鎖定後車廂！快把天窗打開讓我降落！🛸🛰️"
                        },
                        {
                                "role": "alu",
                                "text": "天窗只有 40 公分！阿純的飛碟會卡在車頂變成景觀飾品啦！😱🐻"
                        },
                        {
                                "role": "yijhang",
                                "text": "……別鬧。打雙黃燈靠邊停了，妳直接飛下來走車門。🕶️🚗"
                        }
                ],
                [
                        {
                                "role": "achun",
                                "text": "開飛碟追車太刺激了！但我發現在無重力下打字手腕完全不酸！🛸💻"
                        },
                        {
                                "role": "ayee",
                                "text": "阿純在空中別分心打字啦！阿姨看得心驚膽跳，快下來吃糰子！🍡💦"
                        },
                        {
                                "role": "achun",
                                "text": "收到！飛碟牽引光束鎖定阿姨手上的烤糰子，立刻降落！🛸🤤"
                        }
                ],
                [
                        {
                                "role": "achun",
                                "text": "姨丈！飛碟儀表板警告：『前方 Sienta 轉彎過於帥氣』！🛸😎"
                        },
                        {
                                "role": "yijhang",
                                "text": "……正常發揮。妳的飛碟尾翼氣流有點亂，注意下壓力。🕶️💨"
                        },
                        {
                                "role": "alu",
                                "text": "這兩個人到底在進行什麼跨維度自駕技術交流啦？！🤖🐻"
                        }
                ],
                [
                        {
                                "role": "achun",
                                "text": "等等！我發現飛碟的杯架跟 Sienta 一樣好用，拿鐵一滴都沒灑！🛸☕"
                        },
                        {
                                "role": "ayee",
                                "text": "拿鐵沒灑就好！阿姨這裡還有熱騰騰可樂餅等著餵妳呢！🥟🥰"
                        },
                        {
                                "role": "achun",
                                "text": "聞到香味了！飛碟推力全開，三秒內追上 Sienta 車尾！🛸💨"
                        }
                ],
                [
                        {
                                "role": "achun",
                                "text": "求求你們停車啦！飛碟的 Wi-Fi 訊號很弱，物治報告傳不出去！🛸📶"
                        },
                        {
                                "role": "alu",
                                "text": "本熊立刻開啟車載熱點：『九州熊熊 5G』，密碼是 dorayaki！📶🐻"
                        },
                        {
                                "role": "achun",
                                "text": "連上了！報告傳送成功！飛碟推進器冷卻，準備登艦！🛸🙌"
                        }
                ],
                [
                        {
                                "role": "achun",
                                "text": "開著飛碟在天上俯瞰九州…這視角比打完所有病歷還舒爽！🛸🏔️"
                        },
                        {
                                "role": "yijhang",
                                "text": "……風景再好也得著陸。前面要過收費站了，飛碟不能過 ETC。🕶️🚧"
                        },
                        {
                                "role": "achun",
                                "text": "收到！收起反重力光環，立刻降落 Sienta 旁！🛸🚗"
                        }
                ],
                [
                        {
                                "role": "achun",
                                "text": "嗚嗚飛碟裡的空調太冷了！我想念 Sienta 後座的電熱座椅！🛸🥶"
                        },
                        {
                                "role": "ayee",
                                "text": "可憐的阿純！阿姨已經把毛毯鋪好、暖氣開最強等妳回座了！🛋️🔥"
                        },
                        {
                                "role": "yijhang",
                                "text": "……車已停妥。滑門開了，快進來吹暖氣。🕶️🚪"
                        }
                ],
                [
                        {
                                "role": "achun",
                                "text": "報告！飛碟偵測到阿姨背包裡的薩摩地瓜酥分子濃度激增！🛸🍠"
                        },
                        {
                                "role": "ayee",
                                "text": "鼻子真靈！剛打開保溫盒呢，快降落，第一塊留給妳！🍠🥰"
                        },
                        {
                                "role": "alu",
                                "text": "用外星飛碟的質譜儀追蹤地瓜酥…阿純真是吃貨界的奇蹟！🐻👏"
                        }
                ],
                [
                        {
                                "role": "achun",
                                "text": "各位乘客請注意：本飛碟即將對 Sienta 實施柔和對接！🛸🚗"
                        },
                        {
                                "role": "yijhang",
                                "text": "……對接許可。煞車已踩死，歡迎歸隊。🕶️⚓"
                        },
                        {
                                "role": "achun",
                                "text": "成功降落！太好了，終於可以把筆電放回腿上繼續打紀錄！💻😴"
                        }
                ]
        ],
        "alu": [
                [
                        {
                                "role": "alu",
                                "text": "停車啊姨丈！本熊召喚了九州護體神龍，騎在龍頭上騰雲駕霧追車啦！🐉💨"
                        },
                        {
                                "role": "achun",
                                "text": "阿嚕快看！車上的牛乳霜淇淋跟可樂餅再十秒就要被我消滅囉！🍦😋"
                        },
                        {
                                "role": "alu",
                                "text": "不准動本熊的霜淇淋！神龍擺尾，全速超頻衝刺！！🐉⚡"
                        }
                ],
                [
                        {
                                "role": "alu",
                                "text": "別丟下本熊！神龍問在空中超速會被扣除旅行預算嗎？！🐉🤖"
                        },
                        {
                                "role": "yijhang",
                                "text": "……不會扣預算。我有從後照鏡盯著你們，龍飛得挺平穩。🕶️🚗"
                        },
                        {
                                "role": "ayee",
                                "text": "阿嚕別慌！阿姨把炸魚餅往車窗外遞，神龍聞著香味飛得更快喔！🍢💕"
                        }
                ],
                [
                        {
                                "role": "alu",
                                "text": "呼嚕！龍角太滑了！本熊抓著龍鬚像在公路衝浪！快打雙黃燈靠邊！🐉🐻"
                        },
                        {
                                "role": "achun",
                                "text": "阿嚕騎龍的坐姿太帥了！核心肌群很穩定，物治師打滿分！👏😆"
                        },
                        {
                                "role": "yijhang",
                                "text": "……（踩煞車開滑門）靠邊停了，神龍請緩降，讓熊熊進車。🕶️🚪"
                        }
                ],
                [
                        {
                                "role": "alu",
                                "text": "報告！高空視野太壯觀，本熊在龍背上拍下了三十張九州連峰全景大作！📷🐉"
                        },
                        {
                                "role": "ayee",
                                "text": "阿嚕好厲害！阿姨手上拿著熱騰騰包子在車門口接你啦！🥟🥰"
                        },
                        {
                                "role": "alu",
                                "text": "看見包子的白煙了！神龍俯衝！熊熊飛撲登車！！🐾💨"
                        }
                ],
                [
                        {
                                "role": "alu",
                                "text": "報告姨丈！龍說前面路段有測速照相，它已經自動降至限速 60 了！🐉📸"
                        },
                        {
                                "role": "yijhang",
                                "text": "……守法神龍。剛才看你拍風景拍得太入迷，沒叫你。進來吧。🕶️🚗"
                        },
                        {
                                "role": "alu",
                                "text": "原來只是忘了叫本熊！神龍任務完成，哲學熊回座！🐻🙌"
                        }
                ],
                [
                        {
                                "role": "alu",
                                "text": "神龍的祥雲加速器全力運轉中！排氣管噴出的是草莓味水氣！🍓🐉"
                        },
                        {
                                "role": "achun",
                                "text": "上車立刻給你喝冰麥茶！再幫你的熊大腿做放鬆按摩！🍵💆‍♀️"
                        },
                        {
                                "role": "alu",
                                "text": "為了阿純的專業按摩，本熊就算抓斷龍鬚也要追上！🐾⚡"
                        }
                ],
                [
                        {
                                "role": "alu",
                                "text": "等等我！神龍聞到阿姨手上的黑豚飯糰，正在車頂高空流口水！🐉🍙"
                        },
                        {
                                "role": "yijhang",
                                "text": "……車頂承重有限，別讓神龍降落在車頂。靠邊讓你上車。🕶️🚗"
                        },
                        {
                                "role": "ayee",
                                "text": "阿嚕快下來！阿姨特製特大號黑豚飯糰就是留給你的！🍙🎉"
                        }
                ],
                [
                        {
                                "role": "alu",
                                "text": "呼…本熊終於跳進後座了！軟綿綿的座椅才是宇宙的真理！🛋️🐻"
                        },
                        {
                                "role": "achun",
                                "text": "辛苦啦阿嚕！來，這半塊草莓鬆餅獎勵你的神龍追車！🍓🍰"
                        },
                        {
                                "role": "yijhang",
                                "text": "……全員上齊。電動滑門關閉，再次啟程。🕶️🚗"
                        }
                ]
        ],
        "ayee": [
                [
                        {
                                "role": "ayee",
                                "text": "哎呀快停車！阿姨騎著魔法掃帚在天上看你們呢！等等阿姨呀！🧹✨"
                        },
                        {
                                "role": "achun",
                                "text": "天啊阿姨騎魔法掃帚追車！姨丈快停車，行動糧倉在天上飛！🧹💻😭"
                        },
                        {
                                "role": "yijhang",
                                "text": "……（立刻打雙黃燈減速）看到了。掃帚飛得很穩，已經在等妳了。🕶️🚗"
                        }
                ],
                [
                        {
                                "role": "ayee",
                                "text": "等等我呀！魔法掃帚尾巴掛著四盒燙口黑糖饅頭，快讓我進車餵你們！🥟🧹"
                        },
                        {
                                "role": "achun",
                                "text": "我已經在電動滑門邊張開嘴巴待命了！阿姨快降落～！😋🙌"
                        },
                        {
                                "role": "yijhang",
                                "text": "……（拉下手煞車微笑）妳就算多買八盒，後車廂也裝得下。🕶️📦"
                        }
                ],
                [
                        {
                                "role": "ayee",
                                "text": "老公你看！阿姨學魔女琪琪側坐掃帚，姿勢是不是很優雅！🧹🥰"
                        },
                        {
                                "role": "alu",
                                "text": "本熊立刻抓相機！阿姨側坐掃帚的唯美大作一定要收進九州寫真集！📷🌸"
                        },
                        {
                                "role": "ayee",
                                "text": "阿嚕真乖！降落阿姨先剝三顆最大最甜的櫻島蜜柑給你吃！🍊🥰"
                        }
                ],
                [
                        {
                                "role": "ayee",
                                "text": "風好大呀！阿姨的大圍巾飄起來了，掃帚請減速讓阿姨回後座！🧹🧣"
                        },
                        {
                                "role": "achun",
                                "text": "沒關係阿姨！看到妳掃帚籃子裡那兩大籃紅通通草莓，一切都原諒了！🍓😍"
                        },
                        {
                                "role": "yijhang",
                                "text": "……車門一直為妳開著。慢慢降落，小心台階。🕶️🚗"
                        }
                ],
                [
                        {
                                "role": "ayee",
                                "text": "大家抓緊胃袋！阿姨騎掃帚剛剛搶到最後三個限定栗子蒙布朗！🌰🧹"
                        },
                        {
                                "role": "achun",
                                "text": "天啊是傳說中的名店蒙布朗！阿姨妳是全九州最強美食魔法師！🏆🤤"
                        },
                        {
                                "role": "alu",
                                "text": "本熊在後座舉起『掃帚魔女阿姨萬歲』旗幟熱烈迎接！🚩🐻"
                        }
                ],
                [
                        {
                                "role": "ayee",
                                "text": "阿純阿嚕！阿姨在天上看到下一站的草莓園了，掃帚加速衝刺！🧹🍓"
                        },
                        {
                                "role": "achun",
                                "text": "阿姨的空中偵察導航太強大了！完全不需要 Google Maps！👏😆"
                        },
                        {
                                "role": "yijhang",
                                "text": "……上車擦汗。保溫杯裡的熱茶幫妳旋開了。🕶️🍵"
                        }
                ],
                [
                        {
                                "role": "ayee",
                                "text": "哎唷！掃帚上的金色緞帶打結了，姨丈快打雙黃燈靠邊接阿姨！🧹🎀"
                        },
                        {
                                "role": "yijhang",
                                "text": "……車已停妥。緞帶我幫妳解開，天冷快進車裡暖和一下。🕶️🧣"
                        },
                        {
                                "role": "alu",
                                "text": "姨丈這句話甜度超標！本熊快門再次按下留下珍貴合影！📷❤️"
                        }
                ],
                [
                        {
                                "role": "ayee",
                                "text": "安全降落啦！掃帚收進後車廂，第一排到第三排每人塞滿點心！🧹🍡🙌"
                        },
                        {
                                "role": "achun",
                                "text": "左手可樂餅、右手烤地瓜，幸福感直接拉滿！🍠😋"
                        },
                        {
                                "role": "yijhang",
                                "text": "……糧食充足，全隊士氣高昂。下一站，出發。🕶️🚗"
                        }
                ]
        ]
};

    function pickStragglerScript(role) {
        const list = STRAGGLER_BANTER_SCRIPTS[role];
        if (!list || !list.length) return null;
        if (!Array.isArray(list[0])) return list;
        const history = recentScriptHistories.straggler[role] || (recentScriptHistories.straggler[role] = []);
        return pickRandomNonRepeating(list, history, Math.max(1, list.length - 1));
    }

    // 全家下車散步賞景時的精簡碎嘴劇本群（多款情境輪播）
    const WALK_TOGETHER_BANTER_SCRIPTS = [
        [
                {
                        "role": "yijhang",
                        "text": "……這段風景不錯，下來散步，我順便邊走邊把這關試管倒完。🌲🕶️"
                },
                {
                        "role": "ayee",
                        "text": "散步最棒了！每走十步阿姨就餵你們吃一顆小蜜柑跟麻糬！🍊🍡"
                },
                {
                        "role": "achun",
                        "text": "走五百公尺消化一下，待會又能多吃兩碗黑豚飯跟寫物治紀錄！🍖💻"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "踩在覆雪的泥土上…腳底回傳的磨擦係數非常真實！❄️🐻"
                },
                {
                        "role": "achun",
                        "text": "多走戶外自然路面，能刺激腳底本體感覺神經，大腦更靈活！🧠👟"
                },
                {
                        "role": "ayee",
                        "text": "大腦靈活更要吃甜點！來一人一小塊黑糖花生酥脆餅！🥜🥰"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "大家看這排老杉木！空氣裡都是好聞的芬多精，深呼吸～！🌲👃"
                },
                {
                        "role": "yijhang",
                        "text": "……空氣冷冽清新，提神效果比黑咖啡還顯著。🕶️✨"
                },
                {
                        "role": "alu",
                        "text": "本熊的氣體分析儀回報：純淨森林指數 100%！呼吸超順暢！🍃🐻"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "散步時雙手自然擺動，能帶動胸椎與腰椎的生理旋轉角度！🚶‍♀️✨"
                },
                {
                        "role": "yijhang",
                        "text": "……（單手插口袋另一手點試管）我有保持節奏同步。🕶️📱"
                },
                {
                        "role": "ayee",
                        "text": "老公你連散步都在倒試管！看路看路，阿姨牽著你走！👫💕"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "喀嚓！本熊拍下了陽光透過樹梢照在雪地上的金色光斑！📷✨"
                },
                {
                        "role": "ayee",
                        "text": "拍得真美！等洗成照片阿姨要貼在客廳最顯眼的地方！🖼️🌸"
                },
                {
                        "role": "achun",
                        "text": "阿嚕很有攝影天份耶，光影掌握得比我打病歷還精確！📸💻"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "走走走～前面轉角好像有一家賣現烤地瓜的小推車！🍠💨"
                },
                {
                        "role": "achun",
                        "text": "聞到炭烤香味了！我的步頻自動從每分鐘 100 步加速到 140 步！🏃‍♀️💨"
                },
                {
                        "role": "yijhang",
                        "text": "……不用跑，地瓜不會飛走。我錢包準備好了。🕶️👛"
                }
        ],
        [
                {
                        "role": "alu",
                        "text": "請問大家：漫步在九州島上，是我們在遊歷它，還是它在接納我們？💭🐻"
                },
                {
                        "role": "yijhang",
                        "text": "……互為主體。路是由雙腳走出來的，走過的地方就是記憶。🕶️🛣️"
                },
                {
                        "role": "achun",
                        "text": "姨丈太有深度了！這句話完全可以當我這趟旅行筆記的序言！📝🌟"
                }
        ],
        [
                {
                        "role": "achun",
                        "text": "吸一口清涼空氣，感覺肺活量完全打開，工作壓力全部吐出去！🌬️🙌"
                },
                {
                        "role": "ayee",
                        "text": "吐出去好！阿姨把溫暖的愛心跟甜點幫妳全部補進來！💖🍮"
                },
                {
                        "role": "alu",
                        "text": "本熊的能量核心也充滿了綠色可再生溫馨動能！🔋🐻"
                }
        ],
        [
                {
                        "role": "yijhang",
                        "text": "……前面五百公尺就是觀景台。這段緩坡走起來很舒服。🕶️🏞️"
                },
                {
                        "role": "alu",
                        "text": "本熊負責在前面帶路！熊熊探險隊，全員跟上！🐾🚩"
                },
                {
                        "role": "ayee",
                        "text": "小隊長阿嚕走得好有精神！回頭阿姨獎勵你一顆大草莓！🍓🥰"
                }
        ],
        [
                {
                        "role": "ayee",
                        "text": "全家人一起走在冬天的日本街道上，真的好幸福好難忘喔！🧣❤️"
                },
                {
                        "role": "achun",
                        "text": "有美景、有好吃的、還有隨時能打紀錄的筆電，人生圓滿！💻🎉"
                },
                {
                        "role": "yijhang",
                        "text": "……嗯。好天氣、好風景、好家人。繼續走吧。🕶️🚶‍♂️"
                }
        ]
];
    function pickWalkTogetherScript() {
        return pickRandomNonRepeating(WALK_TOGETHER_BANTER_SCRIPTS, recentScriptHistories.walk, 5);
    }

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
        mainlandCoastPts = coastData && coastData.mainland ? coastData.mainland : null;
        const routeData = await loadJsonData('./portal/data/route.json', 'route');

        const w = container.clientWidth || 800;
        const h = container.clientHeight || 520;
        const isMobile = window.innerWidth < 768;

        // 1. 場景與相機 (配合 1.2x 地圖擴展適度拉遠初始鏡頭，涵蓋熊本機場北端與櫻島南端)
        scene = new THREE.Scene();
        canvasW = w;
        canvasH = h;
        initFireworksPool(scene);
        camera = new THREE.PerspectiveCamera(35, w / h, 0.5, 280);
        camera.position.set(0, 19.8, 26.2);

        // 2. WebGL 渲染器與真實柔和陰影 + 電影感柔和色調映射 (提升通透光影層次與微縮立體感)
        renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
        renderer.setSize(w, h);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.15;
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

        // 7. 建立小巴、熊本市電、西海岸新幹線、東海岸音速號、櫻島渡輪、屋台、商店、貓狗、路人 (貼合地面並避讓車道與地標)
        propState = window.KyushuIsland.Props.populateIslandProps(
            islandRoot,
            terrainState.tramCurve,
            isMobile,
            terrainState.sampleGroundY,
            terrainState.roadCurve,
            routeData.landmarks,
            terrainState.jrCurve,
            terrainState.jrEastCurve
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

        // 8.5 建立人物頭頂專屬位置指標 (Floating Overhead Character Pins)
        createCharacterOverheadMarkers(container);

        // 8.6 建立畫面左上角人物大頭照 (點擊鎖定) 與 IG 便條紙 (Instagram Notes) 狀態列
        createTopLeftAvatarDock(container);

        // 隨機選取 17 處特色景點之一作為本次啟程起點（不再每次都從熊本機場開始，隨機享受全新探索驚喜）
        const randomStartIdx = Math.floor(Math.random() * routeData.landmarks.length);
        const startLandmark = routeData.landmarks[randomStartIdx];
        currentLandmark = startLandmark;

        // 計算該起點景點在自駕環島公路曲線上的精確起點進度 t (0.0 ~ 1.0)
        let startProgress = 0.0;
        if (terrainState && terrainState.roadCurve) {
            let bestT = 0;
            let minD = 999;
            for (let s = 0; s < 600; s++) {
                const t = s / 600;
                const pt = terrainState.roadCurve.getPointAt(t);
                const d = Math.hypot(pt.x - startLandmark.x, pt.z - startLandmark.z);
                if (d < minD) {
                    minD = d;
                    bestT = t;
                }
            }
            startProgress = bestT;
        }
        routeProgress = startProgress;

        // 鏡頭與焦點平滑對準本次隨機起點景點與小巴
        if (controls && camera) {
            controls.target.set(startLandmark.x, 0.75, startLandmark.z);
            camera.position.set(startLandmark.x, 14.8, startLandmark.z + 18.5);
            controls.update();
        }

        updateLocationBanner(currentLandmark);
        updateTourPositions(routeData, 0, 0.016);

        // 9. 事件綁定
        clock = new THREE.Clock();
        renderer.domElement.addEventListener('pointerdown', e => onPointerDown(e, routeData));
        window.addEventListener('resize', () => onResize(container));

        // 啟動高隨機性生活碎嘴對話（打破固定順序與頻率，景點無空白冷場，自然有機隨機輪播）
        function scheduleNextDialogue() {
            setTimeout(() => {
                const now = performance.now();
                if (!isStoppedAtLandmark) {
                    if (!activeSpeaker && banterTimers.length === 0 && now > dialogBusyUntilMs + 320) {
                        // 檢查距離下一個尚未停靠的景點是否還有足夠行車距離，避免剛開講就進站
                        let canSpeak = true;
                        if (terrainState && terrainState.roadCurve) {
                            const vp = terrainState.roadCurve.getPointAt(routeProgress);
                            let minUnvisitedD = 999;
                            routeData.landmarks.forEach(lm => {
                                if (!visitedLandmarksInLap.has(lm.id)) {
                                    const d = Math.hypot(vp.x - lm.x, vp.z - lm.z);
                                    if (d < minUnvisitedD) minUnvisitedD = d;
                                }
                            });
                            if (minUnvisitedD < 1.25) canSpeak = false;
                        }
                        if (canSpeak) {
                            // 動態隨機決定：62% 多人吐槽小劇場、38% 隨機單人突發隨想
                            if (Math.random() < 0.62) {
                                triggerFamilyBanter();
                            } else {
                                const role = pickRandomSpeaker(true);
                                triggerCharacterSpeak(role);
                            }
                        }
                    }
                } else {
                    // 景點停留期間：事件驅動——對話全部說完且動作演出夠久，才開始「準備上車」，上車與呼喊同步進行，無空檔
                    if (!activeSpeaker && banterTimers.length === 0 && !spotArrivalQueueTimer && now > dialogBusyUntilMs + 260 && boardElapsed < 0) {
                        if (!hasPlayedSpotMidstay && stopElapsed > 2.0) {
                            // 景點中段（Mid-Stay）：未發言家人接話 或 現場動作吐槽小劇場（單次停靠至多觸發一次）
                            hasPlayedSpotMidstay = true;
                            const unspoken = ['achun', 'yijhang', 'ayee', 'alu'].filter(r => !spokenRolesInCurrentSpot.has(r));
                            if (unspoken.length > 0 && Math.random() < 0.55 && currentLandmark && currentLandmark.dialogs) {
                                unspoken.sort(() => Math.random() - 0.5);
                                const pickNext = unspoken.slice(0, Math.min(2, unspoken.length));
                                pickNext.forEach(r => spokenRolesInCurrentSpot.add(r));
                                const midScript = pickNext.map(r => ({
                                    role: r,
                                    text: currentLandmark.dialogs[r] || currentLandmark.desc
                                }));
                                triggerCustomBanterScript(midScript, true);
                            } else {
                                const banter = pickRandomNonRepeating(SPOT_MIDSTAY_BANTERS, recentScriptHistories.spotMidstay, 4);
                                if (banter) triggerCustomBanterScript(banter, true);
                            }
                        } else if (hasPlayedSpotMidstay && !hasPlayedSpotDepartureCall && stopElapsed >= SPOT_MIN_DWELL) {
                            // 景點收尾（Departure Call）：呼喊開始的同時，全員走回車旁並依序跳上車
                            hasPlayedSpotDepartureCall = true;
                            boardElapsed = 0;
                            boardTotal = BOARD_MIN;
                            const depCall = pickRandomNonRepeating(SPOT_DEPARTURE_CALLS, recentScriptHistories.spotDeparture, 3);
                            if (depCall) triggerCustomBanterScript(depCall, true);
                        }
                    }
                }
                scheduleNextDialogue();
            }, isStoppedAtLandmark ? (750 + Math.floor(Math.random() * 500)) : (1800 + Math.floor(Math.random() * 1400)));
        }
        scheduleNextDialogue();

        // 預編譯場景內全部著色器（含地形、光影、角色與煙火粒子池、座騎與道具），徹底消除首次互動時的 WebGL 著色器即時編譯頓挫
        if (renderer && scene && camera) {
            const warmupObjects = [];
            if (characters) {
                Object.values(characters).forEach(cg => {
                    const ud = cg.userData;
                    if (!ud) return;
                    ['ufoGroup', 'broomGroup', 'dragonGroup', 'campingDeskGroup', 'picnicMatGroup'].forEach(k => {
                        if (ud[k] && !ud[k].visible) {
                            warmupObjects.push(ud[k]);
                            ud[k].visible = true;
                        }
                    });
                });
            }
            for (let i = 0; i < fireworkPool.length; i++) {
                fireworkPool[i].pSystem.visible = true;
            }
            renderer.compile(scene, camera);
            warmupObjects.forEach(obj => { obj.visible = false; });
            for (let i = 0; i < fireworkPool.length; i++) {
                fireworkPool[i].pSystem.visible = false;
            }
        }

        // 啟動渲染迴圈
        function loop() {
            requestAnimationFrame(loop);
            // 步長嚴格限制在 33ms 內，避免切換分頁或瞬間卡頓時發生巨幅時間步長跳躍 (Hitch Stutter)
            const delta = Math.min(clock.getDelta(), 0.033);
            const elapsed = clock.getElapsedTime();

            Env.updateEnvironment(envState, elapsed, delta);
            window.KyushuIsland.Landmarks.updateLandmarks(landmarkState.animatedLandmarks, elapsed);
            window.KyushuIsland.Props.updatePropsAnimation(propState, terrainState.tramCurve, elapsed, terrainState.jrCurve, terrainState.jrEastCurve);
            updateTourPositions(routeData, elapsed, delta);
            updateLockedCameraFollow();

            controls.update();
            updateBubbleScreenPosition();
            updateCharacterMarkersPosition();
            updateAvatarDockNotes(elapsed);
            updateFireworks(delta);
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
            stopElapsed += delta;
            if (boardElapsed < 0 && stopElapsed > SPOT_MAX_DWELL) {
                boardElapsed = 0; boardTotal = BOARD_MIN; hasPlayedSpotDepartureCall = true;
            }
            if (boardElapsed >= 0) boardElapsed += delta;
            stopTimer = (boardElapsed >= 0) ? Math.max(0, boardTotal - boardElapsed) : 99;
            // 全員就座入定且電動滑門關閉後，立刻發車啟程！徹底告別乾等！
            if (boardElapsed >= 0 && boardElapsed >= BOARD_MIN) {
                boardElapsed = -1;
                isStoppedAtLandmark = false;
                driveCooldown = 2.4; // 啟程後維持約 2.4 秒起步巡航，兼顧每站打卡與公路節奏
                // 恢復離開景點準備啟程時的高頻率落單追車狀態機（60% 落單追車、26% 全員坐車、14% 全家散步）：
                // 阿純開飛碟 (UFO)、阿姨騎魔法掃帚 (Broom)、阿嚕騎東方祥龍 (Dragon)！
                const roll = Math.random();
                if (roll < 0.26) {
                    travelMode = 'all_aboard';
                    stragglerRole = null;
                    if (!activeSpeaker && banterTimers.length === 0) {
                        const carScript = (Math.random() < 0.70)
                            ? pickRandomNonRepeating(IN_CAR_BANTER_SCRIPTS, recentScriptHistories.inCar, 5)
                            : pickRandomNonRepeating(FAMILY_BANTER_SCRIPTS, recentScriptHistories.family, 8);
                        if (carScript) triggerCustomBanterScript(carScript, false);
                    }
                } else if (roll < 0.86) {
                    // 60% 機率由阿純 (飛碟)、阿姨 (掃帚)、阿嚕 (祥龍) 輪替被落下車追車
                    const candidates = ['achun', 'ayee', 'alu'];
                    stragglerRole = candidates[Math.floor(Math.random() * candidates.length)];
                    travelMode = 'straggler_' + stragglerRole;
                    if (!activeSpeaker && banterTimers.length === 0) {
                        const s = pickStragglerScript(stragglerRole);
                        if (s) triggerCustomBanterScript(s, false);
                    }
                } else {
                    travelMode = 'everyone_walk';
                    stragglerRole = null;
                    if (!activeSpeaker && banterTimers.length === 0) {
                        const walkScript = pickWalkTogetherScript();
                        if (walkScript) triggerCustomBanterScript(walkScript, false);
                    }
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

        const asoCrater = routeData._asoCrater || (routeData._asoCrater = routeData.landmarks.find(l => l.id === 'aso_crater'));
        const daikanbo = routeData._daikanbo || (routeData._daikanbo = routeData.landmarks.find(l => l.id === 'daikanbo'));

        // 計算阿蘇火山 (L04) 與大觀峰 (L05) 的山體隆起高度，讓經過或停靠阿蘇火山的角色與車子直接「上山」站在山頭上，絕不被火山擋住！
        function getMountainSummitY(x, z, baseGroundY) {
            let y = baseGroundY;
            if (asoCrater) {
                const lx = asoCrater.renderX !== undefined ? asoCrater.renderX : asoCrater.x;
                const lz = asoCrater.renderZ !== undefined ? asoCrater.renderZ : asoCrater.z;
                const ly = asoCrater.renderY !== undefined ? asoCrater.renderY : baseGroundY;
                const sc = asoCrater.scaleVal || 1.25;
                const d = Math.hypot(x - lx, z - lz);
                const maxR = 1.85 * sc;
                const peakH = 1.20 * sc;
                if (d < maxR) {
                    const ratio = Math.max(0, 1.0 - (d / maxR) * 0.72);
                    y = Math.max(y, ly + peakH * ratio);
                }
            }
            if (daikanbo) {
                const lx = daikanbo.renderX !== undefined ? daikanbo.renderX : daikanbo.x;
                const lz = daikanbo.renderZ !== undefined ? daikanbo.renderZ : daikanbo.z;
                const ly = daikanbo.renderY !== undefined ? daikanbo.renderY : baseGroundY;
                const sc = daikanbo.scaleVal || 1.25;
                const d = Math.hypot(x - lx, z - lz);
                const maxR = 1.20 * sc;
                const peakH = 0.78 * sc;
                if (d < maxR) {
                    const ratio = Math.max(0, 1.0 - (d / maxR) * 0.72);
                    y = Math.max(y, ly + peakH * ratio);
                }
            }
            return y;
        }

        // 檢查是否經過櫻島渡輪海面段 (1.2x 地圖座標)，並動態取樣真實地表高度避免小巴陷入台地
        const onFerry = (vanPos.x > -4.56 && vanPos.x < -3.12 && vanPos.z > 9.78 && vanPos.z < 10.62);
        const rawVanGroundY = Math.max(vanPos.y, getGroundY(vanPos.x, vanPos.z) + 0.05);
        const vanGroundY = onFerry ? 0.38 : getMountainSummitY(vanPos.x, vanPos.z, rawVanGroundY);

        // 方案 A：真・自駕公路旅伴模式 (小巴自然停靠景點專屬車位，絕不變魔術消失，車與人自然解耦漫遊)
        van.visible = true;
        van.scale.setScalar(1.18);
        van.position.set(vanPos.x, vanGroundY, vanPos.z);
        van.rotation.y = vanAngle;

        if (isStoppedAtLandmark) {
            // 景點停靠期：引擎輕柔怠速微震，真實公路旅行沉浸感
            van.position.y += Math.sin(elapsed * 5.0) * 0.003;

            // 姨丈吹哨準備啟程時 (boardElapsed 0~0.6s)，小巴車頭燈親切連閃兩下，按喇叭打信號提醒全家登車！
            if (boardElapsed >= 0 && boardElapsed < 0.6) {
                const blink = Math.sin(boardElapsed * Math.PI * 6.0) > 0;
                if (van.userData.headlights) {
                    van.userData.headlights.forEach(h => { h.intensity = blink ? 3.8 : 0.8; });
                }
            }
        }

        // 控制 Toyota Sienta 左側電動滑門：抵達景點停留時自動向後滑開，全員上車後順暢關閉
        if (van.userData.slidingDoorL) {
            const isBoardingComplete = (boardElapsed >= (BOARD_WALK + BOARD_STAGGER * 3 + BOARD_HOP * 0.8));
            const shouldOpen = isStoppedAtLandmark && !isBoardingComplete;
            const targetDoorZ = shouldOpen ? -0.42 : -0.02;
            const targetDoorX = shouldOpen ? -0.44 : -0.41;
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
            stopElapsed = 0;
            boardElapsed = -1;
            stopTimer = 99;
            spokenRolesInCurrentSpot.clear();
            hasPlayedSpotMidstay = false;
            hasPlayedSpotDepartureCall = false;
            updateLocationBanner(nearest);

            // 檢查目前是否還有「突發追車 / 路途碎嘴對話」正在顯示中：
            // 若還有剩餘閱讀時間，先讓當前對話完整讀完（絕不腰斬！），再無縫接續播放本景點專屬台詞，並把停留秒數自動延長！
            const nowMs = performance.now();
            const remainTransitMs = Math.max(0, dialogBusyUntilMs - nowMs);
            const shuffledRoles = ['achun', 'yijhang', 'ayee', 'alu'].sort(() => Math.random() - 0.5);
            const pickCount = (remainTransitMs > 800) ? 1 : 2;
            const arrivalRoles = shuffledRoles.slice(0, pickCount);
            arrivalRoles.forEach(r => spokenRolesInCurrentSpot.add(r));
            const spotScript = arrivalRoles.map(r => ({
                role: r,
                text: (nearest.dialogs && nearest.dialogs[r]) ? nearest.dialogs[r] : nearest.desc
            }));
            const spotDurationMs = calcScriptDurationMs(spotScript);

            if (spotArrivalQueueTimer) {
                clearTimeout(spotArrivalQueueTimer);
                spotArrivalQueueTimer = null;
            }

            if (remainTransitMs > 120) {
                const handoffDelayMs = remainTransitMs + 200;
                dialogBusyUntilMs = nowMs + handoffDelayMs + spotDurationMs;
                spotArrivalQueueTimer = setTimeout(() => {
                    spotArrivalQueueTimer = null;
                    triggerCustomBanterScript(spotScript, true);
                }, handoffDelayMs);
            } else {
                triggerCustomBanterScript(spotScript, true);
            }
        }

        // Toyota Sienta 全景敞篷車艙內部 4 個座位局部座標 (開放式無車頂，清楚露出 4 位乘員！)
        const carSeatsLocal = {
            yijhang: { x: -0.22, y: 0.28, z: 0.14 },  // 第一排右駕駕駛座
            ayee:    { x: 0.22,  y: 0.28, z: 0.14 },  // 第一排左前副駕駛座
            achun:   { x: 0.23,  y: 0.28, z: -0.26 }, // 第二排左側靠窗舒適位
            alu:     { x: -0.22, y: 0.28, z: -0.26 }  // 第二排右側靠窗位
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

        // 第一階段：計算每位角色的基礎目標座標（在車內坐定，或在車外候車/漫步/追車）
        const outsideChars = [];

        roles.forEach((role, idx) => {
            const charGroup = characters[role];
            if (!charGroup) return;
            const off = walkOffsets[idx];

            // 判斷這位家人現在是否坐在 Toyota Sienta 車廂內
            // 景點停靠時的上車進度：走回車旁 → 依序跳入座位 (hop 0~1)
            let hop = 0;
            if (isStoppedAtLandmark && boardElapsed >= 0) {
                hop = Math.max(0, Math.min(1, (boardElapsed - BOARD_WALK - idx * BOARD_STAGGER) / BOARD_HOP));
            }
            const isAboard = (!isStoppedAtLandmark && (
                travelMode === 'all_aboard' ||
                (travelMode.startsWith('straggler_') && role !== stragglerRole) ||
                onFerry
            )) || (isStoppedAtLandmark && hop >= 1);

            charGroup.userData.isAboard = isAboard;
            charGroup.userData.isUfoChasing = (role === 'achun' && role === stragglerRole && !isStoppedAtLandmark && !isAboard);
            charGroup.userData.isBroomChasing = (role === 'ayee' && role === stragglerRole && !isStoppedAtLandmark && !isAboard);
            charGroup.userData.isDragonChasing = (role === 'alu' && role === stragglerRole && !isStoppedAtLandmark && !isAboard);

            if (isAboard) {
                // 1. 真的坐在 Sienta 全景敞篷休旅車上（無天花板遮擋，清晰露出家人招牌打扮）
                const seat = carSeatsLocal[role];
                const worldX = van.position.x + seat.x * cosA + seat.z * sinA;
                const worldZ = van.position.z - seat.x * sinA + seat.z * cosA;
                const jumpBoost = (charGroup.userData.jumping > 0) ? Math.sin(charGroup.userData.jumping * Math.PI) * 0.18 : 0;

                charGroup.scale.setScalar(0.72);
                charGroup.position.set(worldX, van.position.y + seat.y + jumpBoost, worldZ);
                charGroup.rotation.y = vanAngle;
                charGroup.userData.baseY = van.position.y + seat.y;
                charGroup.userData.prevX = worldX;
                charGroup.userData.prevZ = worldZ;
                charGroup.userData.wasAboard = true;

                window.KyushuIsland.Characters.animateCharacterPose(
                    charGroup,
                    elapsed,
                    delta,
                    'seated'
                );
                return;
            }

            // 跳上車動畫：從車門旁沿弧線躍入座位（取代瞬間傳送入座）
            if (isStoppedAtLandmark && hop > 0 && hop < 1) {
                const seatH = carSeatsLocal[role];
                const seatWX = van.position.x + seatH.x * cosA + seatH.z * sinA;
                const seatWZ = van.position.z - seatH.x * sinA + seatH.z * cosA;
                const seatWY = van.position.y + seatH.y;
                const dLX = -0.82, dLZ = (idx - 1.5) * 0.48;
                const doorWX = vanPos.x + (dLX * cosA + dLZ * sinA);
                const doorWZ = vanPos.z + (-dLX * sinA + dLZ * cosA);
                const doorWY = Math.max(van.position.y, getGroundY(doorWX, doorWZ) + 0.05);
                const e = hop * hop * (3 - 2 * hop);
                charGroup.scale.setScalar(0.96 + (0.72 - 0.96) * e);
                charGroup.position.set(
                    doorWX + (seatWX - doorWX) * e,
                    doorWY + (seatWY - doorWY) * e + Math.sin(hop * Math.PI) * 0.34,
                    doorWZ + (seatWZ - doorWZ) * e
                );
                charGroup.rotation.y = vanAngle;
                charGroup.userData.baseY = seatWY;
                charGroup.userData.prevX = charGroup.position.x;
                charGroup.userData.prevZ = charGroup.position.z;
                charGroup.userData.isSpotBusy = false;
                window.KyushuIsland.Characters.animateCharacterPose(charGroup, elapsed, delta, 'seated');
                return;
            }

            // 在車外時恢復標準 0.96x 飽滿比例
            charGroup.scale.setScalar(0.96);
            let cx, cz, cRotY;
            let customSummitY = null;
            let isMovingOutside = !isStoppedAtLandmark;
            const isSummitSpot = isStoppedAtLandmark && currentLandmark && (currentLandmark.id === 'aso_crater' || currentLandmark.id === 'daikanbo');
            let roamWeight = 0;

            // Sienta 左側電動滑門旁集合點 (車身外側 0.82m，沿車身長度均勻間隔 0.48m，完全避免人物與車身及相互穿模)
            const doorLocalX = -0.82;
            const doorLocalZ = (idx - 1.5) * 0.48;
            const doorSideX = vanPos.x + (doorLocalX * cosA + doorLocalZ * sinA);
            const doorSideZ = vanPos.z + (-doorLocalX * sinA + doorLocalZ * cosA);
            const doorSideY = van.position.y;

            if (isStoppedAtLandmark && currentLandmark) {
                // 計算停留階段權重：剛停車 1.2 秒內從車旁散開 (0➔1)、停留期間就位做各自動作、開車前最後 1.8 秒走回車旁 (1➔0)
                const leaveCarFactor = Math.min(1.0, stopElapsed / 1.20);
                const returnCarFactor = (boardElapsed < 0) ? 1.0 : Math.max(0, 1.0 - boardElapsed / BOARD_WALK);
                roamWeight = leaveCarFactor * returnCarFactor; // 0 = 在車旁集合，1 = 在景點定位定點

                // 剛下車防瞬移安全錨定：若剛下車或 prevX 殘留遠端舊坐標，強制重置起點為車門旁！
                if (charGroup.userData.wasAboard || charGroup.userData.prevX === undefined || Math.hypot(charGroup.userData.prevX - doorSideX, charGroup.userData.prevZ - doorSideZ) > 3.2) {
                    charGroup.userData.prevX = doorSideX;
                    charGroup.userData.prevZ = doorSideZ;
                    charGroup.position.set(doorSideX, doorSideY, doorSideZ);
                    charGroup.userData.wasAboard = false;
                }

                let spotAnchorX, spotAnchorZ, spotAnchorY;
                if (isSummitSpot) {
                    // 抵達阿蘇火山 (L04) 或大觀峰 (L05)：登上山頂火口觀景台 / 展望台安全木棧平臺 (緊湊集中於觀景台範圍內，半徑收縮至安全區，絕不跌出山崖飄浮)
                    const lx = currentLandmark.renderX !== undefined ? currentLandmark.renderX : currentLandmark.x;
                    const lz = currentLandmark.renderZ !== undefined ? currentLandmark.renderZ : currentLandmark.z;
                    const ly = currentLandmark.renderY !== undefined ? currentLandmark.renderY : getGroundY(lx, lz);
                    const sc = currentLandmark.scaleVal || 1.20;
                    const summitSpread = (idx - 1.5) * 0.48; // 緊湊對稱於觀景台中心兩側
                    spotAnchorX = lx + summitSpread;
                    spotAnchorZ = lz + ((currentLandmark.id === 'aso_crater') ? 0.36 * sc : 0.25 * sc);
                    spotAnchorY = ly + ((currentLandmark.id === 'aso_crater') ? 1.18 * sc : 0.76 * sc);
                } else {
                    // 適度擴展下車漫步範圍（半徑 1.8~2.5 米，既具探索感又保證安全在觀景台/路旁平臺內）
                    const roamAnchorsLocal = [
                        { x: -1.75, z: 1.45 }, // 阿純：在開闊草地展開小木桌打病歷
                        { x:  1.35, z: 1.15 }, // 姨丈：在路旁觀景避車彎靠著護欄玩手遊
                        { x: -0.65, z: 2.05 }, // 阿姨：走進景觀前沿開心採買與拍照
                        { x:  1.60, z: 2.20 }  // 阿嚕：跑到最前緣高點架相機取景
                    ];
                    const ra = roamAnchorsLocal[idx];
                    spotAnchorX = vanPos.x + (ra.x * cosA + ra.z * sinA);
                    spotAnchorZ = vanPos.z + (-ra.x * sinA + ra.z * cosA);

                    // 景點錨點安全性初篩：若錨點已經超出海岸線，沿射線平滑收縮至陸地內
                    if (mainlandCoastPts && window.KyushuIsland.Terrain.isPointInPolygon) {
                        const isInsideSafe = (x, z) => window.KyushuIsland.Terrain.isPointInPolygon(x, z, mainlandCoastPts, 1.0, 0.96, -2.40);
                        if (!isInsideSafe(spotAnchorX, spotAnchorZ)) {
                            let safeT = 0.0;
                            for (let step = 1; step <= 8; step++) {
                                const testT = safeT + (1.0 - safeT) * 0.5;
                                const tx = doorSideX + (spotAnchorX - doorSideX) * testT;
                                const tz = doorSideZ + (spotAnchorZ - doorSideZ) * testT;
                                if (isInsideSafe(tx, tz)) safeT = testT;
                            }
                            safeT = Math.max(0.10, safeT - 0.08);
                            spotAnchorX = doorSideX + (spotAnchorX - doorSideX) * safeT;
                            spotAnchorZ = doorSideZ + (spotAnchorZ - doorSideZ) * safeT;
                        }
                    }
                    spotAnchorY = Math.max(doorSideY, getGroundY(spotAnchorX, spotAnchorZ) + 0.05);
                }

                // 景點自由生動漫步：阿姨與阿嚕在廣闊區域內自由踱步賞景，阿純與姨丈定點時亦有悠閒身體微動
                let wanderX = 0;
                let wanderZ = 0;
                if (isSummitSpot) {
                    // 山頂地段安全微動：在山頂觀景台上適度微動 (半徑 <= 0.10m)，絕不因隨意大幅走動而走出木棧台懸空飄浮！
                    const wPhase = elapsed * 0.9 + idx * 2.0;
                    wanderX = (Math.sin(wPhase) * 0.08) * roamWeight;
                    wanderZ = (Math.cos(wPhase * 0.7) * 0.06) * roamWeight;
                } else if (role === 'ayee') {
                    // 阿姨逛特產店、四處走動：半徑達 0.55m 的自由探索八字形動態軌跡
                    const wPhase = elapsed * 1.1 + idx * 1.7;
                    wanderX = (Math.sin(wPhase) * 0.55) * roamWeight;
                    wanderZ = (Math.cos(wPhase * 0.7) * 0.45) * roamWeight;
                } else if (role === 'alu') {
                    // 阿嚕舉著相機換視角取景：前後左右找最佳拍攝角度
                    const wPhase = elapsed * 0.95 + idx * 2.3;
                    wanderX = (Math.sin(wPhase * 0.8) * 0.42) * roamWeight;
                    wanderZ = (Math.cos(wPhase * 1.2) * 0.36) * roamWeight;
                } else if (role === 'yijhang') {
                    // 姨丈路旁踱步推墨鏡
                    const wPhase = elapsed * 0.6 + idx * 3.1;
                    wanderX = (Math.sin(wPhase) * 0.22) * roamWeight;
                    wanderZ = (Math.cos(wPhase * 0.9) * 0.18) * roamWeight;
                }

                cx = doorSideX + (spotAnchorX - doorSideX) * roamWeight + wanderX;
                cz = doorSideZ + (spotAnchorZ - doorSideZ) * roamWeight + wanderZ;
                if (isSummitSpot) {
                    // 山頂真實高度：依據角色當前腳下即時坐標取樣山體表面，杜絕固定線性插值導致的懸空飄起！
                    const summitSurfaceY = getMountainSummitY(cx, cz, getGroundY(cx, cz) + 0.05);
                    customSummitY = doorSideY + (summitSurfaceY - doorSideY) * roamWeight;
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

            // 核心優化：僅在「景點停靠自由散步」且正在說話時，平緩定點避免氣泡大幅漂移；在公路上行走時持續等速並行，絕不定格或瞬間跳躍！
            const isSpeakingNow = (activeSpeaker === role);
            if (isStoppedAtLandmark && isSpeakingNow && boardElapsed < 0 && charGroup.userData.prevX !== undefined && Math.hypot(charGroup.userData.prevX - vanPos.x, charGroup.userData.prevZ - vanPos.z) < 3.2) {
                cx = charGroup.userData.prevX;
                cz = charGroup.userData.prevZ;
                isMovingOutside = false;
            }

            // 嚴格陸地邊界防跌落安全錨定（Coastline Safety Clamping）
            // 解決 1: 鵜戶神宮等靠海狹長景點人物走出陸地掉進海裡
            // 解決 2: 避免大倍率階躍造成的邊界來回抽搐震顫
            if (isStoppedAtLandmark && !isSummitSpot && mainlandCoastPts && window.KyushuIsland.Terrain.isPointInPolygon) {
                const isInside = (x, z) => window.KyushuIsland.Terrain.isPointInPolygon(x, z, mainlandCoastPts, 1.0, 0.96, -2.40);
                if (!isInside(cx, cz)) {
                    let safeT = 0.0;
                    for (let step = 1; step <= 10; step++) {
                        const testT = safeT + (1.0 - safeT) * 0.5;
                        const tx = doorSideX + (cx - doorSideX) * testT;
                        const tz = doorSideZ + (cz - doorSideZ) * testT;
                        if (isInside(tx, tz)) safeT = testT;
                    }
                    safeT = Math.max(0.05, safeT - 0.03); // 平滑拉回陸地邊界，保留充足安全餘裕
                    cx = doorSideX + (cx - doorSideX) * safeT;
                    cz = doorSideZ + (cz - doorSideZ) * safeT;
                }
            }

            outsideChars.push({
                role,
                idx,
                charGroup,
                cx,
                cz,
                cRotY: cRotY || 0,
                customSummitY,
                doorSideX,
                doorSideZ,
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

            // 2. 人物與 Toyota Sienta 休旅車之間 OBB 碰撞盒嚴格避讓，永不穿透車身 (若小巴已收入姨丈口袋則免避讓)
            outsideChars.forEach(c => {
                if (c.isSummitSpot && c.roamWeight > 0.40) return; // 山頂平台遠離停車場小巴
                if (isStoppedAtLandmark && van.scale.x < 0.25) return; // 小巴已魔法收進姨丈口袋，開放全區自由行走
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
            // 採用 AABB 邊界盒快速剔除 (Fast-exit)，且僅在第 0 次迭代計算，大幅減少 99% 無效計算
            if (iter === 0 && obstacles.length > 0) {
                outsideChars.forEach(c => {
                    for (let oi = 0; oi < obstacles.length; oi++) {
                        const obs = obstacles[oi];
                        const dx = c.cx - obs.x;
                        if (dx > 1.2 || dx < -1.2) continue;
                        const dz = c.cz - obs.z;
                        if (dz > 1.2 || dz < -1.2) continue;
                        const minD = obs.r + 0.24;
                        const distSq = dx * dx + dz * dz;
                        if (distSq < minD * minD && distSq > 0.00001) {
                            const d = Math.sqrt(distSq);
                            c.cx = obs.x + (dx / d) * minD;
                            c.cz = obs.z + (dz / d) * minD;
                        }
                    }
                });
            }
        }

        // 確保避讓後的最終座標依然不越過陸地邊界，消除障礙物與海岸線邊界互推震盪（在 3 次碰撞迭代後統一解析一次，省下 90% 多邊形計算）
        if (isStoppedAtLandmark && mainlandCoastPts && window.KyushuIsland.Terrain.isPointInPolygon) {
            const isInside = (x, z) => window.KyushuIsland.Terrain.isPointInPolygon(x, z, mainlandCoastPts, 1.0, 0.96, -2.40);
            outsideChars.forEach(c => {
                if (c.isSummitSpot) return;
                if (!isInside(c.cx, c.cz)) {
                    let safeT = 0.0;
                    const dsX = (c.doorSideX !== undefined) ? c.doorSideX : vanPos.x;
                    const dsZ = (c.doorSideZ !== undefined) ? c.doorSideZ : vanPos.z;
                    for (let step = 1; step <= 8; step++) {
                        const testT = safeT + (1.0 - safeT) * 0.5;
                        const tx = dsX + (c.cx - dsX) * testT;
                        const tz = dsZ + (c.cz - dsZ) * testT;
                        if (isInside(tx, tz)) safeT = testT;
                    }
                    safeT = Math.max(0.05, safeT - 0.03);
                    c.cx = dsX + (c.cx - dsX) * safeT;
                    c.cz = dsZ + (c.cz - dsZ) * safeT;
                }
            });
        }

        // 第三階段：套用最終安全座標、平滑插值濾波、朝向阻尼、物理高度與專屬姿態動畫
        outsideChars.forEach(c => {
            const charGroup = c.charGroup;
            const prevX = (charGroup.userData.prevX !== undefined) ? charGroup.userData.prevX : c.cx;
            const prevZ = (charGroup.userData.prevZ !== undefined) ? charGroup.userData.prevZ : c.cz;

            // 平滑插值濾波 (Exponential Smoothing Filter) 徹底消除邊界與碰撞引發的微幅高頻顫抖 (Tremble/Jitter)
            let finalX = c.cx;
            let finalZ = c.cz;
            const distFromPrev = Math.hypot(c.cx - prevX, c.cz - prevZ);
            if (charGroup.userData.prevX !== undefined && distFromPrev < 1.0) {
                const smoothAlpha = Math.min(1.0, delta * 15.0);
                finalX = prevX + (c.cx - prevX) * smoothAlpha;
                finalZ = prevZ + (c.cz - prevZ) * smoothAlpha;
            }

            const vx = (finalX - prevX) / Math.max(delta, 0.001);
            const vz = (finalZ - prevZ) / Math.max(delta, 0.001);
            const moveSpd = Math.hypot(vx, vz);

            // 具有滯後閾值 (Hysteresis) 的移動判定，杜絕狀態在邊界時快速反覆切換導致的配件閃爍
            let moving = charGroup.userData.wasMoving ? (moveSpd > 0.04) : (moveSpd > 0.09);
            charGroup.userData.wasMoving = moving;

            // 判定是否正處於景點專屬個性動作持續進行期 (已就位且尚未準備上車)
            const isInSpotActivity = c.isStoppedAtLandmark && (c.roamWeight >= 0.75) && (boardElapsed < 0);
            const curYaw = charGroup.rotation.y || 0;
            let targetYaw = curYaw;

            if (isInSpotActivity) {
                // 阿純定點打字、姨丈定點玩試管；阿姨與阿嚕在景點大範圍漫步時保持靈活步伐動畫
                if (c.role === 'achun') {
                    moving = false; // 確保阿純席地坐姿穩定不站起
                    targetYaw = vanAngle + 0.25;
                } else if (c.role === 'ayee' || c.role === 'alu') {
                    if (moving && moveSpd > 0.12) {
                        targetYaw = Math.atan2(vx, vz);
                    } else {
                        targetYaw = vanAngle + (c.idx - 1.5) * 0.40;
                    }
                } else {
                    targetYaw = vanAngle - 0.20;
                }
            } else if (c.isSpeakingNow && c.isStoppedAtLandmark) {
                moving = false;
                targetYaw = vanAngle + Math.sin(elapsed * 0.9 + c.idx) * 0.25;
            } else if (c.isStoppedAtLandmark) {
                if (moving && moveSpd > 0.12) {
                    targetYaw = Math.atan2(vx, vz);
                } else {
                    targetYaw = vanAngle + Math.sin(elapsed * 0.9 + c.idx) * 0.28;
                }
            } else {
                targetYaw = c.cRotY;
            }

            // 角度差最短路徑平滑插值 (Angular Lerp)，杜絕面朝方向 180 度來回抽搐翻轉 (Flapping)
            let diff = targetYaw - curYaw;
            while (diff > Math.PI) diff -= Math.PI * 2;
            while (diff < -Math.PI) diff += Math.PI * 2;
            const finalRotY = curYaw + diff * Math.min(1.0, delta * 9.0);

            charGroup.position.x = finalX;
            charGroup.position.z = finalZ;
            charGroup.rotation.y = finalRotY;
            charGroup.userData.prevX = finalX;
            charGroup.userData.prevZ = finalZ;

            const charOnFerry = (finalX > -4.56 && finalX < -3.12 && finalZ > 9.78 && finalZ < 10.62);
            // 嚴格貼地高度：在景點漫步時，以自身所在座標的地表高度 getGroundY 為準，徹底杜絕因為 vanGroundY 較高而飄浮在空中！
            const actualGroundY = getGroundY(finalX, finalZ) + 0.05;
            const rawCharY = c.isStoppedAtLandmark ? actualGroundY : Math.max(vanGroundY, actualGroundY);
            const targetBaseY = charOnFerry
                ? 0.42
                : (c.customSummitY !== null ? c.customSummitY : getMountainSummitY(finalX, finalZ, rawCharY));

            // 高度亦進行阻尼平滑，杜絕地表高程微跳導致的垂直抖動與陰影閃爍
            const prevBaseY = (charGroup.userData.baseY !== undefined) ? charGroup.userData.baseY : targetBaseY;
            charGroup.userData.baseY = prevBaseY + (targetBaseY - prevBaseY) * Math.min(1.0, delta * 12.0);

            // 景點專屬個性動作標記：
            // 只要在移動邁步 (moving)，阿純與阿姨絕對不處於 busy 狀態，徹底杜絕帶著桌子或野餐墊走動！
            charGroup.userData.isSpotBusy = isInSpotActivity && !moving;

            // 若是落單追車苦主，加快腳步頻率並舉手揮動呼喊；景點散開漫步或走回車旁時亦播放雙腳邁步動畫
            const animElapsed = (c.role === stragglerRole && !c.isStoppedAtLandmark) ? elapsed * 1.65 : elapsed;
            window.KyushuIsland.Characters.animateCharacterPose(
                charGroup,
                animElapsed,
                delta,
                moving
            );
            const isChasingOnMount = (charGroup.userData.isUfoChasing || charGroup.userData.isBroomChasing || charGroup.userData.isDragonChasing);
            if (c.role === stragglerRole && !c.isStoppedAtLandmark && !isChasingOnMount && charGroup.userData.armL) {
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

    // 根據台詞字數動態計算對話框停留時間：確保文字有充分閱讀時間（基礎 3.6 秒 + 每個字 110 毫秒，最短 4.8 秒，最長 7.8 秒）
    function calcReadDurationMs(text) {
        const len = (text || '').length;
        return Math.max(4800, Math.min(7800, 3600 + len * 110));
    }

    function calcScriptDurationMs(script) {
        if (!script || !script.length) return 0;
        let total = 0;
        script.forEach((line, idx) => {
            total += calcReadDurationMs(line.text);
            if (idx < script.length - 1) total += 520;
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
            // 下一句在當前這句完整顯示完畢後，再留 520ms 舒適呼吸間隔接話
            cumulativeDelay += lineReadMs + 520;
        });
        dialogBusyUntilMs = performance.now() + cumulativeDelay - 520;

        // 啟程呼喊台詞在行駛中亦能平順閱讀，絕不在車內長時間死等對話！
        // 上車程序總長嚴格由全員入座與滑門關閉時間決定（約 3.1 秒），入座後即刻發車
    }

    // 抵達景點下車時，觸發該景點專屬的接力感言 (1~3人隨機洗牌，發言順序全隨機)
    function triggerLandmarkArrivalDialog(lm) {
        if (lm && lm.dialogs) {
            const shuffledRoles = ['achun', 'yijhang', 'ayee', 'alu'].sort(() => Math.random() - 0.5);
            const rollCount = Math.random();
            const pickCount = (rollCount < 0.22) ? 1 : (rollCount < 0.72 ? 2 : 3);
            const picked = shuffledRoles.slice(0, pickCount);
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

    // 觸發一段角色間互相吐槽與接話的碎嘴小劇場 (根據目前狀態智慧無重複隨機輪播)
    function triggerFamilyBanter() {
        if (!isStoppedAtLandmark) {
            if (travelMode.startsWith('straggler_') && stragglerRole && STRAGGLER_BANTER_SCRIPTS[stragglerRole]) {
                const s = pickStragglerScript(stragglerRole);
                if (s) {
                    triggerCustomBanterScript(s, false);
                    return;
                }
            }
            if (travelMode === 'all_aboard') {
                const carScript = (Math.random() < 0.75)
                    ? pickRandomNonRepeating(IN_CAR_BANTER_SCRIPTS, recentScriptHistories.inCar, 5)
                    : pickRandomNonRepeating(FAMILY_BANTER_SCRIPTS, recentScriptHistories.family, 8);
                if (carScript) {
                    triggerCustomBanterScript(carScript, false);
                    return;
                }
            }
            if (travelMode === 'everyone_walk') {
                const walkScript = pickWalkTogetherScript();
                if (walkScript) {
                    triggerCustomBanterScript(walkScript, false);
                    return;
                }
            }
        }
        const script = pickRandomNonRepeating(FAMILY_BANTER_SCRIPTS, recentScriptHistories.family, 8);
        if (script) {
            triggerCustomBanterScript(script, false);
        }
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
            const history = recentScriptHistories.soloQuotes[role] || (recentScriptHistories.soloQuotes[role] = []);
            text = pickRandomNonRepeating(pool, history, 4);
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

    const _tempBubblePos = new THREE.Vector3();

    function updateBubbleScreenPosition() {
        if (!activeSpeaker || !characters[activeSpeaker] || !camera || !renderer) return;
        const bubble = document.getElementById('char-speech-bubble');
        if (!bubble) return;

        const charGroup = characters[activeSpeaker];
        charGroup.getWorldPosition(_tempBubblePos);
        _tempBubblePos.y += 1.95;
        _tempBubblePos.project(camera);

        const x = (_tempBubblePos.x * 0.5 + 0.5) * canvasW;
        const y = (-(_tempBubblePos.y * 0.5) + 0.5) * canvasH;

        const halfW = Math.min(136, canvasW / 2 - 6);
        const clampedX = Math.max(halfW, Math.min(canvasW - halfW, x));
        const clampedY = Math.max(85, Math.min(canvasH - 35, y));

        bubble.style.left = `${clampedX}px`;
        bubble.style.top = `${clampedY}px`;
    }

    // 畫面左上角人物大頭照 (點擊切換鎖定) 與 IG 便條紙 (Instagram Notes) 狀態列管理器
    let charAvatars = {};

    function createTopLeftAvatarDock(container) {
        charAvatars = {};
        const oldDock = container.querySelector('#kyushu-avatar-dock');
        if (oldDock) oldDock.remove();

        // 狀態列平時收合（僅顯示頭像，不遮擋 3D 畫面）；桌機 hover、手機點擊頭像時才展開便條紙
        if (!document.getElementById('kyushu-avatar-dock-style')) {
            const dockStyle = document.createElement('style');
            dockStyle.id = 'kyushu-avatar-dock-style';
            dockStyle.textContent = `
                #kyushu-avatar-dock .ig-note-block { display:none; }
                #kyushu-avatar-dock.expanded .ig-note-block { display:flex; animation: kyushuNoteIn 0.18s ease-out; }
                #kyushu-avatar-dock .kyushu-avatar-btn.speaking { box-shadow:0 0 0 3px rgba(239,68,68,0.55), 0 2px 6px rgba(0,0,0,0.15) !important; animation: kyushuSpeakPulse 1.1s ease-in-out infinite; }
                @keyframes kyushuNoteIn { from { opacity:0; transform:translateX(-6px); } to { opacity:1; transform:none; } }
                @keyframes kyushuSpeakPulse { 0%,100% { transform:scale(1); } 50% { transform:scale(1.12); } }
                @media (max-width: 640px) {
                    #kyushu-avatar-dock { top:8px !important; left:8px !important; gap:5px !important; }
                    #kyushu-avatar-dock .kyushu-avatar-btn { width:38px !important; height:38px !important; font-size:18px !important; }
                    #kyushu-avatar-dock .ig-note-bubble { height:auto !important; min-height:26px; padding:4px 9px !important; max-width:52vw !important; }
                    #kyushu-avatar-dock .ig-note-text { font-size:12px !important; max-width:48vw !important; }
                }
            `;
            document.head.appendChild(dockStyle);
        }

        const dock = document.createElement('div');
        dock.id = 'kyushu-avatar-dock';
        dock.style.cssText = [
            'position:absolute;',
            'top:12px;',
            'left:12px;',
            'z-index:32;',
            'display:flex;',
            'flex-direction:column;',
            'align-items:flex-start;',
            'gap:6px;',
            'pointer-events:none;',
            'user-select:none;'
        ].join('');

        // 排序嚴格遵循：阿純 ➔ 阿姨 ➔ 姨丈 ➔ 啊嚕
        const roleOrder = ['achun', 'ayee', 'yijhang', 'alu'];
        const roleEmojis = { achun: '🧶', ayee: '🍡', yijhang: '🕶️', alu: '🐻' };
        const roleShortNames = { achun: '阿純', ayee: '阿姨', yijhang: '姨丈', alu: '啊嚕' };

        roleOrder.forEach(role => {
            const st = ROLE_MARKER_STYLES[role];
            const item = document.createElement('div');
            item.className = 'kyushu-avatar-item';
            item.dataset.role = role;
            item.style.cssText = [
                'display:flex;',
                'flex-direction:row;',
                'align-items:center;',
                'gap:4px;',
                'pointer-events:auto;',
                'cursor:pointer;',
                'transition:transform 0.16s ease;'
            ].join('');

            // 左側頭像與名字直列包裝 (Avatar Block)
            const avatarBlock = document.createElement('div');
            avatarBlock.style.cssText = [
                'display:flex;',
                'flex-direction:column;',
                'align-items:center;',
                'position:relative;',
                'flex-shrink:0;'
            ].join('');

            // 圓形大頭照按鈕 (縮小至 34px × 34px)
            const avatarBtn = document.createElement('div');
            avatarBtn.className = 'kyushu-avatar-btn';
            avatarBtn.style.cssText = [
                'width:34px;',
                'height:34px;',
                'border-radius:9999px;',
                `background:${st.bg};`,
                `border:2px solid ${st.border};`,
                'display:flex;',
                'align-items:center;',
                'justify-content:center;',
                'font-size:16px;',
                'box-shadow:0 2px 6px rgba(0,0,0,0.10);',
                'position:relative;',
                'transition:transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;'
            ].join('');
            avatarBtn.textContent = roleEmojis[role] || '👤';

            // 鎖定角標 🔒
            const lockBadge = document.createElement('span');
            lockBadge.className = 'ig-avatar-lock-badge';
            lockBadge.style.cssText = [
                'position:absolute;',
                'bottom:-2px;',
                'right:-2px;',
                'background:#ef4444;',
                'color:#ffffff;',
                'font-size:7.5px;',
                'font-weight:900;',
                'border-radius:999px;',
                'padding:0.5px 3px;',
                'border:1.2px solid #ffffff;',
                'box-shadow:0 1px 3px rgba(0,0,0,0.3);',
                'display:none;'
            ].join('');
            lockBadge.textContent = '🔒';
            avatarBtn.appendChild(lockBadge);

            // 角色名字膠囊標籤 (精巧 8.5px)
            const nameBadge = document.createElement('div');
            nameBadge.style.cssText = [
                'background:rgba(255,255,255,0.92);',
                'border:1px solid rgba(0,0,0,0.08);',
                'border-radius:999px;',
                'padding:0.5px 4.5px;',
                'font-size:8.5px;',
                'font-weight:900;',
                'color:#1e293b;',
                'margin-top:1px;',
                'box-shadow:0 1px 2px rgba(0,0,0,0.06);',
                'white-space:nowrap;'
            ].join('');
            nameBadge.textContent = roleShortNames[role] || role;

            avatarBlock.appendChild(avatarBtn);
            avatarBlock.appendChild(nameBadge);

            // 右側：狀態便條紙區塊 (Note Block: 包含向左指的小尾巴 + 便條紙氣泡)
            const noteBlock = document.createElement('div');
            noteBlock.className = 'ig-note-block';
            noteBlock.style.cssText = [
                'align-items:center;',
                'position:relative;'
            ].join('');

            // 向左指的小尾巴 (Left-pointing Triangle Tail)
            const noteTail = document.createElement('div');
            noteTail.className = 'ig-note-tail';
            noteTail.style.cssText = [
                'width:0;',
                'height:0;',
                'border-top:4px solid transparent;',
                'border-bottom:4px solid transparent;',
                `border-right:5px solid ${st.border};`,
                'margin-right:-1px;',
                'flex-shrink:0;',
                'transition:border-color 0.16s ease;'
            ].join('');

            // 便條紙氣泡 (精緻小巧，高度 23px)
            const noteBubble = document.createElement('div');
            noteBubble.className = 'ig-note-bubble';
            noteBubble.style.cssText = [
                'background:#ffffff;',
                `border:1.5px solid ${st.border};`,
                'border-radius:10px;',
                'padding:2.5px 7px;',
                'box-shadow:0 2px 8px rgba(0,0,0,0.10);',
                'max-width:145px;',
                'min-width:54px;',
                'height:23px;',
                'display:flex;',
                'align-items:center;',
                'justify-content:center;',
                'box-sizing:border-box;',
                'transition:border-color 0.16s ease, box-shadow 0.16s ease;'
            ].join('');

            const noteTextEl = document.createElement('span');
            noteTextEl.className = 'ig-note-text';
            noteTextEl.style.cssText = [
                'font-size:9.5px;',
                'font-weight:800;',
                'color:#1e293b;',
                'line-height:1.2;',
                'white-space:nowrap;',
                'overflow:hidden;',
                'text-overflow:ellipsis;',
                'max-width:130px;',
                'display:block;'
            ].join('');
            noteTextEl.textContent = '…';
            noteBubble.appendChild(noteTextEl);

            noteBlock.appendChild(noteTail);
            noteBlock.appendChild(noteBubble);

            item.appendChild(avatarBlock);
            item.appendChild(noteBlock);

            item.addEventListener('mouseenter', () => {
                if (lockedRole !== role) {
                    avatarBtn.style.transform = 'scale(1.08)';
                    noteBubble.style.transform = 'translateX(2px)';
                }
            });
            item.addEventListener('mouseleave', () => {
                if (lockedRole !== role) {
                    avatarBtn.style.transform = 'scale(1)';
                    noteBubble.style.transform = 'translateX(0)';
                }
            });
            item.addEventListener('click', ev => {
                ev.stopPropagation();
                focusCharacter(role);
                // 觸控裝置：點擊頭像同時展開便條紙 4 秒後自動收合
                if (dock._isTouch) {
                    dock.classList.add('expanded');
                    clearTimeout(dock._collapseTimer);
                    dock._collapseTimer = setTimeout(() => dock.classList.remove('expanded'), 4000);
                }
            });

            dock.appendChild(item);
            charAvatars[role] = {
                item,
                noteBubble,
                noteTextEl,
                noteTail,
                avatarBtn,
                lockBadge,
                borderCol: st.border
            };
        });

        dock.addEventListener('pointerdown', ev => { dock._isTouch = (ev.pointerType === 'touch' || ev.pointerType === 'pen'); });
        dock.addEventListener('mouseenter', () => {
            if (!dock._isTouch) dock.classList.add('expanded');
        });
        dock.addEventListener('mouseleave', () => {
            if (!dock._isTouch) dock.classList.remove('expanded');
        });

        container.appendChild(dock);
    }

    // 動態更新左上角大頭照旁的 IG 便條紙狀態文字（支援景點專屬個性動作、行車打瞌睡/手遊、追車狂奔與發言狀態）
    function updateAvatarDockNotes(elapsed) {
        const roles = ['achun', 'yijhang', 'ayee', 'alu'];
        for (let i = 0; i < roles.length; i++) {
            const role = roles[i];
            const av = charAvatars[role];
            if (!av) continue;

            const cg = characters[role];
            const isSpeaking = (activeSpeaker === role);
            let targetText = '';

            if (isSpeaking) {
                targetText = '💬 發言中…';
            } else if (isStoppedAtLandmark) {
                if (boardElapsed >= BOARD_WALK) {
                    targetText = '🚗 順暢入座就位！';
                } else if (boardElapsed >= 0) {
                    if (role === 'yijhang') targetText = '🚙 駕駛門旁吹哨喊上車！';
                    else if (role === 'achun') targetText = '💻 收起筆電小跑步回車！';
                    else if (role === 'alu') targetText = '📸 關閉閃光燈快步登車！';
                    else targetText = '🧺 收好點心快步登車！';
                } else {
                    const list = ROLE_SPOT_STATUSES[role] || [];
                    const sIdx = Math.floor(elapsed * 0.30) % (list.length || 1);
                    targetText = list[sIdx] || '';
                }
            } else {
                if (role === stragglerRole) {
                    if (role === 'achun') targetText = '🛸 飛碟追車！';
                    else if (role === 'ayee') targetText = '🧹 魔法掃帚飛行！';
                    else if (role === 'alu') targetText = '🐉 祥龍騰雲追車！';
                    else targetText = '🏃 狂奔追車中！';
                } else if (cg && cg.userData && cg.userData.isAboard) {
                    const list = ROLE_DRIVE_STATUSES[role] || [];
                    const dIdx = Math.floor(elapsed * 0.22) % (list.length || 1);
                    targetText = list[dIdx] || '🚗 乘車賞景中';
                } else {
                    targetText = '🚶 沿途賞景漫步';
                }
            }

            if (av.avatarBtn && av._wasSpeaking !== isSpeaking) {
                av._wasSpeaking = isSpeaking;
                av.avatarBtn.classList.toggle('speaking', isSpeaking);
            }
            if (av.noteTextEl.textContent !== targetText) {
                av.noteTextEl.textContent = targetText;
            }
        }
    }

    // 建立 4 位家族角色頭頂的浮動位置指標 (Overhead Character Pins) - 畫面中純淨無多餘狀態列干擾
    function createCharacterOverheadMarkers(container) {
        charMarkers = {};
        const markerLayer = document.createElement('div');
        markerLayer.id = 'char-overhead-markers-layer';
        markerLayer.style.cssText = 'position:absolute;inset:0;pointer-events:none;z-index:22;overflow:hidden;';
        container.appendChild(markerLayer);

        // 注入頭頂名牌半透明與平時收折 CSS
        let markerStyle = document.getElementById('char-marker-css');
        if (!markerStyle) {
            markerStyle = document.createElement('style');
            markerStyle.id = 'char-marker-css';
            markerStyle.textContent = `
                .char-overhead-btn {
                    position:absolute;
                    transform:translate(-50%, -100%);
                    pointer-events:auto;
                    cursor:pointer;
                    display:flex;
                    flex-direction:column;
                    align-items:center;
                    transition:transform 0.18s cubic-bezier(0.16, 1, 0.3, 1);
                    background:transparent;
                    border:none;
                    padding:0;
                    touch-action:manipulation;
                }
                .char-pin-badge {
                    display:flex;
                    align-items:center;
                    gap:4px;
                    padding:3px 5px;
                    border-radius:9999px;
                    backdrop-filter:blur(6px);
                    -webkit-backdrop-filter:blur(6px);
                    box-shadow:0 2px 8px rgba(0,0,0,0.12);
                    transition:all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
                    line-height:1.2;
                }
                .char-pin-icon {
                    font-size:13px;
                    display:inline-flex;
                    align-items:center;
                    justify-content:center;
                    line-height:1;
                }
                .char-pin-text-block {
                    display:none;
                    align-items:center;
                    gap:3px;
                    white-space:nowrap;
                    font-size:10.5px;
                    font-weight:900;
                    animation: charPinExpand 0.16s ease-out;
                }
                /* hover 時 或 被鎖定時 (locked) 完整展開半透明精緻名牌 */
                .char-overhead-btn:hover .char-pin-badge,
                .char-overhead-btn.locked .char-pin-badge {
                    padding:3px 8px;
                    box-shadow:0 4px 14px rgba(0,0,0,0.22);
                    background-color:rgba(255, 255, 255, 0.92);
                }
                .char-overhead-btn:hover .char-pin-text-block,
                .char-overhead-btn.locked .char-pin-text-block {
                    display:inline-flex;
                }
                @keyframes charPinExpand {
                    from { opacity:0; transform:translateX(-4px); }
                    to { opacity:1; transform:none; }
                }
            `;
            document.head.appendChild(markerStyle);
        }

        Object.keys(ROLE_MARKER_STYLES).forEach(role => {
            const st = ROLE_MARKER_STYLES[role];
            const el = document.createElement('button');
            el.type = 'button';
            el.className = 'char-overhead-btn';
            el.dataset.role = role;

            el.innerHTML = `
                <div class="char-pin-badge" style="
                    background:${st.bg};
                    border:1.5px solid ${st.border};
                    color:${st.text};
                ">
                    <span class="char-pin-icon">${st.icon}</span>
                    <div class="char-pin-text-block">
                        <span>${st.title} ${st.name}</span>
                        <span class="mode-icon" style="font-size:9.5px;opacity:0.9;"></span>
                        <span class="lock-icon" style="display:none;font-size:9px;background:${st.border};color:#fff;padding:0 4px;border-radius:999px;">🔒跟隨中</span>
                    </div>
                </div>
                <div style="
                    width:0;height:0;
                    border-left:4px solid transparent;
                    border-right:4px solid transparent;
                    border-top:5px solid ${st.border};
                    margin-top:-1px;
                    opacity:0.85;
                "></div>
            `;

            // 快取 DOM 節點引用
            el._modeSpan = el.querySelector('.mode-icon');
            el._lockSpan = el.querySelector('.lock-icon');

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

    const _reusableMarkerPos = new THREE.Vector3();

    function updateCharacterMarkersPosition() {
        if (!camera || !renderer) return;
        const w = canvasW;
        const h = canvasH;
        if (!w || !h) return;

        // 為了避免 4 人距離太近時頭頂指標完全重疊，根據角色索引給予微幅水平錯開與高度階層
        const roleOffsets = {
            achun:   { dx: -24, dy: -8 },
            yijhang: { dx: 24,  dy: -8 },
            ayee:    { dx: -26, dy: -28 },
            alu:     { dx: 26,  dy: -28 }
        };

        const roles = Object.keys(charMarkers);
        for (let i = 0; i < roles.length; i++) {
            const role = roles[i];
            const el = charMarkers[role];
            const cg = characters[role];
            if (!el || !cg) continue;

            const modeSpan = el._modeSpan;
            if (modeSpan) {
                let targetMode = '';
                if (cg.userData.isAboard) {
                    targetMode = '🚗';
                } else if (!isStoppedAtLandmark && role === stragglerRole) {
                    if (role === 'achun') targetMode = '🛸💨';
                    else if (role === 'ayee') targetMode = '🧹💨';
                    else if (role === 'alu') targetMode = '🐉💨';
                    else targetMode = '🏃💨';
                }
                if (modeSpan.textContent !== targetMode) {
                    modeSpan.textContent = targetMode;
                }
            }

            cg.getWorldPosition(_reusableMarkerPos);
            _reusableMarkerPos.y += cg.userData.isAboard ? 0.90 : 1.05;
            _reusableMarkerPos.project(camera);

            // 視錐與相機前後平滑裁切（增加 0.02 滯後閾值，避免臨界點 display:none 與 flex 反覆頻繁震盪閃爍）
            const isCurrentlyHidden = (el.style.display === 'none');
            const shouldHide = isCurrentlyHidden ? (_reusableMarkerPos.z > 0.99) : (_reusableMarkerPos.z > 1.01);
            if (shouldHide) {
                if (!isCurrentlyHidden) el.style.display = 'none';
                continue;
            }
            if (isCurrentlyHidden) el.style.display = 'flex';

            const off = roleOffsets[role] || { dx: 0, dy: 0 };
            const x = (_reusableMarkerPos.x * 0.5 + 0.5) * w + off.dx;
            const y = (-(_reusableMarkerPos.y * 0.5) + 0.5) * h + off.dy;

            const clampedX = Math.round(Math.max(48, Math.min(w - 48, x)));
            const clampedY = Math.round(Math.max(44, Math.min(h - 16, y)));

            if (el._lastX !== clampedX || el._lastY !== clampedY) {
                el._lastX = clampedX;
                el._lastY = clampedY;
                el.style.left = `${clampedX}px`;
                el.style.top = `${clampedY}px`;
            }

            const isLocked = (lockedRole === role);
            if (el._wasLocked !== isLocked) {
                el._wasLocked = isLocked;
                el.classList.toggle('locked', isLocked);
                el.style.zIndex = isLocked ? '28' : '22';
                el.style.transform = isLocked ? 'translate(-50%, -100%) scale(1.14)' : 'translate(-50%, -100%) scale(1)';
            }
        }
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
            // 1. 更新畫面左上角大頭照 dock (IG 便條紙與鎖定光圈)
            const av = charAvatars[r];
            if (av) {
                const isLocked = (lockedRole === r);
                if (isLocked) {
                    av.avatarBtn.style.boxShadow = '0 0 0 3px #ef4444, 0 3px 10px rgba(239, 68, 68, 0.45)';
                    av.avatarBtn.style.transform = 'scale(1.08)';
                    av.lockBadge.style.display = 'inline-block';
                    av.noteBubble.style.borderColor = '#ef4444';
                    av.noteBubble.style.boxShadow = '0 3px 10px rgba(239, 68, 68, 0.25)';
                    av.noteTail.style.borderRightColor = '#ef4444';
                } else {
                    av.avatarBtn.style.boxShadow = '0 2px 6px rgba(0,0,0,0.10)';
                    av.avatarBtn.style.transform = 'scale(1)';
                    av.lockBadge.style.display = 'none';
                    av.noteBubble.style.borderColor = av.borderCol;
                    av.noteBubble.style.boxShadow = '0 2px 8px rgba(0,0,0,0.10)';
                    av.noteTail.style.borderRightColor = av.borderCol;
                }
            }

            // 2. 更新頭頂指標上的 🔒 標籤與 locked 類別
            const markerEl = charMarkers[r];
            if (markerEl) {
                markerEl.classList.toggle('locked', lockedRole === r);
                const lockSpan = markerEl._lockSpan || markerEl.querySelector('.lock-icon');
                if (lockSpan) {
                    lockSpan.style.display = (lockedRole === r) ? 'inline-block' : 'none';
                }
            }
            // 3. 更新下方角色按鈕鎖定狀態文字與外框高亮
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
            const randRole = pickRandomSpeaker(false);
            triggerCharacterSpeak(randRole, (info.dialogs && info.dialogs[randRole]) ? info.dialogs[randRole] : info.desc);
        }
    }

    let lastCheerTime = 0;
    function cheerEveryone() {
        const now = performance.now();
        if (now - lastCheerTime < 500) return; // 500ms 節流防抖，避免重複連擊造成並發堆疊卡頓
        lastCheerTime = now;

        const roles = ['achun', 'yijhang', 'ayee', 'alu'];
        // 全體跳躍歡呼
        roles.forEach((r, idx) => {
            setTimeout(() => {
                if (characters[r]) {
                    characters[r].userData.jumping = 1.0;
                    characters[r].userData.quirkType = 1 + (idx % 3);
                    characters[r].userData.quirkDuration = 2.6;
                    characters[r].userData.quirkMaxDur = 2.6;
                }
            }, idx * 90);
        });

        // 1. 車頂彩色煙火連續爆發！(零GC、零著色器重編譯)
        launchFireworksFromCar(5);

        // 2. 隨機指定一人大聲講出專屬歡呼台詞
        const luckyRole = roles[Math.floor(Math.random() * roles.length)];
        const pool = CHEER_QUOTES[luckyRole] || CHEER_QUOTES.achun;
        const quote = pool[Math.floor(Math.random() * pool.length)];

        // 延遲 180ms 配合煙火升空瞬間開口！
        setTimeout(() => {
            triggerCharacterSpeak(luckyRole, quote, true, false);
            const spotEl = document.getElementById('bubble-spot-tag');
            if (spotEl) spotEl.textContent = '🎆 全員大歡呼！';
        }, 180);
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
        canvasW = w || 800;
        canvasH = h || 520;
        camera.aspect = canvasW / canvasH;
        camera.updateProjectionMatrix();
        renderer.setSize(canvasW, canvasH);
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
        toggleSnow,
        debug: {
            getRouteProgress: () => routeProgress,
            getStopTimer: () => stopTimer,
            getStopElapsed: () => stopElapsed,
            getBoardElapsed: () => boardElapsed,
            isStopped: () => isStoppedAtLandmark,
            getCurrentLandmark: () => currentLandmark ? currentLandmark.id : null,
            getVisitedLandmarks: () => Array.from(visitedLandmarksInLap),
            getDriveCooldown: () => driveCooldown,
            getTravelMode: () => travelMode,
            getDialogBusyUntil: () => dialogBusyUntilMs,
            getPerformanceNow: () => performance.now(),
            getActiveSpeaker: () => activeSpeaker,
            getHasPlayedDepCall: () => hasPlayedSpotDepartureCall,
            getSpokenRoles: () => Array.from(spokenRolesInCurrentSpot)
        }
    };
})();
