#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from exercises.voices_exercise import VoicesExercise
from gui.page_window import PageWindow
from gui.picture_label import PictureLabel
from notes.height import Height
from notes.interval import Interval
from notes.scale import Scale
from synthesis.noise_synthesizer import NoiseSynthesizer
from synthesis.saw_synthesizer import SawSynthesizer
from synthesis.sine_synthesizer import SineSynthesizer
from synthesis.square_synthesizer import SquareSynthesizer
from synthesis.triangle_synthesizer import TriangleSynthesizer


class VoicesWindow(PageWindow):
    def __init__(self):
        super().__init__()
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)

        # Add exercise class
        self.exercise = VoicesExercise(
            sampling_frequency=44100
        )

        # Add pictures
        self.label_widget = QtWidgets.QWidget(self)
        grid_layout.addWidget(
            self.label_widget,
            0, 0,
            1, 7,
            QtCore.Qt.AlignCenter
        )
        self.labels = list()
        self.labels_layout = QtWidgets.QGridLayout(self.label_widget)

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
        self.action_button = QtWidgets.QPushButton("Generate New Example", self)
        grid_layout.addWidget(
            self.action_button,
            1, 3,
            alignment=QtCore.Qt.AlignCenter
        )
        self.action_button.clicked.connect(
            self.make_handleButton("action_button")
        )

        # Add answer button
        self.answer_button = QtWidgets.QPushButton("Check answer", self)
        grid_layout.addWidget(
            self.answer_button,
            1, 4,
            alignment=QtCore.Qt.AlignCenter
        )
        self.answer_button.clicked.connect(
            self.make_handleButton("answer_button")
        )

        # Add button to settings page
        settings_button = QtWidgets.QPushButton("Exercise Settings", self)
        grid_layout.addWidget(
            settings_button,
            1, 5,
            alignment=QtCore.Qt.AlignCenter
        )
        settings_button.clicked.connect(
            self.make_handleButton("settings_button")
        )

        # Add button to generator page
        generator_button = QtWidgets.QPushButton("Sound Generator", self)
        grid_layout.addWidget(
            generator_button,
            1, 6,
            alignment=QtCore.Qt.AlignCenter
        )
        generator_button.clicked.connect(
            self.make_handleButton("generator_button")
        )
    
    def reset_window(self):
        self.state_label.setText("Press button to generate new example -->")
        self.action_button.setText("Generate New Example")
        self.reset_labels()
        for label in self.labels:
            label.if_active = False

    def reset_labels(self):
        # Clear old labels
        for i in reversed(range(self.labels_layout.count())):
            self.labels_layout.itemAt(i).widget().setParent(None)
        self.labels = list()

        # Create new labels
        for i in range(self.exercise.get_voice_length()):
            self.labels.append(PictureLabel(
                picture_path='graphics/heights2.png',
                max_markers=self.exercise.get_chord_size()
            ))

        # Attach events to labels
        for i in range(len(self.labels)):
            self.labels[i].set_move_event(self.move_event, i)
            self.labels[i].set_left_click_event(self.left_click_event, i)
            self.labels[i].set_right_click_event(self.right_click_event, i)
        
        # Attach labels to layout
        for i in range(len(self.labels)):
            self.labels_layout.addWidget(
                self.labels[i],
                i, 0,
                alignment=QtCore.Qt.AlignCenter
            )

    def make_handleButton(self, button):
        def handleButton():
            if button == "settings_button":
                self.goto("voices_settings_page")
            elif button == "generator_button":
                self.goto("voices_generator_page")
            elif button == "back_button":
                self.labels = list()
                self.goto("main_page")
            elif button == "action_button":
                if not self.labels[0].if_active:
                    # Reset labels
                    for label in self.labels:
                        label.reset()
                    self.state_label.setText(
                        "Click near correct values on figure above"
                    )

                    # Create new example
                    self.exercise.generate_new_example()
                    first_note = self.exercise.get_first_note()
                    if first_note is not None:
                        self.labels[0].add_unerasable_marker(
                            first_note.get_cents_from_a()/4 + 835
                        )
                    self.exercise.play_example()
                    self.action_button.setText("Listen Again")
                elif self.labels[0].if_active:
                    self.exercise.play_example()
            elif button == "answer_button":
                if self.labels[0].if_active:
                    # Get label markers
                    user_answers = list()
                    for label in self.labels:
                        user_answers.append(label.markers)

                    # Convert to cents
                    for i in range(len(user_answers)):
                        for j in range(len(user_answers[i])):
                            user_answers[i][j] = 4*(user_answers[i][j] - 835)

                    # Get real answers
                    real_answer = self.exercise.answer_example(
                        user_answers
                    )

                    # Mark them on labels
                    for i in range(real_answer.example.get_voice_length()):
                        for j in range(real_answer.example.get_chord_size()):
                            if_correct, true_value = real_answer.get_height(i, j)
                            self.labels[i].mark_correct_answer(
                                if_correct,
                                true_value.get_cents_from_a()/4 + 835
                            )
                    self.state_label.setText(
                        "Press button to generate new example -->"
                    )
                    self.action_button.setText("Generate New Example")
        return handleButton

    def move_event(self, x, y, label_id):
        self.labels[label_id].mark_max_error(
            x,
            self.exercise.get_possible_error()/4
        )

    def left_click_event(self, x, y, label_id):
        # answer = 4*(x - 835)
        self.labels[label_id].mark_user_answer(x)

    def right_click_event(self, x, y, label_id):
        # answer = 4*(x - 835)
        self.labels[label_id].erase_user_answer(
            x,
            self.exercise.get_possible_error()/4
        )


