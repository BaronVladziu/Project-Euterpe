#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random

from notes.pitch import Pitch
from notes.scale import Scale

class PitchGenerator:
    def __init__(self,
        scale=Scale('12-TET (A=440Hz)'),
        lowest_pitch=Pitch(21),
        highest_pitch=Pitch(108),
        possible_detune=1.0
    ):
        self._scale = scale
        self._lowest_pitch = lowest_pitch
        self._highest_pitch = highest_pitch
        self._possible_detune = possible_detune

    def set_scale(self, scale:Scale):
        self._scale = scale

    def set_lowest_pitch(self, lowest_pitch:Pitch):
        self._lowest_pitch = lowest_pitch

    def set_highest_pitch(self, highest_pitch:Pitch):
        self._highest_pitch = highest_pitch

    def set_possible_detune(self, possible_detune:float):
        self._possible_detune = possible_detune

    def generate_pitch(self) -> Pitch:
        # Choose one randomly
        choice = random.choice(self._scale.get_pitches(
            from_pitch=self._lowest_pitch,
            to_pitch=self._highest_pitch,
        ))

        # Detune
        choice = choice.copy(detune=random.randint(
            -self._possible_detune,
            self._possible_detune
        ))
        return choice
