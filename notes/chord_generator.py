#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from notes.chord import Chord
from notes.pitch import Pitch
from notes.interval import Interval
from notes.scale import Scale

class ChordGenerator:
    def __init__(self,
        scale=Scale('12-TET (A=440Hz)'),
        lowest_pitch=Pitch.from_name('C2'),
        highest_pitch=Pitch.from_name('C6'),
        possible_detune=1.0,
        smallest_interval=Interval.from_name('unison'),
        largest_interval=Interval.from_name('octave'),
        chord_size=3
    ):
        self._scale = scale
        self._lowest_pitch = lowest_pitch
        self._highest_pitch = highest_pitch
        self._possible_detune = possible_detune
        self._smallest_interval = smallest_interval
        self._largest_interval = largest_interval
        self._chord_size = chord_size

    def set_scale(self, scale:Scale):
        self._scale = scale

    def set_lowest_pitch(self, lowest_pitch:Pitch):
        self._lowest_pitch = lowest_pitch

    def set_highest_pitch(self, highest_pitch:Pitch):
        self._highest_pitch = highest_pitch

    def set_possible_detune(self, possible_detune:float):
        self._possible_detune = possible_detune

    def set_smallest_interval(self, smallest_interval:Interval):
        self._smallest_interval = smallest_interval

    def set_largest_interval(self, largest_interval:Interval):
        self._largest_interval = largest_interval

    def set_chord_size(self, chord_size:int):
        self._chord_size = chord_size

    def generate_chord(self) -> Chord:
        # Get all available pitches
        available_pitches = self._scale.get_pitches(
            from_pitch=self._lowest_pitch,
            to_pitch=self._highest_pitch
        )

        chosen_pitches = list()
        for i in range(self._chord_size):
            # Choose random pitch
            new_pitch = random.choice(available_pitches)
            chosen_pitches.append(new_pitch)

            # Remove unavailable pitches from list
            new_available_pitches = list()
            for pitch in available_pitches:
                if self._smallest_interval.get_cents()\
                        <= abs(Interval.from_pitches(
                            pitch,
                            new_pitch
                        ).get_cents())\
                        <= self._largest_interval.get_cents():
                    new_available_pitches.append(pitch)
            available_pitches = new_available_pitches

        # Return chord
        return Chord(chosen_pitches)
