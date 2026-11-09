# -*- coding: utf-8 -*-
"""
2026 日本退稅新制 (阿蘇熊本機場 KMJ 實戰長輩防呆指南) 模組
專為 2026 南九州冬季自駕手帳打造：超直觀圖解、避坑對照、常見 QA 與互動檢查清單
"""

def get_tax_refund_guide_html():
    return '''
            <!-- 🛍️ 2026 日本退稅新制・阿蘇熊本機場 (KMJ) 實戰長輩防呆指南 -->
            <div id="tax-refund-guide" class="cute-card p-5 sm:p-7 relative border-2 border-rose-300 bg-gradient-to-b from-white via-rose-50/20 to-amber-50/30 space-y-6 shadow-md">
                <div class="washi-tape washi-tape-red"></div>

                <!-- 頂部標題區 -->
                <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b-2 border-rose-100 gap-3">
                    <div>
                        <div class="flex flex-wrap items-center gap-2">
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-black bg-rose-600 text-white shadow-xs animate-pulse">
                                ⚡ 2026/11/1 日本全面實施
                            </span>
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-black bg-amber-100 text-amber-800 border border-amber-300">
                                🛫 熊本機場 (KMJ) 專屬通關指南
                            </span>
                        </div>
                        <h3 class="text-xl sm:text-2xl font-black text-stone-800 mt-2 flex items-center gap-2">
                            <span>🛍️</span> 2026 日本退稅新制・全家實戰長輩防呆攻略
                        </h3>
                        <p class="text-xs sm:text-sm text-stone-500 mt-1">
                            新制改為「先付含稅價、出境機場核驗後退稅」！破解網路 8 大機場領現迷思，長輩放心買、晚輩手機搞定、行李通關零踩雷。
                        </p>
                    </div>

                    <a href="#tax-refund-checklist" class="self-start md:self-center px-3.5 py-2 rounded-2xl bg-white hover:bg-rose-50 border-2 border-rose-200 text-rose-700 font-black text-xs flex items-center gap-1.5 shadow-xs transition">
                        <span>📋</span> 跳至離境檢核清單
                    </a>
                </div>

                <!-- 💡 長輩安心定心丸金牌 Banner -->
                <div class="bg-gradient-to-r from-amber-500 via-rose-500 to-red-500 p-0.5 rounded-2xl shadow-sm">
                    <div class="bg-white rounded-[14px] p-4 sm:p-5 flex flex-col sm:flex-row items-start sm:items-center gap-3 sm:gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-amber-100 text-amber-700 flex items-center justify-center text-2xl shrink-0 shadow-inner">
                            👵
                        </div>
                        <div class="flex-1 space-y-1">
                            <div class="flex items-center gap-2">
                                <span class="text-xs font-black px-2 py-0.5 rounded-md bg-amber-100 text-amber-800">長輩必看・一句話定心丸</span>
                                <span class="text-xs text-rose-600 font-black">店員催掃 QR Code 免驚慌！</span>
                            </div>
                            <p class="text-xs sm:text-sm text-stone-700 font-bold leading-relaxed">
                                「在唐吉訶德、百貨店裡開開心心挑選！結帳時只要<strong>出示護照、付含稅總價，把收據小白單夾在護照裡收好</strong>就好！店員叫你拿手機掃 QR Code <strong>完全不用緊張</strong>，回飯店由晚輩幫忙掃，甚至<strong>回台灣 180 天之內上網登記信用卡都有效</strong>！」
                            </p>
                        </div>
                    </div>
                </div>

                <!-- 🚀 3 步驟圖解流程卡片 (Step 1, Step 2, Step 3) -->
                <div>
                    <h4 class="text-sm font-black text-stone-700 mb-3 flex items-center gap-1.5">
                        <span>🗺️</span> 全程 3 步驟實戰圖解：
                    </h4>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <!-- Step 1: 購物 -->
                        <div class="rounded-2xl p-4 sm:p-5 bg-white border-2 border-sky-200 relative shadow-sm flex flex-col justify-between space-y-3">
                            <div class="washi-tape washi-tape-blue"></div>
                            <div class="space-y-2.5">
                                <div class="flex items-center justify-between">
                                    <span class="px-2.5 py-1 rounded-full bg-sky-100 text-sky-700 font-black text-xs">
                                        STEP 1・市區購物
                                    </span>
                                    <span class="text-2xl">🏬</span>
                                </div>
                                <h5 class="font-black text-stone-800 text-base">出示護照・拿齊小白單</h5>
                                <div class="text-xs text-stone-600 space-y-2 leading-relaxed">
                                    <div class="flex items-start gap-1.5">
                                        <span class="text-sky-600 font-bold">●</span>
                                        <span><strong>門檻合算：</strong>同一店當日未稅滿 <strong>5,000 日圓</strong>。一般品與藥妝消耗品可<strong>合併累計</strong>！</span>
                                    </div>
                                    <div class="flex items-start gap-1.5">
                                        <span class="text-sky-600 font-bold">●</span>
                                        <span><strong>付含稅價：</strong>新制店面不再直接扣稅，結帳付含稅金額（消費稅 10% 或食品 8%）。</span>
                                    </div>
                                    <div class="flex items-start gap-1.5">
                                        <span class="text-sky-600 font-bold">●</span>
                                        <span><strong>收好單據：</strong>店員給的含稅發票與退稅明細（附 QR Code），集中放進隨身護照袋。</span>
                                    </div>
                                    <div class="flex items-start gap-1.5 text-sky-700 bg-sky-50 p-2 rounded-xl border border-sky-100">
                                        <span>✨</span>
                                        <span><strong>取消密封袋：</strong>不用再忍受透明紅膠帶塑膠袋，打包更自由！</span>
                                    </div>
                                </div>
                            </div>
                            <div class="pt-2 border-t border-sky-100 text-[11px] text-sky-600 font-black">
                                💡 晚輩回飯店再用手機幫全家掃碼登記！
                            </div>
                        </div>

                        <!-- Step 2: 打包 -->
                        <div class="rounded-2xl p-4 sm:p-5 bg-white border-2 border-amber-300 relative shadow-sm flex flex-col justify-between space-y-3">
                            <div class="washi-tape washi-tape-gold"></div>
                            <div class="space-y-2.5">
                                <div class="flex items-center justify-between">
                                    <span class="px-2.5 py-1 rounded-full bg-amber-100 text-amber-800 font-black text-xs">
                                        STEP 2・飯店打包
                                    </span>
                                    <span class="text-2xl">🧳</span>
                                </div>
                                <h5 class="font-black text-stone-800 text-base">高價品手提・勿境內拆用</h5>
                                <div class="text-xs text-stone-600 space-y-2 leading-relaxed">
                                    <div class="flex items-start gap-1.5 text-rose-700 bg-rose-50 p-2 rounded-xl border border-rose-200 font-bold">
                                        <span>🚨</span>
                                        <span><strong>切勿拆封吃用：</strong>免稅品出境前<strong>絕對不能在境內拆開吃掉或使用</strong>！若海關抽驗缺件會被追討 10% 稅金。</span>
                                    </div>
                                    <div class="flex items-start gap-1.5">
                                        <span class="text-amber-600 font-bold">●</span>
                                        <span><strong>高價品放隨身包：</strong>名牌包、昂貴相機、電器、高級保養品<strong>請放手提隨身行李</strong>，不要塞大行李箱託運！</span>
                                    </div>
                                    <div class="flex items-start gap-1.5">
                                        <span class="text-amber-600 font-bold">●</span>
                                        <span><strong>避免抽查落空：</strong>若行李先託運送走，到機台被抽查亮紅燈卻拿不出實物，該筆退稅直接被廢除。</span>
                                    </div>
                                </div>
                            </div>
                            <div class="pt-2 border-t border-amber-100 text-[11px] text-amber-700 font-black">
                                ⚠️ 液體類（超過100ml）依規定放託運，但大行李先別送走！
                            </div>
                        </div>

                        <!-- Step 3: 機場 -->
                        <div class="rounded-2xl p-4 sm:p-5 bg-white border-2 border-rose-300 relative shadow-sm flex flex-col justify-between space-y-3">
                            <div class="washi-tape washi-tape-red"></div>
                            <div class="space-y-2.5">
                                <div class="flex items-center justify-between">
                                    <span class="px-2.5 py-1 rounded-full bg-rose-100 text-rose-700 font-black text-xs">
                                        STEP 3・熊本機場 KMJ
                                    </span>
                                    <span class="text-2xl">🛫</span>
                                </div>
                                <h5 class="font-black text-stone-800 text-base">先刷機台 ➔ 再掛託運行李</h5>
                                <div class="text-xs text-stone-600 space-y-2 leading-relaxed">
                                    <div class="flex items-start gap-1.5 text-rose-800 bg-rose-50 p-2 rounded-xl border border-rose-200">
                                        <span>🚫</span>
                                        <span><strong>熊本無吐鈔機：</strong>熊本機場沒有管制區現金退稅機！<strong>稅金一律自動退回信用卡</strong>。</span>
                                    </div>
                                    <div class="flex items-start gap-1.5">
                                        <span class="text-rose-600 font-bold">1.</span>
                                        <span>到出境大廳 <code>TAX REFUND</code> KIOSK 刷護照。</span>
                                    </div>
                                    <div class="flex items-start gap-1.5">
                                        <span class="text-emerald-600 font-bold">🟢</span>
                                        <span><strong>綠燈：</strong>系統核驗通過！推大行李去華航 CI195 櫃檯報到託運。</span>
                                    </div>
                                    <div class="flex items-start gap-1.5">
                                        <span class="text-rose-600 font-bold">🔴</span>
                                        <span><strong>紅燈：</strong>推行李至海關櫃台出示隨身物品核驗蓋章。</span>
                                    </div>
                                </div>
                            </div>
                            <div class="pt-2 border-t border-rose-100 text-[11px] text-rose-600 font-black">
                                🎉 通過安檢後，退稅款將自動刷退至卡片帳單！
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ⚖️ 避坑對照表：網路 8 大機場貼文 vs 熊本機場 KMJ 實戰 -->
                <div class="cute-card p-4 sm:p-5 border-2 border-stone-200 bg-stone-50/60 rounded-2xl space-y-3">
                    <div class="flex items-center gap-2">
                        <span class="text-base">⚖️</span>
                        <h4 class="text-sm font-black text-stone-800">
                            打破迷思！網路瘋傳的「大機場懶人法」與「熊本機場 (KMJ)」實況對照
                        </h4>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full text-xs text-left text-stone-700 bg-white rounded-xl border border-stone-200 overflow-hidden">
                            <thead class="bg-stone-100 text-stone-600 font-black border-b border-stone-200">
                                <tr>
                                    <th class="p-2.5 sm:p-3">比較項目</th>
                                    <th class="p-2.5 sm:p-3 text-stone-500">成田 / 關西 / 福岡 (8 大國際機場)</th>
                                    <th class="p-2.5 sm:p-3 text-rose-600 bg-rose-50/50">阿蘇熊本機場 (KMJ) ⭐️ 本次家族旅行</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-stone-100">
                                <tr>
                                    <td class="p-2.5 sm:p-3 font-bold text-stone-800">退稅款領取方式</td>
                                    <td class="p-2.5 sm:p-3">可至管制區機台領日圓現金，或退信用卡</td>
                                    <td class="p-2.5 sm:p-3 font-black text-rose-700 bg-rose-50/30">一律退回信用卡 / 電子支付帳戶（無現金機）</td>
                                </tr>
                                <tr>
                                    <td class="p-2.5 sm:p-3 font-bold text-stone-800">店員給的 QR Code</td>
                                    <td class="p-2.5 sm:p-3">若選現金機退款可暫時不管</td>
                                    <td class="p-2.5 sm:p-3 font-bold text-stone-800 bg-rose-50/30">需透過手機掃碼綁定信用卡（180天內完成即可）</td>
                                </tr>
                                <tr>
                                    <td class="p-2.5 sm:p-3 font-bold text-stone-800">託運與掃機台順序</td>
                                    <td class="p-2.5 sm:p-3">先掃機台看青紅燈 ➔ 再託運</td>
                                    <td class="p-2.5 sm:p-3 font-black text-amber-700 bg-rose-50/30">嚴格遵守先掃機台確認綠燈 ➔ 再託運行李！</td>
                                </tr>
                                <tr>
                                    <td class="p-2.5 sm:p-3 font-bold text-stone-800">手續費真實比例</td>
                                    <td class="p-2.5 sm:p-3" colspan="2">各退稅平台手續費約為未稅消費總額之 <strong>1% ~ 1.1%</strong>（絕非謠傳的整筆被吃掉10%）</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- ❓ 長輩常見問答 QA -->
                <div class="space-y-3">
                    <h4 class="text-sm font-black text-stone-700 flex items-center gap-1.5">
                        <span>💬</span> 家族常見疑問 QA（一秒解答長輩疑慮）：
                    </h4>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                        <div class="p-3.5 rounded-2xl bg-white border border-stone-200 shadow-xs space-y-1">
                            <div class="font-black text-rose-700 flex items-center gap-1.5">
                                <span>Q1.</span> 阿姨、姨丈如果沒有信用卡怎麼辦？
                            </div>
                            <p class="text-stone-600 leading-relaxed">
                                <strong>免擔心！</strong> 晚輩（阿純、阿嚕）的手機直接幫忙掃描收據上的 QR Code，綁定晚輩的信用卡帳號統一退稅，收到刷退款項後再轉發台幣或日圓給長輩即可！
                            </p>
                        </div>

                        <div class="p-3.5 rounded-2xl bg-white border border-stone-200 shadow-xs space-y-1">
                            <div class="font-black text-rose-700 flex items-center gap-1.5">
                                <span>Q2.</span> 熊本機場安檢過後的免稅店買伴手禮，還要退稅嗎？
                            </div>
                            <p class="text-stone-600 leading-relaxed">
                                <strong>完全不用！</strong> 過了安檢進入熊本國際線候機區的免稅店（Duty Free），標價本來就是免稅價，直接出示登機證結帳即可帶上飛機，完全不需任何退稅步驟。
                            </p>
                        </div>

                        <div class="p-3.5 rounded-2xl bg-white border border-stone-200 shadow-xs space-y-1">
                            <div class="font-black text-rose-700 flex items-center gap-1.5">
                                <span>Q3.</span> 買好的零食藥妝，回飯店能先拆來吃或試用嗎？
                            </div>
                            <p class="text-stone-600 leading-relaxed">
                                <strong>絕對不行！</strong> 雖然新制取消了密封膠袋，但免稅法的本質是「供帶出日本境外使用」。若海關抽查發現已被拆封使用或數量短缺，會被取消免稅資格並要求補繳 10% 消費稅！
                            </p>
                        </div>

                        <div class="p-3.5 rounded-2xl bg-white border border-stone-200 shadow-xs space-y-1">
                            <div class="font-black text-rose-700 flex items-center gap-1.5">
                                <span>Q4.</span> 如果忘記在日本登記信用卡，回台灣還能退嗎？
                            </div>
                            <p class="text-stone-600 leading-relaxed">
                                <strong>可以！</strong> 只要在熊本機場機台有掃過護照完成出境查驗，收據上的 QR Code 在購買日起 <strong>180 天內</strong>，就算回台灣打開網頁登記信用卡，稅金一樣會刷退到卡片裡！
                            </p>
                        </div>
                    </div>
                </div>

                <!-- 📋 互動式：離境退稅 5 點安心檢核表 (LocalStorage 記憶) -->
                <div id="tax-refund-checklist" class="p-4 sm:p-5 rounded-2xl bg-gradient-to-r from-rose-50 to-amber-50 border-2 border-rose-200 space-y-3">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <span class="text-base">✅</span>
                            <h4 class="text-sm font-black text-stone-800">離境出發前・5 點退稅安心核對清單</h4>
                        </div>
                        <span id="tax-checklist-progress" class="cute-pill bg-rose-100 text-rose-700 font-black text-[11px]">
                            進度 0 / 5
                        </span>
                    </div>

                    <div class="space-y-2 text-xs">
                        <label class="flex items-start gap-2.5 p-2.5 bg-white/90 rounded-xl border border-stone-200 cursor-pointer hover:bg-white transition">
                            <input type="checkbox" id="taxchk-1" onchange="updateTaxChecklist()" class="mt-0.5 rounded text-rose-600 focus:ring-rose-400">
                            <span class="text-stone-700 font-medium">1. 全家 4 本<strong>護照正本</strong>皆在隨身小包包中，方便出入機場機台隨時掃描。</span>
                        </label>
                        <label class="flex items-start gap-2.5 p-2.5 bg-white/90 rounded-xl border border-stone-200 cursor-pointer hover:bg-white transition">
                            <input type="checkbox" id="taxchk-2" onchange="updateTaxChecklist()" class="mt-0.5 rounded text-rose-600 focus:ring-rose-400">
                            <span class="text-stone-700 font-medium">2. 所有購物時取得的<strong>含稅收據小白單與 QR Code 明細</strong>已集中存放在護照夾中。</span>
                        </label>
                        <label class="flex items-start gap-2.5 p-2.5 bg-white/90 rounded-xl border border-stone-200 cursor-pointer hover:bg-white transition">
                            <input type="checkbox" id="taxchk-3" onchange="updateTaxChecklist()" class="mt-0.5 rounded text-rose-600 focus:ring-rose-400">
                            <span class="text-stone-700 font-medium">3. <strong>高單價退稅品</strong>（名牌精品、昂貴相機/電器等）已放入隨身手提袋，<strong>未</strong>直接塞進大行李箱託運。</span>
                        </label>
                        <label class="flex items-start gap-2.5 p-2.5 bg-white/90 rounded-xl border border-stone-200 cursor-pointer hover:bg-white transition">
                            <input type="checkbox" id="taxchk-4" onchange="updateTaxChecklist()" class="mt-0.5 rounded text-rose-600 focus:ring-rose-400">
                            <span class="text-stone-700 font-medium">4. 晚輩已協助長輩完成各店家 QR Code 退款管道綁定（填寫信用卡號或返台後 180 天內補填）。</span>
                        </label>
                        <label class="flex items-start gap-2.5 p-2.5 bg-white/90 rounded-xl border border-stone-200 cursor-pointer hover:bg-white transition">
                            <input type="checkbox" id="taxchk-5" onchange="updateTaxChecklist()" class="mt-0.5 rounded text-rose-600 focus:ring-rose-400">
                            <span class="text-stone-700 font-medium">5. 抵達熊本機場國際線大廳時，<strong>先至 TAX REFUND 機台刷護照亮綠燈</strong>，才推行李箱至 CI195 櫃檯辦理託運。</span>
                        </label>
                    </div>
                </div>

                <script>
                function initTaxChecklist() {
                    let count = 0;
                    for (let i = 1; i <= 5; i++) {
                        const el = document.getElementById('taxchk-' + i);
                        if (el) {
                            const saved = localStorage.getItem('kyushu_taxchk_' + i);
                            if (saved === 'true') {
                                el.checked = true;
                                count++;
                            }
                        }
                    }
                    updateTaxChecklistProgress(count);
                }

                function updateTaxChecklist() {
                    let checkedCount = 0;
                    for (let i = 1; i <= 5; i++) {
                        const el = document.getElementById('taxchk-' + i);
                        if (el) {
                            localStorage.setItem('kyushu_taxchk_' + i, el.checked ? 'true' : 'false');
                            if (el.checked) checkedCount++;
                        }
                    }
                    updateTaxChecklistProgress(checkedCount);
                }

                function updateTaxChecklistProgress(count) {
                    if (count === undefined) {
                        count = 0;
                        for (let i = 1; i <= 5; i++) {
                            const el = document.getElementById('taxchk-' + i);
                            if (el && el.checked) count++;
                        }
                    }
                    const progEl = document.getElementById('tax-checklist-progress');
                    if (progEl) {
                        progEl.textContent = '進度 ' + count + ' / 5';
                        if (count === 5) {
                            progEl.className = 'cute-pill bg-emerald-100 text-emerald-800 font-black text-[11px] animate-bounce';
                            progEl.textContent = '🎉 全數過關！安心出境！';
                        } else {
                            progEl.className = 'cute-pill bg-rose-100 text-rose-700 font-black text-[11px]';
                        }
                    }
                }

                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', initTaxChecklist);
                } else {
                    initTaxChecklist();
                }
                </script>
            </div>
'''
