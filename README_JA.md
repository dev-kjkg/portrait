# Portrait（日本語版完全解説）

<div align="center">

```
⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠙⢷⣤⣤⣴⣶⣶⣦⣤⣤⡾⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣿⣿⣉⣹⣿⣿⣿⣿⣏⣉⣿⣿⣧⠀⠀⠀⠀
⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀
⣠⣄⠀⢠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⡄⠀⣠⣄
⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿
⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿
⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿
⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿
⠻⠟⠁⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠈⠻⠟
⠀⠀⠀⠀⠉⠉⣿⣿⣿⡏⠉⠉⢹⣿⣿⣿⠉⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀
```

### [MysticGSI](https://github.com/MysticGSI/mysticgsi) 公式CLIをGUIからワンクリック操作できる、Linux / WSL向けネイティブフロントエンド

[![License](https://img.shields.io/badge/License-Apache--2.0%20%2F%20MIT-blue.svg)](#ライセンス--クレジット)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%2F%20WSL2-green.svg)](#wsl--wslg環境での利用)
[![GUI](https://img.shields.io/badge/GUI-PyQt5%20%2F%20Qt%20Widgets-brightgreen.svg)](#インストール)
[![MysticGSI](https://img.shields.io/badge/MysticGSI-v2.0%2B-orange.svg)](https://github.com/MysticGSI/mysticgsi)
[![Version](https://img.shields.io/badge/Portrait-v1.2.0-purple.svg)](#バージョン確認)

[English README](README.md) · [Issue Tracker](https://github.com/dev-kjkg/portrait/issues) · [Discussions](https://github.com/dev-kjkg/portrait/discussions)

</div>

---

## 目次

1. [Portraitとは](#portraitとは)
2. [設計思想とアーキテクチャ](#設計思想とアーキテクチャ)
3. [MysticGSIエコシステム（GSIとは何か）](#mysticgsiエコシステムgsiとは何か)
4. [機能一覧](#機能一覧)
5. [インストール](#インストール)
   - [前提環境](#前提環境)
   - [ワンライン導入（最速）](#ワンライン導入最速)
   - [段階ごとの詳しい導入手順](#段階ごとの詳しい導入手順)
   - [導入後の配置](#導入後の配置)
   - [バージョン確認](#バージョン確認)
6. [MysticGSI本体のセットアップ（必須前提）](#mysticgsi本体のセットアップ必須前提)
7. [GUI操作完全ガイド](#gui操作完全ガイド)
   - [初回起動と作業フォルダの指定](#初回起動と作業フォルダの指定)
   - [「ビルド」タブ 項目リファレンス](#ビルドタブ-項目リファレンス)
   - [「管理・出力」タブ](#管理出力タブ)
   - [リアルタイム実行ログの見方](#リアルタイム実行ログの見方)
8. [CLIリファレンス（portraitコマンド）](#cliリファレンスportraitコマンド)
9. [対応ROM種別と対応ファームウェア形式](#対応rom種別と対応ファームウェア形式)
10. [WSL / WSLg環境での利用](#wsl--wslg環境での利用)
11. [実機フラッシュ＆デバイス側の注意点（Androidマニア向け）](#実機フラッシュデバイス側の注意点androidマニア向け)
12. [設定と環境変数](#設定と環境変数)
13. [トラブルシューティング＆よくある質問](#トラブルシューティングよくある質問)
14. [アンインストール](#アンインストール)
15. [開発・コントリビュート](#開発コントリビュート)
16. [ライセンス / クレジット](#ライセンス--クレジット)

---

## Portraitとは

**Portrait**は、Android stockファームウェアからProject Treble互換の**Generic System Image (GSI)**を生成するツール「[MysticGSI](https://github.com/MysticGSI/mysticgsi)」を、GUI（PyQt5 / Qt Widgets）から操作できるようにするLinux / WSL向けネイティブフロントエンドです。

通常、MysticGSIでGSIをビルドするには仮想環境内で公式`cli.py`に`--type`、`--format`、`--avb-key`、`--compress`などのフラグを手動で指定する必要があります。Portraitはこれらを直感的な2タブUIに集約し、**MysticGSI本体に手を加える（forkする）ことなく**、公式CLIの全機能を画面上から引き出します。

### 特長

- **GUIで完結するGSIビルド**: ROMファイルをファイルピッカーで選ぶかURLを貼り、フラグを選んで「Portraitで実行」を押すだけ
- **ROMファイルのゼロコピー安全設計**: 選択したROMをコピー・移動しません。解決した絶対パスを配列で渡すため、スペース入りパスや特殊文字でも安全
- **GUI内にsudoを持ち込まない**: パッケージ導入やMysticGSIセットアップなど管理者権限が必要な処理はGUI内で実行せず、自分のターミナルへ貼る正確なコマンドを提示
- **CLIラッパーも同時提供**: `portrait build ...`コマンドで、どのディレクトリからでも相対パスのまま実行可能（相対パスは自動で絶対パスに解決）
- **WSL / WSLg完全対応**: WSL2環境を自動検出し、`xcb`プラットフォーム・ソフトウェア描画・Display設定を自動調整

> **重要**: PortraitはMysticGSIの**forkではありません**。ROM展開やパッチ処理の独自コードは持たず、GUIからMysticGSI公式の`cli.py`を`QProcess`で安全に呼び出します。ROM互換性・パッチ品質・ビルド成否はMysticGSI本体側に依存します。

---

## 設計思想とアーキテクチャ

```
  ┌─────────────────────────────────────────────────────────────┐
  │                         User Layer                          │
  │     [Portrait Qt Widgets GUI]       [portrait CLIラッパー]  │
  │     (portrait_qt.py)                (bash launcher)         │
  └──────────────────────────┬──────────────────────────────────┘
                             │  QProcess / exec
                             ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                 MysticGSI（公式・改変なし）                 │
  │    ~/mysticgsi/cli.py  ◄── .venv/bin/python で実行          │
  │         │                                                   │
  │         ├─► extract_firmware (aria2c / 7z / libarchive / …)  │
  │         ├─► unpack_partitions (simg2img / lpunpack / …)     │
  │         ├─► パッチパイプライン (SELinux / Treble / vendors) │
  │         ├─► イメージ生成 (mke2fs / mkfs.erofs)              │
  │         ├─► AVB 2.0 署名 (avbtool RSA)                      │
  │         └─► 圧縮 (.zip)                                     │
  │                                                             │
  │    tmp/<build>/                out/<build>/                 │
  │    ├── images/ (生ツリー)      ├── <name>.img               │
  │    ├── payload展開             ├── <name>.zip               │
  │    └── gsilist.json            └── output.txt (ビルド情報)  │
  └─────────────────────────────────────────────────────────────┘
```

| 設計方針 | Portraitでの実装 |
|---|---|
| **非侵襲** | MysticGSIのソースを一切変更せず、公式`cli.py`引数とファイル経由のみで連携 |
| **ゼロコピー** | ROMファイルは`os.path.realpath`で解決した絶対パスで参照（6GB超のROMでも移動・複製なし） |
| **権限分離** | GUI内で`sudo`を実行しない。セットアップはターミナル用コマンドとして提示 |
| **同時実行保護** | GUIが多重起動をブロック＋MysticGSI自身の`buildlock.py`排他制御 |
| **可搬性** | `$MYSTICGSI_DIR` / XDG標準設定ファイル / 標準PATH規則を尊重 |

---

## MysticGSIエコシステム（GSIとは何か）

**Project Treble**（Android 8.0以降）によって、OS本体（`system`）と端末固有ドライバ（`vendor`）が分離されました。**GSI（Generic System Image）**は共通仕様で作られたシステムイメージで、OEMのvendorを保持したままOS部分だけを差し替えられます。例えばOnePlus端末上でHyperOSを、Xiaomi端末上でOne UIを動かすことが可能です。

[MysticGSI](https://github.com/MysticGSI/mysticgsi)はPython 3.10+で書かれたAOSP/OEM stock ROM → GSI移植ツールです。OEMファームウェアを展開し、**SELinuxポリシー調整、Treble互換性パッチ、apex設定、USBデバッグ強制有効化、AB更新関連ファイルの除去**などの深いパッチパイプラインを通した後、filesystemイメージを再生成しAVB 2.0署名まで行います。Portraitはその公式GUIフロントエンドです。

### 対応Androidバージョン

MysticGSIは**Android 10 (API 29) 〜 Android 16+ (API 37 / Baklava / CinnamonBun / CANARY)**までのバージョン別パッチツリーを同梱しています。移植元ROMがこのバージョンのいずれかに基づいていれば処理可能です。

---

## 機能一覧

| 機能 | CLI (`portrait`) | GUI (`portrait --gui`) | MysticGSI公式 |
|---|:---:|:---:|:---:|
| `build` — 新規GSIビルド | ✔ | ✔ | ✔ |
| `rebuild` — 編集済み`tmp/<name>/images`から再生成 | ✔ | ✔ | ✔ |
| `list` — 記録済みビルド一覧 (`gsilist.json`) | ✔ | ✔ | ✔ |
| `clean` — 全`tmp/`＋`out/`削除（確認ダイアログ付き） | ✔ | ✔ | ✔ |
| `--type TYPE[:CUSTOM]` — ROM種別の指定 | ✔ | ✔ | ✔ |
| ext4 vs EROFS（`lz4` / `lz4hc` / `lzma`） | ✔ | ✔ | ✔ |
| `--compress` — ZIP出力（既定ON） | ✔ | ✔ | ✔ |
| `--no-debloat` — OEMアプリの維持 | ✔ | ✔ | ✔ |
| `--no-merge` — 個別パーティション出力 | ✔ | ✔ | ✔ |
| `--avb-key <PEM>` — 独自署名鍵 | ✔ | ✔ | ✔ |
| `--add <tag>` — ビルド名へのタグ追加 | ✔ | ✔ | ✔ |
| ローカルROMファイルピッカー | — | ✔ | — |
| HTTP/HTTPS ROM URL（aria2c高速DL） | ✔ | ✔ | ✔ |
| 相対パスの自動絶対パス解決（ファイル移動不要） | ✔ | ✔ | — |
| リアルタイム統合ログ表示（stdout/stderr統合） | — | ✔ | — |
| `tmp/` / `out/` をファイルマネージャーで開く | — | ✔ | — |
| 成果物（.img/.zip）を別先へ安全コピー | — | ✔ | — |
| リポジトリ位置の永続保存 | ✔ | ✔ | — |
| アスキーアートロゴ＆バージョン表示 | ✔ | — | — |
| WSL / WSLg自動検出＆描画最適化 | ✔ | ✔ | — |
| デスクトップアプリ登録＆クリーンアンインストーラー | ✔ | — | — |

---

## インストール

### 前提環境

| 項目 | 要件 | 備考 |
|---|---|---|
| OS | Ubuntu 22.04 / 24.04（ネイティブまたはWSL2）、Debian 12 等 | openSUSE/Arch/FedoraもMysticGSI可能。PortraitインストーラーはDebian/Ubuntu系向け |
| Python | 3.10以上 | Ubuntu 22.04+は標準同梱 |
| シェル | bash（shは不可） | インストーラーが`$BASH_VERSION`を明示検証 |
| 実行権限 | **通常ユーザー** | `sudo`や`sh install.sh`では実行しないでください |

### ワンライン導入（最速）

```bash
git clone https://github.com/dev-kjkg/portrait.git && bash portrait/install.sh && hash -r && sudo apt update && sudo apt install -y python3-pyqt5 && portrait --gui
```

### 段階ごとの詳しい導入手順

```bash
# 1. Portraitリポジトリをclone
git clone https://github.com/dev-kjkg/portrait.git

# 2. インストーラーを【通常ユーザーのままbashで】実行（shやsudo shは禁止）
cd portrait
bash install.sh

# 3. bashのコマンドハッシュテーブルをリフレッシュ
hash -r

# 4. aptインデックスを更新
sudo apt update

# 5. PortraitのUI基盤であるPyQt5（Qt Widgets）を導入
sudo apt install python3-pyqt5

# 6. GUIを起動
portrait --gui
```

#### 各ステップの技術的根拠

- **`bash install.sh`**: スクリプト冒頭で`BASH_VERSION`と`EUID != 0`を検証しており、`sh`や`sudo`での実行は即座に弾かれます。通常ユーザーで実行するのが仕様です。
- **`hash -r`**: `install.sh`が`~/.local/bin`にバイナリを配置します。ログイン時に同ディレクトリが存在しなかったシェルはコマンド位置をハッシュテーブルにキャッシュしているため、`hash -r`でキャッシュをクリアして新コマンドを**現在開いているターミナルで即座に**認識させます。それでも認識されない場合は`source ~/.bashrc`を一度実行してください。
- **PyQt5を別コマンドで入れる理由**: `install.sh`は監査可能・安全であることを重視し、**内部でsudoを一切呼ばない**設計です。GUI依存関係は明示的にユーザー自身が`sudo apt`で導入します。

### 導入後の配置

```
~/.local/
├── bin/
│   └── portrait                    # メインCLIラッパー（実行権限付き）
├── opt/
│   └── portrait/
│       ├── portrait_qt.py          # PyQt5ネイティブGUIアプリ本体
│       ├── run_portrait.sh         # WSL対応起動スクリプト（依存チェック含む）
│       └── README.md               # 同梱ドキュメント
└── share/
    └── applications/
        └── portrait.desktop        # アプリ一覧登録（「Portrait」）

~/.config/portrait/
└── settings.json                   # MysticGSIリポジトリ位置の保存先
```

PATH連携: `install.sh`は`~/.profile`と`~/.bashrc`へ`# Portrait local-bin PATH`マーカー付きで`export PATH="$HOME/.local/bin:$PATH"`を追記します。重複追加はされず、アンインストーラーが綺麗に除去できます。

### バージョン確認

```bash
portrait version
```

PortraitのAndroidロボット風アスキーアートと下記が表示されれば導入成功です：

```
Portrait CLI 1.2.0 — MysticGSI helper
```

```bash
# Qt Widgetsが正常に使えるかの確認
python3 -c 'from PyQt5.QtCore import QT_VERSION_STR; from PyQt5.QtWidgets import QApplication; print("Qt:", QT_VERSION_STR)'
```

---

## MysticGSI本体のセットアップ（必須前提）

PortraitはMysticGSIのフロントエンドであるため、**MysticGSI本体が別途必要**です。既定の場所は**`~/mysticgsi`**です。

```bash
# 1. cloneとデバイス通信に必要な最小ツール
sudo apt update && sudo apt install -y python3 git adb fastboot

# 2. MysticGSIをホームへclone
git clone https://github.com/MysticGSI/mysticgsi.git ~/mysticgsi

# 3. 公式のホスト環境セットアップを実行
cd ~/mysticgsi && ./setup_host.py
```

`setup_host.py`がDebian/Ubuntu向けに不足パッケージ（**curl, aria2, openssl, patch, ca-certificates, libarchive-tools, default-jre-headless** 等）を自動導入し、CLIが使う`.venv`仮想環境を作成します。※Javaは同梱Apktoolの実行に必須です。

GUI右上の**「セットアップ手順」**ボタンを押せば、いつでも上記コマンドをポップアップで確認・コピーできます。

---

## GUI操作完全ガイド

起動コマンド：

```bash
portrait --gui
```

### 初回起動と作業フォルダの指定

起動時、Portraitは下記順でMysticGSIを探します：

1. 環境変数 `$MYSTICGSI_DIR`
2. `~/.config/portrait/settings.json`（前回の保存値）
3. `~/mysticgsi`（既定値）

見つからない場合は「選択…」から`cli.py`があるフォルダを指定してください。指定値は`~/.config/portrait/settings.json`へ自動保存されます。

### 「ビルド」タブ 項目リファレンス

| 項目 | 説明 | 公式CLI対応 |
|---|---|---|
| **コマンド** | `build`（新規移植）または `rebuild`（`tmp/<name>/images`編集後の再生成） | `build` / `rebuild` |
| **ビルド名** | 内部識別名。英数字・ドット・ハイフン・アンダースコア最大64文字 | `<name>` 引数 |
| **ROMファイル / URL** | ファイルピッカーで全形式選択可、またはHTTP/HTTPSの直リンク | `<source>` 引数 |
| **ROM種別 (`--type`)** | 既定値`auto`。公式ベンダー名、または`TYPE:CUSTOMNAME`（例: `pixel:custom`） | `--type <type>` |
| **出力形式** | `ext4`（既定）、`EROFS / lz4`、`EROFS / lz4hc`、`EROFS / lzma` | `--format <comp>` |
| **--compress** | `<partition>.img`入りZIPも同時出力（既定ON） | `--compress` |
| **--no-debloat** | パッチセットが通常除去するOEMアプリを維持（詳細は下記） | `--no-debloat` |
| **--no-merge** | パーティションを`system`へ統合せず個別イメージ出力 | `--no-merge` |
| **--add タグ** | ビルド表示名に付加する任意タグ | `--add <tag>` |
| **AVB秘密鍵** | 独自署名用のRSA PEM秘密鍵ファイル（`*.pem`フィルタ） | `--avb-key <pem>` |

#### 出力ファイル名規則

生成されるイメージは下記形式で`out/<ビルド名>/`に出力されます：

```
<ROM種別名>-<デバイスコードネーム>-<Androidバージョン>-<ビルド番号>-AB-<YYYYMMDD>-MysticGSI.img
```

ビルド名には`hyperos-12tpro`のような識別しやすい名前を推奨します。

#### `--no-debloat`フラグの意味（中級者向け）

MysticGSIのパッチパイプラインは、一部のROMで`surfaceflinger`をクラッシュさせる**Dolphin**ライブラリ（`libdolphin.so`）、**Dirac**音響サービス、Qualcommの位置情報アプリを無条件で除去します。`--no-debloat`を付けると、これら以外のOEMアプリ群が維持されます。OEM独自機能が必須な場合や、除去起因のブートループを疑う際に活用してください。

#### `--no-merge`フラグの意味（動的パーティション関連）

近年のOEM ROMはUIやOEMアプリを`system_ext`、`product`、`my_bigball`、`mi_ext`等へ分散配置しています。既定ではMysticGSIがこれらを単一の`system`イメージに統合して古い機種でも`fastboot flash system`一発で動くようにします。`--no-merge`を選ぶと`*-system.img`、`*-product.img`等が個別出力され、動的パーティションを持つ最新端末の純正レイアウトに近い状態で移植できます。

#### 出力形式：ext4 vs EROFS

| 形式 | 長所 | 注意点 |
|---|---|---|
| **ext4**（既定） | ほぼ全端末で起動可能 | イメージサイズは最大 |
| **EROFS / lz4** | 30〜50%小型、超高速展開 | 端末側カーネルのEROFS対応が必須 |
| **EROFS / lz4hc** | lz4より高圧縮 | 生成がやや遅い |
| **EROFS / lzma** | 最小イメージ | `CONFIG_EROFS_FS_ZIP_LZMA`がカーネルに必要 |

> **必須要件**: EROFSを使う場合、端末側のカーネルがEROFSをサポートし、vendorの`fstab`が`erofs`指定でマウントしている必要があります。端末上で `cat /proc/filesystems | grep erofs`（root）で確認できます。

#### AVB署名

既定では**AOSPのAVB RSA-2048テスト鍵**で署名されます。`vbmeta`検証をバイパスして独自鍵で統一運用したい場合は、**AVB秘密鍵**欄に自前の`key.pem`を指定してください。

### 「管理・出力」タブ

| ボタン | 動作 |
|---|---|
| **ビルド一覧（list）** | `tmp/gsilist.json`の履歴を一覧表示（削除済みイメージは`(missing)`表示） |
| **tmpを開く** | `tmp/`をファイルマネージャーで開く |
| **outを開く** | `out/`をファイルマネージャーで開く |
| **出力ファイルをコピー…** | `out/`内の`.img`/`.zip`を選び、**元を残したまま**任意先へ複製 |
| **全tmp/outを削除（clean）…** | 削除対象パスを明示した確認ダイアログ後に公式`clean`を実行 |

> ⚠️ **`clean`は完全削除です**: 単一ビルドだけでなく、MysticGSI作業フォルダ直下の**`tmp/`と`out/`の全エントリ**を一括削除します。特定ビルドだけ消したい場合はフォルダを個別に手動削除してください。

### リアルタイム実行ログの見方

等幅フォントのログ欄へ、パーセント進捗・ステージ名・展開・パッチ・イメージ生成・署名の全ログがリアルタイムに流れます（最大3,000ブロック、stdout/stderr統合）。ステージ順序：

1. `extract` — 最適な展開ツールによるファームウェア解凍
2. `unpack` — 各パーティションイメージの展開（`simg2img`、`lpunpack`等）
3. `patch` — ベンダー判定、SELinuxポリシー整理、Treble互換化、フレームワークフック
4. `prepare` — 動的パーティションの統合（または分離維持）
5. `mke2fs` / mkfs.erofs — 最終イメージ生成
6. `sign` — AVB RSA署名
7. `done` — サマリー表示、`tmp/gsilist.json`へ記録

ステータスバーと行末に終了コードが表示されます（`0`で成功）。

---

## CLIリファレンス（portraitコマンド）

`~/.local/bin/portrait`はMysticGSI公式CLIと完全互換のオプションをそのまま通しつつ、**どのディレクトリから実行しても相対パスを絶対パスへ自動変換する**安全性向上レイヤーとして機能します。

```
portrait build <name> <firmware|URL> [公式CLIのオプション...]
portrait rebuild <name> [--compress] [--avb-key <pem>]
portrait list
portrait clean
portrait --gui
portrait version
portrait uninstall [--purge]
```

### 使用例

**MIUIファストブートZIPからローカルビルド（ZIP移動不要）：**

```bash
cd ~/Downloads
portrait build miui-note13 \
  miui_KLEINGlobal_V816.0.5.0.VGSMIXM_96c116ff32_15.0.zip \
  --type miui --compress
```

**HTTPの直URLからaria2c高速ダウンロード併用ビルド：**

```bash
portrait build raven \
  https://dl.google.com/dl/android/aosp/raven-up1a.231105.003-factory-76a795d5.zip \
  --type pixel --compress
```

**`tmp/mybuild/images`を手動編集後の再生成：**

```bash
# systemツリーを手で微修正した後に実行
portrait rebuild mybuild --compress
```

**独自AVB鍵＋EROFS構成：**

```bash
portrait build hyperos-tpro ~/firmware/os.zip \
  --type hyperos --format lz4 \
  --avb-key ~/.keys/my_avb.pem --compress
```

**既定外のMysticGSIフォルダを使う：**

```bash
export MYSTICGSI_DIR="$HOME/projects/mysticgsi"
portrait list
```

---

## 対応ROM種別と対応ファームウェア形式

### `--type`で指定可能なベンダー一覧

MysticGSI本体のベンダーフック定義（`tools/porting/vendors/__init__.py`）に基づく一覧です。通常は**`auto`**（既定）で自動判定されますが、誤判定時は明示指定できます：

| `--type` 値 | ベンダー / ROM | 判定に使う主なプロパティ |
|---|---|---|
| `pixel` | Google Pixel | factory image構造 |
| `alos` | AOSP / ALOS 汎用ベース | 参照実装 |
| `miui` | Xiaomi MIUI 12–14 | `ro.miui.ui.version.name` |
| `hyperos` | Xiaomi HyperOS 1.x–2.x+ | `ro.mi.os.version.incremental`, `mi_ext` |
| `joyui` | Black Shark JOYUI | Xiaomi系ゲーミングROM |
| `oneui` | Samsung One UI | `ro.build.version.oneui` |
| `coloros` | OPPO ColorOS | `ro.build.version.oplusrom`（oppoブランド） |
| `oxygenos` | OnePlus OxygenOS | `ro.build.version.oplusrom`（oneplusブランド） |
| `realmeui` | Realme Realme UI | `ro.build.version.oplusrom`（realmeブランド） |
| `emui` | Huawei EMUI | `UPDATE.APP` |
| `magicos` | Honor MagicOS | `product_h`＋`hw_product`の`local.prop` |
| `harmonyos` | Huawei HarmonyOS | Huaweiプロパティ群 |
| `zui` | Lenovo ZUI | Lenovo端末 |
| `nothing` | Nothing OS | `ro.nothing.version.id`（`update_engine`温存） |
| `myos` | ZTE MyOS | ZTE端末 |
| `redmagic` | Nubia RedMagic OS | ゲーミングZTE端末 |
| `nebulaos` | ZTE NebulaOS | ZTEミドル端末 |
| `auto` | 自動判定（既定） | 上記プロパティを順に走査 |

**自動検出されるカスタムROM**: LineageOS（`ro.lineage.build.version`）、Evolution X、crDroid、Pixel Experience、Project Blaze、RisingOS、VoltageOS。

**カスタム命名構文**: `pixel:custom`（または`TYPE:CUSTOMNAME`）で、ベンダーフックを維持しつつビルド表示名のバリアントタグを独自名に変更可能。

### 対応ファームウェア形式

- **フルOTA ZIP**（`payload.bin`内包）… Pixel、OnePlus、Nothing、Xiaomi、Motorola等
- **fastboot ROMパッケージ**（Xiaomi `.tgz` 等）
- **`super.img`** および **sparseイメージ**（内部で`simg2img`自動変換）
- **`system.new.dat` / `system.new.dat.br`**（旧世代OTA）
- **Samsung `.tar` / `.tar.md5`**
- **Huawei `UPDATE.APP`**
- **Unisoc `.pac`**（Spreadtrum SoC端末）
- **LG `.kdz`**
- **OPPO `.ozip`**（暗号化ROM）
- **QFILパッケージ**（Qualcomm EDL書き込み用ROM）
- **Sony `.sin`**
- **Pixel factoryイメージ**（`image-*.zip`）

### 内包パーティションのファイルシステム

**ext4 / EROFS / F2FS** のいずれにも対応。

---

## WSL / WSLg Guide

PortraitはWSL2（Ubuntu）を第一級プラットフォームとして扱います。ランチャーはWSL環境を`/proc/sys/kernel/osrelease`や`WSL_DISTRO_NAME`で自動検出し、以下を自動適用します：

```bash
export QT_QPA_PLATFORM="${PORTRAIT_QT_PLATFORM:-xcb}"
export LIBGL_ALWAYS_SOFTWARE=1
export QT_X11_NO_MITSHM=1
export DISPLAY="${DISPLAY:-:0}"
```

### WSLg動作確認チェックリスト

```bash
# 1. Qtが正常にimportできるか
python3 -c 'from PyQt5.QtCore import QT_VERSION_STR; from PyQt5.QtWidgets import QApplication; print("PyQt/Qt:", QT_VERSION_STR)'

# 2. ディスプレイ環境変数
echo "DISPLAY=$DISPLAY"
echo "WAYLAND_DISPLAY=$WAYLAND_DISPLAY"
```

`DISPLAY`が空の場合、**Windows側PowerShell**からWSLを更新・再起動してください：

```powershell
wsl --update
wsl --shutdown
```

Ubuntuを開き直して `portrait --gui` を再実行します。

### WSL1 / 外部Xサーバー併用時

VcXsrvなどの外部Xサーバーを使う場合、ホスト側IPへDISPLAYを向け（`export DISPLAY=$(ip route show default | awk '{print $3}'):0`）、Xサーバーのアクセス制御を無効化（`-ac`）してください。

---

## 実機フラッシュ＆デバイス側の注意点（Androidマニア向け）

> **免責**: Portraitは**ビルド専用**ツールです。端末への書き込みは一切行いません。第三者製イメージのフラッシュは端末の文鎮化・保証失効・Knoxトリップのリスクを伴います。必ず stockの boot / vendor / recovery パーティションをバックアップした上で作業してください。

### 基本のfastbootd書き込み手順（動的パーティション機、Android 10+）

```bash
# 1. fastbootdへ再起動（bootloaderではなくfastbootd！）
adb reboot fastboot

# 2. AVB検証を無効化（必要な機種のみ）
fastboot flash vbmeta --disable-verity --disable-verification /path/to/stock/vbmeta.img

# 3. GSIの書き込み
fastboot flash system /path/to/out/<name>/<output>.img

# 4. 初回起動時は必須のファクトリーリセット
fastboot -w

# 5. 再起動
fastboot reboot
```

### 焼き込み前チェックリスト

| 項目 | 理由 |
|---|---|
| Treble対応 | `adb shell getprop ro.treble.enabled` → `true` |
| 32bit非対応機の罠 | Portraitビルドサマリーで「Warning: this image needs a device with 32-bit support」が出た場合、64bit専用Soc（Pixel 7以降等）では一部コンポーネントが動かない |
| 新ARM命令の警告 | MysticGSIが`init`/`linker64`/`surfaceflinger`をスキャンし検出した新ARM命令を警告表示。古いarm64-v8aコアではブートループの原因に |
| EROFS対応 | `--format`指定時は端末側で `cat /proc/filesystems \| grep erofs` を確認 |
| 分割パーティション | `--no-merge`時は`system`/`product`/`system_ext`等を各スロットへ個別にflash |
| 音響・カメラ等のお作法 | 起動後に**Phhusson Treble App**（またはTrebleDroid設定）を導入してベンダー個別quirkを調整 |

---

## 設定と環境変数

| 項目 | 役割 | 既定値 |
|---|---|---|
| `$MYSTICGSI_DIR` | MysticGSIリポジトリの絶対パス | 未設定（保存値 → `~/mysticgsi`の順） |
| `$PORTRAIT_QT_PLATFORM` | Qt QPAプラットフォーム強制（`xcb`/`wayland`等） | WSLでは`xcb`、通常は未設定 |
| `$XDG_CONFIG_HOME` | 設定ディレクトリ基底 | `~/.config` |
| `~/.config/portrait/settings.json` | GUI設定の保存先（repoパス等） | 初回GUI起動時に生成 |
| `$PORTRAIT_APP_DIR` | アプリ本体の配置場所（スクリプト移動時用） | `~/.local/opt/portrait` |

`settings.json` の例：

```json
{
  "repo": "/home/user/mysticgsi"
}
```

---

## トラブルシューティング＆よくある質問

### Q. `MysticGSI cli.py not found` と怒られる
A. `~/mysticgsi`にcloneされているか確認するか、`export MYSTICGSI_DIR=/path/to/mysticgsi`を設定してください。

### Q. `MysticGSI virtualenv not found` と表示される
A. MysticGSI内の`.venv`が未作成です。以下を実行してください：
```bash
cd ~/mysticgsi && ./setup_host.py
```

### Q. `command not found: portrait`
A. `~/.local/bin`が現在のシェルPATHに入っていません。`hash -r`および`source ~/.bashrc`を実行してください。

### Q. `could not connect to display` / `No Qt platform plugin`
A. [WSL / WSLg Guide](#wsl--wslg環境での利用)を参照。PowerShellから `wsl --update` → `wsl --shutdown` で直るケースが大半です。

### Q. `mke2fs` や `mkfs.erofs` の段階でビルド失敗
A. EROFSビルドには`mkfs.erofs`が必要です（`sudo apt install erofs-utils`）。また、`tmp/`用の空き容量不足も典型例（1ビルドあたり**15〜30GB**消費）。`df -h`で容量を確認してください。

### Q. `waiting for another build to finish...` で止まる
A. 前回のビルドが異常終了して`buildlock`ファイルが残留している可能性があります。別プロセスが動いていないことを確認し、MysticGSI直下のロックファイルを削除してください。

### Q. URL指定時のaria2エラー
A. 高速ダウンローダーを導入してください：
```bash
sudo apt install aria2
```

---

## アンインストール

```bash
portrait uninstall
```

確認プロンプトに `yes` と入力すると以下が削除されます：

- `~/.local/bin/portrait`
- `~/.local/share/applications/portrait.desktop`
- `~/.local/opt/portrait/`
- `~/.profile` と `~/.bashrc` に追記された `# Portrait local-bin PATH` の行

**MysticGSI本体、ROMファイル、`tmp/`、`out/`の成果物、PyQt5は一切削除されません。**

設定ファイル（`~/.config/portrait`）も含めて完全削除する場合：

```bash
portrait uninstall --purge
```

---

## 開発・コントリビュート

Issue・PRは [dev-kjkg/portrait](https://github.com/dev-kjkg/portrait) へ歓迎します。

1. フォークしてフィーチャーブランチを作成（`git checkout -b feature/xyz`）
2. `portrait_qt.py`と`portrait`はPython 3.10+ / Qt 5およびbash互換を維持
3. CLIとGUI双方の動作確認後にPRを作成
4. ROM展開失敗やパッチの不具合は upstream の [MysticGSI/mysticgsi/issues](https://github.com/MysticGSI/mysticgsi/issues) へ報告

## ライセンス / クレジット

- **Portrait**: Copyright (c) 2024–2026 dev-kjkg. **Apache License 2.0** で配布（CLIスクリプトはMIT互換）
- **[MysticGSI](https://github.com/MysticGSI/mysticgsi)**: 上流ツール本体、Apache License 2.0
- **Qt / PyQt5**: Riverbank Computing / The Qt Company（GPL v3 / LGPL v3）
- **avbtool**: MIT License（MysticGSIに同梱）
- Project Treble、XDA Developers、そしてGSI移植に関わるコミュニティの皆さまに感謝いたします

---

<div align="center">

**[Portrait](https://github.com/dev-kjkg/portrait) — Treble GSIのビルドを、本来あるべき手軽さへ。**

</div>
