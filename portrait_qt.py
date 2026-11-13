#!/usr/bin/env python3
"""Portrait: multilingual Qt Widgets helper for the official MysticGSI CLI."""
from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

if os.environ.get("WSL_DISTRO_NAME") or "microsoft" in open("/proc/sys/kernel/osrelease", encoding="utf-8").read().lower():
    os.environ["DISPLAY"] = os.environ.get("DISPLAY") or ":0"
    os.environ["QT_QPA_PLATFORM"] = os.environ.get("PORTRAIT_QT_PLATFORM", "xcb")
    os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
    os.environ["QT_X11_NO_MITSHM"] = "1"

from PyQt5.QtCore import QProcess, QProcessEnvironment, QThread, QTimer, QUrl, Qt, pyqtSignal
from PyQt5.QtGui import QDesktopServices, QFontDatabase, QTextCursor
from PyQt5.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFileDialog, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox,
    QPlainTextEdit, QProgressBar, QPushButton, QTableWidget, QTableWidgetItem,
    QTabWidget, QVBoxLayout, QWidget, QAbstractItemView, QHeaderView,
)

APP_NAME = "Portrait"
CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "portrait"
CONFIG_FILE = CONFIG_DIR / "settings.json"
LANGUAGES = [("en", "English"), ("de", "Deutsch"), ("zh", "简体中文"), ("ja", "日本語"), ("hi", "हिन्दी")]

