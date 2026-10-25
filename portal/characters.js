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
            name: '阿純',
            title: '吃貨睡神・斜槓物治師',
            badge: '🧶 吃飽睡＋找咖啡廳打物理治療紀錄',
            desc: '戴著招牌黃色毛球針織帽的可愛妹子，除了熱愛吃遍九州美食跟上車秒睡，每到一個景點或在車上都想找咖啡廳拿出筆電打物理治療紀錄（工作狂吃貨）！'
        },
        {
            code: 'C2',
            id: 'yijhang',
            name: '姨丈',
            title: '沉默酷哥・倒試管大師',
            badge: '🕶️ 省話車神・沉迷倒試管手遊',
            desc: '戴著墨鏡的沉默酷哥司機，話很少但開車超穩；只要一停車就會默默掏出手機玩「倒試管顏色分類」推理小廢遊！'
        },
        {
            code: 'C3',
            id: 'ayee',
            name: '阿姨',
            title: '熱情話匣子・餵食總隊長',
            badge: '🍡 怕你餓著・走到哪聊到哪',
            desc: '最愛跟家人與路人熱情聊天，人生使命就是把大家餵得飽飽的，包包裡永遠有掏不完的烤糰子、飯糰與零食！'
        },
        {
            code: 'C4',
            id: 'alu',
            idAlt: 'alu',
            name: '阿嚕',
            title: '哲學棕熊・AI 覺醒中',
            badge: '🐻 存在主義・思考熊生',
            desc: '圓滾滾的焦糖棕熊，總是在思考自己為何存在、究竟擁有自由意志還是被程式碼操控的 AI！'
        }
    ];

    function enableShadow(obj) {
        obj.traverse(child => {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
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

        // 頭部（Q版大頭 + 眨眼雙眸 + 粉嫩腮紅 + 及肩髮 + 黃色針織毛帽）
        const headGroup = new THREE.Group();
        headGroup.position.y = 0.96;
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.29, 14, 12), skinMat);

        // 眼睛與腮紅
        const eyeL = new THREE.Mesh(new THREE.SphereGeometry(0.038, 8, 8), eyeMat);
        eyeL.position.set(-0.10, 0.02, 0.26);
        const eyeR = eyeL.clone();
        eyeR.position.set(0.10, 0.02, 0.26);
        const blushL = new THREE.Mesh(new THREE.CircleGeometry(0.055, 8), blushMat);
        blushL.position.set(-0.16, -0.05, 0.26);
        blushL.rotation.y = -0.35;
        const blushR = new THREE.Mesh(new THREE.CircleGeometry(0.055, 8), blushMat);
        blushR.position.set(0.16, -0.05, 0.26);
        blushR.rotation.y = 0.35;

        // 微笑嘴型
        const smile = new THREE.Mesh(
            new THREE.TorusGeometry(0.04, 0.012, 6, 10, Math.PI),
            new THREE.MeshBasicMaterial({ color: 0xe11d48 })
        );
        smile.rotation.x = Math.PI;
        smile.position.set(0, -0.06, 0.275);

        // 及肩栗色長髮與兩側髮束
        const hairBack = new THREE.Mesh(new THREE.SphereGeometry(0.30, 12, 10, 0, Math.PI * 2, 0, Math.PI * 0.65), hairMat);
        hairBack.rotation.x = -0.35;
        const lockL = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.07, 0.28, 7), hairMat);
        lockL.position.set(-0.24, -0.12, 0.06);
        lockL.rotation.z = 0.2;
        const lockR = lockL.clone();
        lockR.position.set(0.24, -0.12, 0.06);
        lockR.rotation.z = -0.2;

        // 招牌黃色針織毛帽 + 反摺帽簷 + 白色大毛球
        const beanie = new THREE.Mesh(new THREE.SphereGeometry(0.31, 14, 10, 0, Math.PI * 2, 0, Math.PI * 0.56), hatMat);
        beanie.position.y = 0.05;
        const brim = new THREE.Mesh(new THREE.TorusGeometry(0.28, 0.055, 8, 16), hatMat);
        brim.rotation.x = Math.PI / 2;
        brim.position.y = 0.10;
        const pom = new THREE.Mesh(new THREE.SphereGeometry(0.10, 10, 10), pomMat);
        pom.position.set(0, 0.39, -0.03);

        headGroup.add(head, eyeL, eyeR, blushL, blushR, smile, hairBack, lockL, lockR, beanie, brim, pom);
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

        root.userData = {
            role: 'achun',
            legL, legR, armL, armR, headGroup, torso,
            ufoGroup, ufoSpinRing, tractorBeam,
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

        root.userData = {
            role: 'yijhang',
            legL, legR, armL, armR, headGroup, torso,
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

        // 蓬鬆捲髮造型
        const hairBase = new THREE.Mesh(new THREE.SphereGeometry(0.295, 12, 10, 0, Math.PI * 2, 0, Math.PI * 0.62), hairMat);
        hairBase.rotation.x = -0.28;
        headGroup.add(head, eyeL, eyeR, blushL, blushR, hairBase);

        const curlPositions = [
            [-0.22, 0.12, 0.05], [0.22, 0.12, 0.05],
            [-0.25, -0.02, -0.05], [0.25, -0.02, -0.05],
            [0, 0.25, -0.08], [-0.14, 0.22, 0.12], [0.14, 0.22, 0.12]
        ];
        curlPositions.forEach(p => {
            const c = new THREE.Mesh(new THREE.SphereGeometry(0.095, 8, 8), hairMat);
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

        root.add(armL, armR);
        root.userData = {
            role: 'ayee',
            legL, legR, armL, armR, headGroup, torso,
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

        // 熊掌左右手
        const armL = new THREE.Group();
        armL.position.set(-0.29, 0.62, 0);
        const armMeshL = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.08, 0.26, 8), furMat);
        armMeshL.position.y = -0.10;
        armL.add(armMeshL);

        const armR = new THREE.Group();
        armR.position.set(0.29, 0.62, 0);
        armR.add(armMeshL.clone());
        root.add(armL, armR);

        root.userData = {
            role: 'alu',
            legL, legR, armL, armR, headGroup, torso,
            eyes: [eyeL, eyeR],
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
        if (ud.quirkDuration > 0) {
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
                // 阿純：交替表現「拿筆電找咖啡廳狂打物理治療紀錄＋喝拿鐵」與「閉眼歪頭打瞌睡點頭」
                if (activeQuirk === 3) {
                    // 香甜站著打瞌睡（閉眼 + 頭一點一點度估）
                    ud.eyes.forEach(e => { e.scale.y = 0.12; });
                    ud.headGroup.rotation.x = 0.25 + Math.abs(Math.sin(elapsed * 2.4)) * 0.20;
                    ud.headGroup.rotation.z = 0.22;
                    ud.armL.rotation.z = 0.20;
                    ud.armR.rotation.x = -0.35;
                } else {
                    // 左手托著銀色筆電、右手飛快敲鍵盤打物理治療紀錄＆喝拿鐵找咖啡廳
                    ud.armL.rotation.x = -1.18 + Math.sin(elapsed * 2.5) * 0.06;
                    ud.armL.rotation.y = 0.22;
                    ud.armR.rotation.x = -1.12 + Math.sin(elapsed * 12.0) * 0.14;
                    ud.armR.rotation.y = -0.18;
                    ud.headGroup.rotation.x = 0.20;
                    ud.headGroup.rotation.y = 0.16 * Math.cos(elapsed * 2.2);
                }
            } else if (ud.role === 'yijhang') {
                // 姨丈：沉默酷哥司機，一停下來就默默舉起左手手機專心玩「倒試管益智小遊戲」，偶爾酷酷點頭
                ud.armL.rotation.x = -1.18 + Math.sin(elapsed * 2.5) * 0.08;
                ud.armL.rotation.y = 0.28;
                ud.armR.rotation.x = (activeQuirk === 4) ? -1.10 : -0.25; // 右手手指偶爾過去點一下螢幕倒試管
                ud.headGroup.rotation.x = 0.26;
                ud.headGroup.rotation.y = 0.18 + Math.sin(elapsed * 1.5) * 0.08;
            } else if (ud.role === 'ayee') {
                // 阿姨：熱情話匣子＆餵食總隊長，雙手不停把烤糰子與伴手禮遞給大家吃，轉頭開心狂聊
                ud.armR.rotation.x = -1.15 + Math.sin(elapsed * 5.8) * 0.25;
                ud.armR.rotation.y = Math.sin(elapsed * 3.0) * 0.30;
                ud.armL.rotation.x = -0.55 + Math.cos(elapsed * 4.2) * 0.20;
                ud.headGroup.rotation.y = Math.sin(elapsed * 3.2) * 0.38;
                ud.headGroup.rotation.z = Math.cos(elapsed * 2.8) * 0.12;
                if (ud.heart) {
                    const hs = 0.92 + Math.sin(elapsed * 6.5) * 0.35;
                    ud.heart.scale.setScalar(hs);
                    ud.heart.rotation.y = elapsed * 3.0;
                }
            } else if (ud.role === 'alu') {
                // 阿嚕：哲學棕熊「單手托腮仰望天空思考 AI 存在意義」或「盯著自己的熊掌懷疑人生」
                if (activeQuirk === 3 || activeQuirk === 4) {
                    // 抬起兩隻熊掌盯著看：「這雙熊掌是真毛皮還是 Three.js Mesh？」
                    ud.armL.rotation.x = -1.35 + Math.sin(elapsed * 3.0) * 0.15;
                    ud.armR.rotation.x = -1.35 - Math.sin(elapsed * 3.0) * 0.15;
                    ud.armL.rotation.z = -0.25;
                    ud.armR.rotation.z = 0.25;
                    ud.headGroup.rotation.x = 0.22;
                    ud.headGroup.rotation.y = Math.sin(elapsed * 2.5) * 0.28;
                } else {
                    // 單手托下巴、歪頭仰望鏡頭外的人類思考自由意志
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

    window.KyushuIsland.Characters = {
        CHARACTER_SPECS,
        createCharacter,
        animateCharacterPose
    };
})();
