/**
 * portal/characters.js
 * 4 位家族成員精緻 Low-poly 3D 角色模型與豐富動作系統：
 * - C1 阿純 (achun)：可愛妹子、及肩栗色長髮、黃色毛線帽＋白色大毛球、珊瑚粉羽絨外套＋米白圍巾、斜背小相機、拿手機自拍與雀躍揮手
 * - C2 姨丈 (yijhang)：專業司機、帥氣飛行墨鏡、深藍防風夾克＋翻領、手持方向盤/車鑰匙、伸懶腰與比讚
 * - C3 阿姨 (ayee)：和藹婦人、蓬鬆捲髮、暖杏色冬季長大衣＋酒紅圍巾、手提日本伴手禮紙袋、右手拿三色糰子/可樂餅津津有味品嚐＋頭頂冒愛心
 * - C4 阿嚕 (alu)：圓滾滾焦糖棕熊（原創可愛森林棕熊，非熊本熊）、圓耳朵、腮紅、聖誕紅白格紋圍巾、摸圓肚肚與搖擺踏步
 */
(function () {
    window.KyushuIsland = window.KyushuIsland || {};

    const CHARACTER_SPECS = [
        {
            code: 'C1',
            id: 'achun',
            name: '首席導遊 阿純',
            title: '🧭 首席導遊・吃貨睡神',
            badge: '🧭 總策劃導遊・吃飽睡睡飽吃',
            desc: '戴著招牌黃色毛球針織帽的可愛妹子兼首席導遊，一手策劃南九州自駕之旅，隨時隨地活力滿滿又愛香甜補眠！'
        },
        {
            code: 'C2',
            id: 'yijhang',
            name: '榮譽總指揮 姨丈',
            title: '🎩 榮譽總指揮・倒試管大師',
            badge: '🚗 首席掌舵官・沉迷倒試管手遊',
            desc: '戴著墨鏡的榮譽總指揮兼神級老司機，話很少但開車超穩；只要一停車就會默默掏出手機玩「倒試管顏色分類」推理小廢遊！'
        },
        {
            code: 'C3',
            id: 'ayee',
            name: '美食評鑑官 阿姨',
            title: '⭐ 美食評鑑官・餵食總隊長',
            badge: '🍡 尊榮美食品嚐・走到哪聊到哪',
            desc: '最愛跟家人與路人熱情聊天的美食評鑑官，人生使命就是把大家餵得飽飽的，包包裡永遠有掏不完的烤糰子、伴手禮與零食！'
        },
        {
            code: 'C4',
            id: 'alu',
            idAlt: 'alu',
            name: '總務大臣 阿嚕',
            title: '💰 總務大臣・哲學AI熊',
            badge: '🐻 掌櫃導航員・思考熊生',
            desc: '圓滾滾的總務大臣焦糖棕熊，專門掌管帳目與行車導航，偶爾認真思考自己究竟是真熊還是被程式碼操控的 AI！'
        }
    ];

    function enableShadow(obj) {
        obj.traverse(child => {
            if (child.isMesh) {
                // 特殊光效、透明粒子與光環嚴禁投射陰影，否則會在身上產生方形投影！
                if (child.material && child.material.transparent && child.material.opacity === 0) {
                    child.castShadow = false;
                    child.receiveShadow = false;
                } else if (child.geometry && (child.geometry.type === 'PlaneGeometry' || child.geometry.type === 'RingGeometry')) {
                    child.castShadow = false;
                    child.receiveShadow = false;
                } else {
                    child.castShadow = true;
                    child.receiveShadow = true;
                }
            }
        });
    }

    // 建立 C1 阿純 (可愛妹子 + 黃色毛帽 + 及肩髮 + 羽絨衣 + 手機自拍棒)
    function buildC1_Achun() {
        const root = new THREE.Group();
        const skinMat   = new THREE.MeshLambertMaterial({ color: 0xffe4c4 });
        const hairMat   = new THREE.MeshLambertMaterial({ color: 0x5c3a21, flatShading: true });
        const hatMat    = new THREE.MeshLambertMaterial({ color: 0xfacc15, flatShading: true }); // 招牌亮黃毛帽
        const pomMat    = new THREE.MeshLambertMaterial({ color: 0xfffbeb });
        const coatMat   = new THREE.MeshLambertMaterial({ color: 0xfb7185, flatShading: true }); // 甜美珊瑚粉羽絨衣
        const skirtMat  = new THREE.MeshLambertMaterial({ color: 0xfef3c7 });
        const bootMat   = new THREE.MeshLambertMaterial({ color: 0x78350f });
        const scarfMat  = new THREE.MeshLambertMaterial({ color: 0xfef08a });
        const blushMat  = new THREE.MeshBasicMaterial({ color: 0xf43f5e, transparent: true, opacity: 0.55 });
        const eyeMat    = new THREE.MeshBasicMaterial({ color: 0x1e293b });

        // 雙腿與雪靴
        const legL = new THREE.Group();
        legL.position.set(-0.11, 0.28, 0);
        const legMeshL = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.06, 0.26, 8), bootMat);
        legMeshL.position.y = -0.12;
        legL.add(legMeshL);

        const legR = new THREE.Group();
        legR.position.set(0.11, 0.28, 0);
        const legMeshR = legMeshL.clone();
        legR.add(legMeshR);
        root.add(legL, legR);

        // 身體（羽絨外套 + 百褶短裙）
        const torso = new THREE.Group();
        torso.position.y = 0.52;
        const coat = new THREE.Mesh(new THREE.CylinderGeometry(0.20, 0.26, 0.44, 10), coatMat);
        const skirt = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.29, 0.16, 12), skirtMat);
        skirt.position.y = -0.22;
        const scarf = new THREE.Mesh(new THREE.TorusGeometry(0.19, 0.065, 8, 14), scarfMat);
        scarf.rotation.x = Math.PI / 2;
        scarf.position.y = 0.21;
        torso.add(coat, skirt, scarf);
        root.add(torso);

        // 頭部（Q版大頭 + 眨眼雙眸 + 粉嫩腮紅 + 及肩長髮 + 黃色針織毛帽）
        const headGroup = new THREE.Group();
        headGroup.position.y = 0.96;
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.29, 14, 12), skinMat);

        // 雙眸與粉嫩腮紅（眼睛向前微凸 z = 0.275，確保清楚鑲嵌於白皙臉蛋，絕對不被任何帽簷或髮片遮蓋）
        const eyeL = new THREE.Mesh(new THREE.SphereGeometry(0.038, 8, 8), eyeMat);
        eyeL.position.set(-0.095, 0.015, 0.275);
        const eyeR = eyeL.clone();
        eyeR.position.set(0.095, 0.015, 0.275);
        const blushL = new THREE.Mesh(new THREE.CircleGeometry(0.052, 8), blushMat);
        blushL.position.set(-0.16, -0.06, 0.27);
        blushL.rotation.y = -0.35;
        const blushR = new THREE.Mesh(new THREE.CircleGeometry(0.052, 8), blushMat);
        blushR.position.set(0.16, -0.06, 0.27);
        blushR.rotation.y = 0.35;

        // 甜美微微笑嘴型（高於下巴，避免被圍巾遮擋）
        const smile = new THREE.Mesh(
            new THREE.TorusGeometry(0.036, 0.010, 6, 10, Math.PI),
            new THREE.MeshBasicMaterial({ color: 0xe11d48 })
        );
        smile.rotation.x = Math.PI;
        smile.position.set(0, -0.075, 0.28);

        // 栗色秀髮基底（完美對稱包覆後腦、兩側太陽穴與後頸部，徹底消除禿頭空洞！）
        // Three.js 座標：正臉朝向 +Z (phi = 0.50pi)，臉部開口從 0.32pi 到 0.68pi (寬度 0.36pi，精確露出一雙大眼與腮紅)
        // 秀髮從 0.68pi 環繞後腦勺 (1.50pi) 直達 0.32pi (總長 1.64pi)，嚴格左右對稱且完全包覆兩側！
        const hairBase = new THREE.Mesh(
            new THREE.SphereGeometry(0.298, 20, 16, Math.PI * 0.68, Math.PI * 1.64, 0, Math.PI * 0.82),
            hairMat
        );
        hairBase.position.set(0, 0.01, 0);

        // 左右兩側柔順微捲及肩長髮（自然順著臉頰外側垂落至胸前，完全消弭任何木棍違和感，打造甜美日系鮑伯及肩層次）
        const sideHairGeo = new THREE.CylinderGeometry(0.065, 0.088, 0.30, 10, 1, false);
        const sideHairL = new THREE.Mesh(sideHairGeo, hairMat);
        sideHairL.position.set(-0.22, -0.09, 0.10);
        sideHairL.rotation.set(0.10, -0.18, 0.14);

        const sideHairR = new THREE.Mesh(sideHairGeo, hairMat);
        sideHairR.position.set(0.22, -0.09, 0.10);
        sideHairR.rotation.set(0.10, 0.18, -0.14);

        // 後頸溫柔及肩長髮下擺（銜接後頸與米白圍巾，讓整個後腦勺與側面線條飽滿圓潤）
        const backHairLow = new THREE.Mesh(
            new THREE.CylinderGeometry(0.20, 0.25, 0.18, 14, 1, false, Math.PI * 0.75, Math.PI * 1.50),
            hairMat
        );
        backHairLow.position.set(0, -0.14, -0.08);

        // 日系柔和弧度齊瀏海（位於高額頭 y = 0.14~0.19，自然弧度覆蓋額骨，完全在眼睛 y = 0.015 上方，零穿模）
        const bangs = new THREE.Mesh(
            new THREE.CylinderGeometry(0.294, 0.297, 0.065, 14, 1, false, Math.PI * 0.32, Math.PI * 0.36),
            hairMat
        );
        bangs.position.set(0, 0.155, 0.02);
        bangs.rotation.x = 0.12;

        // 招牌亮黃針織毛帽（大號飽滿毛帽，帽簷嚴密包覆壓在秀髮基底之上，一體成型天衣無縫）
        const beanie = new THREE.Mesh(new THREE.SphereGeometry(0.316, 18, 14, 0, Math.PI * 2, 0, Math.PI * 0.54), hatMat);
        beanie.position.set(0, 0.11, -0.02);
        beanie.rotation.x = -0.08;
        const brim = new THREE.Mesh(new THREE.TorusGeometry(0.288, 0.048, 8, 20), hatMat);
        brim.rotation.x = Math.PI / 2 - 0.08;
        brim.position.set(0, 0.13, 0.01);
        const pom = new THREE.Mesh(new THREE.SphereGeometry(0.10, 10, 10), pomMat);
        pom.position.set(0, 0.43, -0.08);

        headGroup.add(head, eyeL, eyeR, blushL, blushR, smile, hairBase, sideHairL, sideHairR, backHairLow, bangs, beanie, brim, pom);
        root.add(headGroup);

        // 左右手臂（左手拿銀色筆電隨時打「物理治療紀錄」、右手拿外帶熱拿鐵咖啡杯）
        const armL = new THREE.Group();
        armL.position.set(-0.25, 0.66, 0);
        const armMeshL = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.05, 0.28, 8), coatMat);
        armMeshL.position.y = -0.11;

        // 隨身銀色筆電 (鍵盤底座 + 掀開的發光螢幕顯示物理治療紀錄表單)
        const laptopGroup = new THREE.Group();
        const silverMat = new THREE.MeshLambertMaterial({ color: 0xcbd5e1 });
        const kbMat     = new THREE.MeshLambertMaterial({ color: 0x334155 });
        const screenGlow= new THREE.MeshBasicMaterial({ color: 0xe0f2fe });
        const chartBar1 = new THREE.MeshBasicMaterial({ color: 0x0284c7 });
        const chartBar2 = new THREE.MeshBasicMaterial({ color: 0x10b981 });

        const lapBase = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.018, 0.16), silverMat);
        const lapKb   = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.020, 0.11), kbMat);
        lapKb.position.y = 0.002;
        const lapScreenGroup = new THREE.Group();
        lapScreenGroup.position.set(0, 0.01, -0.075);
        lapScreenGroup.rotation.x = -0.35; // 微仰角掀開螢幕
        const lapLid = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.15, 0.014), silverMat);
        lapLid.position.y = 0.075;
        const lapDisp = new THREE.Mesh(new THREE.BoxGeometry(0.19, 0.12, 0.016), screenGlow);
        lapDisp.position.set(0, 0.075, 0.002);
        const ptHeader = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.022, 0.018), chartBar1);
        ptHeader.position.set(0, 0.115, 0.004);
        const ptRow1 = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.016, 0.018), chartBar2);
        ptRow1.position.set(-0.01, 0.082, 0.004);
        const ptRow2 = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.016, 0.018), chartBar1);
        ptRow2.position.set(-0.02, 0.052, 0.004);
        lapScreenGroup.add(lapLid, lapDisp, ptHeader, ptRow1, ptRow2);

        laptopGroup.add(lapBase, lapKb, lapScreenGroup);
        laptopGroup.position.set(0.06, -0.22, 0.13);
        laptopGroup.rotation.x = 0.45;
        armL.add(armMeshL, laptopGroup);

        const armR = new THREE.Group();
        armR.position.set(0.25, 0.66, 0);
        const armMeshR = armMeshL.clone();
        // 外帶咖啡廳熱拿鐵杯 (白杯身 + 牛皮紙隔熱杯套 + 深棕杯蓋)
        const cupGroup = new THREE.Group();
        const cupBody = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.032, 0.11, 8), pomMat);
        const cupSleeve = new THREE.Mesh(new THREE.CylinderGeometry(0.044, 0.038, 0.045, 8), new THREE.MeshLambertMaterial({ color: 0xb45309 }));
        const cupLid = new THREE.Mesh(new THREE.CylinderGeometry(0.046, 0.045, 0.02, 8), bootMat);
        cupLid.position.y = 0.06;
        cupGroup.add(cupBody, cupSleeve, cupLid);
        cupGroup.position.set(0, -0.23, 0.08);
        cupGroup.rotation.x = -0.45;
        armR.add(armMeshR, cupGroup);
        root.add(armL, armR);

        // 阿純落單追車專屬座騎：科幻發光飛碟 (UFO Flying Saucer，預設隱藏，被落下車時自動召喚開飛碟狂追！)
        const ufoGroup = new THREE.Group();
        ufoGroup.position.y = 0.34;
        const ufoMetalMat = new THREE.MeshLambertMaterial({ color: 0x94a3b8, flatShading: true });
        const ufoRimMat   = new THREE.MeshLambertMaterial({ color: 0x475569, flatShading: true });
        const ufoDomeMat  = new THREE.MeshPhongMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.42, shininess: 90 });
        const ufoBeamMat  = new THREE.MeshBasicMaterial({ color: 0x22d3ee, transparent: true, opacity: 0.30, side: THREE.DoubleSide });
        const ufoBulbMat1 = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
        const ufoBulbMat2 = new THREE.MeshBasicMaterial({ color: 0xf43f5e });

        const saucerTop = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.58, 0.12, 16), ufoMetalMat);
        const saucerBot = new THREE.Mesh(new THREE.CylinderGeometry(0.58, 0.24, 0.10, 16), ufoRimMat);
        saucerBot.position.y = -0.10;
        const saucerTorus = new THREE.Mesh(new THREE.TorusGeometry(0.57, 0.04, 8, 20), new THREE.MeshBasicMaterial({ color: 0x38bdf8 }));
        saucerTorus.rotation.x = Math.PI / 2;
        saucerTorus.position.y = -0.04;

        // 透明環形座艙罩
        const cockpitGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.36, 0.18, 16, 1, true), ufoDomeMat);
        cockpitGlass.position.y = 0.12;

        // 底部反重力推進光束
        const tractorBeam = new THREE.Mesh(new THREE.ConeGeometry(0.38, 0.36, 14, 1, true), ufoBeamMat);
        tractorBeam.position.y = -0.28;

        // 飛碟外圈 8 顆旋轉霓虹燈
        const ufoSpinRing = new THREE.Group();
        for (let i = 0; i < 8; i++) {
            const ang = (i / 8) * Math.PI * 2;
            const bulb = new THREE.Mesh(
                new THREE.SphereGeometry(0.052, 8, 8),
                (i % 2 === 0) ? ufoBulbMat1 : ufoBulbMat2
            );
            bulb.position.set(Math.cos(ang) * 0.58, -0.03, Math.sin(ang) * 0.58);
            ufoSpinRing.add(bulb);
        }

        ufoGroup.add(saucerTop, saucerBot, saucerTorus, cockpitGlass, tractorBeam, ufoSpinRing);
        ufoGroup.visible = false;
        root.add(ufoGroup);

        // 阿純打紀錄時自動變出折疊露營桌椅 (Camping Desk & Workstation)
        const campingDeskGroup = new THREE.Group();
        const woodMat = new THREE.MeshLambertMaterial({ color: 0x9a3412, flatShading: true }); // 溫暖原木桌板
        const darkFrameMat = new THREE.MeshLambertMaterial({ color: 0x1e293b }); // 鋁合金折疊骨架
        const canvasMat = new THREE.MeshLambertMaterial({ color: 0x3f6212, flatShading: true }); // 戶外露營帆布

        // 1. 折疊露營桌 (大幅加大為 0.82x0.46 寬敞大木桌，擺放筆電、外帶熱咖啡與病歷板夾)
        const tableGroup = new THREE.Group();
        tableGroup.position.set(0, 0, 0.35);
        const tableTop = new THREE.Mesh(new THREE.BoxGeometry(0.82, 0.026, 0.46), woodMat);
        tableTop.position.y = 0.34;

        // 蛋捲木紋凹槽裝飾
        for (let ix = -3; ix <= 3; ix++) {
            const groove = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.028, 0.45), darkFrameMat);
            groove.position.set(ix * 0.11, 0.34, 0);
            tableGroup.add(groove);
        }

        // 鋁合金四角支架
        [[-0.35, -0.18], [0.35, -0.18], [-0.35, 0.18], [0.35, 0.18]].forEach(p => {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, 0.34, 6), darkFrameMat);
            leg.position.set(p[0], 0.17, p[1]);
            tableGroup.add(leg);
        });

        // 桌面配件 1: 銀色 MacBook 筆電 (螢幕轉軸位於遠端 +Z，螢幕與 SOAP 醫療病歷面板正面朝向阿純 -Z！)
        const laptop = new THREE.Group();
        laptop.position.set(-0.14, 0.353, -0.02);

        // 機身底座 (精準貼合桌面，鍵盤靠向阿純側)
        const lBase = new THREE.Mesh(
            new THREE.BoxGeometry(0.25, 0.012, 0.18),
            new THREE.MeshLambertMaterial({ color: 0xcbd5e1 })
        );
        lBase.position.set(0, 0.006, 0);

        // 巧控鍵盤區 (黑色鍵帽凹槽，靠近阿純操作側 -Z)
        const lKeyboard = new THREE.Mesh(
            new THREE.BoxGeometry(0.21, 0.006, 0.095),
            new THREE.MeshLambertMaterial({ color: 0x1e293b })
        );
        lKeyboard.position.set(0, 0.012, -0.005);

        // 巧控觸控板 (最靠近阿純前端手腕處)
        const lTrackpad = new THREE.Mesh(
            new THREE.BoxGeometry(0.08, 0.004, 0.045),
            new THREE.MeshLambertMaterial({ color: 0x94a3b8 })
        );
        lTrackpad.position.set(0, 0.012, -0.062);

        laptop.add(lBase, lKeyboard, lTrackpad);

        // 筆電螢幕轉軸組 (鉸鏈位於遠離阿純的遠端 +Z，掀開面向阿純視線)
        const screenGroup = new THREE.Group();
        screenGroup.position.set(0, 0.010, 0.082);
        screenGroup.rotation.x = 0.28; // 向外微傾仰角，讓螢幕正面對準阿純視線

        // 螢幕外殼背蓋 (銀灰外殼，朝向遠端桌外 +Z 方向)
        const lLid = new THREE.Mesh(
            new THREE.BoxGeometry(0.25, 0.165, 0.010),
            new THREE.MeshLambertMaterial({ color: 0x64748b })
        );
        lLid.position.set(0, 0.0825, 0.005);

        // 外殼 Apple 經典發光標誌 (朝向外部 +Z)
        const appleLogo = new THREE.Mesh(
            new THREE.CircleGeometry(0.018, 12),
            new THREE.MeshBasicMaterial({ color: 0xffffff })
        );
        appleLogo.position.set(0, 0.085, 0.011);
        screenGroup.add(lLid, appleLogo);

        // 螢幕面板 (Display 面朝 -Z，正對阿純雙眼！)
        const lDisplay = new THREE.Mesh(
            new THREE.PlaneGeometry(0.22, 0.135),
            new THREE.MeshBasicMaterial({ color: 0x0f172a })
        );
        lDisplay.position.set(0, 0.0825, -0.001);
        lDisplay.rotation.y = Math.PI; // 旋轉 180 度讓正面對準阿純
        screenGroup.add(lDisplay);

        // 物理治療 SOAP 系統 UI 面板 (正對阿純)
        const uiHeader = new THREE.Mesh(
            new THREE.PlaneGeometry(0.19, 0.022),
            new THREE.MeshBasicMaterial({ color: 0x0284c7 })
        );
        uiHeader.position.set(0, 0.130, -0.002);
        uiHeader.rotation.y = Math.PI;

        const uiVital = new THREE.Mesh(
            new THREE.PlaneGeometry(0.17, 0.016),
            new THREE.MeshBasicMaterial({ color: 0x10b981 })
        );
        uiVital.position.set(-0.01, 0.096, -0.002);
        uiVital.rotation.y = Math.PI;

        const uiLine1 = new THREE.Mesh(
            new THREE.PlaneGeometry(0.14, 0.013),
            new THREE.MeshBasicMaterial({ color: 0x38bdf8 })
        );
        uiLine1.position.set(-0.025, 0.068, -0.002);
        uiLine1.rotation.y = Math.PI;

        const uiLine2 = new THREE.Mesh(
            new THREE.PlaneGeometry(0.12, 0.013),
            new THREE.MeshBasicMaterial({ color: 0xa855f7 })
        );
        uiLine2.position.set(-0.035, 0.044, -0.002);
        uiLine2.rotation.y = Math.PI;

        screenGroup.add(uiHeader, uiVital, uiLine1, uiLine2);
        laptop.add(screenGroup);
        tableGroup.add(laptop);

        // 桌面配件 2: 外帶熱拿鐵 (牛皮紙隔熱套 + 黑色杯蓋)
        const coffee = new THREE.Group();
        coffee.position.set(0.25, 0.355, 0.08);
        const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.038, 0.030, 0.11, 10), new THREE.MeshLambertMaterial({ color: 0xfafaf9 }));
        cup.position.y = 0.055;
        const sleeve = new THREE.Mesh(new THREE.CylinderGeometry(0.039, 0.035, 0.05, 10), new THREE.MeshLambertMaterial({ color: 0xb45309 }));
        sleeve.position.y = 0.055;
        const lid = new THREE.Mesh(new THREE.CylinderGeometry(0.040, 0.040, 0.018, 10), new THREE.MeshLambertMaterial({ color: 0x1e293b }));
        lid.position.y = 0.112;
        coffee.add(cup, sleeve, lid);
        tableGroup.add(coffee);

        // 桌面配件 3: 物理治療 SOAP 評估病歷板夾
        const clipboard = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.010, 0.14), new THREE.MeshLambertMaterial({ color: 0xfef08a }));
        clipboard.position.set(0.16, 0.355, -0.08);
        clipboard.rotation.y = 0.18;
        tableGroup.add(clipboard);

        tableGroup.add(tableTop);

        // 2. 折疊露營椅 (置於阿純身下)
        const chairGroup = new THREE.Group();
        chairGroup.position.set(0, 0, -0.04);
        const chairSeat = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.025, 0.28), canvasMat);
        chairSeat.position.y = 0.20;
        const chairBack = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.28, 0.025), canvasMat);
        chairBack.position.set(0, 0.32, -0.13);
        chairBack.rotation.x = -0.15;
        // X 型椅腳骨架
        const legF1 = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.26, 6), darkFrameMat);
        legF1.position.set(-0.13, 0.10, 0);
        legF1.rotation.z = 0.25;
        const legF2 = legF1.clone();
        legF2.position.x = 0.13;
        legF2.rotation.z = -0.25;
        chairGroup.add(chairSeat, chairBack, legF1, legF2);

        campingDeskGroup.add(tableGroup, chairGroup);
        campingDeskGroup.scale.setScalar(0.001);
        campingDeskGroup.visible = false;
        root.add(campingDeskGroup);

        root.userData = {
            role: 'achun',
            legL, legR, armL, armR, headGroup, torso,
            ufoGroup, ufoSpinRing, tractorBeam,
            campingDeskGroup,
            laptopGroup,
            cupGroup,
            deskScale: 0,
            eyes: [eyeL, eyeR],
            jumping: 0,
            actionPhase: Math.random() * 10
        };
        enableShadow(root);
        return root;
    }

    // 建立 C2 姨丈 (戴墨鏡的專業司機 + 飛行夾克 + 方向盤/車鑰匙)
    function buildC2_Yijhang() {
        const root = new THREE.Group();
        const skinMat   = new THREE.MeshLambertMaterial({ color: 0xf5d0a9 });
        const jacketMat = new THREE.MeshLambertMaterial({ color: 0x1e3a8a, flatShading: true }); // 深藍專業駕駛夾克
        const collarMat = new THREE.MeshLambertMaterial({ color: 0xfef3c7 }); // 羊毛翻領
        const pantsMat  = new THREE.MeshLambertMaterial({ color: 0x334155 });
        const hairMat   = new THREE.MeshLambertMaterial({ color: 0x1e293b, flatShading: true });
        const shadeMat  = new THREE.MeshBasicMaterial({ color: 0x090d16 });
        const goldMat   = new THREE.MeshBasicMaterial({ color: 0xfacc15 });

        // 雙腿
        const legL = new THREE.Group();
        legL.position.set(-0.12, 0.30, 0);
        const legMeshL = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.065, 0.30, 8), pantsMat);
        legMeshL.position.y = -0.14;
        legL.add(legMeshL);

        const legR = new THREE.Group();
        legR.position.set(0.12, 0.30, 0);
        legR.add(legMeshL.clone());
        root.add(legL, legR);

        // 身體（挺拔飛行夾克 + 翻領 + 司機領帶徽章）
        const torso = new THREE.Group();
        torso.position.y = 0.56;
        const body = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.25, 0.48, 10), jacketMat);
        const collar = new THREE.Mesh(new THREE.TorusGeometry(0.20, 0.055, 7, 12), collarMat);
        collar.rotation.x = Math.PI / 2;
        collar.position.y = 0.22;
        const badge = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.05, 0.02), goldMat);
        badge.position.set(0.10, 0.10, 0.24);
        torso.add(body, collar, badge);
        root.add(torso);

        // 頭部（利落短髮 + 帥氣雙鏡片金屬框飛行墨鏡 + 自信笑容）
        const headGroup = new THREE.Group();
        headGroup.position.y = 1.00;
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.28, 14, 12), skinMat);
        const hair = new THREE.Mesh(new THREE.SphereGeometry(0.295, 12, 10, 0, Math.PI * 2, 0, Math.PI * 0.52), hairMat);
        hair.rotation.x = -0.18;
        hair.position.y = 0.03;

        // 帥氣墨鏡 (雙鏡片 + 金色鼻橋)
        const lensL = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.10, 0.05), shadeMat);
        lensL.position.set(-0.10, 0.03, 0.26);
        const lensR = lensL.clone();
        lensR.position.set(0.10, 0.03, 0.26);
        const bridge = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.022, 0.055), goldMat);
        bridge.position.set(0, 0.06, 0.26);

        headGroup.add(head, hair, lensL, lensR, bridge);
        root.add(headGroup);

        // 左右手（左手拿手機玩「彩色倒試管益智小遊戲」、右手握方向盤/車鑰匙）
        const armL = new THREE.Group();
        armL.position.set(-0.28, 0.70, 0);
        const armMeshL = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.055, 0.30, 8), jacketMat);
        armMeshL.position.y = -0.12;

        // 姨丈的智慧型手機（螢幕顯示紅、藍、黃三支彩色試管！）
        const puzzlePhone = new THREE.Group();
        const phoneBody = new THREE.Mesh(
            new THREE.BoxGeometry(0.09, 0.15, 0.022),
            new THREE.MeshBasicMaterial({ color: 0x1e293b })
        );
        const phoneScreen = new THREE.Mesh(
            new THREE.BoxGeometry(0.076, 0.13, 0.025),
            new THREE.MeshBasicMaterial({ color: 0x0f172a })
        );
        // 螢幕上的三支彩色小試管液體條
        const tube1 = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.075, 0.028), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
        tube1.position.set(-0.02, -0.01, 0);
        const tube2 = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.075, 0.028), new THREE.MeshBasicMaterial({ color: 0x38bdf8 }));
        tube2.position.set(0, -0.01, 0);
        const tube3 = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.075, 0.028), new THREE.MeshBasicMaterial({ color: 0xfacc15 }));
        tube3.position.set(0.02, -0.01, 0);
        puzzlePhone.add(phoneBody, phoneScreen, tube1, tube2, tube3);
        puzzlePhone.position.set(0.02, -0.25, 0.09);
        puzzlePhone.rotation.x = -0.75;

        armL.add(armMeshL, puzzlePhone);

        const armR = new THREE.Group();
        armR.position.set(0.28, 0.70, 0);
        const armMeshR = armMeshL.clone();
        const wheelRing = new THREE.Mesh(
            new THREE.TorusGeometry(0.09, 0.022, 6, 12),
            new THREE.MeshLambertMaterial({ color: 0x1c1917 })
        );
        wheelRing.position.set(0, -0.25, 0.08);
        armR.add(armMeshR, wheelRing);
        root.add(armL, armR);

        // 姨丈魔法懸浮倒試管配件 (Floating Water-Sort Puzzle Test Tubes)
        const puzzleTubeGroup = new THREE.Group();
        puzzleTubeGroup.position.set(0, 0.72, 0.28);
        const glassMat = new THREE.MeshPhongMaterial({
            color: 0x93c5fd,
            transparent: true,
            opacity: 0.55,
            shininess: 90
        });
        const liquidBlueMat = new THREE.MeshBasicMaterial({ color: 0x0284c7 });
        const liquidYellowMat = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
        const sparkleMat = new THREE.MeshBasicMaterial({ color: 0xffffff });

        // 左試管 (傾斜 45 度倒出水流)
        const tubeLeftGroup = new THREE.Group();
        tubeLeftGroup.position.set(-0.11, 0.05, 0);
        const tubeLeftGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, 0.18, 12, 1, true), glassMat);
        const tubeLeftLiquid = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.028, 0.10, 10), liquidBlueMat);
        tubeLeftLiquid.position.y = -0.03;
        tubeLeftGroup.add(tubeLeftGlass, tubeLeftLiquid);
        tubeLeftGroup.rotation.z = -0.72;

        // 倒出的優美液體弧線 (Liquid Stream)
        const streamMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.012, 0.12, 6), liquidBlueMat);
        streamMesh.position.set(0, 0.04, 0);
        streamMesh.rotation.z = 0.45;

        // 右試管 (正立接水)
        const tubeRightGroup = new THREE.Group();
        tubeRightGroup.position.set(0.11, -0.04, 0);
        const tubeRightGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, 0.18, 12, 1, true), glassMat);
        const tubeRightLiquid = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.028, 0.11, 10), liquidYellowMat);
        tubeRightLiquid.position.y = -0.03;
        tubeRightGroup.add(tubeRightGlass, tubeRightLiquid);

        // 試管上方過關金色星芒
        const sparkle = new THREE.Mesh(new THREE.OctahedronGeometry(0.045, 0), sparkleMat);
        sparkle.position.set(0.11, 0.10, 0);

        puzzleTubeGroup.add(tubeLeftGroup, streamMesh, tubeRightGroup, sparkle);
        puzzleTubeGroup.scale.setScalar(0.001);
        puzzleTubeGroup.visible = false;
        root.add(puzzleTubeGroup);

        root.userData = {
            role: 'yijhang',
            legL, legR, armL, armR, headGroup, torso,
            puzzleTubeGroup,
            tubeScale: 0,
            eyes: [],
            jumping: 0,
            actionPhase: Math.random() * 10
        };
        enableShadow(root);
        return root;
    }

    // 建立 C3 阿姨 (和藹婦人 + 溫暖捲髮 + 大衣 + 伴手禮提袋 + 烤糰子串 + 頭頂小愛心)
    function buildC3_Ayee() {
        const root = new THREE.Group();
        const skinMat  = new THREE.MeshLambertMaterial({ color: 0xffe4c4 });
        const coatMat  = new THREE.MeshLambertMaterial({ color: 0xd97706, flatShading: true }); // 溫暖焦糖杏色大衣
        const scarfMat = new THREE.MeshLambertMaterial({ color: 0xbe123c }); // 酒紅保暖圍巾
        const hairMat  = new THREE.MeshLambertMaterial({ color: 0x451a03, flatShading: true });
        const eyeMat   = new THREE.MeshBasicMaterial({ color: 0x1e293b });
        const blushMat = new THREE.MeshBasicMaterial({ color: 0xfb7185, transparent: true, opacity: 0.5 });

        // 雙腿
        const legL = new THREE.Group();
        legL.position.set(-0.11, 0.28, 0);
        const legMeshL = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.06, 0.26, 8), new THREE.MeshLambertMaterial({ color: 0x44403c }));
        legMeshL.position.y = -0.12;
        legL.add(legMeshL);

        const legR = new THREE.Group();
        legR.position.set(0.11, 0.28, 0);
        legR.add(legMeshL.clone());
        root.add(legL, legR);

        // 身體（長版暖色大衣 + 酒紅圍巾）
        const torso = new THREE.Group();
        torso.position.y = 0.52;
        const coat = new THREE.Mesh(new THREE.CylinderGeometry(0.21, 0.28, 0.48, 10), coatMat);
        const scarf = new THREE.Mesh(new THREE.TorusGeometry(0.19, 0.06, 8, 14), scarfMat);
        scarf.rotation.x = Math.PI / 2;
        scarf.position.y = 0.22;
        torso.add(coat, scarf);
        root.add(torso);

        // 頭部（和藹笑眼 + 蓬鬆優雅捲髮 + 珍珠耳環）
        const headGroup = new THREE.Group();
        headGroup.position.y = 0.96;
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.28, 14, 12), skinMat);

        const eyeL = new THREE.Mesh(new THREE.SphereGeometry(0.035, 8, 8), eyeMat);
        eyeL.position.set(-0.095, 0.02, 0.255);
        const eyeR = eyeL.clone();
        eyeR.position.set(0.095, 0.02, 0.255);

        const blushL = new THREE.Mesh(new THREE.CircleGeometry(0.05, 8), blushMat);
        blushL.position.set(-0.15, -0.04, 0.25);
        blushL.rotation.y = -0.35;
        const blushR = blushL.clone();
        blushR.position.set(0.15, -0.04, 0.25);
        blushR.rotation.y = 0.35;

        // 優雅溫婉深棕秀髮基底（全包覆頭頂與後腦，前額傾角適度，徹底根除禿頭與怪異中分分岔！）
        // 採用平滑後仰球冠罩蓋，額頭正面露出圓潤笑臉，完全沒有生硬的 V 字高分岔
        const hairBase = new THREE.Mesh(
            new THREE.SphereGeometry(0.294, 18, 14, 0, Math.PI * 2, 0, Math.PI * 0.58),
            hairMat
        );
        hairBase.rotation.x = -0.22; // 微微後仰，自然露出光潔額頭與和藹笑眼
        hairBase.position.set(0, 0.04, -0.02);

        // 後頸部秀髮收口（銜接大衣與圍巾）
        const hairBack = new THREE.Mesh(
            new THREE.SphereGeometry(0.292, 16, 12, Math.PI * 0.70, Math.PI * 1.60, 0, Math.PI * 0.78),
            hairMat
        );
        hairBack.position.set(0, 0, -0.02);

        // 溫柔優雅斜旁分微蓬瀏海（以球體層次自然斜斜搭在高額頭上方 y = 0.12~0.15，柔和自然，絕不中分生硬！）
        const bangsSide = new THREE.Mesh(
            new THREE.SphereGeometry(0.12, 10, 8),
            hairMat
        );
        bangsSide.scale.set(1.6, 0.65, 0.9);
        bangsSide.position.set(0.04, 0.14, 0.22);
        bangsSide.rotation.set(-0.15, 0.10, -0.12);

        headGroup.add(head, eyeL, eyeR, blushL, blushR, hairBase, hairBack, bangsSide);

        // 蓬鬆立體貴婦優雅波浪捲髮（飽滿環繞在頭頂、兩側耳際與臉頰旁，線條圓潤優美，層次非常自然）
        const curlPositions = [
            // 左右兩側耳際與臉頰豐盈修飾捲
            [-0.22, 0.06, 0.06], [0.22, 0.06, 0.06],
            [-0.24, -0.04, -0.02], [0.24, -0.04, -0.02],
            // 前額兩側優雅過渡微捲
            [-0.12, 0.16, 0.19], [0.15, 0.15, 0.17],
            // 頭頂蓬鬆圓潤弧度
            [-0.12, 0.24, 0.02], [0.12, 0.24, 0.02],
            [0, 0.26, -0.06],
            // 後腦與後頸優雅收口
            [-0.16, 0.04, -0.17], [0.16, 0.04, -0.17],
            [0, -0.07, -0.19]
        ];
        curlPositions.forEach(p => {
            const c = new THREE.Mesh(new THREE.SphereGeometry(0.088, 8, 8), hairMat);
            c.position.set(p[0], p[1], p[2]);
            headGroup.add(c);
        });

        // 吃到美食時頭頂浮現的粉紅小愛心
        const heart = new THREE.Mesh(
            new THREE.OctahedronGeometry(0.09, 0),
            new THREE.MeshBasicMaterial({ color: 0xf43f5e })
        );
        heart.position.set(0, 0.46, 0);
        headGroup.add(heart);
        root.add(headGroup);

        // 左手提九州伴手禮紙袋、右手拿花見三色糰子串
        const armL = new THREE.Group();
        armL.position.set(-0.25, 0.66, 0);
        const armMeshL = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.05, 0.26, 8), coatMat);
        armMeshL.position.y = -0.11;
        const shoppingBag = new THREE.Mesh(
            new THREE.BoxGeometry(0.18, 0.22, 0.10),
            new THREE.MeshLambertMaterial({ color: 0xfef08a })
        );
        shoppingBag.position.set(-0.04, -0.26, 0.04);
        armL.add(armMeshL, shoppingBag);

        const armR = new THREE.Group();
        armR.position.set(0.25, 0.66, 0);
        const armMeshR = armMeshL.clone();
        // 三色烤糰子串 (粉紅、白、抹茶綠)
        const dangoStick = new THREE.Group();
        const stick = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.24, 6), new THREE.MeshLambertMaterial({ color: 0xd97706 }));
        const d1 = new THREE.Mesh(new THREE.SphereGeometry(0.042, 8, 8), new THREE.MeshLambertMaterial({ color: 0xf472b6 }));
        d1.position.y = 0.08;
        const d2 = new THREE.Mesh(new THREE.SphereGeometry(0.042, 8, 8), new THREE.MeshLambertMaterial({ color: 0xffffff }));
        d2.position.y = 0.01;
        const d3 = new THREE.Mesh(new THREE.SphereGeometry(0.042, 8, 8), new THREE.MeshLambertMaterial({ color: 0x84cc16 }));
        d3.position.y = -0.06;
        dangoStick.add(stick, d1, d2, d3);
        dangoStick.position.set(0.02, -0.20, 0.12);
        dangoStick.rotation.x = -0.8;
        armR.add(armMeshR, dangoStick);

        // 阿姨野餐墊與點心茶席配件 (Gingham Picnic Blanket & Sweets Feast)
        const picnicMatGroup = new THREE.Group();
        picnicMatGroup.position.set(0.24, 0.035, 0.20);

        // 紅白格紋野餐墊 (採用具備微厚度之立體編織薄盒，杜絕穿模與 Z-fighting 破圖)
        const matBase = new THREE.Mesh(
            new THREE.BoxGeometry(0.82, 0.012, 0.82),
            new THREE.MeshLambertMaterial({ color: 0xfef2f2 })
        );
        matBase.position.y = 0.006;
        picnicMatGroup.add(matBase);
        // 紅色格紋交錯裝飾方塊
        const redSqMat = new THREE.MeshLambertMaterial({ color: 0xef4444 });
        for (let ix = -3; ix <= 3; ix += 2) {
            for (let iz = -3; iz <= 3; iz += 2) {
                const sq = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.014, 0.11), redSqMat);
                sq.position.set(ix * 0.11, 0.008, iz * 0.11);
                picnicMatGroup.add(sq);
            }
        }

        // 竹編草莓籃
        const basket = new THREE.Mesh(
            new THREE.CylinderGeometry(0.10, 0.08, 0.07, 10),
            new THREE.MeshLambertMaterial({ color: 0x92400e })
        );
        basket.position.set(-0.16, 0.045, -0.14);
        const berryMat = new THREE.MeshLambertMaterial({ color: 0xdc2626 });
        for (let i = 0; i < 5; i++) {
            const b = new THREE.Mesh(new THREE.ConeGeometry(0.026, 0.045, 6), berryMat);
            b.rotation.x = Math.PI;
            b.position.set(-0.16 + (Math.sin(i * 1.5)) * 0.04, 0.075, -0.14 + (Math.cos(i * 1.5)) * 0.04);
            picnicMatGroup.add(b);
        }
        picnicMatGroup.add(basket);

        // 黑色漆器托盤 + 三色糰子點心
        const tray = new THREE.Mesh(
            new THREE.BoxGeometry(0.22, 0.018, 0.16),
            new THREE.MeshLambertMaterial({ color: 0x1c1917 })
        );
        tray.position.set(0.14, 0.020, -0.12);
        const sw1 = new THREE.Mesh(new THREE.SphereGeometry(0.032, 8, 8), new THREE.MeshLambertMaterial({ color: 0xf472b6 }));
        sw1.position.set(0.10, 0.040, -0.12);
        const sw2 = new THREE.Mesh(new THREE.SphereGeometry(0.032, 8, 8), new THREE.MeshLambertMaterial({ color: 0xffffff }));
        sw2.position.set(0.14, 0.040, -0.12);
        const sw3 = new THREE.Mesh(new THREE.SphereGeometry(0.032, 8, 8), new THREE.MeshLambertMaterial({ color: 0x84cc16 }));
        sw3.position.set(0.18, 0.040, -0.12);
        picnicMatGroup.add(tray, sw1, sw2, sw3);

        // 陶瓷保溫熱茶壺
        const teapot = new THREE.Mesh(
            new THREE.CylinderGeometry(0.042, 0.048, 0.11, 10),
            new THREE.MeshLambertMaterial({ color: 0x0284c7 })
        );
        teapot.position.set(0, 0.06, 0.16);
        picnicMatGroup.add(teapot);

        picnicMatGroup.scale.setScalar(0.001);
        picnicMatGroup.visible = false;
        root.add(picnicMatGroup);

        root.add(armL, armR);
        root.userData = {
            role: 'ayee',
            legL, legR, armL, armR, headGroup, torso,
            picnicMatGroup,
            matScale: 0,
            eyes: [eyeL, eyeR],
            heart,
            dangoStick,
            jumping: 0,
            actionPhase: Math.random() * 10
        };
        enableShadow(root);
        return root;
    }

    // 建立 C4 阿嚕 (圓滾滾焦糖棕熊 + 圓耳朵 + 奶油色肚皮與吻部 + 紅圍巾)
    function buildC4_Alu() {
        const root = new THREE.Group();
        const furMat   = new THREE.MeshLambertMaterial({ color: 0x92400e, flatShading: true }); // 溫暖焦糖棕毛色 (非黑色熊本熊)
        const creamMat = new THREE.MeshLambertMaterial({ color: 0xfde68a }); // 奶油色肚皮與嘴鼻區
        const noseMat  = new THREE.MeshBasicMaterial({ color: 0x292524 });
        const scarfMat = new THREE.MeshLambertMaterial({ color: 0xdc2626 }); // 聖誕紅保暖圍巾
        const blushMat = new THREE.MeshBasicMaterial({ color: 0xfb7185, transparent: true, opacity: 0.60 });

        // 短短圓熊腿
        const legL = new THREE.Group();
        legL.position.set(-0.14, 0.22, 0);
        const pawL = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.09, 0.22, 8), furMat);
        pawL.position.y = -0.09;
        legL.add(pawL);

        const legR = new THREE.Group();
        legR.position.set(0.14, 0.22, 0);
        legR.add(pawL.clone());
        root.add(legL, legR);

        // 圓滾滾熊肚子 + 奶油色肚皮 + 圓尾巴 + 紅圍巾
        const torso = new THREE.Group();
        torso.position.y = 0.50;
        const belly = new THREE.Mesh(new THREE.SphereGeometry(0.32, 14, 12), furMat);
        belly.scale.set(1.0, 1.05, 0.95);
        const bellyPatch = new THREE.Mesh(new THREE.SphereGeometry(0.23, 12, 10), creamMat);
        bellyPatch.scale.set(0.9, 0.95, 0.45);
        bellyPatch.position.set(0, -0.02, 0.22);
        const tail = new THREE.Mesh(new THREE.SphereGeometry(0.085, 8, 8), furMat);
        tail.position.set(0, -0.10, -0.30);
        const scarf = new THREE.Mesh(new THREE.TorusGeometry(0.23, 0.065, 8, 14), scarfMat);
        scarf.rotation.x = Math.PI / 2;
        scarf.position.y = 0.25;
        const scarfTail = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.22, 0.04), scarfMat);
        scarfTail.position.set(0.12, 0.14, 0.26);
        scarfTail.rotation.z = -0.2;
        torso.add(belly, bellyPatch, tail, scarf, scarfTail);
        root.add(torso);

        // 圓熊頭 + 兩隻圓耳朵 + 奶油吻部 + 黑鼻頭 + 腮紅
        const headGroup = new THREE.Group();
        headGroup.position.y = 0.96;
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.31, 14, 12), furMat);
        head.scale.set(1.06, 0.96, 0.98);

        // 圓熊耳
        const earL = new THREE.Mesh(new THREE.SphereGeometry(0.11, 10, 10), furMat);
        earL.position.set(-0.24, 0.24, -0.02);
        const earInnerL = new THREE.Mesh(new THREE.SphereGeometry(0.06, 8, 8), creamMat);
        earInnerL.position.set(-0.24, 0.24, 0.05);
        const earR = earL.clone();
        earR.position.set(0.24, 0.24, -0.02);
        const earInnerR = earInnerL.clone();
        earInnerR.position.set(0.24, 0.24, 0.05);

        // 奶油色突出吻部與黑鼻頭
        const snout = new THREE.Mesh(new THREE.SphereGeometry(0.12, 10, 10), creamMat);
        snout.scale.set(1.1, 0.85, 0.8);
        snout.position.set(0, -0.05, 0.27);
        const nose = new THREE.Mesh(new THREE.SphereGeometry(0.042, 8, 8), noseMat);
        nose.position.set(0, -0.02, 0.36);

        // 圓眼睛與粉嫩腮紅
        const eyeL = new THREE.Mesh(new THREE.SphereGeometry(0.038, 8, 8), noseMat);
        eyeL.position.set(-0.11, 0.05, 0.27);
        const eyeR = eyeL.clone();
        eyeR.position.set(0.11, 0.05, 0.27);

        const blushL = new THREE.Mesh(new THREE.CircleGeometry(0.055, 8), blushMat);
        blushL.position.set(-0.19, -0.04, 0.25);
        blushL.rotation.y = -0.4;
        const blushR = blushL.clone();
        blushR.position.set(0.19, -0.04, 0.25);
        blushR.rotation.y = 0.4;

        // 頭頂溫泉白色小毛巾
        const onsenTowel = new THREE.Mesh(
            new THREE.BoxGeometry(0.22, 0.045, 0.14),
            new THREE.MeshLambertMaterial({ color: 0xf8fafc })
        );
        onsenTowel.position.set(0, 0.29, 0.02);

        headGroup.add(head, earL, earInnerL, earR, earInnerR, snout, nose, eyeL, eyeR, blushL, blushR, onsenTowel);
        root.add(headGroup);

        // 熊掌左右手與拍照專用復古相機
        const armL = new THREE.Group();
        armL.position.set(-0.29, 0.62, 0);
        const armMeshL = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.08, 0.26, 8), furMat);
        armMeshL.position.y = -0.10;
        armL.add(armMeshL);

        const armR = new THREE.Group();
        armR.position.set(0.29, 0.62, 0);
        const armMeshR = armMeshL.clone();
        armR.add(armMeshR);

        // 阿嚕專屬 3D 經典復古高階相機（大幅放大加強，銀黑雙色機身 + 大口徑光學鍍膜鏡頭 + 經典紅標快門 + 掛帶，一眼即辨！）
        const cameraGroup = new THREE.Group();
        const silverCamMat = new THREE.MeshLambertMaterial({ color: 0xe2e8f0 }); // 頂蓋與底板經典銀色金屬
        const camGripMat   = new THREE.MeshLambertMaterial({ color: 0x1e293b }); // 機身中央防滑黑蒙皮
        const camLeatherMat= new THREE.MeshLambertMaterial({ color: 0xb45309 }); // 復古焦糖皮質飾邊
        const lensBlackMat = new THREE.MeshLambertMaterial({ color: 0x0f172a, flatShading: true }); // 大口徑金屬鏡筒
        const lensGoldMat  = new THREE.MeshBasicMaterial({ color: 0xf59e0b }); // 奢華金圈鏡頭飾環
        const glassMat     = new THREE.MeshBasicMaterial({ color: 0x38bdf8 }); // 湛藍光學多層鍍膜前玉
        const redDotMat    = new THREE.MeshBasicMaterial({ color: 0xef4444 }); // 經典紅標 (Leica Red Dot)

        // 1. 寬版經典復古機身 (大幅放大至 0.28 × 0.18 × 0.13，視覺份量十足)
        const camBase = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.18, 0.13), camGripMat);
        const camTopPlate = new THREE.Mesh(new THREE.BoxGeometry(0.282, 0.045, 0.132), silverCamMat);
        camTopPlate.position.y = 0.07;
        const camBottomPlate = new THREE.Mesh(new THREE.BoxGeometry(0.282, 0.025, 0.132), silverCamMat);
        camBottomPlate.position.y = -0.08;
        const camGripAccent = new THREE.Mesh(new THREE.BoxGeometry(0.284, 0.085, 0.134), camLeatherMat);
        camGripAccent.position.y = -0.005;

        // 2. 機頂快門鈕、轉盤與紅標
        const shutterBtn = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.024, 0.035, 12), redDotMat);
        shutterBtn.position.set(0.08, 0.105, 0.02);
        const modeDial = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.030, 12), silverCamMat);
        modeDial.position.set(-0.08, 0.102, 0.02);
        const redDotLogo = new THREE.Mesh(new THREE.CircleGeometry(0.022, 10), redDotMat);
        redDotLogo.position.set(0.09, 0.045, 0.068);

        // 3. 大口徑大光圈鏡頭群 (多重金屬階層 + 藍色鍍膜前玉玻璃 + 奢華金圈)
        const lensBase = new THREE.Mesh(new THREE.CylinderGeometry(0.078, 0.082, 0.05, 14), lensBlackMat);
        lensBase.rotation.x = Math.PI / 2;
        lensBase.position.set(0, -0.005, 0.085);

        const goldRing = new THREE.Mesh(new THREE.CylinderGeometry(0.079, 0.079, 0.012, 14), lensGoldMat);
        goldRing.rotation.x = Math.PI / 2;
        goldRing.position.set(0, -0.005, 0.105);

        const lensFront = new THREE.Mesh(new THREE.CylinderGeometry(0.072, 0.076, 0.045, 14), lensBlackMat);
        lensFront.rotation.x = Math.PI / 2;
        lensFront.position.set(0, -0.005, 0.125);

        const glassOptic = new THREE.Mesh(new THREE.CircleGeometry(0.065, 14), glassMat);
        glassOptic.position.set(0, -0.005, 0.149);

        // 4. 機頂復古熱靴閃光燈
        const flashHousing = new THREE.Mesh(new THREE.BoxGeometry(0.065, 0.045, 0.035), silverCamMat);
        flashHousing.position.set(-0.065, 0.055, 0.07);
        const flashWindow = new THREE.Mesh(new THREE.PlaneGeometry(0.052, 0.032), new THREE.MeshBasicMaterial({ color: 0xfef08a }));
        flashWindow.position.set(-0.065, 0.055, 0.089);
        flashWindow.castShadow = false;
        flashWindow.receiveShadow = false;

        const flashGlow = new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 8), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0 }));
        flashGlow.position.set(-0.065, 0.055, 0.11);
        flashGlow.visible = false;
        flashGlow.castShadow = false;
        flashGlow.receiveShadow = false;

        // 5. 拍照爆閃光源 (PointLight) 與星芒光環（改為圓形 RingGeometry，嚴禁投射陰影，避免阿嚕身體出現巨大方形陰影！）
        const flashLight = new THREE.PointLight(0xffffff, 0, 9.5);
        flashLight.position.set(-0.065, 0.055, 0.18);
        flashLight.castShadow = false;
        const flashBurst = new THREE.Mesh(
            new THREE.RingGeometry(0.02, 0.28, 16),
            new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide })
        );
        flashBurst.position.set(-0.065, 0.055, 0.20);
        flashBurst.visible = false;
        flashBurst.castShadow = false;
        flashBurst.receiveShadow = false;

        // 6. 專業皮質相機背帶 (掛在阿嚕胸前)
        const strapMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
        const strapL = new THREE.Mesh(new THREE.CylinderGeometry(0.010, 0.010, 0.22, 6), strapMat);
        strapL.position.set(-0.14, 0.10, -0.02);
        strapL.rotation.z = -0.35;
        const strapR = new THREE.Mesh(new THREE.CylinderGeometry(0.010, 0.010, 0.22, 6), strapMat);
        strapR.position.set(0.14, 0.10, -0.02);
        strapR.rotation.z = 0.35;

        cameraGroup.add(
            camBase, camTopPlate, camBottomPlate, camGripAccent,
            shutterBtn, modeDial, redDotLogo,
            lensBase, goldRing, lensFront, glassOptic,
            flashHousing, flashWindow, flashGlow, flashLight, flashBurst,
            strapL, strapR
        );
        cameraGroup.position.set(-0.10, -0.12, 0.17);
        armR.add(cameraGroup);

        root.add(armL, armR);

        root.userData = {
            role: 'alu',
            legL, legR, armL, armR, headGroup, torso,
            eyes: [eyeL, eyeR],
            cameraGroup,
            flashGlow,
            flashLight,
            flashBurst,
            jumping: 0,
            actionPhase: Math.random() * 10
        };
        enableShadow(root);
        return root;
    }

    const CHAR_BUILDERS = {
        C1: buildC1_Achun,
        achun: buildC1_Achun,
        C2: buildC2_Yijhang,
        yijhang: buildC2_Yijhang,
        C3: buildC3_Ayee,
        ayee: buildC3_Ayee,
        C4: buildC4_Alu,
        alu: buildC4_Alu
    };

    function createCharacter(key) {
        const fn = CHAR_BUILDERS[key];
        return fn ? fn() : buildC1_Achun();
    }

    // 更新單一角色的精緻動作（走路擺臂、眨眼、隨機小劇場動作狀態機、以及依角色觸發專屬動作）
    function animateCharacterPose(charGroup, elapsed, delta, isWalking) {
        const ud = charGroup.userData;
        if (!ud) return;

        // 初始化隨機動作狀態機 (Random Quirky Gesture State Machine)
        if (ud.quirkTimer === undefined) {
            ud.quirkTimer = 1.5 + Math.random() * 3.5;
            ud.quirkDuration = 0;
            ud.quirkType = 0;
            ud.spinBaseY = 0;
        }

        ud.quirkTimer -= delta;
        if (ud.quirkTimer <= 0 && ud.quirkDuration <= 0) {
            // 隨機抽籤觸發 5 種生動小動作之一：
            // 1=原地開心轉圈圈, 2=雀躍二連跳+高舉雙手, 3=好奇左顧右盼張望, 4=角色招牌特技強化, 5=向隔壁家人招手歪頭互動
            ud.quirkType = 1 + Math.floor(Math.random() * 5);
            ud.quirkDuration = 1.8 + Math.random() * 1.4;
            ud.quirkMaxDur = ud.quirkDuration;
            ud.quirkTimer = 3.2 + Math.random() * 4.5;
        }

        let activeQuirk = 0;
        let quirkProgress = 0;
        if (ud.isSpotBusy) {
            // 在景點執行專屬動作期間（如席地打筆電、拍照、玩手遊），暫停隨機轉圈或亂跳，專注呈現沉浸動作
            activeQuirk = 0;
            ud.quirkDuration = 0;
        } else if (ud.quirkDuration > 0) {
            ud.quirkDuration = Math.max(0, ud.quirkDuration - delta);
            activeQuirk = ud.quirkType;
            quirkProgress = 1.0 - (ud.quirkDuration / (ud.quirkMaxDur || 2.0));
        }

        const phase = elapsed * 6.5 + (ud.actionPhase || 0);

        // 1. 自然眨眼 (每 3.4 秒眨眼一次，有時快速連眨兩下)
        if (ud.eyes && ud.eyes.length) {
            const blinkWindow = (elapsed + (ud.actionPhase || 0)) % 3.4;
            const isBlinking = (blinkWindow > 3.25) || (blinkWindow > 1.6 && blinkWindow < 1.68 && activeQuirk === 3);
            const eyeScaleY = isBlinking ? 0.12 : 1.0;
            ud.eyes.forEach(e => { e.scale.y = eyeScaleY; });
        }

        // 2. 點擊彈跳或隨機二連跳
        let jumpOffset = 0;
        if (ud.jumping > 0) {
            ud.jumping = Math.max(0, ud.jumping - delta * 2.1);
            jumpOffset = Math.sin(ud.jumping * Math.PI) * 0.65;
        } else if (activeQuirk === 2) {
            // 隨機雀躍二連小跳步
            jumpOffset = Math.abs(Math.sin(quirkProgress * Math.PI * 2)) * 0.36;
        }

        // 先重置副軸旋轉以免不同動作殘留姿勢
        ud.armL.rotation.set(0, 0, 0);
        ud.armR.rotation.set(0, 0, 0);
        ud.torso.rotation.set(0, 0, 0);
        ud.headGroup.rotation.set(0, 0, 0);
        if (ud.ufoGroup) {
            ud.ufoGroup.visible = !!ud.isUfoChasing;
            ud.legL.visible = !ud.isUfoChasing;
            ud.legR.visible = !ud.isUfoChasing;
        }

        if (ud.isUfoChasing && ud.ufoGroup) {
            // 阿純被落下車時：召喚並駕駛科幻飛碟 (UFO) 在後面高速懸浮追車！
            if (ud.laptopGroup) ud.laptopGroup.visible = true;
            if (ud.cupGroup) ud.cupGroup.visible = true;
            if (ud.campingDeskGroup) ud.campingDeskGroup.visible = false;
            const baseY = (ud.baseY !== undefined) ? ud.baseY : 0.76;
            charGroup.position.y = baseY + 0.36 + Math.sin(elapsed * 7.5) * 0.08 + jumpOffset;
            if (ud.ufoSpinRing) ud.ufoSpinRing.rotation.y = elapsed * 6.5;
            if (ud.tractorBeam) ud.tractorBeam.scale.setScalar(0.92 + Math.sin(elapsed * 12.0) * 0.14);
            ud.ufoGroup.rotation.z = Math.sin(elapsed * 5.0) * 0.09;
            ud.ufoGroup.rotation.x = 0.14; // 飛碟微幅前傾衝刺
            // 左手托著筆電繼續打物理治療紀錄，右手緊張高舉拿鐵揮手大喊「等等我！」
            ud.armL.rotation.x = -1.15;
            ud.armL.rotation.y = 0.25;
            ud.armR.rotation.x = -2.35 + Math.sin(elapsed * 15.0) * 0.42;
            ud.headGroup.rotation.y = Math.sin(elapsed * 6.0) * 0.22;
            return;
        }

        if (isWalking === 'seated') {
            // 坐在 Toyota Sienta 7 人座車艙內的專屬乘車姿勢
            ud.legL.rotation.x = -Math.PI * 0.44;
            ud.legR.rotation.x = -Math.PI * 0.44;
            if (ud.role === 'yijhang') {
                // 姨丈坐在右駕駕駛座雙手穩握方向盤 + 左右觀察路況
                ud.armL.rotation.x = -1.05 + Math.sin(elapsed * 3.5) * 0.12;
                ud.armR.rotation.x = -1.05 - Math.sin(elapsed * 3.5) * 0.12;
                ud.headGroup.rotation.y = Math.sin(elapsed * 1.6) * 0.18;
            } else if (ud.role === 'achun') {
                if (ud.campingDeskGroup) ud.campingDeskGroup.visible = false;
                if (ud.laptopGroup) ud.laptopGroup.visible = true;
                if (ud.cupGroup) ud.cupGroup.visible = true;
                // 阿純在車上：交替表現「把筆電放腿上狂打物理治療紀錄」與「打完字靠窗香甜度估睡覺」
                if (activeQuirk === 1 || activeQuirk === 2 || activeQuirk === 4) {
                    ud.armL.rotation.x = -1.05;
                    ud.armR.rotation.x = -1.05 + Math.sin(elapsed * 14.0) * 0.12;
                    ud.headGroup.rotation.x = 0.22;
                    ud.headGroup.rotation.y = Math.sin(elapsed * 3.0) * 0.10;
                } else {
                    ud.eyes.forEach(e => { e.scale.y = 0.12; });
                    ud.headGroup.rotation.z = 0.25 + Math.sin(elapsed * 2.2) * 0.08;
                    ud.headGroup.rotation.x = 0.18 + Math.abs(Math.sin(elapsed * 2.2)) * 0.12;
                }
            } else if (ud.role === 'ayee') {
                // 阿姨坐在副駕/後座轉頭遞烤糰子與零食給大家吃
                ud.armR.rotation.x = -0.85 + Math.sin(elapsed * 4.2) * 0.18;
                ud.headGroup.rotation.y = 0.35 + Math.sin(elapsed * 2.0) * 0.25;
                if (ud.heart) {
                    ud.heart.scale.setScalar(0.85 + Math.sin(elapsed * 5.5) * 0.25);
                }
            } else if (ud.role === 'alu') {
                // 阿嚕坐在後座托腮望向車窗外思考 AI 熊生
                ud.armR.rotation.x = -1.35;
                ud.armR.rotation.z = 0.28;
                ud.headGroup.rotation.y = -0.35 + Math.sin(elapsed * 1.5) * 0.20;
                ud.headGroup.rotation.z = -0.15;
            }
            return;
        }

        if (isWalking) {
            // 行走邁步時：阿純嚴格收納露營桌椅（絕不帶桌子走路！），手上拿著隨身筆電與熱拿鐵
            if (ud.role === 'achun') {
                if (ud.campingDeskGroup) ud.campingDeskGroup.visible = false;
                ud.deskScale = 0;
                if (ud.laptopGroup) ud.laptopGroup.visible = true;
                if (ud.cupGroup) ud.cupGroup.visible = true;
            }
            // 行走時四肢擺動與輕快彈跳 + 隨機邊走邊做小動作
            const stride = Math.sin(phase) * 0.58;
            ud.legL.rotation.x = stride;
            ud.legR.rotation.x = -stride;
            ud.armL.rotation.x = -stride * 0.78;
            ud.armR.rotation.x = stride * 0.78;
            ud.torso.rotation.z = Math.cos(phase) * 0.06;
            ud.headGroup.rotation.z = Math.sin(phase * 0.5) * 0.07;
            ud.headGroup.rotation.y = Math.sin(elapsed * 1.6 + ud.actionPhase) * 0.22;
            const baseY = (ud.baseY !== undefined) ? ud.baseY : 0.76;
            charGroup.position.y = baseY + Math.abs(Math.sin(phase)) * 0.09 + jumpOffset;

            // 邊走邊觸發的隨機小動作
            if (activeQuirk === 1) {
                // 邊走邊開心轉一圈
                ud.torso.rotation.y = quirkProgress * Math.PI * 2;
                ud.headGroup.rotation.y = quirkProgress * Math.PI * 2;
                ud.armL.rotation.z = 0.7;
                ud.armR.rotation.z = -0.7;
            } else if (activeQuirk === 2) {
                // 邊走邊舉雙手歡呼小跳步
                ud.armL.rotation.x = -2.4 + Math.sin(elapsed * 10) * 0.25;
                ud.armR.rotation.x = -2.4 - Math.sin(elapsed * 10) * 0.25;
            } else if (activeQuirk === 3) {
                // 邊走邊大幅度左右張望看風景/找美食
                ud.headGroup.rotation.y = Math.sin(quirkProgress * Math.PI * 3) * 0.62;
                ud.headGroup.rotation.x = -0.15;
            } else if (activeQuirk === 4) {
                // 邊走邊做角色招牌小動作
                if (ud.role === 'achun') {
                    // 阿純邊走邊打瞌睡點頭（釣魚度估）或伸懶腰想吃東西
                    ud.eyes.forEach(e => { e.scale.y = 0.12; });
                    ud.headGroup.rotation.x = 0.28 + Math.sin(elapsed * 4.0) * 0.18;
                    ud.headGroup.rotation.z = 0.22;
                } else if (ud.role === 'yijhang') {
                    // 姨丈邊走邊默默低頭看左手手機玩「倒試管顏色分類小遊戲」
                    ud.armL.rotation.x = -1.25;
                    ud.armL.rotation.y = 0.35;
                    ud.headGroup.rotation.x = 0.28;
                    ud.headGroup.rotation.y = 0.22;
                } else if (ud.role === 'ayee') {
                    // 阿姨邊走邊熱情把右手三色烤糰子往前遞：「來來來張嘴再吃一口！」
                    ud.armR.rotation.x = -1.35 + Math.sin(elapsed * 8.0) * 0.22;
                    ud.armL.rotation.z = 0.35;
                    ud.headGroup.rotation.y = Math.sin(elapsed * 4.5) * 0.35;
                } else if (ud.role === 'alu') {
                    // 阿嚕邊走邊單手托腮、仰望天空思考「我究竟是真熊還是 AI」
                    ud.armR.rotation.x = -1.55;
                    ud.armR.rotation.z = 0.35;
                    ud.headGroup.rotation.x = -0.32;
                    ud.headGroup.rotation.z = -0.22;
                }
            } else if (activeQuirk === 5) {
                // 向旁邊的家人揮揮手碎嘴聊天
                ud.armL.rotation.z = 0.85 + Math.sin(elapsed * 9) * 0.35;
                ud.headGroup.rotation.y = 0.42;
                ud.headGroup.rotation.z = 0.14;
            }
        } else {
            // 抵達景點下車散步 / 豐富隨機待機動作
            ud.legL.rotation.x = Math.sin(phase * 0.5) * 0.16;
            ud.legR.rotation.x = -Math.sin(phase * 0.5) * 0.16;
            const baseY = (ud.baseY !== undefined) ? ud.baseY : 0.76;
            charGroup.position.y = baseY + Math.abs(Math.sin(phase * 0.5)) * 0.045 + jumpOffset;

            if (activeQuirk === 1) {
                // 原地 360 度開心轉圈圈展示穿搭
                ud.torso.rotation.y = quirkProgress * Math.PI * 2;
                ud.headGroup.rotation.y = quirkProgress * Math.PI * 2;
                ud.armL.rotation.z = 0.75;
                ud.armR.rotation.z = -0.75;
                return;
            } else if (activeQuirk === 2) {
                // 雙手高舉比耶二連跳
                ud.armL.rotation.x = -2.5;
                ud.armL.rotation.z = 0.35;
                ud.armR.rotation.x = -2.5;
                ud.armR.rotation.z = -0.35;
                ud.headGroup.rotation.x = -0.18;
                return;
            }

            if (ud.role === 'achun') {
                // 阿純景點動作配件：只有在完全就座定點打紀錄時 (isSpotBusy 且非行走 moving)，才展開木質露營桌與折疊椅！
                const shouldShowDesk = !!(ud.isSpotBusy && !isWalking);
                if (ud.campingDeskGroup) {
                    if (shouldShowDesk) {
                        ud.deskScale = Math.min(1.0, (ud.deskScale || 0) + delta * 4.0);
                        ud.campingDeskGroup.visible = true;
                    } else {
                        ud.deskScale = Math.max(0, (ud.deskScale || 0) - delta * 6.0);
                        if (ud.deskScale <= 0.01) ud.campingDeskGroup.visible = false;
                    }
                    ud.campingDeskGroup.scale.setScalar(ud.deskScale);
                }

                // 核心修復：只有在展開桌子且定點坐好時，手上筆電才隱藏；走路邁步時手上隨身拿著筆電！
                const hasDesk = !!(shouldShowDesk && ud.deskScale && ud.deskScale > 0.05);
                if (ud.laptopGroup) ud.laptopGroup.visible = !hasDesk;
                if (ud.cupGroup) ud.cupGroup.visible = !hasDesk;

                if (shouldShowDesk) {
                    // 坐在露營休閒椅上（桌椅骨架垂直貼合地面 baseY 絕不穿模下陷，阿純骨盆準確落座帆布椅面）
                    ud.legL.rotation.x = -Math.PI * 0.44;
                    ud.legR.rotation.x = -Math.PI * 0.44;
                    charGroup.position.y = baseY - 0.12;
                    if (ud.campingDeskGroup) ud.campingDeskGroup.position.y = 0.12;

                    // 每 5.2 秒觸發一段 1.8 秒的舒爽「大伸懶腰」放鬆胸椎腰椎 (Deep Spine Stretch & Yawn)
                    const stretchCycle = (elapsed * 0.95 + (ud.actionPhase || 0)) % 5.2;
                    if (stretchCycle < 1.8) {
                        const arch = Math.sin((stretchCycle / 1.8) * Math.PI);
                        // 雙手高舉過頭拉伸筋膜、背部微後仰、仰頭舒爽閉目
                        ud.armL.rotation.set(-2.65 - arch * 0.25, 0.18, 0.30);
                        ud.armR.rotation.set(-2.65 - arch * 0.25, -0.18, -0.30);
                        ud.torso.rotation.x = -0.18 * arch;
                        ud.headGroup.rotation.x = -0.28 * arch;
                        if (ud.eyes && ud.eyes.length) ud.eyes.forEach(e => { e.scale.y = 0.12; });
                    } else {
                        // 筆電鍵盤飛快敲打打字 (SOAP 評估表狂敲中)
                        ud.armL.rotation.set(-1.15 + Math.sin(elapsed * 16.0) * 0.08, 0.22, 0);
                        ud.armR.rotation.set(-1.15 + Math.cos(elapsed * 16.0) * 0.08, -0.22, 0);
                        ud.headGroup.rotation.x = 0.22 + Math.sin(elapsed * 2.8) * 0.05;
                        ud.headGroup.rotation.y = Math.cos(elapsed * 1.8) * 0.10;
                    }
                } else if (activeQuirk === 3) {
                    // 香甜站著打瞌睡（閉眼 + 頭一點一點度估）
                    ud.eyes.forEach(e => { e.scale.y = 0.12; });
                    ud.headGroup.rotation.x = 0.25 + Math.abs(Math.sin(elapsed * 2.4)) * 0.20;
                    ud.headGroup.rotation.z = 0.22;
                    ud.armL.rotation.z = 0.20;
                    ud.armR.rotation.x = -0.35;
                } else {
                    // 站立時左手托著銀色筆電、右手敲鍵盤或喝拿鐵
                    ud.armL.rotation.x = -1.18 + Math.sin(elapsed * 2.5) * 0.06;
                    ud.armL.rotation.y = 0.22;
                    ud.armR.rotation.x = -1.12 + Math.sin(elapsed * 12.0) * 0.14;
                    ud.armR.rotation.y = -0.18;
                    ud.headGroup.rotation.x = 0.20;
                    ud.headGroup.rotation.y = 0.16 * Math.cos(elapsed * 2.2);
                }
            } else if (ud.role === 'yijhang') {
                // 姨丈景點動作配件：自動懸浮透明雙試管魔法倒水 + 帥氣推墨鏡手勢
                if (ud.puzzleTubeGroup) {
                    if (ud.isSpotBusy) {
                        ud.tubeScale = Math.min(1.0, (ud.tubeScale || 0) + delta * 4.0);
                        ud.puzzleTubeGroup.visible = true;
                    } else {
                        ud.tubeScale = Math.max(0, (ud.tubeScale || 0) - delta * 5.0);
                        if (ud.tubeScale <= 0.01) ud.puzzleTubeGroup.visible = false;
                    }
                    ud.puzzleTubeGroup.scale.setScalar(ud.tubeScale);
                    ud.puzzleTubeGroup.position.y = 0.72 + Math.sin(elapsed * 2.5) * 0.025;
                }

                if (ud.isSpotBusy) {
                    const puzzleCycle = (elapsed * 0.85 + (ud.actionPhase || 0)) % 4.2;
                    if (puzzleCycle < 2.6) {
                        // 雙手專心低頭滑手機倒試管
                        ud.armL.rotation.set(-1.22 + Math.sin(elapsed * 2.0) * 0.05, 0.32, 0);
                        ud.armR.rotation.set(-1.20 + Math.sin(elapsed * 8.0) * 0.12, -0.28, 0);
                        ud.headGroup.rotation.set(0.32, 0.10 * Math.sin(elapsed * 1.5), 0);
                    } else {
                        // 帥氣推墨鏡 (右手抬至墨鏡鼻樑處推一下，展現車神淡定)
                        ud.armL.rotation.set(-0.85, 0.20, 0);
                        ud.armR.rotation.set(-1.52, -0.32, -0.14);
                        ud.headGroup.rotation.set(-0.06, 0.16, 0.04);
                    }
                } else {
                    ud.armL.rotation.x = -1.22 + Math.sin(elapsed * 2.0) * 0.05;
                    ud.armL.rotation.y = 0.32;
                    ud.armR.rotation.x = -1.20 + Math.sin(elapsed * 7.5) * 0.12;
                    ud.armR.rotation.y = -0.28;
                    ud.headGroup.rotation.x = 0.34;
                    ud.headGroup.rotation.y = 0.12 * Math.sin(elapsed * 1.5);
                }
            } else if (ud.role === 'ayee') {
                // 阿姨在景點中是大範圍散步採買逛街的美食評鑑官，絕不帶著野餐墊移動！
                if (ud.picnicMatGroup) {
                    // 漫步走動時 (行走 isWalking 或非靜止 busy) 嚴格隱藏收納野餐墊
                    const shouldShowMat = !!(ud.isSpotBusy && !isWalking);
                    if (shouldShowMat) {
                        ud.matScale = Math.min(1.0, (ud.matScale || 0) + delta * 4.0);
                        ud.picnicMatGroup.visible = true;
                    } else {
                        ud.matScale = Math.max(0, (ud.matScale || 0) - delta * 6.0);
                        if (ud.matScale <= 0.01) ud.picnicMatGroup.visible = false;
                    }
                    ud.picnicMatGroup.scale.setScalar(ud.matScale);
                }

                if (ud.isSpotBusy) {
                    // 站在野餐墊旁熱情揮手遞糰子餵食
                    ud.armR.rotation.x = -1.25 + Math.sin(elapsed * 6.5) * 0.28;
                    ud.armR.rotation.y = 0.20 + Math.sin(elapsed * 3.0) * 0.25;
                    ud.armL.rotation.x = -0.55 + Math.cos(elapsed * 4.0) * 0.20;
                    ud.headGroup.rotation.y = Math.sin(elapsed * 3.0) * 0.35;
                    ud.headGroup.rotation.z = Math.cos(elapsed * 2.5) * 0.10;
                } else {
                    ud.armR.rotation.x = -1.15 + Math.sin(elapsed * 5.8) * 0.25;
                    ud.armR.rotation.y = Math.sin(elapsed * 3.0) * 0.30;
                    ud.armL.rotation.x = -0.55 + Math.cos(elapsed * 4.2) * 0.20;
                    ud.headGroup.rotation.y = Math.sin(elapsed * 3.2) * 0.38;
                    ud.headGroup.rotation.z = Math.cos(elapsed * 2.8) * 0.12;
                }
                if (ud.heart) {
                    const hs = 0.92 + Math.sin(elapsed * 6.5) * 0.35;
                    ud.heart.scale.setScalar(hs);
                    ud.heart.rotation.y = elapsed * 3.0;
                }
            } else if (ud.role === 'alu') {
                // 阿嚕景點動作配件：雙手舉起復古相機，真實閃光燈爆閃 + 星芒光環
                if (ud.isSpotBusy) {
                    ud.armL.rotation.set(-1.42, 0.26, 0.32);
                    ud.armR.rotation.set(-1.40, -0.26, -0.32);
                    const photoCycle = (elapsed * 0.95 + (ud.actionPhase || 0)) % 2.6;
                    if (photoCycle < 0.22) {
                        // 拍照爆閃瞬間！
                        const flashT = photoCycle / 0.22;
                        const flashIntensity = Math.sin(flashT * Math.PI) * 5.5;
                        if (ud.flashLight) ud.flashLight.intensity = flashIntensity;
                        if (ud.flashBurst) {
                            ud.flashBurst.visible = true;
                            ud.flashBurst.material.opacity = Math.sin(flashT * Math.PI) * 0.95;
                            ud.flashBurst.scale.setScalar(1.0 + Math.sin(flashT * Math.PI) * 1.8);
                            ud.flashBurst.rotation.z = elapsed * 8.0;
                        }
                        if (ud.flashGlow) {
                            ud.flashGlow.visible = true;
                            ud.flashGlow.material.opacity = 0.95;
                        }
                    } else {
                        if (ud.flashLight) ud.flashLight.intensity = 0;
                        if (ud.flashBurst) {
                            ud.flashBurst.visible = false;
                            ud.flashBurst.material.opacity = 0;
                        }
                        if (ud.flashGlow) {
                            ud.flashGlow.visible = false;
                            ud.flashGlow.material.opacity = 0;
                        }
                        if (photoCycle < 1.1) {
                            // 低頭查看相片成果
                            ud.armL.rotation.set(-1.08, 0.18, 0.10);
                            ud.armR.rotation.set(-1.08, -0.18, -0.10);
                            ud.headGroup.rotation.set(0.30 + Math.sin(elapsed * 3.5) * 0.08, 0, 0);
                        } else {
                            // 舉起相機環顧四周取景
                            ud.headGroup.rotation.y = Math.sin(elapsed * 1.8) * 0.42;
                            ud.headGroup.rotation.x = -0.06 + Math.cos(elapsed * 1.4) * 0.08;
                        }
                    }
                } else {
                    if (ud.flashLight) ud.flashLight.intensity = 0;
                    if (ud.flashBurst) {
                        ud.flashBurst.visible = false;
                        ud.flashBurst.material.opacity = 0;
                    }
                    if (ud.flashGlow) {
                        ud.flashGlow.visible = false;
                        ud.flashGlow.material.opacity = 0;
                    }
                    if (activeQuirk === 3 || activeQuirk === 4) {
                        ud.armL.rotation.x = -1.35 + Math.sin(elapsed * 3.0) * 0.15;
                        ud.armR.rotation.x = -1.35 - Math.sin(elapsed * 3.0) * 0.15;
                        ud.armL.rotation.z = -0.25;
                        ud.armR.rotation.z = 0.25;
                        ud.headGroup.rotation.x = 0.22;
                        ud.headGroup.rotation.y = Math.sin(elapsed * 2.5) * 0.28;
                    } else {
                        ud.torso.rotation.z = Math.sin(elapsed * 2.5) * 0.08;
                        ud.armR.rotation.x = -1.48;
                        ud.armR.rotation.z = 0.32;
                        ud.armL.rotation.z = 0.25;
                        ud.headGroup.rotation.x = -0.24 + Math.sin(elapsed * 2.0) * 0.08;
                        ud.headGroup.rotation.z = -0.18;
                    }
                }
            }
        }
    }

    window.KyushuIsland.Characters = {
        CHARACTER_SPECS,
        createCharacter,
        animateCharacterPose
    };
})();
