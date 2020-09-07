#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from gui.page_window import PageWindow
from gui.style import Style


class MainWindow(PageWindow):
    def __init__(
        self,
        voices_window
    ):
        super().__init__()
        self.voices_window = voices_window

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)
        central_widget.setStyleSheet(Style.get_window_style())

        # Add title
        title_label = QtWidgets.QLabel()
        title_label.setText("Welcome to EUTERPE")
        grid_layout.addWidget(title_label, 0, 0, 1, 6, QtCore.Qt.AlignCenter)
        title_label.setStyleSheet(Style.get_text_style())

        # Add title
        help_label = QtWidgets.QLabel()
        help_label.setText("What would you like to do today?")
        grid_layout.addWidget(help_label, 1, 0, 1, 6, QtCore.Qt.AlignCenter)
        help_label.setStyleSheet(Style.get_text_style())

        # Add button to pitches page
        pitches_button = QtWidgets.QPushButton("Recognise Pitches", self)
        grid_layout.addWidget(pitches_button, 2, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
        pitches_button.setStyleSheet(Style.get_button_style())
        pitches_button.clicked.connect(
            self.make_handleButton("ten_o_pitches_button")
        )

        # Add button to intervals page
        intervals_button = QtWidgets.QPushButton("Recognise Intervals", self)
        grid_layout.addWidget(intervals_button, 2, 2, 1, 2, alignment=QtCore.Qt.AlignCenter)
        intervals_button.setStyleSheet(Style.get_button_style())
        intervals_button.clicked.connect(
            self.make_handleButton("intervals_button")
        )

        # Add button to voices page
        voices_button = QtWidgets.QPushButton("Recognise Chords and Melodies", self)
        grid_layout.addWidget(voices_button, 2, 4, 1, 2, alignment=QtCore.Qt.AlignCenter)
        voices_button.setStyleSheet(Style.get_button_style())
        voices_button.clicked.connect(
            self.make_handleButton("voices_button")
        )

        # Add button to microtones page
        microtones_button = QtWidgets.QPushButton("Recognise Microtones", self)
        grid_layout.addWidget(microtones_button, 3, 0, 1, 3, alignment=QtCore.Qt.AlignCenter)
        microtones_button.setStyleSheet(Style.get_button_style())
        microtones_button.clicked.connect(
            self.make_handleButton("microtones_button")
        )

        # Add button to detuning page
        detuning_button = QtWidgets.QPushButton("Recognise Detuning", self)
        grid_layout.addWidget(detuning_button, 3, 3, 1, 3, alignment=QtCore.Qt.AlignCenter)
        detuning_button.setStyleSheet(Style.get_button_style())
        detuning_button.clicked.connect(
            self.make_handleButton("detuning_button")
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "ten_o_pitches_button":
                self.goto("ten_o_pitches_instruction_page")
            if button == "intervals_button":
                self.goto("intervals_instruction_page")
            if button == "voices_button":
                self.voices_window.reset_labels()
                self.goto("voices_instruction_page")
            if button == "microtones_button":
                self.goto("microtones_instruction_page")
            if button == "detuning_button":
                self.goto("detuning_instruction_page")
        return handleButton
