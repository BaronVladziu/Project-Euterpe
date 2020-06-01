#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from notes.height import Height
from notes.height_generator import HeightGenerator
from synthesis.player import Player
from notes.scale import Scale
from synthesis.synthesizer import Synthesizer


class TenOHeightsExercise:
    def __init__(self, sampling_frequency:int):
        # exercise settings
        self._sampling_frequency = sampling_frequency
        self._volume = None
        self._scale = None
        self._lowest_height = None
        self._highest_height = None
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

    def set_scale(self, scale:Scale):
        self._scale = scale

    def set_lowest_height(self, lowest_height:Height):
        self._lowest_height = lowest_height

    def set_highest_height(self, highest_height:Height):
        self._highest_height = highest_height

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
        height_generator = HeightGenerator(
            scale=self._scale,
            lowest_height=self._lowest_height,
            highest_height=self._highest_height,
            possible_detune=self._possible_detune
        )
        self._actual_example = height_generator.generate_height()

    def play_example(self):
        if self._actual_example is None:
            raise RuntimeError(
                '[TenOHeightsExercise::play_example()] No example to play!'
            )
        self._player.play(
            self._synthesizer.generate_height(
                height=self._actual_example,
                time=1
            )
        )

    def answer_example(self, answer) -> (bool, float):
        if self._actual_example.get_cents_from_a()\
                + self._possible_error\
                >= answer\
                >= self._actual_example.get_cents_from_a()\
                - self._possible_error:
            return True, self._actual_example.get_cents_from_a()
        else:
            return False, self._actual_example.get_cents_from_a()