# GUI strings are localized. MysticGSI's own CLI output intentionally remains English.
TEXT = {
"en": {
"title":"Portrait — MysticGSI helper", "language":"Language", "repo":"MysticGSI folder", "browse":"Browse…", "setup":"Setup help", "build_tab":"Build / CLI", "out_tab":"Output files", "log":"Build log", "command":"Command", "build":"Build", "rebuild":"Rebuild", "list":"List", "clean":"Clean", "name":"Build name", "source":"Firmware file / URL", "pick_file":"Choose file…", "rom_type":"ROM type (--type)", "type_hint":"Pick a suggestion or type TYPE[:CUSTOM]", "format":"Image format", "ext4":"ext4 (default)", "lz4":"EROFS · lz4", "lz4hc":"EROFS · lz4hc", "lzma":"EROFS · lzma", "options":"Options", "compress":"--compress (also create ZIP)", "no_merge":"--no-merge (keep partitions separate)", "no_debloat":"--no-debloat (keep removable apps)", "add_tag":"--add tag", "tag_hint":"Optional output-name tag", "avb":"AVB signing key (--avb-key)", "key_hint":"RSA PEM key (optional)", "pick_key":"Choose key…", "advanced":"Advanced: extra official CLI arguments", "extra_hint":"Optional raw arguments; e.g. --help. Quote paths containing spaces.", "run":"Run command", "filter":"Filter files…", "file_kind":"File type", "all_files":"All files", "images":"Images (.img)", "archives":"Archives (.zip)", "text_files":"Info (.txt/.json)", "col_name":"Name", "col_type":"Type", "col_size":"Size", "col_modified":"Modified", "col_path":"Relative path", "refresh":"Refresh", "export_selected":"Export selected…", "export_all":"Export all…", "quick_export":"Quick export to Downloads", "open_folder":"Open containing folder", "open_out":"Open out folder", "clean_all":"Clean tmp + out…", "clean_warning":"Clean removes all entries under tmp/ and out/. It cannot delete only one build.", "status_ready":"Ready", "status_running":"Running…", "status_done":"Completed", "status_failed":"Failed (exit code {code})", "status_cancelled":"Cancelled", "status_files":"{count} files · {size}", "progress_idle":"Idle", "state_extract":"Extracting firmware", "state_unpack":"Unpacking images", "state_patch":"Patching ROM", "state_prepare":"Preparing filesystem", "state_mke2fs":"Creating image", "state_sign":"Signing image", "state_done":"Build complete", "repo_missing":"MysticGSI cli.py was not found in:\n{path}\nSelect the repository root folder.", "venv_missing":"MysticGSI virtual environment not found. Run setup_host.py in:\n{path}", "name_required":"Enter a build name.", "source_required":"Select a firmware file or enter an HTTP/HTTPS URL.", "source_missing":"Firmware file not found:\n{path}", "key_missing":"AVB key not found:\n{path}", "bad_args":"Could not parse extra arguments:\n{error}", "clean_confirm":"This deletes everything under:\n{tmp}\nand\n{out}\nContinue?", "export_dir":"Choose export folder", "export_none":"Select one or more files first.", "export_done":"Exported {count} file(s) to:\n{path}", "export_failed":"Export failed:\n{error}", "setup_text":"Run these commands in a terminal (sudo authentication is not entered in the GUI):\n\nsudo apt update && sudo apt install -y python3 git adb fastboot\ngit clone https://github.com/MysticGSI/mysticgsi.git ~/mysticgsi\ncd ~/mysticgsi && ./setup_host.py", "custom":"Custom / generic", "type_note":"Suggestions come from the repository's patch folders and vendor hooks; the field remains editable. MysticGSI accepts TYPE[:CUSTOM].", "no_out":"No files found under out/.", "all_types":"All", "selected":"Selected: {count}", "extra_help":"Extra arguments are appended to the official command. The GUI exposes all current options; use this field for new or uncommon CLI flags.", "folder_open_error":"Could not open folder:\n{path}", "command_label":"Command", "fmt_note":"EROFS needs target-device kernel/fstab support. The default is ext4.",
},
"de": {
"title":"Portrait — MysticGSI-Helfer", "language":"Sprache", "repo":"MysticGSI-Ordner", "browse":"Durchsuchen…", "setup":"Setup-Hilfe", "build_tab":"Build / CLI", "out_tab":"Ausgabedateien", "log":"Build-Protokoll", "command":"Befehl", "build":"Build", "rebuild":"Neu erstellen", "list":"Liste", "clean":"Bereinigen", "name":"Build-Name", "source":"Firmwaredatei / URL", "pick_file":"Datei wählen…", "rom_type":"ROM-Typ (--type)", "type_hint":"Vorschlag wählen oder TYPE[:CUSTOM] eingeben", "format":"Image-Format", "ext4":"ext4 (Standard)", "lz4":"EROFS · lz4", "lz4hc":"EROFS · lz4hc", "lzma":"EROFS · lzma", "options":"Optionen", "compress":"--compress (zusätzlich ZIP erstellen)", "no_merge":"--no-merge (Partitionen getrennt halten)", "no_debloat":"--no-debloat (entfernte Apps behalten)", "add_tag":"--add-Tag", "tag_hint":"Optionaler Tag für den Ausgabenamen", "avb":"AVB-Signaturschlüssel (--avb-key)", "key_hint":"RSA-PEM-Schlüssel (optional)", "pick_key":"Schlüssel wählen…", "advanced":"Erweitert: zusätzliche offizielle CLI-Argumente", "extra_hint":"Optionale Argumente, z. B. --help. Pfade mit Leerzeichen in Anführungszeichen setzen.", "run":"Befehl ausführen", "filter":"Dateien filtern…", "file_kind":"Dateityp", "all_files":"Alle Dateien", "images":"Images (.img)", "archives":"Archive (.zip)", "text_files":"Info (.txt/.json)", "col_name":"Name", "col_type":"Typ", "col_size":"Größe", "col_modified":"Geändert", "col_path":"Relativer Pfad", "refresh":"Aktualisieren", "export_selected":"Auswahl exportieren…", "export_all":"Alle exportieren…", "quick_export":"Schnellexport nach Downloads", "open_folder":"Enthaltenden Ordner öffnen", "open_out":"out-Ordner öffnen", "clean_all":"tmp + out bereinigen…", "clean_warning":"Clean entfernt alle Einträge unter tmp/ und out/. Einzelne Builds können damit nicht gelöscht werden.", "status_ready":"Bereit", "status_running":"Wird ausgeführt…", "status_done":"Abgeschlossen", "status_failed":"Fehlgeschlagen (Exitcode {code})", "status_cancelled":"Abgebrochen", "status_files":"{count} Dateien · {size}", "progress_idle":"Inaktiv", "state_extract":"Firmware wird entpackt", "state_unpack":"Images werden entpackt", "state_patch":"ROM wird gepatcht", "state_prepare":"Dateisystem wird vorbereitet", "state_mke2fs":"Image wird erstellt", "state_sign":"Image wird signiert", "state_done":"Build abgeschlossen", "repo_missing":"MysticGSI cli.py wurde hier nicht gefunden:\n{path}\nWähle den Stammordner des Repositorys.", "venv_missing":"MysticGSI-Umgebung nicht gefunden. Führe setup_host.py aus in:\n{path}", "name_required":"Gib einen Build-Namen ein.", "source_required":"Wähle eine Firmwaredatei oder gib eine HTTP/HTTPS-URL ein.", "source_missing":"Firmwaredatei nicht gefunden:\n{path}", "key_missing":"AVB-Schlüssel nicht gefunden:\n{path}", "bad_args":"Zusatzargumente konnten nicht gelesen werden:\n{error}", "clean_confirm":"Dies löscht alles unter:\n{tmp}\nund\n{out}\nFortfahren?", "export_dir":"Exportordner wählen", "export_none":"Wähle zuerst eine oder mehrere Dateien aus.", "export_done":"{count} Datei(en) exportiert nach:\n{path}", "export_failed":"Export fehlgeschlagen:\n{error}", "setup_text":"Führe diese Befehle in einem Terminal aus (sudo-Passwort nicht in der GUI eingeben):\n\nsudo apt update && sudo apt install -y python3 git adb fastboot\ngit clone https://github.com/MysticGSI/mysticgsi.git ~/mysticgsi\ncd ~/mysticgsi && ./setup_host.py", "custom":"Benutzerdefiniert / generisch", "type_note":"Vorschläge stammen aus Patch-Ordnern und Vendor-Hooks; das Feld bleibt editierbar. MysticGSI akzeptiert TYPE[:CUSTOM].", "no_out":"Keine Dateien unter out/ gefunden.", "all_types":"Alle", "selected":"Ausgewählt: {count}", "extra_help":"Zusatzargumente werden an den offiziellen Befehl angehängt. Aktuelle Optionen sind verfügbar; dieses Feld dient neuen oder seltenen CLI-Flags.", "folder_open_error":"Ordner konnte nicht geöffnet werden:\n{path}", "command_label":"Befehl", "fmt_note":"EROFS benötigt Kernel-/fstab-Unterstützung auf dem Zielgerät. Standard ist ext4.",
},
"zh": {
"title":"Portrait — MysticGSI 助手", "language":"语言", "repo":"MysticGSI 工作目录", "browse":"浏览…", "setup":"安装说明", "build_tab":"构建 / CLI", "out_tab":"输出文件", "log":"构建日志", "command":"命令", "build":"构建", "rebuild":"重新构建", "list":"列表", "clean":"清理", "name":"构建名称", "source":"固件文件 / URL", "pick_file":"选择文件…", "rom_type":"ROM 类型 (--type)", "type_hint":"选择建议项或输入 TYPE[:CUSTOM]", "format":"镜像格式", "ext4":"ext4（默认）", "lz4":"EROFS · lz4", "lz4hc":"EROFS · lz4hc", "lzma":"EROFS · lzma", "options":"选项", "compress":"--compress（同时生成 ZIP）", "no_merge":"--no-merge（保留独立分区）", "no_debloat":"--no-debloat（保留待移除的应用）", "add_tag":"--add 标签", "tag_hint":"可选的输出名称标签", "avb":"AVB 签名密钥 (--avb-key)", "key_hint":"RSA PEM 密钥（可选）", "pick_key":"选择密钥…", "advanced":"高级：附加官方 CLI 参数", "extra_hint":"可选原始参数，例如 --help。路径含空格时请加引号。", "run":"运行命令", "filter":"筛选文件…", "file_kind":"文件类型", "all_files":"所有文件", "images":"镜像 (.img)", "archives":"压缩包 (.zip)", "text_files":"信息 (.txt/.json)", "col_name":"名称", "col_type":"类型", "col_size":"大小", "col_modified":"修改时间", "col_path":"相对路径", "refresh":"刷新", "export_selected":"导出所选…", "export_all":"导出全部…", "quick_export":"快速导出到 Downloads", "open_folder":"打开所在文件夹", "open_out":"打开 out 文件夹", "clean_all":"清理 tmp + out…", "clean_warning":"Clean 会删除 tmp/ 和 out/ 下的全部内容，不能只删除单个构建。", "status_ready":"就绪", "status_running":"运行中…", "status_done":"已完成", "status_failed":"失败（退出代码 {code}）", "status_cancelled":"已取消", "status_files":"{count} 个文件 · {size}", "progress_idle":"空闲", "state_extract":"正在提取固件", "state_unpack":"正在解包镜像", "state_patch":"正在修补 ROM", "state_prepare":"正在准备文件系统", "state_mke2fs":"正在创建镜像", "state_sign":"正在签名镜像", "state_done":"构建完成", "repo_missing":"未在此目录找到 MysticGSI cli.py：\n{path}\n请选择仓库根目录。", "venv_missing":"未找到 MysticGSI 虚拟环境，请在此目录运行 setup_host.py：\n{path}", "name_required":"请输入构建名称。", "source_required":"请选择固件文件或输入 HTTP/HTTPS URL。", "source_missing":"找不到固件文件：\n{path}", "key_missing":"找不到 AVB 密钥：\n{path}", "bad_args":"无法解析附加参数：\n{error}", "clean_confirm":"将删除以下目录中的所有内容：\n{tmp}\n和\n{out}\n继续吗？", "export_dir":"选择导出文件夹", "export_none":"请先选择一个或多个文件。", "export_done":"已导出 {count} 个文件到：\n{path}", "export_failed":"导出失败：\n{error}", "setup_text":"请在终端运行以下命令（不要在 GUI 中输入 sudo 密码）：\n\nsudo apt update && sudo apt install -y python3 git adb fastboot\ngit clone https://github.com/MysticGSI/mysticgsi.git ~/mysticgsi\ncd ~/mysticgsi && ./setup_host.py", "custom":"自定义 / 通用", "type_note":"建议项来自仓库补丁目录和厂商钩子；输入框仍可编辑。MysticGSI 接受 TYPE[:CUSTOM]。", "no_out":"out/ 中没有文件。", "all_types":"全部", "selected":"已选择：{count}", "extra_help":"附加参数会原样传给官方命令。GUI 已提供当前全部选项；此处可填写新选项或少用选项。", "folder_open_error":"无法打开文件夹：\n{path}", "command_label":"命令", "fmt_note":"EROFS 需要目标设备内核和 fstab 支持。默认格式为 ext4。",
},
"ja": {
"title":"Portrait — MysticGSI ヘルパー", "language":"言語", "repo":"MysticGSI作業フォルダ", "browse":"選択…", "setup":"セットアップ案内", "build_tab":"ビルド / CLI", "out_tab":"出力ファイル", "log":"ビルド進捗ログ", "command":"コマンド", "build":"build（新規）", "rebuild":"rebuild（再作成）", "list":"list（一覧）", "clean":"clean（全削除）", "name":"ビルド名", "source":"ファームウェアファイル / URL", "pick_file":"ファイル選択…", "rom_type":"ROM type (--type)", "type_hint":"候補から選択、またはTYPE[:CUSTOM]を入力", "format":"イメージ形式", "ext4":"ext4（既定）", "lz4":"EROFS · lz4", "lz4hc":"EROFS · lz4hc", "lzma":"EROFS · lzma", "options":"オプション", "compress":"--compress（ZIPも作成）", "no_merge":"--no-merge（パーティションを分離）", "no_debloat":"--no-debloat（削除対象アプリを残す）", "add_tag":"--add タグ", "tag_hint":"出力名に追加する任意のタグ", "avb":"AVB署名鍵 (--avb-key)", "key_hint":"RSA PEM鍵（任意）", "pick_key":"鍵を選択…", "advanced":"詳細設定：公式CLIへ追加で渡す引数", "extra_hint":"任意の追加引数。例：--help。空白を含むパスは引用符で囲んでください。", "run":"コマンドを実行", "filter":"ファイル名で絞り込み…", "file_kind":"ファイル種別", "all_files":"すべて", "images":"イメージ (.img)", "archives":"アーカイブ (.zip)", "text_files":"情報 (.txt/.json)", "col_name":"名前", "col_type":"種類", "col_size":"サイズ", "col_modified":"更新日時", "col_path":"相対パス", "refresh":"更新", "export_selected":"選択項目をExport…", "export_all":"すべてExport…", "quick_export":"Downloadsへ簡単Export", "open_folder":"保存先フォルダを開く", "open_out":"outフォルダを開く", "clean_all":"tmp + outをclean…", "clean_warning":"cleanはtmp/とout/の中をすべて削除します。個別ビルドだけは削除できません。", "status_ready":"準備完了", "status_running":"実行中…", "status_done":"完了", "status_failed":"失敗（終了コード {code}）", "status_cancelled":"キャンセル", "status_files":"{count}ファイル · {size}", "progress_idle":"待機中", "state_extract":"ファームウェアを展開中", "state_unpack":"イメージを展開中", "state_patch":"ROMをパッチ中", "state_prepare":"ファイルシステムを準備中", "state_mke2fs":"イメージを作成中", "state_sign":"イメージに署名中", "state_done":"ビルド完了", "repo_missing":"次の場所にMysticGSIのcli.pyがありません：\n{path}\nリポジトリのルートを選択してください。", "venv_missing":"MysticGSIの仮想環境がありません。次の場所でsetup_host.pyを実行してください：\n{path}", "name_required":"ビルド名を入力してください。", "source_required":"ファームウェアファイルを選ぶか、HTTP/HTTPS URLを入力してください。", "source_missing":"ファイルが見つかりません：\n{path}", "key_missing":"AVB鍵が見つかりません：\n{path}", "bad_args":"追加引数を解析できません：\n{error}", "clean_confirm":"次の中身をすべて削除します：\n{tmp}\nおよび\n{out}\n続けますか？", "export_dir":"Export先フォルダを選択", "export_none":"先にファイルを1つ以上選択してください。", "export_done":"{count}個のファイルを次へExportしました：\n{path}", "export_failed":"Exportに失敗しました：\n{error}", "setup_text":"ターミナルで次のコマンドを実行してください（GUI内でsudo認証は行いません）：\n\nsudo apt update && sudo apt install -y python3 git adb fastboot\ngit clone https://github.com/MysticGSI/mysticgsi.git ~/mysticgsi\ncd ~/mysticgsi && ./setup_host.py", "custom":"カスタム / 汎用", "type_note":"候補はリポジトリ内のパッチフォルダとベンダーフックから読み込みます。欄は自由入力でき、MysticGSIはTYPE[:CUSTOM]を受け付けます。", "no_out":"out/にファイルがありません。", "all_types":"すべて", "selected":"選択中：{count}", "extra_help":"追加引数は公式コマンドへそのまま渡します。現在の全オプションを画面に用意し、新しい引数や普段使わない引数はここから渡せます。", "folder_open_error":"フォルダを開けません：\n{path}", "command_label":"コマンド", "fmt_note":"EROFSは端末側のカーネル/FSTAB対応が必要です。既定はext4です。",
},
"hi": {
"title":"Portrait — MysticGSI सहायक", "language":"भाषा", "repo":"MysticGSI फ़ोल्डर", "browse":"ब्राउज़…", "setup":"सेटअप सहायता", "build_tab":"बिल्ड / CLI", "out_tab":"आउटपुट फ़ाइलें", "log":"बिल्ड लॉग", "command":"कमांड", "build":"बिल्ड", "rebuild":"फिर से बिल्ड", "list":"सूची", "clean":"साफ़ करें", "name":"बिल्ड नाम", "source":"फ़र्मवेयर फ़ाइल / URL", "pick_file":"फ़ाइल चुनें…", "rom_type":"ROM प्रकार (--type)", "type_hint":"सुझाव चुनें या TYPE[:CUSTOM] लिखें", "format":"इमेज फ़ॉर्मैट", "ext4":"ext4 (डिफ़ॉल्ट)", "lz4":"EROFS · lz4", "lz4hc":"EROFS · lz4hc", "lzma":"EROFS · lzma", "options":"विकल्प", "compress":"--compress (ZIP भी बनाएँ)", "no_merge":"--no-merge (पार्टिशन अलग रखें)", "no_debloat":"--no-debloat (हटाए जाने वाले ऐप रखें)", "add_tag":"--add टैग", "tag_hint":"आउटपुट नाम के लिए वैकल्पिक टैग", "avb":"AVB हस्ताक्षर कुंजी (--avb-key)", "key_hint":"RSA PEM कुंजी (वैकल्पिक)", "pick_key":"कुंजी चुनें…", "advanced":"उन्नत: अतिरिक्त आधिकारिक CLI तर्क", "extra_hint":"वैकल्पिक तर्क, जैसे --help। स्पेस वाले पथ को उद्धरण में रखें।", "run":"कमांड चलाएँ", "filter":"फ़ाइलें फ़िल्टर करें…", "file_kind":"फ़ाइल प्रकार", "all_files":"सभी फ़ाइलें", "images":"इमेज (.img)", "archives":"आर्काइव (.zip)", "text_files":"जानकारी (.txt/.json)", "col_name":"नाम", "col_type":"प्रकार", "col_size":"आकार", "col_modified":"बदला गया", "col_path":"सापेक्ष पथ", "refresh":"रीफ़्रेश", "export_selected":"चयनित निर्यात…", "export_all":"सभी निर्यात…", "quick_export":"Downloads में तुरंत निर्यात", "open_folder":"फ़ोल्डर खोलें", "open_out":"out फ़ोल्डर खोलें", "clean_all":"tmp + out साफ़ करें…", "clean_warning":"clean, tmp/ और out/ के सभी आइटम हटाता है। केवल एक बिल्ड हटाना संभव नहीं है।", "status_ready":"तैयार", "status_running":"चल रहा है…", "status_done":"पूरा हुआ", "status_failed":"विफल (exit code {code})", "status_cancelled":"रद्द", "status_files":"{count} फ़ाइलें · {size}", "progress_idle":"निष्क्रिय", "state_extract":"फ़र्मवेयर निकाल रहा है", "state_unpack":"इमेज खोल रहा है", "state_patch":"ROM पैच कर रहा है", "state_prepare":"फ़ाइल सिस्टम तैयार कर रहा है", "state_mke2fs":"इमेज बना रहा है", "state_sign":"इमेज पर हस्ताक्षर कर रहा है", "state_done":"बिल्ड पूरा", "repo_missing":"इस स्थान पर MysticGSI cli.py नहीं मिला:\n{path}\nरिपॉज़िटरी का मूल फ़ोल्डर चुनें।", "venv_missing":"MysticGSI virtualenv नहीं मिला। इस फ़ोल्डर में setup_host.py चलाएँ:\n{path}", "name_required":"बिल्ड नाम दर्ज करें।", "source_required":"फ़र्मवेयर फ़ाइल चुनें या HTTP/HTTPS URL दर्ज करें।", "source_missing":"फ़ाइल नहीं मिली:\n{path}", "key_missing":"AVB कुंजी नहीं मिली:\n{path}", "bad_args":"अतिरिक्त तर्क पढ़े नहीं जा सके:\n{error}", "clean_confirm":"इन सभी आइटमों को हटाया जाएगा:\n{tmp}\nऔर\n{out}\nजारी रखें?", "export_dir":"निर्यात फ़ोल्डर चुनें", "export_none":"पहले एक या अधिक फ़ाइलें चुनें।", "export_done":"{count} फ़ाइलें यहाँ निर्यात हुईं:\n{path}", "export_failed":"निर्यात विफल:\n{error}", "setup_text":"टर्मिनल में ये कमांड चलाएँ (GUI में sudo पासवर्ड न डालें):\n\nsudo apt update && sudo apt install -y python3 git adb fastboot\ngit clone https://github.com/MysticGSI/mysticgsi.git ~/mysticgsi\ncd ~/mysticgsi && ./setup_host.py", "custom":"कस्टम / सामान्य", "type_note":"सुझाव रिपॉज़िटरी के patch फ़ोल्डरों और vendor hooks से आते हैं; फ़ील्ड संपादन योग्य है। MysticGSI TYPE[:CUSTOM] स्वीकार करता है।", "no_out":"out/ में कोई फ़ाइल नहीं मिली।", "all_types":"सभी", "selected":"चयनित: {count}", "extra_help":"अतिरिक्त तर्क आधिकारिक कमांड को दिए जाते हैं। वर्तमान सभी विकल्प स्क्रीन पर हैं; नए या कम उपयोग वाले CLI फ़्लैग यहाँ दें।", "folder_open_error":"फ़ोल्डर नहीं खुल सका:\n{path}", "command_label":"कमांड", "fmt_note":"EROFS के लिए लक्ष्य डिवाइस का kernel/fstab समर्थन आवश्यक है। डिफ़ॉल्ट ext4 है।",
}}

