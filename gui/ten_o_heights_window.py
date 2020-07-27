#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from exercises.ten_o_heights_exercise import TenOHeightsExercise
from gui.exercise_window import ExerciseInstructionWindow, ExerciseMainWindow, ExerciseSettingsWindow
from gui.picture_label import PictureLabel
from notes.height import Height
from notes.scale import Scale
from synthesis.noise_synthesizer import NoiseSynthesizer
from synthesis.saw_synthesizer import SawSynthesizer
from synthesis.sine_synthesizer import SineSynthesizer
from synthesis.square_synthesizer import SquareSynthesizer
from synthesis.triangle_synthesizer import TriangleSynthesizer


class TenOHeightsWindow():
    def __init__(self):
        # Add exercise class
        self.exercise = TenOHeightsExercise(
            sampling_frequency=44100
        )

        # === INSTRUCTION WINDOW ===
        self.instruction_window = ExerciseInstructionWindow(
            instruction="TEN_O_HEIGHT",
            back_button_name="back_from_instruction_button",
            forward_button_name="forward_from_instruction_button",
            button_method=self.make_handleButton
        )

        # === MAIN WINDOW ===
        self.main_window = ExerciseMainWindow()

        # Add picture
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.label = PictureLabel('graphics/heights1.png')
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
            text="Generate New Height",
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

        # Add button to ten_o_heights page
        self.generator_window.add_button(
            name="back_from_generator",
            text="Back",
            button_method=self.make_handleButton
        )

        # === EXERCISE SETTINGS WINDOW ===
        self.setting_window = ExerciseSettingsWindow()

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

        # Add scale setting
        self.setting_window.add_setting(
            name="lowest_height",
            text="Lowest Height:",
            values=[
                "C0",
                "C1",
                "C2",
                "C3",
                "C4",
                "C5",
                "C6",
                "C7"
            ],
            default_option_index=0,
            setting_method=self.lowest_height_changed
        )

        # Add highest height setting
        self.setting_window.add_setting(
            name="highest_height",
            text="Highest Height:",
            values=[
                "C1",
                "C2",
                "C3",
                "C4",
                "C5",
                "C6",
                "C7",
                "C8"
            ],
            default_option_index=7,
            setting_method=self.highest_height_changed
        )

        # Add possible detune setting
        self.setting_window.add_setting(
            name="possible_detune",
            text="Possible Detune:",
            values=[
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
            ],
            default_option_index=1,
            setting_method=self.possible_detune_changed
        )

        # Add possible error setting
        self.setting_window.add_setting(
            name="possible_error",
            text="Possible Error:",
            values=[
                "5",
                "10",
                "20",
                "50",
                "100",
                "200",
                "500",
                "1000",
                "2000"
            ],
            default_option_index=6,
            setting_method=self.possible_error_changed
        )

        # Add button to ten_o_heights page
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
                self.main_window.goto("ten_o_heights_settings_page")
            elif button == "generator_button":
                self.main_window.goto("ten_o_heights_generator_page")
            elif button == "back_from_instruction_button":
                self.instruction_window.goto("main_page")
            elif button == "forward_from_instruction_button":
                self.instruction_window.goto("ten_o_heights_page")
            elif button == "back_button":
                self.label.if_active = False
                self.main_window.goto("main_page")
            elif button == "back_from_generator":
                self.generator_window.goto("ten_o_heights_page")
            elif button == "back_from_settings":
                self.reset_window()
                self.setting_window.goto("ten_o_heights_page")
            elif button == "action_button":
                if not self.label.if_active:
                    # Reset label
                    self.label.reset()
                    self.main_window.state_label.change_text(
                        "Click near correct values on figure above"
                    )

                    # Create new example
                    self.exercise.generate_new_example()
                    self.exercise.play_example(memory_flush=True)
                    self.main_window.buttons["action_button"].change_text("Listen Again")

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
        self.label.mark_correct_answer(if_correct, true_value/10 + 581)

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
                '[TenOHeightsGeneratorWindow::synthesizer_type_changed()] Unknown synthesizer "'\
                + self.generator_window.get_setting("synthesizer_type")\
                + '"!'
            )

    def sampling_frequency_changed(self):
        self.exercise.set_sampling_frequency(
            int(self.generator_window.get_setting("sampling_frequency"))
        )

    # === EXERCISE SETTINGS METHODS ===
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

    def possible_detune_changed(self):
        self.exercise.set_possible_detune(
            int(self.setting_window.get_setting("possible_detune"))
        )

    def possible_error_changed(self):
        self.exercise.set_possible_error(
            int(self.setting_window.get_setting("possible_error"))
        )
