#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from gui.button import Button
from gui.page_window import PageWindow
from gui.state_label import StateLabel


# class ExerciseInfoWindow(PageWindow):
#     def __init__(self):
#         super().__init__()


class ExerciseMainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        self.grid_layout = QtWidgets.QGridLayout(central_widget)

        # Add buttons
        self.buttons = dict()

        # Add state label
        self.state_label = None

    def add_button(self,
        name:str,
        position:int,
        size:int,
        text:str,
        method
    ):
        self.buttons[name] = Button(text, self)
        self.grid_layout.addWidget(
            self.buttons[name],
            1, position,
            1, size,
            alignment=QtCore.Qt.AlignCenter
        )
        self.buttons[name].clicked.connect(
            method(name)
        )

    def add_state_label(self, text:str, position:int, size:int):
        self.state_label = StateLabel(text)
        self.grid_layout.addWidget(
            self.state_label,
            1, position,
            1, size,
            alignment=QtCore.Qt.AlignCenter
        )

    def reset_window(self):
        self.state_label.reset_text()
        for key in self.buttons:
            self.buttons[key].reset_text()


class ExerciseSettingsWindow(PageWindow):
    def __init__(self):
        super().__init__()

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        self.grid_layout = QtWidgets.QGridLayout(central_widget)

        self._settings = dict()
        self.buttons = dict()

    def add_setting(self,
        name:str,
        text:str,
        values:list,
        default_option_index:int,
        setting_method
    ):
        setting_label = QtWidgets.QLabel()
        setting_label.setText(text)
        self.grid_layout.addWidget(
            setting_label,
            len(self._settings) + len(self.buttons), 0,
            alignment=QtCore.Qt.AlignCenter
        )
        setting_list = QtWidgets.QComboBox()
        setting_list.addItems(values)
        setting_list.setCurrentIndex(default_option_index)
        self.grid_layout.addWidget(
            setting_list,
            len(self._settings) + len(self.buttons), 1,
            alignment=QtCore.Qt.AlignCenter
        )
        setting_list.currentIndexChanged.connect(
            setting_method
        )
        self._settings[name] = setting_list
        setting_method()
    
    def get_setting(self, name:str) -> str:
        return self._settings[name].currentText()

    def add_button(self, name:str, text:str, button_method):
        self.buttons[name] = Button(text, self)
        self.grid_layout.addWidget(
            self.buttons[name],
            len(self._settings) + len(self.buttons), 0,
            1, 2,
            alignment=QtCore.Qt.AlignCenter
        )
        self.buttons[name].clicked.connect(
            button_method(name)
        )
