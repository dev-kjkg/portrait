# Portrait

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

### The native Linux GUI frontend for [MysticGSI](https://github.com/MysticGSI/mysticgsi) — build Treble GSIs with one click.

[![License](https://img.shields.io/badge/License-Apache--2.0%20%2F%20MIT-blue.svg)](#license)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%2F%20WSL2-green.svg)](#wsl-support)
[![GUI](https://img.shields.io/badge/GUI-PyQt5%20%2F%20Qt%20Widgets-brightgreen.svg)](#installation)
[![MysticGSI](https://img.shields.io/badge/MysticGSI-v2.0%2B-orange.svg)](https://github.com/MysticGSI/mysticgsi)
[![Version](https://img.shields.io/badge/Portrait-v1.2.0-purple.svg)](#version)
[![Target](https://img.shields.io/badge/Android-10%20%E2%86%92%2016%20%28API%2029--37%29-yellow.svg)](#mysticgsi-ecosystem)

[**日本語ドキュメント (Japanese README)**](README_JA.md) · [Issue Tracker](https://github.com/dev-kjkg/portrait/issues) · [Discussions](https://github.com/dev-kjkg/portrait/discussions)

</div>

---

## Table of Contents

- [Overview](#overview)

- [Architecture & Design Principles](#architecture--design-principles)

- [MysticGSI Ecosystem](#mysticgsi-ecosystem)

- [Feature Matrix](#feature-matrix)

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [One-Line Quick Start](#one-line-quick-start)
  - [Step-by-Step Breakdown](#step-by-step-breakdown)
  - [Verifying the Installation](#verifying-the-installation)

- [Setting Up MysticGSI](#setting-up-mysticgsi)

- [GUI Walkthrough](#gui-walkthrough)
  - [First Launch](#first-launch)
  - [Build Tab Reference](#build-tab-reference)
  - [Manage & Output Tab](#manage--output-tab)
  - [Real-time Log Viewer](#real-time-log-viewer)

- [CLI Reference](#cli-reference)

- [Supported ROM Types & Firmware Formats](#supported-rom-types--firmware-formats)

- [WSL & WSLg Guide](#wsl--wslg-guide)

- [Flashing & Device-Side Guide](#flashing--device-side-guide)

- [Configuration & Environment](#configuration--environment)

- [Troubleshooting & FAQ](#troubleshooting--faq)

- [Uninstallation](#uninstallation)

- [Contributing](#contributing)

- [License & Credits](#license--credits)

---

## Overview

**Portrait** is a native Linux GUI (PyQt5 / Qt Widgets) for [MysticGSI](https://github.com/MysticGSI/mysticgsi), the modern tool that ports stock Android vendor firmware into Project Treble–compatible **Generic System Images (GSIs)**.

Building a GSI normally requires juggling MysticGSI's official `cli.py` flags — ROM type, filesystem format, AVB keys, compression, tag modifiers — inside a virtual environment. Portrait wraps the entire official CLI in an intuitive, two-tab desktop app, **without modifying or forking MysticGSI**:

- **Point-and-click builds**: select a local ROM archive or paste a download URL, tweak any official flag, and hit *“Portraitで実行”* (Run with Portrait).

- **Zero-copy safety**: your ROM file is never moved or duplicated; Portrait passes its absolute path safely through a proper argument array (immune to spaces and shell-injection).

- **No privilege escalation in-app**: sudo operations (package installs, MysticGSI setup) are never run inside the GUI — Portrait gives you exact copy-paste commands for your own terminal.

- **Full CLI parity**: Portrait also installs a `portrait` command so you can keep working from the terminal if you prefer, with automatic relative-to-absolute path resolution.

- **WSL-first**: built-in detection for WSL2/WSLg with automatic `xcb` platform selection, software rendering, and display checks.

> **Important**: Portrait is **not** a MysticGSI fork and contains **no ROM processing code**. It invokes MysticGSI's official `cli.py` binary via `QProcess` or bash. All ROM compatibility, patches, and build results are produced by upstream MysticGSI.

---

## Architecture & Design Principles

```
  ┌─────────────────────────────────────────────────────────────┐
  │                         User Layer                          │
  │     [Portrait Qt Widgets GUI]       [portrait CLI wrapper]   │
  │     (portrait_qt.py)                (bash launcher)         │
  └──────────────────────────┬──────────────────────────────────┘
                             │  QProcess / exec
                             ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                 MysticGSI (upstream, untouched)             │
  │    ~/mysticgsi/cli.py  ◄── run via .venv/bin/python          │
  │         │                                                   │
  │         ├─► extract_firmware (aria2c / 7z / libarchive / …)  │
  │         ├─► unpack_partitions (simg2img / lpunpack / …)     │
  │         ├─► patch pipeline (SELinux / Treble / vendors)     │
  │         ├─► make image (mke2fs / mkfs.erofs)                │
  │         ├─► AVB sign (avbtool RSA)                          │
  │         └─► compress (.zip)                                 │
  │                                                             │
  │    tmp/<build>/                out/<build>/                 │
  │    ├── images/ (raw trees)     ├── <name>.img               │
  │    ├── payload extracts        ├── <name>.zip               │
  │    └── gsilist.json            └── output.txt (build info)  │
  └─────────────────────────────────────────────────────────────┘
```

| Principle | How Portrait Implements It |
| --- | --- |
| **Non-invasive** | Does not touch MysticGSI sources; all communication happens through official `cli.py` arguments and files. |
| **Zero-copy** | ROM files are referenced by resolved absolute path (`os.path.realpath`). A 6 GB firmware file is neither copied nor moved. |
| **Separation of privileges** | No `sudo` inside the GUI. Package installation & setup are delegated to the user's terminal where sudo prompts are safe. |
| **Concurrency safety** | GUI prevents overlapping builds (`QProcess` state guard); MysticGSI itself adds `buildlock.py` mutex. |
| **Portability** | Respects `$MYSTICGSI_DIR`, `$XDG_CONFIG_HOME`, `~/.config/portrait/settings.json`, and PATH conventions. |

---

## MysticGSI Ecosystem

For those new to the GSI scene: **Project Treble** (Android 8.0 Oreo and above) separated the Android OS framework (`system`) from vendor-specific drivers (`vendor`). A **Generic System Image** replaces the stock system partition while keeping OEM vendor blobs, allowing you to run, say, HyperOS on a OnePlus phone or One UI on a Xiaomi device.

[MysticGSI](https://github.com/MysticGSI/mysticgsi) is an AOSP/OEM stock ROM → GSI porter written in Python (3.10+). It unpacks OEM firmware, runs a deep **patch pipeline** (SELinux policy cleanup, Treble compatibility fixes, apex configuration, USB debugging forced on, AB-file stripping), rebuilds the filesystem image, and signs it with AVB 2.0. Portrait is the official GUI companion layer for it.

### Android Version Coverage

MysticGSI ships versioned patch trees from **Android 10 (API 29)** through **Android 16+ (API 37 / Baklava / CinnamonBun / CANARY)**. If the ROM you are porting is based on any of these releases, MysticGSI's patch pipeline can handle it.

---

## Feature Matrix

| Feature | CLI (`portrait`) | GUI (`portrait --gui`) | Upstream mysticgsi |
| --- | --- | --- | --- |
| `build` new GSI | ✔ | ✔ | ✔ |
| `rebuild` from edited `tmp/<build>/images` | ✔ | ✔ | ✔ |
| `list` recorded builds (`gsilist.json`) | ✔ | ✔ | ✔ |
| `clean` all `tmp/` + `out/` (with confirmation) | ✔ | ✔ | ✔ |
| `--type TYPE[:CUSTOM]` ROM override | ✔ | ✔ | ✔ |
| ext4 vs EROFS (`lz4` / `lz4hc` / `lzma`) | ✔ | ✔ | ✔ |
| `--compress` (ZIP output) | ✔ | ✔ | ✔ |
| `--no-debloat` (preserve stock apps) | ✔ | ✔ | ✔ |
| `--no-merge` (split `system`/`product`/… images) | ✔ | ✔ | ✔ |
| `--avb-key <PEM>` custom signing key | ✔ | ✔ | ✔ |
| `--add <tag>` build name tag | ✔ | ✔ | ✔ |
| Local ROM file picker | — | ✔ | — |
| HTTP/HTTPS ROM URL (aria2c accelerated) | ✔ | ✔ | ✔ |
| Relative-path auto-resolution (no copying) | ✔ | ✔ | — |
| Real-time merged log streaming | — | ✔ | — |
| Open `tmp/` & `out/` in file manager | — | ✔ | — |
| Copy artifacts to any destination | — | ✔ | — |
| Saved repo location | ✔ | ✔ | — |
| ASCII art logo & version banner | ✔ | — | — |
| WSL / WSLg auto-detection & tuning | ✔ | ✔ | — |
| Desktop app entry & clean uninstaller | ✔ | — | — |

---

## Installation

### Prerequisites

| Component | Requirement | Notes |
| --- | --- | --- |
| OS | Ubuntu 22.04 / 24.04 (native or WSL2), Debian 12, or derivatives | openSUSE / Arch / Fedora also viable for MysticGSI; Portrait installer is debian-apt-targeted |
| Python | 3.10 or newer | Bundled with Ubuntu 22.04+ |
| Shell | bash (not sh) | Installer explicitly validates `$BASH_VERSION` |
| privileges | **normal user** | Do **not** run `install.sh` as root / with `sudo` |

### One-Line Quick Start

```bash
git clone https://github.com/dev-kjkg/portrait.git && bash portrait/install.sh && hash -r && sudo apt update && sudo apt install -y python3-pyqt5 && portrait --gui
```

### Step-by-Step Breakdown

The official, recommended install flow:

```bash
# 1. Clone the Portrait repository
git clone https://github.com/dev-kjkg/portrait.git

# 2. Run the installer AS A NORMAL USER (never 'sh' or 'sudo sh')
bash install.sh

# 3. Refresh Bash's command-location hash table
hash -r

# 4. Update apt indexes
sudo apt update

# 5. Install PyQt5 (the Qt Widgets bindings Portrait runs on)
sudo apt install python3-pyqt5

# 6. Launch the GUI
portrait --gui
```

> **Why ****`hash -r`****?**The installer drops the `portrait` binary into `~/.local/bin`. On many Ubuntu installs this directory is in your `PATH` only if it existed when you logged in, or the installer adds it to `~/.bashrc` / `~/.profile`. Either way, Bash caches known command locations; `hash -r` clears that cache so Bash immediately finds the new binary in the **current** terminal without a reboot. If your shell still cannot find it, run `source ~/.bashrc` once.

> **Why PyQt5 separately via apt?**`install.sh` deliberately contains **no ****`sudo`**** operations** so it can be audited and run safely as an unprivileged user. GUI libraries are installed explicitly via `sudo apt` — Portrait never tries to escalate privileges silently.

### Filesystem Layout After Installation

```
~/.local/
├── bin/
│   └── portrait                    # Main CLI launcher (executable)
├── opt/
│   └── portrait/
│       ├── portrait_qt.py          # Native PyQt5 GUI application
│       ├── run_portrait.sh         # WSL-aware launcher (checks Qt deps)
│       └── README.md               # Embedded docs
└── share/
    └── applications/
        └── portrait.desktop        # Application menu entry ("Portrait")

~/.config/portrait/
└── settings.json                   # Saved MysticGSI repo path
```

PATH integration: `install.sh` appends `export PATH="$HOME/.local/bin:$PATH"` to `~/.profile` and `~/.bashrc` (guarded by the `# Portrait local-bin PATH` marker so it is only added once and cleanly removed by the uninstaller).

### Verifying the Installation

```bash
portrait version
```

Expected output: Portrait's Android-robot ASCII art and:

```
Portrait CLI 1.2.0 — MysticGSI helper
```

```bash
# Verify Qt Widgets availability:
python3 -c 'from PyQt5.QtCore import QT_VERSION_STR; from PyQt5.QtWidgets import QApplication; print("Qt:", QT_VERSION_STR)'
```

---

## Setting Up MysticGSI

Portrait requires a MysticGSI checkout. The default location is **`~/mysticgsi`**.

### Official Automatic Setup

```bash
# 1. Base tools for cloning and device communication
sudo apt update && sudo apt install -y python3 git adb fastboot

# 2. Clone MysticGSI
git clone https://github.com/MysticGSI/mysticgsi.git ~/mysticgsi

# 3. Run MysticGSI's official host-setup script
cd ~/mysticgsi && ./setup_host.py
```

`setup_host.py` automatically installs MysticGSI's remaining build dependencies on Debian/Ubuntu — **curl, aria2, openssl, patch, ca-certificates, libarchive-tools, and a headless JRE** (required by the bundled Apktool) — and creates the `.venv` virtual environment MysticGSI's CLI runs inside.

Portrait's GUI also has a **“セットアップ手順”** (Setup Instructions) button on the main toolbar that prints exactly these commands for copy-pasting.

---

## GUI Walkthrough

Launch the GUI:

```bash
portrait --gui
```

### First Launch

On startup, Portrait looks for MysticGSI in this order:

1. `$MYSTICGSI_DIR` environment variable

1. `~/.config/portrait/settings.json` (saved from a previous session)

1. `~/mysticgsi` (the default)

Point **“MysticGSI作業フォルダ”** at your checkout root (the directory containing `cli.py`). The choice is persisted to `~/.config/portrait/settings.json`, so you only need to configure it once.

### Build Tab Reference

The **ビルド** tab is where GSI builds are configured:

| Field | Description | MysticGSI CLI equivalent |
| --- | --- | --- |
| **コマンド** | `build` (fresh port) or `rebuild` (re-assemble after editing `tmp/<name>/images`) | `build` / `rebuild` |
| **ビルド名** | Short internal build identifier. Drives `tmp/<name>` and `out/<name>` | `<name>` positional argument |
| **ROMファイル / URL** | Local archive via file picker (any file) or direct HTTP/HTTPS URL | `<source>` argument |
| **ROM種別 (****`--type`****)** | `auto` by default; or any official vendor type, optionally `TYPE:CUSTOMNAME` | `--type <type>` |
| **出力形式** | `ext4` (default), `EROFS / lz4`, `EROFS / lz4hc`, `EROFS / lzma` | `--format <comp>` (omitted for ext4) |
| **--compress** | Also pack the output into a `.zip` containing `<partition>.img` entries (enabled by default) | `--compress` |
| **--no-debloat** | Keep OEM apps the patch set would otherwise strip (see [Debloat details](#the-no-debloat-flag)) | `--no-debloat` |
| **--no-merge** | Output separate partition images instead of folding them into `system` | `--no-merge` |
| **--add タグ** | Free-form label appended to the build display name | `--add <tag>` |
| **AVB秘密鍵** | Custom RSA PEM private key for signing (picker filters `*.pem`) | `--avb-key <pem>` |

#### Naming conventions

MysticGSI generates output files named like:

```
<ROM_NAME>-<device_codename>-<android_version>-<incremental>-AB-<YYYYMMDD>-MysticGSI.img
```

Picking a clean, unique build name such as `hyperos-12tpro` or `oneui-s23fe` keeps `out/` organized. MysticGSI enforces a safe-name regex (`^[A-Za-z0-9._-]{1,64}$`) on the build name.

#### The `--no-debloat` flag

MysticGSI's patch pipeline unconditionally strips certain troublesome OEM components: the **Dolphin** library (known to crash `surfaceflinger` on some vendor trees), **Dirac** audio services, and Qualcomm's `com.qualcomm.location`. Passing `--no-debloat` preserves these (except the unconditional removals listed above). Enable it when you suspect stripped OEM features are causing boot issues or when you genuinely need stock vendor apps.

#### The `--no-merge` flag

Modern OEMs split UI and vendor apps across `system_ext`, `product`, `my_bigball`, `mi_ext`, etc. By default, MysticGSI merges eligible partitions into the single `system` GSI image so a one-line `fastboot flash system` works on older devices. `--no-merge` leaves them separate and produces `*-system.img`, `*-product.img`, etc. Use this for devices whose `fstab` already mounts individual dynamic partitions — it keeps the ROM closer to the stock layout.

#### Output format: ext4 vs EROFS

| Format | Pros | Cons | Notes |
| --- | --- | --- | --- |
| **ext4** (default) | Boots on virtually all devices | Largest images | MysticGSI auto-sizes images ~5% above content size |
| **EROFS / lz4** | ~30–50% smaller, ultra-fast decompression | Needs EROFS-enabled kernel | Recommended EROFS choice for daily use |
| **EROFS / lz4hc** | Better compression than lz4 | Slower to compress | Still fast to read |
| **EROFS / lzma** | Smallest image | Slowest; needs `CONFIG_EROFS_FS_ZIP_LZMA` | Best for space-critical devices |

> **Requirement**: your target device's kernel must have `CONFIG_EROFS_FS` enabled and the vendor `fstab` must mount partitions with `erofs`. Check with `cat /proc/filesystems | grep erofs` on the device (root required).

#### AVB Signing

By default, MysticGSI signs images using the **AOSP AVB RSA-2048 test key**. If you maintain your own signing key (recommended if you disable `vbmeta` verification per-build or use a custom AVB key), point the **AVB秘密鍵** field at your `key.pem`.

### Manage & Output Tab

The **管理・出力** tab handles artifacts and maintenance:

| Button | Action |
| --- | --- |
| **ビルド一覧（list）** | Prints the history from `tmp/gsilist.json`, with `(missing)` marks for deleted images |
| **tmpを開く** | Opens `tmp/` in your file manager (`xdg-open` via `QDesktopServices`) |
| **outを開く** | Opens `out/` in your file manager |
| **出力ファイルをコピー…** | Picks a `.img` or `.zip` from `out/` and copies it (e.g. to `~` or your SD card) **without touching the original** |
| **全tmp/outを削除（clean）…** | Runs MysticGSI's `clean` after an **explicit confirmation dialog** listing the exact paths about to be removed |

> ⚠️ **`clean`**** is a nuclear option**: it removes **every entry under ****`tmp/`**** and ****`out/`** in the MysticGSI working directory, not just a single build. Portrait shows a confirmation dialog explicitly naming both directories before executing. If you only want to free space for one build, delete its folders manually or use the file-manager buttons above.

### Real-time Log Viewer

Build output (progress percentage, stage names, extraction logs, patch steps, `mke2fs` progress, AVB signing) streams live into the monospace log panel, with merged stdout/stderr and a 3,000-line buffer. Stages you will see, in order:

1. `extract` — unpacking the firmware archive via the best available extractor

1. `unpack` — unpacking filesystem partitions (`simg2img`, `lpunpack`, EROFS/ext4 extractors)

1. `patch` — vendor detection, SELinux policy cleanup, Treble fixes, framework hooks

1. `prepare` — dynamic-partition merge (or separation)

1. `mke2fs` / mkfs.erofs — final filesystem generation

1. `sign` — AVB signing with RSA key

1. `done` — summary printed, build logged to `tmp/gsilist.json`

The status label and window status bar reflect the current stage and final exit code (`0` = success).

---

## CLI Reference

`portrait` installed at `~/.local/bin/portrait` mirrors MysticGSI's official CLI while adding safety ergonomics:

```
Portrait — MysticGSI command helper

Usage:
  portrait build <name> <firmware|URL> [MysticGSI options...]
  portrait rebuild <name> [--compress] [--avb-key <pem>]
  portrait list
  portrait clean
  portrait --gui
  portrait version
  portrait uninstall [--purge]
```

### Examples

**Standard build from a local MIUI fastboot ZIP:**

```bash
cd ~/Downloads
portrait build miui-note13 \
  miui_KLEINGlobal_V816.0.5.0.VGSMIXM_96c116ff32_15.0.zip \
  --type miui --compress
```

Notice: no need to move the ZIP or `cd` into the MysticGSI repo. Relative paths are converted to absolute automatically; MysticGSI itself always runs from its repo root, so `tmp/` and `out/` stay grouped there.

**Build directly from an HTTP URL (aria2c accelerated):**

```bash
portrait build raven \
  https://dl.google.com/dl/android/aosp/raven-up1a.231105.003-factory-76a795d5.zip \
  --type pixel --compress
```

**Rebuild after manual edits to ****`tmp/mybuild/images`****:**

```bash
# edit something under ~/mysticgsi/tmp/mybuild/images/system/...
portrait rebuild mybuild --compress
```

**Custom AVB key and EROFS output:**

```bash
portrait build hyperos-tpro ~/firmware/os.zip \
  --type hyperos \
  --format lz4 \
  --avb-key ~/.keys/my_avb.pem \
  --compress
```

**Selecting a non-default MysticGSI repo:**

```bash
export MYSTICGSI_DIR="$HOME/projects/mysticgsi"
portrait list
```

**Launch the GUI:**

```bash
portrait --gui
```

---

## Supported ROM Types & Firmware Formats

### Vendor Types (`--type`)

MysticGSI's patch engine ships vendor-specific hook modules. Portrait lets you enter any of them or rely on **`auto`** detection:

| `--type` value | Vendor / ROM family | Key properties |
| --- | --- | --- |
| `pixel` | Google Pixel factory images | AVB/vbmeta signed |
| `alos` | AOSP / ALOS generic base | reference implementation |
| `miui` | Xiaomi MIUI 12–14 | `ro.miui.ui.version.name` |
| `hyperos` | Xiaomi HyperOS 1.x–2.x+ | `ro.mi.os.version.incremental`, `mi_ext` support |
| `joyui` | Black Shark JOYUI | Xiaomi-derived gaming skin |
| `oneui` | Samsung One UI (Galaxy stock TAR) | `ro.build.version.oneui` |
| `coloros` | OPPO ColorOS | `ro.build.version.oplusrom` (oppo) |
| `oxygenos` | OnePlus OxygenOS | `ro.build.version.oplusrom` (oneplus) |
| `realmeui` | Realme Realme UI | `ro.build.version.oplusrom` (realme) |
| `emui` | Huawei EMUI | `UPDATE.APP` firmware |
| `magicos` | Honor MagicOS | `product_h` + `hw_product` props |
| `harmonyos` | Huawei HarmonyOS | Huawei proprietary stack |
| `zui` | Lenovo ZUI | Lenovo phones & tablets |
| `nothing` | Nothing OS | `ro.nothing.version.id` (preserves `update_engine`) |
| `myos` | ZTE MyOS | ZTE flagships |
| `redmagic` | Nubia RedMagic OS | ZTE gaming line |
| `nebulaos` | ZTE NebulaOS | ZTE midrange |
| `auto` | Automatic heuristic detection (default) | scans build props listed above |

**Auto-detected custom ROMs**: LineageOS (`ro.lineage.build.version`), Evolution X, crDroid, Pixel Experience, Project Blaze, RisingOS, VoltageOS.

**Custom naming syntax**: `--type pixel:custom` (or `TYPE:CUSTOMNAME`) overrides the build's displayed variant tag while reusing the vendor's patch hook.

### Supported Firmware Archives

MysticGSI accepts virtually every stock firmware packaging ever shipped:

- **full OTA ZIPs** containing `payload.bin` (modern Pixel, OnePlus, Nothing, Xiaomi, Motorola…)

- **fastboot ROM packages** (Xiaomi `.tgz`, etc.)

- **`super.img`** and **sparse images** (`simg2img` conversion built-in)

- **`system.new.dat`**** / ****`system.new.dat.br`** legacy OTA formats

- **Samsung ****`.tar`**** / ****`.tar.md5`** firmware

- **Huawei ****`UPDATE.APP`** packages

- **Unisoc ****`.pac`** firmware (spreadtrum SoC devices)

- **LG ****`.kdz`** firmware

- **OPPO ****`.ozip`** (encrypted Oppo ROMs)

- **QFIL packages** (Qualcomm flash files)

- **Sony ****`.sin`** images

- **Pixel factory images** (`image-*.zip`)

Partitions inside may be **ext4, EROFS, or F2FS**.

---

## WSL & WSLg Guide

Portrait was built with WSL2 in mind. On a stock **Ubuntu WSL** instance, the launcher (`run_portrait.sh` and `portrait_qt.py`) automatically applies the correct Qt platform parameters:

```bash
export QT_QPA_PLATFORM="${PORTRAIT_QT_PLATFORM:-xcb}"
export LIBGL_ALWAYS_SOFTWARE=1
export QT_X11_NO_MITSHM=1
export DISPLAY="${DISPLAY:-:0}"
```

### WSLg checklist

WSLg (Windows 11, or Windows 10 build 19044+ with the latest WSL update) provides a built-in Wayland/X11 display server. After installing Portrait, run:

```bash
# 1. Smoke-test Qt import
python3 -c 'from PyQt5.QtCore import QT_VERSION_STR; from PyQt5.QtWidgets import QApplication; print("PyQt/Qt:", QT_VERSION_STR)'

# 2. Confirm a display is available
echo "DISPLAY=$DISPLAY"
echo "WAYLAND_DISPLAY=$WAYLAND_DISPLAY"
```

If `DISPLAY` is empty, **update WSL from PowerShell** and restart it:

```
wsl --update
wsl --shutdown
```

Then re-open Ubuntu and launch `portrait --gui`.

### WSL1 / third-party X servers

On WSL1 or when running a custom X server (VcXsrv, Xming, vcXsrv with `--no-render`), make sure `DISPLAY` is exported pointing at the Windows host (`export DISPLAY=$(ip route show default | awk '{print $3}'):0`) and disable access control in the X server (`-ac` flag).

### Overriding the Qt platform

```bash
PORTRAIT_QT_PLATFORM=xcb portrait --gui
```

---

## Flashing & Device-Side Guide

> **Disclaimer**: Portrait only **builds** GSIs — it never interacts with a device and never flashes anything. Flashing third-party firmware may brick your device, void your warranty, or trip Knox/bootloader fuses. Always back up the stock boot/vendor/recovery partitions first.

### Generic `fastbootd` flashing flow (Android 10+ dynamic partitions)

```bash
# 1. Boot into fastbootd (NOT bootloader!)
adb reboot fastboot

# 2. Disable AVB verification if your vendor bootloader requires it
fastboot flash vbmeta --disable-verity --disable-verification /path/to/stock/vbmeta.img

# 3. Flash the GSI
fastboot flash system /path/to/out/<name>/<output>.img

# 4. Factory reset (mandatory for first boot)
fastboot -w

# 5. Reboot into the new GSI
fastboot reboot
```

### Checklist before flashing

| Check | Why it matters |
| --- | --- |
| Device reports Treble support | `adb shell getprop ro.treble.enabled` should return `true` |
| `ro.product.cpu.abilist` | If Portrait's build summary warns about **32-bit-only programs** in the ROM, a 64-bit-only device may fail to boot those components |
| ARM architecture warning | MysticGSI scans `init`, `linker64`, `surfaceflinger`, etc. for newer ARM instructions and logs a warning if found — old arm64-v8a cores may bootloop |
| EROFS support | If you built with `--format`, verify `cat /proc/filesystems \| grep erofs` on the device |
| Separate partitions | If you used `--no-merge`, flash `system`, `product`, `system_ext`, … each to its slot |
| Overlay / audio / camera fixes | Install **Phhusson's Treble App** (or TrebleDroid settings) post-boot for per-vendor quirks |

---

## Configuration & Environment

| Variable / File | Purpose | Default |
| --- | --- | --- |
| `$MYSTICGSI_DIR` | Absolute path of the MysticGSI checkout | unset (falls back to saved config, then `~/mysticgsi`) |
| `$PORTRAIT_QT_PLATFORM` | Qt QPA platform override | `xcb` on WSL |
| `$XDG_CONFIG_HOME` | Base config directory | `~/.config` |
| `~/.config/portrait/settings.json` | Persistent settings (GUI repo path) | created on first GUI run |
| `$PORTRAIT_APP_DIR` | App install root for standalone runs | `~/.local/opt/portrait` |

Example `settings.json`:

```json
{
  "repo": "/home/user/mysticgsi"
}
```

---

## Troubleshooting & FAQ

### `Portrait: MysticGSI cli.py not found`

MysticGSI is not installed at the expected path. Either clone it to `~/mysticgsi` or export `MYSTICGSI_DIR=/path/to/mysticgsi`.

### `Portrait: MysticGSI virtualenv not found`

The `.venv` virtual environment inside the MysticGSI checkout is missing. Run:

```bash
cd /path/to/mysticgsi && ./setup_host.py
```

### `command not found: portrait`

`~/.local/bin` is not yet in your current shell's PATH. Run `hash -r` and `source ~/.bashrc`.

### `could not connect to display` / `No Qt platform plugin could be initialized`

See [WSL & WSLg Guide](#wsl--wslg-guide). On WSL2, run `wsl --update` then `wsl --shutdown` from PowerShell. On native Linux, verify `echo $DISPLAY` is set (usually `:0`).

### Build fails during `mke2fs` or `mkfs.erofs`

Native image tools are bundled with MysticGSI under `tools/bin/<platform>/<arch>`, but the EROFS path requires `mkfs.erofs` on PATH. On Ubuntu:

```bash
sudo apt install erofs-utils
```

### `waiting for another build to finish...`

MysticGSI uses a file lock (`buildlock.py`) to prevent parallel builds colliding in `tmp/`. If a previous build crashed, remove the stale lock file in the MysticGSI root or wait for the other build to complete.

### Aria2 errors when passing a URL

Install the accelerated downloader:

```bash
sudo apt install aria2
```

### Disk space warning

A single build may use **15–30 GB** inside `tmp/` (raw unpacked partition trees, payloads). If builds fail mysteriously midway through `mke2fs`, run `df -h` to check available space. Use Portrait's **clean** button when previous builds are no longer needed.

### Does Portrait work on Wayland natively?

Yes — you can force the Wayland platform: `QT_QPA_PLATFORM=wayland portrait --gui` (requires `qtwayland5`). The default on WSL is `xcb` because WSLg's XWayland bridge is the most widely compatible.

---

## Uninstallation

```bash
portrait uninstall
```

You will be prompted to type `yes`. The uninstaller removes:

- `~/.local/bin/portrait`

- `~/.local/share/applications/portrait.desktop`

- `~/.local/opt/portrait/`

- The PATH export lines `# Portrait local-bin PATH` added to `~/.profile` and `~/.bashrc`

**MysticGSI itself, your ROM files, and all build outputs (****`out/`****, ****`tmp/`****) are untouched.**

To also delete Portrait's settings file (`~/.config/portrait`), use:

```bash
portrait uninstall --purge
```

---

## Contributing

Issues, bug reports, and pull requests are welcome at [dev-kjkg/portrait](https://github.com/dev-kjkg/portrait):

1. Fork the repo and create a feature branch (`git checkout -b feature/xyz`)

1. Keep `portrait_qt.py` and `portrait` compatible with Python 3.10+ / Qt 5 and bash

1. Test both the CLI and the GUI before opening a PR

1. For issues with ROM extraction, patch failures, or filesystem corruption, report upstream to [MysticGSI/mysticgsi](https://github.com/MysticGSI/mysticgsi/issues) instead

## License & Credits

- **Portrait**: Copyright (c) 2024–2026 dev-kjkg. Distributed under the **Apache License 2.0** (with MIT-compatible CLI scripts).

- [**MysticGSI**](https://github.com/MysticGSI/mysticgsi): upstream tool, Apache License 2.0.

- **Qt / PyQt5**: Riverbank Computing / The Qt Company (GPL v3 / LGPL v3).

- **avbtool**: MIT License (bundled with MysticGSI).

- Special thanks to the **Project Treble**, **XDA Developers**, and GSI-porting communities for keeping Android open and flashable.

---

<div align="center">

[**Portrait**](https://github.com/dev-kjkg/portrait)** — Making Treble GSI builds as effortless as they should be.**

*Star the repo if it saved you a terminal command!*

</div>
