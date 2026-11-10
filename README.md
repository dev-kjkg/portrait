# Portrait

Portraitは、**別途インストールしたMysticGSIをGUIから操作するLinux向けヘルパー**です。MysticGSIのforkではなく、MysticGSI本体やROM処理コードを内蔵しません。GUIからMysticGSI公式の`cli.py`を呼び出します。

GUIはLinuxデスクトップ標準のGTK 3を使うネイティブアプリです。MysticGSI本体は別途インストールしてCLIを呼び出します。

## 対応機能

- `build`と`rebuild`を画面から実行
- `list`でビルド一覧を表示
- `clean`で全ビルドデータを削除（確認ダイアログを表示）
- `--type`、`--add`、`--compress`、`--no-debloat`、`--no-merge`、`--format`、`--avb-key`に対応
- ext4（MysticGSIの既定形式）またはEROFS（lz4 / lz4hc / lzma）を指定
- `auto`または公式CLIの任意の`TYPE[:CUSTOM]`を指定（特定ROM種別に固定しません）
- ROMをファイルピッカーで選択、またはURLを入力。ファイルピッカーは全ファイルを選択可能
- `tmp/`と`out/`をファイルマネージャーで開く
- `out/`から`.img`や`.zip`をホームなどへコピー
- 実行ログと終了コードをGUI上で確認

選択したROMファイルは**移動も複製もしません**。そのファイルの絶対パスをMysticGSIへ渡します。MysticGSIのCLIはローカルの絶対パスを入力にできるため、一時フォルダへの移動や作業後の戻し処理は行いません。ファイル名に空白があっても、引数配列で安全に渡します。

MysticGSIが対応するフルOTA ZIP（`payload.bin`）、fastbootパッケージ、`super.img`やsparseイメージ、`system.new.dat`、Samsung TAR、Huawei `UPDATE.APP`、Unisoc `.pac`、LG `.kdz`、Oppo `.ozip`、QFIL、Sony `.sin`、Pixelファクトリーイメージなどは、公式CLIへそのまま渡します。Portrait側で展開形式を独自に解釈したり変換したりはしません。

## インストール

Ubuntu/Debian系Linuxを想定しています。GTK GUIとCLIラッパーの前提パッケージを用意します。

```sh
sudo apt install python3 python3-gi gir1.2-gtk-3.0 git adb fastboot
```

このフォルダで、**sudoを付けず通常ユーザーのまま**Bashからインストーラーを実行します。`sh install.sh`や`sudo sh install.sh`では実行しないでください。

```sh
bash install.sh
```

Portraitは`~/.local/opt/portrait/`へ配置され、`~/.local/bin/portrait`コマンドとアプリ一覧の「Portrait」が追加されます。ファイルマネージャーから`install.sh`を実行するのではなく、ターミナルから実行してください。WSLなどで`~/.local/bin`がPATHにない場合、インストーラーが`~/.profile`と`~/.bashrc`にPATH設定を追加します。新しいシェルを開くか、`source ~/.bashrc`で反映してください。

## WSL/Linuxのportraitコマンド

インストール後は、MysticGSIのリポジトリに移動しなくても、どのディレクトリからでも公式CLIを呼び出せます。既定では`~/mysticgsi`を実行場所として使います。

```sh
cd ~/Downloads
portrait build klein-v816.0.5.0-vgsmixm \\
  miui_KLEINGlobal_V816.0.5.0.VGSMIXM_96c116ff32_15.0.zip \\
  --type miui --compress
```

相対ファイル名はコマンドを実行したディレクトリ（この例では`~/Downloads`）を基準に絶対パスへ変換してから渡します。ROMファイルを移動する必要はありません。`tmp/`と`out/`はMysticGSIのリポジトリ内に作られます。HTTP/HTTPS URLはそのまま公式CLIへ渡します。

主なサブコマンド：

```sh
portrait build <name> <firmware|URL> [公式CLIのオプション]
portrait rebuild <name> [--compress] [--avb-key /path/to/key.pem]
portrait list
portrait clean
portrait version
portrait --gui
portrait uninstall [--purge]
```

`portrait version`はPortraitのロゴとバージョンを表示します。`portrait --gui`はGTK 3版GUIを起動します。GUI起動後にCtrl+Cを押すとプロセスが中断されます。WSLでGUIを使うにはWSLg、またはXサーバーが必要です。GTK 3/PyGObjectが未導入の場合、WSLから起動したランチャーは今開いている端末で依存パッケージを導入します。WSLgではX11 backendを先に試し、接続できない場合にWayland backendを試します。

WSLgを使う場合は、`portrait --gui`を実行した後にエラーが出たら、まず次を確認してください。

```sh
python3 -c 'import gi; gi.require_version("Gtk", "3.0"); from gi.repository import Gtk; print(Gtk.init_check())'
echo "$DISPLAY"
echo "$WAYLAND_DISPLAY"
```

