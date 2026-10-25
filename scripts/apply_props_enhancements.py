#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_props_enhancements.py
Adds roadside scenery builders, placements, and animations to portal/props.js:
- P15: Roadside Torii gates
- P16: Rural Bus Stops
- P17: Stone Lanterns & Jizo
- P18: Coastal Wind Turbines (with rotating blades)
- P19: Small Fishing Boats (with bobbing animation)
- P20: Highway Mileage Signs
- Dense tree coordinates (expanded from 38 to 92 trees)
"""
import os
import re

PROPS_PATH = '/Users/reyhsu/.gemini/antigravity/scratch/kyushu-travel-2026/portal/props.js'

with open(PROPS_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Builders for P15 ~ P20 to insert before PROP_SPECS
new_builders = """
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
"""

# Insert new builders right before `const PROP_SPECS = [`
specs_idx = content.find('    const PROP_SPECS = [')
if specs_idx == -1:
    print("ERROR: PROP_SPECS not found")
    exit(1)

content = content[:specs_idx] + new_builders + "\n" + content[specs_idx:]

# Also update PROP_SPECS list to include P15-P20
specs_replace = """        { code: 'P14', name: '朱紅溪谷拱橋', badge: '🌉 河川名橋', desc: '橫跨球磨川、五瀨川與大淀川的日式朱紅拱橋。', build: buildP14_RedArchBridge },
        { code: 'P15', name: '公路沿線朱紅鳥居', badge: '⛩️ 神道地標', desc: '佇立於公路邊、通往山林古社的朱紅神道鳥居。', build: buildP15_RoadsideTorii },
        { code: 'P16', name: '九州懷舊鄉間巴士站', badge: '🚏 鄉村站牌', desc: '木造遮雨棚、圓形站牌與長椅的經典日式鄉村巴士候車亭。', build: buildP16_BusStop },
        { code: 'P17', name: '日式石燈籠與地藏小祠', badge: '🏮 古道守護', desc: '點綴在公路與溫泉古道的暖光石燈籠與紅色圍兜地藏菩薩。', build: buildP17_StoneLantern },
        { code: 'P18', name: '沿海風力發電機', badge: '💨 海岸風車', desc: '佇立於日向灘與日南海岸公路旁的旋轉白色大型風力發電機。', build: buildP18_WindTurbine },
        { code: 'P19', name: '鹿兒島灣彩色小漁船', badge: '⛵ 港灣船隻', desc: '停泊在錦江灣與日南海岸外海的日式近海彩色漁船。', build: () => buildP19_SmallFishingBoat(0x2563eb) },
        { code: 'P20', name: '國道公路里程指示牌', badge: '🛣️ 國道路標', desc: '標示 R3、R57、R220 國道地名與里程的綠底白字公路標誌。', build: buildP20_RoadMileageSign }"""

content = content.replace(
    "        { code: 'P14', name: '朱紅溪谷拱橋', badge: '🌉 河川名橋', desc: '橫跨球磨川、五瀨川與大淀川的日式朱紅拱橋。', build: buildP14_RedArchBridge }",
    specs_replace
)

# 2. Update populateIslandProps to place all the new props and dense trees!
# We find treeCoords definition
tree_coords_old = """        // 11. 冬季覆雪杉木林、金黃銀杏林與雪人點綴 (增加到 38 處，1.2x 地圖座標)
        const treeCoords = [
            // 阿蘇・黑川・高千穗北部山林
            [1.44, -16.32, 0.96, 'snow'],   [2.64, -18.00, 0.96, 'snow'],   [5.88, -17.40, 0.96, 'snow'],
            [6.24, -13.44, 0.96, 'snow'],   [5.52, -10.32, 0.96, 'snow'],   [2.88, -10.08, 1.02, 'snow'],
            [0.72, -15.84, 0.80, 'ginkgo'], [-3.12, -14.64,0.80, 'ginkgo'], [-0.96, -11.76,0.80, 'tree_only'],
            // 中央山地與球磨川流域大森林 (填滿中央區域)
            [0.96, -7.80,  1.02, 'snow'],   [3.12, -8.16,  1.05, 'snow'],   [4.56, -9.00,  1.02, 'snow'],
            [5.76, -6.24,  1.02, 'tree_only'],[3.60, -5.40,1.02, 'snow'],   [1.68, -4.20,  1.02, 'tree_only'],
            [0.24, -5.76,  0.96, 'ginkgo'], [-2.16, -5.04, 0.82, 'tree_only'],[-2.88, -7.44,0.80, 'ginkgo'],
            [6.96, -8.16,  0.96, 'tree_only'],[8.16, -5.76,0.82, 'tree_only'],[7.44, -2.64, 0.82, 'ginkgo'],
            [4.56, -2.16,  0.96, 'tree_only'],[2.40, -1.80,0.96, 'snow'],   [0.60, -0.48,  0.96, 'tree_only'],
            // 霧島・人吉・宮崎・鹿兒島南部林木
            [-2.64, 0.60,  0.80, 'ginkgo'], [-0.72, 2.16,  0.96, 'tree_only'],[1.80, 2.64,  0.96, 'snow'],
            [3.84,  1.92,  0.96, 'tree_only'],[5.76, 0.96, 0.82, 'ginkgo'], [7.68, 4.32,    0.80, 'tree_only'],
            [-0.96, 6.48,  0.96, 'snow'],   [2.16,  6.96,  0.82, 'tree_only'],[4.20, 6.24,  0.82, 'ginkgo'],
            [-5.52, 11.28, 0.80, 'ginkgo'], [-4.56, 13.44, 0.80, 'tree_only'],[0.96, 11.76, 0.80, 'tree_only'],
            [1.92,  9.84,  0.80, 'ginkgo'], [-0.24, 13.80, 0.80, 'tree_only']
        ];"""

tree_coords_new = """        // 11. 覆雪杉木林、金黃銀杏林與雪人點綴 (高密度擴充至 92 處，徹底消除公路兩側空洞)
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
        ];"""

content = content.replace(tree_coords_old, tree_coords_new)

# Insert Roadside Props (P15 Torii, P16 Bus Stop, P17 Stone Lantern, P18 Wind Turbines, P19 Fishing Boats, P20 Roadside Signs) right after tree placement
roadside_placement_code = """
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
"""

# Find return statement of populateIslandProps
old_return = "return { propsGroup, minivan, tram, ferry, pets, walkers, cattleList, sampleGroundY: getGroundY };"
new_return = "return { propsGroup, minivan, tram, ferry, pets, walkers, cattleList, windTurbines, fishingBoats, sampleGroundY: getGroundY };"

ret_idx = content.find(old_return)
if ret_idx == -1:
    print("ERROR: old_return not found")
    exit(1)

content = content[:ret_idx] + roadside_placement_code + "\n        " + new_return + content[ret_idx + len(old_return):]

# 3. In updatePropsAnimation, add animation for wind turbines and fishing boats
old_update_end = """        // 5. 阿蘇赤牛低頭吃草擺動
        if (propState.cattleList) {
            propState.cattleList.forEach(cow => {
                if (cow.userData.head) {
                    cow.userData.head.rotation.x = 0.25 + Math.sin(elapsed * 2.2 + cow.userData.phase) * 0.22;
                }
            });
        }
    }"""

new_update_end = """        // 5. 阿蘇赤牛低頭吃草擺動
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
    }"""

content = content.replace(old_update_end, new_update_end)

with open(PROPS_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("portal/props.js successfully updated with roadside props and 92 trees!")
