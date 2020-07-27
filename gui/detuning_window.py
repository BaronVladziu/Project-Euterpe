#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from exercises.detuning_exercise import DetuningExercise
from gui.exercise_window import ExerciseMainWindow, ExerciseSettingsWindow
from gui.picture_label import PictureLabel
from notes.height import Height
from notes.interval import Interval
from notes.scale import Scale
from synthesis.noise_synthesizer import NoiseSynthesizer
from synthesis.saw_synthesizer import SawSynthesizer
from synthesis.sine_synthesizer import SineSynthesizer
from synthesis.square_synthesizer import SquareSynthesizer
from synthesis.triangle_synthesizer import TriangleSynthesizer


class DetuningWindow():
    def __init__(self):
        # Add exercise class
        self.exercise = DetuningExercise(
            sampling_frequency=44100
        )

        # === MAIN WINDOW ===
        self.main_window = ExerciseMainWindow()

        # Add picture
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.label = PictureLabel('graphics/intervals3.png')
        self.main_window.grid_layout.addWidget(
            self.label,
            0, 0,
            1, 6,
            QtCore.Qt.AlignCenter
        )
        self.label.set_move_event(self.move_event)
        self.label.set_left_click_event(self.press_event)

        # Add button to main page
        self.main_window.add_button(
            name="back_button",
            position=0,
            size=1,
            text="Back",
            method=self.make_handleButton
        )

        # Add state label
        self.main_window.add_state_label(
            text="Press button to generate new example -->",
            position=1,
            size=2
        )

        # Add action button
        self.main_window.add_button(
            name="action_button",
            position=3,
            size=1,
            text="Generate New Detuned Melody",
            method=self.make_handleButton
        )

        # Add button to settings page
        self.main_window.add_button(
            name="settings_button",
            position=4,
            size=1,
            text="Exercise Settings",
            method=self.make_handleButton
        )

        # Add button to generator page
        self.main_window.add_button(
            name="generator_button",
            position=5,
            size=1,
            text="Sound Generator",
            method=self.make_handleButton
        )

        # === GENERATOR SETTINGS WINDOW ===
        self.generator_window = ExerciseSettingsWindow()

        # Add volume setting
        self.generator_window.add_setting(
            name="volume",
            text="Volume:",
            values=[
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
            ],
            default_option_index=10,
            setting_method=self.volume_changed
        )

        # Add synthesizer type setting
        self.generator_window.add_setting(
            name="synthesizer_type",
            text="Synthesizer Type:",
            values=[
                "Sine",
                "Saw",
                "Triangle",
                "Square",
                "Noise"
            ],
            default_option_index=2,
            setting_method=self.synthesizer_type_changed
        )

        # Add sampling frequency setting
        self.generator_window.add_setting(
            name="sampling_frequency",
            text="Sampling Frequency:",
            values=[
                "8000",
                "16000",
                "22050",
                "44100",
                "48000",
                "96000",
                "192000"
            ],
            default_option_index=3,
            setting_method=self.sampling_frequency_changed
        )

        # Add play type setting
        self.generator_window.add_setting(
            name="play_type",
            text="Play Type:",
            values=[
                "Upwards",
                "Downwards",
                "Upwards with hold",
                "Downwards with hold",
                "Together"
            ],
            default_option_index=4,
            setting_method=self.play_type_changed
        )

        # Add button to detuning page
        self.generator_window.add_button(
            name="back_from_generator",
            text="Back",
            button_method=self.make_handleButton
        )

        # === EXERCISE SETTINGS WINDOW ===
        self.setting_window = ExerciseSettingsWindow()

        # Add chord size setting
        self.setting_window.add_setting(
            name="chord_size",
            text="Number of sounds in a chord:",
            values=[
                "1",
                "2",
                "3",
                "4",
                "5"
            ],
            default_option_index=1,
            setting_method=self.chord_size_changed
        )

        # Add voice length setting
        self.setting_window.add_setting(
            name="voice_length",
            text="Number of chords:",
            values=[
                "1",
                "2",
                "3",
                "4",
                "5"
            ],
            default_option_index=3,
            setting_method=self.voice_length_changed
        )

        # Add scale setting
        self.setting_window.add_setting(
            name="scale",
            text="Scale:",
            values=[
                "12-TET (A=440Hz)",
                "24-TET (A=440Hz)",
                "31-TET (A=440Hz)",
                "Pythagorean (C-based) (A=440Hz)",
                "Just (C-based) (A=440Hz)",
                "Quarter-comma meantone (C-based) (A=440Hz)",
                "Bach's (according to Werckmeister)"
            ],
            default_option_index=0,
            setting_method=self.scale_changed
        )

        # Add lowest height setting
        self.setting_window.add_setting(
            name="lowest_height",
            text="Lowest Height:",
            values=[
                "C2",
                "C3",
                "C4",
                "C5"
            ],
            default_option_index=0,
            setting_method=self.lowest_height_changed
        )

        # Add highest height setting
        self.setting_window.add_setting(
            name="highest_height",
            text="Highest Height:",
            values=[
                "C3",
                "C4",
                "C5",
                "C6"
            ],
            default_option_index=3,
            setting_method=self.highest_height_changed
        )

        # Add smallest interval setting
        self.setting_window.add_setting(
            name="smallest_interval",
            text="Smallest Interval in Chord:",
            values=[
                "20",
                "400",
                "700",
                "1200"
            ],
            default_option_index=0,
            setting_method=self.smallest_interval_changed
        )

        # Add largest interval setting
        self.setting_window.add_setting(
            name="largest_interval",
            text="Largest Interval in Chord:",
            values=[
                "400",
                "700",
                "1200",
                "1900",
                "2400",
                "3600",
                "4800"
            ],
            default_option_index=6,
            setting_method=self.largest_interval_changed
        )

        # Add max detuning setting
        self.setting_window.add_setting(
            name="max_detuning",
            text="Max Detuning:",
            values=[
                "3",
                "5",
                "10",
                "20",
                "30",
                "50"
            ],
            default_option_index=5,
            setting_method=self.max_detuning_changed
        )

        # Add possible error setting
        self.setting_window.add_setting(
            name="possible_error",
            text="Possible Error:",
            values=[
                "1",
                "2",
                "3",
                "5",
                "10",
                "20",
                "30"
            ],
            default_option_index=4,
            setting_method=self.possible_error_changed
        )

        # Add button to detuning page
        self.setting_window.add_button(
            name="back_from_settings",
            text="Back",
            button_method=self.make_handleButton
        )

    def reset_window(self):
        self.main_window.reset_window()
        self.label.if_active = False

    def make_handleButton(self, button):
        def handleButton():
            if button == "settings_button":
                self.main_window.goto("detuning_settings_page")
            elif button == "generator_button":
                self.main_window.goto("detuning_generator_page")
            elif button == "back_button":
                self.label.if_active = False
                self.main_window.goto("main_page")
            elif button == "back_from_generator":
                self.generator_window.goto("detuning_page")
            elif button == "back_from_settings":
                self.reset_window()
                self.setting_window.goto("detuning_page")
            elif button == "action_button":
                if not self.label.if_active:
                    # Reset label
                    self.label.reset()
                    self.main_window.state_label.change_text(
                        "Click near correct values on figure above"
                    )

                    # Create new example
                    self.exercise.generate_new_example()
                    self.exercise.play_example()
                    self.main_window.buttons["action_button"].change_text("Listen Again")

                elif self.label.if_active:
                    self.exercise.play_example()
        return handleButton

    def move_event(self, x, y):
        self.label.mark_max_error(x, self.exercise.get_possible_error()*24)

    def press_event(self, x, y):
        answer = (x - 10)/24
        if_correct, true_value = self.exercise.answer_example(
            answer
        )
        if if_correct:
            self.main_window.state_label.change_text(
                "CORRECT! Pressed: "\
                + "{:.2f}".format(answer)\
                + "±"\
                + str(int(self.exercise.get_possible_error()))\
                + "c, Real value: "\
                + "{:.2f}".format(true_value)
            )
        else:
            self.main_window.state_label.change_text(
                "WRONG :c Pressed: "\
                + "{:.2f}".format(answer)\
                + "±"\
                + str(int(self.exercise.get_possible_error()))\
                + "c, Real value: "\
                + "{:.2f}".format(true_value)\
                + "c"
            )
        self.main_window.buttons["action_button"].reset_text()
        self.label.mark_correct_answer(if_correct, true_value*24 + 10)

    # === EXERCISE GENERATOR METHODS ===
    def volume_changed(self):
        self.exercise.set_volume(
            float(self.generator_window.get_setting("volume"))
        )

    def synthesizer_type_changed(self):
        if self.generator_window.get_setting("synthesizer_type") == "Sine":
            self.exercise.set_synthesizer(
                SineSynthesizer
            )
        elif self.generator_window.get_setting("synthesizer_type") == "Saw":
            self.exercise.set_synthesizer(
                SawSynthesizer
            )
        elif self.generator_window.get_setting("synthesizer_type") == "Triangle":
            self.exercise.set_synthesizer(
                TriangleSynthesizer
            )
        elif self.generator_window.get_setting("synthesizer_type") == "Square":
            self.exercise.set_synthesizer(
                SquareSynthesizer
            )
        elif self.generator_window.get_setting("synthesizer_type") == "Noise":
            self.exercise.set_synthesizer(
                NoiseSynthesizer
            )
        else:
            raise RuntimeError(
                '[DetuningGeneratorWindow::synthesizer_type_changed()] Unknown synthesizer "'\
                + self.generator_window.get_setting("synthesizer_type")\
                + '"!'
            )

    def sampling_frequency_changed(self):
        self.exercise.set_sampling_frequency(
            int(self.generator_window.get_setting("sampling_frequency"))
        )

    def play_type_changed(self):
        self.exercise.set_play_type(
            self.generator_window.get_setting("play_type")
        )

    # === EXERCISE SETTINGS METHODS ===
    def chord_size_changed(self):
        self.exercise.set_chord_size(
            int(self.setting_window.get_setting("chord_size"))
        )

    def voice_length_changed(self):
        self.exercise.set_voice_length(
            int(self.setting_window.get_setting("voice_length"))
        )

    def scale_changed(self):
        self.exercise.set_scale(
            Scale(self.setting_window.get_setting("scale"))
        )

    def lowest_height_changed(self):
        self.exercise.set_lowest_height(
            Height.from_name(self.setting_window.get_setting("lowest_height"))
        )

    def highest_height_changed(self):
        self.exercise.set_highest_height(
            Height.from_name(self.setting_window.get_setting("highest_height"))
        )

    def smallest_interval_changed(self):
        self.exercise.set_smallest_interval(
            Interval.from_cents(
                int(self.setting_window.get_setting("smallest_interval"))
            )
        )

    def largest_interval_changed(self):
        self.exercise.set_largest_interval(
            Interval.from_cents(
                int(self.setting_window.get_setting("largest_interval"))
            )
        )

    def max_detuning_changed(self):
        self.exercise.set_max_detuning(
            float(self.setting_window.get_setting("max_detuning"))
        )

    def possible_error_changed(self):
        self.exercise.set_possible_error(
            int(self.setting_window.get_setting("possible_error"))
        )