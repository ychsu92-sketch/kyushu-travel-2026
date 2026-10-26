#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成家族專屬品牌識別圖示 (Favicon, Apple Touch Icon, Family Logo Badge)
來源：使用者上傳的南九州星芒山脈暖陽標誌 (Mountain, Sun & Star Minimalist Icon)
"""

import os
from PIL import Image, ImageDraw
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_IMG = "/Users/hsuyingchun/.gemini/antigravity/brain/98abf17b-ee9b-4d87-81a7-5d9ccada49a1/.user_uploaded/media_1792982744962_b69a8df5.jpg"

def create_brand_icons():
    print(f"🎨 正在載入全新品牌標誌: {SRC_IMG}")
    raw_img = Image.open(SRC_IMG).convert('RGBA')
    arr = np.array(raw_img, dtype=float)

    # 1. 外部米白象牙色背景精準轉透明與邊緣抗鋸齒羽化
    bg_ref = np.array([253, 250, 243])
    dist = np.sqrt(np.sum((arr[:, :, :3] - bg_ref)**2, axis=2))

    # 邊緣平滑過渡 (Anti-aliasing alpha mask)
    alpha = np.clip((dist - 10.0) / (28.0 - 10.0) * 255.0, 0, 255).astype(np.uint8)

    res_arr = np.array(raw_img)
    res_arr[:, :, 3] = alpha
    transparent_img = Image.fromarray(res_arr)

    # 2. 依視覺幾何中心 (523, 502) 裁切出邊長 680 的正方形畫布
    cx, cy = 523, 502
    half = 340
    crop_box = (cx - half, cy - half, cx + half, cy + half)
    cropped = transparent_img.crop(crop_box)
    
    # 建立 512x512 高畫質主 Logo (透明底)
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

    # 建立輸出目錄清單
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
        
        # 3. favicon.png (32x32 與 192x192, 512x512)
        badge.resize((32, 32), Image.Resampling.LANCZOS).save(os.path.join(d, 'favicon-32x32.png'), 'PNG')
        badge.resize((16, 16), Image.Resampling.LANCZOS).save(os.path.join(d, 'favicon-16x16.png'), 'PNG')
        badge.resize((192, 192), Image.Resampling.LANCZOS).save(os.path.join(d, 'favicon.png'), 'PNG')
        badge.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(d, 'icon-512.png'), 'PNG')
        
        # 4. apple-touch-icon.png (180x180 iOS 書籤圖示)
        apple_icon = Image.new('RGBA', (180, 180), (255, 255, 255, 255))
        scaled_inner = cropped.resize((156, 156), Image.Resampling.LANCZOS)
        apple_icon.paste(scaled_inner, (12, 12), scaled_inner)
        apple_icon.save(os.path.join(d, 'apple-touch-icon.png'), 'PNG')
        
        # 5. favicon.ico (多尺寸圖標)
        badge.resize((64, 64), Image.Resampling.LANCZOS).save(
            os.path.join(d, 'favicon.ico'),
            format='ICO',
            sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
        )
        print(f"✅ 全新圖標套件已產出至: {d}")

if __name__ == '__main__':
    create_brand_icons()
