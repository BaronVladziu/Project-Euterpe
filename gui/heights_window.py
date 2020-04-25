#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from gui.page_window import PageWindow

class HeightsWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        self.setWindowTitle("Euterpe pre-alpha")
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)

        # Add button to main page
        back_button = QtWidgets.QPushButton("Back", self)
        grid_layout.addWidget(back_button, 0, 0)
        back_button.clicked.connect(
            self.make_handleButton("back_button")
        )

        # Add button to settings page
        settings_button = QtWidgets.QPushButton("Exercise Settings", self)
        grid_layout.addWidget(settings_button, 0, 1)
        settings_button.clicked.connect(
            self.make_handleButton("settings_button")
        )

        # Add button to generator page
        generator_button = QtWidgets.QPushButton("Sound Generator", self)
        grid_layout.addWidget(generator_button, 0, 2)
        generator_button.clicked.connect(
            self.make_handleButton("generator_button")
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "settings_button":
                self.goto("heights_settings_page")
            if button == "generator_button":
                self.goto("heights_generator_page")
            if button == "back_button":
                self.goto("main_page")
        return handleButton


class HeightsGeneratorWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Euterpe pre-alpha")
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)

        # Add button to heights page
        back_button = QtWidgets.QPushButton("Back", self)
        grid_layout.addWidget(back_button, 0, 0)
        back_button.clicked.connect(
            self.make_handleButton("back_button")
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "back_button":
                self.goto("heights_page")
        return handleButton


class HeightsSettingsWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        self.setWindowTitle("Euterpe pre-alpha")
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)

        # Add button to heights page
        back_button = QtWidgets.QPushButton("Back", self)
        grid_layout.addWidget(back_button, 0, 0)
        back_button.clicked.connect(
            self.make_handleButton("back_button")
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "back_button":
                self.goto("heights_page")
        return handleButton
