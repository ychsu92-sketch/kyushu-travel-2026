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

        // 繪製細緻草地陽光顆粒與微紋理 (避免深黑點造成畫面發灰)
        for (let i = 0; i < 1100; i++) {
            const x = Math.random() * 256;
            const y = Math.random() * 256;
            ctx.fillStyle = (i % 2 === 0) ? '#fffbeb' : '#558b3e';
            ctx.globalAlpha = grainOpacity * 0.28;
            ctx.fillRect(x, y, 2, 2);
        }

        const tex = new THREE.CanvasTexture(canvas);
        tex.wrapS = THREE.RepeatWrapping;
        tex.wrapT = THREE.RepeatWrapping;
        tex.repeat.set(0.35, 0.35);
        return tex;
    }

    // 輔助函式：判斷任意 (x, z) 是否在多邊形內部
    function isPointInPolygon(x, z, poly, scale, cx, cz) {
        let inside = false;
        const n = poly.length;
        for (let i = 0; i < n; i++) {
            const x1 = cx + (poly[i][0] - cx) * scale;
            const z1 = cz + (poly[i][1] - cz) * scale;
            const next = poly[(i + 1) % n];
            const x2 = cx + (next[0] - cx) * scale;
            const z2 = cz + (next[1] - cz) * scale;
            if ((z1 > z) !== (z2 > z)) {
                const xCross = (x2 - x1) * (z - z1) / (z2 - z1 + 1e-12) + x1;
                if (x < xCross) inside = !inside;
            }
        }
        return inside;
    }

    // 全島台地等高線階梯解析網格 (Terrace Elevation Grid - 徹底解決階梯高地穿模融合問題)
    let terraceGrid = null;
    const GRID_MIN_X = -10, GRID_MAX_X = 12, GRID_STEP_X = 0.4;
    const GRID_MIN_Z = -24, GRID_MAX_Z = 18, GRID_STEP_Z = 0.4;
    const gridCols = Math.ceil((GRID_MAX_X - GRID_MIN_X) / GRID_STEP_X);
    const gridRows = Math.ceil((GRID_MAX_Z - GRID_MIN_Z) / GRID_STEP_Z);

    function initTerraceGrid(pts) {
        if (!pts || !pts.length) return;
        terraceGrid = new Float32Array(gridCols * gridRows);
        for (let r = 0; r < gridRows; r++) {
            const z = GRID_MIN_Z + r * GRID_STEP_Z;
            for (let c = 0; c < gridCols; c++) {
                const x = GRID_MIN_X + c * GRID_STEP_X;
                let h = 0.88; // 第一階 Coastal Meadow 表面基準高度 (turfMesh1 頂面)
                if (isPointInPolygon(x, z, pts, 0.60, 2.16, -5.40)) {
                    h = 1.34; // 第三階 中央山麓高原層 (meshT3 頂面)
                } else if (isPointInPolygon(x, z, pts, 0.82, 0.96, -2.40)) {
                    h = 1.06; // 第二階 內陸丘陵台地 (meshT2 頂面)
                }
                terraceGrid[r * gridCols + c] = h;
            }
        }
    }

    function sampleTerraceBaseY(x, z) {
        if (!terraceGrid) return 0.88;
        const c = (x - GRID_MIN_X) / GRID_STEP_X;
        const r = (z - GRID_MIN_Z) / GRID_STEP_Z;
        if (c < 0 || c >= gridCols - 1 || r < 0 || r >= gridRows - 1) return 0.88;
        const c0 = Math.floor(c), r0 = Math.floor(r);
        const fx = c - c0, fz = r - r0;
        const v00 = terraceGrid[r0 * gridCols + c0];
        const v10 = terraceGrid[r0 * gridCols + (c0 + 1)];
        const v01 = terraceGrid[(r0 + 1) * gridCols + c0];
        const v11 = terraceGrid[(r0 + 1) * gridCols + (c0 + 1)];
        return (v00 * (1 - fx) + v10 * fx) * (1 - fz) + (v01 * (1 - fx) + v11 * fx) * fz;
    }

    // 計算任一 (x, z) 在南九州地表上的真實物理高度 (嚴格貼合 3 層等高線階梯台地與櫻島島嶼，杜絕物件虛假懸空)
    function getTerrainElevation(x, z) {
        // 櫻島活火山島表面 (turfMesh1 基準高度 0.88)
        if (x > -4.6 && x < -2.2 && z > 9.2 && z < 11.1) {
            return 0.88;
        }
        return sampleTerraceBaseY(x, z);
    }

    function createPolygonShape(pts, scaleFactor, centerOffset) {
        const shape = new THREE.Shape();
        if (!pts || !pts.length) return shape;
        const sf = scaleFactor || 1.0;
        const cx = centerOffset ? centerOffset[0] : 0.96;
        const cz = centerOffset ? centerOffset[1] : -2.40;

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

        // 4. 第一階：沿海平原草地層 (Coastal Lowland Meadow - 溫潤自然抹茶綠)
        const turfTex1 = createMicroTerrainTexture(options.turfHex1 || '#7f9968', '#688252', 0.30);
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
            color: 0xfafaf9,
            map: turfTex1,
            bumpMap: turfTex1,
            bumpScale: 0.04,
            roughness: 0.90,
            metalness: 0.01,
            flatShading: true
        });
        const turfMesh1 = new THREE.Mesh(turfGeo1, turfMat1);
        turfMesh1.position.y = 0.48;
        turfMesh1.castShadow = true;
        turfMesh1.receiveShadow = true;
        group.add(turfMesh1);

        // 5. 第二階與第三階：內陸等高線階梯台地 (Stepped Contour Terraces - 解決扁平單調感！)
        if (options.enableTerraces) {
            // 第二階：內陸丘陵台地 (縮放 0.82，溫潤冬日橄欖抹茶綠)
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
            const texT2 = createMicroTerrainTexture('#6e8759', '#587046', 0.32);
            const matT2 = new THREE.MeshStandardMaterial({
                color: 0xfafaf9,
                map: texT2,
                bumpMap: texT2,
                bumpScale: 0.05,
                roughness: 0.91,
                flatShading: true
            });
            const meshT2 = new THREE.Mesh(geoT2, matT2);
            meshT2.position.y = 0.72;
            meshT2.castShadow = true;
            meshT2.receiveShadow = true;
            group.add(meshT2);

            // 第三階：中央山麓高原層 (縮放 0.60，暖褐枯草高地色)
            const shapeT3 = createPolygonShape(pts, 0.60, [2.16, -5.40]);
            const geoT3 = new THREE.ExtrudeGeometry(shapeT3, {
                depth: 0.26,
                bevelEnabled: true,
                bevelSegments: 2,
                steps: 1,
                bevelSize: 0.10,
                bevelThickness: 0.12
            });
            geoT3.rotateX(-Math.PI / 2);
            const texT3 = createMicroTerrainTexture('#637a50', '#847459', 0.35);
            const matT3 = new THREE.MeshStandardMaterial({
                color: 0xfafaf9,
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

    // 建立地貌拼布細節：農田/茶園方塊、冬季枯黃芒草原、球磨川與大淀川蜿蜒溪流、海岸礁石 (1.2x 地圖座標)
    function buildBiomePatchesAndRivers(parent) {
        const biomeGroup = new THREE.Group();

        // 1. 田園拼布色塊 (熊本平原、人吉盆地、宮崎平原、知覽茶園)
        const patchDefs = [
            // 熊本與菊池平原農田 (自動貼合等高線台地高度 + 深度偏移 polygonOffset，杜絕 Z-fighting 破圖閃爍)
            { x: -1.08, z: -12.24, w: 1.7, d: 1.2, rot: 0.2,   color: 0x9cb376 },
            { x: 0.72,  z: -12.96, w: 1.5, d: 1.1, rot: -0.15, color: 0xb5a876 },
            { x: -2.64, z: -11.40, w: 1.4, d: 1.0, rot: 0.35,  color: 0x829e65 },
            // 阿蘇外輪山冬日枯草原 (精確避開阿蘇火山體與自駕公路)
            { x: 5.60,  z: -17.20, w: 1.6, d: 1.2, rot: -0.3,  color: 0xb89f72 },
            // 人吉球磨盆地與霧島山麓茶園
            { x: -0.72, z: -2.64,  w: 2.0, d: 1.5, rot: 0.25,  color: 0x8fa868 },
            { x: -2.16, z: 2.16,   w: 1.8, d: 1.3, rot: -0.2,  color: 0x9ab372 },
            // 薩摩半島知覽茶園與指宿菜の花田（冬季暖黃綠）
            { x: -5.52, z: 11.76,  w: 1.7, d: 1.4, rot: 0.18,  color: 0xa3bd6a },
            { x: -5.04, z: 13.68,  w: 1.5, d: 1.1, rot: -0.1,  color: 0xd4be6a },
            // 大隅半島與宮崎日南陽光草坡
            { x: 0.72,  z: 11.04,  w: 2.1, d: 1.6, rot: -0.25, color: 0x8ca668 },
            { x: 8.16,  z: 1.80,   w: 1.9, d: 2.3, rot: 0.12,  color: 0x96b070 },
            { x: 6.60,  z: -4.20,  w: 2.2, d: 1.7, rot: -0.2,  color: 0x7d965e }
        ];

        patchDefs.forEach(p => {
            const pg = new THREE.Group();
            const groundY = sampleTerraceBaseY(p.x, p.z);
            const py = (p.y !== undefined) ? Math.max(p.y, groundY + 0.02) : (groundY + 0.02);
            const baseMat = new THREE.MeshLambertMaterial({
                color: p.color,
                flatShading: true,
                polygonOffset: true,
                polygonOffsetFactor: -1.2,
                polygonOffsetUnits: -1.2
            });
            const base = new THREE.Mesh(
                new THREE.BoxGeometry(p.w, 0.06, p.d),
                baseMat
            );
            pg.add(base);
            // 田畦條紋細節
            const stripeMat = new THREE.MeshLambertMaterial({
                color: 0x657d4c,
                polygonOffset: true,
                polygonOffsetFactor: -1.8,
                polygonOffsetUnits: -1.8
            });
            for (let s = -2; s <= 2; s++) {
                const stripe = new THREE.Mesh(new THREE.BoxGeometry(p.w * 0.88, 0.075, 0.07), stripeMat);
                stripe.position.z = s * (p.d * 0.18);
                pg.add(stripe);
            }
            pg.position.set(p.x, py, p.z);
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
                new THREE.Vector3(2.64, 1.15, -4.20),
                new THREE.Vector3(0.48, 1.05, -2.88),
                new THREE.Vector3(-1.56, 0.90, -2.16),
                new THREE.Vector3(-3.12, 0.78, -3.84)
            ],
            // 五瀨川 (從阿蘇高千穗流向延岡日向灘)
            [
                new THREE.Vector3(5.04, 1.15, -13.80),
                new THREE.Vector3(7.56, 1.02, -11.88),
                new THREE.Vector3(9.84, 0.82, -10.20)
            ],
            // 大淀川 (從都城盆地流向宮崎海岸)
            [
                new THREE.Vector3(3.00, 1.02, 3.84),
                new THREE.Vector3(6.72, 0.90, 3.36),
                new THREE.Vector3(10.20, 0.78, 3.00)
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
            if (pt[1] < -15.0) {
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

    // 建立立體感十足的九州連綿山脈與 12 月冬季覆雪高地群（嚴格退縮避開自駕路線、景點與鐵道，杜絕穿模）
    function buildMountainRanges(parent, roadCurve, landmarks, jrCurve, jrEastCurve) {
        const hillGroup = new THREE.Group();
        const winterOliveMat = new THREE.MeshLambertMaterial({ color: 0x658352, flatShading: true });
        const highlandMat    = new THREE.MeshLambertMaterial({ color: 0x7c9668, flatShading: true });
        const rockSlopeMat   = new THREE.MeshLambertMaterial({ color: 0x78685a, flatShading: true });
        const snowMat        = new THREE.MeshLambertMaterial({ color: 0xf8fafc, flatShading: true });

        // 預先取樣自駕路線與專用鐵道路廊所有點，用來限制山腳半徑不壓到公路、鐵道或景點
        const routeSamples = [];
        if (roadCurve) {
            for (let i = 0; i < 200; i++) {
                routeSamples.push(roadCurve.getPointAt(i / 200));
            }
        }
        if (jrCurve) {
            for (let i = 0; i < 150; i++) {
                routeSamples.push(jrCurve.getPointAt(i / 150));
            }
        }
        if (jrEastCurve) {
            for (let i = 0; i < 150; i++) {
                routeSamples.push(jrEastCurve.getPointAt(i / 150));
            }
        }

        const ranges = [
            // 北部：九重連山與黑川後山（退至路線北側外圍，壓低高度避免遮擋視線，1.2x 地圖座標）
            { x: 6.96,  z: -19.44, r: 1.15, h: 0.85, snow: true,  rocky: true },
            { x: 0.96,  z: -18.72, r: 1.10, h: 0.75, snow: true,  rocky: false },
            // 九州脊樑山地（壓低高度作為中景起伏丘陵，絕不遮擋北側熊本與阿蘇車道上的人物）
            { x: 2.64,  z: -9.00,  r: 1.35, h: 0.72, snow: true,  rocky: true },
            { x: 5.04,  z: -6.60,  r: 1.35, h: 0.68, snow: true,  rocky: false },
            { x: 2.40,  z: -5.04,  r: 1.25, h: 0.65, snow: false, rocky: false },
            { x: 5.28,  z: -3.00,  r: 1.30, h: 0.65, snow: false, rocky: false },
            { x: 3.36,  z: -0.48,  r: 1.25, h: 0.62, snow: false, rocky: false },
            { x: 5.40,  z: 1.44,   r: 1.25, h: 0.60, snow: false, rocky: false },
            // 霧島連山（位於霧島神宮東側後山）
            { x: 2.88,  z: 3.84,   r: 1.15, h: 0.82, snow: true,  rocky: true },
            // 薩摩半島（開聞岳/薩摩富士）與大隅半島
            { x: -4.68, z: 15.12,  r: 0.95, h: 0.85, snow: true,  rocky: true },
            { x: 0.96,  z: 12.72,  r: 1.25, h: 0.65, snow: false, rocky: false }
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

            mGroup.position.set(m.x, sampleTerraceBaseY(m.x, m.z), m.z);
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
            const gy = sampleGroundY ? sampleGroundY(pt.x, pt.z) : 0.88;
            return new THREE.Vector3(pt.x, gy + 0.05, pt.z);
        });
        const roadCurve = new THREE.CatmullRomCurve3(curvePoints, true, 'catmullrom', 0.35);

        const roadMat = new THREE.MeshLambertMaterial({
            color: 0x64748b,
            polygonOffset: true,
            polygonOffsetFactor: -1.5,
            polygonOffsetUnits: -1.5
        });
        const curbMat = new THREE.MeshLambertMaterial({
            color: 0xe2e8f0,
            polygonOffset: true,
            polygonOffsetFactor: -1.2,
            polygonOffsetUnits: -1.2
        });
        const dashMat = new THREE.MeshBasicMaterial({
            color: 0xfacc15,
            polygonOffset: true,
            polygonOffsetFactor: -2.5,
            polygonOffsetUnits: -2.5
        });
        const ferryBuoyMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });

        const samples = 360;
        for (let i = 0; i < samples; i++) {
            const t = i / samples;
            const pos = roadCurve.getPointAt(t);
            const tangent = roadCurve.getTangentAt(t);
            const angle = Math.atan2(tangent.x, tangent.z);

            const isFerryWater = (pos.x > -4.56 && pos.x < -3.06 && pos.z > 9.78 && pos.z < 10.62);

            if (isFerryWater) {
                if (i % 3 === 0) {
                    const buoy = new THREE.Mesh(new THREE.SphereGeometry(0.08, 6, 6), ferryBuoyMat);
                    buoy.position.set(pos.x, 0.05, pos.z);
                    roadGroup.add(buoy);
                }
            } else {
                const gy = sampleGroundY ? sampleGroundY(pos.x, pos.z) : 0.88;
                const roadY = Math.max(pos.y, gy + 0.04);
                const curb = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.06, 0.42), curbMat);
                curb.position.set(pos.x, roadY - 0.015, pos.z);
                curb.rotation.y = angle;
                curb.receiveShadow = true;
                roadGroup.add(curb);

                const seg = new THREE.Mesh(new THREE.BoxGeometry(0.56, 0.07, 0.40), roadMat);
                seg.position.set(pos.x, roadY, pos.z);
                seg.rotation.y = angle;
                seg.receiveShadow = true;
                roadGroup.add(seg);

                if (i % 2 === 0) {
                    const dash = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 0.18), dashMat);
                    dash.position.set(pos.x, roadY + 0.01, pos.z);
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

        for (let i = 0; i <= 46; i++) {
            const t = i / 46;
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

        // 建立 JR 九州縱貫主幹線鐵道 (九州新幹線 / 鹿兒島本線專用立體高架路廊，嚴格避開家族公路與景點)
        const jrCurvePoints = [
            new THREE.Vector3(-5.85, (sampleGroundY ? sampleGroundY(-5.85, -17.50) : 0.88) + 0.08, -17.50), // 熊本荒尾・玉名
            new THREE.Vector3(-6.05, (sampleGroundY ? sampleGroundY(-6.05, -14.20) : 1.06) + 0.08, -14.20), // JR 熊本車站 (西側新幹線高架站)
            new THREE.Vector3(-5.80, (sampleGroundY ? sampleGroundY(-5.80, -11.50) : 1.06) + 0.08, -11.50), // 熊本南宇土西平原
            new THREE.Vector3(-5.45, (sampleGroundY ? sampleGroundY(-5.45,  -8.20) : 1.06) + 0.08,  -8.20), // 八代球磨川高架鐵橋
            new THREE.Vector3(-5.50, (sampleGroundY ? sampleGroundY(-5.50,  -4.00) : 1.06) + 0.08,  -4.00), // 水俁不知火海岸
            new THREE.Vector3(-6.10, (sampleGroundY ? sampleGroundY(-6.10,   0.80) : 1.06) + 0.08,   0.80), // 出水野鶴之里
            new THREE.Vector3(-6.60, (sampleGroundY ? sampleGroundY(-6.60,   4.80) : 1.06) + 0.08,   4.80), // 川內高架鐵橋
            new THREE.Vector3(-7.00, (sampleGroundY ? sampleGroundY(-7.00,   7.60) : 1.06) + 0.08,   7.60), // 薩摩伊集院
            new THREE.Vector3(-7.25, (sampleGroundY ? sampleGroundY(-7.25,   9.60) : 1.06) + 0.08,   9.60), // JR 鹿兒島中央站 (新幹線終點高架月台)
            // 雙軌返程線 (平行間距 ~0.35)
            new THREE.Vector3(-6.95, (sampleGroundY ? sampleGroundY(-6.95,   7.80) : 1.06) + 0.08,   7.80),
            new THREE.Vector3(-6.30, (sampleGroundY ? sampleGroundY(-6.30,   4.60) : 1.06) + 0.08,   4.60),
            new THREE.Vector3(-5.80, (sampleGroundY ? sampleGroundY(-5.80,   0.60) : 1.06) + 0.08,   0.60),
            new THREE.Vector3(-5.20, (sampleGroundY ? sampleGroundY(-5.20,  -4.20) : 1.06) + 0.08,  -4.20),
            new THREE.Vector3(-5.15, (sampleGroundY ? sampleGroundY(-5.15,  -8.40) : 1.06) + 0.08,  -8.40),
            new THREE.Vector3(-5.50, (sampleGroundY ? sampleGroundY(-5.50, -11.70) : 1.06) + 0.08, -11.70),
            new THREE.Vector3(-5.75, (sampleGroundY ? sampleGroundY(-5.75, -14.40) : 1.06) + 0.08, -14.40)
        ];
        const jrCurve = new THREE.CatmullRomCurve3(jrCurvePoints, true, 'catmullrom', 0.25);

        // 鋪設 JR 九州高架鐵道路基、道碴、雙軌鋼軌與門型電車線鋼架
        const ballastMat = new THREE.MeshLambertMaterial({ color: 0x334155 }); // 深灰玄武岩道碴
        const jrSleeperMat = new THREE.MeshLambertMaterial({ color: 0xe2e8f0 }); // 淺灰預力混凝土枕木 (PC 枕木)
        const jrRailMat = new THREE.MeshLambertMaterial({ color: 0x94a3b8 });    // 銀灰高碳鋼鋼軌
        const mastMat = new THREE.MeshLambertMaterial({ color: 0x475569 });      // 門型架空線支柱
        const pierMat = new THREE.MeshLambertMaterial({ color: 0x94a3b8 });      // 高架橋墩混凝土材質

        const jrSamples = 240;
        for (let i = 0; i < jrSamples; i++) {
            const t = i / jrSamples;
            const p = jrCurve.getPointAt(t);
            const tan = jrCurve.getTangentAt(t);
            const ang = Math.atan2(tan.x, tan.z);
            const gy = sampleGroundY ? sampleGroundY(p.x, p.z) : 0.88;
            const railY = Math.max(p.y, gy + 0.04);

            // 每隔 10 節在路基下方立一座扎實的混凝土高架橋墩 (Viaduct Piers)，徹底排除軌道懸空與穿模
            if (i % 10 === 0) {
                const pierH = Math.max(0.12, railY - (gy || 0.80));
                const pier = new THREE.Mesh(new THREE.BoxGeometry(0.26, pierH, 0.22), pierMat);
                pier.position.set(p.x, railY - pierH * 0.5, p.z);
                pier.rotation.y = ang;
                roadGroup.add(pier);
            }

            // 道碴道床
            const ballast = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.04, 0.16), ballastMat);
            ballast.position.set(p.x, railY, p.z);
            ballast.rotation.y = ang;
            roadGroup.add(ballast);

            // PC 混凝土枕木
            const sleeper = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.025, 0.06), jrSleeperMat);
            sleeper.position.set(p.x, railY + 0.02, p.z);
            sleeper.rotation.y = ang;
            roadGroup.add(sleeper);

            // 雙軌鋼軌
            [-0.09, 0.09].forEach(offX => {
                const rail = new THREE.Mesh(new THREE.BoxGeometry(0.026, 0.035, 0.16), jrRailMat);
                const rx = p.x + Math.cos(ang) * offX;
                const rz = p.z - Math.sin(ang) * offX;
                rail.position.set(rx, railY + 0.035, rz);
                rail.rotation.y = ang;
                roadGroup.add(rail);
            });

            // 每隔 14 節豎立一座 JR 日本經典門型高架電車線架 (Catenary Mast，加寬立柱避免車體傾斜時擦撞)
            if (i % 14 === 0) {
                const gantry = new THREE.Group();
                const mastH = 0.42;
                [-0.24, 0.24].forEach(mx => {
                    const post = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, mastH, 6), mastMat);
                    post.position.set(mx, mastH * 0.5, 0);
                    gantry.add(post);
                });
                const beam = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.022, 0.022), mastMat);
                beam.position.set(0, mastH, 0);
                const insul = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.05, 6), jrSleeperMat);
                insul.position.set(0, mastH - 0.025, 0);
                gantry.add(beam, insul);
                gantry.position.set(p.x, railY + 0.02, p.z);
                gantry.rotation.y = ang;
                roadGroup.add(gantry);
            }
        }

        // 建立 JR 九州東海岸路廊（日豐本線・日南海岸專用立體海濱高架路廊，嚴格避開公路動線）
        const jrEastCurvePoints = [
            // 延岡海灣立體鐵道
            new THREE.Vector3(12.20, (sampleGroundY ? sampleGroundY(12.20, -12.50) : 1.06) + 0.08, -12.50), // 延岡
            new THREE.Vector3(11.80, (sampleGroundY ? sampleGroundY(11.80,  -8.50) : 1.06) + 0.08,  -8.50), // 日向灘美美津
            new THREE.Vector3(11.60, (sampleGroundY ? sampleGroundY(11.60,  -4.50) : 1.06) + 0.08,  -4.50), // 都農・高鍋海岸
            new THREE.Vector3(11.50, (sampleGroundY ? sampleGroundY(11.50,  -0.50) : 0.88) + 0.08,  -0.50), // JR 宮崎站
            new THREE.Vector3(11.40, (sampleGroundY ? sampleGroundY(11.40,   3.50) : 0.88) + 0.08,   3.50), // 青島外海景觀線
            new THREE.Vector3(11.00, (sampleGroundY ? sampleGroundY(11.00,   7.00) : 0.88) + 0.08,   7.00), // JR 日南海岸站
            new THREE.Vector3(10.40, (sampleGroundY ? sampleGroundY(10.40,  10.00) : 0.88) + 0.08,  10.00), // 油津港海崖
            // 東側返程線 (平行複線間距 ~0.35)
            new THREE.Vector3(10.75, (sampleGroundY ? sampleGroundY(10.75,   9.80) : 0.88) + 0.08,   9.80),
            new THREE.Vector3(11.35, (sampleGroundY ? sampleGroundY(11.35,   6.80) : 0.88) + 0.08,   6.80),
            new THREE.Vector3(11.75, (sampleGroundY ? sampleGroundY(11.75,   3.30) : 0.88) + 0.08,   3.30),
            new THREE.Vector3(11.85, (sampleGroundY ? sampleGroundY(11.85,  -0.70) : 0.88) + 0.08,  -0.70),
            new THREE.Vector3(11.95, (sampleGroundY ? sampleGroundY(11.95,  -4.70) : 0.88) + 0.08,  -4.70),
            new THREE.Vector3(12.15, (sampleGroundY ? sampleGroundY(12.15,  -8.70) : 1.06) + 0.08,  -8.70),
            new THREE.Vector3(12.55, (sampleGroundY ? sampleGroundY(12.55, -12.70) : 1.06) + 0.08, -12.70)
        ];
        const jrEastCurve = new THREE.CatmullRomCurve3(jrEastCurvePoints, true, 'catmullrom', 0.25);

        const jrEastSamples = 220;
        for (let i = 0; i < jrEastSamples; i++) {
            const t = i / jrEastSamples;
            const p = jrEastCurve.getPointAt(t);
            const tan = jrEastCurve.getTangentAt(t);
            const ang = Math.atan2(tan.x, tan.z);
            const gy = sampleGroundY ? sampleGroundY(p.x, p.z) : 0.88;
            const railY = Math.max(p.y, gy + 0.04);

            // 每隔 10 節建立一座穩固的混凝土海景高架橋墩
            if (i % 10 === 0) {
                const pierH = Math.max(0.12, railY - (gy || 0.80));
                const pier = new THREE.Mesh(new THREE.BoxGeometry(0.26, pierH, 0.22), pierMat);
                pier.position.set(p.x, railY - pierH * 0.5, p.z);
                pier.rotation.y = ang;
                roadGroup.add(pier);
            }

            // 道碴
            const ballast = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.04, 0.16), ballastMat);
            ballast.position.set(p.x, railY, p.z);
            ballast.rotation.y = ang;
            roadGroup.add(ballast);

            // PC 枕木
            const sleeper = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.025, 0.06), jrSleeperMat);
            sleeper.position.set(p.x, railY + 0.02, p.z);
            sleeper.rotation.y = ang;
            roadGroup.add(sleeper);

            // 雙軌
            [-0.09, 0.09].forEach(offX => {
                const rail = new THREE.Mesh(new THREE.BoxGeometry(0.026, 0.035, 0.16), jrRailMat);
                const rx = p.x + Math.cos(ang) * offX;
                const rz = p.z - Math.sin(ang) * offX;
                rail.position.set(rx, railY + 0.035, rz);
                rail.rotation.y = ang;
                roadGroup.add(rail);
            });

            // 門型電車線鋼架
            if (i % 14 === 0) {
                const gantry = new THREE.Group();
                const mastH = 0.42;
                [-0.24, 0.24].forEach(mx => {
                    const post = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, mastH, 6), mastMat);
                    post.position.set(mx, mastH * 0.5, 0);
                    gantry.add(post);
                });
                const beam = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.022, 0.022), mastMat);
                beam.position.set(0, mastH, 0);
                const insul = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.05, 6), jrSleeperMat);
                insul.position.set(0, mastH - 0.025, 0);
                gantry.add(beam, insul);
                gantry.position.set(p.x, railY + 0.02, p.z);
                gantry.rotation.y = ang;
                roadGroup.add(gantry);
            }
        }

        parent.add(roadGroup);
        return { roadCurve, tramCurve, jrCurve, jrEastCurve, roadGroup };
    }

    function buildSouthKyushuTerrain(scene, coastData, routeData) {
        const root = new THREE.Group();

        // 0. 初始化階梯高地地形解析網格（確保道路、景點、車輛與角色能精確貼合所有台地表面）
        if (coastData && coastData.mainland) {
            initTerraceGrid(coastData.mainland);
        }

        // 1. 南九州主島（含 3 層立體等高線階梯台地 + 程序化微縮模型凹凸貼圖，1.2x 地圖尺寸）
        const mainland = buildLayeredLandmass(coastData.mainland, {
            turfHex1: '#7f9968',
            cliffHex: '#865639',
            cliffDepth: 1.95,
            enableTerraces: true,
            center: [0.96, -2.40]
        });
        root.add(mainland.group);

        // 2. 錦江灣中央的櫻島活火山島
        const sakurajima = buildLayeredLandmass(coastData.sakurajima, {
            turfHex1: '#647b50',
            cliffHex: '#593e32',
            cliffDepth: 1.65,
            enableTerraces: false,
            center: [-3.24, 10.20]
        });
        root.add(sakurajima.group);

        // 3. 西側天草群島
        if (coastData.amakusa) {
            coastData.amakusa.forEach(poly => {
                const ama = buildLayeredLandmass(poly, {
                    turfHex1: '#829b6b',
                    cliffHex: '#8c5c3e',
                    cliffDepth: 1.45,
                    enableTerraces: false
                });
                root.add(ama.group);
            });
        }

        // 4. 田園/茶園/枯草原拼布與球磨川等三大水系
        buildBiomePatchesAndRivers(root);

        // 建立高效地面高度取樣器（採用解析數學公式 getTerrainElevation，0 毫秒極速計算，徹底杜絕每幀 Raycaster 遍歷導致的畫面卡頓）
        function sampleGroundY(x, z) {
            // 錦江灣渡輪水道 (1.2x 地圖座標)
            if (x > -4.56 && x < -3.06 && z > 9.78 && z < 10.62) {
                return 0.12;
            }
            return getTerrainElevation(x, z);
        }

        // 5. 環島自駕公路與路面電車軌道（先鋪設道路，再根據道路安全距離放山脈）
        const roads = buildRoadsAndTracks(root, routeData, sampleGroundY);

        // 6. 北側浮空島斷面岩層與全島立體山脈群（自動避開道路、景點與鐵道路廊）
        buildNorthernStrataWall(root, coastData.mainland);
        buildMountainRanges(root, roads.roadCurve, routeData.landmarks, roads.jrCurve, roads.jrEastCurve);

        scene.add(root);
        return {
            terrainGroup: root,
            mainlandMesh: mainland.turfMesh,
            sakurajimaMesh: sakurajima.foamMesh,
            roadCurve: roads.roadCurve,
            tramCurve: roads.tramCurve,
            jrCurve: roads.jrCurve,
            jrEastCurve: roads.jrEastCurve,
            sampleGroundY,
            foamMeshes: [mainland.foamMesh, sakurajima.foamMesh]
        };
    }

    window.KyushuIsland.Terrain = {
        getTerrainElevation,
        buildSouthKyushuTerrain,
        isPointInPolygon
    };
})();
