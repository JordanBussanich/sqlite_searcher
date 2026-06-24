# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

import threading

import sqlite_search

#from .view import MainView

class MainController:
    def __init__(self):
        self.view = None
        pass

    def bind_view(self, view):
        self.view = view
    
    
    