GTK importに失敗する場合は`sudo apt update && sudo apt install python3-gi gir1.2-gtk-3.0`を実行します。WSL2のWSLg環境で`DISPLAY`と`WAYLAND_DISPLAY`の両方が空なら、Windows PowerShellで`wsl --update`、次に`wsl --shutdown`を実行してからWSLを再起動してください。WSL1やWSLgを使わない構成では、Windows側のXサーバーと正しい`DISPLAY`設定が必要です。GTKはLinuxネイティブのGUIですが、WSLの表示サーバー自体が使えない場合はウィンドウを表示できません。

backendを手動で指定するには、`PORTRAIT_GDK_BACKEND=x11 portrait --gui`または`PORTRAIT_GDK_BACKEND=wayland portrait --gui`を使います。

Portraitを削除する場合は、次を実行して確認プロンプトで`yes`を入力します。

```sh
portrait uninstall
```

これはPortrait本体、コマンド、デスクトップ項目、Portraitが追加したPATH行を削除します。MysticGSI、ROM、`tmp/`、`out/`、GTK 3/PyGObjectは削除しません。Portrait設定も削除する場合は`portrait uninstall --purge`を使います。

MysticGSIが既定の`~/mysticgsi`以外にある場合は、環境変数を設定します。

```sh
export MYSTICGSI_DIR="$HOME/projects/mysticgsi"
portrait list
```

GUIから指定した作業フォルダは設定ファイルにも保存されます。CLIで確実に指定する場合は`MYSTICGSI_DIR`を使ってください。

## 初回起動

アプリ起動時、既定の`~/mysticgsi`に`cli.py`がある場合は既存インストール済みとして認識し、セットアップを行いません。別の場所へインストールした場合は「MysticGSI作業フォルダ」でその場所を選びます。

まだインストールされていない場合、初回確認ダイアログが表示されます。「いいえ」を選ぶと、確認のうえ、別ターミナルで次のセットアップを開始します。

```sh
sudo apt install -y python3 git adb fastboot python3-gi gir1.2-gtk-3.0
git clone https://github.com/MysticGSI/mysticgsi.git ~/mysticgsi
cd ~/mysticgsi
./setup_host.py
```

実装では選択したMysticGSIフォルダへcloneします。`setup_host.py`は公式手順どおりに追加のシステム依存関係と`.venv`を設定します。sudo認証を安全に入力できるよう、初期化処理は画面内ではなくターミナルで行います。**既にインストール済み**を選ぶと初期セットアップはスキップされます。

クローン先が既に存在してMysticGSIの`cli.py`もある場合、「セットアップ…」は既存フォルダで`./setup_host.py`を再実行します。既存の無関係なフォルダを指定してはいけません。

## 使い方

1. 「MysticGSI作業フォルダ」に、`cli.py`があるリポジトリのルートを指定します。
2. 「ビルド」タブで`build`または`rebuild`を選びます。
3. ビルド名を入力します。`build`の場合はROMのZIP/イメージファイルを選択するか、直接URLを入力します。
4. 必要に応じて`--type`欄へ`auto`または公式CLIの`TYPE[:CUSTOM]`を入力し、圧縮、パーティション統合、debloat、タグ、署名鍵、画像形式を選びます。
5. 「Portraitで実行」を押し、ログと終了コードを確認します。

ext4はMysticGSIの既定形式なので`--format`を付けません。EROFSを選択すると、公式CLIの`--format lz4`、`--format lz4hc`または`--format lzma`を付けます。EROFSで起動するには書き込み先端末のカーネルとfstabが対応している必要があります。

コマンド対応は公式README記載の範囲です。`build`は`--type`、`--format`、`--compress`、`--add`、`--no-debloat`、`--no-merge`、`--avb-key`に対応します。`rebuild`は`--compress`と`--avb-key`に対応します。`list`と`clean`も管理タブから実行できます。`--type`は固定候補のプルダウンではなく自由入力欄なので、公式CLIで使う種別名を指定できます。

アプリは`.venv/bin/python`があればそれを使います。セットアップ前でもシステムの`python3`でCLIを起動しますが、必要な依存関係がなければ実行エラーになります。

## クリーンアップと成果物

`list`はMysticGSI公式CLIのビルド一覧を表示します。`tmpを開く`と`outを開く`で各フォルダをファイルマネージャーで開けます。「出力ファイルをコピー…」は`out/`内の`.img`や`.zip`を選び、保存先へコピーします。元の成果物は残ります。

MysticGSIの公式`clean`は**特定ビルドだけでなく、作業フォルダ内の`tmp/`と`out/`を全削除**します。Portraitは実行前に対象パスを明示して確認します。特定のビルドのみ消す意図でこのボタンを使わないでください。

## 手動起動

```sh
python3 portrait_gtk.py
```

インストールせず起動する場合は、実行フォルダにある`run_portrait.sh`を使います。GTK依存関係を確認し、WSLでは現在の端末から不足パッケージを導入します。

## 注意

- PortraitはROMの互換性やビルド成功を保証しません。
- GSIを実機へ書き込む操作は行いません。ROM書き込みは別手順です。
- `clean`は不可逆な削除です。必要な成果物は事前にコピーしてください。
- 元ROMや生成物の利用条件は利用者が確認してください。