EXTRA_TEXT = {
    "en": {"process_start_failed":"Could not start the CLI process.", "process_exited":"Process exited with code {code}", "export_progress":"Exporting {percent}%", "export_log":"Exported {count} file(s) to {path}", "setup_action":"Setup…", "first_run_title":"MysticGSI setup", "first_run_question":"MysticGSI was not found at {path}. Choose setup, or select an existing installation.", "setup_now":"Set up MysticGSI", "already_installed":"MysticGSI is installed", "cancel":"Not now", "select_installed":"Select existing MysticGSI folder", "installed_missing":"cli.py was not found in the selected folder:\n{path}", "setup_started":"Setup was opened in a terminal. Complete the commands there, then return to Portrait.", "setup_no_terminal":"No supported terminal app was found. Run these commands manually in a terminal:\n\n{commands}", "setup_bad_target":"The selected folder is not empty and has no cli.py. Choose an empty folder or an existing MysticGSI checkout:\n{path}", "setup_again_confirm":"Run setup_host.py for this MysticGSI checkout? This may install system dependencies and prepare its virtual environment.\n\n{path}"},
    "de": {"process_start_failed":"Der CLI-Prozess konnte nicht gestartet werden.", "process_exited":"Prozess mit Exitcode {code} beendet", "export_progress":"Export läuft: {percent}%", "export_log":"{count} Datei(en) exportiert nach {path}", "setup_action":"Einrichten…", "first_run_title":"MysticGSI einrichten", "first_run_question":"MysticGSI wurde nicht unter {path} gefunden. Richte es ein oder wähle eine vorhandene Installation.", "setup_now":"MysticGSI einrichten", "already_installed":"MysticGSI ist installiert", "cancel":"Nicht jetzt", "select_installed":"Vorhandenen MysticGSI-Ordner wählen", "installed_missing":"cli.py wurde im ausgewählten Ordner nicht gefunden:\n{path}", "setup_started":"Das Setup wurde in einem Terminal geöffnet. Führe dort die Befehle aus und kehre dann zu Portrait zurück.", "setup_no_terminal":"Keine unterstützte Terminal-App gefunden. Führe diese Befehle manuell in einem Terminal aus:\n\n{commands}", "setup_bad_target":"Der Ordner ist nicht leer und enthält keine cli.py. Wähle einen leeren Ordner oder einen vorhandenen MysticGSI-Checkout:\n{path}", "setup_again_confirm":"setup_host.py für diesen MysticGSI-Checkout erneut ausführen? Dabei können Systemabhängigkeiten installiert und die virtuelle Umgebung eingerichtet werden.\n\n{path}"},
    "zh": {"process_start_failed":"无法启动 CLI 进程。", "process_exited":"进程已退出，代码 {code}", "export_progress":"正在导出 {percent}%", "export_log":"已导出 {count} 个文件到 {path}", "setup_action":"设置…", "first_run_title":"设置 MysticGSI", "first_run_question":"在 {path} 未找到 MysticGSI。可以进行设置，或选择已有安装。", "setup_now":"设置 MysticGSI", "already_installed":"MysticGSI 已安装", "cancel":"暂不", "select_installed":"选择已有 MysticGSI 文件夹", "installed_missing":"所选文件夹中未找到 cli.py：\n{path}", "setup_started":"已在终端打开设置流程。请在终端完成命令，然后返回 Portrait。", "setup_no_terminal":"未找到可用的终端程序。请在终端手动运行以下命令：\n\n{commands}", "setup_bad_target":"所选文件夹非空且没有 cli.py。请选择空文件夹或已有 MysticGSI 仓库：\n{path}", "setup_again_confirm":"要对此 MysticGSI 仓库重新运行 setup_host.py 吗？这可能会安装系统依赖并准备虚拟环境。\n\n{path}"},
    "ja": {"process_start_failed":"CLIプロセスを起動できませんでした。", "process_exited":"プロセス終了コード：{code}", "export_progress":"Export中 {percent}%", "export_log":"{count}個のファイルを{path}へExportしました", "setup_action":"セットアップ…", "first_run_title":"MysticGSIのセットアップ", "first_run_question":"{path}にMysticGSIが見つかりません。新規セットアップするか、既に導入済みのフォルダを選択してください。", "setup_now":"MysticGSIをセットアップ", "already_installed":"MysticGSIは導入済み", "cancel":"今はしない", "select_installed":"導入済みMysticGSIフォルダを選択", "installed_missing":"選択したフォルダにcli.pyが見つかりません：\n{path}", "setup_started":"セットアップ用ターミナルを開きました。ターミナルでコマンドを完了してからPortraitに戻ってください。", "setup_no_terminal":"対応するターミナルアプリが見つかりません。ターミナルで次のコマンドを実行してください：\n\n{commands}", "setup_bad_target":"選択したフォルダは空ではなくcli.pyもありません。空のフォルダまたはMysticGSIの導入先を選んでください：\n{path}", "setup_again_confirm":"このMysticGSIフォルダでsetup_host.pyを再実行しますか？システム依存関係の導入や仮想環境の設定を行う場合があります。\n\n{path}"},
    "hi": {"process_start_failed":"CLI प्रक्रिया शुरू नहीं हो सकी।", "process_exited":"प्रक्रिया exit code {code} के साथ समाप्त हुई", "export_progress":"निर्यात {percent}%", "export_log":"{count} फ़ाइलें {path} में निर्यात हुईं", "setup_action":"सेटअप…", "first_run_title":"MysticGSI सेटअप", "first_run_question":"{path} पर MysticGSI नहीं मिला। सेटअप करें या पहले से इंस्टॉल फ़ोल्डर चुनें।", "setup_now":"MysticGSI सेटअप करें", "already_installed":"MysticGSI इंस्टॉल है", "cancel":"अभी नहीं", "select_installed":"मौजूदा MysticGSI फ़ोल्डर चुनें", "installed_missing":"चुने गए फ़ोल्डर में cli.py नहीं मिला:\n{path}", "setup_started":"सेटअप टर्मिनल में खुल गया है। वहाँ कमांड पूरी करें, फिर Portrait पर लौटें।", "setup_no_terminal":"कोई समर्थित टर्मिनल ऐप नहीं मिला। टर्मिनल में ये कमांड चलाएँ:\n\n{commands}", "setup_bad_target":"फ़ोल्डर खाली नहीं है और उसमें cli.py नहीं है। खाली फ़ोल्डर या मौजूदा MysticGSI checkout चुनें:\n{path}", "setup_again_confirm":"क्या इस MysticGSI checkout पर setup_host.py फिर से चलाना है? यह सिस्टम निर्भरताएँ इंस्टॉल कर सकता है और virtualenv तैयार कर सकता है।\n\n{path}"},
}
for _language, _choices in {
    "en": {"yes":"Yes", "no":"No"},
    "de": {"yes":"Ja", "no":"Nein"},
    "zh": {"yes":"是", "no":"否"},
    "ja": {"yes":"はい", "no":"いいえ"},
    "hi": {"yes":"हाँ", "no":"नहीं"},
}.items():
    EXTRA_TEXT[_language].update(_choices)
