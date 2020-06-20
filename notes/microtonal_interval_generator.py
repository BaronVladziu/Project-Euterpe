#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from notes.height import Height
from notes.interval import Interval
from notes.interval_scale import IntervalScale

class MicrotonalIntervalGenerator:
    def __init__(self,
        scale=IntervalScale('Whole Tone Fractions'),
        lowest_height=Height.from_name('C3'),
        highest_height=Height.from_name('C5'),
        possible_detune=0.5
    ):
        self._scale = scale
        self._lowest_height = lowest_height
        self._highest_height = highest_height
        self._possible_detune = possible_detune

    def set_scale(self, scale:IntervalScale):
        self._scale = scale

    def set_lowest_height(self, lowest_height:Height):
        self._lowest_height = lowest_height

    def set_highest_height(self, highest_height:Height):
        self._highest_height = highest_height

    def set_possible_detune(self, possible_detune:int):
        self._possible_detune = possible_detune

    def generate_interval(self) -> (Interval, Height, Height):
        # Generate first random height
        height1 = Height.from_frequency(
            random.uniform(
                self._lowest_height.get_frequency(),
                self._highest_height.get_frequency()
            )
        )

        # Generate second random height
        output_interval = random.choice(
            self._scale.get_intervals()
        )
        height2 = height1.add_interval(
            output_interval
        )
        if height2 == Height.higher(
            self._highest_height,
            height2
        ):
            height2 = height1.copy(
                detune=-output_interval.get_cents()
            )
        if height2 == Height.lower(
            self._lowest_height,
            height2
        ):
            raise RuntimeError(
                '[MicrotonalIntervalGenerator:generate_interval()] ' +
                'Could not generate interval! ' +
                'Make sure that lowest_height is sufficiently lower than highest_height!'
            )

        # Return interval and heights
        output_height1 = Height.from_height(
            height=Height.lower(height1, height2),
            detune=random.uniform(
                -self._possible_detune/2,
                self._possible_detune/2
            )
        )
        output_height2 = Height.from_height(
            height=Height.higher(height1, height2),
            detune=random.uniform(
                -self._possible_detune/2,
                self._possible_detune/2
            )
        )
        return output_interval, output_height1, output_height2
