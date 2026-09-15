# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

import i18n
import tkinter as tk

from pathlib import Path

from ui.main.controller import MainController
from ui.main.view import MainView

from sqlite_search import *
from version import __version__

def initialize() -> None:
    root = tk.Tk()

    translations_folder = Path(__file__).parent.resolve() / "ui" / "translations"

    # Uncomment to test it in French
    i18n.set("locale", "fr")

    i18n.load_path.append(str(translations_folder))

    # Ignores the locale in the root of the JSON files
    i18n.set("skip_locale_root_data", True)

    # namespace maps to the View name so ui/translations/en/<namespace>.json
    i18n.set("filename_format", "{namespace}.{format}")

    # Read the locale from the folder names in ui/translations
    i18n.set("use_locale_dirs", True)

    print(i18n.t("sqlite_file"))

    controller = MainController()

    view = MainView(root, controller, __version__)

    controller.bind_view(view)

    root.mainloop()


if __name__ == "__main__":
    initialize()
