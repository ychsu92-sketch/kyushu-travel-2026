#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python3 "$DIR/build_portal.py"
open "$DIR/index.html"
echo "🚀 已在預設瀏覽器中開啟生活小秘書【家族旅行手帳大廳】！"
