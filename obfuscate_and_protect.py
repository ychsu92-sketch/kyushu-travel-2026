#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端安全加固與程式碼混淆器 (Code Obfuscator & Anti-Tamper Shield)
為「旅行大廳 (index.html)」與「2026 南九州旅行手帳」提供：
1. 深度 JavaScript 混淆（控制流平坦化、字串十六進位 Base64 編碼、變數名混淆）
2. 防右鍵拆解與防檢視原始碼 (Disable Context Menu, View Source & DevTools Shortcuts)
3. 主控台智慧安全浮水印 (Console Copyright Watermark)
4. 防全選盜取與防拖曳 (CSS Anti-Scraping Shield)
"""

import os
import re
import subprocess
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ANTI_TAMPER_SHIELD_JS = """
(function() {
    // 1. 主控台智慧安全宣告
    try {
        console.log(
            "%c🔒 2026 南九州家族旅行手帳\\n%c本網站所有 3D 演算法、動態互動與視覺設計均受著作權法保護。\\n所有程式碼皆已進行深度混淆與完整防篡改防護，嚴禁任何未經授權的逆向工程、拆解或複製抄襲行為。",
            "color:#DC2626;font-size:20px;font-weight:900;text-shadow:1px 1px 2px rgba(0,0,0,0.2);",
            "color:#4B5563;font-size:13px;font-weight:600;line-height:1.6;"
        );
    } catch(e) {}

    // 2. 防右鍵檢視選單 (防直接按檢查)
    document.addEventListener('contextmenu', function(e) {
        // 允許表單輸入框正常操作
        if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) return;
        e.preventDefault();
        showSecurityToast("🔒 本手帳受家庭隱私與版權保護，感謝您的理解！");
        return false;
    });

    // 3. 防常見開發者快捷鍵 (F12, Ctrl+U, Ctrl+Shift+I, Cmd+Opt+I)
    document.addEventListener('keydown', function(e) {
        // F12
        if (e.keyCode === 123) {
            e.preventDefault();
            return false;
        }
        // Ctrl+Shift+I (Win) 或 Cmd+Opt+I (Mac)
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.keyCode === 73 || e.key === 'I' || e.key === 'i')) {
            e.preventDefault();
            return false;
        }
        // Ctrl+Shift+J (Win) 或 Cmd+Opt+J (Mac)
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.keyCode === 74 || e.key === 'J' || e.key === 'j')) {
            e.preventDefault();
            return false;
        }
        // Ctrl+Shift+C (Win) 或 Cmd+Opt+C (Mac)
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.keyCode === 67 || e.key === 'C' || e.key === 'c')) {
            e.preventDefault();
            return false;
        }
        // Ctrl+U / Cmd+U (檢視原始碼)
        if ((e.ctrlKey || e.metaKey) && (e.keyCode === 85 || e.key === 'u' || e.key === 'U')) {
            e.preventDefault();
            return false;
        }
        // Ctrl+S / Cmd+S (存檔)
        if ((e.ctrlKey || e.metaKey) && (e.keyCode === 83 || e.key === 's' || e.key === 'S')) {
            e.preventDefault();
            return false;
        }
    });

    // 4. 防拖曳抓取
    document.addEventListener('dragstart', function(e) {
        if (e.target.tagName === 'IMG') e.preventDefault();
    });

    // 5. 輕量溫馨 Toast 提示
    function showSecurityToast(msg) {
        let toast = document.getElementById('sec-shield-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'sec-shield-toast';
            toast.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:rgba(28,25,23,0.92);color:#fff;padding:10px 20px;border-radius:9999px;font-size:13px;font-weight:700;box-shadow:0 10px 25px rgba(0,0,0,0.3);z-index:99999;pointer-events:none;transition:opacity 0.3s;opacity:0;backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.15);';
            document.body.appendChild(toast);
        }
        toast.textContent = msg;
        toast.style.opacity = '1';
        clearTimeout(toast._timer);
        toast._timer = setTimeout(function() {
            toast.style.opacity = '0';
        }, 2200);
    }
})();
"""

def obfuscate_javascript_code(js_code: str) -> str:
    """使用 javascript-obfuscator 對 JavaScript 程式碼進行深度混淆"""
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as src:
        src.write(js_code)
        src_path = src.name
        
    out_path = src_path + '.obf.js'
    
    cmd = [
        'npx', '--yes', 'javascript-obfuscator', src_path,
        '--output', out_path,
        '--compact', 'true',
        '--control-flow-flattening', 'true',
        '--control-flow-flattening-threshold', '0.4',
        '--string-array', 'true',
        '--string-array-encoding', 'base64',
        '--string-array-threshold', '0.7',
        '--identifier-names-generator', 'hexadecimal'
    ]
    
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if os.path.exists(out_path):
            with open(out_path, 'r', encoding='utf-8') as f:
                obf_code = f.read()
            return obf_code
    except Exception as e:
        print(f"⚠️ 混淆過程失敗，退回原程式碼: {e}")
        return js_code
    finally:
        if os.path.exists(src_path):
            os.remove(src_path)
        if os.path.exists(out_path):
            os.remove(out_path)
            
    return js_code

def protect_html_file(file_path: str):
    """加固單一 HTML 檔案"""
    if not os.path.exists(file_path):
        print(f"❌ 檔案不存在: {file_path}")
        return
        
    print(f"🛡️ 正在安全加固: {file_path} ...")
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # 尋找所有 inline <script> 區塊 (不包含 <script src=...>)
    pattern = re.compile(r'(<script(?![^>]*\bsrc\b)[^>]*>)(.*?)(</script>)', re.DOTALL | re.IGNORECASE)
    
    def replacer(match):
        open_tag = match.group(1)
        code = match.group(2).strip()
        close_tag = match.group(3)
        
        # 只對長度大於 300 字元的邏輯核心區塊進行深度混淆
        if len(code) > 300:
            print(f"   ⚡ 正在混淆核心腳本 (原長度: {len(code):,} 字元)...")
            # 注入防拆解防護盾
            combined = ANTI_TAMPER_SHIELD_JS + "\n" + code
            obfuscated = obfuscate_javascript_code(combined)
            print(f"   ✅ 混淆完成 (混淆後長度: {len(obfuscated):,} 字元)")
            return f"{open_tag}\n{obfuscated}\n{close_tag}"
        else:
            return match.group(0)
            
    new_html = pattern.sub(replacer, html)
    
    # 寫回加固後的 HTML
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"🎉 檔案安全加固成功: {file_path}")

def run_protection():
    # 1. 加固入口大廳
    portal_html = os.path.join(BASE_DIR, 'index.html')
    protect_html_file(portal_html)
    
    # 2. 加固南九州專題手帳
    kyushu_html = os.path.join(BASE_DIR, '2026 南九州冬季聖誕自駕', 'index.html')
    protect_html_file(kyushu_html)

if __name__ == '__main__':
    run_protection()
