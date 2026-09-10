# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

import threading

import sqlite_search

class MainController:
    def __init__(self) -> None:
        self.view = None
        pass


    def bind_view(self, view) -> None:
        self.view = view
    

    def search(
            self, 
            db_file: str, 
            query: str, 
            is_case_sensitive: bool,
            use_regex: bool
        ) -> None:
        thread = threading.Thread(
            target=lambda: self._search_worker(
                db_file, 
                query, 
                is_case_sensitive,
                use_regex
            ),
            daemon=True
        ).start()
    

    def _search_worker(
            self, 
            db_file: str, 
            query: str, 
            is_case_sensitive: bool,
            use_regex: bool
    ) -> None:
        
        self.view.search_started()

        try:
            searcher: sqlite_search.CellSearcher

            if use_regex:
                searcher = sqlite_search.RegexCellSearcher(query, is_case_sensitive)
            else:
                searcher = sqlite_search.TextCellSearcher(query, is_case_sensitive)
            
            raw_results = sqlite_search.search_sqlite([searcher], db_file)

            results = [
                self.view.ResultsItem(
                    item.table_name,
                    item.search_term,
                    item.column,
                    item.rowid
                )
                for item in raw_results[1]
            ]

            self.view.show_results(results)
        finally:
            self.view.search_finished()
    