# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

import i18n
import sys
import tkinter as tk

from pathlib import Path
from tkinter import ttk

from .main.controller import MainController
from .main.view import MainView
from version import __version__

def set_theme(root: tk.Tk) -> None:
    style = ttk.Style()

    available_themes = set(style.theme_names())

    preferred: list[str] = []
    if sys.platform.startswith("win"):
        preferred = ["vista", "winnative", "xpnative", "clam"]
    
    elif sys.platform == "darwin":
        preferred = ["aqua", "clam"]
    
    else:
        preferred = ["yaru", "adwaita", "clam", "alt", "classic", "default"]
    
    for theme in preferred:
        if theme in available_themes:
            style.theme_use(theme)
            return


def start() -> None:
    root = tk.Tk()

    set_theme(root)

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

    controller = MainController()

    view = MainView(root, controller, __version__)

    controller.bind_view(view)

    root.mainloop()
