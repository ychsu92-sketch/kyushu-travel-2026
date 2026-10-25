#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成家族專屬品牌識別圖示 (Favicon, Apple Touch Icon, Family Logo Badge)
來源：使用者上傳的 HSU 紫金繁星花體標誌
"""

import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from collections import deque

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_IMG = "/Users/hsuyingchun/.gemini/antigravity/brain/98abf17b-ee9b-4d87-81a7-5d9ccada49a1/.user_uploaded/media_1792901320074_1f755579.jpg"

def create_brand_icons():
    print(f"🎨 正在載入原始標誌: {SRC_IMG}")
    raw_img = Image.open(SRC_IMG).convert('RGBA')
    arr = np.array(raw_img)
    h, w = arr.shape[:2]

    # 1. 外部純白背景漸進泛洪轉透明
    visited = np.zeros((h, w), dtype=bool)
    queue = deque([(0, 0), (0, w-1), (h-1, 0), (h-1, w-1)])
    for y, x in queue:
        visited[y, x] = True

    def is_bg(r, g, b):
        return r > 246 and g > 246 and b > 246

    while queue:
        cy, cx = queue.popleft()
        arr[cy, cx, 3] = 0
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                visited[ny, nx] = True
                r, g, b, _ = arr[ny, nx]
                if is_bg(r, g, b):
                    queue.append((ny, nx))

    transparent_img = Image.fromarray(arr)

    # 尋找圖形邊界
    coords = np.argwhere(arr[:, :, 3] > 0)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    max_dim = max(x1 - x0, y1 - y0) + 36
    half = max_dim // 2

    crop_box = (max(0, cx - half), max(0, cy - half), min(w, cx + half), min(h, cy + half))
    cropped = transparent_img.crop(crop_box)
    
    # 建立 512x512 高畫質主 Logo
    logo_512 = cropped.resize((512, 512), Image.Resampling.LANCZOS)
    
    # 建立圓形白色背底徽章 (適用於瀏覽器標籤頁與深色模式 Favicon)
    badge_size = 512
    badge = Image.new('RGBA', (badge_size, badge_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    
    # 畫柔和圓形白底徽章
    margin = 8
    draw.ellipse([margin, margin, badge_size - margin, badge_size - margin], fill=(255, 255, 255, 255))
    
    # 將 Logo 貼在白底徽章中央
    inner_size = badge_size - margin * 4
    inner_logo = cropped.resize((inner_size, inner_size), Image.Resampling.LANCZOS)
    badge.paste(inner_logo, (margin * 2, margin * 2), inner_logo)

    # 建立輸出目錄
    out_dirs = [
        BASE_DIR,
        os.path.join(BASE_DIR, '2026 南九州冬季聖誕自駕'),
        '/tmp/kyushu-travel-deploy',
        '/tmp/kyushu-travel-deploy/2026 南九州冬季聖誕自駕',
        '/tmp/kyushu-travel-deploy/kyushu-2026',
        '/tmp/kyushu-travel-deploy/旅行'
    ]

    for d in out_dirs:
        os.makedirs(d, exist_ok=True)
        # 1. family_logo.png (高解析透明底主標誌)
        logo_512.save(os.path.join(d, 'family_logo.png'), 'PNG')
        
        # 2. family_badge.png (圓形白色徽章)
        badge.save(os.path.join(d, 'family_badge.png'), 'PNG')
        
        # 3. favicon.png (32x32 與 192x192)
        badge.resize((32, 32), Image.Resampling.LANCZOS).save(os.path.join(d, 'favicon-32x32.png'), 'PNG')
        badge.resize((16, 16), Image.Resampling.LANCZOS).save(os.path.join(d, 'favicon-16x16.png'), 'PNG')
        badge.resize((192, 192), Image.Resampling.LANCZOS).save(os.path.join(d, 'favicon.png'), 'PNG')
        badge.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(d, 'icon-512.png'), 'PNG')
        
        # 4. apple-touch-icon.png (180x180 iOS 書籤圖示)
        apple_icon = Image.new('RGBA', (180, 180), (255, 255, 255, 255))
        scaled_inner = cropped.resize((160, 160), Image.Resampling.LANCZOS)
        apple_icon.paste(scaled_inner, (10, 10), scaled_inner)
        apple_icon.save(os.path.join(d, 'apple-touch-icon.png'), 'PNG')
        
        # 5. favicon.ico (多尺寸圖標)
        badge.resize((64, 64), Image.Resampling.LANCZOS).save(
            os.path.join(d, 'favicon.ico'),
            format='ICO',
            sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
        )
        print(f"✅ 圖標套件已產出至: {d}")

if __name__ == '__main__':
    create_brand_icons()
