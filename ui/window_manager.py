# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C)  2026  Jordan Bussanich

# SQLite Search UI
# Hacked together by Jordan Bussanich

from abc import ABC, abstractmethod

class AbstractWindow(ABC):
    def __init__(
        self, 
        view: AbstractView, 
        controller: AbstractController,
        version: str
    ) -> None:
        self.view = view
        self.controller = controller
        self.version = version

        # Bind the controller/view
        self.view._controller = controller
        self.controller._view = view


    @abstractmethod
    def open(self) -> None:
        pass


class AbstractView(ABC):
    @property
    @abstractmethod
    def controller(self) -> AbstractController:
        pass

    def __init__(self) -> None:
        self._controller: AbstractController


class AbstractController(ABC):
    @property
    @abstractmethod
    def view(self) -> AbstractView:
        pass

    def __init__(self) -> None:
        self._view: AbstractView
