#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from gui.button import Button
from gui.page_window import PageWindow
from gui.state_label import StateLabel
from gui.style import Style


class ExerciseInstructionWindow(PageWindow):
    def __init__(self,
        instruction:str,
        back_button_name:str,
        forward_button_name:str,
        button_method
    ):
        super().__init__()
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        self.grid_layout = QtWidgets.QGridLayout(central_widget)
        central_widget.setStyleSheet(Style.get_window_style())

        self.label = QtWidgets.QLabel()
        self.label.setText(instruction)
        self.grid_layout.addWidget(
            self.label,
            0, 0,
            1, 2,
            QtCore.Qt.AlignCenter
        )
        self.label.setStyleSheet(Style.get_text_style())

        self.back_button = Button("Back", self)
        self.grid_layout.addWidget(
            self.back_button,
            1, 0,
            1, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.back_button.setStyleSheet(Style.get_button_style())
        self.back_button.clicked.connect(
            button_method(back_button_name)
        )

        self.forward_button = Button("Ok", self)
        self.grid_layout.addWidget(
            self.forward_button,
            1, 1,
            1, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.forward_button.setStyleSheet(Style.get_button_style())
        self.forward_button.clicked.connect(
            button_method(forward_button_name)
        )


class ExerciseMainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        self.grid_layout = QtWidgets.QGridLayout(central_widget)
        central_widget.setStyleSheet(Style.get_window_style())

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
        self.buttons[name].setStyleSheet(Style.get_button_style())
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
        self.state_label.setStyleSheet(Style.get_text_style())

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
        central_widget.setStyleSheet(Style.get_window_style())

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
        setting_label.setStyleSheet(Style.get_text_style())
        setting_list = QtWidgets.QComboBox()
        setting_list.addItems(values)
        setting_list.setCurrentIndex(default_option_index)
        self.grid_layout.addWidget(
            setting_list,
            len(self._settings) + len(self.buttons), 1,
            alignment=QtCore.Qt.AlignCenter
        )
        setting_list.setStyleSheet(Style.get_list_style())
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
        self.buttons[name].setStyleSheet(Style.get_button_style())
        self.buttons[name].clicked.connect(
            button_method(name)
        )