for _language, _label in {
    "en":"Open tmp folder", "de":"tmp-Ordner öffnen", "zh":"打开 tmp 文件夹", "ja":"tmpフォルダを開く", "hi":"tmp फ़ोल्डर खोलें",
}.items():
    EXTRA_TEXT[_language]["open_tmp"] = _label

TYPE_PRESETS = ["auto", "generic", "custom", "pixel", "alos", "miui", "hyperos", "joyui", "oneui", "emui", "magicos", "harmonyos", "zui", "nothing", "realmeui", "oxygenos", "coloros", "myos", "redmagic", "nebulaos"]
STATE_KEYS = {"extract":"state_extract", "unpack":"state_unpack", "patch":"state_patch", "prepare":"state_prepare", "mke2fs":"state_mke2fs", "sign":"state_sign", "done":"state_done"}
PROGRESS_RE = re.compile(r"^\[\s*(\d{1,3})%\]\s*([A-Za-z_]+)(?:\s*==\s*(.*))?")
ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def read_settings():
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}


def save_settings(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def expanded(value):
    return Path(os.path.expandvars(os.path.expanduser(value.strip())))


def human_size(size):
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TiB"


class ExportWorker(QThread):
    progress_changed = pyqtSignal(int, str)
    completed = pyqtSignal(int, str)
    failed = pyqtSignal(str)

    def __init__(self, sources, target):
        super().__init__()
        self.sources = list(sources)
        self.target = Path(target)

    def run(self):
        destination = None
        try:
            total = sum(path.stat().st_size for path in self.sources)
            total = max(total, 1)
            copied = 0
            count = 0
            self.target.mkdir(parents=True, exist_ok=True)
            for source in self.sources:
                destination = self.target / source.name
                index = 1
                while destination.exists():
                    destination = self.target / f"{source.stem} ({index}){source.suffix}"
                    index += 1
                with source.open("rb") as incoming, destination.open("wb") as outgoing:
                    while True:
                        chunk = incoming.read(8 * 1024 * 1024)
                        if not chunk:
                            break
                        outgoing.write(chunk)
                        copied += len(chunk)
                        self.progress_changed.emit(min(100, copied * 100 // total), source.name)
                shutil.copystat(source, destination)
                count += 1
            self.completed.emit(count, str(self.target))
        except Exception as exc:
            if destination is not None:
                try:
                    destination.unlink(missing_ok=True)
                except OSError:
                    pass
            self.failed.emit(str(exc))


class PortraitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = read_settings()
        self.language = self.settings.get("language", "ja")
        if self.language not in TEXT:
            self.language = "ja"
        self._bindings = []
        self._stream_buffer = ""
        self.process = None
        self.output_paths = []
        self.export_worker = None
        self.setMinimumSize(850, 690)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.root_layout = QVBoxLayout(self.central)
        self.root_layout.setContentsMargins(12, 10, 12, 10)
        self.root_layout.setSpacing(8)

        self.header = QHBoxLayout()
        self.repo_label = self.label("repo")
        self.repo_edit = QLineEdit(self.settings.get("repo", os.environ.get("MYSTICGSI_DIR", str(Path.home() / "mysticgsi"))))
        self.repo_edit.editingFinished.connect(self.refresh_type_choices)
        self.repo_edit.editingFinished.connect(self.refresh_output)
        self.repo_browse = self.button("browse", self.choose_repo)
        self.setup_button = self.button("setup_action", self.setup_action)
        self.lang_label = self.label("language")
        self.language_combo = QComboBox()
        for code, native_name in LANGUAGES:
            self.language_combo.addItem(native_name, code)
        self.language_combo.currentIndexChanged.connect(self.language_changed)
        self.header.addWidget(self.repo_label)
        self.header.addWidget(self.repo_edit, 1)
        self.header.addWidget(self.repo_browse)
        self.header.addWidget(self.setup_button)
        self.header.addSpacing(10)
        self.header.addWidget(self.lang_label)
        self.header.addWidget(self.language_combo)
        self.root_layout.addLayout(self.header)

        self.tabs = QTabWidget()
        self.build_page_widget = self.build_page()
        self.out_page_widget = self.output_page()
        self.tabs.addTab(self.build_page_widget, "")
        self.tabs.addTab(self.out_page_widget, "")
        self.tabs.currentChanged.connect(self.tab_changed)
        self.root_layout.addWidget(self.tabs, 1)

        self.log_label = self.label("log")
        self.root_layout.addWidget(self.log_label)
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.log.setMaximumBlockCount(5000)
        self.log.setMinimumHeight(125)
        self.root_layout.addWidget(self.log)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.root_layout.addWidget(self.progress)
        self.status = QLabel("")
        self.root_layout.addWidget(self.status)

        self.retranslate_ui()
        idx = self.language_combo.findData(self.language)
        self.language_combo.blockSignals(True)
        self.language_combo.setCurrentIndex(max(idx, 0))
        self.language_combo.blockSignals(False)
        self.refresh_type_choices()
        self.refresh_output()
        self.show()
        self.raise_()
        self.activateWindow()
        QTimer.singleShot(500, self.first_run_setup_check)

    def t(self, key):
        return TEXT.get(self.language, TEXT["en"]).get(key, EXTRA_TEXT.get(self.language, EXTRA_TEXT["en"]).get(key, TEXT["en"].get(key, EXTRA_TEXT["en"].get(key, key))))

    def bind(self, widget, key, method="setText"):
        self._bindings.append((widget, key, method))
        getattr(widget, method)(self.t(key))
        return widget

    def label(self, key):
        return self.bind(QLabel(), key)

    def button(self, key, callback):
        widget = self.bind(QPushButton(), key)
        widget.clicked.connect(callback)
        return widget

    def build_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.command_combo = QComboBox()
        self.command_combo.currentIndexChanged.connect(self.command_changed)
        self.name_edit = QLineEdit()
        self.source_edit = QLineEdit()
        self.source_pick = self.button("pick_file", self.choose_source)
        source_row = QWidget()
        source_layout = QHBoxLayout(source_row)
        source_layout.setContentsMargins(0, 0, 0, 0)
        source_layout.addWidget(self.source_edit, 1)
        source_layout.addWidget(self.source_pick)

        self.type_combo = QComboBox()
        self.type_combo.setEditable(True)
        self.type_combo.setInsertPolicy(QComboBox.NoInsert)
        self.type_combo.setToolTip(self.t("type_note"))
        self.format_combo = QComboBox()
        self.compress_check = self.bind(QCheckBox(), "compress")
        self.no_merge_check = self.bind(QCheckBox(), "no_merge")
        self.no_debloat_check = self.bind(QCheckBox(), "no_debloat")
        options = QWidget()
        options_layout = QVBoxLayout(options)
        options_layout.setContentsMargins(0, 0, 0, 0)
        options_layout.addWidget(self.compress_check)
        options_layout.addWidget(self.no_merge_check)
        options_layout.addWidget(self.no_debloat_check)
        self.tag_edit = QLineEdit()
        self.avb_edit = QLineEdit()
        self.key_pick = self.button("pick_key", self.choose_key)
        key_row = QWidget()
        key_layout = QHBoxLayout(key_row)
        key_layout.setContentsMargins(0, 0, 0, 0)
        key_layout.addWidget(self.avb_edit, 1)
        key_layout.addWidget(self.key_pick)

        self.extra_group = QGroupBox()
        self.bind(self.extra_group, "advanced", "setTitle")
        self.extra_group.setCheckable(True)
        self.extra_group.setChecked(False)
        extra_layout = QVBoxLayout(self.extra_group)
        self.extra_edit = QLineEdit()
        self.extra_layout_hint = self.label("extra_hint")
        extra_layout.addWidget(self.extra_edit)
        extra_layout.addWidget(self.extra_layout_hint)

        self.form_labels = {}
        for key, widget in (("command", self.command_combo), ("name", self.name_edit), ("source", source_row), ("rom_type", self.type_combo), ("format", self.format_combo), ("options", options), ("add_tag", self.tag_edit), ("avb", key_row)):
            label = self.label(key)
            self.form_labels[key] = label
            form.addRow(label, widget)
        layout.addLayout(form)
        self.type_note_label = self.label("type_note")
        self.type_note_label.setWordWrap(True)
        layout.addWidget(self.type_note_label)
        self.format_note_label = self.label("fmt_note")
        self.format_note_label.setWordWrap(True)
        layout.addWidget(self.format_note_label)
        layout.addWidget(self.extra_group)
        self.run_button = self.button("run", self.run_action)
        layout.addWidget(self.run_button)
        layout.addStretch(1)
        return page

    def output_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        toolbar = QHBoxLayout()
        self.file_filter = QLineEdit()
        self.bind(self.file_filter, "filter", "setPlaceholderText")
        self.file_filter.textChanged.connect(self.apply_output_filter)
        self.filetype_combo = QComboBox()
        self.filetype_combo.currentIndexChanged.connect(self.apply_output_filter)
        self.filetype_label = self.label("file_kind")
        self.refresh_button = self.button("refresh", self.refresh_output)
        self.export_selected_button = self.button("export_selected", self.export_selected)
        self.export_all_button = self.button("export_all", self.export_all)
        self.quick_export_button = self.button("quick_export", self.quick_export)
        self.open_folder_button = self.button("open_folder", self.open_selected_folder)
        self.open_tmp_button = self.button("open_tmp", self.open_tmp_folder)
        self.open_out_button = self.button("open_out", self.open_out_folder)
        self.clean_button = self.button("clean_all", self.clean_all)
        toolbar.addWidget(self.file_filter, 1)
        toolbar.addWidget(self.filetype_label)
        toolbar.addWidget(self.filetype_combo)
        layout.addLayout(toolbar)

        self.output_table = QTableWidget(0, 5)
        self.output_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.output_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.output_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.output_table.setAlternatingRowColors(True)
        self.output_table.setSortingEnabled(True)
        self.output_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.output_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.output_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.output_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.output_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.output_table.itemSelectionChanged.connect(self.update_selection_status)
        self.output_table.cellDoubleClicked.connect(self.open_file_parent)
        layout.addWidget(self.output_table, 1)

        buttons = QGridLayout()
        for index, button in enumerate((self.refresh_button, self.export_selected_button, self.export_all_button, self.quick_export_button, self.open_folder_button, self.open_tmp_button, self.open_out_button, self.clean_button)):
            buttons.addWidget(button, index // 4, index % 4)
        layout.addLayout(buttons)
        self.clean_warning_label = self.label("clean_warning")
        self.clean_warning_label.setWordWrap(True)
        layout.addWidget(self.clean_warning_label)
        self.out_status = QLabel("")
        layout.addWidget(self.out_status)
        return page

    def retranslate_ui(self):
        self.setWindowTitle(self.t("title"))
        for widget, key, method in self._bindings:
            getattr(widget, method)(self.t(key))
        self.tabs.setTabText(0, self.t("build_tab"))
        self.tabs.setTabText(1, self.t("out_tab"))
        self.output_table.setHorizontalHeaderLabels([self.t("col_name"), self.t("col_type"), self.t("col_size"), self.t("col_modified"), self.t("col_path")])
        if hasattr(self, "command_combo"):
            current = self.command_combo.currentData() or "build"
            self.command_combo.blockSignals(True)
            self.command_combo.clear()
            for key, val in (("build", "build"), ("rebuild", "rebuild"), ("list", "list"), ("clean", "clean")):
                self.command_combo.addItem(self.t(key), val)
            self.command_combo.setCurrentIndex(max(0, self.command_combo.findData(current)))
            self.command_combo.blockSignals(False)
            old_format = self.format_combo.currentData()
            self.format_combo.clear()
            self.format_combo.addItem(self.t("ext4"), "")
            for value in ("lz4", "lz4hc", "lzma"):
                self.format_combo.addItem(self.t(value), value)
            ix = self.format_combo.findData(old_format if old_format is not None else "")
            self.format_combo.setCurrentIndex(max(ix, 0))
            old_filter = self.filetype_combo.currentData() or "all"
            self.filetype_combo.clear()
            for key, val in (("all_files", "all"), ("images", "img"), ("archives", "zip"), ("text_files", "text")):
                self.filetype_combo.addItem(self.t(key), val)
            self.filetype_combo.setCurrentIndex(max(0, self.filetype_combo.findData(old_filter)))
            self.command_changed(self.command_combo.currentIndex())
        if hasattr(self, "status") and self.process is None:
            self.status.setText(self.t("status_ready"))
        self.update_selection_status()
        self.apply_output_filter()

    def language_changed(self, _index):
        code = self.language_combo.currentData()
        if code and code != self.language:
            self.language = code
            self.settings["language"] = code
            save_settings(self.settings)
            self.retranslate_ui()
            self.refresh_type_choices()
            self.refresh_output()

    def repo_path(self):
        return expanded(self.repo_edit.text()).resolve()

    def refresh_type_choices(self):
        if not hasattr(self, "type_combo"):
            return
        current = self.type_combo.currentText()
        values = set(TYPE_PRESETS)
        root = self.repo_path() / "patches"
        if root.is_dir():
            ignored_roots = {"all", "miui_device_features", "vndk"}
            for version in root.iterdir():
                if not version.is_dir() or version.name in ignored_roots:
                    continue
                try:
                    for candidate in version.iterdir():
                        if candidate.is_dir() and not candidate.name.isdigit():
                            values.add(candidate.name)
                except OSError:
                    continue
        self.type_combo.blockSignals(True)
        self.type_combo.clear()
        self.type_combo.addItems(["auto", *sorted(v for v in values if v != "auto")])
        self.type_combo.setEditText(current or "auto")
        self.type_combo.blockSignals(False)
        self.type_combo.setToolTip(self.t("type_note"))

    def choose_repo(self):
        path = QFileDialog.getExistingDirectory(self, self.t("repo"), self.repo_edit.text())
        if path:
            self.repo_edit.setText(path)
            self.refresh_type_choices()
            self.refresh_output()

    def choose_source(self):
        path, _ = QFileDialog.getOpenFileName(self, self.t("source"), str(Path.home()), self.t("all_files") + " (*)")
        if path:
            self.source_edit.setText(path)

    def choose_key(self):
        path, _ = QFileDialog.getOpenFileName(self, self.t("avb"), str(Path.home()), "PEM (*.pem);;" + self.t("all_files") + " (*)")
        if path:
            self.avb_edit.setText(path)

    def first_run_setup_check(self):
        if (self.repo_path() / "cli.py").is_file() or self.settings.get("first_run_prompt_dismissed"):
            return
        dialog = QMessageBox(self)
        dialog.setWindowTitle(self.t("first_run_title"))
        dialog.setText(self.t("first_run_question").format(path=self.repo_path()))
        setup_button = dialog.addButton(self.t("setup_now"), QMessageBox.AcceptRole)
        installed_button = dialog.addButton(self.t("already_installed"), QMessageBox.ActionRole)
        dialog.addButton(self.t("cancel"), QMessageBox.RejectRole)
        dialog.exec_()
        clicked = dialog.clickedButton()
        self.settings["first_run_prompt_dismissed"] = True
        save_settings(self.settings)
        if clicked is setup_button:
            self.start_setup_terminal(self.repo_path())
        elif clicked is installed_button:
            self.choose_installed_repo()

    def choose_installed_repo(self):
        selected = QFileDialog.getExistingDirectory(self, self.t("select_installed"), str(Path.home()))
        if not selected:
            return
        path = Path(selected).expanduser().resolve()
        if not (path / "cli.py").is_file():
            QMessageBox.warning(self, APP_NAME, self.t("installed_missing").format(path=path))
            return
        self.repo_edit.setText(str(path))
        self.settings["repo"] = str(path)
        save_settings(self.settings)
        self.refresh_type_choices()
        self.refresh_output()

    def setup_action(self):
        path = self.repo_path()
        if (path / "cli.py").is_file():
            if not self.confirm_yes_no(self.t("setup_action"), self.t("setup_again_confirm").format(path=path)):
                return
        self.start_setup_terminal(path)

    def confirm_yes_no(self, title, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle(title)
        dialog.setText(message)
        yes_button = dialog.addButton(self.t("yes"), QMessageBox.AcceptRole)
        dialog.addButton(self.t("no"), QMessageBox.RejectRole)
        dialog.exec_()
        return dialog.clickedButton() is yes_button

    def start_setup_terminal(self, path):
        path = Path(path).expanduser().resolve()
        cli_file = path / "cli.py"
        if path.exists() and not cli_file.is_file():
            try:
                nonempty = any(path.iterdir())
            except OSError:
                nonempty = True
            if nonempty:
                QMessageBox.warning(self, APP_NAME, self.t("setup_bad_target").format(path=path))
                return
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            QMessageBox.critical(self, APP_NAME, str(exc))
            return
        self.repo_edit.setText(str(path))
        self.settings["repo"] = str(path)
        save_settings(self.settings)
        repo_q = shlex.quote(str(path))
        cli_q = shlex.quote(str(cli_file))
        shell_script = "\n".join((
            "set -e",
            "trap 'echo; read -r -p \"Press Enter to close this terminal...\" _' EXIT",
            "sudo apt update",
            "sudo apt install -y python3 git adb fastboot python3-pyqt5",
            f"if [[ ! -f {cli_q} ]]; then git clone https://github.com/MysticGSI/mysticgsi.git {repo_q}; fi",
            f"cd {repo_q}",
            "./setup_host.py",
            "echo 'Setup finished. Return to Portrait; use Refresh or restart the app if needed.'",
        ))
        terminals = ("x-terminal-emulator", "gnome-terminal", "mate-terminal", "konsole", "xfce4-terminal", "tilix", "xterm")
        terminal = next(((name, shutil.which(name)) for name in terminals if shutil.which(name)), None)
        if terminal is None:
            QApplication.clipboard().setText(shell_script)
            QMessageBox.information(self, APP_NAME, self.t("setup_no_terminal").format(commands=shell_script))
            return
        name, executable = terminal
        if name in ("gnome-terminal", "mate-terminal", "tilix"):
            arguments = ["--", "bash", "-lc", shell_script]
        elif name == "xfce4-terminal":
            arguments = ["--command", "bash -lc " + shlex.quote(shell_script)]
        else:
            arguments = ["-e", "bash", "-lc", shell_script]
        try:
            result = QProcess.startDetached(executable, arguments, str(Path.home()))
            started = result[0] if isinstance(result, tuple) else bool(result)
        except (OSError, TypeError):
            started = False
        if started:
            QMessageBox.information(self, APP_NAME, self.t("setup_started"))
        else:
            QApplication.clipboard().setText(shell_script)
            QMessageBox.information(self, APP_NAME, self.t("setup_no_terminal").format(commands=shell_script))

    def command_changed(self, _index):
        if not hasattr(self, "command_combo"):
            return
        command = self.command_combo.currentData()
        build = command == "build"
        named = command in ("build", "rebuild")
        for widget in (self.source_edit, self.source_pick, self.type_combo, self.format_combo, self.no_merge_check, self.no_debloat_check, self.tag_edit):
            widget.setEnabled(build)
        self.name_edit.setEnabled(named)
        self.compress_check.setEnabled(named)
        self.avb_edit.setEnabled(named)
        self.key_pick.setEnabled(named)
        command_name = self.t(command or "build")
        self.run_button.setText(self.t("run") + f" — {command_name}")

    def run_action(self):
        command = self.command_combo.currentData() or "build"
        extra_text = self.extra_edit.text().strip() if self.extra_group.isChecked() else ""
        try:
            extra_args = shlex.split(extra_text) if extra_text else []
        except ValueError as exc:
            QMessageBox.warning(self, APP_NAME, self.t("bad_args").format(error=exc))
            return
        args = [command]
        if command in ("build", "rebuild"):
            name = self.name_edit.text().strip()
            if not name:
                QMessageBox.warning(self, APP_NAME, self.t("name_required"))
                return
            args.append(name)
        if command == "build":
            source = self.source_edit.text().strip()
            if not source:
                QMessageBox.warning(self, APP_NAME, self.t("source_required"))
                return
            parsed = urlparse(source)
            if not (parsed.scheme in ("http", "https") and parsed.netloc):
                path = expanded(source).resolve()
                if not path.is_file():
                    QMessageBox.warning(self, APP_NAME, self.t("source_missing").format(path=path))
                    return
                source = str(path)
            args.append(source)
            rom_type = self.type_combo.currentText().strip() or "auto"
            args += ["--type", rom_type]
            fmt = self.format_combo.currentData()
            if fmt:
                args += ["--format", fmt]
            if self.compress_check.isChecked(): args.append("--compress")
            if self.no_merge_check.isChecked(): args.append("--no-merge")
            if self.no_debloat_check.isChecked(): args.append("--no-debloat")
            tag = self.tag_edit.text().strip()
            if tag: args += ["--add", tag]
        if command in ("build", "rebuild"):
            if self.compress_check.isChecked() and command == "rebuild": args.append("--compress")
            key = self.avb_edit.text().strip()
            if key:
                key_path = expanded(key).resolve()
                if not key_path.is_file():
                    QMessageBox.warning(self, APP_NAME, self.t("key_missing").format(path=key_path))
                    return
                args += ["--avb-key", str(key_path)]
        if command == "clean":
            repo = self.repo_path()
            if not self.confirm_yes_no(self.t("clean"), self.t("clean_confirm").format(tmp=repo / "tmp", out=repo / "out")):
                return
            args.append("--yes")
        args.extend(extra_args)
        self.launch(args)

    def repo(self):
        path = self.repo_path()
        if not path.is_dir() or not (path / "cli.py").is_file():
            QMessageBox.critical(self, APP_NAME, self.t("repo_missing").format(path=path))
            return None
        self.settings["repo"] = str(path)
        save_settings(self.settings)
        return path

    def launch(self, args):
        if self.process is not None and self.process.state() != QProcess.NotRunning:
            return
        if self.export_worker is not None and self.export_worker.isRunning():
            return
        repo = self.repo()
        if repo is None:
            return
        python = repo / ".venv/bin/python"
        if not python.is_file():
            QMessageBox.critical(self, APP_NAME, self.t("venv_missing").format(path=repo))
            return
        self.process = QProcess(self)
        environment = QProcessEnvironment.systemEnvironment()
        environment.insert("PYTHONUNBUFFERED", "1")
        self.process.setProcessEnvironment(environment)
        self.process.setWorkingDirectory(str(repo))
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.finished.connect(self.process_finished)
        full = [str(python), "-u", str(repo / "cli.py"), *args]
        self.current_action = args[0]
        self._stream_buffer = ""
        self.progress.setValue(0)
        self.progress.setFormat(self.t("status_running"))
        self.status.setText(self.t("status_running"))
        self.log.appendPlainText("\n$ " + shlex.join(full))
        self.set_busy(True)
        self.process.start(full[0], full[1:])
        if not self.process.waitForStarted(3000):
            self.process = None
            self.set_busy(False)
            self.status.setText(self.t("status_failed").format(code="start"))
            self.log.appendPlainText(self.t("process_start_failed"))

    def read_output(self):
        raw = bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="replace")
        raw = ANSI_RE.sub("", raw).replace("\r\n", "\n").replace("\r", "\n")
        text = self._stream_buffer + raw
        lines = text.split("\n")
        self._stream_buffer = lines.pop()
        for line in lines:
            self.process_line(line)

    def process_line(self, line):
        match = PROGRESS_RE.match(line.strip())
        if match:
            percent = max(0, min(100, int(match.group(1))))
            state = match.group(2).lower()
            self.progress.setValue(percent)
            self.progress.setFormat(f"{percent}%")
            state_key = STATE_KEYS.get(state)
            if state_key:
                self.status.setText(f"{percent}% — {self.t(state_key)}")
            if match.group(3):
                detail = match.group(3).strip()
                self.log.appendPlainText(f"[{percent:3d}%] {self.t(state_key) if state_key else state} — {detail}")
                return
        if line:
            self.log.appendPlainText(line)
        self.log.moveCursor(QTextCursor.End)
        self.log.ensureCursorVisible()

    def process_finished(self, code, _exit_status):
        self.read_output()
        if self._stream_buffer:
            self.process_line(self._stream_buffer)
            self._stream_buffer = ""
        action = getattr(self, "current_action", "")
        self.status.setText(self.t("status_done") if code == 0 else self.t("status_failed").format(code=code))
        if code == 0:
            self.progress.setValue(100)
            self.progress.setFormat("100%")
        self.log.appendPlainText("\n" + self.t("process_exited").format(code=code))
        self.process = None
        self.set_busy(False)
        self.refresh_output()

    def set_busy(self, busy):
        for widget in (self.run_button, self.export_selected_button, self.export_all_button, self.quick_export_button, self.clean_button):
            widget.setEnabled(not busy)

    def refresh_output(self):
        if not hasattr(self, "output_table"):
            return
        repo = self.repo_path()
        out = repo / "out"
        files = []
        if out.is_dir():
            for path in out.rglob("*"):
                try:
                    if path.is_file():
                        files.append(path)
                except OSError:
                    continue
            files.sort(key=lambda path: (path.stat().st_mtime if path.exists() else 0, str(path).casefold()), reverse=True)
        self.output_paths = files
        self.output_table.setSortingEnabled(False)
        self.output_table.setRowCount(0)
        for path in files:
            row = self.output_table.rowCount()
            self.output_table.insertRow(row)
            try:
                stat = path.stat()
                size_text = human_size(stat.st_size)
                modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            except OSError:
                size_text, modified = "?", "?"
            rel = str(path.relative_to(out))
            values = (path.name, path.suffix.lstrip(".").upper() or "FILE", size_text, modified, rel)
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, str(path))
                item.setToolTip(str(path))
                if col == 2:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.output_table.setItem(row, col, item)
        self.output_table.setSortingEnabled(True)
        self.apply_output_filter()
        self.out_status.setText(self.t("status_files").format(count=len(files), size=self.total_output_size(files)))

    def tab_changed(self, index):
        if index == 1:
            self.refresh_output()

    def total_output_size(self, files):
        total = 0
        for path in files:
            try: total += path.stat().st_size
            except OSError: pass
        return human_size(total)

    def apply_output_filter(self, *_):
        if not hasattr(self, "output_table"):
            return
        query = self.file_filter.text().casefold().strip()
        kind = self.filetype_combo.currentData() or "all"
        for row in range(self.output_table.rowCount()):
            name = self.output_table.item(row, 0).text().casefold()
            path = self.output_table.item(row, 4).text().casefold()
            suffix = Path(path).suffix.lower()
            text_match = not query or query in name or query in path
            kind_match = kind == "all" or (kind == "img" and suffix == ".img") or (kind == "zip" and suffix == ".zip") or (kind == "text" and suffix in (".txt", ".json"))
            self.output_table.setRowHidden(row, not (text_match and kind_match))
        if not self.output_paths:
            self.out_status.setText(self.t("no_out"))

    def selected_files(self):
        result = set()
        for index in self.output_table.selectionModel().selectedRows():
            item = self.output_table.item(index.row(), 0)
            if item:
                result.add(Path(item.data(Qt.UserRole)))
        return sorted(result)

    def update_selection_status(self):
        if not hasattr(self, "out_status"):
            return
        selected = len(self.selected_files())
        total = len(self.output_paths)
        if selected:
            self.out_status.setText(self.t("selected").format(count=selected) + f" / {total}")

    def open_out_folder(self):
        path = self.repo_path() / "out"
        path.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def open_tmp_folder(self):
        path = self.repo_path() / "tmp"
        path.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def open_selected_folder(self):
        paths = self.selected_files()
        if not paths:
            return
        parent = paths[0].parent
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(parent)))

    def open_file_parent(self, row, _column):
        item = self.output_table.item(row, 0)
        if item:
            path = Path(item.data(Qt.UserRole))
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path.parent)))

    def export_selected(self):
        files = self.selected_files()
        if not files:
            QMessageBox.information(self, APP_NAME, self.t("export_none"))
            return
        self.export_files(files)

    def export_all(self):
        self.export_files(self.output_paths)

    def quick_export(self):
        files = self.selected_files()
        if not files:
            QMessageBox.information(self, APP_NAME, self.t("export_none"))
            return
        target = Path.home() / "Downloads"
        target.mkdir(parents=True, exist_ok=True)
        self.copy_to_folder(files, target)

    def export_files(self, files):
        if not files:
            QMessageBox.information(self, APP_NAME, self.t("no_out"))
            return
        target = QFileDialog.getExistingDirectory(self, self.t("export_dir"), str(Path.home() / "Downloads"))
        if target:
            self.copy_to_folder(files, Path(target))

    def copy_to_folder(self, files, target):
        if self.export_worker is not None and self.export_worker.isRunning():
            return
        if self.process is not None and self.process.state() != QProcess.NotRunning:
            return
        self.progress.setValue(0)
        self.progress.setFormat(self.t("export_progress").format(percent="%p"))
        self.status.setText(self.t("status_running"))
        self.export_worker = ExportWorker(files, target)
        self.export_worker.progress_changed.connect(self.export_progress)
        self.export_worker.completed.connect(self.export_completed)
        self.export_worker.failed.connect(self.export_failed)
        self.export_worker.finished.connect(self.export_finished)
        self.set_busy(True)
        self.export_worker.start()

    def export_progress(self, percent, filename):
        self.progress.setValue(percent)
        self.status.setText(self.t("export_progress").format(percent=percent) + f" — {filename}")

    def export_completed(self, count, path):
        self.progress.setValue(100)
        self.progress.setFormat("100%")
        self.status.setText(self.t("status_done"))
        QMessageBox.information(self, APP_NAME, self.t("export_done").format(count=count, path=path))
        self.log.appendPlainText(self.t("export_log").format(count=count, path=path))

    def export_failed(self, error):
        self.status.setText(self.t("status_failed").format(code="export"))
        QMessageBox.critical(self, APP_NAME, self.t("export_failed").format(error=error))

    def export_finished(self):
        self.export_worker = None
        self.set_busy(False)

    def clean_all(self):
        command_index = self.command_combo.findData("clean")
        self.command_combo.setCurrentIndex(command_index)
        self.run_action()


def main():
    app = QApplication(sys.argv[:1])
    window = PortraitWindow()
    window.show()
    window.raise_()
    window.activateWindow()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
