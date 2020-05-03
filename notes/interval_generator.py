#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from notes.height import Height
from notes.height_generator import HeightGenerator
from notes.interval import Interval
from notes.scale import Scale

class IntervalGenerator:
    def __init__(self,
        scale=Scale('12-TET (A=440Hz)'),
        lowest_height=Height.from_midi(21),
        highest_height=Height.from_midi(108),
        possible_detune=1,
        smallest_interval=Interval.from_name('unison'),
        largest_interval=Interval.from_name('octave')
    ):
        self._scale = scale
        self._lowest_height = lowest_height
        self._highest_height = highest_height
        self._possible_detune = possible_detune
        self._smallest_interval = smallest_interval
        self._largest_interval = largest_interval

    def set_scale(self, scale:Scale):
        self._scale = scale

    def set_lowest_height(self, lowest_height:Height):
        self._lowest_height = lowest_height

    def set_highest_height(self, highest_height:Height):
        self._highest_height = highest_height

    def set_possible_detune(self, possible_detune:int):
        self._possible_detune = possible_detune

    def set_smallest_interval(self, smallest_interval:Interval):
        self._smallest_interval = smallest_interval

    def set_largest_interval(self, largest_interval:Interval):
        self._largest_interval = largest_interval

    def generate_interval(self) -> (Interval, Height, Height):
        # Generate first random height
        height_generator = HeightGenerator(
            scale=self._scale,
            lowest_height=self._lowest_height,
            highest_height=self._highest_height,
            possible_detune=0
        )
        height1 = height_generator.generate_height()

        # Generate second random height
        possible_heights = list()
        for height in self._scale.get_heights(
            from_height=self._lowest_height,
            to_height=self._highest_height
        ):
            interval = Interval.from_heights(
                from_height=Height.lower(height1, height),
                to_height=Height.higher(height1, height)
            )
            if self._largest_interval.get_cents()\
                    >= interval.get_cents()\
                    >= self._smallest_interval.get_cents():
                possible_heights.append(height)
        height2 = random.choice(possible_heights)

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
        output_interval = Interval.from_heights(
            from_height=output_height1,
            to_height=output_height2
        )
        return output_interval, output_height1, output_height2
