# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

import sys
import tkinter as tk
import tkinter.font as tkfont

from dataclasses import dataclass
from tkinter import ttk, filedialog, messagebox
from textwrap import dedent

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


class MainView:
    @dataclass
    class ResultsItem:
        table_name: str
        search_term: str
        column_name: str
        row_id: int
    

    def __init__(self, root: tk.Tk, controller) -> None:    
        self.controller = controller
        
        set_theme(root)

        default_font = tkfont.nametofont("TkDefaultFont")

        self.root = root
        self.root.title("SQLite Searcher UI")
        self.root.geometry("600x600")
        self.root.minsize(600, 600)

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
            height=80
        )

        self.search_query_frame.pack(fill="x")

        self.search_query_frame.grid_propagate(False)

        self.search_query_frame.columnconfigure(0, weight=0)
        self.search_query_frame.columnconfigure(1, weight=0)
        self.search_query_frame.columnconfigure(2, weight=1)

        self.search_query_entry = ttk.Entry(
            self.search_query_frame,
            state="disabled"
        )

        self.search_query_entry.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=8,
            pady=(8, 0)
        )

        self.case_sensitive = tk.BooleanVar(value=False)
        self.case_sensitive_check = ttk.Checkbutton(
            self.search_query_frame,
            text="Case Sensitive",
            variable=self.case_sensitive,
            state="disabled"
        )

        self.case_sensitive_check.grid(
            row=1,
            column=0,
            sticky="w",
            padx=8,
            pady=(8, 0)
        )

        self.use_regex = tk.BooleanVar(value=False)
        self.use_regex_check = ttk.Checkbutton(
            self.search_query_frame,
            text="Use RegEx",
            variable=self.use_regex,
            state="disabled"
        )

        self.use_regex_check.grid(
            row=1,
            column=1,
            sticky="w",
            padx=8,
            pady=(8, 0)
        )
        
        self.search_results_frame = ttk.LabelFrame(
            self.search_frame,
            text="Results"
        )
        
        self.search_results_frame.pack(fill="both", expand="true")

        self.results = ttk.Treeview(
            self.search_results_frame,
            columns=("search_term", "column_name", "rowid"),
            show="tree headings"
        )

        self.results.column("#0", width=100)
        self.results.column("search_term", width=100)
        self.results.column("column_name", width=100)
        self.results.column("rowid", width=50)

        self.results.heading("#0", text="Table")
        self.results.heading("search_term", text="Search Term")
        self.results.heading("column_name", text="Column Name")
        self.results.heading("rowid", text="RowId")

        self.results.tag_configure(
            "bold",
            font=(default_font.actual()["family"], default_font.actual()["size"], "bold")
        )

        self.results.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8,
        )

        # Search button row (maybe some other options here later)***************
        self.search_button_frame = ttk.Frame(self.main_frame)
        self.search_button_frame.pack(fill="x", pady=8)

        self.search_button = ttk.Button(
            self.search_button_frame,
            text="Search",
            command=lambda: self._on_search_click(),
            state="disabled"
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


    def clear_results(self) -> None:
        def callback() -> None:
            self.results.delete(*self.results.get_children())

        self.root.after(0, callback)
    

    def search_started(self) -> None:
        def callback() -> None:
            self.root.config(cursor="wait")
        
        self.root.after(0, callback)


    def search_finished(self) -> None:
        def callback() -> None:
            self.root.config(cursor="")
        
        self.root.after(0, callback)


    def show_results(self, results: list[ResultsItem]) -> None:
        def callback() -> None:
            for table_name in set(result.table_name for result in results):
                table_id = self.results.insert(
                    "",
                    "end",
                    text=table_name,
                    open=True,
                    tags=("bold",)
                )

                for result in sorted(
                    (r for r in results if r.table_name == table_name),
                    key=lambda r: (r.row_id, r.column_name)
                ):
                    self.results.insert(
                        table_id,
                        "end",
                        values=(
                            result.search_term,
                            result.column_name,
                            result.row_id
                        )
                    )
                    

        self.root.after(0, callback) 


    def _on_browse_click(self, entry: ttk.Entry) -> None:
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

            self.search_button.config(state="normal")
            self.search_query_entry.config(state="normal")
            self.case_sensitive_check.config(state="normal")
            self.use_regex_check.config(state="normal")

    
    def _on_search_click(self) -> None:
        self.clear_results()

        self.controller.search(
            self.sqlite_file_entry.get(),
            self.search_query_entry.get(),
            self.case_sensitive.get(),
            self.use_regex.get()
        )


    def _on_clear_click(self) -> None:
        self.clear_results()


    def _on_about_click(self) -> None:
        messagebox.showinfo(
            "About SQLite Searcher UI",
            """SQLite Search Copyright (C) 2023, 2026  Jordan Bussanich
SQLite Search UI Copyright (C) 2026  Jordan Bussanich

This software is licensed under the GNU GPL v2.0 Only licence.

Made in Canada / Fabriqué au Canada""")