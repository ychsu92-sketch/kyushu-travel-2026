/**
 * portal/props.js
 * 豐富動態物件與街景道具產生器 (P01 ~ P14，大幅擴充島嶼豐富度與放大模型比例)：
 * - P01: 8人座紅色冬季雪胎自駕小巴（含車頂行李架、黃藍行李箱、雪地頭燈、轉動車輪）
 * - P02: 熊本懷舊路面電車（雙色車身、車頂集電弓、溫暖車窗燈光，沿軌道往返）
 * - P03: 櫻島橫渡渡輪（雙層甲板、橘白煙囪、船尾浪花，往返鹿兒島港與櫻島港）
 * - P04: 屋台拉麵攤與燒鳥小吃店（紅燈籠、暖簾、吧台座椅、熱氣）
 * - P05: 溫泉街伴手禮木造商店（招財擺飾、木造招牌、門前雪人）
 * - P06: 九州三毛貓（翹尾巴、三角耳、散步搖尾）
 * - P07: 九州柴犬（捲尾巴、紅項圈、活潑小跑）
 * - P08: 冬季路人與旅人（穿大衣戴圍巾散步的九州居民與遊客）
 * - P09: 冬季覆雪杉木、銀杏樹與聖誕雪人組合
 * - P10: 日式木造町家聚落組（雙棟傳統瓦頂民家 + 圍牆 + 暖色窗光，填滿城鎮空白區）
 * - P11: 阿蘇草千里放牧赤牛與駿馬（低頭吃草搖尾的九州赤牛與小馬）
 * - P12: 日本街角自販機與紅色郵筒組（發光溫暖熱飲自動販賣機 + 復古圓柱郵筒 + 巴士站牌）
 * - P13: 薩摩/天草白色海角燈塔與彩色漁船（點綴海岸岬角與外海）
 * - P14: 球磨川朱紅拱橋與鐵道高架橋（橫跨人吉球磨川與山谷）
 */
