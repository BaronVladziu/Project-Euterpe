#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from gui.detuning_window import DetuningWindow
from gui.intervals_window import IntervalsWindow
from gui.main_window import MainWindow
from gui.microtones_window import MicrotonesWindow
from gui.page_window import PageWindow
from gui.ten_o_heights_window import TenOHeightsWindow
from gui.voices_window import VoicesWindow

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        ten_o_heights_window = TenOHeightsWindow()
        self.register(
            ten_o_heights_window.instruction_window,
            "ten_o_heights_instruction_page"
        )
        self.register(
            ten_o_heights_window.main_window,
            "ten_o_heights_page"
        )
        self.register(
            ten_o_heights_window.generator_window,
            "ten_o_heights_generator_page"
        )
        self.register(
            ten_o_heights_window.setting_window,
            "ten_o_heights_settings_page"
        )

        intervals_window = IntervalsWindow()
        self.register(
            intervals_window.instruction_window,
            "intervals_instruction_page"
        )
        self.register(
            intervals_window.main_window,
            "intervals_page"
        )
        self.register(
            intervals_window.generator_window,
            "intervals_generator_page"
        )
        self.register(
            intervals_window.setting_window,
            "intervals_settings_page"
        )

        voices_window = VoicesWindow()
        self.register(
            voices_window.instruction_window,
            "voices_instruction_page"
        )
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
            microtones_window.instruction_window,
            "microtones_instruction_page"
        )
        self.register(
            microtones_window.main_window,
            "microtones_page"
        )
        self.register(
            microtones_window.generator_window,
            "microtones_generator_page"
        )
        self.register(
            microtones_window.setting_window,
            "microtones_settings_page"
        )

        detuning_window = DetuningWindow()
        self.register(
            detuning_window.instruction_window,
            "detuning_instruction_page"
        )
        self.register(
            detuning_window.main_window,
            "detuning_page"
        )
        self.register(
            detuning_window.generator_window,
            "detuning_generator_page"
        )
        self.register(
            detuning_window.setting_window,
            "detuning_settings_page"
        )

        self.register(
            MainWindow(
                voices_window=voices_window
            ),
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
