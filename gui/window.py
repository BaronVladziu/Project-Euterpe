#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from gui.heights_window import HeightsWindow, HeightsGeneratorWindow, HeightsSettingsWindow
from gui.intervals_window import IntervalsWindow, IntervalsGeneratorWindow, IntervalsSettingsWindow
from gui.main_window import MainWindow
from gui.page_window import PageWindow

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(MainWindow(), "main_page")
        self.register(HeightsWindow(), "heights_page")
        self.register(HeightsGeneratorWindow(), "heights_generator_page")
        self.register(HeightsSettingsWindow(), "heights_settings_page")
        intervals_window = IntervalsWindow()
        self.register(intervals_window, "intervals_page")
        self.register(IntervalsGeneratorWindow(intervals_window), "intervals_generator_page")
        self.register(IntervalsSettingsWindow(intervals_window), "intervals_settings_page")

        self.goto("main_page")

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())
