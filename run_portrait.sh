#!/usr/bin/env bash
set -euo pipefail
APP_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

is_wsl=false
if grep -qiE 'microsoft|wsl' /proc/sys/kernel/osrelease 2>/dev/null; then
  is_wsl=true
fi

if ! python3 - <<'PY' >/dev/null 2>&1
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
PY
then
  if [[ "$is_wsl" == true && -t 0 ]]; then
    echo "GTK 3/PyGObjectがありません。PortraitネイティブGUIの依存関係を導入します。"
    sudo apt-get update
    sudo apt-get install -y python3-gi gir1.2-gtk-3.0
  else
    echo "GTK 3/PyGObjectがありません。Ubuntu/WSLでは次を実行してください:" >&2
    echo "  sudo apt update && sudo apt install python3-gi gir1.2-gtk-3.0" >&2
    exit 1
  fi
fi

if [[ "$is_wsl" == true && -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
  cat >&2 <<'MSG'
WSLのGUIディスプレイが見つかりません。GTKでも画面を表示するにはWSLg、またはWSLから接続できるXサーバーが必要です。
Windows PowerShellで `wsl --update` を実行し、続けて `wsl --shutdown` してからWSLを再起動してください。
再起動後に echo $DISPLAY または echo $WAYLAND_DISPLAY で値が設定されているか確認してください。
MSG
  exit 1
fi

gtk_display_check() {
  GDK_BACKEND="$1" python3 - <<'PY' >/dev/null 2>&1
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
result = Gtk.init_check()
ok = result[0] if isinstance(result, tuple) else result
raise SystemExit(0 if ok else 1)
PY
}

if [[ "$is_wsl" == true ]]; then
  connected=false
  preferred="${PORTRAIT_GDK_BACKEND:-x11 wayland}"
  for backend in $preferred; do
    if gtk_display_check "$backend"; then
      export GDK_BACKEND="$backend"
      connected=true
      echo "GTK backend: $GDK_BACKEND"
      break
    fi
  done
  if [[ "$connected" != true ]]; then
    echo "GTK 3がX11/Waylandのどちらにも接続できません。WSLg/XサーバーとDISPLAY/WAYLAND_DISPLAYを確認してください。" >&2
    exit 1
  fi
elif ! gtk_display_check "${GDK_BACKEND:-x11}"; then
  echo "GTK 3が表示サーバーへ接続できません。DISPLAY/WAYLAND_DISPLAYとデスクトップセッションを確認してください。" >&2
  exit 1
fi

exec python3 "$APP_DIR/portrait_gtk.py"
