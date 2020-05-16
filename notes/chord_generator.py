#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from notes.chord import Chord
from notes.height import Height
from notes.interval import Interval
from notes.scale import Scale

class ChordGenerator:
    def __init__(self,
        scale=Scale('12-TET (A=440Hz)'),
        lowest_height=Height.from_name('C2'),
        highest_height=Height.from_name('C6'),
        possible_detune=1,
        smallest_interval=Interval.from_name('unison'),
        largest_interval=Interval.from_name('octave'),
        chord_size=3
    ):
        self._scale = scale
        self._lowest_height = lowest_height
        self._highest_height = highest_height
        self._possible_detune = possible_detune
        self._smallest_interval = smallest_interval
        self._largest_interval = largest_interval
        self._chord_size = chord_size

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

    def set_chord_size(self, chord_size:int):
        self._chord_size = chord_size

    def generate_chord(self) -> Chord:
        # Get all available heights
        available_heights = self._scale.get_heights(
            from_height=self._lowest_height,
            to_height=self._highest_height
        )

        chosen_heights = list()
        for i in range(self._chord_size):
            # Choose random height
            new_height = random.choice(available_heights)
            chosen_heights.append(new_height)

            # Remove unavailable heights from list
            new_available_heights = list()
            for height in available_heights:
                if self._smallest_interval.get_cents()\
                        <= abs(Interval.from_heights(
                            height,
                            new_height
                        ).get_cents())\
                        <= self._largest_interval.get_cents():
                    new_available_heights.append(height)
            available_heights = new_available_heights

        # Return chord
        return Chord(chosen_heights)
