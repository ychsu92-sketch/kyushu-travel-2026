/**
 * portal/terrain.js
 * 南九州真實輪廓 2.5D 浮空島地形系統（立體等高線階梯 & 豐富地貌紋理升級版）：
 * - 打破單一扁平平面：採用「4 層立體等高線階梯台地 (Stepped Contour Terraces)」+「多面體稜角山巒」+「球磨川/筑後川/大淀川水系」+「農田/茶園/火山灰地貌拼布」
 * - 雙重程序化立體貼圖 (Procedural Canvas Bump + Color Texture) 結合多色階層，呈現如手工微縮模型般的溫潤 2.5D 質感
 * - 真實切入錦江灣，櫻島獨立於海灣中央，外圍環繞天草群島
 * - 北側切口呈現浮空島塊幾何岩壁斷面與覆雪山脊
 * - 環島自駕公路（加寬並附木製護欄與里程路標）、櫻島渡輪航道、熊本路面電車軌道
 */
(function () {
    window.KyushuIsland = window.KyushuIsland || {};

    // 建立程序化微縮模型地表貼圖 (含草地雜訊顆粒、微光斑駁感、凹凸紋理)
    function createMicroTerrainTexture(baseHex, accentHex, grainOpacity) {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 256;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = baseHex;
        ctx.fillRect(0, 0, 256, 256);

        // 繪製柔和有機色塊斑紋
        for (let i = 0; i < 90; i++) {
            const x = Math.random() * 256;
            const y = Math.random() * 256;
            const r = 10 + Math.random() * 28;
            ctx.fillStyle = accentHex;
            ctx.globalAlpha = grainOpacity * 0.55;
            ctx.beginPath();
            ctx.arc(x, y, r, 0, Math.PI * 2);
            ctx.fill();
        }

        // 繪製細緻草地顆粒與等高線微網格
        for (let i = 0; i < 1400; i++) {
            const x = Math.random() * 256;
            const y = Math.random() * 256;
            ctx.fillStyle = (i % 2 === 0) ? '#ffffff' : '#2d3a24';
            ctx.globalAlpha = grainOpacity * 0.35;
            ctx.fillRect(x, y, 2, 2);
        }

        const tex = new THREE.CanvasTexture(canvas);
        tex.wrapS = THREE.RepeatWrapping;
        tex.wrapT = THREE.RepeatWrapping;
        tex.repeat.set(0.35, 0.35);
        return tex;
    }

    // 計算任一 (x, z) 在南九州地表上的基礎海拔高度 (供物件、景點與道路自動貼合高低起伏)
    function getTerrainElevation(x, z) {
        let h = 0.78;
        const regions = [
            { x: 3.28,  z: -12.94, r: 3.6, amp: 0.85 }, // 阿蘇高地
            { x: 4.09,  z: -16.14, r: 3.2, amp: 0.75 }, // 黑川・九重高原
            { x: 6.30,  z: -9.98,  r: 3.4, amp: 0.70 }, // 高千穗山地
            { x: 2.20,  z: -5.20,  r: 4.5, amp: 0.82 }, // 九州中央山地
            { x: 0.29,  z: 3.99,   r: 3.0, amp: 0.72 }, // 霧島山塊
            { x: -2.70, z: 8.50,   r: 1.2, amp: 0.55 }  // 櫻島台地
        ];
        for (let i = 0; i < regions.length; i++) {
            const p = regions[i];
            const d2 = (x - p.x) * (x - p.x) + (z - p.z) * (z - p.z);
            const r2 = p.r * p.r;
            if (d2 < r2 * 2.2) {
                h += p.amp * Math.exp(-d2 / r2);
            }
        }
        return h;
    }

    function createPolygonShape(pts, scaleFactor, centerOffset) {
        const shape = new THREE.Shape();
        if (!pts || !pts.length) return shape;
        const sf = scaleFactor || 1.0;
        const cx = centerOffset ? centerOffset[0] : 0.8;
        const cz = centerOffset ? centerOffset[1] : -2.0;

        for (let i = 0; i < pts.length; i++) {
            const px = cx + (pts[i][0] - cx) * sf;
            const pz = cz + (pts[i][1] - cz) * sf;
            if (i === 0) shape.moveTo(px, -pz);
            else shape.lineTo(px, -pz);
        }
        shape.closePath();
        return shape;
    }

    function buildLayeredLandmass(pts, options) {
        const group = new THREE.Group();
        const shape = createPolygonShape(pts, 1.0, options.center);

        // 1. 最外圈雙層動態岸邊白浪環 (Foam Rim)
        const foamGeo = new THREE.ExtrudeGeometry(shape, {
            depth: 0.14,
            bevelEnabled: true,
            bevelSegments: 2,
            steps: 1,
            bevelSize: 0.52,
            bevelThickness: 0.06
        });
        foamGeo.rotateX(-Math.PI / 2);
        const foamMat = new THREE.MeshBasicMaterial({
            color: 0xf8fafc,
            transparent: true,
            opacity: 0.72
        });
        const foamMesh = new THREE.Mesh(foamGeo, foamMat);
        foamMesh.position.y = -0.31;
        group.add(foamMesh);

        // 2. 暖米金海岸沙灘與礁岩層 (Warm Sand & Coastal Shelf)
        const sandGeo = new THREE.ExtrudeGeometry(shape, {
            depth: 0.30,
            bevelEnabled: true,
            bevelSegments: 2,
            steps: 1,
            bevelSize: 0.30,
            bevelThickness: 0.14
        });
        sandGeo.rotateX(-Math.PI / 2);
        const sandMat = new THREE.MeshLambertMaterial({
            color: 0xe7d3b0,
            flatShading: true
        });
        const sandMesh = new THREE.Mesh(sandGeo, sandMat);
        sandMesh.position.y = -0.22;
        sandMesh.receiveShadow = true;
        group.add(sandMesh);

        // 3. 浮空島下層雙色岩壁斷面 (Upper Hinoki Terracotta + Lower Deep Basalt)
        const cliffDepth = options.cliffDepth || 1.85;
        const cliffGeo = new THREE.ExtrudeGeometry(shape, {
            depth: cliffDepth,
            bevelEnabled: true,
            bevelSegments: 3,
            steps: 3,
            bevelSize: 0.14,
            bevelThickness: 0.22
        });
        cliffGeo.rotateX(-Math.PI / 2);

        // 對岩壁頂點做有機凹凸擾動與底部收斂，讓斷面呈現立體低多邊形岩石稜角
        const cPos = cliffGeo.attributes.position;
        for (let i = 0; i < cPos.count; i++) {
            const px = cPos.getX(i);
            const py = cPos.getY(i);
            const pz = cPos.getZ(i);
            if (py < 0.35) {
                const taper = 0.88 + (py / cliffDepth) * 0.12;
                const jitter = Math.sin(px * 1.7 + pz * 1.3) * 0.08;
                cPos.setX(i, px * taper + jitter);
                cPos.setZ(i, pz * taper - jitter);
            }
        }
        cliffGeo.computeVertexNormals();

        const cliffTex = createMicroTerrainTexture(options.cliffHex || '#8c583a', '#6e4023', 0.28);
        const cliffMat = new THREE.MeshLambertMaterial({
            color: 0xffffff,
            map: cliffTex,
            flatShading: true
        });
        const cliffMesh = new THREE.Mesh(cliffGeo, cliffMat);
        cliffMesh.position.y = -1.25;
        cliffMesh.castShadow = true;
        cliffMesh.receiveShadow = true;
        group.add(cliffMesh);

        // 4. 第一階：沿海平原草地層 (Coastal Lowland Meadow - 柔和暖抹茶綠)
        const turfTex1 = createMicroTerrainTexture(options.turfHex1 || '#88a66e', '#6f8f56', 0.32);
        const turfGeo1 = new THREE.ExtrudeGeometry(shape, {
            depth: 0.28,
            bevelEnabled: true,
            bevelSegments: 2,
            steps: 1,
            bevelSize: 0.06,
            bevelThickness: 0.12
        });
        turfGeo1.rotateX(-Math.PI / 2);
        const turfMat1 = new THREE.MeshStandardMaterial({
            color: 0xffffff,
            map: turfTex1,
            bumpMap: turfTex1,
            bumpScale: 0.04,
            roughness: 0.88,
            metalness: 0.02,
            flatShading: true
        });
        const turfMesh1 = new THREE.Mesh(turfGeo1, turfMat1);
        turfMesh1.position.y = 0.48;
        turfMesh1.castShadow = true;
        turfMesh1.receiveShadow = true;
        group.add(turfMesh1);

        // 5. 第二階與第三階：內陸等高線階梯台地 (Stepped Contour Terraces - 解決扁平單調感！)
        if (options.enableTerraces) {
            // 第二階：內陸丘陵台地 (縮放 0.82，深一階的冬日橄欖抹茶色)
            const shapeT2 = createPolygonShape(pts, 0.82, options.center);
            const geoT2 = new THREE.ExtrudeGeometry(shapeT2, {
                depth: 0.24,
                bevelEnabled: true,
                bevelSegments: 2,
                steps: 1,
                bevelSize: 0.08,
                bevelThickness: 0.10
            });
            geoT2.rotateX(-Math.PI / 2);
            const texT2 = createMicroTerrainTexture('#73915c', '#5c7847', 0.35);
            const matT2 = new THREE.MeshStandardMaterial({
                color: 0xffffff,
                map: texT2,
                bumpMap: texT2,
                bumpScale: 0.05,
                roughness: 0.90,
                flatShading: true
            });
            const meshT2 = new THREE.Mesh(geoT2, matT2);
            meshT2.position.y = 0.72;
            meshT2.castShadow = true;
            meshT2.receiveShadow = true;
            group.add(meshT2);

            // 第三階：中央山麓高原層 (縮放 0.60，暖褐枯草高地色)
            const shapeT3 = createPolygonShape(pts, 0.60, [1.8, -4.5]);
            const geoT3 = new THREE.ExtrudeGeometry(shapeT3, {
                depth: 0.26,
                bevelEnabled: true,
                bevelSegments: 2,
                steps: 1,
                bevelSize: 0.10,
                bevelThickness: 0.12
            });
            geoT3.rotateX(-Math.PI / 2);
            const texT3 = createMicroTerrainTexture('#688252', '#8a795d', 0.38);
            const matT3 = new THREE.MeshStandardMaterial({
                color: 0xffffff,
                map: texT3,
                bumpMap: texT3,
                bumpScale: 0.06,
                roughness: 0.92,
                flatShading: true
            });
            const meshT3 = new THREE.Mesh(geoT3, matT3);
            meshT3.position.y = 0.96;
            meshT3.castShadow = true;
            meshT3.receiveShadow = true;
            group.add(meshT3);
        }

        return { group, turfMesh: turfMesh1, cliffMesh, foamMesh };
    }

    // 建立地貌拼布細節：農田/茶園方塊、冬季枯黃芒草原、球磨川與大淀川蜿蜒溪流、海岸礁石
    function buildBiomePatchesAndRivers(parent) {
        const biomeGroup = new THREE.Group();

        // 1. 田園拼布色塊 (熊本平原、人吉盆地、宮崎平原、知覽茶園)
        const patchDefs = [
            // 熊本與菊池平原農田
            { x: -0.9, z: -10.2, w: 1.6, d: 1.1, rot: 0.2,  color: 0x9cb376, y: 0.80 },
            { x: 0.6,  z: -10.8, w: 1.4, d: 1.0, rot: -0.15,color: 0xb5a876, y: 0.80 },
            { x: -2.2, z: -9.5,  w: 1.3, d: 0.9, rot: 0.35, color: 0x829e65, y: 0.80 },
            // 阿蘇草千里與牛奶之路冬日金黃枯草原
            { x: 2.2,  z: -13.6, w: 2.2, d: 1.5, rot: 0.1,  color: 0xc2a878, y: 1.02 },
            { x: 4.5,  z: -14.2, w: 1.8, d: 1.3, rot: -0.3, color: 0xb89f72, y: 1.02 },
            // 人吉球磨盆地與霧島山麓茶園
            { x: -0.6, z: -2.2,  w: 1.9, d: 1.4, rot: 0.25, color: 0x8fa868, y: 1.02 },
            { x: -1.8, z: 1.8,   w: 1.7, d: 1.2, rot: -0.2, color: 0x9ab372, y: 0.82 },
            // 薩摩半島知覽茶園與指宿菜の花田（冬季暖黃綠）
            { x: -4.6, z: 9.8,   w: 1.6, d: 1.3, rot: 0.18, color: 0xa3bd6a, y: 0.80 },
            { x: -4.2, z: 11.4,  w: 1.4, d: 1.0, rot: -0.1, color: 0xd4be6a, y: 0.80 },
            // 大隅半島與宮崎日南陽光草坡
            { x: 0.6,  z: 9.2,   w: 2.0, d: 1.5, rot: -0.25,color: 0x8ca668, y: 0.80 },
            { x: 6.8,  z: 1.5,   w: 1.8, d: 2.2, rot: 0.12, color: 0x96b070, y: 0.82 },
            { x: 5.5,  z: -3.5,  w: 2.1, d: 1.6, rot: -0.2, color: 0x7d965e, y: 1.02 }
        ];

        patchDefs.forEach(p => {
            const pg = new THREE.Group();
            const base = new THREE.Mesh(
                new THREE.BoxGeometry(p.w, 0.08, p.d),
                new THREE.MeshLambertMaterial({ color: p.color, flatShading: true })
            );
            pg.add(base);
            // 田畦條紋細節
            const stripeMat = new THREE.MeshLambertMaterial({ color: 0x657d4c });
            for (let s = -2; s <= 2; s++) {
                const stripe = new THREE.Mesh(new THREE.BoxGeometry(p.w * 0.88, 0.095, 0.07), stripeMat);
                stripe.position.z = s * (p.d * 0.18);
                pg.add(stripe);
            }
            pg.position.set(p.x, p.y, p.z);
            pg.rotation.y = p.rot;
            pg.receiveShadow = true;
            biomeGroup.add(pg);
        });

        // 2. 南九州三大水系（五瀨川/高千穗溪流、球磨川、大淀川）閃耀藍色河帶
        const riverMat = new THREE.MeshPhongMaterial({
            color: 0x38bdf8,
            emissive: 0x0284c7,
            emissiveIntensity: 0.15,
            shininess: 60
        });
        const rivers = [
            // 球磨川 (從九州山地流經人吉盆地注入八代海)
            [
                new THREE.Vector3(2.2, 1.15, -3.5),
                new THREE.Vector3(0.4, 1.05, -2.4),
                new THREE.Vector3(-1.3, 0.90, -1.8),
                new THREE.Vector3(-2.6, 0.78, -3.2)
            ],
            // 五瀨川 (從阿蘇高千穗流向延岡日向灘)
            [
                new THREE.Vector3(4.2, 1.15, -11.5),
                new THREE.Vector3(6.3, 1.02, -9.9),
                new THREE.Vector3(8.2, 0.82, -8.5)
            ],
            // 大淀川 (從都城盆地流向宮崎海岸)
            [
                new THREE.Vector3(2.5, 1.02, 3.2),
                new THREE.Vector3(5.6, 0.90, 2.8),
                new THREE.Vector3(8.5, 0.78, 2.5)
            ]
        ];

        rivers.forEach(pts => {
            const curve = new THREE.CatmullRomCurve3(pts);
            const tubeGeo = new THREE.TubeGeometry(curve, 24, 0.14, 6, false);
            tubeGeo.scale(1.0, 0.22, 1.0);
            const rMesh = new THREE.Mesh(tubeGeo, riverMat);
            rMesh.position.y = 0.62;
            biomeGroup.add(rMesh);
        });

        parent.add(biomeGroup);
    }

    // 建立北側「浮空島斷面岩層」與地層紋理塊
    function buildNorthernStrataWall(parent, mainlandPts) {
        const strataGroup = new THREE.Group();
        const darkRockMat = new THREE.MeshLambertMaterial({ color: 0x6e4228, flatShading: true });
        const midRockMat  = new THREE.MeshLambertMaterial({ color: 0x9c6b49, flatShading: true });
        const snowCapMat  = new THREE.MeshLambertMaterial({ color: 0xf8fafc, flatShading: true });

        for (let i = 0; i < mainlandPts.length; i += 2) {
            const pt = mainlandPts[i];
            if (pt[1] < -12.5) {
                const rock = new THREE.Mesh(
                    new THREE.DodecahedronGeometry(0.55 + (i % 3) * 0.18, 0),
                    i % 2 === 0 ? darkRockMat : midRockMat
                );
                rock.scale.set(1.3, 1.85, 1.0);
                rock.position.set(pt[0], -0.10 - (i % 3) * 0.18, pt[1] - 0.12);
                rock.rotation.set(i * 0.3, i * 0.5, 0);
                rock.castShadow = true;
                rock.receiveShadow = true;
                strataGroup.add(rock);

                if (pt[0] > 0.5) {
                    const snow = new THREE.Mesh(
                        new THREE.ConeGeometry(0.58, 0.45, 6),
                        snowCapMat
                    );
                    snow.position.set(pt[0], 0.92, pt[1] + 0.18);
                    snow.receiveShadow = true;
                    strataGroup.add(snow);
                }
            }
        }
        parent.add(strataGroup);
    }

    // 建立立體感十足的九州連綿山脈與 12 月冬季覆雪高地群（嚴格退縮避開自駕路線與景點，杜絕穿模）
    function buildMountainRanges(parent, roadCurve, landmarks) {
        const hillGroup = new THREE.Group();
        const winterOliveMat = new THREE.MeshLambertMaterial({ color: 0x658352, flatShading: true });
        const highlandMat    = new THREE.MeshLambertMaterial({ color: 0x7c9668, flatShading: true });
        const rockSlopeMat   = new THREE.MeshLambertMaterial({ color: 0x78685a, flatShading: true });
        const snowMat        = new THREE.MeshLambertMaterial({ color: 0xf8fafc, flatShading: true });

        // 預先取樣自駕路線所有點，用來限制山腳半徑不壓到公路或景點
        const routeSamples = [];
        if (roadCurve) {
            for (let i = 0; i < 200; i++) {
                routeSamples.push(roadCurve.getPointAt(i / 200));
            }
        }

        const ranges = [
            // 北部：九重連山與黑川後山（退至路線北側外圍）
            { x: 5.5,  z: -15.8, r: 1.35, h: 1.25, snow: true,  rocky: true },
            { x: 1.3,  z: -15.2, r: 1.35, h: 1.05, snow: true,  rocky: false },
            // 阿蘇外輪山與祖母傾山（退至路線外側）
            { x: 5.6,  z: -12.8, r: 1.35, h: 1.18, snow: true,  rocky: true },
            { x: 7.7,  z: -10.5, r: 1.35, h: 1.15, snow: true,  rocky: true },
            // 九州脊樑山地（位於東側宮崎公路與西側人吉公路正中央的無人山區，絕不碰觸兩側道路）
            { x: 3.8,  z: -8.2,  r: 1.75, h: 1.22, snow: true,  rocky: false },
            { x: 2.2,  z: -6.8,  r: 1.95, h: 1.38, snow: true,  rocky: true },
            { x: 4.5,  z: -5.5,  r: 1.85, h: 1.22, snow: true,  rocky: false },
            { x: 1.8,  z: -4.2,  r: 1.75, h: 1.15, snow: true,  rocky: false },
            { x: 4.6,  z: -2.8,  r: 1.80, h: 0.98, snow: false, rocky: false },
            { x: 2.8,  z: -0.6,  r: 1.65, h: 0.92, snow: false, rocky: false },
            { x: 4.8,  z: 1.2,   r: 1.60, h: 0.88, snow: false, rocky: false },
            // 霧島連山（位於霧島神宮東側後山）
            { x: 2.2,  z: 3.6,   r: 1.45, h: 1.28, snow: true,  rocky: true },
            // 薩摩半島（開聞岳/薩摩富士 & 金峰山）與大隅半島（高隈山）
            { x: -5.1, z: 10.6,  r: 1.35, h: 0.78, snow: false, rocky: false },
            { x: -3.9, z: 12.6,  r: 1.05, h: 1.15, snow: true,  rocky: true },
            { x: 0.5,  z: 10.4,  r: 1.65, h: 0.88, snow: false, rocky: false },
            { x: -0.6, z: 12.2,  r: 1.45, h: 0.72, snow: false, rocky: false }
        ];

        ranges.forEach((m, idx) => {
            // 自動安全檢查：若山體邊緣太靠近自駕道路或景點，自動縮小山腳半徑留出安全走廊
            let safeR = m.r;
            routeSamples.forEach(rp => {
                const dist = Math.hypot(m.x - rp.x, m.z - rp.z);
                if (dist - 0.85 < safeR) {
                    safeR = Math.max(0.55, dist - 0.85);
                }
            });
            if (landmarks) {
                landmarks.forEach(lm => {
                    const dist = Math.hypot(m.x - lm.x, m.z - lm.z);
                    if (dist - 1.10 < safeR) {
                        safeR = Math.max(0.55, dist - 1.10);
                    }
                });
            }

            const mGroup = new THREE.Group();

            // 1. 第一層寬闊山麓台地
            const base = new THREE.Mesh(
                new THREE.CylinderGeometry(safeR * 0.70, safeR, m.h * 0.48, 7),
                idx % 2 === 0 ? winterOliveMat : highlandMat
            );
            base.position.y = m.h * 0.24;
            base.rotation.y = idx * 0.8;
            mGroup.add(base);

            // 2. 第二層立體山腰（岩石或深林）
            const mid = new THREE.Mesh(
                new THREE.CylinderGeometry(safeR * 0.40, safeR * 0.72, m.h * 0.42, 7),
                m.rocky ? rockSlopeMat : winterOliveMat
            );
            mid.position.y = m.h * 0.65;
            mid.rotation.y = idx * 0.8 + 0.3;
            mGroup.add(mid);

            // 3. 第三層山峰與 12 月冬季皚皚白雪冠
            if (m.snow) {
                const snowCap = new THREE.Mesh(
                    new THREE.ConeGeometry(safeR * 0.44, m.h * 0.48, 7),
                    snowMat
                );
                snowCap.position.y = m.h * 1.02;
                snowCap.rotation.y = idx * 0.8;
                mGroup.add(snowCap);
            } else {
                const greenPeak = new THREE.Mesh(
                    new THREE.ConeGeometry(safeR * 0.42, m.h * 0.38, 7),
                    highlandMat
                );
                greenPeak.position.y = m.h * 0.98;
                greenPeak.rotation.y = idx * 0.8;
                mGroup.add(greenPeak);
            }

            mGroup.position.set(m.x, 0.78, m.z);
            mGroup.traverse(c => {
                if (c.isMesh) {
                    c.castShadow = true;
                    c.receiveShadow = true;
                }
            });
            hillGroup.add(mGroup);
        });

        parent.add(hillGroup);
    }

    // 建立環島自駕公路、櫻島渡輪航道與熊本市電軌道（支援隨等高線階梯自動升降高度）
    function buildRoadsAndTracks(parent, routeData, sampleGroundY) {
        const roadGroup = new THREE.Group();

        const curvePoints = routeData.route.map(pt => {
            if (pt.mode === 'ferry') {
                return new THREE.Vector3(pt.x, 0.12, pt.z);
            }
            const gy = sampleGroundY ? sampleGroundY(pt.x, pt.z) : 0.86;
            return new THREE.Vector3(pt.x, gy + 0.04, pt.z);
        });
        const roadCurve = new THREE.CatmullRomCurve3(curvePoints, true, 'catmullrom', 0.35);

        const roadMat = new THREE.MeshLambertMaterial({ color: 0x64748b });
        const curbMat = new THREE.MeshLambertMaterial({ color: 0xe2e8f0 });
        const dashMat = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
        const ferryBuoyMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });

        const samples = 300;
        for (let i = 0; i < samples; i++) {
            const t = i / samples;
            const pos = roadCurve.getPointAt(t);
            const tangent = roadCurve.getTangentAt(t);
            const angle = Math.atan2(tangent.x, tangent.z);

            const isFerryWater = (pos.x > -3.80 && pos.x < -2.55 && pos.z > 8.15 && pos.z < 8.85);

            if (isFerryWater) {
                if (i % 3 === 0) {
                    const buoy = new THREE.Mesh(new THREE.SphereGeometry(0.08, 6, 6), ferryBuoyMat);
                    buoy.position.set(pos.x, 0.05, pos.z);
                    roadGroup.add(buoy);
                }
            } else {
                const gy = sampleGroundY ? sampleGroundY(pos.x, pos.z) : 0.80;
                const curb = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.06, 0.42), curbMat);
                curb.position.set(pos.x, gy + 0.02, pos.z);
                curb.rotation.y = angle;
                curb.receiveShadow = true;
                roadGroup.add(curb);

                const seg = new THREE.Mesh(new THREE.BoxGeometry(0.56, 0.07, 0.40), roadMat);
                seg.position.set(pos.x, gy + 0.035, pos.z);
                seg.rotation.y = angle;
                seg.receiveShadow = true;
                roadGroup.add(seg);

                if (i % 2 === 0) {
                    const dash = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 0.18), dashMat);
                    dash.position.set(pos.x, gy + 0.042, pos.z);
                    dash.rotation.y = angle;
                    roadGroup.add(dash);
                }
            }
        }

        // 熊本路面電車專用軌道
        const tramPts = routeData.tram_line.map(p => {
            const gy = sampleGroundY ? sampleGroundY(p.x, p.z) : 0.82;
            return new THREE.Vector3(p.x, gy + 0.04, p.z);
        });
        const tramCurve = new THREE.CatmullRomCurve3(tramPts, false);
        const railMat = new THREE.MeshLambertMaterial({ color: 0x475569 });
        const sleeperMat = new THREE.MeshLambertMaterial({ color: 0x78350f });

        for (let i = 0; i <= 38; i++) {
            const t = i / 38;
            const p = tramCurve.getPointAt(t);
            const tan = tramCurve.getTangentAt(t);
            const ang = Math.atan2(tan.x, tan.z);
            const gy = sampleGroundY ? sampleGroundY(p.x, p.z) : 0.80;

            const sleeper = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.05, 0.10), sleeperMat);
            sleeper.position.set(p.x, gy + 0.025, p.z);
            sleeper.rotation.y = ang;
            roadGroup.add(sleeper);

            const rail = new THREE.Mesh(new THREE.BoxGeometry(0.30, 0.06, 0.16), railMat);
            rail.position.set(p.x, gy + 0.035, p.z);
            rail.rotation.y = ang;
            roadGroup.add(rail);
        }

        parent.add(roadGroup);
        return { roadCurve, tramCurve, roadGroup };
    }

    function buildSouthKyushuTerrain(scene, coastData, routeData) {
        const root = new THREE.Group();

        // 1. 南九州主島（含 3 層立體等高線階梯台地 + 程序化微縮模型凹凸貼圖）
        const mainland = buildLayeredLandmass(coastData.mainland, {
            turfHex1: '#86a56c',
            cliffHex: '#8c583a',
            cliffDepth: 1.95,
            enableTerraces: true,
            center: [0.8, -2.0]
        });
        root.add(mainland.group);

        // 2. 錦江灣中央的櫻島活火山島
        const sakurajima = buildLayeredLandmass(coastData.sakurajima, {
            turfHex1: '#688253',
            cliffHex: '#5c4033',
            cliffDepth: 1.65,
            enableTerraces: false,
            center: [-2.7, 8.5]
        });
        root.add(sakurajima.group);

        // 3. 西側天草群島
        if (coastData.amakusa) {
            coastData.amakusa.forEach(poly => {
                const ama = buildLayeredLandmass(poly, {
                    turfHex1: '#8ba872',
                    cliffHex: '#936040',
                    cliffDepth: 1.45,
                    enableTerraces: false
                });
                root.add(ama.group);
            });
        }

        // 4. 田園/茶園/枯草原拼布與球磨川等三大水系
        buildBiomePatchesAndRivers(root);

        // 建立垂直向下 Raycaster 地面高度取樣器（確保道路、小巴、4位家人、貓狗路人與景點永遠貼合真實等高線台地表面，絕不陷入地表！）
        root.updateMatrixWorld(true);
        const groundRaycaster = new THREE.Raycaster();
        const downDir = new THREE.Vector3(0, -1, 0);
        const rayOrigin = new THREE.Vector3();
        const groundTargets = [mainland.group, sakurajima.group];

        function sampleGroundY(x, z) {
            // 錦江灣渡輪水道
            if (x > -3.80 && x < -2.55 && z > 8.15 && z < 8.85) {
                return 0.12;
            }
            rayOrigin.set(x, 12.0, z);
            groundRaycaster.set(rayOrigin, downDir);
            const hits = groundRaycaster.intersectObjects(groundTargets, true);
            if (hits.length > 0) {
                return Math.max(0.76, hits[0].point.y);
            }
            return 0.78;
        }

        // 5. 環島自駕公路與路面電車軌道（先鋪設道路，再根據道路安全距離放山脈）
        const roads = buildRoadsAndTracks(root, routeData, sampleGroundY);

        // 6. 北側浮空島斷面岩層與全島立體山脈群（自動避開道路與景點）
        buildNorthernStrataWall(root, coastData.mainland);
        buildMountainRanges(root, roads.roadCurve, routeData.landmarks);

        scene.add(root);
        return {
            terrainGroup: root,
            mainlandMesh: mainland.turfMesh,
            sakurajimaMesh: sakurajima.foamMesh,
            roadCurve: roads.roadCurve,
            tramCurve: roads.tramCurve,
            sampleGroundY,
            foamMeshes: [mainland.foamMesh, sakurajima.foamMesh]
        };
    }

    window.KyushuIsland.Terrain = {
        getTerrainElevation,
        buildSouthKyushuTerrain
    };
})();
