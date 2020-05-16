#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from gui.intervals_window import IntervalsWindow, IntervalsGeneratorWindow, IntervalsSettingsWindow
from gui.main_window import MainWindow
from gui.page_window import PageWindow
from gui.ten_o_heights_window import TenOHeightsWindow, TenOHeightsGeneratorWindow, TenOHeightsSettingsWindow
from gui.voices_window import VoicesWindow, VoicesGeneratorWindow, VoicesSettingsWindow

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        ten_o_heights_window = TenOHeightsWindow()
        self.register(
            ten_o_heights_window,
            "ten_o_heights_page"
        )
        self.register(
            TenOHeightsGeneratorWindow(ten_o_heights_window),
            "ten_o_heights_generator_page"
        )
        self.register(
            TenOHeightsSettingsWindow(ten_o_heights_window),
            "ten_o_heights_settings_page"
        )

        intervals_window = IntervalsWindow()
        self.register(
            intervals_window,
            "intervals_page"
        )
        self.register(
            IntervalsGeneratorWindow(intervals_window),
            "intervals_generator_page"
        )
        self.register(
            IntervalsSettingsWindow(intervals_window),
            "intervals_settings_page"
        )

        voices_window = VoicesWindow()
        self.register(
            voices_window,
            "voices_page"
        )
        self.register(
            VoicesGeneratorWindow(voices_window),
            "voices_generator_page"
        )
        self.register(
            VoicesSettingsWindow(voices_window),
            "voices_settings_page"
        )

        self.register(MainWindow(
            ten_o_heights_window,
            intervals_window,
            voices_window
        ), "main_page")

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
