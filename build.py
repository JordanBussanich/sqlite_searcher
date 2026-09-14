# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C)  2026  Jordan Bussanich

# This script builds and package the application into a single executable.
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

subprocess.check_call([
    sys.executable,
    "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", "SQLite Searcher",
    "--add-data", "pyproject.toml:.",
    "sqlite_search_ui.py"
])
