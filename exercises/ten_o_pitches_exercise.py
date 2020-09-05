#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from notes.pitch import Pitch
from notes.pitch_generator import PitchGenerator
from synthesis.player import Player
from notes.scale import Scale
from synthesis.synthesizer import Synthesizer


class TenOPitchesExercise:
    def __init__(self, sampling_frequency:int):
        # exercise settings
        self._sampling_frequency = sampling_frequency
        self._volume = None
        self._scale = None
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

    def set_scale(self, scale:Scale):
        self._scale = scale

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
        pitch_generator = PitchGenerator(
            scale=self._scale,
            lowest_pitch=self._lowest_pitch,
            highest_pitch=self._highest_pitch,
            possible_detune=self._possible_detune
        )
        self._actual_example = pitch_generator.generate_pitch()

    def play_example(self, memory_flush=False):
        # Check exercise state
        if self._actual_example is None:
            raise RuntimeError(
                '[TenOPitchesExercise::play_example()] No example to play!'
            )

        # Generate memory flush
        signal = np.zeros(0)
        if memory_flush:
            signal = np.concatenate([
                signal,
                self._synthesizer.generate_memory_flush(
                    lowest_pitch=self._lowest_pitch,
                    highest_pitch=self._highest_pitch
                ),
                np.zeros(self._sampling_frequency)
            ])
        
        # Play
        self._player.play(
            np.concatenate([
                signal,
                self._synthesizer.generate_pitch(
                    pitch=self._actual_example,
                    time=1
                )
            ])
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
