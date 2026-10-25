/**
 * portal/env.js
 * 自然背景環境：12 月冬季晴空漸層圓頂、冬日暖陽與長陰影、
 * 錦江灣與外海 Low-poly 動態波浪海面、岸邊浪花、緩飄雲朵與可開關雪花粒子。
 */
(function () {
    window.KyushuIsland = window.KyushuIsland || {};

    function createSkyDome(scene) {
        const vertexShader = `
            varying vec3 vWorldPosition;
            void main() {
                vec4 worldPosition = modelMatrix * vec4(position, 1.0);
                vWorldPosition = worldPosition.xyz;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `;
        const fragmentShader = `
            varying vec3 vWorldPosition;
            void main() {
                float h = normalize(vWorldPosition + vec3(0.0, 18.0, 0.0)).y;
                vec3 zenithColor = vec3(0.55, 0.76, 0.94);   // 冬日清澈淡天藍
                vec3 midColor    = vec3(0.84, 0.91, 0.97);   // 柔和淺霧藍
                vec3 horizonColor= vec3(0.99, 0.91, 0.80);   // 12月低角度冬陽暖杏色
                vec3 col = mix(horizonColor, midColor, smoothstep(0.0, 0.28, max(h, 0.0)));
                col = mix(col, zenithColor, smoothstep(0.28, 0.78, max(h, 0.0)));
                gl_FragColor = vec4(col, 1.0);
            }
        `;
        const skyGeo = new THREE.SphereGeometry(115, 28, 20);
        const skyMat = new THREE.ShaderMaterial({
            vertexShader: vertexShader,
            fragmentShader: fragmentShader,
            side: THREE.BackSide,
            depthWrite: false
        });
        const skyMesh = new THREE.Mesh(skyGeo, skyMat);
        scene.add(skyMesh);
        return skyMesh;
    }

    function setupWinterLights(scene) {
        // 1. 柔和冬季環境光
        const ambient = new THREE.AmbientLight(0xfff5eb, 0.62);
        scene.add(ambient);

        // 2. 天空與大地半球反射光 (Heart-Island 溫潤立體感關鍵)
        const hemiLight = new THREE.HemisphereLight(0xdbeafe, 0xd6c7b2, 0.48);
        hemiLight.position.set(0, 35, 0);
        scene.add(hemiLight);

        // 3. 12 月冬季低角度暖陽 (產生柔和長陰影)
        const sunLight = new THREE.DirectionalLight(0xffe0b2, 1.15);
        sunLight.position.set(26, 22, 18);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 2048;
        sunLight.shadow.mapSize.height = 2048;
        sunLight.shadow.camera.near = 4;
        sunLight.shadow.camera.far = 85;
        const d = 24;
        sunLight.shadow.camera.left = -d;
        sunLight.shadow.camera.right = d;
        sunLight.shadow.camera.top = d;
        sunLight.shadow.camera.bottom = -d;
        sunLight.shadow.bias = -0.0006;
        scene.add(sunLight);

        // 4. 背光側暖色補光，避免暗部死黑
        const fillLight = new THREE.DirectionalLight(0xc7d2fe, 0.32);
        fillLight.position.set(-22, 14, -18);
        scene.add(fillLight);

        // 5. 可見的冬日太陽球體與光暈
        const sunGroup = new THREE.Group();
        sunGroup.position.set(42, 34, -36);
        const sunCore = new THREE.Mesh(
            new THREE.SphereGeometry(3.2, 16, 16),
            new THREE.MeshBasicMaterial({ color: 0xffedd5 })
        );
        const sunHalo = new THREE.Mesh(
            new THREE.SphereGeometry(5.2, 16, 16),
            new THREE.MeshBasicMaterial({ color: 0xfde68a, transparent: true, opacity: 0.28 })
        );
        sunGroup.add(sunCore);
        sunGroup.add(sunHalo);
        scene.add(sunGroup);

        return { ambient, hemiLight, sunLight, fillLight, sunGroup };
    }

    function createOcean(scene) {
        const oceanGroup = new THREE.Group();

        // 1. 深海底層
        const deepGeo = new THREE.CircleGeometry(98, 48);
        deepGeo.rotateX(-Math.PI / 2);
        const deepMat = new THREE.MeshLambertMaterial({ color: 0x16425b });
        const deepMesh = new THREE.Mesh(deepGeo, deepMat);
        deepMesh.position.y = -1.65;
        oceanGroup.add(deepMesh);

        // 2. 表層 Low-poly 動態折面波浪海面 (拉高細分與波峰立體起伏、隨浪高動態變色)
        const seaGeo = new THREE.PlaneGeometry(130, 130, 76, 76);
        seaGeo.rotateX(-Math.PI / 2);
        const posAttr = seaGeo.attributes.position;
        const baseX = new Float32Array(posAttr.count);
        const baseZ = new Float32Array(posAttr.count);
        const colors = new Float32Array(posAttr.count * 3);
        const randJitter = new Float32Array(posAttr.count);

        for (let i = 0; i < posAttr.count; i++) {
            // 加入微幅水平擾動讓 Low-poly 三角網格更有不規則海浪切面感
            const x = posAttr.getX(i) + (Math.random() - 0.5) * 0.45;
            const z = posAttr.getZ(i) + (Math.random() - 0.5) * 0.45;
            posAttr.setX(i, x);
            posAttr.setZ(i, z);
            baseX[i] = x;
            baseZ[i] = z;
            randJitter[i] = Math.random() * Math.PI * 2;
            colors[i * 3] = 0.22;
            colors[i * 3 + 1] = 0.54;
            colors[i * 3 + 2] = 0.68;
        }
        seaGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        seaGeo.userData = { baseX, baseZ, randJitter };

        const seaMat = new THREE.MeshPhongMaterial({
            vertexColors: true,
            emissive: 0x0b2942,
            emissiveIntensity: 0.22,
            specular: 0xe0f2fe,
            shininess: 48,
            flatShading: true,
            transparent: true,
            opacity: 0.92
        });
        const seaMesh = new THREE.Mesh(seaGeo, seaMat);
        seaMesh.position.y = -0.32;
        seaMesh.receiveShadow = true;
        oceanGroup.add(seaMesh);

        // 3. 海面動態白色湧浪白沫條 (Whitecaps / Wave Crests) 與陽光粼粼閃光點
        const crestsGroup = new THREE.Group();
        const crestMat = new THREE.MeshBasicMaterial({
            color: 0xf0f9ff,
            transparent: true,
            opacity: 0.72
        });
        const waveCrests = [];
        for (let i = 0; i < 46; i++) {
            const angle = (i / 46) * Math.PI * 2 + (Math.random() - 0.5) * 0.2;
            const dist = 11.5 + Math.random() * 16.0;
            const cx = Math.cos(angle) * dist * 0.88;
            const cz = Math.sin(angle) * dist * 1.15;
            const w = 0.85 + Math.random() * 1.25;
            const crestGeo = new THREE.BoxGeometry(w, 0.05, 0.16);
            const crest = new THREE.Mesh(crestGeo, crestMat.clone());
            crest.position.set(cx, -0.18, cz);
            crest.rotation.y = -angle + Math.PI / 2 + (Math.random() - 0.5) * 0.35;
            crest.userData = {
                baseX: cx,
                baseZ: cz,
                dirX: -Math.cos(angle),
                dirZ: -Math.sin(angle),
                speed: 0.55 + Math.random() * 0.45,
                phase: Math.random() * Math.PI * 2,
                baseScaleX: 0.7 + Math.random() * 0.6
            };
            crestsGroup.add(crest);
            waveCrests.push(crest);
        }

        // 錦江灣與日南海岸近岸湧浪線
        const coastalWaveSpots = [
            { x: -3.2, z: 7.4, rot: 0.2 },   { x: -3.0, z: 9.2, rot: -0.3 },  // 錦江灣
            { x: 9.2,  z: 2.2, rot: 1.4 },   { x: 8.8,  z: 4.8, rot: 1.35 },  // 宮崎青島外海
            { x: 8.2,  z: 7.4, rot: 1.25 },  { x: 6.2,  z: 10.2, rot: 1.0 },  // 日南鵜戶海岸
            { x: -6.2, z: -9.8, rot: -1.2 }, { x: -5.8, z: -7.2, rot: -1.3 }, // 天草灘
            { x: -5.5, z: 11.8, rot: -0.8 }, { x: -1.8, z: 12.8, rot: 0.4 }   // 指宿與佐多岬外海
        ];
        coastalWaveSpots.forEach((cw, idx) => {
            const crest = new THREE.Mesh(new THREE.BoxGeometry(1.45, 0.06, 0.20), crestMat.clone());
            crest.position.set(cw.x, -0.16, cw.z);
            crest.rotation.y = cw.rot;
            crest.userData = {
                baseX: cw.x,
                baseZ: cw.z,
                dirX: Math.sin(cw.rot),
                dirZ: Math.cos(cw.rot),
                speed: 0.85,
                phase: idx * 0.9,
                baseScaleX: 1.0
            };
            crestsGroup.add(crest);
            waveCrests.push(crest);
        });

        oceanGroup.add(crestsGroup);
        scene.add(oceanGroup);
        return { oceanGroup, seaMesh, waveCrests };
    }

    function createClouds(scene) {
        const cloudsGroup = new THREE.Group();
        const cloudMat = new THREE.MeshLambertMaterial({
            color: 0xfffdf9,
            flatShading: true,
            transparent: true,
            opacity: 0.92
        });

        const cloudConfigs = [
            { x: -16, y: 11.5, z: -14, scale: 1.2, speed: 0.35 },
            { x: 14,  y: 12.8, z: -18, scale: 1.45, speed: 0.28 },
            { x: -18, y: 10.5, z: 6,   scale: 1.0, speed: 0.42 },
            { x: 18,  y: 11.2, z: 8,   scale: 1.3, speed: 0.31 },
            { x: 2,   y: 13.5, z: -24, scale: 1.5, speed: 0.25 },
            { x: -8,  y: 12.0, z: 18,  scale: 1.15, speed: 0.38 }
        ];

        const clouds = [];
        cloudConfigs.forEach(cfg => {
            const c = new THREE.Group();
            const p1 = new THREE.Mesh(new THREE.DodecahedronGeometry(1.2, 1), cloudMat);
            const p2 = new THREE.Mesh(new THREE.DodecahedronGeometry(0.95, 1), cloudMat);
            p2.position.set(1.05, -0.15, 0.2);
            const p3 = new THREE.Mesh(new THREE.DodecahedronGeometry(0.85, 1), cloudMat);
            p3.position.set(-1.0, -0.2, -0.15);
            const p4 = new THREE.Mesh(new THREE.DodecahedronGeometry(0.7, 1), cloudMat);
            p4.position.set(0.3, 0.45, -0.3);
            [p1, p2, p3, p4].forEach(m => {
                m.scale.y = 0.62;
                c.add(m);
            });
            c.position.set(cfg.x, cfg.y, cfg.z);
            c.scale.setScalar(cfg.scale);
            c.userData = { baseX: cfg.x, speed: cfg.speed, phase: Math.random() * Math.PI * 2 };
            cloudsGroup.add(c);
            clouds.push(c);
        });

        scene.add(cloudsGroup);
        return clouds;
    }

    function createSnowSystem(scene, isMobile) {
        const count = isMobile ? 160 : 320;
        const geo = new THREE.BufferGeometry();
        const positions = new Float32Array(count * 3);
        const velocities = new Float32Array(count * 3);

        for (let i = 0; i < count; i++) {
            positions[i * 3]     = (Math.random() - 0.5) * 38;
            positions[i * 3 + 1] = Math.random() * 18 + 0.5;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 44;

            velocities[i * 3]     = (Math.random() - 0.5) * 0.4;
            velocities[i * 3 + 1] = -(0.6 + Math.random() * 0.7);
            velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.4;
        }

        geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geo.userData.velocities = velocities;

        const mat = new THREE.PointsMaterial({
            color: 0xffffff,
            size: 0.22,
            transparent: true,
            opacity: 0.82
        });

        const points = new THREE.Points(geo, mat);
        points.visible = true;
        scene.add(points);
        return points;
    }

    function updateEnvironment(envState, elapsed, delta) {
        // 1. 海面多頻率 Gerstner 風格立體波浪 + 波峰白浪花與波谷深海漸層色動態變化
        if (envState.seaMesh) {
            const geo = envState.seaMesh.geometry;
            const pos = geo.attributes.position;
            const col = geo.attributes.color;
            const { baseX, baseZ, randJitter } = geo.userData;

            for (let i = 0; i < pos.count; i++) {
                const bx = baseX[i];
                const bz = baseZ[i];
                const jit = randJitter[i];

                // 三組不同方向與波長的湧浪疊加 + 向島嶼中心傳遞的環狀波紋
                const distFromCenter = Math.hypot(bx * 0.85, bz * 0.72);
                const w1 = Math.sin(bx * 0.42 + bz * 0.18 + elapsed * 1.85) * 0.15;
                const w2 = Math.cos(bz * 0.48 - bx * 0.22 + elapsed * 1.45) * 0.13;
                const w3 = Math.sin(distFromCenter * 0.65 - elapsed * 2.15 + jit * 0.3) * 0.09;
                const chop = Math.sin(elapsed * 3.2 + jit) * 0.04;

                const waveH = w1 + w2 + w3 + chop;

                // 水平微幅往復擺動 (模擬真實海浪湧動感)
                pos.setX(i, bx + Math.cos(bx * 0.35 + elapsed * 1.6) * 0.10);
                pos.setY(i, waveH);
                pos.setZ(i, bz + Math.sin(bz * 0.35 + elapsed * 1.4) * 0.10);

                // 依據波浪高低與離岸距離動態混色：波谷深海藍 -> 中層清澈海藍 -> 波峰亮白青浪花
                const normH = Math.max(0, Math.min(1, (waveH + 0.32) / 0.68));
                const foamBoost = normH > 0.74 ? (normH - 0.74) * 2.2 : 0.0;
                const shallowBoost = Math.max(0, 1.0 - distFromCenter / 18.0) * 0.12;

                const r = Math.min(0.96, 0.16 + normH * 0.24 + shallowBoost * 0.25 + foamBoost * 0.52);
                const g = Math.min(0.98, 0.44 + normH * 0.28 + shallowBoost * 0.38 + foamBoost * 0.32);
                const b = Math.min(1.00, 0.62 + normH * 0.24 + shallowBoost * 0.22 + foamBoost * 0.20);
                col.setXYZ(i, r, g, b);
            }
            pos.needsUpdate = true;
            col.needsUpdate = true;
            geo.computeVertexNormals();
        }

        // 2. 海面動態白色湧浪條 (Wave Crests) 推進與呼吸起伏
        if (envState.waveCrests) {
            envState.waveCrests.forEach(crest => {
                const u = crest.userData;
                const cycle = (elapsed * u.speed + u.phase) % (Math.PI * 2);
                const slide = Math.sin(cycle) * 0.65;
                const pulse = (Math.cos(cycle) + 1) * 0.5; // 0 ~ 1

                crest.position.x = u.baseX + u.dirX * slide;
                crest.position.z = u.baseZ + u.dirZ * slide;
                crest.position.y = -0.22 + Math.sin(elapsed * 2.2 + u.phase) * 0.09;
                crest.scale.x = u.baseScaleX * (0.65 + pulse * 0.75);
                crest.scale.z = 0.7 + pulse * 0.8;
                crest.material.opacity = 0.18 + pulse * 0.68;
            });
        }

        // 3. 環繞主島與櫻島岸邊的白色海浪泡沫圈呼吸拍岸效果
        if (envState.foamMeshes) {
            envState.foamMeshes.forEach((fm, idx) => {
                if (!fm) return;
                const tide = Math.sin(elapsed * 2.1 + idx * 1.4);
                fm.position.y = -0.20 + tide * 0.04;
                const s = 1.018 + tide * 0.008;
                fm.scale.set(s, 1.0, s);
                if (fm.material) {
                    fm.material.opacity = 0.62 + tide * 0.22;
                }
            });
        }

        // 雲朵緩飄
        if (envState.clouds) {
            envState.clouds.forEach(c => {
                c.position.x = c.userData.baseX + Math.sin(elapsed * 0.15 * c.userData.speed + c.userData.phase) * 3.5;
                c.position.y += Math.sin(elapsed * 0.8 + c.userData.phase) * 0.0015;
            });
        }

        // 飄雪更新
        if (envState.snow && envState.snow.visible) {
            const pos = envState.snow.geometry.attributes.position;
            const vel = envState.snow.geometry.userData.velocities;
            for (let i = 0; i < pos.count; i++) {
                let x = pos.getX(i) + vel[i * 3] * delta + Math.sin(elapsed + i) * 0.008;
                let y = pos.getY(i) + vel[i * 3 + 1] * delta;
                let z = pos.getZ(i) + vel[i * 3 + 2] * delta;
                if (y < 0.0) {
                    y = 17.5;
                    x = (Math.random() - 0.5) * 36;
                    z = (Math.random() - 0.5) * 42;
                }
                pos.setXYZ(i, x, y, z);
            }
            pos.needsUpdate = true;
        }
    }

    window.KyushuIsland.Env = {
        createSkyDome,
        setupWinterLights,
        createOcean,
        createClouds,
        createSnowSystem,
        updateEnvironment
    };
})();
