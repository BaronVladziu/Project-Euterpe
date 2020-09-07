#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from notes.pitch import Pitch
from notes.pitch_generator import PitchGenerator
from notes.interval import Interval
from notes.scale import Scale

class IntervalGenerator:
    def __init__(self,
        scale=Scale('12-TET (A=440Hz)'),
        lowest_pitch=Pitch.from_midi(21),
        highest_pitch=Pitch.from_midi(108),
        possible_detune=1.0,
        smallest_interval=Interval.from_name('unison'),
        largest_interval=Interval.from_name('octave')
    ):
        self._scale = scale
        self._lowest_pitch = lowest_pitch
        self._highest_pitch = highest_pitch
        self._possible_detune = possible_detune
        self._smallest_interval = smallest_interval
        self._largest_interval = largest_interval

    def set_scale(self, scale:Scale):
        self._scale = scale

    def set_lowest_pitch(self, lowest_pitch:Pitch):
        self._lowest_pitch = lowest_pitch

    def set_highest_pitch(self, highest_pitch:Pitch):
        self._highest_pitch = highest_pitch

    def set_possible_detune(self, possible_detune:int):
        self._possible_detune = possible_detune

    def set_smallest_interval(self, smallest_interval:Interval):
        self._smallest_interval = smallest_interval

    def set_largest_interval(self, largest_interval:Interval):
        self._largest_interval = largest_interval

    def generate_interval(self) -> (Interval, Pitch, Pitch):
        # Generate first random pitch
        pitch_generator = PitchGenerator(
            scale=self._scale,
            lowest_pitch=self._lowest_pitch,
            highest_pitch=self._highest_pitch,
            possible_detune=0
        )
        pitch1 = pitch_generator.generate_pitch()

        # Generate second random pitch
        possible_pitches = list()
        for pitch in self._scale.get_pitches(
            from_pitch=self._lowest_pitch,
            to_pitch=self._highest_pitch
        ):
            interval = Interval.from_pitches(
                from_pitch=Pitch.lower(pitch1, pitch),
                to_pitch=Pitch.higher(pitch1, pitch)
            )
            if self._largest_interval.get_cents()\
                    >= interval.get_cents()\
                    >= self._smallest_interval.get_cents():
                possible_pitches.append(pitch)
        pitch2 = random.choice(possible_pitches)

        # Return interval and pitches
        output_pitch1 = Pitch.from_pitch(
            pitch=Pitch.lower(pitch1, pitch2),
            detune=random.uniform(
                -self._possible_detune/2,
                self._possible_detune/2
            )
        )
        output_pitch2 = Pitch.from_pitch(
            pitch=Pitch.higher(pitch1, pitch2),
            detune=random.uniform(
                -self._possible_detune/2,
                self._possible_detune/2
            )
        )
        output_interval = Interval.from_pitches(
            from_pitch=output_pitch1,
            to_pitch=output_pitch2
        )
        return output_interval, output_pitch1, output_pitch2
