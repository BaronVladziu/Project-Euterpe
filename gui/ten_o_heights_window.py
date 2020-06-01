#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from exercises.ten_o_heights_exercise import TenOHeightsExercise
from gui.page_window import PageWindow
from gui.picture_label import PictureLabel
from notes.height import Height
from notes.scale import Scale
from synthesis.noise_synthesizer import NoiseSynthesizer
from synthesis.saw_synthesizer import SawSynthesizer
from synthesis.sine_synthesizer import SineSynthesizer
from synthesis.square_synthesizer import SquareSynthesizer
from synthesis.triangle_synthesizer import TriangleSynthesizer


class TenOHeightsWindow(PageWindow):
    def __init__(self):
        super().__init__()
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)

        # Add picture
        self.label = PictureLabel('graphics/heights1.png')
        grid_layout.addWidget(
            self.label,
            0, 0,
            1, 6,
            QtCore.Qt.AlignCenter
        )
        self.label.set_move_event(self.move_event)
        self.label.set_left_click_event(self.press_event)

        # Add button to main page
        back_button = QtWidgets.QPushButton("Back", self)
        grid_layout.addWidget(
            back_button,
            1, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        back_button.clicked.connect(
            self.make_handleButton("back_button")
        )

        # Add state label
        self.state_label = QtWidgets.QLabel()
        self.state_label.setText("Press button to generate new example -->")
        grid_layout.addWidget(
            self.state_label,
            1, 1,
            1, 2,
            alignment=QtCore.Qt.AlignCenter
        )

        # Add action button
        self.action_button = QtWidgets.QPushButton("Generate New Height", self)
        grid_layout.addWidget(
            self.action_button,
            1, 3,
            alignment=QtCore.Qt.AlignCenter
        )
        self.action_button.clicked.connect(
            self.make_handleButton("action_button")
        )

        # Add button to settings page
        settings_button = QtWidgets.QPushButton("Exercise Settings", self)
        grid_layout.addWidget(
            settings_button,
            1, 4,
            alignment=QtCore.Qt.AlignCenter
        )
        settings_button.clicked.connect(
            self.make_handleButton("settings_button")
        )

        # Add button to generator page
        generator_button = QtWidgets.QPushButton("Sound Generator", self)
        grid_layout.addWidget(
            generator_button,
            1, 5,
            alignment=QtCore.Qt.AlignCenter
        )
        generator_button.clicked.connect(
            self.make_handleButton("generator_button")
        )

        # Add exercise class
        self.exercise = TenOHeightsExercise(
            sampling_frequency=44100
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "settings_button":
                self.goto("ten_o_heights_settings_page")
            elif button == "generator_button":
                self.goto("ten_o_heights_generator_page")
            elif button == "back_button":
                self.label.if_active = False
                self.goto("main_page")
            elif button == "action_button":
                if not self.label.if_active:
                    self.label.reset()
                    self.state_label.setText("Click near correct value on figure above")
                    self.exercise.generate_new_example()
                    self.exercise.play_example(memory_flush=True)
                    self.action_button.setText("Listen Again")
                elif self.label.if_active:
                    self.exercise.play_example()
        return handleButton

    def move_event(self, x, y):
        self.label.mark_max_error(x, self.exercise.get_possible_error()/10)

    def press_event(self, x, y):
        answer = 10*(x - 581)
        if_correct, true_value = self.exercise.answer_example(
            answer
        )
        if if_correct:
            self.state_label.setText(
                "CORRECT! Pressed: "\
                + str(answer)\
                + "±"\
                + str(int(self.exercise.get_possible_error()))\
                + "c, Real value: "\
                + str(int(true_value))
            )
        else:
            self.state_label.setText(
                "WRONG :c Pressed: "\
                + str(answer)\
                + "±"\
                + str(int(self.exercise.get_possible_error()))\
                + "c, Real value: "\
                + str(int(true_value))\
                + "c"
            )
        self.action_button.setText("Generate New Interval")
        self.label.mark_correct_answer(if_correct, true_value/10 + 581)
            

class TenOHeightsGeneratorWindow(PageWindow):
    def __init__(self, parent:TenOHeightsWindow):
        super().__init__()
        self.parent = parent

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)

        # Add volume setting
        self.volume_label = QtWidgets.QLabel()
        self.volume_label.setText("Volume:")
        grid_layout.addWidget(
            self.volume_label,
            0, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.volume_list = QtWidgets.QComboBox()
        self.volume_list.addItems([
            "0.0",
            "0.1",
            "0.2",
            "0.3",
            "0.4",
            "0.5",
            "0.6",
            "0.7",
            "0.8",
            "0.9",
            "1.0"
        ])
        self.volume_list.setCurrentIndex(10)
        grid_layout.addWidget(
            self.volume_list,
            0, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.volume_list.currentIndexChanged.connect(
            self.volume_changed
        )
        self.volume_changed()

        # Add synthesizer type setting
        self.synthesizer_type_label = QtWidgets.QLabel()
        self.synthesizer_type_label.setText("Synthesizer Type:")
        grid_layout.addWidget(
            self.synthesizer_type_label,
            1, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.synthesizer_type_list = QtWidgets.QComboBox()
        self.synthesizer_type_list.addItems([
            "Sine",
            "Saw",
            "Triangle",
            "Square",
            "Noise"
        ])
        self.synthesizer_type_list.setCurrentIndex(2)
        grid_layout.addWidget(
            self.synthesizer_type_list,
            1, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.synthesizer_type_list.currentIndexChanged.connect(
            self.synthesizer_type_changed
        )
        self.synthesizer_type_changed()

        # Add sampling frequency setting
        self.sampling_frequency_label = QtWidgets.QLabel()
        self.sampling_frequency_label.setText("Sampling Frequency:")
        grid_layout.addWidget(
            self.sampling_frequency_label,
            2, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.sampling_frequency_list = QtWidgets.QComboBox()
        self.sampling_frequency_list.addItems([
            "8000",
            "16000",
            "22050",
            "44100",
            "48000",
            "96000",
            "192000"
        ])
        self.sampling_frequency_list.setCurrentIndex(3)
        grid_layout.addWidget(
            self.sampling_frequency_list,
            2, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.sampling_frequency_list.currentIndexChanged.connect(
            self.sampling_frequency_changed
        )
        self.sampling_frequency_changed()

        # Add button to ten_o_heights page
        back_button = QtWidgets.QPushButton("Back", self)
        grid_layout.addWidget(
            back_button,
            3, 0,
            1, 2,
            alignment=QtCore.Qt.AlignCenter
        )
        back_button.clicked.connect(
            self.make_handleButton("back_button")
        )

    def volume_changed(self):
        self.parent.exercise.set_volume(
            float(self.volume_list.currentText())
        )

    def synthesizer_type_changed(self):
        if self.synthesizer_type_list.currentText() == "Sine":
            self.parent.exercise.set_synthesizer(
                SineSynthesizer
            )
        elif self.synthesizer_type_list.currentText() == "Saw":
            self.parent.exercise.set_synthesizer(
                SawSynthesizer
            )
        elif self.synthesizer_type_list.currentText() == "Triangle":
            self.parent.exercise.set_synthesizer(
                TriangleSynthesizer
            )
        elif self.synthesizer_type_list.currentText() == "Square":
            self.parent.exercise.set_synthesizer(
                SquareSynthesizer
            )
        elif self.synthesizer_type_list.currentText() == "Noise":
            self.parent.exercise.set_synthesizer(
                NoiseSynthesizer
            )
        else:
            raise RuntimeError(
                '[TenOHeightsGeneratorWindow::synthesizer_type_changed()] Unknown synthesizer "'\
                + self.synthesizer_type_list.currentText()\
                + '"!'
            )

    def sampling_frequency_changed(self):
        self.parent.exercise.set_sampling_frequency(
            int(self.sampling_frequency_list.currentText())
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "back_button":
                self.goto("ten_o_heights_page")
        return handleButton


class TenOHeightsSettingsWindow(PageWindow):
    def __init__(self, parent:TenOHeightsWindow):
        super().__init__()
        self.parent = parent

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)

        # Add scale setting
        self.scale_label = QtWidgets.QLabel()
        self.scale_label.setText("Scale:")
        grid_layout.addWidget(
            self.scale_label,
            0, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.scale_list = QtWidgets.QComboBox()
        self.scale_list.addItems([
            "12-TET (A=440Hz)",
            "24-TET (A=440Hz)",
            "31-TET (A=440Hz)",
            "Pythagorean (C-based) (A=440Hz)",
            "Just (C-based) (A=440Hz)",
            "Quarter-comma meantone (C-based) (A=440Hz)",
            "Bach's (according to Werckmeister)"
        ])
        self.scale_list.setCurrentIndex(0)
        grid_layout.addWidget(
            self.scale_list,
            0, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.scale_list.currentIndexChanged.connect(
            self.scale_changed
        )
        self.scale_changed()

        # Add lowest height setting
        self.lowest_height_label = QtWidgets.QLabel()
        self.lowest_height_label.setText("Lowest Height:")
        grid_layout.addWidget(
            self.lowest_height_label,
            1, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.lowest_height_list = QtWidgets.QComboBox()
        self.lowest_height_list.addItems([
            "C0",
            "C1",
            "C2",
            "C3",
            "C4",
            "C5",
            "C6",
            "C7"
        ])
        self.lowest_height_list.setCurrentIndex(0)
        grid_layout.addWidget(
            self.lowest_height_list,
            1, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.lowest_height_list.currentIndexChanged.connect(
            self.lowest_height_changed
        )
        self.lowest_height_changed()

        # Add highest height setting
        self.highest_height_label = QtWidgets.QLabel()
        self.highest_height_label.setText("Highest Height:")
        grid_layout.addWidget(
            self.highest_height_label,
            2, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.highest_height_list = QtWidgets.QComboBox()
        self.highest_height_list.addItems([
            "C1",
            "C2",
            "C3",
            "C4",
            "C5",
            "C6",
            "C7",
            "C8"
        ])
        self.highest_height_list.setCurrentIndex(7)
        grid_layout.addWidget(
            self.highest_height_list,
            2, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.highest_height_list.currentIndexChanged.connect(
            self.highest_height_changed
        )
        self.highest_height_changed()

        # Add possible detune setting
        self.possible_detune_label = QtWidgets.QLabel()
        self.possible_detune_label.setText("Possible Detune:")
        grid_layout.addWidget(
            self.possible_detune_label,
            3, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.possible_detune_list = QtWidgets.QComboBox()
        self.possible_detune_list.addItems([
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20"
        ])
        self.possible_detune_list.setCurrentIndex(1)
        grid_layout.addWidget(
            self.possible_detune_list,
            3, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.possible_detune_list.currentIndexChanged.connect(
            self.possible_detune_changed
        )
        self.possible_detune_changed()

        # Add possible error setting
        self.possible_error_label = QtWidgets.QLabel()
        self.possible_error_label.setText("Possible Error:")
        grid_layout.addWidget(
            self.possible_error_label,
            4, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.possible_error_list = QtWidgets.QComboBox()
        self.possible_error_list.addItems([
            "5",
            "10",
            "20",
            "50",
            "100",
            "200",
            "500",
            "1000",
            "2000"
        ])
        self.possible_error_list.setCurrentIndex(6)
        grid_layout.addWidget(
            self.possible_error_list,
            4, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.possible_error_list.currentIndexChanged.connect(
            self.possible_error_changed
        )
        self.possible_error_changed()

        # Add button to ten_o_heights page
        back_button = QtWidgets.QPushButton("Back", self)
        grid_layout.addWidget(
            back_button,
            5, 0,
            1, 2,
            alignment=QtCore.Qt.AlignCenter
        )
        back_button.clicked.connect(
            self.make_handleButton("back_button")
        )

    def scale_changed(self):
        self.parent.exercise.set_scale(
            Scale(self.scale_list.currentText())
        )

    def lowest_height_changed(self):
        self.parent.exercise.set_lowest_height(
            Height.from_name(self.lowest_height_list.currentText())
        )

    def highest_height_changed(self):
        self.parent.exercise.set_highest_height(
            Height.from_name(self.highest_height_list.currentText())
        )

    def possible_detune_changed(self):
        self.parent.exercise.set_possible_detune(
            int(self.possible_detune_list.currentText())
        )

    def possible_error_changed(self):
        self.parent.exercise.set_possible_error(
            int(self.possible_error_list.currentText())
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "back_button":
                self.goto("ten_o_heights_page")
        return handleButton
