/**
 * portal/landmarks.js
 * 南九州 17 處真實地理景點 Low-poly 精緻模型與動態特效產生器。
 * 每個景點皆有獨立 builder，供完整大廳島嶼與 preview.html 單項旋轉預覽共用。
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

    function createToriiGate(scale, colorHex) {
        const g = new THREE.Group();
        const mat = new THREE.MeshLambertMaterial({ color: colorHex || 0xdc2626, flatShading: true });
        const blackMat = new THREE.MeshLambertMaterial({ color: 0x1c1917 });

        const postGeo = new THREE.CylinderGeometry(0.05 * scale, 0.06 * scale, 0.9 * scale, 8);
        const postL = new THREE.Mesh(postGeo, mat);
        postL.position.set(-0.32 * scale, 0.45 * scale, 0);
        const postR = new THREE.Mesh(postGeo, mat);
        postR.position.set(0.32 * scale, 0.45 * scale, 0);

        const baseGeo = new THREE.CylinderGeometry(0.08 * scale, 0.09 * scale, 0.12 * scale, 8);
        const baseL = new THREE.Mesh(baseGeo, blackMat);
        baseL.position.set(-0.32 * scale, 0.06 * scale, 0);
        const baseR = new THREE.Mesh(baseGeo, blackMat);
        baseR.position.set(0.32 * scale, 0.06 * scale, 0);

        const kasagi = new THREE.Mesh(new THREE.BoxGeometry(1.05 * scale, 0.09 * scale, 0.14 * scale), mat);
        kasagi.position.set(0, 0.90 * scale, 0);
        const shimaki = new THREE.Mesh(new THREE.BoxGeometry(0.92 * scale, 0.06 * scale, 0.11 * scale), blackMat);
        shimaki.position.set(0, 0.96 * scale, 0);
        const nuki = new THREE.Mesh(new THREE.BoxGeometry(0.82 * scale, 0.06 * scale, 0.08 * scale), mat);
        nuki.position.set(0, 0.68 * scale, 0);

        g.add(postL, postR, baseL, baseR, kasagi, shimaki, nuki);
        enableShadow(g);
        return g;
    }

    // L01: 熊本機場 KMJ (2023 新阿蘇熊本木造航廈 + 管制塔台 + 空橋 + 條紋跑道 + 華航客機起降)
    function buildL01_Airport() {
        const g = new THREE.Group();
        const woodMat = new THREE.MeshLambertMaterial({ color: 0xd97706, flatShading: true });
        const roofMat = new THREE.MeshLambertMaterial({ color: 0x334155, flatShading: true });
        const glassMat = new THREE.MeshLambertMaterial({ color: 0x7dd3fc });
        const whiteMat = new THREE.MeshLambertMaterial({ color: 0xf8fafc });
        const redAccent = new THREE.MeshLambertMaterial({ color: 0xe11d48 });
        const yellowMat = new THREE.MeshLambertMaterial({ color: 0xfacc15 });

        // 1. 航廈主體與木造格柵屋頂
        const term = new THREE.Mesh(new THREE.BoxGeometry(1.24, 0.38, 0.58), woodMat);
        term.position.set(0, 0.19, -0.06);
        const glass = new THREE.Mesh(new THREE.BoxGeometry(1.16, 0.24, 0.60), glassMat);
        glass.position.set(0, 0.19, -0.06);
        const roof = new THREE.Mesh(new THREE.BoxGeometry(1.36, 0.08, 0.72), roofMat);
        roof.position.set(0, 0.41, -0.06);
        const roofUpper = new THREE.Mesh(new THREE.BoxGeometry(0.86, 0.07, 0.46), woodMat);
        roofUpper.position.set(0, 0.48, -0.06);
        // 航廈頂部 KMJ 紅底招牌
        const signBoard = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.12, 0.06), redAccent);
        signBoard.position.set(0.12, 0.57, 0.18);
        g.add(term, glass, roof, roofUpper, signBoard);

        // 2. 登機空橋 (Jetbridge)
        const bridge = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.12, 0.38), whiteMat);
        bridge.position.set(0.26, 0.22, 0.26);
        g.add(bridge);

        // 3. 紅白相間飛航管制塔台
        const towerShaft = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.12, 0.84, 8), whiteMat);
        towerShaft.position.set(-0.48, 0.42, -0.22);
        const towerBand = new THREE.Mesh(new THREE.CylinderGeometry(0.098, 0.105, 0.16, 8), redAccent);
        towerBand.position.set(-0.48, 0.66, -0.22);
        const towerCab = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.13, 0.18, 8), glassMat);
        towerCab.position.set(-0.48, 0.90, -0.22);
        const towerRoof = new THREE.Mesh(new THREE.ConeGeometry(0.20, 0.12, 8), roofMat);
        towerRoof.position.set(-0.48, 1.04, -0.22);
        const radarBeacon = new THREE.Mesh(new THREE.SphereGeometry(0.05, 8, 8), yellowMat);
        radarBeacon.position.set(-0.48, 1.13, -0.22);
        g.add(towerShaft, towerBand, towerCab, towerRoof, radarBeacon);

        // 4. 柏油跑道與白色虛線標線
        const runway = new THREE.Mesh(
            new THREE.BoxGeometry(1.56, 0.025, 0.34),
            new THREE.MeshLambertMaterial({ color: 0x1e293b })
        );
        runway.position.set(0.05, 0.015, 0.52);
        g.add(runway);

        for (let i = -3; i <= 3; i++) {
            const stripe = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.03, 0.035), whiteMat);
            stripe.position.set(0.05 + i * 0.21, 0.018, 0.52);
            g.add(stripe);
        }

        // 5. 華航紅梅尾翼客機 (雙引擎 + 機翼 + 駕駛艙窗)
        const plane = new THREE.Group();
        const fuselage = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.065, 0.66, 10), whiteMat);
        fuselage.rotation.z = Math.PI / 2;
        const nose = new THREE.Mesh(new THREE.SphereGeometry(0.074, 8, 8), whiteMat);
        nose.position.set(0.32, 0, 0);
        const cockpit = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.045, 0.09), glassMat);
        cockpit.position.set(0.29, 0.035, 0);
        const wing = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.022, 0.68), whiteMat);
        wing.position.set(0.02, -0.01, 0);
        const engGeo = new THREE.CylinderGeometry(0.032, 0.032, 0.12, 8);
        engGeo.rotateZ(Math.PI / 2);
        const engL = new THREE.Mesh(engGeo, roofMat);
        engL.position.set(0.04, -0.04, 0.18);
        const engR = new THREE.Mesh(engGeo, roofMat);
        engR.position.set(0.04, -0.04, -0.18);
        const tail = new THREE.Mesh(
            new THREE.BoxGeometry(0.13, 0.19, 0.035),
            new THREE.MeshLambertMaterial({ color: 0xf43f5e }) // 華航紅梅尾翼意象
        );
        tail.position.set(-0.27, 0.10, 0);
        plane.add(fuselage, nose, cockpit, wing, engL, engR, tail);
        plane.position.set(0.12, 0.18, 0.52);
        plane.rotation.z = 0.15;
        g.add(plane);
        g.userData.plane = plane;

        enableShadow(g);
        return g;
    }

    // L02: 熊本城 (武者返石垣 + 多層黑白色天守閣 + 鯱 + 城彩苑町屋)
    function buildL02_KumamotoCastle() {
        const g = new THREE.Group();
        const stoneMat = new THREE.MeshLambertMaterial({ color: 0x78716c, flatShading: true });
        const wallBlack = new THREE.MeshLambertMaterial({ color: 0x292524, flatShading: true });
        const wallWhite = new THREE.MeshLambertMaterial({ color: 0xfafaf9, flatShading: true });
        const roofDark = new THREE.MeshLambertMaterial({ color: 0x334155, flatShading: true });
        const goldMat = new THREE.MeshLambertMaterial({ color: 0xfacc15 });

        // 武者返斜石垣
        const ishigaki = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.85, 0.48, 4), stoneMat);
        ishigaki.rotation.y = Math.PI / 4;
        ishigaki.position.y = 0.24;
        g.add(ishigaki);

        // 三層天守閣
        const tiers = [
            { w: 0.72, h: 0.30, y: 0.62, roofW: 0.96 },
            { w: 0.54, h: 0.26, y: 0.92, roofW: 0.76 },
            { w: 0.38, h: 0.24, y: 1.18, roofW: 0.58 }
        ];
        tiers.forEach(t => {
            const wBody = new THREE.Mesh(new THREE.BoxGeometry(t.w, t.h * 0.4, t.w), wallWhite);
            wBody.position.y = t.y - t.h * 0.25;
            const bBody = new THREE.Mesh(new THREE.BoxGeometry(t.w * 0.98, t.h * 0.6, t.w * 0.98), wallBlack);
            bBody.position.y = t.y + t.h * 0.15;
            const roof = new THREE.Mesh(new THREE.ConeGeometry(t.roofW * 0.72, 0.16, 4), roofDark);
            roof.rotation.y = Math.PI / 4;
            roof.position.y = t.y + t.h * 0.52;
            g.add(wBody, bBody, roof);
        });

        // 屋頂金鯱
        const shachiL = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.09, 0.05), goldMat);
        shachiL.position.set(-0.12, 1.44, 0);
        const shachiR = shachiL.clone();
        shachiR.position.set(0.12, 1.44, 0);
        g.add(shachiL, shachiR);

        // 城彩苑木造小吃屋
        const shop = new THREE.Mesh(
            new THREE.BoxGeometry(0.42, 0.26, 0.30),
            new THREE.MeshLambertMaterial({ color: 0x9a3412 })
        );
        shop.position.set(0.68, 0.13, 0.35);
        const shopRoof = new THREE.Mesh(new THREE.ConeGeometry(0.34, 0.15, 4), roofDark);
        shopRoof.rotation.y = Math.PI / 4;
        shopRoof.position.set(0.68, 0.32, 0.35);
        g.add(shop, shopRoof);

        enableShadow(g);
        return g;
    }

    // L03: 水前寺成趣園 (迷你富士山築山 + 湧泉池 + 茶屋 + 石橋)
    function buildL03_Suizenji() {
        const g = new THREE.Group();
        const waterMat = new THREE.MeshLambertMaterial({ color: 0x38bdf8 });
        const grassMat = new THREE.MeshLambertMaterial({ color: 0x65a30d, flatShading: true });
        const snowMat = new THREE.MeshLambertMaterial({ color: 0xf8fafc, flatShading: true });

        // 湧泉池
        const pond = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.65, 0.06, 14), waterMat);
        pond.position.set(0.1, 0.03, 0.1);
        g.add(pond);

        // 水前寺富士築山
        const fuji = new THREE.Mesh(new THREE.ConeGeometry(0.42, 0.58, 10), grassMat);
        fuji.position.set(-0.22, 0.29, -0.18);
        const fujiTop = new THREE.Mesh(new THREE.ConeGeometry(0.16, 0.22, 10), snowMat);
        fujiTop.position.set(-0.22, 0.48, -0.18);
        g.add(fuji, fujiTop);

        // 古今傳授之間茶屋
        const chaya = new THREE.Mesh(
            new THREE.BoxGeometry(0.38, 0.22, 0.28),
            new THREE.MeshLambertMaterial({ color: 0xb45309 })
        );
        chaya.position.set(0.35, 0.12, -0.22);
        const thatch = new THREE.Mesh(
            new THREE.ConeGeometry(0.32, 0.18, 4),
            new THREE.MeshLambertMaterial({ color: 0x78350f })
        );
        thatch.rotation.y = Math.PI / 4;
        thatch.position.set(0.35, 0.30, -0.22);
        g.add(chaya, thatch);

        enableShadow(g);
        return g;
    }

    // L04: 阿蘇中岳火山口・草千里 (破火山口 + 翠綠火口湖 + 山頂雪原觀景平台 + 白煙粒子)
    function buildL04_AsoCrater() {
        const g = new THREE.Group();
        const rockMat = new THREE.MeshLambertMaterial({ color: 0x57534e, flatShading: true });
        const snowMat = new THREE.MeshLambertMaterial({ color: 0xf8fafc, flatShading: true });
        const woodMat = new THREE.MeshLambertMaterial({ color: 0x92400e });
        const lakeMat = new THREE.MeshBasicMaterial({ color: 0x2dd4bf }); // 中岳翠綠湯溜り

        const cone = new THREE.Mesh(new THREE.CylinderGeometry(0.82, 1.42, 1.12, 10), rockMat);
        cone.position.y = 0.56;
        g.add(cone);

        // 山頂寬闊積雪環與火口觀景步道平台 (讓 4 位角色可以直接站上阿蘇火山頂！)
        const snowRing = new THREE.Mesh(new THREE.CylinderGeometry(0.86, 1.02, 0.34, 10), snowMat);
        snowRing.position.y = 0.98;
        g.add(snowRing);

        const summitDeck = new THREE.Mesh(new THREE.BoxGeometry(1.45, 0.10, 0.52), woodMat);
        summitDeck.position.set(0, 1.15, 0.36);
        g.add(summitDeck);

        // 火山口翡翠綠湖面
        const craterLake = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.38, 0.08, 10), lakeMat);
        craterLake.position.set(0, 1.16, -0.10);
        g.add(craterLake);

        // 袅袅白煙球團 (由動畫迴圈更新)
        const puffs = [];
        const puffMat = new THREE.MeshLambertMaterial({ color: 0xffffff, transparent: true, opacity: 0.75 });
        for (let i = 0; i < 5; i++) {
            const p = new THREE.Mesh(new THREE.DodecahedronGeometry(0.18 + i * 0.04, 0), puffMat.clone());
            p.position.set((Math.random() - 0.5) * 0.2, 1.3 + i * 0.28, (Math.random() - 0.5) * 0.2);
            p.userData = { baseY: 1.25, offset: i * 0.2 };
            g.add(p);
            puffs.push(p);
        }
        g.userData.puffs = puffs;

        enableShadow(g);
        return g;
    }

    // L05: 大觀峰展望台 (斷崖展望台 + 望遠鏡 + 小國牛乳亭)
    function buildL05_Daikanbo() {
        const g = new THREE.Group();
        const cliffMat = new THREE.MeshLambertMaterial({ color: 0x658354, flatShading: true });
        const snowMat = new THREE.MeshLambertMaterial({ color: 0xf1f5f9, flatShading: true });
        const woodMat = new THREE.MeshLambertMaterial({ color: 0x92400e });

        const ridge = new THREE.Mesh(new THREE.ConeGeometry(0.85, 0.82, 7), cliffMat);
        ridge.position.y = 0.41;
        const deck = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.45, 0.12, 8), snowMat);
        deck.position.y = 0.72;
        const rail = new THREE.Mesh(new THREE.CylinderGeometry(0.40, 0.40, 0.10, 8, 1, true), woodMat);
        rail.position.y = 0.82;

        // 展望台地標石碑
        const pillar = new THREE.Mesh(
            new THREE.BoxGeometry(0.12, 0.28, 0.12),
            new THREE.MeshLambertMaterial({ color: 0x44403c })
        );
        pillar.position.set(0, 0.90, 0);

        g.add(ridge, deck, rail, pillar);
        enableShadow(g);
        return g;
    }

    // L06: 黑川溫泉・山彥旅館・湯明竹燈祭 (木造旅館 + 檜木露天風呂 + 發光竹燈籠 + 溫泉蒸氣)
    function buildL06_KurokawaOnsen() {
        const g = new THREE.Group();
        const woodDark = new THREE.MeshLambertMaterial({ color: 0x451a03, flatShading: true });
        const wallWarm = new THREE.MeshLambertMaterial({ color: 0xfef3c7 });
        const snowRoofMat = new THREE.MeshLambertMaterial({ color: 0xf8fafc, flatShading: true });
        const waterMat = new THREE.MeshLambertMaterial({ color: 0x38bdf8 });
        const lanternMat = new THREE.MeshBasicMaterial({ color: 0xfbbf24 });

        // 山彥旅館木造建築
        const inn = new THREE.Mesh(new THREE.BoxGeometry(0.75, 0.45, 0.52), wallWarm);
        inn.position.set(-0.22, 0.22, -0.15);
        const beams = new THREE.Mesh(new THREE.BoxGeometry(0.77, 0.12, 0.54), woodDark);
        beams.position.set(-0.22, 0.36, -0.15);
        const roof = new THREE.Mesh(new THREE.ConeGeometry(0.62, 0.28, 4), snowRoofMat);
        roof.rotation.y = Math.PI / 4;
        roof.position.set(-0.22, 0.56, -0.15);
        g.add(inn, beams, roof);

        // 仙人風呂露天岩石湯池
        const tubOuter = new THREE.Mesh(
            new THREE.CylinderGeometry(0.46, 0.50, 0.22, 10),
            new THREE.MeshLambertMaterial({ color: 0x78350f, flatShading: true })
        );
        tubOuter.position.set(0.38, 0.11, 0.22);
        const tubWater = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.24, 10), waterMat);
        tubWater.position.set(0.38, 0.12, 0.22);
        g.add(tubOuter, tubWater);

        // 冬季限定「湯明 (Yuakari)」竹燈籠球
        const lanterns = [];
        for (let i = 0; i < 6; i++) {
            const ang = (i / 6) * Math.PI * 2;
            const l = new THREE.Mesh(new THREE.SphereGeometry(0.065, 8, 8), lanternMat.clone());
            l.position.set(0.38 + Math.cos(ang) * 0.44, 0.28, 0.22 + Math.sin(ang) * 0.44);
            g.add(l);
            lanterns.push(l);
        }
        g.userData.lanterns = lanterns;

        // 溫泉白煙蒸氣
        const steam = [];
        const steamMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.55 });
        for (let i = 0; i < 3; i++) {
            const s = new THREE.Mesh(new THREE.SphereGeometry(0.11 + i * 0.03, 6, 6), steamMat.clone());
            s.position.set(0.38 + (i - 1) * 0.1, 0.32 + i * 0.18, 0.22);
            s.userData = { baseY: 0.28, offset: i * 0.33 };
            g.add(s);
            steam.push(s);
        }
        g.userData.puffs = steam;

        enableShadow(g);
        return g;
    }

    // L07: 上色見熊野座神社 (杉木森林參道 + 青苔石燈籠列 + 穿戶岩)
    function buildL07_Kamishikimi() {
        const g = new THREE.Group();
        const mossStone = new THREE.MeshLambertMaterial({ color: 0x657761, flatShading: true });
        const cedarMat = new THREE.MeshLambertMaterial({ color: 0x1e3f20, flatShading: true });
        const trunkMat = new THREE.MeshLambertMaterial({ color: 0x451a03 });
        const glowMat = new THREE.MeshBasicMaterial({ color: 0xfef08a });

        // 石階參道與兩側石燈籠
        for (let i = 0; i < 4; i++) {
            const z = 0.45 - i * 0.28;
            const y = i * 0.08;
            const step = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.08, 0.26), mossStone);
            step.position.set(0, y + 0.04, z);
            g.add(step);

            [-0.28, 0.28].forEach(xSide => {
                const lantern = new THREE.Group();
                const post = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.04, 0.22, 6), mossStone);
                post.position.y = 0.11;
                const fireBox = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.07, 0.07), glowMat);
                fireBox.position.y = 0.24;
                const cap = new THREE.Mesh(new THREE.ConeGeometry(0.09, 0.07, 6), mossStone);
                cap.position.y = 0.30;
                lantern.add(post, fireBox, cap);
                lantern.position.set(xSide, y, z);
                g.add(lantern);
            });
        }

        // 參天杉木群
        [[-0.48, -0.1], [0.48, -0.1], [-0.42, 0.28], [0.42, 0.28]].forEach(pos => {
            const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.07, 0.55, 6), trunkMat);
            trunk.position.set(pos[0], 0.27, pos[1]);
            const foliage = new THREE.Mesh(new THREE.ConeGeometry(0.26, 0.75, 6), cedarMat);
            foliage.position.set(pos[0], 0.72, pos[1]);
            g.add(trunk, foliage);
        });

        enableShadow(g);
        return g;
    }

    // L08: 高千穗峽谷・真名井瀑布 (柱狀玄武岩雙側絕壁 + 翡翠溪流 + 白色瀑布 + 手划小舟)
    function buildL08_TakachihoGorge() {
        const g = new THREE.Group();
        const basaltMat = new THREE.MeshLambertMaterial({ color: 0x44403c, flatShading: true });
        const riverMat = new THREE.MeshLambertMaterial({ color: 0x0d9488 });
        const waterfallMat = new THREE.MeshBasicMaterial({ color: 0xe0f2fe });
        const boatMat = new THREE.MeshLambertMaterial({ color: 0xd97706 });

        // 翡翠河道
        const river = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.06, 1.25), riverMat);
        river.position.y = 0.03;
        g.add(river);

        // 左右兩側六角柱狀玄武岩絕壁
        for (let i = 0; i < 6; i++) {
            const z = -0.5 + i * 0.20;
            const hL = 0.55 + (i % 3) * 0.12;
            const colL = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.15, hL, 6), basaltMat);
            colL.position.set(-0.38, hL / 2, z);
            const hR = 0.58 + ((i + 1) % 3) * 0.12;
            const colR = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.15, hR, 6), basaltMat);
            colR.position.set(0.38, hR / 2, z);
            g.add(colL, colR);
        }

        // 真名井瀑布水簾
        const fall = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.58, 0.06), waterfallMat);
        fall.position.set(-0.26, 0.30, -0.15);
        fall.rotation.z = -0.15;
        g.add(fall);

        // 峽谷手划小舟
        const boat = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.07, 0.36), boatMat);
        boat.position.set(0.04, 0.08, 0.18);
        g.add(boat);
        g.userData.boat = boat;

        enableShadow(g);
        return g;
    }

    // L09: 宮崎海景渡假區 (高聳海景飯店大樓 + 鳳凰棕櫚樹 + 陽光沙灘陽傘)
    function buildL09_MiyazakiSeagaia() {
        const g = new THREE.Group();
        const hotelMat = new THREE.MeshLambertMaterial({ color: 0xf8fafc, flatShading: true });
        const glassMat = new THREE.MeshLambertMaterial({ color: 0x38bdf8 });
        const trunkMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
        const palmMat = new THREE.MeshLambertMaterial({ color: 0x4d7c0f, flatShading: true });

        // 海景渡假大樓 (弧形稜柱體)
        const tower = new THREE.Mesh(new THREE.BoxGeometry(0.52, 1.05, 0.28), hotelMat);
        tower.position.set(0, 0.52, -0.15);
        const windows = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.88, 0.30), glassMat);
        windows.position.set(0, 0.54, -0.15);
        g.add(tower, windows);

        // 南國鳳凰棕櫚樹 x2
        [-0.45, 0.45].forEach(x => {
            const palm = new THREE.Group();
            const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.05, 0.52, 6), trunkMat);
            trunk.position.y = 0.26;
            palm.add(trunk);
            for (let k = 0; k < 5; k++) {
                const leaf = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.32, 4), palmMat);
                leaf.position.y = 0.52;
                leaf.rotation.z = 1.1;
                leaf.rotation.y = (k / 5) * Math.PI * 2;
                palm.add(leaf);
            }
            palm.position.set(x, 0, 0.22);
            g.add(palm);
        });

        enableShadow(g);
        return g;
    }

    // L10: 青島神社・鬼之洗衣板 (波狀海蝕岩盤 + 海上朱紅鳥居 + 彌生橋 + 黃色小嘟嘟車)
    function buildL10_AoshimaShrine() {
        const g = new THREE.Group();
        const rockMat = new THREE.MeshLambertMaterial({ color: 0x57534e, flatShading: true });

        // 鬼之洗衣板波狀條紋岩盤
        for (let i = -3; i <= 3; i++) {
            const ridge = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.07, 0.08), rockMat);
            ridge.position.set(0, 0.035, i * 0.13);
            g.add(ridge);
        }

        // 海中朱紅鳥居
        const torii = createToriiGate(0.78, 0xdc2626);
        torii.position.set(0, 0.06, 0);
        g.add(torii);

        // 青島黃色嘟嘟車 (Tuk-tuk)
        const tuktuk = new THREE.Mesh(
            new THREE.BoxGeometry(0.22, 0.16, 0.14),
            new THREE.MeshLambertMaterial({ color: 0xfacc15 })
        );
        tuktuk.position.set(-0.42, 0.12, 0.32);
        g.add(tuktuk);

        enableShadow(g);
        return g;
    }

    // L11: 日南太陽花園・摩艾石像 (翠綠山坡上的 5 座經典復活節島摩艾像)
    function buildL11_SunMesseMoai() {
        const g = new THREE.Group();
        const stoneMat = new THREE.MeshLambertMaterial({ color: 0xa8a29e, flatShading: true });
        const pukaoMat = new THREE.MeshLambertMaterial({ color: 0x991b1b, flatShading: true });
        const baseMat = new THREE.MeshLambertMaterial({ color: 0x78716c });

        const platform = new THREE.Mesh(new THREE.BoxGeometry(1.35, 0.10, 0.42), baseMat);
        platform.position.y = 0.05;
        g.add(platform);

        for (let i = -2; i <= 2; i++) {
            const moai = new THREE.Group();
            const h = 0.42 + (2 - Math.abs(i)) * 0.04;
            const torso = new THREE.Mesh(new THREE.BoxGeometry(0.18, h * 0.55, 0.16), stoneMat);
            torso.position.y = 0.10 + h * 0.27;
            const head = new THREE.Mesh(new THREE.BoxGeometry(0.15, h * 0.52, 0.17), stoneMat);
            head.position.y = 0.10 + h * 0.72;
            const brow = new THREE.Mesh(new THREE.BoxGeometry(0.17, 0.04, 0.19), stoneMat);
            brow.position.set(0, 0.10 + h * 0.85, 0.02);
            const nose = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.12, 0.06), stoneMat);
            nose.position.set(0, 0.10 + h * 0.72, 0.09);
            moai.add(torso, head, brow, nose);

            if (i === 0 || i === 1) {
                // 紅石髮髻 Pukao
                const hat = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.08, 8), pukaoMat);
                hat.position.y = 0.10 + h * 1.02;
                moai.add(hat);
            }
            moai.position.x = i * 0.24;
            g.add(moai);
        }

        enableShadow(g);
        return g;
    }

    // L12: 鵜戶神宮 (海蝕洞懸崖 + 朱紅社殿 + 海中靈石龜石與運玉繩圈)
    function buildL12_UdoJingu() {
        const g = new THREE.Group();
        const cliffMat = new THREE.MeshLambertMaterial({ color: 0x78553a, flatShading: true });
        const redMat = new THREE.MeshLambertMaterial({ color: 0xdc2626, flatShading: true });
        const ropeMat = new THREE.MeshLambertMaterial({ color: 0xfacc15 });

        // 海蝕洞拱門懸崖
        const caveArch = new THREE.Mesh(new THREE.TorusGeometry(0.45, 0.18, 6, 10, Math.PI), cliffMat);
        caveArch.position.set(0, 0.08, -0.12);
        g.add(caveArch);

        // 洞內朱紅本殿
        const shrine = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.28, 0.28), redMat);
        shrine.position.set(0, 0.14, -0.12);
        g.add(shrine);

        // 海中龜石與注連繩圈
        const turtleRock = new THREE.Mesh(new THREE.DodecahedronGeometry(0.22, 0), cliffMat);
        turtleRock.scale.set(1.2, 0.5, 1.0);
        turtleRock.position.set(0.32, 0.06, 0.38);
        const ropeRing = new THREE.Mesh(new THREE.TorusGeometry(0.09, 0.02, 6, 12), ropeMat);
        ropeRing.rotation.x = Math.PI / 2;
        ropeRing.position.set(0.32, 0.16, 0.38);
        g.add(turtleRock, ropeRing);

        enableShadow(g);
        return g;
    }

    // L13: 鹿兒島天文館・聖誕燈飾市集 (拱廊商店街 + 巨型發光聖誕樹 + 彩色燈串 + 白熊冰招牌)
    function buildL13_TenmonkanXmas() {
        const g = new THREE.Group();
        const arcadeMat = new THREE.MeshLambertMaterial({ color: 0xfef3c7 });
        const roofMat = new THREE.MeshLambertMaterial({ color: 0xb91c1c });
        const pineMat = new THREE.MeshLambertMaterial({ color: 0x15803d, flatShading: true });
        const goldMat = new THREE.MeshBasicMaterial({ color: 0xfacc15 });

        // 天文館拱廊建築
        const bldg = new THREE.Mesh(new THREE.BoxGeometry(0.78, 0.48, 0.45), arcadeMat);
        bldg.position.set(-0.22, 0.24, -0.15);
        const awning = new THREE.Mesh(new THREE.BoxGeometry(0.84, 0.10, 0.52), roofMat);
        awning.position.set(-0.22, 0.50, -0.15);
        g.add(bldg, awning);

        // 巨型聖誕樹
        const treeGroup = new THREE.Group();
        [0.42, 0.34, 0.24].forEach((r, idx) => {
            const cone = new THREE.Mesh(new THREE.ConeGeometry(r, 0.38, 8), pineMat);
            cone.position.y = 0.22 + idx * 0.25;
            treeGroup.add(cone);
        });
        const star = new THREE.Mesh(new THREE.OctahedronGeometry(0.11, 0), goldMat);
        star.position.y = 0.96;
        treeGroup.add(star);

        // 聖誕樹閃爍彩燈球
        const bulbs = [];
        const bulbColors = [0xef4444, 0xfacc15, 0x38bdf8, 0xf472b6, 0x4ade80];
        for (let i = 0; i < 10; i++) {
            const ang = (i / 10) * Math.PI * 4;
            const h = 0.22 + (i / 10) * 0.58;
            const rad = 0.36 * (1 - (i / 10) * 0.55);
            const bMat = new THREE.MeshBasicMaterial({ color: bulbColors[i % bulbColors.length] });
            const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.045, 6, 6), bMat);
            bulb.position.set(Math.cos(ang) * rad, h, Math.sin(ang) * rad);
            treeGroup.add(bulb);
            bulbs.push(bulb);
        }
        treeGroup.position.set(0.42, 0, 0.20);
        g.add(treeGroup);
        g.userData.xmasBulbs = bulbs;
        g.userData.xmasStar = star;

        enableShadow(g);
        return g;
    }

    // L14: 仙巖園 (島津別邸書院 + 反射爐石造遺構 + 翠竹林)
    function buildL14_SenganEn() {
        const g = new THREE.Group();
        const woodMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
        const roofMat = new THREE.MeshLambertMaterial({ color: 0x334155, flatShading: true });
        const bambooMat = new THREE.MeshLambertMaterial({ color: 0x4d7c0f });

        const villa = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.28, 0.42), woodMat);
        villa.position.set(-0.1, 0.14, 0);
        const roof = new THREE.Mesh(new THREE.ConeGeometry(0.52, 0.22, 4), roofMat);
        roof.rotation.y = Math.PI / 4;
        roof.position.set(-0.1, 0.38, 0);
        g.add(villa, roof);

        // 江南竹林
        for (let i = 0; i < 5; i++) {
            const stalk = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.03, 0.65, 6), bambooMat);
            stalk.position.set(0.35 + (i % 2) * 0.1, 0.32, -0.2 + i * 0.1);
            g.add(stalk);
        }

        enableShadow(g);
        return g;
    }

    // L15: 櫻島活火山・溶岩足湯 (雙峰御岳火山錐 + 持續噴發火山灰煙雲 + 岸邊赤褐溶岩足湯亭)
    function buildL15_SakurajimaVolcano() {
        const g = new THREE.Group();
        const lavaMat = new THREE.MeshLambertMaterial({ color: 0x443730, flatShading: true });
        const ashMat = new THREE.MeshLambertMaterial({ color: 0x57534e, flatShading: true });
        const snowMat = new THREE.MeshLambertMaterial({ color: 0xe2e8f0, flatShading: true });
        const glowLava = new THREE.MeshBasicMaterial({ color: 0xf97316 });

        // 北岳與南岳雙峰火山體
        const mainPeak = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 1.15, 1.32, 9), lavaMat);
        mainPeak.position.y = 0.66;
        const subPeak = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.78, 0.98, 8), ashMat);
        subPeak.position.set(0.35, 0.49, 0.18);
        const snowCrown = new THREE.Mesh(new THREE.CylinderGeometry(0.44, 0.68, 0.28, 9), snowMat);
        snowCrown.position.y = 1.12;
        const craterGlow = new THREE.Mesh(new THREE.CylinderGeometry(0.30, 0.26, 0.06, 9), glowLava);
        craterGlow.position.y = 1.33;
        g.add(mainPeak, subPeak, snowCrown, craterGlow);

        // 火山灰濃煙球團 (持續往上飄動)
        const puffs = [];
        const smokeMat = new THREE.MeshLambertMaterial({ color: 0xd6d3d1, transparent: true, opacity: 0.80 });
        for (let i = 0; i < 6; i++) {
            const p = new THREE.Mesh(new THREE.DodecahedronGeometry(0.20 + i * 0.05, 0), smokeMat.clone());
            p.position.set((Math.random() - 0.5) * 0.2, 1.45 + i * 0.30, (Math.random() - 0.5) * 0.2);
            p.userData = { baseY: 1.40, offset: i * 0.17 };
            g.add(p);
            puffs.push(p);
        }
        g.userData.puffs = puffs;

        enableShadow(g);
        return g;
    }

    // L16: 霧島神宮 (國寶大鳥居 + 朱紅社殿 + 老杉木參道)
    function buildL16_KirishimaJingu() {
        const g = new THREE.Group();
        const redMat = new THREE.MeshLambertMaterial({ color: 0xb91c1c, flatShading: true });
        const roofMat = new THREE.MeshLambertMaterial({ color: 0x1e293b, flatShading: true });
        const goldMat = new THREE.MeshLambertMaterial({ color: 0xfacc15 });

        // 國寶朱紅社殿
        const honden = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.38, 0.46), redMat);
        honden.position.set(0, 0.19, -0.20);
        const roof = new THREE.Mesh(new THREE.ConeGeometry(0.58, 0.30, 4), roofMat);
        roof.rotation.y = Math.PI / 4;
        roof.position.set(0, 0.50, -0.20);
        const goldTrim = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.08, 0.48), goldMat);
        goldTrim.position.set(0, 0.36, -0.20);
        g.add(honden, roof, goldTrim);

        // 前方迎賓大鳥居
        const torii = createToriiGate(0.95, 0xdc2626);
        torii.position.set(0, 0, 0.38);
        g.add(torii);

        enableShadow(g);
        return g;
    }

    // L17: 人吉百年炭火鰻魚・青井阿蘇神社 (白壁土藏鰻魚老舖 + 茅草屋頂樓門 + 球磨川石橋)
    function buildL17_HitoyoshiUnagi() {
        const g = new THREE.Group();
        const whiteWall = new THREE.MeshLambertMaterial({ color: 0xfafaf9 });
        const darkWood = new THREE.MeshLambertMaterial({ color: 0x292524 });
        const thatchRoof = new THREE.MeshLambertMaterial({ color: 0x713f12, flatShading: true });
        const norenRed = new THREE.MeshLambertMaterial({ color: 0xdc2626 });

        // 上村百年鰻魚老舖町家
        const shop = new THREE.Mesh(new THREE.BoxGeometry(0.64, 0.38, 0.44), whiteWall);
        shop.position.set(-0.18, 0.19, 0);
        const timber = new THREE.Mesh(new THREE.BoxGeometry(0.66, 0.14, 0.46), darkWood);
        timber.position.set(-0.18, 0.08, 0);
        const roof = new THREE.Mesh(new THREE.ConeGeometry(0.52, 0.24, 4), thatchRoof);
        roof.rotation.y = Math.PI / 4;
        roof.position.set(-0.18, 0.48, 0);

        // 紅色「うなぎ」暖簾
        const noren = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.12, 0.04), norenRed);
        noren.position.set(-0.18, 0.22, 0.23);
        g.add(shop, timber, roof, noren);

        // 炭火烤鰻魚香氣白煙
        const smoke = [];
        const sMat = new THREE.MeshBasicMaterial({ color: 0xfef3c7, transparent: true, opacity: 0.65 });
        for (let i = 0; i < 3; i++) {
            const p = new THREE.Mesh(new THREE.SphereGeometry(0.08 + i * 0.02, 6, 6), sMat.clone());
            p.position.set(0.05, 0.55 + i * 0.16, 0);
            p.userData = { baseY: 0.52, offset: i * 0.3 };
            g.add(p);
            smoke.push(p);
        }
        g.userData.puffs = smoke;

        enableShadow(g);
        return g;
    }

    const BUILDERS = {
        L01: buildL01_Airport,
        L02: buildL02_KumamotoCastle,
        L03: buildL03_Suizenji,
        L04: buildL04_AsoCrater,
        L05: buildL05_Daikanbo,
        L06: buildL06_KurokawaOnsen,
        L07: buildL07_Kamishikimi,
        L08: buildL08_TakachihoGorge,
        L09: buildL09_MiyazakiSeagaia,
        L10: buildL10_AoshimaShrine,
        L11: buildL11_SunMesseMoai,
        L12: buildL12_UdoJingu,
        L13: buildL13_TenmonkanXmas,
        L14: buildL14_SenganEn,
        L15: buildL15_SakurajimaVolcano,
        L16: buildL16_KirishimaJingu,
        L17: buildL17_HitoyoshiUnagi
    };

    function createLandmarkByCode(code) {
        const fn = BUILDERS[code];
        return fn ? fn() : new THREE.Group();
    }

    function buildAllLandmarks(parent, landmarksData, sampleGroundY, roadCurve) {
        const landmarkGroup = new THREE.Group();
        const animatedLandmarks = [];
        const landmarkMap = {};

        // 預先取樣道路中心線，確保地標模型不會直接蓋在馬路正中央造成小巴與人物穿模
        const roadSamples = [];
        if (roadCurve) {
            for (let i = 0; i <= 200; i++) {
                roadSamples.push(roadCurve.getPointAt(i / 200));
            }
        }

        // 依據不同景點類型給予適當放大比例（火山適度收斂並退至道路北側後方，絕不擋住前方人物）
        const SCALE_MAP = {
            L01: 1.62, // 熊本機場（起點地標放大）
            L02: 1.60, // 熊本城（主力地標放大）
            L03: 1.38, // 水前寺
            L04: 1.18, // 阿蘇中岳火山口（收斂尺寸並退居車道後方，避免火山錐擋住人物）
            L05: 1.40, // 大觀峰
            L06: 1.50, // 黑川溫泉山彥旅館
            L07: 1.42, // 上色見神社
            L08: 1.52, // 高千穗峽谷
            L09: 1.48, // 宮崎海景渡假區
            L10: 1.45, // 青島神社
            L11: 1.50, // 日南摩艾石像
            L12: 1.45, // 鵜戶神宮
            L13: 1.58, // 鹿兒島天文館聖誕市集
            L14: 1.42, // 仙巖園
            L15: 1.18, // 櫻島活火山（退居渡輪碼頭後方，不遮擋人物）
            L16: 1.52, // 霧島神宮
            L17: 1.50  // 人吉百年鰻魚
        };

        landmarksData.forEach(item => {
            const meshGroup = createLandmarkByCode(item.code);
            const scaleVal = SCALE_MAP[item.code] || 1.45;
            meshGroup.scale.setScalar(scaleVal);

            let lx = item.x;
            let lz = item.z;

            // 將火山與景點統一退往車道北側後方（遠離鏡頭的 -Z 側），而阿蘇火山直接坐落於站點旁讓角色登上山頂！
            if (item.code === 'L15') {
                lx = -2.46;
                lz = 9.60;
            } else if (item.code === 'L04') {
                lx = item.x;
                lz = item.z - 0.32;
            } else if (roadSamples.length > 0) {
                let nearestPt = null;
                let minD = 999;
                for (let i = 0; i < roadSamples.length; i++) {
                    const d = Math.hypot(lx - roadSamples[i].x, lz - roadSamples[i].z);
                    if (d < minD) {
                        minD = d;
                        nearestPt = roadSamples[i];
                    }
                }
                const minClearance = 1.32;
                if (nearestPt && minD < minClearance) {
                    let dx = lx - nearestPt.x;
                    let dz = lz - nearestPt.z;
                    const len = Math.hypot(dx, dz);
                    if (len < 0.08) {
                        dx = (nearestPt.x >= 0) ? 0.45 : -0.45;
                        dz = -0.95;
                    }
                    const norm = Math.hypot(dx, dz);
                    lx = nearestPt.x + (dx / norm) * minClearance;
                    lz = nearestPt.z + (dz / norm) * minClearance;
                }
            }

            // 根據真實地形取樣高度貼合台地表面
            let baseY = sampleGroundY ? sampleGroundY(lx, lz) : 0.88;
            if (item.code === 'L15') baseY = Math.max(0.72, baseY - 0.04);
            else baseY += 0.012; // 微微墊高 1.2cm，確保地標基座、跑道、石垣永不被草地微凸起覆蓋

            meshGroup.position.set(lx, baseY, lz);
            item.renderX = lx;
            item.renderZ = lz;
            item.renderY = baseY;
            item.scaleVal = scaleVal;
            meshGroup.userData.landmarkInfo = item;
            landmarkGroup.add(meshGroup);
            animatedLandmarks.push(meshGroup);
            landmarkMap[item.id] = meshGroup;
        });

        parent.add(landmarkGroup);
        return { landmarkGroup, animatedLandmarks, landmarkMap };
    }

    function updateLandmarks(animatedLandmarks, elapsed) {
        animatedLandmarks.forEach(lm => {
            // 1. 火山白煙、黑川溫泉蒸氣、人吉烤鰻魚煙霧上升循環
            if (lm.userData.puffs) {
                lm.userData.puffs.forEach((p, idx) => {
                    const cycle = (elapsed * 0.45 + p.userData.offset) % 1.0;
                    p.position.y = p.userData.baseY + cycle * 1.35;
                    const s = 0.7 + cycle * 0.95;
                    p.scale.set(s, s, s);
                    p.material.opacity = (1.0 - cycle) * 0.75;
                });
            }
            // 2. 熊本機場飛機微微起降搖擺
            if (lm.userData.plane) {
                lm.userData.plane.position.y = 0.16 + Math.sin(elapsed * 2.2) * 0.04;
            }
            // 3. 高千穗峽谷小舟搖曳
            if (lm.userData.boat) {
                lm.userData.boat.position.z = 0.15 + Math.sin(elapsed * 1.5) * 0.12;
                lm.userData.boat.rotation.z = Math.sin(elapsed * 2.5) * 0.08;
            }
            // 4. 鹿兒島天文館聖誕樹燈飾閃爍與星星自轉
            if (lm.userData.xmasStar) {
                lm.userData.xmasStar.rotation.y = elapsed * 1.8;
            }
            if (lm.userData.xmasBulbs) {
                lm.userData.xmasBulbs.forEach((b, i) => {
                    const pulse = 0.85 + Math.sin(elapsed * 5.0 + i * 1.1) * 0.25;
                    b.scale.setScalar(pulse);
                });
            }
        });
    }

    window.KyushuIsland.Landmarks = {
        createLandmarkByCode,
        buildAllLandmarks,
        updateLandmarks,
        BUILDERS
    };
})();
