# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

import sys
import tkinter as tk

from tkinter import ttk

from .controller import MainController
from .view import MainView

from ..window_manager import AbstractWindow

class MainWindow(AbstractWindow):
    def __init__(self, version: str) -> None:
        self.root = tk.Tk()
        set_theme(self.root)

        view = MainView(self.root, version)
        controller = MainController()
        super().__init__(view, controller, version)
        

    def open(self) -> None:
        self.root.mainloop()


def set_theme() -> None:
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
