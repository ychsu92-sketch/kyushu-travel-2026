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
                vec3 zenithColor = vec3(0.53, 0.72, 0.88);   // 清透溫潤冬日晴空藍
                vec3 midColor    = vec3(0.80, 0.88, 0.94);   // 柔和淺天藍
                vec3 horizonColor= vec3(0.95, 0.88, 0.79);   // 冬日暖陽杏米色地平線
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
        // 1. 柔和冬季環境光 (自然溫潤、不灰暗也不過曝)
        const ambient = new THREE.AmbientLight(0xfff5eb, 0.54);
        scene.add(ambient);

        // 2. 天空與大地半球反射光
        const hemiLight = new THREE.HemisphereLight(0xd6e6f5, 0xc9b9a3, 0.42);
        hemiLight.position.set(0, 35, 0);
        scene.add(hemiLight);

        // 3. 12 月冬季低角度暖陽 (產生柔和長陰影，色澤溫暖清透)
        const sunLight = new THREE.DirectionalLight(0xffdeb8, 0.98);
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
        const fillLight = new THREE.DirectionalLight(0xb8c4d9, 0.24);
        fillLight.position.set(-22, 14, -18);
        scene.add(fillLight);

        // 5. 可見的冬日太陽球體與光暈
        const sunGroup = new THREE.Group();
        sunGroup.position.set(42, 34, -36);
        const sunCore = new THREE.Mesh(
            new THREE.SphereGeometry(3.2, 16, 16),
            new THREE.MeshBasicMaterial({ color: 0xf7e6cc })
        );
        const sunHalo = new THREE.Mesh(
            new THREE.SphereGeometry(5.2, 16, 16),
            new THREE.MeshBasicMaterial({ color: 0xeed6a4, transparent: true, opacity: 0.22 })
        );
        sunGroup.add(sunCore);
        sunGroup.add(sunHalo);
        scene.add(sunGroup);

        return { ambient, hemiLight, sunLight, fillLight, sunGroup };
    }

    function createOcean(scene) {
        const oceanGroup = new THREE.Group();

        // 1. 深海襯底層
        const deepGeo = new THREE.CircleGeometry(98, 48);
        deepGeo.rotateX(-Math.PI / 2);
        const deepMat = new THREE.MeshLambertMaterial({ color: 0x264b5e });
        const deepMesh = new THREE.Mesh(deepGeo, deepMat);
        deepMesh.position.y = -1.65;
        oceanGroup.add(deepMesh);

        // 2. 平靜溫潤的冬日海面 (清透海藍搭配白色線條波紋，符合插畫微縮模型風格)
        const seaGeo = new THREE.PlaneGeometry(130, 130, 32, 32);
        seaGeo.rotateX(-Math.PI / 2);
        const seaMat = new THREE.MeshLambertMaterial({
            color: 0x3d7ea0,
            transparent: true,
            opacity: 0.94
        });
        const seaMesh = new THREE.Mesh(seaGeo, seaMat);
        seaMesh.position.y = -0.32;
        seaMesh.receiveShadow = true;
        oceanGroup.add(seaMesh);

        // 3. 插畫風白色線條波紋 (Minimalist White Line Ripples)
        const linesGroup = new THREE.Group();
        const waveLines = [];

        // 生成手繪感波紋線段 (~~~~~~ 與長短雙線組合)
        function createWaveLineUnit(width, style) {
            const g = new THREE.Group();
            const mat = new THREE.MeshBasicMaterial({
                color: 0xf1f5f9,
                transparent: true,
                opacity: 0.72
            });

            if (style === 'wavy') {
                // 連續波浪曲線細線條
                const pts = [];
                const segs = 16;
                for (let s = 0; s <= segs; s++) {
                    const u = (s / segs) - 0.5;
                    const x = u * width;
                    const z = Math.sin((s / segs) * Math.PI * 3.0) * 0.11;
                    pts.push(new THREE.Vector3(x, 0, z));
                }
                const curve = new THREE.CatmullRomCurve3(pts);
                const tubeGeo = new THREE.TubeGeometry(curve, 20, 0.032, 5, false);
                tubeGeo.scale(1.0, 0.25, 1.0);
                const mesh = new THREE.Mesh(tubeGeo, mat);
                g.add(mesh);

                // 伴隨一條短平行白線增加插畫層次
                const subBar = new THREE.Mesh(new THREE.BoxGeometry(width * 0.42, 0.015, 0.045), mat);
                subBar.position.set(width * 0.15, 0, 0.22);
                g.add(subBar);
            } else {
                // 簡約雙重平行白細線波紋
                const mainLine = new THREE.Mesh(new THREE.BoxGeometry(width, 0.015, 0.05), mat);
                const subLine = new THREE.Mesh(new THREE.BoxGeometry(width * 0.55, 0.015, 0.045), mat);
                subLine.position.set(-width * 0.18, 0, 0.18);
                g.add(mainLine, subLine);
            }
            g.userData.mat = mat;
            return g;
        }

        // 外海環狀分布的白線波紋 (64 組)
        for (let i = 0; i < 64; i++) {
            const angle = (i / 64) * Math.PI * 2 + (Math.random() - 0.5) * 0.18;
            const dist = 10.5 + (i % 5) * 3.6 + Math.random() * 1.8;
            const cx = Math.cos(angle) * dist * 0.88;
            const cz = Math.sin(angle) * dist * 1.15;
            const width = 1.15 + (i % 3) * 0.45;
            const lineUnit = createWaveLineUnit(width, i % 2 === 0 ? 'wavy' : 'double');

            lineUnit.position.set(cx, -0.28, cz);
            lineUnit.rotation.y = -angle + Math.PI / 2 + (Math.random() - 0.5) * 0.25;
            lineUnit.userData = {
                mat: lineUnit.userData.mat,
                baseX: cx,
                baseZ: cz,
                dirX: -Math.cos(angle),
                dirZ: -Math.sin(angle),
                speed: 0.65 + (i % 4) * 0.15,
                phase: i * 0.65,
                amp: 0.35 + (i % 3) * 0.12
            };
            linesGroup.add(lineUnit);
            waveLines.push(lineUnit);
        }

        // 錦江灣、宮崎日南海岸、天草海域與薩摩半島近岸白線波紋 (18 組)
        const coastalLineSpots = [
            { x: -3.2, z: 7.3,  rot: 0.15, w: 1.1 },  { x: -3.1, z: 9.2,  rot: -0.2, w: 1.1 }, // 錦江灣
            { x: -1.8, z: 7.6,  rot: 0.4,  w: 0.9 },  { x: -2.0, z: 9.5,  rot: -0.4, w: 1.0 },
            { x: 9.0,  z: 1.8,  rot: 1.45, w: 1.5 },  { x: 8.8,  z: 4.5,  rot: 1.38, w: 1.5 }, // 宮崎日向灘
            { x: 8.2,  z: 7.2,  rot: 1.25, w: 1.4 },  { x: 6.4,  z: 10.1, rot: 1.05, w: 1.5 }, // 日南海岸
            { x: 9.5,  z: -3.5, rot: 1.50, w: 1.5 },  { x: 9.2,  z: -7.2, rot: 1.55, w: 1.4 },
            { x: -6.2, z: -9.8, rot: -1.25,w: 1.4 },  { x: -5.8, z: -6.8, rot: -1.35,w: 1.4 }, // 天草灘
            { x: -4.8, z: -3.2, rot: -1.45,w: 1.3 },  { x: -5.2, z: 2.5,  rot: -1.40,w: 1.4 }, // 八代海・薩摩西岸
            { x: -6.2, z: 7.8,  rot: -1.30,w: 1.5 },  { x: -5.5, z: 11.8, rot: -0.75,w: 1.5 },
            { x: -2.2, z: 12.8, rot: 0.15, w: 1.4 },  { x: 1.8,  z: 12.2, rot: 0.65, w: 1.5 }  // 指宿與佐多岬外海
        ];
        coastalLineSpots.forEach((cl, idx) => {
            const lineUnit = createWaveLineUnit(cl.w, idx % 2 === 0 ? 'wavy' : 'double');
            lineUnit.position.set(cl.x, -0.27, cl.z);
            lineUnit.rotation.y = cl.rot;
            lineUnit.userData = {
                mat: lineUnit.userData.mat,
                baseX: cl.x,
                baseZ: cl.z,
                dirX: Math.sin(cl.rot),
                dirZ: Math.cos(cl.rot),
                speed: 0.80,
                phase: idx * 0.85,
                amp: 0.28
            };
            linesGroup.add(lineUnit);
            waveLines.push(lineUnit);
        });

        oceanGroup.add(linesGroup);
        scene.add(oceanGroup);
        return { oceanGroup, seaMesh, waveLines };
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
        // 1. 海面微幅平緩起伏
        if (envState.seaMesh) {
            envState.seaMesh.position.y = -0.32 + Math.sin(elapsed * 1.4) * 0.025;
        }

        // 2. 插畫風白色線條波紋 (White Line Ripples) 優雅推進與呼吸淡入淡出
        if (envState.waveLines) {
            envState.waveLines.forEach(line => {
                const u = line.userData;
                const cycle = (elapsed * u.speed + u.phase) % (Math.PI * 2);
                const slide = Math.sin(cycle) * u.amp;
                const pulse = (Math.cos(cycle) + 1) * 0.5; // 0 ~ 1

                line.position.x = u.baseX + u.dirX * slide;
                line.position.z = u.baseZ + u.dirZ * slide;
                line.position.y = -0.27 + Math.sin(elapsed * 1.4) * 0.025;
                const s = 0.72 + pulse * 0.45;
                line.scale.set(s, 1.0, 1.0);
                if (u.mat) {
                    u.mat.opacity = 0.15 + pulse * 0.65;
                }
            });
        }

        // 3. 環繞主島與櫻島岸邊的白色海浪泡沫圈呼吸拍岸效果
        if (envState.foamMeshes) {
            envState.foamMeshes.forEach((fm, idx) => {
                if (!fm) return;
                const tide = Math.sin(elapsed * 1.8 + idx * 1.4);
                fm.position.y = -0.22 + tide * 0.025;
                const s = 1.015 + tide * 0.007;
                fm.scale.set(s, 1.0, s);
                if (fm.material) {
                    fm.material.opacity = 0.52 + tide * 0.20;
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