class VoicesGeneratorWindow(PageWindow):
    def __init__(self, parent:VoicesWindow):
        super().__init__()
        self.parent = parent

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)

        # Add synthesizer type setting
        self.synthesizer_type_label = QtWidgets.QLabel()
        self.synthesizer_type_label.setText("Synthesizer Type:")
        grid_layout.addWidget(
            self.synthesizer_type_label,
            0, 0,
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
            0, 1,
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
            1, 0,
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
            1, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.sampling_frequency_list.currentIndexChanged.connect(
            self.sampling_frequency_changed
        )
        self.sampling_frequency_changed()

        # Add play type setting
        self.play_type_label = QtWidgets.QLabel()
        self.play_type_label.setText("Play Type:")
        grid_layout.addWidget(
            self.play_type_label,
            2, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.play_type_list = QtWidgets.QComboBox()
        self.play_type_list.addItems([
            "Upwards",
            "Downwards",
            "Upwards with hold",
            "Downwards with hold",
            "Together"
        ])
        self.play_type_list.setCurrentIndex(4)
        grid_layout.addWidget(
            self.play_type_list,
            2, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.play_type_list.currentIndexChanged.connect(
            self.play_type_changed
        )
        self.play_type_changed()

        # Add button to voices page
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
                '[VoicesGeneratorWindow::synthesizer_type_changed()] Unknown synthesizer "'\
                + self.synthesizer_type_list.currentText()\
                + '"!'
            )

    def sampling_frequency_changed(self):
        self.parent.exercise.set_sampling_frequency(
            int(self.sampling_frequency_list.currentText())
        )

    def play_type_changed(self):
        self.parent.exercise.set_play_type(
            self.play_type_list.currentText()
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "back_button":
                self.goto("voices_page")
        return handleButton


class VoicesSettingsWindow(PageWindow):
    def __init__(self, parent:VoicesWindow):
        super().__init__()
        self.parent = parent

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)

        # Add chord size setting
        self.chord_size_label = QtWidgets.QLabel()
        self.chord_size_label.setText("Number of sounds in a chord:")
        grid_layout.addWidget(
            self.chord_size_label,
            0, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.chord_size_list = QtWidgets.QComboBox()
        self.chord_size_list.addItems([
            "1",
            "2",
            "3",
            "4",
            "5"
        ])
        self.chord_size_list.setCurrentIndex(1)
        grid_layout.addWidget(
            self.chord_size_list,
            0, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.chord_size_list.currentIndexChanged.connect(
            self.chord_size_changed
        )
        self.chord_size_changed()

        # Add voice length setting
        self.voice_length_label = QtWidgets.QLabel()
        self.voice_length_label.setText("Number of chords:")
        grid_layout.addWidget(
            self.voice_length_label,
            1, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.voice_length_list = QtWidgets.QComboBox()
        self.voice_length_list.addItems([
            "1",
            "2",
            "3",
            "4",
            "5"
        ])
        self.voice_length_list.setCurrentIndex(1)
        grid_layout.addWidget(
            self.voice_length_list,
            1, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.voice_length_list.currentIndexChanged.connect(
            self.voice_length_changed
        )
        self.voice_length_changed()

        # Add scale setting
        self.scale_label = QtWidgets.QLabel()
        self.scale_label.setText("Scale:")
        grid_layout.addWidget(
            self.scale_label,
            2, 0,
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
            2, 1,
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
            3, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.lowest_height_list = QtWidgets.QComboBox()
        self.lowest_height_list.addItems([
            "C2",
            "C3",
            "C4",
            "C5"
        ])
        self.lowest_height_list.setCurrentIndex(0)
        grid_layout.addWidget(
            self.lowest_height_list,
            3, 1,
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
            4, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.highest_height_list = QtWidgets.QComboBox()
        self.highest_height_list.addItems([
            "C3",
            "C4",
            "C5",
            "C6"
        ])
        self.highest_height_list.setCurrentIndex(3)
        grid_layout.addWidget(
            self.highest_height_list,
            4, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.highest_height_list.currentIndexChanged.connect(
            self.highest_height_changed
        )
        self.highest_height_changed()

        # Add smallest interval setting
        self.smallest_interval_label = QtWidgets.QLabel()
        self.smallest_interval_label.setText("Smallest Interval in Chord:")
        grid_layout.addWidget(
            self.smallest_interval_label,
            5, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.smallest_interval_list = QtWidgets.QComboBox()
        self.smallest_interval_list.addItems([
            "20",
            "400",
            "700",
            "1200"
        ])
        self.smallest_interval_list.setCurrentIndex(0)
        grid_layout.addWidget(
            self.smallest_interval_list,
            5, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.smallest_interval_list.currentIndexChanged.connect(
            self.smallest_interval_changed
        )
        self.smallest_interval_changed()

        # Add largest interval setting
        self.largest_interval_label = QtWidgets.QLabel()
        self.largest_interval_label.setText("Largest Interval in Chord:")
        grid_layout.addWidget(
            self.largest_interval_label,
            6, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.largest_interval_list = QtWidgets.QComboBox()
        self.largest_interval_list.addItems([
            "400",
            "700",
            "1200",
            "1900",
            "2400",
            "3600",
            "4800"
        ])
        self.largest_interval_list.setCurrentIndex(6)
        grid_layout.addWidget(
            self.largest_interval_list,
            6, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.largest_interval_list.currentIndexChanged.connect(
            self.largest_interval_changed
        )
        self.largest_interval_changed()

        # Add possible detune setting
        self.possible_detune_label = QtWidgets.QLabel()
        self.possible_detune_label.setText("Possible Detune:")
        grid_layout.addWidget(
            self.possible_detune_label,
            7, 0,
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
            7, 1,
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
            8, 0,
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
            "500"
        ])
        self.possible_error_list.setCurrentIndex(2)
        grid_layout.addWidget(
            self.possible_error_list,
            8, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.possible_error_list.currentIndexChanged.connect(
            self.possible_error_changed
        )
        self.possible_error_changed()

        # Add if first note provided
        self.if_first_note_provided_label = QtWidgets.QLabel()
        self.if_first_note_provided_label.setText("Is First Note Provided:")
        grid_layout.addWidget(
            self.if_first_note_provided_label,
            9, 0,
            alignment=QtCore.Qt.AlignCenter
        )
        self.if_first_note_provided_list = QtWidgets.QComboBox()
        self.if_first_note_provided_list.addItems([
            "Yes",
            "No"
        ])
        self.if_first_note_provided_list.setCurrentIndex(0)
        grid_layout.addWidget(
            self.if_first_note_provided_list,
            9, 1,
            alignment=QtCore.Qt.AlignCenter
        )
        self.if_first_note_provided_list.currentIndexChanged.connect(
            self.if_first_note_provided_changed
        )
        self.if_first_note_provided_changed()

        # Add button to voices page
        back_button = QtWidgets.QPushButton("Back", self)
        grid_layout.addWidget(
            back_button,
            10, 0,
            1, 2,
            alignment=QtCore.Qt.AlignCenter
        )
        back_button.clicked.connect(
            self.make_handleButton("back_button")
        )

    def chord_size_changed(self):
        self.parent.exercise.set_chord_size(
            int(self.chord_size_list.currentText())
        )

    def voice_length_changed(self):
        self.parent.exercise.set_voice_length(
            int(self.voice_length_list.currentText())
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

    def smallest_interval_changed(self):
        self.parent.exercise.set_smallest_interval(
            Interval.from_cents(
                int(self.smallest_interval_list.currentText())
            )
        )

    def largest_interval_changed(self):
        self.parent.exercise.set_largest_interval(
            Interval.from_cents(
                int(self.largest_interval_list.currentText())
            )
        )

    def possible_detune_changed(self):
        self.parent.exercise.set_possible_detune(
            int(self.possible_detune_list.currentText())
        )

    def possible_error_changed(self):
        self.parent.exercise.set_possible_error(
            int(self.possible_error_list.currentText())
        )

    def if_first_note_provided_changed(self):
        if self.if_first_note_provided_list.currentText() == 'Yes':
            self.parent.exercise.set_if_first_note_provided(True)
        elif self.if_first_note_provided_list.currentText() == 'No':
            self.parent.exercise.set_if_first_note_provided(False)
        else:
            raise ValueError(
                '[VoicesSettingsWindow::if_first_note_provided_changed()'\
                + 'Unknown boolean value: '\
                + self.if_first_note_provided_list.currentText()\
                + ' !'
            )

    def make_handleButton(self, button):
        def handleButton():
            if button == "back_button":
                self.parent.reset_window()
                self.goto("voices_page")
        return handleButton
