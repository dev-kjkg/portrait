#!/usr/bin/env python3
"""Portrait native GTK 3 UI. MysticGSI remains a separate CLI dependency."""
from __future__ import annotations

import json
import os
import queue
import shlex
import shutil
import subprocess
import sys
import threading
from pathlib import Path
from urllib.parse import urlparse

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, GLib, Gtk

APP_NAME = "Portrait"
APP_ID = "org.mysticgsi.Portrait"
CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "portrait"
CONFIG_FILE = CONFIG_DIR / "settings.json"


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


class Portrait(Gtk.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.settings = read_settings()
        self.events = queue.Queue()
        self.busy = False

    def do_activate(self):
        if hasattr(self, "window"):
            self.window.present()
            return
        self.window = Gtk.ApplicationWindow(application=self, title=APP_NAME)
        self.window.set_default_size(950, 760)
        self.window.set_border_width(12)
        self.repo_entry = Gtk.Entry()
        self.repo_entry.set_text(self.settings.get("repo", os.environ.get("MYSTICGSI_DIR", str(Path.home() / "mysticgsi"))))

        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.set_title(APP_NAME)
        header.set_subtitle("MysticGSI CLI helper")
        self.window.set_titlebar(header)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.window.add(root)
        repo_box = Gtk.Box(spacing=6)
        repo_box.pack_start(Gtk.Label(label="MysticGSI作業フォルダ"), False, False, 0)
        repo_box.pack_start(self.repo_entry, True, True, 0)
        browse = Gtk.Button(label="選択…")
        browse.connect("clicked", self.choose_repo)
        repo_box.pack_start(browse, False, False, 0)
        root.pack_start(repo_box, False, False, 0)

        self.notebook = Gtk.Notebook()
        root.pack_start(self.notebook, True, True, 0)
        self.notebook.append_page(self.build_page(), Gtk.Label(label="ビルド"))
        self.notebook.append_page(self.manage_page(), Gtk.Label(label="管理・出力"))

        log_frame = Gtk.Frame(label="実行ログ")
        log_scroll = Gtk.ScrolledWindow()
        log_scroll.set_min_content_height(155)
        self.log = Gtk.TextView()
        self.log.set_editable(False)
        self.log.set_monospace(True)
        self.log_buffer = self.log.get_buffer()
        log_scroll.add(self.log)
        log_frame.add(log_scroll)
        root.pack_start(log_frame, False, True, 0)
        self.status = Gtk.Label(label="準備完了", xalign=0)
        root.pack_start(self.status, False, False, 0)

        GLib.timeout_add(100, self.poll_events)
        self.window.show_all()
        GLib.idle_add(self.window.present)
        GLib.timeout_add(250, self.first_run)

    def build_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        grid = Gtk.Grid(column_spacing=10, row_spacing=8)
        page.pack_start(grid, False, False, 0)
        self.command = Gtk.ComboBoxText()
        self.command.append_text("build")
        self.command.append_text("rebuild")
        self.command.set_active(0)
        self.command.connect("changed", self.command_changed)
        self.name = Gtk.Entry()
        self.name.set_placeholder_text("例: klein-v816.0.5.0-vgsmixm")
        self.source = Gtk.Entry()
        self.source.set_placeholder_text("ROMのファイルパス、またはHTTP/HTTPS URL")
        self.source_button = Gtk.Button(label="ファイル選択…")
        self.source_button.connect("clicked", self.choose_source)
        source_row = Gtk.Box(spacing=6)
        source_row.pack_start(self.source, True, True, 0)
        source_row.pack_start(self.source_button, False, False, 0)
        self.rom_type = Gtk.Entry()
        self.rom_type.set_text("auto")
        self.rom_type.set_placeholder_text("auto または公式CLIのTYPE[:CUSTOM]")
        self.format = Gtk.ComboBoxText()
        for value in ("ext4", "EROFS / lz4", "EROFS / lz4hc", "EROFS / lzma"):
            self.format.append_text(value)
        self.format.set_active(0)
        self.compress = Gtk.CheckButton(label="--compress（出力ZIPも作成）")
        self.compress.set_active(True)
        self.nodebloat = Gtk.CheckButton(label="--no-debloat（通常削除されるアプリを残す）")
        self.nomerge = Gtk.CheckButton(label="--no-merge（パーティションを統合しない）")
        self.tag = Gtk.Entry()
        self.tag.set_placeholder_text("--add タグ（任意）")
        key_row = Gtk.Box(spacing=6)
        self.avb = Gtk.Entry()
        self.avb.set_placeholder_text("AVB RSA秘密鍵（任意）")
        key_button = Gtk.Button(label="鍵を選択…")
        key_button.connect("clicked", self.choose_key)
        key_row.pack_start(self.avb, True, True, 0)
        key_row.pack_start(key_button, False, False, 0)

        items = [
            ("コマンド", self.command),
            ("ビルド名", self.name),
            ("ROMファイル / URL", source_row),
            ("ROM種別 (--type)", self.rom_type),
            ("出力形式", self.format),
            ("オプション", self.check_options()),
            ("--add タグ", self.tag),
            ("AVB秘密鍵", key_row),
        ]
        for row, (label, widget) in enumerate(items):
            grid.attach(Gtk.Label(label=label, xalign=0), 0, row, 1, 1)
            grid.attach(widget, 1, row, 1, 1)
        grid.set_column_homogeneous(False)
        grid.get_child_at(1, 2).set_hexpand(True)
        grid.get_child_at(1, 7).set_hexpand(True)
        info = Gtk.Label(label="--typeはautoまたはTYPE[:CUSTOM]を指定できます。対応するファームウェアは公式CLIに渡します。ext4は既定形式。EROFSは端末側のカーネル/FSTAB対応が必要です。", xalign=0)
        info.set_line_wrap(True)
        page.pack_start(info, False, False, 4)
        self.run_button = Gtk.Button(label="Portraitで実行")
        self.run_button.connect("clicked", self.run_build)
        page.pack_start(self.run_button, False, False, 0)
        page.set_border_width(8)
        return page

    def check_options(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        box.pack_start(self.compress, False, False, 0)
        box.pack_start(self.nodebloat, False, False, 0)
        box.pack_start(self.nomerge, False, False, 0)
        return box

    def manage_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        row = Gtk.Box(spacing=8)
        for label, callback in (("ビルド一覧（list）", self.list_builds), ("tmpを開く", lambda *_: self.open_dir("tmp")), ("outを開く", lambda *_: self.open_dir("out")), ("出力ファイルをコピー…", self.copy_output)):
            button = Gtk.Button(label=label)
            button.connect("clicked", callback)
            row.pack_start(button, False, False, 0)
        page.pack_start(row, False, False, 0)
        page.pack_start(Gtk.Separator(), False, False, 4)
        note = Gtk.Label(label="cleanは作業フォルダ内のtmp/とout/をすべて削除します。特定のビルドだけではありません。", xalign=0)
        note.set_line_wrap(True)
        page.pack_start(note, False, False, 0)
        clean = Gtk.Button(label="全tmp/outを削除（clean）…")
        clean.set_halign(Gtk.Align.START)
        clean.connect("clicked", self.clean_all)
        page.pack_start(clean, False, False, 0)
        page.pack_start(Gtk.Separator(), False, False, 4)
        help_text = Gtk.Label(label="ファイルピッカーで選んだROMは元の場所に残し、絶対パスを渡します。URLも入力できます。MysticGSI本体は同梱しません。", xalign=0)
        help_text.set_line_wrap(True)
        page.pack_start(help_text, False, False, 0)
        page.set_border_width(8)
        return page

    def repo(self, check=True):
        path = expanded(self.repo_entry.get_text()).resolve()
        if check and not (path.is_dir() and (path / "cli.py").is_file()):
            self.dialog("MysticGSIのcli.pyが見つかりません。作業フォルダを選択してください。", error=True)
            return None
        self.settings["repo"] = str(path)
        save_settings(self.settings)
        return path

    def dialog(self, text, error=False, question=False):
        kind = Gtk.MessageType.QUESTION if question else (Gtk.MessageType.ERROR if error else Gtk.MessageType.INFO)
        buttons = Gtk.ButtonsType.YES_NO if question else Gtk.ButtonsType.CLOSE
        dialog = Gtk.MessageDialog(transient_for=self.window, modal=True, message_type=kind, buttons=buttons, text=text)
        response = dialog.run()
        dialog.destroy()
        return response

    def first_run(self):
        path = expanded(self.repo_entry.get_text())
        if path.is_dir() and (path / "cli.py").is_file():
            self.status.set_text("MysticGSIを確認しました")
        else:
            self.status.set_text("作業フォルダを選択するか、先にMysticGSIをセットアップしてください")
        return GLib.SOURCE_REMOVE

    def choose_repo(self, *_):
        dialog = Gtk.FileChooserDialog(title="MysticGSIフォルダを選択", transient_for=self.window, action=Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "選択", Gtk.ResponseType.OK)
        if dialog.run() == Gtk.ResponseType.OK:
            self.repo_entry.set_text(dialog.get_filename())
        dialog.destroy()

    def choose_source(self, *_):
        dialog = Gtk.FileChooserDialog(title="ROMファイルを選択", transient_for=self.window, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "選択", Gtk.ResponseType.OK)
        if dialog.run() == Gtk.ResponseType.OK:
            self.source.set_text(dialog.get_filename())
        dialog.destroy()

    def choose_key(self, *_):
        dialog = Gtk.FileChooserDialog(title="AVB秘密鍵を選択", transient_for=self.window, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "選択", Gtk.ResponseType.OK)
        if dialog.run() == Gtk.ResponseType.OK:
            self.avb.set_text(dialog.get_filename())
        dialog.destroy()

    def command_changed(self, *_):
        build = self.command.get_active_text() == "build"
        self.source.set_sensitive(build)
        self.source_button.set_sensitive(build)
        self.rom_type.set_sensitive(build)
        self.format.set_sensitive(build)
        self.nodebloat.set_sensitive(build)
        self.nomerge.set_sensitive(build)
        self.tag.set_sensitive(build)

    def append_log(self, text):
        end = self.log_buffer.get_end_iter()
        self.log_buffer.insert(end, text)
        mark = self.log_buffer.create_mark(None, self.log_buffer.get_end_iter(), False)
        self.log.scroll_mark_onscreen(mark)

    def launch(self, args):
        if self.busy:
            self.dialog("別の処理が実行中です。終了後に再度お試しください。")
            return
        repo = self.repo()
        if repo is None:
            return
        python = repo / ".venv/bin/python"
        if not python.is_file():
            python = Path(sys.executable)
        command = [str(python), str(repo / "cli.py"), *args]
        self.busy = True
        self.run_button.set_sensitive(False)
        self.status.set_text("実行中…")
        self.append_log("\n$ " + shlex.join(command) + "\n")

        def worker():
            try:
                proc = subprocess.Popen(command, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
                assert proc.stdout
                for line in proc.stdout:
                    self.events.put(("line", line))
                self.events.put(("done", str(proc.wait())))
            except Exception as exc:
                self.events.put(("error", str(exc)))
        threading.Thread(target=worker, daemon=True).start()

    def poll_events(self):
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "line":
                    self.append_log(value)
                elif kind == "done":
                    self.busy = False
                    self.run_button.set_sensitive(True)
                    code = int(value)
                    self.status.set_text("完了" if code == 0 else f"終了コード {code}")
                    self.append_log(f"\n処理終了（終了コード {code}）\n")
                elif kind == "error":
                    self.busy = False
                    self.run_button.set_sensitive(True)
                    self.dialog(value, error=True)
        except queue.Empty:
            pass
        return GLib.SOURCE_CONTINUE

    def run_build(self, *_):
        repo = self.repo()
        if repo is None:
            return
        name = self.name.get_text().strip()
        if not name:
            self.dialog("ビルド名を入力してください。", error=True)
            return
        cmd = self.command.get_active_text()
        args = [cmd, name]
        if cmd == "build":
            source = self.source.get_text().strip()
            if not source:
                self.dialog("ROMファイルまたはURLを指定してください。", error=True)
                return
            parsed = urlparse(source)
            if not (parsed.scheme in ("http", "https") and parsed.netloc):
                source_path = expanded(source).resolve()
                if not source_path.is_file():
                    self.dialog(f"ファイルが見つかりません:\n{source_path}", error=True)
                    return
                source = str(source_path)
            args.append(source)
            rom_type = self.rom_type.get_text().strip() or "auto"
            if rom_type != "auto":
                args += ["--type", rom_type]
            fmt = self.format.get_active_text()
            if fmt.startswith("EROFS"):
                args += ["--format", fmt.split("/", 1)[1].strip()]
            if self.compress.get_active(): args.append("--compress")
            if self.nodebloat.get_active(): args.append("--no-debloat")
            if self.nomerge.get_active(): args.append("--no-merge")
            if self.tag.get_text().strip(): args += ["--add", self.tag.get_text().strip()]
        elif self.compress.get_active():
            args.append("--compress")
        key = self.avb.get_text().strip()
        if key:
            key_path = expanded(key).resolve()
            if not key_path.is_file():
                self.dialog(f"AVB秘密鍵が見つかりません:\n{key_path}", error=True)
                return
            args += ["--avb-key", str(key_path)]
        self.launch(args)

    def list_builds(self, *_):
        self.launch(["list"])

    def clean_all(self, *_):
        repo = self.repo()
        if repo is None: return
        result = self.dialog(f"{repo / 'tmp'} と {repo / 'out'} の全データを削除します。ビルド成果物もすべて消えます。続行しますか？", question=True)
        if result == Gtk.ResponseType.YES:
            self.launch(["clean", "--yes"])

    def open_dir(self, name):
        repo = self.repo()
        if repo is None: return
        path = repo / name
        path.mkdir(exist_ok=True)
        opener = shutil.which("xdg-open")
        if opener:
            subprocess.Popen([opener, str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            self.dialog("xdg-openが見つかりません。", error=True)

    def copy_output(self, *_):
        repo = self.repo()
        if repo is None: return
        out = repo / "out"
        out.mkdir(exist_ok=True)
        dialog = Gtk.FileChooserDialog(title="out/からコピーする成果物を選択", transient_for=self.window, action=Gtk.FileChooserAction.OPEN)
        dialog.set_current_folder(str(out))
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "選択", Gtk.ResponseType.OK)
        if dialog.run() != Gtk.ResponseType.OK:
            dialog.destroy(); return
        src = Path(dialog.get_filename())
        dialog.destroy()
        save = Gtk.FileChooserDialog(title="コピー先を選択", transient_for=self.window, action=Gtk.FileChooserAction.SAVE)
        save.set_current_name(src.name)
        save.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "コピー", Gtk.ResponseType.OK)
        if save.run() == Gtk.ResponseType.OK:
            dst = Path(save.get_filename())
            try:
                shutil.copy2(src, dst)
                self.append_log(f"コピーしました: {src}\n→ {dst}\n")
                self.status.set_text("出力ファイルをコピーしました")
            except OSError as exc:
                self.dialog(str(exc), error=True)
        save.destroy()


def main():
    app = Portrait()
    return app.run(sys.argv[:1])


if __name__ == "__main__":
    raise SystemExit(main())
