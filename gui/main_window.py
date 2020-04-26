#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from gui.page_window import PageWindow

class MainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)

        # Add title
        title_label = QtWidgets.QLabel()
        title_label.setText("Welcome to EUTERPE")
        grid_layout.addWidget(title_label, 0, 0, 1, 2, QtCore.Qt.AlignCenter)

        # Add title
        help_label = QtWidgets.QLabel()
        help_label.setText("What would you like to do today?")
        grid_layout.addWidget(help_label, 1, 0, 1, 2, QtCore.Qt.AlignCenter)

        # Add button to heights page
        heights_button = QtWidgets.QPushButton("Recognise Heights", self)
        grid_layout.addWidget(heights_button, 2, 0, alignment=QtCore.Qt.AlignCenter)
        heights_button.clicked.connect(
            self.make_handleButton("ten_o_heights_button")
        )

        # Add button to intervals page
        intervals_button = QtWidgets.QPushButton("Recognise Intervals", self)
        grid_layout.addWidget(intervals_button, 2, 1, alignment=QtCore.Qt.AlignCenter)
        intervals_button.clicked.connect(
            self.make_handleButton("intervals_button")
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "ten_o_heights_button":
                self.goto("ten_o_heights_page")
            if button == "intervals_button":
                self.goto("intervals_page")
        return handleButton
