#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_visual_and_tree_enhancements.py
1. Slight saturation & lighting enhancement:
   - env.js: sunlight 1.00 -> 1.10 (warm winter gold), ambient 0.56 -> 0.52 (better contrast), fillLight 0.25 -> 0.28
   - island.js: canvas filter 'saturate(1.22) brightness(1.02) contrast(1.02)', toneMappingExposure 1.02
2. Background tree & prop animations:
   - props.js: foliageGroup pivot on pine/ginkgo trees, gentle winter wind sway in updatePropsAnimation
   - bus stop sign subtle wind flutter
"""
import os

BASE_DIR = '/Users/reyhsu/.gemini/antigravity/scratch/kyushu-travel-2026'
ENV_PATH = os.path.join(BASE_DIR, 'portal/env.js')
ISLAND_PATH = os.path.join(BASE_DIR, 'portal/island.js')
PROPS_PATH = os.path.join(BASE_DIR, 'portal/props.js')

# 1. Update portal/env.js
with open(ENV_PATH, 'r', encoding='utf-8') as f:
    env_content = f.read()

old_env_lights = """    function setupWinterLights(scene) {
        // 1. 柔和冬季環境光 (自然溫潤、不灰暗也不過曝)
        const ambient = new THREE.AmbientLight(0xfff5eb, 0.56);
        scene.add(ambient);

        // 2. 天空與大地半球反射光
        const hemiLight = new THREE.HemisphereLight(0xd6e6f5, 0xc9b9a3, 0.44);
        hemiLight.position.set(0, 35, 0);
        scene.add(hemiLight);

        // 3. 12 月冬季低角度暖陽 (產生柔和長陰影，色澤溫暖清透)
        const sunLight = new THREE.DirectionalLight(0xffdeb8, 1.00);
        sunLight.position.set(26, 22, 18);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 2048;
        sunLight.shadow.mapSize.height = 2048;
        sunLight.shadow.camera.near = 4;
        sunLight.shadow.camera.far = 95;
        const d = 29;
        sunLight.shadow.camera.left = -d;
        sunLight.shadow.camera.right = d;
        sunLight.shadow.camera.top = d;
        sunLight.shadow.camera.bottom = -d;
        sunLight.shadow.bias = -0.0006;
        scene.add(sunLight);

        // 4. 背光側暖色補光，避免暗部死黑
        const fillLight = new THREE.DirectionalLight(0xb8c4d9, 0.25);"""

new_env_lights = """    function setupWinterLights(scene) {
        // 1. 柔和冬季環境光 (自然溫潤、明暗對比適度提升)
        const ambient = new THREE.AmbientLight(0xfff7ed, 0.52);
        scene.add(ambient);

        // 2. 天空與大地半球反射光 (清透天藍與溫暖大地)
        const hemiLight = new THREE.HemisphereLight(0xd0e6ff, 0xc7b299, 0.46);
        hemiLight.position.set(0, 35, 0);
        scene.add(hemiLight);

        // 3. 12 月冬季低角度暖金陽光 (光影立體感微幅提升，色澤溫暖清透)
        const sunLight = new THREE.DirectionalLight(0xffe2bf, 1.10);
        sunLight.position.set(26, 22, 18);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 2048;
        sunLight.shadow.mapSize.height = 2048;
        sunLight.shadow.camera.near = 4;
        sunLight.shadow.camera.far = 95;
        const d = 29;
        sunLight.shadow.camera.left = -d;
        sunLight.shadow.camera.right = d;
        sunLight.shadow.camera.top = d;
        sunLight.shadow.camera.bottom = -d;
        sunLight.shadow.bias = -0.0006;
        scene.add(sunLight);

        // 4. 背光側清透天光補光，加強陰影層次與通透感
        const fillLight = new THREE.DirectionalLight(0xb8d4f0, 0.28);"""

if old_env_lights in env_content:
    env_content = env_content.replace(old_env_lights, new_env_lights)
    with open(ENV_PATH, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("portal/env.js updated with enhanced lighting!")
else:
    print("portal/env.js already has enhanced lighting.")

# 2. Update portal/island.js
with open(ISLAND_PATH, 'r', encoding='utf-8') as f:
    island_content = f.read()

old_filter = "renderer.toneMappingExposure = 1.00;\n        renderer.domElement.style.filter = 'saturate(1.16) brightness(1.01) contrast(1.01)';"
new_filter = "renderer.toneMappingExposure = 1.02;\n        renderer.domElement.style.filter = 'saturate(1.22) brightness(1.02) contrast(1.02)';"

if old_filter in island_content:
    island_content = island_content.replace(old_filter, new_filter)
    with open(ISLAND_PATH, 'w', encoding='utf-8') as f:
        f.write(island_content)
    print("portal/island.js updated with enhanced saturation and exposure!")
else:
    print("portal/island.js already has enhanced saturation and exposure.")

# 3. Update portal/props.js
with open(PROPS_PATH, 'r', encoding='utf-8') as f:
    props_content = f.read()

# 3A. Update buildP09_WinterPineAndSnowman to wrap foliage in foliageGroup
old_tree_code = """        const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 0.32, 6), trunkMat);
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
        }"""

new_tree_code = """        const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 0.32, 6), trunkMat);
        trunk.position.y = 0.16;
        g.add(trunk);

        // 建立微風搖擺樹冠群組 (foliageGroup，支點位於樹幹頂端 y = 0.24)
        const foliageGroup = new THREE.Group();
        foliageGroup.position.y = 0.24;

        const foliage1 = new THREE.Mesh(new THREE.ConeGeometry(0.32, 0.46, 7), pineMat);
        foliage1.position.y = 0.18;
        const foliage2 = new THREE.Mesh(new THREE.ConeGeometry(0.25, 0.38, 7), pineMat);
        foliage2.position.y = 0.42;
        foliageGroup.add(foliage1, foliage2);

        if (!isGinkgo) {
            const snowCap = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.24, 7), snowMat);
            snowCap.position.y = 0.54;
            foliageGroup.add(snowCap);
        }
        g.add(foliageGroup);
        g.userData.foliageGroup = foliageGroup;"""

if old_tree_code not in props_content:
    print("ERROR: old_tree_code not found in props.js")
    exit(1)

props_content = props_content.replace(old_tree_code, new_tree_code)

# 3B. Update buildP16_BusStop to add roundSign userData
old_bus_sign = """        const roundSign = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.02, 16), signMat);
        roundSign.rotation.x = Math.PI / 2;
        roundSign.position.set(0.32, 0.46, 0.06);"""

new_bus_sign = """        const roundSign = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.02, 16), signMat);
        roundSign.rotation.x = Math.PI / 2;
        roundSign.position.set(0.32, 0.46, 0.06);
        g.userData.roundSign = roundSign;"""

if old_bus_sign in props_content:
    props_content = props_content.replace(old_bus_sign, new_bus_sign)

# 3C. In populateIslandProps, collect trees and busStops
old_tree_populate = """        treeCoords.forEach((tc, idx) => {
            const pos = nudgeOffRoadAndLandmarks(tc[0], tc[1], 0.90, 0.95);
            const t = buildP09_WinterPineAndSnowman(tc[3]);
            t.scale.setScalar(1.05 + (idx % 3) * 0.22);
            t.position.set(pos.x, pos.y, pos.z);
            t.rotation.y = idx * 1.1;
            propsGroup.add(t);
        });"""

new_tree_populate = """        const trees = [];
        treeCoords.forEach((tc, idx) => {
            const pos = nudgeOffRoadAndLandmarks(tc[0], tc[1], 0.90, 0.95);
            const t = buildP09_WinterPineAndSnowman(tc[3]);
            t.scale.setScalar(1.05 + (idx % 3) * 0.22);
            t.position.set(pos.x, pos.y, pos.z);
            t.rotation.y = idx * 1.1;
            t.userData.windPhase = idx * 0.73;
            propsGroup.add(t);
            trees.push(t);
            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.38 });
        });"""

if old_tree_populate not in props_content:
    print("ERROR: old_tree_populate not found in props.js")
    exit(1)

props_content = props_content.replace(old_tree_populate, new_tree_populate)

# 3D. Collect busStops
old_bus_populate = """        busStopCoords.forEach(bc => {
            const pos = nudgeOffRoadAndLandmarks(bc.x, bc.z, 0.88, 0.92);
            const bs = buildP16_BusStop();
            bs.scale.setScalar(1.15);
            bs.position.set(pos.x, pos.y, pos.z);
            bs.rotation.y = bc.rot;
            propsGroup.add(bs);
            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.42 });
        });"""

new_bus_populate = """        const busStops = [];
        busStopCoords.forEach(bc => {
            const pos = nudgeOffRoadAndLandmarks(bc.x, bc.z, 0.88, 0.92);
            const bs = buildP16_BusStop();
            bs.scale.setScalar(1.15);
            bs.position.set(pos.x, pos.y, pos.z);
            bs.rotation.y = bc.rot;
            propsGroup.add(bs);
            busStops.push(bs);
            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.42 });
        });"""

if old_bus_populate not in props_content:
    print("ERROR: old_bus_populate not found in props.js")
    exit(1)

props_content = props_content.replace(old_bus_populate, new_bus_populate)

# 3E. Update return of populateIslandProps
old_props_return = "return { propsGroup, minivan, tram, ferry, pets, walkers, cattleList, windTurbines, fishingBoats, sampleGroundY: getGroundY };"
new_props_return = "return { propsGroup, minivan, tram, ferry, pets, walkers, cattleList, windTurbines, fishingBoats, trees, busStops, sampleGroundY: getGroundY };"

if old_props_return not in props_content:
    print("ERROR: old_props_return not found in props.js")
    exit(1)

props_content = props_content.replace(old_props_return, new_props_return)

# 3F. In updatePropsAnimation, add tree and bus stop sway
old_update_end = """        // 7. 外海彩色小漁船隨波浪起伏晃動
        if (propState.fishingBoats) {
            propState.fishingBoats.forEach((boat, idx) => {
                const phase = elapsed * 1.8 + idx * 1.5;
                boat.position.y = -0.06 + Math.sin(phase) * 0.025;
                boat.rotation.z = Math.sin(phase * 0.8) * 0.05;
                boat.rotation.x = Math.cos(phase * 0.9) * 0.035;
            });
        }
    }"""

new_update_end = """        // 7. 外海彩色小漁船隨波浪起伏晃動
        if (propState.fishingBoats) {
            propState.fishingBoats.forEach((boat, idx) => {
                const phase = elapsed * 1.8 + idx * 1.5;
                boat.position.y = -0.06 + Math.sin(phase) * 0.025;
                boat.rotation.z = Math.sin(phase * 0.8) * 0.05;
                boat.rotation.x = Math.cos(phase * 0.9) * 0.035;
            });
        }

        // 8. 全島 92 棵覆雪杉木與銀杏樹隨冬日微風自然輕柔搖擺 (Winter Wind Tree Sway)
        if (propState.trees) {
            propState.trees.forEach(t => {
                const phase = elapsed * 1.55 + (t.userData.windPhase || 0);
                const gust = Math.sin(elapsed * 0.42 + (t.userData.windPhase || 0) * 0.5) * 0.25 + 0.75;
                if (t.userData.foliageGroup) {
                    t.userData.foliageGroup.rotation.z = Math.sin(phase) * (0.048 * gust);
                    t.userData.foliageGroup.rotation.x = Math.cos(phase * 0.82) * (0.032 * gust);
                } else {
                    t.rotation.z = Math.sin(phase) * (0.032 * gust);
                }
            });
        }

        // 9. 鄉間巴士站圓形站牌微風輕擺
        if (propState.busStops) {
            propState.busStops.forEach((bs, idx) => {
                if (bs.userData.roundSign) {
                    bs.userData.roundSign.rotation.z = Math.sin(elapsed * 2.2 + idx * 0.8) * 0.045;
                }
            });
        }
    }"""

if old_update_end not in props_content:
    print("ERROR: old_update_end not found in props.js")
    exit(1)

props_content = props_content.replace(old_update_end, new_update_end)

with open(PROPS_PATH, 'w', encoding='utf-8') as f:
    f.write(props_content)

print("portal/props.js successfully updated with tree swaying and bus stop flutter animations!")
