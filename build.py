# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C)  2026  Jordan Bussanich

# This script builds and package the application.
# Hacked together by Jordan Bussanich

import subprocess
import sys

subprocess.check_call([
    sys.executable,
    "-m", "pip", "install",
    "-r", "requirements.txt"
])

subprocess.check_call([
    sys.executable,
    "-m", "pip", "install",
    "-r", "requirements-build.txt"
])

if sys.platform.startswith("win"):
    subprocess.check_call([
        "powershell.exe",
        "-NoProfile",
        "-Command",
        (
            "& 'C:\\Program Files (x86)\\Microsoft Visual Studio\\18\\BuildTools"
            "\\Common7\\Tools\\Launch-VsDevShell.ps1'; "
            f'& "{sys.executable}" -m nuitka '
            "--mode=standalone "
            "--msvc=latest "
            "--windows-console-mode=disable "
            "--enable-plugin=tk-inter "
            "--include-data-dir=ui\\translations=ui\\translations "
            "--include-data-files=pyproject.toml=pyproject.toml "
            '--output-filename="SQLite Searcher.exe" '
            "sqlite_search_ui.py"
        ),
    ])
