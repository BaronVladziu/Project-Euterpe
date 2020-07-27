#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from gui.detuning_window import DetuningWindow, DetuningGeneratorWindow, DetuningSettingsWindow
from gui.intervals_window import IntervalsWindow, IntervalsGeneratorWindow, IntervalsSettingsWindow
from gui.main_window import MainWindow
from gui.microtones_window import MicrotonesWindow, MicrotonesGeneratorWindow, MicrotonesSettingsWindow
from gui.page_window import PageWindow
from gui.ten_o_heights_window import TenOHeightsWindow, TenOHeightsGeneratorWindow, TenOHeightsSettingsWindow
from gui.voices_window import VoicesWindow

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
            voices_window.main_window,
            "voices_page"
        )
        self.register(
            voices_window.generator_window,
            "voices_generator_page"
        )
        self.register(
            voices_window.setting_window,
            "voices_settings_page"
        )

        microtones_window = MicrotonesWindow()
        self.register(
            microtones_window,
            "microtones_page"
        )
        self.register(
            MicrotonesGeneratorWindow(microtones_window),
            "microtones_generator_page"
        )
        self.register(
            MicrotonesSettingsWindow(microtones_window),
            "microtones_settings_page"
        )

        detuning_window = DetuningWindow()
        self.register(
            detuning_window,
            "detuning_page"
        )
        self.register(
            DetuningGeneratorWindow(detuning_window),
            "detuning_generator_page"
        )
        self.register(
            DetuningSettingsWindow(detuning_window),
            "detuning_settings_page"
        )

        self.register(
            MainWindow(voices_window),
            "main_page"
        )

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
