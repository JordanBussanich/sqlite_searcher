# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C)  2026  Jordan Bussanich

# This module manages the version number
# Hacked together by Jordan Bussanich

import sys
import tomllib

from pathlib import Path

base_path: str
if getattr(sys, "frozen", False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).resolve().parent

with open(base_path / "pyproject.toml", "rb") as version_file:
    config = tomllib.load(version_file)

__version__: str = config["project"]["version"]
