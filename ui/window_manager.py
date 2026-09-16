# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

import tkinter as tk

from abc import ABC, abstractmethod

class AbstractWindow(ABC):
    @abstractmethod
    def open(self) -> None:
        pass

    def __init__(
        self, 
        view: AbstractView, 
        controller: AbstractController,
        top_level: tk.TopLevel
    ) -> None:
        self.view = view
        self.controller = controller
        self.top_level = top_level


class AbstractView(ABC):
    def __init__(self) -> None:
        self._controller: AbstractController


    @property
    @abstractmethod
    def controller(self) -> AbstractController:
        pass


class AbstractController(ABC):
    def __init__(self) -> None:
        self._view: AbstractView


    @property
    @abstractmethod
    def view(self) -> AbstractView:
        pass
