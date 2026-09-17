# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

import i18n

from pathlib import Path

from .main.window import MainWindow

from version import __version__


def start() -> None:
    translations_folder = Path(__file__).parent.resolve() / "translations"

    # Uncomment to test it in French
    #i18n.set("locale", "fr")

    i18n.load_path.append(str(translations_folder))

    # Ignores the locale in the root of the JSON files
    i18n.set("skip_locale_root_data", True)

    # namespace maps to the View name so ui/translations/en/<namespace>.json
    i18n.set("filename_format", "{namespace}.{format}")

    # Read the locale from the folder names in ui/translations
    i18n.set("use_locale_dirs", True)

    window = MainWindow(__version__)

    window.open()
