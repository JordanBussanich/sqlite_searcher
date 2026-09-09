# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

import tkinter as tk

from tkinter import ttk, filedialog

from ui.main.controller import MainController
from ui.main.view import MainView

from sqlite_search import *


def initialize() -> None:
    root = tk.Tk()

    controller = MainController()

    view = MainView(root, controller)

    controller.bind_view(view)

    root.mainloop()



if __name__ == "__main__":
    initialize()
