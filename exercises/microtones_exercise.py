#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exercises.intervals_exercise import IntervalExample
from notes.pitch import Pitch
from notes.interval import Interval
from notes.microtonal_interval_generator import MicrotonalIntervalGenerator
from synthesis.player import Player
from notes.interval_scale import IntervalScale
from synthesis.synthesizer import Synthesizer


class MicrotonesExercise:
    def __init__(self, sampling_frequency:int):
        # exercise settings
        self._sampling_frequency = sampling_frequency
        self._volume = None
        self._play_type = None
        self._interval_scale = None
        self._lowest_pitch = None
        self._highest_pitch = None
        self._possible_detune = None
        self._synthesizer = Synthesizer(sampling_frequency)
        self._possible_error = None

        # other variables
        self._actual_example = None
        self._player = Player(sampling_frequency)

    def set_sampling_frequency(self, sampling_frequency:int):
        self._sampling_frequency = sampling_frequency
        self._synthesizer.set_sampling_frequency(sampling_frequency)
        self._player.set_sampling_frequency(sampling_frequency)

    def set_volume(self, volume:float):
        self._volume = volume
        self._synthesizer.set_volume(volume)

    def set_play_type(self, play_type:str):
        self._play_type = play_type

    def set_interval_scale(self, interval_scale:IntervalScale):
        self._interval_scale = interval_scale

    def set_lowest_pitch(self, lowest_pitch:Pitch):
        self._lowest_pitch = lowest_pitch

    def set_highest_pitch(self, highest_pitch:Pitch):
        self._highest_pitch = highest_pitch

    def set_possible_detune(self, possible_detune:float):
        self._possible_detune = possible_detune

    def set_synthesizer(self, synthesizer:type):
        self._synthesizer = Synthesizer(
            self._sampling_frequency,
            synthesizer
        )

    def get_possible_error(self):
        return self._possible_error

    def set_possible_error(self, possible_error:float):
        self._possible_error = possible_error

    def generate_new_example(self):
        microtone_generator = MicrotonalIntervalGenerator(
            scale=self._interval_scale,
            lowest_pitch=self._lowest_pitch,
            highest_pitch=self._highest_pitch,
            possible_detune=self._possible_detune
        )
        self._actual_example = IntervalExample(
            microtone_generator.generate_interval()
        )

    def play_example(self):
        if self._actual_example is None:
            raise RuntimeError(
                '[MicrotonesExercise::play_example()] No example to play!'
            )
        if self._play_type is None:
            raise RuntimeError(
                '[MicrotonesExercise::play_example()] No play type chosen!'
            )
        elif self._play_type == 'Upwards':
            self._player.play(
                self._synthesizer.generate_interval_up(
                    self._actual_example.lower_pitch,
                    self._actual_example.higher_pitch
                )
            )
        elif self._play_type == 'Downwards':
            self._player.play(
                self._synthesizer.generate_interval_down(
                    self._actual_example.lower_pitch,
                    self._actual_example.higher_pitch
                )
            )
        elif self._play_type == 'Upwards with hold':
            self._player.play(
                self._synthesizer.generate_interval_up_hold(
                    self._actual_example.lower_pitch,
                    self._actual_example.higher_pitch
                )
            )
        elif self._play_type == 'Downwards with hold':
            self._player.play(
                self._synthesizer.generate_interval_down_hold(
                    self._actual_example.lower_pitch,
                    self._actual_example.higher_pitch
                )
            )
        elif self._play_type == 'Together':
            self._player.play(
                self._synthesizer.generate_interval_together(
                    self._actual_example.lower_pitch,
                    self._actual_example.higher_pitch
                )
            )
        else:
            raise RuntimeError(
                '[MicrotonesExercise::play_example()] Unknown play type!'
            )

    def answer_example(self, answer:float) -> (bool, float):
        if self._actual_example.interval.get_cents()\
                + self._possible_error\
                >= answer\
                >= self._actual_example.interval.get_cents()\
                - self._possible_error:
            return True, self._actual_example.interval.get_cents()
        else:
            return False, self._actual_example.interval.get_cents()
