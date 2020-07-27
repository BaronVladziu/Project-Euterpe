#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from gui.page_window import PageWindow


class Button(QtWidgets.QPushButton):
    def __init__(self, text:str, anchor:PageWindow):
        super().__init__(text, anchor)
        self.text = text

    def change_text(self, text:str):
        self.setText(text)

    def reset_text(self):
        self.setText(self.text)