(function () {
    window.KyushuIsland = window.KyushuIsland || {};

    function enableShadow(obj) {
        obj.traverse(child => {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
            }
        });
    }

    // P01: 第三代 Toyota Sienta 七人座休旅車 (Shikakumaru 方圓美學設計 + 雙側滑門防刮飾板 + 環形 Bi-Beam LED 頭燈 + 3排7座透視車艙與可開關側滑門)
    function buildP01_Minivan() {
        const g = new THREE.Group();

        // 材質定義：經典 Sienta 緋紅雙色塗裝 (Scarlet Metallic + 黑色懸浮車頂 + 霧黑 Shikakumaru 防刮護板)
        const bodyPaintMat = new THREE.MeshStandardMaterial({
            color: 0xc82829,
            roughness: 0.36,
            metalness: 0.15,
            flatShading: true
        });
        const roofBlackMat = new THREE.MeshLambertMaterial({ color: 0x1e293b, flatShading: true });
        const trimBlackMat = new THREE.MeshLambertMaterial({ color: 0x262626, flatShading: true });
        const glassMat = new THREE.MeshPhongMaterial({
            color: 0xdbeafe,
            specular: 0xffffff,
            shininess: 90,
            transparent: true,
            opacity: 0.34,
            side: THREE.DoubleSide
        });
        const seatMat      = new THREE.MeshLambertMaterial({ color: 0x475569 });
        const dashMat      = new THREE.MeshLambertMaterial({ color: 0x1e293b });
        const tireMat      = new THREE.MeshLambertMaterial({ color: 0x18181b });
        const rimMat       = new THREE.MeshLambertMaterial({ color: 0xd4d4d8 });
        const ledWhiteMat  = new THREE.MeshBasicMaterial({ color: 0xffffff });
        const fogAmberMat  = new THREE.MeshBasicMaterial({ color: 0xfde047 });
        const tailRedMat   = new THREE.MeshBasicMaterial({ color: 0xef4444 });
        const plateMat     = new THREE.MeshBasicMaterial({ color: 0xfef9c3 });

        // 1. 底盤與下護板 (Shikakumaru 圓角包覆感底盤)
        const chassis = new THREE.Mesh(new THREE.BoxGeometry(0.84, 0.14, 1.62), trimBlackMat);
        chassis.position.set(0, 0.18, 0);
        g.add(chassis);

        // 2. 車身下半部主體 (加寬加長以容納 7 人座與真實乘員)
        const lowerBody = new THREE.Mesh(new THREE.BoxGeometry(0.82, 0.32, 1.54), bodyPaintMat);
        lowerBody.position.set(0, 0.34, -0.02);
        g.add(lowerBody);

        // Sienta 招牌斜傾引擎蓋 (短車頭圓潤流線)
        const hood = new THREE.Mesh(new THREE.BoxGeometry(0.78, 0.22, 0.42), bodyPaintMat);
        hood.position.set(0, 0.42, 0.56);
        hood.rotation.x = 0.28;
        g.add(hood);

        // Sienta 招牌「微笑大嘴格柵 (Trapezoidal Grille)」與前後保桿
        const frontGrille = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.18, 0.06), trimBlackMat);
        frontGrille.position.set(0, 0.28, 0.77);
        const silverBadge = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.06, 0.07), rimMat);
        silverBadge.position.set(0, 0.36, 0.77);
        const plateFront = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.08, 0.07), plateMat);
        plateFront.position.set(0, 0.20, 0.77);
        const plateRear = plateFront.clone();
        plateRear.position.set(0, 0.24, -0.80);
        g.add(frontGrille, silverBadge, plateFront, plateRear);

        // Sienta 招牌「雙側防刮黑色拱形護板 (Side Protective Cladding)」與電動滑門軌道
        const sideCladL = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.16, 0.96), trimBlackMat);
        sideCladL.position.set(-0.41, 0.25, -0.02);
        const sideCladR = sideCladL.clone();
        sideCladR.position.x = 0.41;
        g.add(sideCladL, sideCladR);

        // 可開闔的左側電動滑門 (到站上下車時會向後滑開)
        const slidingDoorL = new THREE.Group();
        const doorPanel = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.28, 0.44), bodyPaintMat);
        doorPanel.position.set(0, 0.35, 0);
        const doorHandle = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.03, 0.09), trimBlackMat);
        doorHandle.position.set(-0.01, 0.42, 0.12);
        slidingDoorL.add(doorPanel, doorHandle);
        slidingDoorL.position.set(-0.41, 0, -0.02);
        g.add(slidingDoorL);

        // 3. 3 排 7 人座精緻內裝 (儀表板 + 方向盤 + 第一排雙座 + 第二排三座 + 第三排雙座)
        const interiorGroup = new THREE.Group();
        // 中控台與右駕方向盤 (日本右駕 RHD，位於 x = -0.18, z = 0.34)
        const dashboard = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.18, 0.20), dashMat);
        dashboard.position.set(0, 0.42, 0.38);
        const steerWheel = new THREE.Mesh(new THREE.TorusGeometry(0.075, 0.018, 6, 12), trimBlackMat);
        steerWheel.position.set(-0.18, 0.52, 0.28);
        steerWheel.rotation.x = -0.45;
        interiorGroup.add(dashboard, steerWheel);

        // 建立 3 排 7 人座座椅靠背與坐墊
        const seatRows = [
            { z: 0.14, xs: [-0.19, 0.19], w: 0.22 },         // 第一排：右駕駕駛座 (-0.19) + 左前副駕 (0.19)
            { z: -0.22, xs: [-0.21, 0, 0.21], w: 0.19 },     // 第二排：三人寬敞沙發座
            { z: -0.54, xs: [-0.18, 0.18], w: 0.20 }         // 第三排：雙人收折座 (7人座專屬)
        ];
        seatRows.forEach(row => {
            row.xs.forEach(sx => {
                const cushion = new THREE.Mesh(new THREE.BoxGeometry(row.w, 0.06, 0.20), seatMat);
                cushion.position.set(sx, 0.36, row.z);
                const backrest = new THREE.Mesh(new THREE.BoxGeometry(row.w, 0.22, 0.06), seatMat);
                backrest.position.set(sx, 0.48, row.z - 0.08);
                backrest.rotation.x = -0.12;
                interiorGroup.add(cushion, backrest);
            });
        });
        g.add(interiorGroup);

        // 4. 高頂挑高透明玻璃座艙 + A/B/C/D 柱 + 懸浮式雙色黑車頂
        const glassCabin = new THREE.Mesh(new THREE.BoxGeometry(0.76, 0.32, 1.24), glassMat);
        glassCabin.position.set(0, 0.64, -0.10);
        g.add(glassCabin);

        // 黑色車窗立柱 (營造懸浮車頂感)
        [[-0.38, 0.42], [0.38, 0.42], [-0.38, -0.05], [0.38, -0.05], [-0.38, -0.68], [0.38, -0.68]].forEach(p => {
            const pillar = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.34, 0.05), roofBlackMat);
            pillar.position.set(p[0], 0.64, p[1]);
            g.add(pillar);
        });

        // 圓潤挑高車頂與車側導流凹槽
        const roof = new THREE.Mesh(new THREE.BoxGeometry(0.78, 0.07, 1.28), bodyPaintMat);
        roof.position.set(0, 0.82, -0.10);
        const roofSpoiler = new THREE.Mesh(new THREE.BoxGeometry(0.74, 0.05, 0.14), bodyPaintMat);
        roofSpoiler.position.set(0, 0.83, -0.72);
        g.add(roof, roofSpoiler);

        // 後視鏡
        const mirrorL = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.07, 0.06), roofBlackMat);
        mirrorL.position.set(-0.44, 0.52, 0.34);
        const mirrorR = mirrorL.clone();
        mirrorR.position.x = 0.44;
        g.add(mirrorL, mirrorR);

        // 5. Sienta 招牌圓角環形 Bi-Beam LED 頭燈 + 黃金雪地霧燈 + 直立式雙側尾燈
        [-0.27, 0.27].forEach(hx => {
            const headHousing = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.10, 0.06), roofBlackMat);
            headHousing.position.set(hx, 0.42, 0.74);
            const ledLamp = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.07, 0.07), ledWhiteMat);
            ledLamp.position.set(hx, 0.42, 0.75);
            const fogLamp = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.06, 8), fogAmberMat);
            fogLamp.rotation.x = Math.PI / 2;
            fogLamp.position.set(hx, 0.22, 0.76);
            // 車尾直立式 LED 導光尾燈組
            const tailLamp = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.26, 0.05), tailRedMat);
            tailLamp.position.set(hx * 1.25, 0.58, -0.74);
            g.add(headHousing, ledLamp, fogLamp, tailLamp);
        });

        // 6. 冬季自駕車頂橫桿與雙色行李箱 (稍微退至第 3 排上方，不遮擋第 1、2 排乘員頭頂視線)
        const rackBar1 = new THREE.Mesh(new THREE.BoxGeometry(0.76, 0.03, 0.05), trimBlackMat);
        rackBar1.position.set(0, 0.87, -0.25);
        const rackBar2 = rackBar1.clone();
        rackBar2.position.z = -0.58;
        const roofBox = new THREE.Mesh(
            new THREE.BoxGeometry(0.32, 0.13, 0.52),
            new THREE.MeshLambertMaterial({ color: 0xf8fafc })
        );
        roofBox.position.set(0.14, 0.94, -0.42);
        const skiBag = new THREE.Mesh(
            new THREE.BoxGeometry(0.22, 0.11, 0.46),
            new THREE.MeshLambertMaterial({ color: 0xf59e0b })
        );
        skiBag.position.set(-0.16, 0.93, -0.42);
        g.add(rackBar1, rackBar2, roofBox, skiBag);

        // 7. 4 顆冬季雙色切削鋁圈雪胎 (含輪圈蓋細節)
        const wheels = [];
        const tireGeo = new THREE.CylinderGeometry(0.155, 0.155, 0.11, 14);
        tireGeo.rotateZ(Math.PI / 2);
        const rimGeo = new THREE.CylinderGeometry(0.095, 0.095, 0.12, 8);
        rimGeo.rotateZ(Math.PI / 2);

        [[-0.41, 0.155, 0.46], [0.41, 0.155, 0.46], [-0.41, 0.155, -0.48], [0.41, 0.155, -0.48]].forEach(pos => {
            const wg = new THREE.Group();
            const tire = new THREE.Mesh(tireGeo, tireMat);
            const rim = new THREE.Mesh(rimGeo, rimMat);
            wg.add(tire, rim);
            wg.position.set(pos[0], pos[1], pos[2]);
            g.add(wg);
            wheels.push(wg);
        });

        g.userData.wheels = wheels;
        g.userData.slidingDoorL = slidingDoorL;

        enableShadow(g);
        return g;
    }

    // P02: 熊本懷舊路面電車 (市電)
    function buildP02_KumamotoTram() {
        const g = new THREE.Group();
        const creamMat = new THREE.MeshLambertMaterial({ color: 0xfef3c7 });
        const greenMat = new THREE.MeshLambertMaterial({ color: 0x15803d });
        const winMat   = new THREE.MeshBasicMaterial({ color: 0xbae6fd });
        const darkMat  = new THREE.MeshLambertMaterial({ color: 0x334155 });

        const lower = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.24, 1.15), greenMat);
        lower.position.y = 0.18;
        const upper = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.26, 1.12), creamMat);
        upper.position.y = 0.42;
        const win = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.16, 0.96), winMat);
        win.position.y = 0.42;
        const roof = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.06, 1.05), darkMat);
        roof.position.y = 0.58;

        const panto = new THREE.Mesh(new THREE.OctahedronGeometry(0.12, 0), darkMat);
        panto.scale.set(0.6, 1.0, 1.2);
        panto.position.y = 0.68;

        g.add(lower, upper, win, roof, panto);
        enableShadow(g);
        return g;
    }

    // P03: 櫻島橫渡渡輪 (Sakurajima Ferry)
    function buildP03_SakurajimaFerry() {
        const g = new THREE.Group();
        const hullWhite = new THREE.MeshLambertMaterial({ color: 0xf8fafc, flatShading: true });
        const hullBlue  = new THREE.MeshLambertMaterial({ color: 0x0284c7 });
        const deckMat   = new THREE.MeshLambertMaterial({ color: 0xe2e8f0 });
        const funnelMat = new THREE.MeshLambertMaterial({ color: 0xf97316 });
        const winMat    = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });

        const hullBottom = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.16, 1.25), hullBlue);
        hullBottom.position.y = 0.08;
        const hullMain = new THREE.Mesh(new THREE.BoxGeometry(0.60, 0.18, 1.18), hullWhite);
        hullMain.position.y = 0.25;
        const cabin = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.18, 0.78), deckMat);
        cabin.position.set(0, 0.42, -0.05);
        const bridge = new THREE.Mesh(new THREE.BoxGeometry(0.50, 0.10, 0.68), winMat);
        bridge.position.set(0, 0.43, -0.05);
        const funnel = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.10, 0.22, 8), funnelMat);
        funnel.position.set(0, 0.58, -0.22);

        g.add(hullBottom, hullMain, cabin, bridge, funnel);
        enableShadow(g);
        return g;
    }

    // P04: 九州屋台拉麵攤 (木造推車 + 紅燈籠 + 暖簾)
    function buildP04_RamenYatai() {
        const g = new THREE.Group();
        const woodMat = new THREE.MeshLambertMaterial({ color: 0xb45309 });
        const roofMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
        const redMat  = new THREE.MeshBasicMaterial({ color: 0xef4444 });
        const norenMat= new THREE.MeshLambertMaterial({ color: 0x991b1b });

        const counter = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.24, 0.36), woodMat);
        counter.position.y = 0.12;
        const roof = new THREE.Mesh(new THREE.ConeGeometry(0.44, 0.20, 4), roofMat);
        roof.rotation.y = Math.PI / 4;
        roof.position.y = 0.52;
        const noren = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.14, 0.04), norenMat);
        noren.position.set(0, 0.35, 0.18);

        [-0.20, 0.20].forEach(x => {
            const lantern = new THREE.Mesh(new THREE.SphereGeometry(0.06, 8, 8), redMat);
            lantern.scale.y = 1.3;
            lantern.position.set(x, 0.32, 0.22);
            g.add(lantern);
        });

        g.add(counter, roof, noren);
        enableShadow(g);
        return g;
    }

    // P05: 溫泉街伴手禮木造商店
    function buildP05_OnsenShop() {
        const g = new THREE.Group();
        const wallMat = new THREE.MeshLambertMaterial({ color: 0xfef3c7 });
        const woodMat = new THREE.MeshLambertMaterial({ color: 0x451a03 });
        const roofMat = new THREE.MeshLambertMaterial({ color: 0x334155, flatShading: true });
        const signMat = new THREE.MeshLambertMaterial({ color: 0xf59e0b });

        const box = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.38, 0.44), wallMat);
        box.position.y = 0.19;
        const trim = new THREE.Mesh(new THREE.BoxGeometry(0.60, 0.09, 0.46), woodMat);
        trim.position.y = 0.35;
        const roof = new THREE.Mesh(new THREE.ConeGeometry(0.50, 0.24, 4), roofMat);
        roof.rotation.y = Math.PI / 4;
        roof.position.y = 0.48;
        const sign = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.11, 0.04), signMat);
        sign.position.set(0, 0.33, 0.24);

        g.add(box, trim, roof, sign);
        enableShadow(g);
        return g;
    }

    // P06: 九州三毛貓 (Calico Cat)
    function buildP06_CalicoCat() {
        const g = new THREE.Group();
        const whiteMat  = new THREE.MeshLambertMaterial({ color: 0xfffbeb });
        const orangeMat = new THREE.MeshLambertMaterial({ color: 0xf97316 });
        const darkMat   = new THREE.MeshLambertMaterial({ color: 0x292524 });

        const body = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.14, 0.26), whiteMat);
        body.position.y = 0.12;
        const patch = new THREE.Mesh(new THREE.BoxGeometry(0.165, 0.09, 0.11), orangeMat);
        patch.position.set(0, 0.14, -0.02);
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.105, 10, 10), whiteMat);
        head.position.set(0, 0.22, 0.13);

        const earL = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.08, 4), orangeMat);
        earL.position.set(-0.055, 0.31, 0.13);
        const earR = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.08, 4), darkMat);
        earR.position.set(0.055, 0.31, 0.13);

        const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.024, 0.18, 6), orangeMat);
        tail.position.set(0, 0.22, -0.14);
        tail.rotation.x = -0.5;

        g.add(body, patch, head, earL, earR, tail);
        g.userData.tail = tail;
        enableShadow(g);
        return g;
    }

    // P07: 九州柴犬 (Shiba Inu)
    function buildP07_ShibaDog() {
        const g = new THREE.Group();
        const shibaMat  = new THREE.MeshLambertMaterial({ color: 0xd97706 });
        const creamMat  = new THREE.MeshLambertMaterial({ color: 0xfef3c7 });
        const collarMat = new THREE.MeshLambertMaterial({ color: 0xdc2626 });

        const body = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.16, 0.30), shibaMat);
        body.position.y = 0.15;
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.115, 10, 10), shibaMat);
        head.position.set(0, 0.26, 0.15);
        const snout = new THREE.Mesh(new THREE.SphereGeometry(0.06, 8, 8), creamMat);
        snout.position.set(0, 0.24, 0.24);
        const collar = new THREE.Mesh(new THREE.TorusGeometry(0.085, 0.022, 6, 10), collarMat);
        collar.rotation.x = Math.PI / 2;
        collar.position.set(0, 0.20, 0.12);

        const earL = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.085, 4), shibaMat);
        earL.position.set(-0.065, 0.35, 0.14);
        const earR = earL.clone();
        earR.position.set(0.065, 0.35, 0.14);

        const tail = new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.022, 6, 8, Math.PI * 1.3), shibaMat);
        tail.position.set(0, 0.25, -0.15);
        tail.rotation.y = Math.PI / 2;

        g.add(body, head, snout, collar, earL, earR, tail);
        g.userData.tail = tail;
        enableShadow(g);
        return g;
    }

    // P08: 九州冬季路人/旅人
    function buildP08_Pedestrian(coatColor) {
        const g = new THREE.Group();
        const skinMat = new THREE.MeshLambertMaterial({ color: 0xffe4c4 });
        const coatMat = new THREE.MeshLambertMaterial({ color: coatColor || 0x0d9488, flatShading: true });
        const hatMat  = new THREE.MeshLambertMaterial({ color: 0xe11d48 });

        const body = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.15, 0.34, 8), coatMat);
        body.position.y = 0.21;
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.13, 10, 10), skinMat);
        head.position.y = 0.46;
        const hat = new THREE.Mesh(new THREE.SphereGeometry(0.135, 10, 8, 0, Math.PI * 2, 0, Math.PI * 0.55), hatMat);
        hat.position.y = 0.49;

        g.add(body, head, hat);
        enableShadow(g);
        return g;
    }

    // P09: 冬季覆雪杉木、金黃銀杏樹與聖誕雪人組合
    function buildP09_WinterPineAndSnowman(variant) {
        const g = new THREE.Group();
        const trunkMat = new THREE.MeshLambertMaterial({ color: 0x5c3a21 });
        const isGinkgo = (variant === 'ginkgo');
        const pineMat  = new THREE.MeshLambertMaterial({
            color: isGinkgo ? 0xeab308 : 0x2d5a27,
            flatShading: true
        });
        const snowMat  = new THREE.MeshLambertMaterial({ color: 0xf8fafc, flatShading: true });
        const carrotMat= new THREE.MeshLambertMaterial({ color: 0xf97316 });

        const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 0.32, 6), trunkMat);
        trunk.position.y = 0.16;
        const foliage1 = new THREE.Mesh(new THREE.ConeGeometry(0.32, 0.46, 7), pineMat);
        foliage1.position.y = 0.42;
        const foliage2 = new THREE.Mesh(new THREE.ConeGeometry(0.25, 0.38, 7), pineMat);
        foliage2.position.y = 0.66;
        g.add(trunk, foliage1, foliage2);

        if (!isGinkgo) {
            const snowCap = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.24, 7), snowMat);
            snowCap.position.y = 0.78;
            g.add(snowCap);
        }

        if (variant !== 'tree_only') {
            const smBottom = new THREE.Mesh(new THREE.SphereGeometry(0.14, 10, 10), snowMat);
            smBottom.position.set(0.34, 0.13, 0.12);
            const smTop = new THREE.Mesh(new THREE.SphereGeometry(0.10, 10, 10), snowMat);
            smTop.position.set(0.34, 0.31, 0.12);
            const nose = new THREE.Mesh(new THREE.ConeGeometry(0.022, 0.09, 6), carrotMat);
            nose.rotation.x = Math.PI / 2;
            nose.position.set(0.34, 0.31, 0.22);
            g.add(smBottom, smTop, nose);
        }

        enableShadow(g);
        return g;
    }

    // P10: 日式木造町家聚落組 (填補城鎮與鄉村空白，含暖黃色窗戶燈光)
    function buildP10_MachiyaVillage() {
        const g = new THREE.Group();
        const wallMat1 = new THREE.MeshLambertMaterial({ color: 0xfef9c3 });
        const wallMat2 = new THREE.MeshLambertMaterial({ color: 0xfafaf9 });
        const roofMat1 = new THREE.MeshLambertMaterial({ color: 0x334155, flatShading: true });
        const roofMat2 = new THREE.MeshLambertMaterial({ color: 0x7c2d12, flatShading: true });
        const winGlow  = new THREE.MeshBasicMaterial({ color: 0xfde047 });

        // 主屋
        const h1 = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.32, 0.36), wallMat1);
        h1.position.set(-0.20, 0.16, 0);
        const r1 = new THREE.Mesh(new THREE.ConeGeometry(0.38, 0.20, 4), roofMat1);
        r1.rotation.y = Math.PI / 4;
        r1.position.set(-0.20, 0.42, 0);
        const w1 = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.10, 0.38), winGlow);
        w1.position.set(-0.20, 0.18, 0);

        // 側屋
        const h2 = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.26, 0.32), wallMat2);
        h2.position.set(0.24, 0.13, 0.10);
        const r2 = new THREE.Mesh(new THREE.ConeGeometry(0.30, 0.18, 4), roofMat2);
        r2.rotation.y = Math.PI / 4;
        r2.position.set(0.24, 0.34, 0.10);

        g.add(h1, r1, w1, h2, r2);
        enableShadow(g);
        return g;
    }

    // P11: 阿蘇草千里放牧赤牛與駿馬組 (Akaushi Cattle & Horse)
    function buildP11_AsoCattle() {
        const g = new THREE.Group();
        const akaushiMat = new THREE.MeshLambertMaterial({ color: 0xb45309, flatShading: true }); // 阿蘇褐毛和牛 (赤牛)
        const hornMat    = new THREE.MeshLambertMaterial({ color: 0xfef3c7 });
        const darkMat    = new THREE.MeshLambertMaterial({ color: 0x292524 });

        const body = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.18, 0.36), akaushiMat);
        body.position.y = 0.18;
        const head = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.14, 0.18), akaushiMat);
        head.position.set(0, 0.24, 0.22);
        const hornL = new THREE.Mesh(new THREE.ConeGeometry(0.025, 0.08, 5), hornMat);
        hornL.position.set(-0.08, 0.33, 0.22);
        hornL.rotation.z = 0.4;
        const hornR = hornL.clone();
        hornR.position.set(0.08, 0.33, 0.22);
        hornR.rotation.z = -0.4;

        [[-0.07, 0.08, 0.12], [0.07, 0.08, 0.12], [-0.07, 0.08, -0.12], [0.07, 0.08, -0.12]].forEach(p => {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.025, 0.16, 6), darkMat);
            leg.position.set(p[0], p[1], p[2]);
            g.add(leg);
        });

        g.add(body, head, hornL, hornR);
        g.userData.head = head;
        enableShadow(g);
        return g;
    }

    // P12: 日本街角自販機、復古紅郵筒與巴士站牌組
    function buildP12_VendingAndPostbox() {
        const g = new THREE.Group();
        const vendBlue = new THREE.MeshLambertMaterial({ color: 0x0284c7 });
        const vendRed  = new THREE.MeshLambertMaterial({ color: 0xdc2626 });
        const display  = new THREE.MeshBasicMaterial({ color: 0xfef9c3 });

        // 兩台並排日本自動販賣機
        const v1 = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.34, 0.14), vendBlue);
        v1.position.set(-0.12, 0.17, 0);
        const d1 = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.18, 0.02), display);
        d1.position.set(-0.12, 0.21, 0.07);

        const v2 = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.34, 0.14), vendRed);
        v2.position.set(0.12, 0.17, 0);
        const d2 = d1.clone();
        d2.position.set(0.12, 0.21, 0.07);

        // 復古圓柱紅郵筒
        const post = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.26, 10), vendRed);
        post.position.set(0.32, 0.13, 0.04);
        const cap = new THREE.Mesh(new THREE.SphereGeometry(0.065, 10, 8), vendRed);
        cap.position.set(0.32, 0.26, 0.04);

        g.add(v1, d1, v2, d2, post, cap);
        enableShadow(g);
        return g;
    }

    // P13: 海岸白色燈塔與漁船組 (點綴半島岬角與天草海面)
    function buildP13_Lighthouse() {
        const g = new THREE.Group();
        const whiteMat = new THREE.MeshLambertMaterial({ color: 0xf8fafc });
        const redMat   = new THREE.MeshLambertMaterial({ color: 0xdc2626 });
        const beamMat  = new THREE.MeshBasicMaterial({ color: 0xfef08a });

        const tower = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.15, 0.62, 10), whiteMat);
        tower.position.y = 0.31;
        const lantern = new THREE.Mesh(new THREE.CylinderGeometry(0.10, 0.10, 0.12, 10), beamMat);
        lantern.position.y = 0.66;
        const roof = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.12, 10), redMat);
        roof.position.y = 0.76;

        g.add(tower, lantern, roof);
        enableShadow(g);
        return g;
    }

    // P14: 朱紅溪谷拱橋 (橫跨球磨川/大淀川)
    function buildP14_RedArchBridge() {
        const g = new THREE.Group();
        const redMat  = new THREE.MeshLambertMaterial({ color: 0xdc2626, flatShading: true });
        const deckMat = new THREE.MeshLambertMaterial({ color: 0x78350f });

        const arch = new THREE.Mesh(new THREE.TorusGeometry(0.38, 0.045, 6, 14, Math.PI), redMat);
        arch.position.y = 0.02;
        const deck = new THREE.Mesh(new THREE.BoxGeometry(0.84, 0.05, 0.24), deckMat);
        deck.position.y = 0.36;
        const railF = new THREE.Mesh(new THREE.BoxGeometry(0.84, 0.09, 0.03), redMat);
        railF.position.set(0, 0.42, 0.11);
        const railB = railF.clone();
        railB.position.set(0, 0.42, -0.11);

        g.add(arch, deck, railF, railB);
        enableShadow(g);
        return g;
    }


    // P15: 公路沿線朱紅鳥居 (神道入口與山道守護)
    function buildP15_RoadsideTorii() {
        const g = new THREE.Group();
        const vermilionMat = new THREE.MeshLambertMaterial({ color: 0xd9381e });
        const blackMat = new THREE.MeshLambertMaterial({ color: 0x1f2937 });
        const stoneMat = new THREE.MeshLambertMaterial({ color: 0x9ca3af });

        // 基石石台 (柱座)
        const baseL = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 0.06, 8), stoneMat);
        baseL.position.set(-0.28, 0.03, 0);
        const baseR = baseL.clone();
        baseR.position.x = 0.28;

        // 兩根本柱 (Hashira)
        const colGeom = new THREE.CylinderGeometry(0.042, 0.046, 0.62, 8);
        const colL = new THREE.Mesh(colGeom, vermilionMat);
        colL.position.set(-0.28, 0.34, 0);
        colL.rotation.z = -0.03;
        const colR = new THREE.Mesh(colGeom, vermilionMat);
        colR.position.set(0.28, 0.34, 0);
        colR.rotation.z = 0.03;

        // 貫 (Nuki 下層橫木)
        const nuki = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.045, 0.045), vermilionMat);
        nuki.position.set(0, 0.50, 0);

        // 笠木與島木 (Kasagi 上層頂橫木 + 黑色屋頂護蓋)
        const shimaki = new THREE.Mesh(new THREE.BoxGeometry(0.82, 0.05, 0.065), vermilionMat);
        shimaki.position.set(0, 0.62, 0);
        const kasagiCap = new THREE.Mesh(new THREE.BoxGeometry(0.86, 0.03, 0.08), blackMat);
        kasagiCap.position.set(0, 0.65, 0);

        // 額束 (Gakuzuka 中央匾額)
        const gaku = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.09, 0.055), blackMat);
        gaku.position.set(0, 0.56, 0);

        g.add(baseL, baseR, colL, colR, nuki, shimaki, kasagiCap, gaku);
        enableShadow(g);
        return g;
    }

    // P16: 九州懷舊鄉間巴士站 (候車亭 + 圓形巴士站牌 + 木長椅)
    function buildP16_BusStop() {
        const g = new THREE.Group();
        const woodMat = new THREE.MeshLambertMaterial({ color: 0x854d0e });
        const benchMat = new THREE.MeshLambertMaterial({ color: 0xa16207 });
        const roofMat = new THREE.MeshLambertMaterial({ color: 0x334155 });
        const poleMat = new THREE.MeshLambertMaterial({ color: 0xd1d5db });
        const signMat = new THREE.MeshBasicMaterial({ color: 0xfef08a });
        const textMat = new THREE.MeshBasicMaterial({ color: 0x1e293b });

        // 木造候車棚骨架
        const postGeom = new THREE.BoxGeometry(0.03, 0.44, 0.03);
        const p1 = new THREE.Mesh(postGeom, woodMat); p1.position.set(-0.20, 0.22, -0.12);
        const p2 = new THREE.Mesh(postGeom, woodMat); p2.position.set(0.20, 0.22, -0.12);
        const p3 = new THREE.Mesh(postGeom, woodMat); p3.position.set(-0.20, 0.24, 0.12);
        const p4 = new THREE.Mesh(postGeom, woodMat); p4.position.set(0.20, 0.24, 0.12);

        // 斜頂遮雨棚
        const roof = new THREE.Mesh(new THREE.BoxGeometry(0.50, 0.025, 0.34), roofMat);
        roof.position.set(0, 0.44, 0);
        roof.rotation.x = 0.12;

        // 候車小木椅
        const bench = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.04, 0.12), benchMat);
        bench.position.set(0, 0.14, -0.06);
        const leg1 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.12, 0.10), woodMat);
        leg1.position.set(-0.14, 0.06, -0.06);
        const leg2 = leg1.clone(); leg2.position.x = 0.14;

        // 圓形巴士站牌
        const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.48, 8), poleMat);
        pole.position.set(0.32, 0.24, 0.06);
        const roundSign = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.02, 16), signMat);
        roundSign.rotation.x = Math.PI / 2;
        roundSign.position.set(0.32, 0.46, 0.06);
        const innerDot = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.025, 12), textMat);
        innerDot.rotation.x = Math.PI / 2;
        innerDot.position.set(0.32, 0.46, 0.06);

        g.add(p1, p2, p3, p4, roof, bench, leg1, leg2, pole, roundSign, innerDot);
        enableShadow(g);
        return g;
    }

    // P17: 日式石燈籠與地藏小祠 (公路沿線與古道守護)
    function buildP17_StoneLantern() {
        const g = new THREE.Group();
        const stoneMat = new THREE.MeshLambertMaterial({ color: 0x9ca3af });
        const lightMat = new THREE.MeshBasicMaterial({ color: 0xfef08a });

        // 基座
        const base = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.08, 0.24), stoneMat);
        base.position.y = 0.04;
        // 竿 (柱身)
        const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.06, 0.26, 8), stoneMat);
        pillar.position.y = 0.21;
        // 中台
        const midBase = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.05, 0.20), stoneMat);
        midBase.position.y = 0.36;
        // 火袋
        const fireBox = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.12, 0.14), lightMat);
        fireBox.position.y = 0.44;
        // 笠
        const roof = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.10, 6), stoneMat);
        roof.position.y = 0.55;
        // 寶珠
        const jewel = new THREE.Mesh(new THREE.SphereGeometry(0.035, 8, 8), stoneMat);
        jewel.position.y = 0.62;

        // 小地藏石碑
        const jizo = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.055, 0.18, 8), stoneMat);
        jizo.position.set(0.22, 0.09, 0.04);
        const jizoBib = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.04, 0.04), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
        jizoBib.position.set(0.22, 0.12, 0.06);

        g.add(base, pillar, midBase, fireBox, roof, jewel, jizo, jizoBib);
        enableShadow(g);
        return g;
    }

    // P18: 宮崎/日南沿海白色風力發電機 (旋轉風葉 + 錐形高塔)
    function buildP18_WindTurbine() {
        const g = new THREE.Group();
        const whiteMat = new THREE.MeshLambertMaterial({ color: 0xf8fafc });
        const grayMat  = new THREE.MeshLambertMaterial({ color: 0x94a3b8 });
        const redTipMat= new THREE.MeshBasicMaterial({ color: 0xef4444 });

        // 錐形高塔
        const tower = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.075, 1.35, 12), whiteMat);
        tower.position.y = 0.675;
        g.add(tower);

        // 機艙箱
        const nacelle = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.08, 0.22), whiteMat);
        nacelle.position.set(0, 1.35, 0.02);
        g.add(nacelle);

        // 旋轉葉片組
        const rotorGroup = new THREE.Group();
        rotorGroup.position.set(0, 1.35, 0.14);

        // 輪轂
        const hub = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.08, 12), grayMat);
        hub.rotation.x = Math.PI / 2;
        rotorGroup.add(hub);

        // 3 支風葉
        for (let i = 0; i < 3; i++) {
            const bGroup = new THREE.Group();
            bGroup.rotation.z = (i * Math.PI * 2) / 3;

            const blade = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.46, 0.012), whiteMat);
            blade.position.y = 0.23;

            const redTip = new THREE.Mesh(new THREE.BoxGeometry(0.034, 0.08, 0.014), redTipMat);
            redTip.position.y = 0.42;

            bGroup.add(blade, redTip);
            rotorGroup.add(bGroup);
        }

        g.add(rotorGroup);
        g.userData.rotorGroup = rotorGroup;
        enableShadow(g);
        return g;
    }

    // P19: 鹿兒島灣/日向灘彩色漁船 (停泊外海輕微搖晃)
    function buildP19_SmallFishingBoat(color) {
        const g = new THREE.Group();
        const hullMat = new THREE.MeshLambertMaterial({ color: color || 0x2563eb });
        const whiteMat = new THREE.MeshLambertMaterial({ color: 0xffffff });

        // 船身
        const hull = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.10, 0.52), hullMat);
        hull.position.y = 0.05;
        const bow = new THREE.Mesh(new THREE.ConeGeometry(0.14, 0.18, 4), hullMat);
        bow.rotation.y = Math.PI / 4;
        bow.rotation.x = Math.PI / 2;
        bow.position.set(0, 0.05, 0.32);

        // 甲板與船艙
        const cabin = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.12, 0.18), whiteMat);
        cabin.position.set(0, 0.14, -0.06);
        const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.28, 6), whiteMat);
        mast.position.set(0, 0.24, 0.08);

        g.add(hull, bow, cabin, mast);
        enableShadow(g);
        return g;
    }

    // P20: 九州國道公路里程指示牌 (綠底白字看板 + 雙金屬立柱)
    function buildP20_RoadMileageSign() {
        const g = new THREE.Group();
        const signMat  = new THREE.MeshLambertMaterial({ color: 0x15803d });
        const borderMat= new THREE.MeshBasicMaterial({ color: 0xffffff });
        const poleMat  = new THREE.MeshLambertMaterial({ color: 0x64748b });

        // 雙金屬立柱
        const poleL = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.44, 8), poleMat);
        poleL.position.set(-0.16, 0.22, 0);
        const poleR = poleL.clone();
        poleR.position.x = 0.16;

        // 指示牌面
        const sign = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.22, 0.025), signMat);
        sign.position.set(0, 0.35, 0);
        const border = new THREE.Mesh(new THREE.BoxGeometry(0.40, 0.20, 0.028), borderMat);
        border.position.set(0, 0.35, 0);
        const inner = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.18, 0.03), signMat);
        inner.position.set(0, 0.35, 0);

        // 白色路線代號標記條
        const mark = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.05, 0.034), borderMat);
        mark.position.set(0, 0.35, 0);

        g.add(poleL, poleR, sign, border, inner, mark);
        enableShadow(g);
        return g;
    }

    const PROP_SPECS = [
        { code: 'P01', name: 'Toyota Sienta 七人座冬季自駕休旅', badge: '🚗 主力座駕', desc: '第三代 Shikakumaru 方圓美學設計、雙側電動滑門、3排7座透視車艙與雪胎，載著全家人環遊南九州！', build: buildP01_Minivan },
        { code: 'P02', name: '熊本懷舊路面電車 (市電)', badge: '🚋 城市鐵道', desc: '行駛於熊本城、辛島町與水前寺成趣園之間的經典綠白雙色路面電車。', build: buildP02_KumamotoTram },
        { code: 'P03', name: '櫻島橫渡渡輪', badge: '🚢 錦江灣航線', desc: '24 小時往返鹿兒島本港與櫻島港，連人帶車橫越錦江灣的招牌藍色渡輪。', build: buildP03_SakurajimaFerry },
        { code: 'P04', name: '九州屋台拉麵攤', badge: '🍜 街頭美食', desc: '掛著紅燈籠與暖簾的熊本/鹿兒島街頭屋台，飄著豚骨拉麵與關東煮香氣。', build: buildP04_RamenYatai },
        { code: 'P05', name: '溫泉街伴手禮木造商店', badge: '🛍️ 商店街舖', desc: '黑川溫泉與城彩苑常見的日式木造町家商店，阿姨最愛駐足採買。', build: buildP05_OnsenShop },
        { code: 'P06', name: '九州三毛貓', badge: '🐱 街角萌寵', desc: '在溫泉街與神社石階旁悠閒晃尾巴散步的可愛三花貓。', build: buildP06_CalicoCat },
        { code: 'P07', name: '九州柴犬', badge: '🐕 忠實小狗', desc: '戴著紅色項圈、捲著尾巴在公園與商店街小跑的活潑柴犬。', build: buildP07_ShibaDog },
        { code: 'P08', name: '冬季路人與旅人', badge: '🚶 街景行人', desc: '穿著冬日大衣與毛帽，在各大景點周邊散步拍照的九州居民與遊客。', build: () => buildP08_Pedestrian(0x0d9488) },
        { code: 'P09', name: '冬季覆雪杉木與聖誕雪人', badge: '⛄ 冬季自然', desc: '點綴在阿蘇、霧島與黑川山區的覆雪針葉林、銀杏樹與聖誕小雪人。', build: buildP09_WinterPineAndSnowman },
        { code: 'P10', name: '日式木造町家聚落組', badge: '🏘️ 城鎮民家', desc: '點亮溫暖窗光的雙棟傳統日式瓦頂町家，豐富熊本、人吉與鹿兒島街區。', build: buildP10_MachiyaVillage },
        { code: 'P11', name: '阿蘇放牧赤牛', badge: '🐄 草原牧場', desc: '在阿蘇草千里與牛奶之路草原上悠閒低頭吃草的九州褐毛和牛（赤牛）。', build: buildP11_AsoCattle },
        { code: 'P12', name: '日本街角自販機與紅郵筒', badge: '📮 街角風景', desc: '日本街頭最具代表性的冷熱飲發光自動販賣機與復古圓柱紅郵筒。', build: buildP12_VendingAndPostbox },
        { code: 'P13', name: '薩摩海角白色燈塔', badge: '🗼 海岸地標', desc: '佇立於薩摩半島長崎鼻、大隅佐多岬與天草海岸的白色守望燈塔。', build: buildP13_Lighthouse },
        { code: 'P14', name: '朱紅溪谷拱橋', badge: '🌉 河川名橋', desc: '橫跨球磨川、五瀨川與大淀川的日式朱紅拱橋。', build: buildP14_RedArchBridge },
        { code: 'P15', name: '公路沿線朱紅鳥居', badge: '⛩️ 神道地標', desc: '佇立於公路邊、通往山林古社的朱紅神道鳥居。', build: buildP15_RoadsideTorii },
        { code: 'P16', name: '九州懷舊鄉間巴士站', badge: '🚏 鄉村站牌', desc: '木造遮雨棚、圓形站牌與長椅的經典日式鄉村巴士候車亭。', build: buildP16_BusStop },
        { code: 'P17', name: '日式石燈籠與地藏小祠', badge: '🏮 古道守護', desc: '點綴在公路與溫泉古道的暖光石燈籠與紅色圍兜地藏菩薩。', build: buildP17_StoneLantern },
        { code: 'P18', name: '沿海風力發電機', badge: '💨 海岸風車', desc: '佇立於日向灘與日南海岸公路旁的旋轉白色大型風力發電機。', build: buildP18_WindTurbine },
        { code: 'P19', name: '鹿兒島灣彩色小漁船', badge: '⛵ 港灣船隻', desc: '停泊在錦江灣與日南海岸外海的日式近海彩色漁船。', build: () => buildP19_SmallFishingBoat(0x2563eb) },
        { code: 'P20', name: '國道公路里程指示牌', badge: '🛣️ 國道路標', desc: '標示 R3、R57、R220 國道地名與里程的綠底白字公路標誌。', build: buildP20_RoadMileageSign }
    ];

    function createPropByCode(code) {
        const spec = PROP_SPECS.find(s => s.code === code);
        return spec ? spec.build() : buildP09_WinterPineAndSnowman();
    }

    // 在主島嶼上高密度布置所有放大後的動態載具、店家、聚落、牧場赤牛、貓狗、路人與森林
    // 並透過 sampleGroundY 與道路/地標避讓機制，確保所有物件緊貼地面且不阻擋車隊與人物動線
    function populateIslandProps(parent, tramCurve, isMobile, sampleGroundY, roadCurve, landmarksData) {
        const propsGroup = new THREE.Group();
        const getGroundY = sampleGroundY || (() => 0.80);

        // 預先取樣自駕道路中心線，供靜態道具與樹木避開行車與人物散步走廊
        const roadSamples = [];
        if (roadCurve) {
            for (let i = 0; i <= 200; i++) {
                roadSamples.push(roadCurve.getPointAt(i / 200));
            }
        }

        function nudgeOffRoadAndLandmarks(x, z, minRoadDist, minLmDist) {
            let nx = x;
            let nz = z;
            if (roadSamples.length > 0 && minRoadDist > 0) {
                let nearest = null;
                let bestD = 999;
                for (let i = 0; i < roadSamples.length; i++) {
                    const d = Math.hypot(nx - roadSamples[i].x, nz - roadSamples[i].z);
                    if (d < bestD) {
                        bestD = d;
                        nearest = roadSamples[i];
                    }
                }
                if (nearest && bestD < minRoadDist) {
                    let dx = nx - nearest.x;
                    let dz = nz - nearest.z;
                    if (Math.hypot(dx, dz) < 0.05) { dx = 0.7; dz = -0.7; }
                    const len = Math.hypot(dx, dz);
                    nx = nearest.x + (dx / len) * minRoadDist;
                    nz = nearest.z + (dz / len) * minRoadDist;
                }
            }
            if (landmarksData && minLmDist > 0) {
                landmarksData.forEach(lm => {
                    const lx = lm.renderX !== undefined ? lm.renderX : lm.x;
                    const lz = lm.renderZ !== undefined ? lm.renderZ : lm.z;
                    const d = Math.hypot(nx - lx, nz - lz);
                    if (d < minLmDist) {
                        let dx = nx - lx;
                        let dz = nz - lz;
                        if (Math.hypot(dx, dz) < 0.05) { dx = -0.8; dz = 0.6; }
                        const len = Math.hypot(dx, dz);
                        nx = lx + (dx / len) * minLmDist;
                        nz = lz + (dz / len) * minLmDist;
                    }
                });
            }
            return { x: nx, z: nz, y: getGroundY(nx, nz) };
        }

        // 1. 主角 8 人座紅色自駕小巴 (放大為 1.18x 更醒目)
        const minivan = buildP01_Minivan();
        minivan.scale.setScalar(1.18);
        propsGroup.add(minivan);

        // 2. 熊本路面電車 (放大為 1.12x)
        const tram = buildP02_KumamotoTram();
        tram.scale.setScalar(1.12);
        propsGroup.add(tram);

        // 3. 櫻島渡輪 (放大為 1.18x，配合 1.2x 地圖座標)
        const ferry = buildP03_SakurajimaFerry();
        ferry.scale.setScalar(1.18);
        ferry.position.set(-4.14, 0.02, 10.18);
        propsGroup.add(ferry);

        // 4. 屋台拉麵攤與溫泉商店群 (放大並增加到 9 處，1.2x 地圖座標)
        const shopPlacements = [
            { fn: buildP04_RamenYatai, x: -3.42, z: -13.14, rot: 0.4 },  // 熊本黑亭拉麵屋台
            { fn: buildP04_RamenYatai, x: -5.82, z: 10.62,  rot: 0.8 },  // 鹿兒島屋台村
            { fn: buildP04_RamenYatai, x: 9.54,  z: 2.52,   rot: -0.5 }, // 宮崎地雞屋台
            { fn: buildP05_OnsenShop,  x: 4.02,  z: -18.78, rot: -0.3 }, // 黑川溫泉饅頭店
            { fn: buildP05_OnsenShop,  x: 5.82,  z: -18.96, rot: 0.4 },  // 黑川湯明伴手禮店
            { fn: buildP05_OnsenShop,  x: -2.58, z: -1.74,  rot: 0.5 },  // 人吉老街商店
            { fn: buildP05_OnsenShop,  x: -1.38, z: -14.52, rot: -0.2 }, // 熊本上通商店街
            { fn: buildP05_OnsenShop,  x: 6.66,  z: -11.22, rot: 0.3 },  // 高千穗神樂茶屋
            { fn: buildP05_OnsenShop,  x: -0.66, z: 5.22,   rot: -0.4 }  // 霧島溫泉市場
        ];
        shopPlacements.forEach(s => {
            const pos = nudgeOffRoadAndLandmarks(s.x, s.z, 1.05, 1.10);
            const m = s.fn();
            m.scale.setScalar(1.18);
            m.position.set(pos.x, pos.y, pos.z);
            m.rotation.y = s.rot;
            propsGroup.add(m);
        });

        // 5. 日式木造町家聚落組 (10 處城鎮群落，1.2x 地圖座標)
        const villagePlacements = [
            { x: -1.08, z: -13.68, rot: 0.2 },  // 熊本市區町屋
            { x: -3.12, z: -11.76, rot: -0.4 }, // 八代城下町
            { x: 1.92,  z: -14.16, rot: 0.5 },  // 阿蘇內牧溫泉街
            { x: -0.36, z: -1.44,  rot: -0.3 }, // 人吉球磨川聚落
            { x: -2.88, z: 3.12,   rot: 0.4 },  // 出水武家屋敷
            { x: 3.12,  z: 5.40,   rot: -0.2 }, // 都城聚落
            { x: 8.16,  z: 0.72,   rot: 0.1 },  // 宮崎佐土原城下町
            { x: 8.28,  z: 6.96,   rot: -0.5 }, // 日南飫肥城下町（九州小京都）
            { x: -5.76, z: 12.72,  rot: 0.3 },  // 知覽武家屋敷
            { x: 0.60,  z: 10.32,  rot: -0.3 }  // 鹿屋聚落
        ];
        villagePlacements.forEach(v => {
            const pos = nudgeOffRoadAndLandmarks(v.x, v.z, 1.12, 1.15);
            const m = buildP10_MachiyaVillage();
            m.scale.setScalar(1.22);
            m.position.set(pos.x, pos.y, pos.z);
            m.rotation.y = v.rot;
            propsGroup.add(m);
        });

        // 6. 日本街角自動販賣機與紅郵筒組 (6 處，1.2x 地圖座標)
        const vendingCoords = [
            { x: -1.44, z: -13.92, rot: 0.3 },
            { x: 4.32,  z: -17.76, rot: -0.4 },
            { x: 9.36,  z: 4.20,   rot: -0.8 },
            { x: -4.20, z: 8.88,   rot: 0.5 },
            { x: -2.16, z: -3.00,  rot: 0.2 },
            { x: 1.08,  z: 3.96,   rot: -0.3 }
        ];
        vendingCoords.forEach(vc => {
            const pos = nudgeOffRoadAndLandmarks(vc.x, vc.z, 0.92, 0.95);
            const vm = buildP12_VendingAndPostbox();
            vm.scale.setScalar(1.15);
            vm.position.set(pos.x, pos.y, pos.z);
            vm.rotation.y = vc.rot;
            propsGroup.add(vm);
        });

        // 7. 阿蘇草千里與霧島牧場放牧赤牛群 (7 頭會低頭吃草的赤牛，1.2x 地圖座標)
        const cattleList = [];
        const cattleCoords = [
            { x: 2.52, z: -16.08, rot: 0.5 },
            { x: 3.12, z: -16.56, rot: -0.8 },
            { x: 2.28, z: -16.92, rot: 1.2 },
            { x: 5.28, z: -16.68, rot: -0.3 },
            { x: 5.76, z: -17.28, rot: 0.9 },
            { x: 1.68, z: 5.28,   rot: -0.5 }, // 霧島高千穗牧場
            { x: 2.16, z: 5.76,   rot: 0.7 }
        ];
        cattleCoords.forEach((cc, idx) => {
            const pos = nudgeOffRoadAndLandmarks(cc.x, cc.z, 0.90, 0.95);
            const cow = buildP11_AsoCattle();
            cow.scale.setScalar(1.18);
            cow.position.set(pos.x, pos.y, pos.z);
            cow.rotation.y = cc.rot;
            cow.userData.phase = idx * 1.3;
            propsGroup.add(cow);
            cattleList.push(cow);
        });

        // 8. 海岸岬角白色燈塔與河川朱紅拱橋 (1.2x 地圖座標)
        const lighthouses = [
            { x: -5.04, z: 15.36 }, // 薩摩長崎鼻燈塔
            { x: -0.96, z: 15.60 }, // 大隅佐多岬燈塔
            { x: 10.68, z: -7.80 }, // 日向細島燈塔
            { x: -6.24, z: -11.40 } // 天草燈塔
        ];
        lighthouses.forEach(lh => {
            const m = buildP13_Lighthouse();
            m.scale.setScalar(1.25);
            m.position.set(lh.x, getGroundY(lh.x, lh.z), lh.z);
            propsGroup.add(m);
        });

        const bridges = [
            { x: -0.96, z: -2.64,  rot: 0.4 },  // 人吉球磨川大橋
            { x: 6.60,  z: -12.60, rot: -0.6 }, // 高千穗神都高架橋
            { x: 6.24,  z: 3.48,   rot: 0.15 }  // 大淀川橘橋
        ];
        bridges.forEach(br => {
            const pos = nudgeOffRoadAndLandmarks(br.x, br.z, 0.95, 1.0);
            const b = buildP14_RedArchBridge();
            b.scale.setScalar(1.25);
            b.position.set(pos.x, pos.y, pos.z);
            b.rotation.y = br.rot;
            propsGroup.add(b);
        });

        // 9. 小貓與柴犬 (放大為 1.25x，增加到 8 隻，1.2x 地圖座標)
        const pets = [];
        const petConfigs = [
            { fn: buildP06_CalicoCat, x: 5.34,  z: -18.66, r: 0.34, speed: 1.4 }, // 黑川溫泉貓
            { fn: buildP06_CalicoCat, x: -2.70, z: -13.32, r: 0.32, speed: 1.2 }, // 熊本城三毛貓
            { fn: buildP06_CalicoCat, x: -1.32, z: -2.34,  r: 0.32, speed: 1.3 }, // 人吉溫泉貓
            { fn: buildP06_CalicoCat, x: -4.20, z: 9.36,   r: 0.32, speed: 1.5 }, // 仙巖園貓祠三毛貓
            { fn: buildP07_ShibaDog,  x: -4.50, z: 10.62,  r: 0.36, speed: 1.8 }, // 鹿兒島西鄉隆盛柴犬
            { fn: buildP07_ShibaDog,  x: 9.72,  z: 5.46,   r: 0.35, speed: 1.6 }, // 青島柴犬
            { fn: buildP07_ShibaDog,  x: 0.66,  z: 4.38,   r: 0.34, speed: 1.7 }, // 霧島柴犬
            { fn: buildP07_ShibaDog,  x: 3.42,  z: -17.04, r: 0.34, speed: 1.5 }  // 大觀峰柴犬
        ];
        petConfigs.forEach((cfg, idx) => {
            const pos = nudgeOffRoadAndLandmarks(cfg.x, cfg.z, 0.95, 1.0);
            const pet = cfg.fn();
            pet.scale.setScalar(1.25);
            pet.userData.orbit = { cx: pos.x, cz: pos.z, baseY: pos.y, r: cfg.r, speed: cfg.speed, phase: idx * 1.7 };
            propsGroup.add(pet);
            pets.push(pet);
        });

        // 10. 散步路人 NPC (放大為 1.15x，增加到 12 位，1.2x 地圖座標)
        const walkers = [];
        const walkerCoords = [
            { x: -2.88, z: -14.16, color: 0x0d9488 },
            { x: -0.72, z: -13.80, color: 0xf59e0b },
            { x: 4.44,  z: -18.48, color: 0xe11d48 },
            { x: 3.48,  z: -15.12, color: 0x2563eb },
            { x: 9.72,  z: 3.36,   color: 0xd97706 },
            { x: 8.88,  z: 8.16,   color: 0xec4899 },
            { x: -5.28, z: 9.72,   color: 0x4f46e5 },
            { x: -3.00, z: 9.96,   color: 0x10b981 },
            { x: 7.08,  z: -11.52, color: 0x059669 },
            { x: 0.78,  z: 5.16,   color: 0x9333ea },
            { x: -1.92, z: -1.92,  color: 0xea580c },
            { x: 3.84,  z: -6.60,  color: 0x0284c7 }
        ];
        const maxWalkers = isMobile ? 8 : walkerCoords.length;
        for (let i = 0; i < maxWalkers; i++) {
            const wc = walkerCoords[i];
            const pos = nudgeOffRoadAndLandmarks(wc.x, wc.z, 1.05, 1.05);
            const w = buildP08_Pedestrian(wc.color);
            w.scale.setScalar(1.15);
            w.userData.orbit = { cx: pos.x, cz: pos.z, baseY: pos.y, r: 0.36, speed: 0.85 + (i % 3) * 0.2, phase: i * 1.1 };
            propsGroup.add(w);
            walkers.push(w);
        }

        // 11. 覆雪杉木林、金黃銀杏林與雪人點綴 (高密度擴充至 92 處，徹底消除公路兩側空洞)
        const treeCoords = [
            // 北部熊本市郊・菊池・阿蘇外輪山・黑川山區
            [1.44, -16.32, 0.96, 'snow'],   [2.64, -18.00, 0.96, 'snow'],   [5.88, -17.40, 0.96, 'snow'],
            [6.24, -13.44, 0.96, 'snow'],   [5.52, -10.32, 0.96, 'snow'],   [2.88, -10.08, 1.02, 'snow'],
            [0.72, -15.84, 0.80, 'ginkgo'], [-3.12, -14.64,0.80, 'ginkgo'], [-0.96, -11.76,0.80, 'tree_only'],
            [-2.40, -16.20, 0.80, 'snow'],  [-1.68, -17.40, 0.80, 'ginkgo'], [0.12, -17.80, 0.82, 'snow'],
            [4.08, -16.80, 0.96, 'snow'],   [4.92, -18.24, 0.96, 'snow'],   [6.84, -16.20, 0.96, 'snow'],
            [3.72, -13.20, 0.96, 'tree_only'],[1.20, -13.92, 0.82, 'snow'],[-0.48, -14.88, 0.80, 'ginkgo'],
            // 阿蘇至高千穗峽五瀨川溪谷沿線公路兩側
            [6.48, -11.40, 0.96, 'snow'],   [7.32, -12.96, 0.96, 'snow'],   [8.04, -11.76, 0.96, 'snow'],
            [5.16, -11.88, 0.96, 'tree_only'],[7.80, -14.16, 0.96, 'snow'],[6.96, -9.84,  0.96, 'tree_only'],
            // 中央山地・九重連峰・球磨川流域深山林木
            [0.96, -7.80,  1.02, 'snow'],   [3.12, -8.16,  1.05, 'snow'],   [4.56, -9.00,  1.02, 'snow'],
            [5.76, -6.24,  1.02, 'tree_only'],[3.60, -5.40,1.02, 'snow'],   [1.68, -4.20,  1.02, 'tree_only'],
            [0.24, -5.76,  0.96, 'ginkgo'], [-2.16, -5.04, 0.82, 'tree_only'],[-2.88, -7.44,0.80, 'ginkgo'],
            [6.96, -8.16,  0.96, 'tree_only'],[8.16, -5.76,0.82, 'tree_only'],[7.44, -2.64, 0.82, 'ginkgo'],
            [4.56, -2.16,  0.96, 'tree_only'],[2.40, -1.80,0.96, 'snow'],   [0.60, -0.48,  0.96, 'tree_only'],
            [-1.44, -3.84, 0.82, 'snow'],   [-0.84, -6.24, 0.96, 'tree_only'],[2.04, -6.96, 1.02, 'snow'],
            [4.20, -7.44,  1.02, 'snow'],   [5.04, -4.32,  1.02, 'tree_only'],[3.24, -3.36, 0.96, 'snow'],
            [-1.92, -8.88, 0.82, 'ginkgo'], [-3.60, -9.60, 0.80, 'tree_only'],[-3.84, -6.72, 0.80, 'ginkgo'],
            // 高千穗至日向細島・延岡・宮崎東海岸公路林道
            [9.12, -9.36,  0.82, 'tree_only'],[9.84, -6.48, 0.80, 'ginkgo'], [8.88, -4.08, 0.82, 'tree_only'],
            [9.48, -1.68,  0.80, 'snow'],   [8.64,  0.24,  0.82, 'tree_only'],[9.96,  1.44, 0.80, 'ginkgo'],
            // 霧島連峰・蝦野高原・人吉至鹿兒島內陸縱貫公路
            [-2.64, 0.60,  0.80, 'ginkgo'], [-0.72, 2.16,  0.96, 'tree_only'],[1.80, 2.64,  0.96, 'snow'],
            [3.84,  1.92,  0.96, 'tree_only'],[5.76, 0.96, 0.82, 'ginkgo'], [7.68, 4.32,    0.80, 'tree_only'],
            [-0.96, 6.48,  0.96, 'snow'],   [2.16,  6.96,  0.82, 'tree_only'],[4.20, 6.24,  0.82, 'ginkgo'],
            [0.24,  1.44,  0.96, 'snow'],   [-1.68, 3.84,  0.82, 'tree_only'],[2.88,  4.56, 0.96, 'snow'],
            [-0.12, 4.32,  0.96, 'tree_only'],[3.48,  3.12, 0.82, 'ginkgo'], [5.16,  4.80, 0.82, 'tree_only'],
            // 宮崎至日南海岸・飫肥城下町沿線棕櫚與林木
            [8.88,  5.76,  0.80, 'ginkgo'], [9.36,  7.20,  0.80, 'tree_only'],[7.44,  6.72, 0.82, 'snow'],
            [8.16,  8.88,  0.80, 'ginkgo'], [6.96,  8.16,  0.82, 'tree_only'],[7.80, 10.32, 0.80, 'tree_only'],
            // 薩摩半島・指宿・櫻島・知覽・大隅半島
            [-5.52, 11.28, 0.80, 'ginkgo'], [-4.56, 13.44, 0.80, 'tree_only'],[0.96, 11.76, 0.80, 'tree_only'],
            [1.92,  9.84,  0.80, 'ginkgo'], [-0.24, 13.80, 0.80, 'tree_only'],[-3.84, 14.88, 0.80, 'tree_only'],
            [-2.40, 12.24, 0.82, 'snow'],   [-1.44, 10.56, 0.82, 'tree_only'],[-0.84, 12.48, 0.80, 'ginkgo'],
            [2.88,  8.64,  0.82, 'snow'],   [1.44,  13.44, 0.80, 'ginkgo'], [-6.24, 13.92, 0.80, 'tree_only'],
            // 西部熊本八代・水俁海濱沿線
            [-4.08, -8.16, 0.80, 'tree_only'],[-3.72, -3.12, 0.80, 'ginkgo'],[-4.32, 0.72,  0.80, 'tree_only'],
            [-3.96, 4.80,  0.80, 'snow'],   [-4.68, 7.20,  0.80, 'ginkgo'], [-2.04, -12.48, 0.80, 'snow']
        ];
        treeCoords.forEach((tc, idx) => {
            const pos = nudgeOffRoadAndLandmarks(tc[0], tc[1], 0.90, 0.95);
            const t = buildP09_WinterPineAndSnowman(tc[3]);
            t.scale.setScalar(1.05 + (idx % 3) * 0.22);
            t.position.set(pos.x, pos.y, pos.z);
            t.rotation.y = idx * 1.1;
            propsGroup.add(t);
        });

        parent.add(propsGroup);
        
        // 12. 公路沿線朱紅鳥居 (8 處佇立於山道、神社參道與轉彎路肩)
        const toriiCoords = [
            { x: -0.72, z: -14.64, rot: 0.15 }, // 熊本加藤神社公路前
            { x: 3.84,  z: -17.28, rot: -0.4 }, // 阿蘇外輪山公路口
            { x: 6.84,  z: -11.76, rot: 0.3 },  // 高千穗峽山道入口
            { x: -0.48, z: 2.88,   rot: 0.2 },  // 霧島神宮山麓路肩
            { x: 9.36,  z: 5.76,   rot: -0.6 }, // 青島神社海岸參道口
            { x: 8.52,  z: 8.40,   rot: -0.3 }, // 鵜戶神宮奇岩山道
            { x: -5.04, z: 12.24,  rot: 0.4 },  // 指宿薩摩街道
            { x: -1.68, z: -2.88,  rot: -0.2 }  // 人吉青井阿蘇神社路口
        ];
        toriiCoords.forEach(tc => {
            const pos = nudgeOffRoadAndLandmarks(tc.x, tc.z, 0.90, 0.95);
            const torii = buildP15_RoadsideTorii();
            torii.scale.setScalar(1.20);
            torii.position.set(pos.x, pos.y, pos.z);
            torii.rotation.y = tc.rot;
            propsGroup.add(torii);
        });

        // 13. 九州懷舊鄉間巴士候車亭與站牌 (10 處點綴於鄉間長途路肩)
        const busStopCoords = [
            { x: -2.16, z: -12.72, rot: 0.3 },  // 熊本市郊往八代
            { x: 1.20,  z: -17.28, rot: -0.3 }, // 大觀峰山腳站
            { x: 4.80,  z: -16.08, rot: 0.4 },  // 阿蘇草千里站
            { x: 7.44,  z: -10.08, rot: -0.5 }, // 高千穗町外站
            { x: 8.76,  z: -2.16,  rot: 0.2 },  // 日向灘國道站
            { x: 9.60,  z: 3.96,   rot: -0.4 }, // 宮崎橘通南站
            { x: 8.04,  z: 7.68,   rot: -0.7 }, // 日南海岸公路站
            { x: 2.64,  z: 4.80,   rot: 0.3 },  // 霧島溫泉鄉站
            { x: -3.84, z: 7.92,   rot: -0.3 }, // 鹿兒島北側山道站
            { x: -0.96, z: -4.32,  rot: 0.2 }   // 球磨川沿岸站
        ];
        busStopCoords.forEach(bc => {
            const pos = nudgeOffRoadAndLandmarks(bc.x, bc.z, 0.88, 0.92);
            const bs = buildP16_BusStop();
            bs.scale.setScalar(1.15);
            bs.position.set(pos.x, pos.y, pos.z);
            bs.rotation.y = bc.rot;
            propsGroup.add(bs);
        });

        // 14. 暖光石燈籠與路旁地藏小祠 (10 處古街道守護)
        const lanternCoords = [
            { x: -1.68, z: -14.16, rot: 0.2 },
            { x: 3.24,  z: -17.52, rot: -0.3 },
            { x: 5.40,  z: -18.24, rot: 0.5 },
            { x: 6.36,  z: -12.00, rot: -0.4 },
            { x: 0.24,  z: 3.36,   rot: 0.3 },
            { x: -4.80, z: 10.08,  rot: -0.2 },
            { x: -2.04, z: -1.44,  rot: 0.4 },
            { x: 8.64,  z: 6.24,   rot: -0.6 },
            { x: 2.88,  z: -14.88, rot: 0.2 },
            { x: -0.48, z: 6.00,   rot: -0.3 }
        ];
        lanternCoords.forEach(lc => {
            const pos = nudgeOffRoadAndLandmarks(lc.x, lc.z, 0.85, 0.90);
            const sl = buildP17_StoneLantern();
            sl.scale.setScalar(1.18);
            sl.position.set(pos.x, pos.y, pos.z);
            sl.rotation.y = lc.rot;
            propsGroup.add(sl);
        });

        // 15. 宮崎/日南沿海風力發電機群 (6 座旋轉風車，佇立於日向灘海崖)
        const windTurbines = [];
        const turbineCoords = [
            { x: 10.44, z: -6.00 },
            { x: 10.20, z: -3.60 },
            { x: 10.56, z: -0.96 },
            { x: 10.32, z: 2.16 },
            { x: 9.72,  z: 6.48 },
            { x: 9.12,  z: 9.60 }
        ];
        turbineCoords.forEach((tc, idx) => {
            const wt = buildP18_WindTurbine();
            wt.scale.setScalar(1.22);
            wt.position.set(tc.x, getGroundY(tc.x, tc.z), tc.z);
            wt.rotation.y = -0.4 + idx * 0.15;
            propsGroup.add(wt);
            windTurbines.push(wt);
        });

        // 16. 彩色近海漁船 (6 艘停泊於鹿兒島錦江灣與宮崎日南外海，輕微浪湧晃動)
        const fishingBoats = [];
        const boatCoords = [
            { x: -5.28, z: 10.32, color: 0x2563eb }, // 鹿兒島灣漁船
            { x: -3.84, z: 11.28, color: 0xd97706 },
            { x: -4.92, z: 13.80, color: 0x059669 },
            { x: 10.80, z: -4.80, color: 0xdc2626 }, // 日向灘漁船
            { x: 10.68, z: 3.60,  color: 0x7c3aed },
            { x: 9.96,  z: 8.16,  color: 0x0284c7 }
        ];
        boatCoords.forEach((bc, idx) => {
            const boat = buildP19_SmallFishingBoat(bc.color);
            boat.scale.setScalar(1.20);
            boat.position.set(bc.x, -0.06, bc.z);
            boat.rotation.y = idx * 1.4;
            propsGroup.add(boat);
            fishingBoats.push(boat);
        });

        // 17. 國道里程指示牌 (8 處重要公路路口)
        const signCoords = [
            { x: -1.80, z: -15.12, rot: 0.1 },  // R3 熊本
            { x: 1.92,  z: -17.52, rot: -0.4 }, // R57 阿蘇
            { x: 5.64,  z: -13.92, rot: 0.3 },  // R218 高千穗
            { x: 8.88,  z: -1.20,  rot: -0.2 }, // R10 宮崎
            { x: 8.88,  z: 6.96,   rot: -0.6 }, // R220 日南海岸
            { x: 1.44,  z: 3.84,   rot: 0.2 },  // R223 霧島溫泉
            { x: -4.68, z: 8.88,   rot: 0.4 },  // R10 鹿兒島
            { x: -1.56, z: -3.84,  rot: -0.3 }  // R219 人吉球磨
        ];
        signCoords.forEach(sc => {
            const pos = nudgeOffRoadAndLandmarks(sc.x, sc.z, 0.86, 0.90);
            const rSign = buildP20_RoadMileageSign();
            rSign.scale.setScalar(1.15);
            rSign.position.set(pos.x, pos.y, pos.z);
            rSign.rotation.y = sc.rot;
            propsGroup.add(rSign);
        });

        return { propsGroup, minivan, tram, ferry, pets, walkers, cattleList, windTurbines, fishingBoats, sampleGroundY: getGroundY };
    }

    function updatePropsAnimation(propState, tramCurve, elapsed) {
        const getGroundY = (propState && propState.sampleGroundY) || (() => 0.80);

        // 1. 熊本市電沿軌道平穩往返
        if (propState.tram && tramCurve) {
            const pingPong = (Math.sin(elapsed * 0.45) + 1) * 0.5;
            const pos = tramCurve.getPointAt(pingPong);
            const tan = tramCurve.getTangentAt(pingPong);
            propState.tram.position.set(pos.x, getGroundY(pos.x, pos.z) + 0.04, pos.z);
            propState.tram.rotation.y = Math.atan2(tan.x, tan.z);
        }

        // 2. 櫻島渡輪橫越錦江灣往返鹿兒島港與櫻島 (1.2x 地圖座標)
        if (propState.ferry) {
            const s = (Math.sin(elapsed * 0.65) + 1) * 0.5;
            propState.ferry.position.x = -4.46 + s * 0.70;
            propState.ferry.position.z = 10.18 + Math.sin(elapsed * 1.3) * 0.04;
            propState.ferry.position.y = -0.16 + Math.sin(elapsed * 2.8) * 0.03;
            propState.ferry.rotation.y = Math.PI / 2;
            propState.ferry.rotation.z = Math.sin(elapsed * 2.2) * 0.04;
        }

        // 3. 貓狗小圈散步與搖尾巴 (每幀動態對齊地面高度)
        if (propState.pets) {
            propState.pets.forEach(pet => {
                const o = pet.userData.orbit;
                const ang = elapsed * o.speed + o.phase;
                const px = o.cx + Math.cos(ang) * o.r;
                const pz = o.cz + Math.sin(ang) * o.r;
                const gy = getGroundY(px, pz);
                pet.position.set(
                    px,
                    gy + Math.abs(Math.sin(elapsed * 7.0 + o.phase)) * 0.05,
                    pz
                );
                pet.rotation.y = Math.atan2(-Math.sin(ang), Math.cos(ang));
                if (pet.userData.tail) {
                    pet.userData.tail.rotation.z = Math.sin(elapsed * 10.0) * 0.35;
                }
            });
        }

        // 4. 路人散步 (每幀動態對齊地面高度)
        if (propState.walkers) {
            propState.walkers.forEach(w => {
                const o = w.userData.orbit;
                const ang = elapsed * o.speed + o.phase;
                const wx = o.cx + Math.cos(ang) * o.r;
                const wz = o.cz + Math.sin(ang) * o.r;
                const gy = getGroundY(wx, wz);
                w.position.set(
                    wx,
                    gy + Math.abs(Math.sin(elapsed * 5.0 + o.phase)) * 0.04,
                    wz
                );
                w.rotation.y = Math.atan2(-Math.sin(ang), Math.cos(ang));
            });
        }

        // 5. 阿蘇赤牛低頭吃草擺動
        if (propState.cattleList) {
            propState.cattleList.forEach(cow => {
                if (cow.userData.head) {
                    cow.userData.head.rotation.x = 0.25 + Math.sin(elapsed * 2.2 + cow.userData.phase) * 0.22;
                }
            });
        }

        // 6. 宮崎/日南沿海風力發電機風葉自然旋轉
        if (propState.windTurbines) {
            propState.windTurbines.forEach((wt, idx) => {
                if (wt.userData.rotorGroup) {
                    wt.userData.rotorGroup.rotation.z = elapsed * (1.85 + (idx % 3) * 0.35);
                }
            });
        }

        // 7. 外海彩色小漁船隨波浪起伏晃動
        if (propState.fishingBoats) {
            propState.fishingBoats.forEach((boat, idx) => {
                const phase = elapsed * 1.8 + idx * 1.5;
                boat.position.y = -0.06 + Math.sin(phase) * 0.025;
                boat.rotation.z = Math.sin(phase * 0.8) * 0.05;
                boat.rotation.x = Math.cos(phase * 0.9) * 0.035;
            });
        }
    }

    window.KyushuIsland.Props = {
        PROP_SPECS,
        createPropByCode,
        populateIslandProps,
        updatePropsAnimation
    };
})();
