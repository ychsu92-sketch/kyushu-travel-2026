#!/usr/bin/env python3
# -*- coding: utf-8 -*-
PROPS_PATH = '/Users/reyhsu/.gemini/antigravity/scratch/kyushu-travel-2026/portal/props.js'

with open(PROPS_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 在 populateIslandProps 開頭定義 sceneObstacles
content = content.replace(
    "        const propsGroup = new THREE.Group();\n        const getGroundY = sampleGroundY || (() => 0.80);",
    "        const propsGroup = new THREE.Group();\n        const getGroundY = sampleGroundY || (() => 0.80);\n        const sceneObstacles = [];"
)

# 2. 為每個迴圈增加 sceneObstacles.push
content = content.replace(
    "            propsGroup.add(m);\n        });\n\n        // 5. 日式木造町家聚落組",
    "            propsGroup.add(m);\n            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.65 });\n        });\n\n        // 5. 日式木造町家聚落組"
)

content = content.replace(
    "            propsGroup.add(m);\n        });\n\n        // 6. 日本街角自動販賣機與紅郵筒組",
    "            propsGroup.add(m);\n            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.85 });\n        });\n\n        // 6. 日本街角自動販賣機與紅郵筒組"
)

content = content.replace(
    "            propsGroup.add(vm);\n        });\n\n        // 7. 阿蘇草千里與霧島牧場放牧赤牛群",
    "            propsGroup.add(vm);\n            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.40 });\n        });\n\n        // 7. 阿蘇草千里與霧島牧場放牧赤牛群"
)

content = content.replace(
    "            propsGroup.add(cow);\n            cattleList.push(cow);\n        });",
    "            propsGroup.add(cow);\n            cattleList.push(cow);\n            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.50 });\n        });"
)

content = content.replace(
    "            propsGroup.add(b);\n        });\n\n        // 9. 小貓與柴犬",
    "            propsGroup.add(b);\n            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.60 });\n        });\n\n        // 9. 小貓與柴犬"
)

content = content.replace(
    "            propsGroup.add(t);\n        });\n\n        // 12. 公路沿線朱紅鳥居",
    "            propsGroup.add(t);\n            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.38 });\n        });\n\n        // 12. 公路沿線朱紅鳥居"
)

content = content.replace(
    "            propsGroup.add(torii);\n        });\n\n        // 13. 九州懷舊鄉間巴士候車亭與站牌",
    "            propsGroup.add(torii);\n            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.45 });\n        });\n\n        // 13. 九州懷舊鄉間巴士候車亭與站牌"
)

content = content.replace(
    "            propsGroup.add(bs);\n        });\n\n        // 14. 暖光石燈籠與路旁地藏小祠",
    "            propsGroup.add(bs);\n            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.42 });\n        });\n\n        // 14. 暖光石燈籠與路旁地藏小祠"
)

content = content.replace(
    "            propsGroup.add(sl);\n        });\n\n        // 15. 宮崎/日南沿海風力發電機群",
    "            propsGroup.add(sl);\n            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.35 });\n        });\n\n        // 15. 宮崎/日南沿海風力發電機群"
)

content = content.replace(
    "            propsGroup.add(wt);\n            windTurbines.push(wt);\n        });",
    "            propsGroup.add(wt);\n            windTurbines.push(wt);\n            sceneObstacles.push({ x: tc.x, z: tc.z, r: 0.55 });\n        });"
)

content = content.replace(
    "            propsGroup.add(rSign);\n        });\n\n        return {",
    "            propsGroup.add(rSign);\n            sceneObstacles.push({ x: pos.x, z: pos.z, r: 0.35 });\n        });\n\n        window.KyushuIsland.Obstacles = sceneObstacles;\n\n        return {"
)

with open(PROPS_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Obstacle registry successfully added to portal/props.js")
