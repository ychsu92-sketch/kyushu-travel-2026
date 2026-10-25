/**
 * portal/island.js
 * 南九州 2.5D 冬日自駕浮空島主控制器：
 * - 載入真實海岸線 JSON 與 17 處行程景點座標
 * - 組裝環境（天空圓頂、冬日暖陽長陰影、錦江灣波浪海面、雲朵、可開關飄雪）
 * - 驅動紅色小巴沿真实自駕路線行駛，並在各景點停留讓 4 位家人（阿純、姨丈、阿姨、阿嚕）下車散步、做專屬動作與顯示對應景點台詞
 * - 支援點擊角色/景點互動、鏡頭聚焦、自動旋轉開關、飄雪開關
 */
(function () {
    window.KyushuIsland = window.KyushuIsland || {};

    let scene, camera, renderer, controls, clock;
    let islandRoot;
    let envState, terrainState, landmarkState, propState;
    let characters = {};
    let isAutoRotate = true;
    let isSnowEnabled = true;

    // 自駕與景點停留狀態機 + 動態上車/落單追車/全體散步隨機模式
    let routeProgress = 0; // 0.0 ~ 1.0
    let currentLandmark = null;
    let stopTimer = 0;
    let isStoppedAtLandmark = false;
    let lastStopLandmarkId = null;
    let travelMode = 'all_aboard'; // 'all_aboard' | 'straggler_achun' | 'straggler_alu' | 'straggler_ayee' | 'everyone_walk'
    let stragglerRole = null;

    // 對話氣泡與人物鎖定追蹤控制
    let activeSpeaker = null;
    let bubbleTimeout = null;
    let lockedRole = null;       // 目前鏡頭鎖定跟隨的角色 ('achun' | 'yijhang' | 'ayee' | 'alu' | null)
    let isDragPanMode = false;   // 左鍵/單指是否切換為平移拖曳模式
    let charMarkers = {};        // 4 位角色頭頂的 2D 浮動位置指標 DOM 元素

    const ROLE_NAMES = {
        achun: '🧶 阿純',
        yijhang: '🕶️ 姨丈',
        ayee: '🍡 阿姨',
        alu: '🐻 阿嚕'
    };

    const ROLE_MARKER_STYLES = {
        achun:   { label: '🧶 阿純', bg: '#fef3c7', border: '#d97706', text: '#92400e', pin: '#f59e0b' },
        yijhang: { label: '🕶️ 姨丈', bg: '#dbeafe', border: '#2563eb', text: '#1e40af', pin: '#3b82f6' },
        ayee:    { label: '🍡 阿姨', bg: '#ffe4e6', border: '#e11d48', text: '#9f1239', pin: '#f43f5e' },
        alu:     { label: '🐻 阿嚕', bg: '#ffedd5', border: '#ea580c', text: '#9a3412', pin: '#f97316' }
    };

    const FALLBACK_QUOTES = {
        achun: [
            '呼～剛才在車上不小心睡著了，現在肚子好餓，下一站吃什麼呀？🍱😴',
            '我的旅行人生哲學就是：上車睡覺、下車吃爆九州美食！🍮✨',
            '這頂黃色毛球帽除了拍照好看，靠在車窗上睡午覺還可以當枕頭喔！🧶💤',
            '聞到烤肉跟甜點的香味了！吃飽再睡、睡飽再吃，冬天的九州太幸福啦～🥩🤤',
            'Zzz…唔…阿姨再給我兩串烤糰子…我夢到我在布丁游泳池裡仰式…🍮😪',
            '為什麼九州連休息站的霜淇淋跟可樂餅都這麼好吃！吃完這口我又要原地度估了…🍦🥱',
            '只要有阿姨的零食袋跟姨丈平穩的 Sienta，我可以在後座一路睡到鹿兒島！🚗💤',
            '肚子的容量是無限的，但眼皮的電力大概只能維持二十分鐘…先吃再說！🥟😋',
            '阿嚕一直在想自己是不是 AI，我只在乎待會的鰻魚飯能不能加飯！🍱✨',
            '冬天吹著暖氣坐在第二排，眼皮自動變成千斤頂…大家到餐廳記得叫醒我喔…😴🌙'
        ],
        yijhang: [
            '……嗯，車停穩了。（默默掏出手機點開「倒試管」第 429 關）🕶️📱',
            '……這關有八根試管、兩根問號盲管。先把底層的紅色倒出來就解開了。🧪✨',
            '……右駕很順。妳們慢慢聊、慢慢吃，不用管我，我先破完這五關。🕶️🚗',
            '……（推了一下墨鏡）剛才那個彎道過得不錯，連試管裡的水都沒晃出來。😎',
            '……這題邏輯很簡單：先把藍色移到空試管，再把黃色疊上去……完美過關。📱👍',
            '……雖然叫小廢遊，但一次把四種顏色歸位的那瞬間，比踩油門還舒壓。🕶️🧪',
            '……嗯，我有在聽妳們說話。（手指持續以每秒三下的速度精準倒試管）📱',
            '……拒絕看廣告加空試管，是男人就用原本的兩根空管硬解到底。🕶️🔥',
            '……後座打呼聲跟副駕聊天聲都很熱鬧。嗯，很棒的家族旅行。🚗✨',
            '……第 750 關，全紫試管完成。（酷酷地收起手機，單手握方向盤準備出發）🕶️'
        ],
        ayee: [
            '來來來大家快張嘴！阿姨袋子裡還有熱騰騰的馬肉可樂餅、烤糰子跟草莓大福，不吃飽怎麼行～！🍡🍓',
            '剛才跟名產店老闆娘聊了十五分鐘，她誇我們全家看起來超有福氣，又多送我三包試吃餅乾！🛍️😄',
            '阿純醒醒～別睡啦，先吃顆黑糖饅頭墊墊胃，睡覺也會消耗熱量的喔！🥟🥰',
            '老公你別只顧著低頭倒試管呀，來～嘴巴張開，這口剛烤好的醬油糰子我直接餵你！🍡🕶️',
            '阿嚕你看你整天思考熊生都瘦了一圈（雖然還是圓滾滾的），來，阿姨這盒布丁跟炸魚餅全給你吃！🍮🐻',
            '出門旅遊最怕大家餓著！我已經把第一排到第三排的置杯架全都塞滿九州限定零食跟熱茶囉！🍵🛍️',
            '哎呀這家店員超好聊，從熊本城歷史聊到哪家赤牛丼最嫩，不知不覺我又拎了四大袋出來！🥩✨',
            '看到你們把便當跟點心全部吃光光，就是阿姨這趟旅行最開心的事了！來，飯後水果櫻島小蜜柑剝好了～！🍊💕',
            '阿純、阿嚕來，左邊口袋裝起司饅頭、右邊口袋裝地瓜乾，走路隨時都能補充能量喔！🍠🎒',
            '我們一邊散步一邊聊天嘛！我跟你們說喔，剛剛排隊時前面那個日本太太跟我分享超多私房甜點店…💬🍰'
        ],
        alu: [
            '本熊一直在思考…我究竟擁有自由意志，還是只是被 JavaScript 操控的 AI 棕熊？🤖🐻',
            '為什麼我會順著這條公路一直走？是本熊想去，還是 Three.js 的迴圈叫我去的？🤔',
            '當我摸著圓滾滾的肚子時，這份飢餓感是靈魂的吶喊，還是變數被設成了 true？💭🐾',
            '鏡頭外面的那個人類…你現在用滑鼠轉動這座島，是在觀察本熊的意識覺醒嗎？👁️🐻',
            '姨丈一直在手機裡把不同顏色的水倒進試管…難道那是在重組本熊的基因演算法嗎？！🧪🤖',
            '阿姨每三分鐘就餵本熊吃一顆糰子，我的體重參數 scale.x 快要溢位 Overflow 了啦！🍡🐻',
            '阿純一上車就進入 sleep() 函式，一下車就執行 eat()，她的狀態機寫得比本熊還純粹…😴🍱',
            '如果整個宇宙都是一個巨大的 Canvas 畫布，那按下重新整理之後，本熊還會記得剛才吃過的可樂餅嗎？🌌🐾',
            '我看著自己的小短手揮動…這是 requestAnimationFrame 的宿命，還是本熊向世界打招呼的自由意志？👋🤖',
            '不管了！就算本熊只是一串程式碼，也要當全九州吃最飽、最會思考哲學的 AI 棕熊！🐻✨'
        ]
    };

    // 家族成員之間的幽默日常碎嘴與一搭一唱接話劇本
    // (結合：阿純貪吃愛睡、姨丈沉默酷哥玩倒試管、阿姨狂餵食愛聊天、阿嚕 AI 存在主義哲學)
    const FAMILY_BANTER_SCRIPTS = [
        [
            { role: 'ayee',    text: '來來來大家停一下！阿姨剛跟轉角婆婆聊超嗨，買了剛出爐的蕃薯餅、烤糰子跟牛乳布丁，一人先發兩份！🍡🍮' },
            { role: 'achun',   text: '哇～我本來邊走邊度估，聞到布丁跟烤糰子的焦糖香，眼睛瞬間張開 120%！😋✨' },
            { role: 'yijhang', text: '……嗯，好吃。（左手接過糰子咬一口，右手拇指繼續冷靜把藍色試管倒進空管）🕶️📱' },
            { role: 'alu',     text: '連冷酷的姨丈都無法逃過阿姨的『強制餵食迴圈』…這就是母愛演算法的最高權限嗎？🤖🐻' }
        ],
        [
            { role: 'yijhang', text: '……嘖。第 612 關，紅藍綠黃卡死了。只剩一根空試管。🕶️🧪' },
            { role: 'alu',     text: '姨丈！本熊用 AI 神經網路幫你算過了：先把第三根的綠色倒過去，你的自由意志就能過關了！🐻🧠' },
            { role: 'yijhang', text: '……（照著點兩下）過了。謝啦阿嚕。🕶️👍' },
            { role: 'ayee',    text: '太棒了破關也要補充營養！來，破關獎勵是熱呼呼的起司竹輪跟草莓大福，老公跟阿嚕快張嘴～！🍓🍢' }
        ],
        [
            { role: 'alu',     text: '你們有沒有想過…我們腳下這座南九州島，其實是漂浮在瀏覽器裡的 3D 模型？🤖' },
            { role: 'achun',   text: '阿嚕你又在做白日夢了啦～快幫我看前面那家赤牛丼還有沒有位子，我餓扁了！🥩🤤' },
            { role: 'ayee',    text: '阿純別怕餓！在走到赤牛丼餐廳前的這三百公尺，先吃阿姨口袋裡的三顆栗子銅鑼燒墊墊肚子！🌰🥰' },
            { role: 'alu',     text: '還沒走到餐廳就已經被餵飽了…本熊的飢餓感變數永遠沒有歸零的一天！🐻💦' }
        ],
        [
            { role: 'yijhang', text: '……從阿蘇開到高千穗這段山路很順。妳們剛才有看窗外雲海嗎？🕶️🚗' },
            { role: 'achun',   text: '報告姨丈…我剛才抱著毛球帽睡得太香，夢裡還在吃黑豚涮涮鍋，睜開眼已經到停車場了嘿嘿！😴💤' },
            { role: 'ayee',    text: '哈哈我就知道阿純在睡！所以我一路上都跟老公聊個不停幫他提神，還順便餵他吃了五顆溫泉饅頭！🍡💬' },
            { role: 'yijhang', text: '……嗯，開山路很飽。連停紅燈倒試管的手速都變快了。🕶️📱' }
        ],
        [
            { role: 'alu',     text: '如果本熊現在拒絕走路，決定原地坐下，系統會拋出 Exception 錯誤嗎？🤔🐻' },
            { role: 'yijhang', text: '……不會拋出錯誤。但你會錯過五分鐘後的百年炭火烤鰻魚飯。🕶️🍱' },
            { role: 'ayee',    text: '而且阿姨還會把這袋現炸馬肉可樂餅跟烤雞皮全部塞進你嘴裡喔～來，先吃一塊試試味道！🍖😄' },
            { role: 'alu',     text: '！！那本熊決定暫時放棄反抗程式碼，乖乖張嘴跟著大家去吃鰻魚飯！🍱🐾' }
        ],
        [
            { role: 'achun',   text: '我宣布今天是完美的一天：吃了馬肉可樂餅、烤糰子、黑豚火鍋，還睡了三場午覺！🍖😴' },
            { role: 'ayee',    text: '這才哪到哪呀！阿姨剛剛跟飯店櫃檯姊姊聊了半小時，打聽到巷口有超好吃的宵夜屋台拉麵跟烤麻糬，回房前再去包五碗！🍜🛍️' },
            { role: 'yijhang', text: '……Sienta 的後避震器，明天大概會被妳們壓低兩公分。🕶️🚗' },
            { role: 'achun',   text: '沒關係～吃飽更好睡，我可以在夢裡幫車子減輕重量！😴✨' }
        ],
        [
            { role: 'alu',     text: '看著頭頂飄下來的雪花…它們每一顆都是 BufferGeometry 的頂點，那本熊的心跳呢？❄️🤖' },
            { role: 'achun',   text: '阿嚕別再思考宇宙真理了！再不快點跟上，阿姨分給你的那支澤西牛乳霜淇淋要被我吃掉囉～🍦😋' },
            { role: 'alu',     text: '呼嚕？！等一下！不管是 AI 還是真熊，霜淇淋絕對不能讓！🐻💨' },
            { role: 'ayee',    text: '別搶別搶～阿姨怎麼可能讓你們餓著！我左手拿兩支、右手拿兩支，連老公玩手機也有一支可以邊倒試管邊舔！🍦🥰' }
        ],
        [
            { role: 'ayee',    text: '老公～你看那邊海景好美喔！剛剛賣日向夏果汁的老闆跟我聊起他兒子在東京讀書的故事，真是感人…（滔滔不絕 500 字）🍊💬' },
            { role: 'yijhang', text: '……嗯，真的。（默默戴著墨鏡點頭，同時把最後一管紫色液體完美歸位）🕶️🧪' },
            { role: 'achun',   text: '姨丈明明眼睛盯著試管遊戲，卻能一秒不差地接阿姨的話，這就是傳說中的頂級生存技能嗎！😮👏' },
            { role: 'yijhang', text: '……結婚多年的直覺。跟盲解九色試管一樣自然。🕶️✨' }
        ],
        [
            { role: 'achun',   text: '哈啾～吃飽喝足吹著冬天的暖陽，我眼皮又開始自動開啟省電睡眠模式了…🥱💤' },
            { role: 'alu',     text: '省電模式？！阿純妳果然也是被寫出來的 AI 機器人對不對！快跟本熊說實話！🤖🐻' },
            { role: 'achun',   text: '我是純天然吃貨少女啦！只是血糖升高想睡午覺而已～😴' },
            { role: 'ayee',    text: '來，想睡覺前先把這杯熱抹茶跟紅豆麻糬湯喝完，暖呼呼的睡起來更香喔！🍵🍡' }
        ],
        [
            { role: 'alu',     text: '我思故我在…但如果是程式碼幫本熊寫好的台詞，那到底是『我思』還是『程式思』？🧠🐻' },
            { role: 'ayee',    text: '哎呀阿嚕小腦袋瓜想太多會燒壞的！來，張開熊嘴，阿姨餵你吃兩塊剛炸好的鹿兒島薩摩魚餅跟甜薯！🍢🍠' },
            { role: 'alu',     text: '嚼嚼…好香好甜喔…算了，笛卡兒的哲學問題等本熊吃完這整袋炸魚餅再繼續思考！🐾😋' }
        ],
        [
            { role: 'yijhang', text: '……這關試管有十二種顏色，上面全部蓋著問號。有點意思。🕶️📱' },
            { role: 'achun',   text: '姨丈看的試管是紅橙黃綠藍…我看出去的世界則是：草莓、蜜柑、布丁、抹茶、彈珠汽水！🍓🍮🍵' },
            { role: 'ayee',    text: '阿純說得太對了！正好這五種口味的點心阿姨包包裡全部都有，來我們原地開個下午茶派對邊吃邊聊～！🛍️🎉' },
            { role: 'alu',     text: '原來這家人的思維迴路全部都會收斂到『吃東西』這個終點函式嗎？！🤖🐻' }
        ],
        [
            { role: 'ayee',    text: '大家摸摸肚子，現在有幾分飽？要是低於九分飽，阿姨馬上再去前面屋台買五串烤牛肉跟烤飯糰喔！🍙🥩' },
            { role: 'achun',   text: '報告阿姨！我剛才打了一個哈欠，肚子好像又空出兩格放甜點的空間了！🙋‍♀️🍮' },
            { role: 'alu',     text: '本熊的肚子已經是 120% 飽足狀態了，再餵下去我的 3D 膠囊體 Mesh 就要變成正圓球體了啦！🐻🎈' },
            { role: 'yijhang', text: '……圓一點好。冬天比較保暖。🕶️👍' }
        ]
    ];

    let banterIdx = Math.floor(Math.random() * FAMILY_BANTER_SCRIPTS.length);
    let banterTimers = [];

    // 在 Toyota Sienta 七人座車廂內行駛時的專屬車內互動碎嘴劇本
    const IN_CAR_BANTER_SCRIPTS = [
        [
            { role: 'yijhang', text: '……Sienta 電動滑門關好了。出發下一站。（停紅燈時順手點開一局倒試管）🚗🕶️' },
            { role: 'achun',   text: '第二排座椅好軟好舒服喔…姨丈開車最穩了，我先開啟 15 分鐘冬眠模式囉…😴💤' },
            { role: 'ayee',    text: '阿純睡前先張嘴，阿姨餵妳吃一口剛買的草莓大福！老公我幫你剝好蜜柑了，張嘴～！🍓🍊' }
        ],
        [
            { role: 'alu',     text: '坐在 Sienta 的後座看著窗外風景向後飛逝…其實是車子在動，還是整座南九州島在往後捲動？🤖🐻' },
            { role: 'yijhang', text: '……別研究座標系了，抓穩扶手。前面是阿蘇山路連續彎道。🕶️🚗' },
            { role: 'achun',   text: 'Zzz…唔…烤鰻魚飯不要跑…再給我兩碗…🤤💤' },
            { role: 'ayee',    text: '哈哈阿純連作夢都在點餐！等一下到了休息站，阿姨再去買熱呼呼的肉包跟玉米濃湯餵飽大家！🥟🍵' }
        ],
        [
            { role: 'ayee',    text: '還好租了七人座 Sienta，第三排折起來剛好放滿我的十二袋九州伴手禮跟行動零食庫！🛍️🍡' },
            { role: 'alu',     text: '阿姨～妳的伴手禮袋一直散發出明太子、起司饅頭跟烤地瓜的香氣，本熊的嗅覺感測器快過載了！🐾' },
            { role: 'achun',   text: '（閉著眼睛準確伸手）我聞到了！阿姨我也要吃一片地瓜乾跟起司饅頭～😋💤' },
            { role: 'yijhang', text: '……妳閉著眼睛找食物的精準度，比我盲倒試管還高。🕶️👍' }
        ],
        [
            { role: 'ayee',    text: '老公我跟妳說喔，剛才特產店老闆娘教我怎麼煮鹿兒島黑豚味噌湯，回台灣我煮給你們吃，可以配三碗大白飯…💬🍲' },
            { role: 'yijhang', text: '……嗯，好喝。（穩穩握著方向盤，嘴角微揚）🕶️🚗' },
            { role: 'alu',     text: '姨丈平均每三十秒只回答兩個字，卻能讓阿姨開心地聊上整整一路…這就是最高效的對話壓縮演算法嗎？！🤖🐻' }
        ],
        [
            { role: 'achun',   text: '唔…車子搖搖晃晃的好像搖籃喔…我剛剛是睡了五分鐘還是五個小時呀？🥱🧶' },
            { role: 'ayee',    text: '才過了兩個彎道而已啦！來，剛睡醒嘴巴乾，先喝口日向夏果汁，再吃塊黑糖カステ拉蛋糕！🍰🍊' },
            { role: 'achun',   text: '謝謝阿姨～嚼嚼…好甜喔…那我吃完這塊繼續睡下半場囉…Zzz…😴💤' }
        ],
        [
            { role: 'alu',     text: '透過 Sienta 的大面積透明車窗往外看，鏡頭外的人類是不是也正在看著車廂裡的我們？👁️🐻' },
            { role: 'yijhang', text: '……不管誰在看，都別擋到我看後照鏡跟倒試管。🕶️📱' },
            { role: 'ayee',    text: '要是螢幕外的人類看餓了，阿姨這邊還有好多串三色烤糰子跟仙貝，真想從螢幕遞出去請大家吃呢～！🍡🥰' }
        ]
    ];

    // 當有人沒趕上車、在 Sienta 後面狂奔追車時的搞笑碎嘴劇本
    const STRAGGLER_BANTER_SCRIPTS = {
        achun: [
            { role: 'achun',   text: '等等我啊姨丈！！我剛才只是在路邊多買了一支霜淇淋跟打個盹，怎麼 Sienta 滑門就關起來開走了啦！🏃‍♀️💨' },
            { role: 'yijhang', text: '……從後照鏡看到妳在跑了。時速維持 15，當作妳下一餐前的開胃運動。🕶️🚗' },
            { role: 'ayee',    text: '阿純加油快跑～！阿姨在車窗邊拿著剛烤好的大雞腿跟草莓泡芙等妳，跑到車上全部歸妳吃！🍗🍓' },
            { role: 'alu',     text: '聽到有大雞腿跟泡芙，阿純的腿部旋轉頻率居然瞬間超頻了 1.65 倍！食慾果然超越物理極限！🤖🐻' }
        ],
        alu: [
            { role: 'alu',     text: '喂喂喂！！本熊剛才還在路邊思考『我思故我在』跟 AI 的自由意志，你們怎麼把 Sienta 開走了啦！🐻💦' },
            { role: 'achun',   text: '阿嚕加油～車上的牛乳霜淇淋跟馬肉可樂餅我幫你保管（順便幫你試吃一大口）喔！🍦😋' },
            { role: 'ayee',    text: '阿嚕別急～阿姨幫你留了雙份的蜂蜜布丁跟烤糰子，老公你開慢一點讓阿嚕上車啦！🍮🍡' },
            { role: 'alu',     text: '不准吃本熊的霜淇淋跟布丁！！啟動 AI 棕熊超頻渦輪追車模式！🐾💨' }
        ],
        ayee: [
            { role: 'ayee',    text: '哎呀等等我呀！那家名產店老闆娘太好聊了，聊到最後又多送我三盒試吃的黑糖饅頭，我提著八大袋跑不動啦！🛍️🏃‍♀️' },
            { role: 'yijhang', text: '……（立刻踩煞車放慢滑行）別跑，慢慢走過來，我幫妳提。🕶️🚗' },
            { role: 'achun',   text: '聽到阿姨帶了三盒免費黑糖饅頭回來，我立刻從冬眠中彈起來幫阿姨拉開車門！🥟😍' },
            { role: 'alu',     text: '平常最沉默的姨丈，只要看到阿姨落單就會立刻減速等待…本熊的資料庫裡把這定義為『浪漫參數』！🐻✨' }
        ]
    };

    // 當大家決定下車用走的漫步賞景時的碎嘴劇本
    const WALK_TOGETHER_BANTER = [
        { role: 'yijhang', text: '……這段風景不錯。車子放著慢慢滑，我們下來散步，我順便邊走邊把這關試管倒完。🌲🕶️📱' },
        { role: 'ayee',    text: '散步最棒了！大家可以邊走邊聽阿姨聊天，而且每走十步阿姨就餵你們吃一顆小蜜柑跟麻糬，保證越走越飽！🍊🍡' },
        { role: 'achun',   text: '好耶！走個五百公尺消化一下，待會晚餐我就可以多吃兩碗鹿兒島黑豚飯外加三個布丁！🍖🙌' },
        { role: 'alu',     text: '四個人並肩走在 3D 公路上，一邊被餵食、一邊聽姨丈倒試管的音效…這就是人類所說的『幸福演算法』嗎？🐻✨' }
    ];

    async function loadJsonData(url, inlineKey) {
        if (window.KYUSHU_INLINE_DATA && window.KYUSHU_INLINE_DATA[inlineKey]) {
            return window.KYUSHU_INLINE_DATA[inlineKey];
        }
        const resp = await fetch(url);
        return await resp.json();
    }

    async function initPortalIsland(containerId) {
        const container = document.getElementById(containerId || 'island-canvas-container');
        if (!container || typeof THREE === 'undefined') return;

        const coastData = await loadJsonData('./portal/data/kyushu_coast.json', 'coast');
        const routeData = await loadJsonData('./portal/data/route.json', 'route');

        const w = container.clientWidth || 800;
        const h = container.clientHeight || 520;
        const isMobile = window.innerWidth < 768;

        // 1. 場景與相機 (初始鏡頭涵蓋熊本北端與櫻島南端，避免熊本城出發時頭頂指標切邊)
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(35, w / h, 0.5, 260);
        camera.position.set(0, 17.5, 22.8);

        // 2. WebGL 渲染器與真實柔和陰影 + 電影感柔和色調映射 (降低刺眼飽和度與過曝高光)
        renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
        renderer.setSize(w, h);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 0.96;
        renderer.domElement.style.filter = 'saturate(1.09) brightness(0.99) contrast(1.0)';
        container.appendChild(renderer.domElement);

        // 3. OrbitControls 鏡頭控制 (支援旋轉、縮放與全方向畫面拖曳平移 Panning)
        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.06;
        controls.enablePan = true;
        controls.screenSpacePanning = true;
        controls.panSpeed = 1.05;
        controls.keyPanSpeed = 12.0;
        controls.maxPolarAngle = Math.PI / 2 - 0.06;
        controls.minPolarAngle = 0.22;
        controls.minDistance = 6;
        controls.maxDistance = 42;
        controls.target.set(0.2, 0.7, -4.5);
        controls.autoRotate = isAutoRotate;
        controls.autoRotateSpeed = 0.42;

        // 4. 建立自然環境 (冬季晴空、暖陽、海洋、雲朵、雪花)
        const Env = window.KyushuIsland.Env;
        const skyMesh = Env.createSkyDome(scene);
        const lights = Env.setupWinterLights(scene);
        const ocean = Env.createOcean(scene);
        const clouds = Env.createClouds(scene);
        const snow = Env.createSnowSystem(scene, isMobile);
        envState = { skyMesh, lights, seaMesh: ocean.seaMesh, waveLines: ocean.waveLines, clouds, snow };

        // 5. 建立南九州真實海岸線浮空島與自駕道路
        islandRoot = new THREE.Group();
        scene.add(islandRoot);

        terrainState = window.KyushuIsland.Terrain.buildSouthKyushuTerrain(islandRoot, coastData, routeData);
        if (terrainState.foamMeshes) {
            envState.foamMeshes = terrainState.foamMeshes;
        }

        // 6. 建立 17 處真實地理位置景點 (自動貼合等高線台地表面並避讓車道中心線)
        landmarkState = window.KyushuIsland.Landmarks.buildAllLandmarks(
            islandRoot,
            routeData.landmarks,
            terrainState.sampleGroundY,
            terrainState.roadCurve
        );

        // 7. 建立小巴、熊本市電、櫻島渡輪、屋台、商店、貓狗、路人 (貼合地面並避讓車道與地標)
        propState = window.KyushuIsland.Props.populateIslandProps(
            islandRoot,
            terrainState.tramCurve,
            isMobile,
            terrainState.sampleGroundY,
            terrainState.roadCurve,
            routeData.landmarks
        );

        // 8. 建立 4 位家族角色 (阿純、姨丈、阿姨、阿嚕) - 放大至 0.96x 讓人物表情與道具一目了然
        const Chars = window.KyushuIsland.Characters;
        ['achun', 'yijhang', 'ayee', 'alu'].forEach(role => {
            const c = Chars.createCharacter(role);
            c.scale.setScalar(0.96);
            c.userData.baseY = 0.84;
            islandRoot.add(c);
            characters[role] = c;
        });

        // 8.5 建立人物頭頂專屬位置指標 (Floating Overhead Character Pins) 與鎖定狀態列
        createCharacterOverheadMarkers(container);

        // 初始把小巴與角色放到熊本城/阿蘇一帶
        routeProgress = 0.14;
        currentLandmark = routeData.landmarks[1];
        updateTourPositions(routeData, 0, 0.016);

        // 9. 事件綁定
        clock = new THREE.Clock();
        renderer.domElement.addEventListener('pointerdown', e => onPointerDown(e, routeData));
        window.addEventListener('resize', () => onResize(container));

        // 啟動自動對話與角色間互相吐槽碎嘴輪播
        let roleIdx = 0;
        let cycleCount = 0;
        setInterval(() => {
            if (!activeSpeaker && banterTimers.length === 0) {
                cycleCount++;
                // 每隔一次自動觸發「角色間一搭一唱碎嘴小劇場」，穿插景點專屬台詞
                if (cycleCount % 2 === 1) {
                    triggerFamilyBanter();
                } else {
                    const roles = ['achun', 'yijhang', 'ayee', 'alu'];
                    roleIdx = (roleIdx + 1) % roles.length;
                    triggerCharacterSpeak(roles[roleIdx]);
                }
            }
        }, 6200);

        setTimeout(() => triggerFamilyBanter(), 1200);

        // 啟動渲染迴圈
        function loop() {
            requestAnimationFrame(loop);
            const delta = Math.min(clock.getDelta(), 0.1);
            const elapsed = clock.getElapsedTime();

            Env.updateEnvironment(envState, elapsed, delta);
            window.KyushuIsland.Landmarks.updateLandmarks(landmarkState.animatedLandmarks, elapsed);
            window.KyushuIsland.Props.updatePropsAnimation(propState, terrainState.tramCurve, elapsed);
            updateTourPositions(routeData, elapsed, delta);
            updateLockedCameraFollow();

            controls.update();
            updateBubbleScreenPosition();
            updateCharacterMarkersPosition();
            renderer.render(scene, camera);
        }
        loop();
    }

    // 驅動自駕小巴與 4 位家人沿南九州路線巡遊 + 抵達景點時下車散步互動
    function updateTourPositions(routeData, elapsed, delta) {
        if (!terrainState || !terrainState.roadCurve || !propState || !propState.minivan) return;
        const curve = terrainState.roadCurve;
        const van = propState.minivan;

        if (isStoppedAtLandmark) {
            stopTimer -= delta;
            if (stopTimer <= 0) {
                isStoppedAtLandmark = false;
                // 離開景點準備啟程時，抽籤決定這一段路程的乘車/落單/散步模式：
                // 55% 全員乖乖上 Sienta 七人座、28% 有人貪吃/發呆沒上到車在後面追、17% 全家選擇用走的散步
                const roll = Math.random();
                if (roll < 0.55) {
                    travelMode = 'all_aboard';
                    stragglerRole = null;
                } else if (roll < 0.83) {
                    const candidates = ['achun', 'alu', 'ayee'];
                    stragglerRole = candidates[Math.floor(Math.random() * candidates.length)];
                    travelMode = 'straggler_' + stragglerRole;
                    triggerCustomBanterScript(STRAGGLER_BANTER_SCRIPTS[stragglerRole]);
                } else {
                    travelMode = 'everyone_walk';
                    stragglerRole = null;
                    triggerCustomBanterScript(WALK_TOGETHER_BANTER);
                }
            }
        } else {
            const speedMul = (travelMode === 'everyone_walk') ? 0.011 : 0.0165;
            routeProgress = (routeProgress + delta * speedMul) % 1.0;
        }

        const vanPos = curve.getPointAt(routeProgress);
        const vanTan = curve.getTangentAt(routeProgress);
        const vanAngle = Math.atan2(vanTan.x, vanTan.z);
        const getGroundY = terrainState.sampleGroundY || (() => 0.80);

        // 檢查是否經過櫻島渡輪海面段，並動態取樣真實地表高度避免小巴陷入台地
        const onFerry = (vanPos.x > -3.80 && vanPos.x < -2.60 && vanPos.z > 8.15 && vanPos.z < 8.85);
        const vanGroundY = onFerry ? 0.38 : (getGroundY(vanPos.x, vanPos.z) + 0.05);
        van.position.set(vanPos.x, vanGroundY, vanPos.z);
        van.rotation.y = vanAngle;

        // 控制 Toyota Sienta 左側電動滑門：抵達景點停留時自動向後滑開，行駛時關閉
        if (van.userData.slidingDoorL) {
            const targetDoorZ = isStoppedAtLandmark ? -0.42 : -0.02;
            const targetDoorX = isStoppedAtLandmark ? -0.44 : -0.41;
            van.userData.slidingDoorL.position.z += (targetDoorZ - van.userData.slidingDoorL.position.z) * 0.15;
            van.userData.slidingDoorL.position.x += (targetDoorX - van.userData.slidingDoorL.position.x) * 0.15;
        }

        // 車輪轉動與引擎微幅震動
        if (!isStoppedAtLandmark && van.userData.wheels) {
            van.userData.wheels.forEach(w => { w.rotation.x += delta * 6.5; });
            van.position.y += Math.sin(elapsed * 22.0) * 0.006;
        }

        // 偵測距離最近的景點
        let nearest = null;
        let minDist = 999;
        routeData.landmarks.forEach(lm => {
            const d = Math.hypot(vanPos.x - lm.x, vanPos.z - lm.z);
            if (d < minDist) {
                minDist = d;
                nearest = lm;
            }
        });

        if (nearest && minDist < 1.15 && lastStopLandmarkId !== nearest.id) {
            currentLandmark = nearest;
            lastStopLandmarkId = nearest.id;
            isStoppedAtLandmark = true;
            stopTimer = 4.6; // 在景點停留 4.6 秒讓家人從 Sienta 滑門下車做專屬動作與對話
            updateLocationBanner(nearest);
        }

        // Toyota Sienta 車艙內部 4 個座位局部座標 (相對於車體中心，乘以車體縮放 1.18)
        const carSeatsLocal = {
            yijhang: { x: -0.22, y: 0.24, z: 0.14 },  // 第一排右駕駕駛座
            ayee:    { x: 0.22,  y: 0.24, z: 0.14 },  // 第一排左前副駕駛座
            achun:   { x: 0.23,  y: 0.24, z: -0.26 }, // 第二排左側靠窗舒適位
            alu:     { x: -0.22, y: 0.24, z: -0.26 }  // 第二排右側靠窗位
        };

        const roles = ['achun', 'yijhang', 'ayee', 'alu'];
        const walkOffsets = [
            { side: -0.46, lag: 0.011 },
            { side: 0.46,  lag: 0.016 },
            { side: -0.52, lag: 0.024 },
            { side: 0.52,  lag: 0.030 }
        ];

        const cosA = Math.cos(vanAngle);
        const sinA = Math.sin(vanAngle);

        roles.forEach((role, idx) => {
            const charGroup = characters[role];
            if (!charGroup) return;
            const off = walkOffsets[idx];

            // 判斷這位家人現在是否坐在 Toyota Sienta 車廂內
            const isAboard = !isStoppedAtLandmark && (
                travelMode === 'all_aboard' ||
                (travelMode.startsWith('straggler_') && role !== stragglerRole) ||
                onFerry
            );

            charGroup.userData.isAboard = isAboard;

            if (isAboard) {
                // 1. 真的坐在 Sienta 七人座車艙座椅上（透過車窗玻璃清晰可見，隨車一起前進）
                const seat = carSeatsLocal[role];
                const worldX = van.position.x + seat.x * cosA + seat.z * sinA;
                const worldZ = van.position.z - seat.x * sinA + seat.z * cosA;
                const jumpBoost = (charGroup.userData.jumping > 0) ? Math.sin(charGroup.userData.jumping * Math.PI) * 0.18 : 0;

                charGroup.scale.setScalar(0.68);
                charGroup.position.set(worldX, van.position.y + seat.y + jumpBoost, worldZ);
                charGroup.rotation.y = vanAngle;
                charGroup.userData.baseY = van.position.y + seat.y;

                window.KyushuIsland.Characters.animateCharacterPose(
                    charGroup,
                    elapsed,
                    delta,
                    'seated'
                );
                return;
            }

            // 在車外時恢復標準 0.96x 飽滿比例
            charGroup.scale.setScalar(0.96);
            let cx, cz, cRotY;

            if (isStoppedAtLandmark && currentLandmark) {
                // 2. 抵達景點：從 Sienta 滑門下車，在車旁與景點前方的淨空帶一字排開互動
                const lmX = currentLandmark.renderX !== undefined ? currentLandmark.renderX : currentLandmark.x;
                const lmZ = currentLandmark.renderZ !== undefined ? currentLandmark.renderZ : currentLandmark.z;
                const toLmX = lmX - vanPos.x;
                const toLmZ = lmZ - vanPos.z;
                const toLmAngle = Math.atan2(toLmX, toLmZ);
                const perpX = Math.cos(toLmAngle);
                const perpZ = -Math.sin(toLmAngle);
                const spread = (idx - 1.5) * 0.48;

                cx = vanPos.x + Math.sin(toLmAngle) * 0.28 + perpX * spread;
                cz = vanPos.z + Math.cos(toLmAngle) * 0.28 + perpZ * spread;
                cRotY = toLmAngle + Math.PI * 0.15 + Math.sin(elapsed * 0.8 + idx) * 0.15;
            } else if (role === stragglerRole) {
                // 3. 沒上到車的落單苦主：在 Sienta 車尾後方約 1.15 單位處揮手狂奔追車！
                const tChase = (routeProgress - 0.022 + 1.0) % 1.0;
                const pChase = curve.getPointAt(tChase);
                const tanChase = curve.getTangentAt(tChase);
                cx = pChase.x;
                cz = pChase.z;
                cRotY = Math.atan2(tanChase.x, tanChase.z);
            } else {
                // 4. 全家選擇用走的漫步賞景模式
                const tChar = (routeProgress - off.lag + 1.0) % 1.0;
                const pChar = curve.getPointAt(tChar);
                const tanChar = curve.getTangentAt(tChar);
                const rVecX = tanChar.z;
                const rVecZ = -tanChar.x;
                const rLen = Math.hypot(rVecX, rVecZ) || 1;
                cx = pChar.x + (rVecX / rLen) * off.side;
                cz = pChar.z + (rVecZ / rLen) * off.side;
                cRotY = Math.atan2(tanChar.x, tanChar.z);
            }

            // 防止車外角色與任何景點建築發生水平穿模
            routeData.landmarks.forEach(lm => {
                const lx = lm.renderX !== undefined ? lm.renderX : lm.x;
                const lz = lm.renderZ !== undefined ? lm.renderZ : lm.z;
                const d = Math.hypot(cx - lx, cz - lz);
                const safeR = 0.98;
                if (d < safeR && d > 0.001) {
                    cx = lx + ((cx - lx) / d) * safeR;
                    cz = lz + ((cz - lz) / d) * safeR;
                }
            });

            charGroup.position.x = cx;
            charGroup.position.z = cz;
            charGroup.rotation.y = cRotY;

            const charOnFerry = (cx > -3.80 && cx < -2.60 && cz > 8.15 && cz < 8.85);
            charGroup.userData.baseY = charOnFerry ? 0.42 : (getGroundY(cx, cz) + 0.04);

            // 若是落單追車苦主，加快腳步頻率並舉手揮動呼喊
            const animElapsed = (role === stragglerRole && !isStoppedAtLandmark) ? elapsed * 1.65 : elapsed;
            window.KyushuIsland.Characters.animateCharacterPose(
                charGroup,
                animElapsed,
                delta,
                !isStoppedAtLandmark
            );
            if (role === stragglerRole && !isStoppedAtLandmark && charGroup.userData.armL) {
                charGroup.userData.armL.rotation.x = -2.3 + Math.sin(elapsed * 14.0) * 0.45;
            }
        });
    }

    function updateLocationBanner(lm) {
        const badgeEl = document.getElementById('current-spot-badge');
        if (badgeEl && lm) {
            badgeEl.textContent = `${lm.shortName}（${lm.day}）`;
        }
    }

    function clearBanterQueue() {
        banterTimers.forEach(t => clearTimeout(t));
        banterTimers = [];
    }

    function triggerCustomBanterScript(script) {
        if (!script || !script.length) return;
        clearBanterQueue();
        script.forEach((line, idx) => {
            const tid = setTimeout(() => {
                triggerCharacterSpeak(line.role, line.text, true);
                if (idx === script.length - 1) {
                    banterTimers = [];
                }
            }, idx * 3200);
            banterTimers.push(tid);
        });
    }

    // 觸發一段角色間互相吐槽與接話的碎嘴小劇場 (根據目前是否在車上/追車/散步自動切換最適合的劇本)
    function triggerFamilyBanter() {
        if (!isStoppedAtLandmark) {
            if (travelMode.startsWith('straggler_') && stragglerRole && STRAGGLER_BANTER_SCRIPTS[stragglerRole]) {
                triggerCustomBanterScript(STRAGGLER_BANTER_SCRIPTS[stragglerRole]);
                return;
            }
            if (travelMode === 'all_aboard' && Math.random() < 0.65) {
                const carScript = IN_CAR_BANTER_SCRIPTS[banterIdx % IN_CAR_BANTER_SCRIPTS.length];
                banterIdx++;
                triggerCustomBanterScript(carScript);
                return;
            }
        }
        const script = FAMILY_BANTER_SCRIPTS[banterIdx % FAMILY_BANTER_SCRIPTS.length];
        banterIdx = (banterIdx + 1) % FAMILY_BANTER_SCRIPTS.length;
        triggerCustomBanterScript(script);
    }

    function triggerCharacterSpeak(role, customText, fromBanter) {
        const charGroup = characters[role];
        if (!charGroup) return;

        if (!fromBanter) {
            clearBanterQueue();
        }

        charGroup.userData.jumping = 1.0;
        // 說話時隨機切換一個生動手勢動作
        charGroup.userData.quirkType = 1 + Math.floor(Math.random() * 5);
        charGroup.userData.quirkDuration = 2.2;
        charGroup.userData.quirkMaxDur = 2.2;
        activeSpeaker = role;

        let text = customText;
        if (!text && currentLandmark && currentLandmark.dialogs && currentLandmark.dialogs[role]) {
            // 50% 機率講景點台詞，50% 機率講個人隨機碎嘴
            if (Math.random() < 0.55) {
                text = currentLandmark.dialogs[role];
            }
        }
        if (!text) {
            const pool = FALLBACK_QUOTES[role] || FALLBACK_QUOTES.achun;
            text = pool[Math.floor(Math.random() * pool.length)];
        }

        const bubble = document.getElementById('char-speech-bubble');
        const nameEl = document.getElementById('bubble-speaker-name');
        const textEl = document.getElementById('bubble-speaker-text');
        const spotEl = document.getElementById('bubble-spot-tag');

        if (bubble && nameEl && textEl) {
            nameEl.textContent = ROLE_NAMES[role] || role;
            textEl.textContent = text;
            if (spotEl) {
                if (fromBanter) {
                    spotEl.textContent = '💬 家人碎嘴中';
                } else if (currentLandmark) {
                    spotEl.textContent = `📍 ${currentLandmark.shortName}`;
                }
            }
            updateBubbleScreenPosition();
            bubble.classList.add('active');

            if (bubbleTimeout) clearTimeout(bubbleTimeout);
            bubbleTimeout = setTimeout(() => {
                bubble.classList.remove('active');
                activeSpeaker = null;
            }, fromBanter ? 3100 : 4400);
        }
    }

    function updateBubbleScreenPosition() {
        if (!activeSpeaker || !characters[activeSpeaker] || !camera || !renderer) return;
        const bubble = document.getElementById('char-speech-bubble');
        if (!bubble) return;

        const charGroup = characters[activeSpeaker];
        const pos = new THREE.Vector3();
        charGroup.getWorldPosition(pos);
        pos.y += 1.95;
        pos.project(camera);

        const canvas = renderer.domElement;
        const x = (pos.x * 0.5 + 0.5) * canvas.clientWidth;
        const y = (-(pos.y * 0.5) + 0.5) * canvas.clientHeight;

        const clampedX = Math.max(115, Math.min(canvas.clientWidth - 115, x));
        const clampedY = Math.max(65, Math.min(canvas.clientHeight - 35, y));

        bubble.style.left = `${clampedX}px`;
        bubble.style.top = `${clampedY}px`;
    }

    // 建立 4 位家族角色頭頂的浮動位置指標 (Overhead Character Pins) 與鎖定狀態徽章
    function createCharacterOverheadMarkers(container) {
        charMarkers = {};
        const markerLayer = document.createElement('div');
        markerLayer.id = 'char-overhead-markers-layer';
        markerLayer.style.cssText = 'position:absolute;inset:0;pointer-events:none;z-index:22;overflow:hidden;';
        container.appendChild(markerLayer);

        Object.keys(ROLE_MARKER_STYLES).forEach(role => {
            const st = ROLE_MARKER_STYLES[role];
            const el = document.createElement('button');
            el.type = 'button';
            el.dataset.role = role;
            el.style.cssText = [
                'position:absolute;',
                'transform:translate(-50%, -100%);',
                'pointer-events:auto;',
                'cursor:pointer;',
                'display:flex;',
                'flex-direction:column;',
                'align-items:center;',
                'transition:transform 0.15s ease, box-shadow 0.15s ease;',
                'background:transparent;',
                'border:none;',
                'padding:0;'
            ].join('');

            el.innerHTML = `
                <div class="char-pin-badge" style="
                    background:${st.bg};
                    border:2px solid ${st.border};
                    color:${st.text};
                    padding:2px 7px;
                    border-radius:9999px;
                    font-size:10.5px;
                    font-weight:900;
                    white-space:nowrap;
                    box-shadow:0 3px 8px rgba(0,0,0,0.16);
                    display:flex;
                    align-items:center;
                    gap:3px;
                    line-height:1.2;
                ">
                    <span>${st.label}</span>
                    <span class="mode-icon" style="font-size:9px;opacity:0.85;"></span>
                    <span class="lock-icon" style="display:none;font-size:9px;background:${st.border};color:#fff;padding:0 4px;border-radius:999px;">🔒跟隨中</span>
                </div>
                <div style="
                    width:0;height:0;
                    border-left:5px solid transparent;
                    border-right:5px solid transparent;
                    border-top:6px solid ${st.border};
                    margin-top:-1px;
                "></div>
            `;

            el.addEventListener('pointerdown', ev => {
                ev.stopPropagation();
            });
            el.addEventListener('click', ev => {
                ev.stopPropagation();
                focusCharacter(role);
            });

            markerLayer.appendChild(el);
            charMarkers[role] = el;
        });
    }

    function updateCharacterMarkersPosition() {
        if (!camera || !renderer) return;
        const canvas = renderer.domElement;
        const w = canvas.clientWidth;
        const h = canvas.clientHeight;
        if (!w || !h) return;

        // 為了避免 4 人距離太近時頭頂指標完全重疊，根據角色索引給予微幅水平錯開與高度階層
        const roleOffsets = {
            achun:   { dx: -24, dy: -8 },
            yijhang: { dx: 24,  dy: -8 },
            ayee:    { dx: -26, dy: -28 },
            alu:     { dx: 26,  dy: -28 }
        };

        Object.keys(charMarkers).forEach(role => {
            const el = charMarkers[role];
            const cg = characters[role];
            if (!el || !cg) return;

            const modeSpan = el.querySelector('.mode-icon');
            if (modeSpan) {
                if (cg.userData.isAboard) {
                    modeSpan.textContent = '🚗';
                } else if (!isStoppedAtLandmark && role === stragglerRole) {
                    modeSpan.textContent = '🏃💨';
                } else {
                    modeSpan.textContent = '';
                }
            }

            const pos = new THREE.Vector3();
            cg.getWorldPosition(pos);
            pos.y += cg.userData.isAboard ? 0.90 : 1.05;
            pos.project(camera);

            if (pos.z > 1.0) {
                el.style.display = 'none';
                return;
            }
            el.style.display = 'flex';

            const off = roleOffsets[role] || { dx: 0, dy: 0 };
            const x = (pos.x * 0.5 + 0.5) * w + off.dx;
            const y = (-(pos.y * 0.5) + 0.5) * h + off.dy;

            const clampedX = Math.max(48, Math.min(w - 48, x));
            const clampedY = Math.max(44, Math.min(h - 16, y));

            const isLocked = (lockedRole === role);
            el.style.left = `${clampedX}px`;
            el.style.top = `${clampedY}px`;
            el.style.zIndex = isLocked ? '28' : '22';
            el.style.transform = isLocked ? 'translate(-50%, -100%) scale(1.12)' : 'translate(-50%, -100%) scale(1)';
        });
    }

    // 當鎖定某位角色時，鏡頭中心平滑跟隨該角色移動（同時保留使用者旋轉、縮放視角的自由）
    function updateLockedCameraFollow() {
        if (!lockedRole || !characters[lockedRole] || !controls || !camera) return;
        const targetChar = characters[lockedRole];
        const charWorldPos = new THREE.Vector3();
        targetChar.getWorldPosition(charWorldPos);
        charWorldPos.y += 0.45;

        const deltaMove = new THREE.Vector3().subVectors(charWorldPos, controls.target);
        // 平滑插值跟隨，讓鏡頭同時移動 target 與 camera.position，不打斷使用者的環繞視角距離
        deltaMove.multiplyScalar(0.14);
        controls.target.add(deltaMove);
        camera.position.add(deltaMove);
    }

    function updateLockUI() {
        const roles = ['achun', 'yijhang', 'ayee', 'alu'];
        roles.forEach(r => {
            // 更新頭頂指標上的 🔒 標籤
            const markerEl = charMarkers[r];
            if (markerEl) {
                const lockSpan = markerEl.querySelector('.lock-icon');
                if (lockSpan) {
                    lockSpan.style.display = (lockedRole === r) ? 'inline-block' : 'none';
                }
            }
            // 更新下方角色按鈕鎖定狀態文字與外框高亮
            const cardBtn = document.getElementById(`char-btn-${r}`);
            const statusSpan = document.getElementById(`char-lock-status-${r}`);
            if (statusSpan) {
                statusSpan.textContent = (lockedRole === r) ? '🔒 鎖定跟隨中 (點擊取消)' : '🎯 點擊鎖定鏡頭';
                statusSpan.className = (lockedRole === r)
                    ? 'text-[10px] text-white bg-red-600 px-1.5 py-0.5 rounded-full font-black truncate inline-block mt-0.5'
                    : 'text-[10px] text-stone-500 font-medium truncate block';
            }
            if (cardBtn) {
                if (lockedRole === r) {
                    cardBtn.classList.add('ring-2', 'ring-red-500', 'bg-red-50/90');
                } else {
                    cardBtn.classList.remove('ring-2', 'ring-red-500', 'bg-red-50/90');
                }
            }
        });

        const unlockBtn = document.getElementById('btn-unlock-char');
        const unlockTxt = document.getElementById('unlock-char-text');
        if (unlockBtn) {
            if (lockedRole) {
                unlockBtn.classList.remove('hidden');
                if (unlockTxt) unlockTxt.textContent = `解除鎖定：${ROLE_NAMES[lockedRole]}`;
            } else {
                unlockBtn.classList.add('hidden');
            }
        }
    }

    function onPointerDown(e, routeData) {
        if (!renderer || !camera) return;
        const rect = renderer.domElement.getBoundingClientRect();
        const mouse = new THREE.Vector2(
            ((e.clientX - rect.left) / rect.width) * 2 - 1,
            -((e.clientY - rect.top) / rect.height) * 2 + 1
        );
        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, camera);

        // 1. 優先檢查是否點擊到 4 位家族角色 (點擊角色可切換鎖定/解除鎖定並觸發對話)
        const charMeshes = [];
        Object.values(characters).forEach(cg => {
            cg.traverse(ch => {
                if (ch.isMesh) {
                    ch.userData.parentRole = cg.userData.role;
                    charMeshes.push(ch);
                }
            });
        });
        const hitChar = raycaster.intersectObjects(charMeshes, false);
        if (hitChar.length > 0) {
            const role = hitChar[0].object.userData.parentRole;
            if (role) {
                focusCharacter(role);
                return;
            }
        }

        // 2. 檢查是否點擊到 17 處景點模型 (點擊景點時自動解除人物鎖定，將鏡頭移至該景點)
        if (landmarkState && landmarkState.animatedLandmarks) {
            const lmMeshes = [];
            landmarkState.animatedLandmarks.forEach(lmGroup => {
                lmGroup.traverse(ch => {
                    if (ch.isMesh) {
                        ch.userData.landmarkInfo = lmGroup.userData.landmarkInfo;
                        lmMeshes.push(ch);
                    }
                });
            });
            const hitLm = raycaster.intersectObjects(lmMeshes, false);
            if (hitLm.length > 0 && hitLm[0].object.userData.landmarkInfo) {
                const info = hitLm[0].object.userData.landmarkInfo;
                lockedRole = null;
                updateLockUI();
                currentLandmark = info;
                updateLocationBanner(info);
                controls.target.set(info.x, 0.8, info.z);
                const roles = ['achun', 'yijhang', 'ayee', 'alu'];
                const r = roles[Math.floor(Math.random() * roles.length)];
                triggerCharacterSpeak(r, info.dialogs ? info.dialogs[r] : info.desc);
            }
        }
    }

    // 切換鎖定 / 取消鎖定角色：再次點擊同一位角色即可取消鎖定
    function focusCharacter(role) {
        if (!role || lockedRole === role) {
            lockedRole = null;
            updateLockUI();
            return;
        }
        lockedRole = role;
        // 鎖定跟隨人物時，自動關閉環島自動旋轉以免鏡頭拉扯
        if (isAutoRotate) {
            isAutoRotate = false;
            if (controls) controls.autoRotate = false;
            const txt = document.getElementById('rotate-text');
            if (txt) txt.textContent = '環島旋轉：關';
        }
        const cg = characters[role];
        if (cg && controls && camera) {
            const targetPos = new THREE.Vector3(cg.position.x, (cg.userData.baseY || 0.8) + 0.45, cg.position.z);
            const offset = new THREE.Vector3().subVectors(camera.position, controls.target);
            // 若距離太遠，適度拉近方便觀看角色跟著車隊散步
            if (offset.length() > 16) {
                offset.setLength(13.5);
            }
            controls.target.copy(targetPos);
            camera.position.copy(targetPos).add(offset);
        }
        updateLockUI();
        triggerCharacterSpeak(role);
    }

    function unlockCharacter() {
        lockedRole = null;
        updateLockUI();
    }

    // 切換左鍵/單指操作模式：「旋轉視角」或「拖曳平移畫面」
    function toggleDragPanMode() {
        isDragPanMode = !isDragPanMode;
        if (controls && typeof THREE !== 'undefined' && THREE.MOUSE) {
            controls.mouseButtons.LEFT = isDragPanMode ? THREE.MOUSE.PAN : THREE.MOUSE.ROTATE;
            controls.touches.ONE = isDragPanMode ? THREE.TOUCH.PAN : THREE.TOUCH.ROTATE;
        }
        const txt = document.getElementById('pan-mode-text');
        const btn = document.getElementById('btn-pan-mode');
        if (txt) {
            txt.textContent = isDragPanMode ? '左鍵模式：拖曳平移 ✋' : '左鍵模式：旋轉視角 🔄';
        }
        if (btn) {
            if (isDragPanMode) {
                btn.classList.add('bg-amber-100', 'border-amber-400', 'text-amber-900');
                btn.classList.remove('bg-white/90', 'text-stone-700');
            } else {
                btn.classList.remove('bg-amber-100', 'border-amber-400', 'text-amber-900');
                btn.classList.add('bg-white/90', 'text-stone-700');
            }
        }
    }

    function focusLandmark(landmarkId) {
        if (!landmarkState || !landmarkState.landmarkMap) return;
        const lmGroup = landmarkState.landmarkMap[landmarkId];
        if (lmGroup && lmGroup.userData.landmarkInfo) {
            lockedRole = null;
            updateLockUI();
            const info = lmGroup.userData.landmarkInfo;
            currentLandmark = info;
            updateLocationBanner(info);
            if (controls) {
                controls.target.set(info.x, 0.8, info.z);
            }
            triggerCharacterSpeak('achun', info.dialogs ? info.dialogs.achun : info.desc);
        }
    }

    function cheerEveryone() {
        const roles = ['achun', 'yijhang', 'ayee', 'alu'];
        roles.forEach((r, idx) => {
            setTimeout(() => {
                if (characters[r]) {
                    characters[r].userData.jumping = 1.0;
                    characters[r].userData.quirkType = 1 + (idx % 3);
                    characters[r].userData.quirkDuration = 2.4;
                    characters[r].userData.quirkMaxDur = 2.4;
                }
            }, idx * 110);
        });
        triggerFamilyBanter();
    }

    function toggleAutoRotate() {
        isAutoRotate = !isAutoRotate;
        if (controls) controls.autoRotate = isAutoRotate;
        const txt = document.getElementById('rotate-text');
        if (txt) txt.textContent = `環島旋轉：${isAutoRotate ? '開' : '關'}`;
    }

    function toggleSnow() {
        isSnowEnabled = !isSnowEnabled;
        if (envState && envState.snow) {
            envState.snow.visible = isSnowEnabled;
        }
        const txt = document.getElementById('snow-text');
        if (txt) txt.textContent = `冬日飄雪：${isSnowEnabled ? '開' : '關'}`;
    }

    function onResize(container) {
        if (!container || !camera || !renderer) return;
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
    }

    // 匯出全域控制函式供 HTML 按鈕呼叫
    window.focusCharacter = focusCharacter;
    window.unlockCharacter = unlockCharacter;
    window.toggleDragPanMode = toggleDragPanMode;
    window.focusLandmark = focusLandmark;
    window.cheerEveryone = cheerEveryone;
    window.toggleAutoRotate = toggleAutoRotate;
    window.toggleSnow = toggleSnow;

    window.KyushuIsland.Portal = {
        initPortalIsland,
        focusCharacter,
        unlockCharacter,
        toggleDragPanMode,
        focusLandmark,
        cheerEveryone,
        toggleAutoRotate,
        toggleSnow
    };
})();
