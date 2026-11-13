#!/usr/bin/env bash
if [ -z "${BASH_VERSION:-}" ]; then
  echo "このスクリプトはBash用です。shではなく、通常ユーザーで bash install.sh を実行してください。" >&2
  exit 2
fi
set -euo pipefail
if (( EUID == 0 )); then
  echo "sudo/rootでは実行しないでください。通常ユーザーで bash install.sh を実行してください。" >&2
  exit 2
fi
SOURCE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DEST_DIR="${HOME}/.local/opt/portrait"
DESKTOP_DIR="${HOME}/.local/share/applications"
BIN_DIR="${HOME}/.local/bin"
mkdir -p "$DEST_DIR" "$DESKTOP_DIR" "$BIN_DIR"
cp "$SOURCE_DIR/portrait_qt.py" "$SOURCE_DIR/run_portrait.sh" "$SOURCE_DIR/README.md" "$DEST_DIR/"
rm -f "$DEST_DIR/portrait.py" "$DEST_DIR/portrait_gtk.py"
cp "$SOURCE_DIR/portrait" "$BIN_DIR/portrait"
chmod +x "$DEST_DIR/portrait_qt.py" "$DEST_DIR/run_portrait.sh"
chmod +x "$BIN_DIR/portrait"
cat > "$DESKTOP_DIR/portrait.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Portrait
Comment=Linux GUI helper for MysticGSI
Exec="$DEST_DIR/run_portrait.sh"
Terminal=false
Categories=Utility;System;
EOF
chmod 644 "$DESKTOP_DIR/portrait.desktop"
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
fi
echo "Portraitをインストールしました: $DEST_DIR"
echo "portraitコマンド: $BIN_DIR/portrait"
echo "アプリ一覧からPortraitを起動するか、portrait --guiでGUIを開けます。"
case ":${PATH}:" in
  *":$BIN_DIR:"*) ;;
  *)
    for profile in "$HOME/.profile" "$HOME/.bashrc"; do
      touch "$profile"
      if ! grep -Fq '# Portrait local-bin PATH' "$profile"; then
        printf '\n# Portrait local-bin PATH\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$profile"
      fi
    done
    echo "新しいシェルを開くか、source ~/.bashrc を実行してPATHを反映してください。"
    ;;
esac
echo "MysticGSIが~/mysticgsi以外の場合は MYSTICGSI_DIR=/path/to/mysticgsi を設定してください。"
