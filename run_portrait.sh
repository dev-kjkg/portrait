#!/usr/bin/env bash
set -euo pipefail
APP_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

is_wsl=false
if grep -qiE 'microsoft|wsl' /proc/sys/kernel/osrelease 2>/dev/null; then
  is_wsl=true
fi

if ! python3 -c 'from PyQt5.QtWidgets import QApplication, QWidget' >/dev/null 2>&1; then
  if [[ "$is_wsl" == true && -t 0 ]]; then
    echo "PyQt5/Qt Widgetsがありません。Portrait Linux GUIの依存関係を導入します。"
    sudo apt-get update
    sudo apt-get install -y python3-pyqt5
  else
    echo "PyQt5/Qt Widgetsがありません。Ubuntu/WSLでは次を実行してください:" >&2
    echo "  sudo apt update && sudo apt install python3-pyqt5" >&2
    exit 1
  fi
fi

if [[ "$is_wsl" == true ]]; then
  export QT_QPA_PLATFORM="${PORTRAIT_QT_PLATFORM:-xcb}"
  export LIBGL_ALWAYS_SOFTWARE=1
  if [[ -z "${DISPLAY:-}" ]]; then
    echo "DISPLAYが空です。WSLgまたはXサーバーを起動し、DISPLAYを設定してください。" >&2
    exit 1
  fi
fi

exec python3 "$APP_DIR/portrait_qt.py"
