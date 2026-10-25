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
            title: '行程總召・可愛妹子',
            badge: '🧶 黃色毛帽・自拍達人',
            desc: '戴著招牌黃色毛球針織帽與溫暖圍巾，負責規劃全家人南九州行程與沿途自拍紀錄！'
        },
        {
            code: 'C2',
            id: 'yijhang',
            name: '姨丈',
            title: '王牌駕駛・專業司機',
            badge: '🕶️ 帥氣墨鏡・雪地老司機',
            desc: '戴著招牌墨鏡穩握方向盤，一路征服阿蘇山路、高千穗與日南海岸的可靠車長！'
        },
        {
            code: 'C3',
            id: 'ayee',
            name: '阿姨',
            title: '美食鑑賞・溫柔擔當',
            badge: '🍡 美食雷達・伴手禮女王',
            desc: '笑容和藹親切，手提滿滿九州名產紙袋，走到哪吃到哪（烤糰子、馬肉可樂餅、鰻魚飯）！'
        },
        {
            code: 'C4',
            id: 'alu',
            idAlt: 'alu',
            name: '阿嚕',
            title: '吉祥物・貪吃棕熊',
            badge: '🐻 圓滾棕熊・泡湯愛好者',
            desc: '圓滾滾的焦糖棕熊，圍著紅圍巾搖擺散步，最愛摸肚子討東西吃跟泡黑川溫泉！'
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

        // 左右手臂（右手拿智慧型手機自拍）
        const armL = new THREE.Group();
        armL.position.set(-0.25, 0.66, 0);
        const armMeshL = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.05, 0.28, 8), coatMat);
        armMeshL.position.y = -0.11;
        armL.add(armMeshL);

        const armR = new THREE.Group();
        armR.position.set(0.25, 0.66, 0);
        const armMeshR = armMeshL.clone();
        const phone = new THREE.Mesh(
            new THREE.BoxGeometry(0.08, 0.14, 0.02),
            new THREE.MeshBasicMaterial({ color: 0x38bdf8 })
        );
        phone.position.set(0, -0.24, 0.08);
        phone.rotation.x = -0.5;
        armR.add(armMeshR, phone);
        root.add(armL, armR);

        root.userData = {
            role: 'achun',
            legL, legR, armL, armR, headGroup, torso,
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

        // 左右手（右手握迷你方向盤/車鑰匙圈）
        const armL = new THREE.Group();
        armL.position.set(-0.28, 0.70, 0);
        const armMeshL = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.055, 0.30, 8), jacketMat);
        armMeshL.position.y = -0.12;
        armL.add(armMeshL);

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

    // 更新單一角色的精緻動作（走路擺臂、眨眼、以及依角色觸發專屬動作）
    function animateCharacterPose(charGroup, elapsed, delta, isWalking) {
        const ud = charGroup.userData;
        if (!ud) return;

        const phase = elapsed * 6.5 + (ud.actionPhase || 0);

        // 1. 自然眨眼 (每 3.8 秒眨眼一次)
        if (ud.eyes && ud.eyes.length) {
            const blinkWindow = (elapsed + (ud.actionPhase || 0)) % 3.8;
            const eyeScaleY = (blinkWindow > 3.65) ? 0.12 : 1.0;
            ud.eyes.forEach(e => { e.scale.y = eyeScaleY; });
        }

        // 2. 點擊彈跳或歡呼跳躍
        let jumpOffset = 0;
        if (ud.jumping > 0) {
            ud.jumping = Math.max(0, ud.jumping - delta * 2.1);
            jumpOffset = Math.sin(ud.jumping * Math.PI) * 0.65;
        }

        if (isWalking) {
            // 行走時四肢擺動與輕快彈跳
            const stride = Math.sin(phase) * 0.55;
            ud.legL.rotation.x = stride;
            ud.legR.rotation.x = -stride;
            ud.armL.rotation.x = -stride * 0.75;
            ud.armR.rotation.x = stride * 0.75;
            ud.torso.rotation.z = Math.cos(phase) * 0.05;
            ud.headGroup.rotation.z = Math.sin(phase * 0.5) * 0.06;
            ud.headGroup.rotation.y = Math.sin(elapsed * 1.4 + ud.actionPhase) * 0.18;
            charGroup.position.y = (ud.baseY || 0.76) + Math.abs(Math.sin(phase)) * 0.08 + jumpOffset;
        } else {
            // 抵達景點下車散步 / 專屬待機動作
            ud.legL.rotation.x = Math.sin(phase * 0.5) * 0.15;
            ud.legR.rotation.x = -Math.sin(phase * 0.5) * 0.15;
            charGroup.position.y = (ud.baseY || 0.76) + Math.abs(Math.sin(phase * 0.5)) * 0.04 + jumpOffset;

            if (ud.role === 'achun') {
                // 阿純：高舉右手拿手機自拍 + 左手雀躍揮手
                ud.armR.rotation.x = -1.15 + Math.sin(elapsed * 4.0) * 0.12;
                ud.armL.rotation.z = 0.65 + Math.sin(elapsed * 6.0) * 0.35;
                ud.headGroup.rotation.z = 0.12 * Math.sin(elapsed * 2.5);
            } else if (ud.role === 'yijhang') {
                // 姨丈：專業司機伸懶腰、轉動方向盤與比讚點頭
                ud.armR.rotation.x = -0.75 + Math.sin(elapsed * 3.0) * 0.25;
                ud.armL.rotation.x = -0.35;
                ud.headGroup.rotation.y = Math.sin(elapsed * 1.8) * 0.28;
            } else if (ud.role === 'ayee') {
                // 阿姨：把烤糰子湊近嘴邊品嚐 + 頭頂愛心放大跳動
                ud.armR.rotation.x = -0.95 + Math.sin(elapsed * 4.5) * 0.18;
                ud.armL.rotation.x = 0.15;
                if (ud.heart) {
                    const hs = 0.85 + Math.sin(elapsed * 5.5) * 0.28;
                    ud.heart.scale.setScalar(hs);
                    ud.heart.rotation.y = elapsed * 2.5;
                }
            } else if (ud.role === 'alu') {
                // 阿嚕：搖晃圓滾滾身軀、雙掌拍肚子
                ud.torso.rotation.z = Math.sin(elapsed * 4.0) * 0.12;
                ud.armL.rotation.z = 0.35 + Math.sin(elapsed * 5.0) * 0.20;
                ud.armR.rotation.z = -0.35 - Math.sin(elapsed * 5.0) * 0.20;
                ud.headGroup.rotation.z = Math.sin(elapsed * 3.0) * 0.14;
            }
        }
    }

    window.KyushuIsland.Characters = {
        CHARACTER_SPECS,
        createCharacter,
        animateCharacterPose
    };
})();
