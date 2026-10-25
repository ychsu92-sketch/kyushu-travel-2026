#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo "🔄 正在從 Google 試算表同步最新南九州行程與費用資料..."
python3 "$DIR/sync_from_sheets.py"
open "$DIR/index.html"
echo "🚀 已在預設瀏覽器中開啟生活小秘書【旅行儀表板】！"
