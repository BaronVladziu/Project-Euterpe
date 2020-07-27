#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


class StateLabel(QtWidgets.QLabel):
    def __init__(self, text:str):
        super().__init__()
        self.text = text
        self.setText(self.text)

    def change_text(self, text:str):
        self.setText(text)

    def reset_text(self):
        self.setText(self.text)
