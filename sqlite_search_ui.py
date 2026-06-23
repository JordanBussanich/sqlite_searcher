# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

import tkinter as tk

from tkinter import ttk

from sqlite_search import *

def initialize():
    root = tk.Tk()
    
    root.geometry("400x400")

    root.mainloop()

if __name__ == "__main__":
    initialize()