# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

import sys
import tkinter as tk

from tkinter import ttk, filedialog

#from controller import MainController

def set_theme(root: tk.Tk):
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


class MainView:
    def __init__(self, root: tk.Tk, controller):    
        self.controller = controller
        
        self.root = root
        self.root.title("SQLite Searcher UI")
        self.root.geometry("400x400")

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=12, pady=12, fill="both", expand="true")

        # Open File Row*********************************************************
        self.open_file_frame = ttk.Frame(self.main_frame)
        self.open_file_frame.pack(fill="x", pady=8)

        self.browse_box_label = ttk.Label(
            self.open_file_frame, 
            text="SQLite File"
        )
        self.browse_box_label.pack(side="left")

        self.sqlite_file_entry = ttk.Entry(
            self.open_file_frame,
            state="readonly"
        )
        self.sqlite_file_entry.pack(side="left", fill="x", expand=True, padx=8)
        
        self.browse_button = ttk.Button(
            self.open_file_frame,
            text="Browse...",
            command=lambda: self._on_browse_click(self.sqlite_file_entry)
        )
        self.browse_button.pack(side="left")

        # Search Options / Results Frame****************************************
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(
            pady=8,
            fill="both",
            expand="true"
        )

        self.search_query_frame = ttk.LabelFrame(
            self.search_frame,
            text="Search Query",
            height = 120
        )

        self.search_query_frame.pack(fill="x")

        self.search_query_frame.pack_propagate(False)

        self.search_results_frame = ttk.LabelFrame(
            self.search_frame,
            text="Results"
        )

        self.search_results_frame.pack(fill="both", expand="true")

        # Search button row (maybe some other options here later)***************
        self.search_button_frame = ttk.Frame(self.main_frame)
        self.search_button_frame.pack(fill="x", pady=8)

        self.search_button = ttk.Button(
            self.search_button_frame,
            text="Search",
            command=lambda: self._on_search_click()
        )
        self.search_button.pack(side="right")

        self.clear_button = ttk.Button(
            self.search_button_frame,
            text="Clear",
            command=lambda: self._on_clear_click()
        )

        self.clear_button.pack(side="right", padx=8)

        self.about_button = ttk.Button(
            self.search_button_frame,
            text="About",
            command=lambda: self._on_about_click()
        )
        self.about_button.pack(side="left")


    def _on_browse_click(self, entry: ttk.Entry):
        file_path = filedialog.askopenfilename(
            title="Open SQLite Database...",
            filetypes=[
                ("SQLite Database", "*.db *.sqlite *.sqlite3 *.sqlitedb"), 
                ("All files", "*.*")
            ]
        )

        if file_path:
            # For whatever reason tk uses a forward slash as the folder 
            # separator even on Windows.
            if sys.platform.startswith("win"):
                file_path = file_path.replace('/', '\\')
            
            self.sqlite_file_entry.configure(state="normal")
            self.sqlite_file_entry.delete(0, tk.END)
            self.sqlite_file_entry.insert(0, file_path)
            self.sqlite_file_entry.configure(state="readonly")

    
    def _on_search_click(self):
        pass

    def _on_clear_click(self):
        pass

    def _on_about_click(self):
        pass
