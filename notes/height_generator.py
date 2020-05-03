#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random

from notes.height import Height
from notes.scale import Scale

class HeightGenerator:
    def __init__(self,
        scale=Scale('12-TET (A=440Hz)'),
        lowest_height=Height(21),
        highest_height=Height(108),
        possible_detune=1
    ):
        self._scale = scale
        self._lowest_height = lowest_height
        self._highest_height = highest_height
        self._possible_detune = possible_detune

    def set_scale(self, scale:Scale):
        self._scale = scale

    def set_lowest_height(self, lowest_height:Height):
        self._lowest_height = lowest_height

    def set_highest_height(self, highest_height:Height):
        self._highest_height = highest_height

    def set_possible_detune(self, possible_detune:int):
        self._possible_detune = possible_detune

    def generate_height(self) -> Height:
        # Choose one randomly
        choice = random.choice(self._scale.get_heights(
            from_height=self._lowest_height,
            to_height=self._highest_height,
        ))

        # Detune
        choice = choice.copy(detune=random.randint(
            -self._possible_detune,
            self._possible_detune
        ))
        return choice
