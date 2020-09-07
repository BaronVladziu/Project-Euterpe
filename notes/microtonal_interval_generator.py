#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from notes.pitch import Pitch
from notes.interval import Interval
from notes.interval_scale import IntervalScale

class MicrotonalIntervalGenerator:
    def __init__(self,
        scale=IntervalScale('Whole Tone Fractions'),
        lowest_pitch=Pitch.from_name('C3'),
        highest_pitch=Pitch.from_name('C5'),
        possible_detune=0.5
    ):
        self._scale = scale
        self._lowest_pitch = lowest_pitch
        self._highest_pitch = highest_pitch
        self._possible_detune = possible_detune

    def set_scale(self, scale:IntervalScale):
        self._scale = scale

    def set_lowest_pitch(self, lowest_pitch:Pitch):
        self._lowest_pitch = lowest_pitch

    def set_highest_pitch(self, highest_pitch:Pitch):
        self._highest_pitch = highest_pitch

    def set_possible_detune(self, possible_detune:float):
        self._possible_detune = possible_detune

    def generate_interval(self) -> (Interval, Pitch, Pitch):
        # Generate first random pitch
        pitch1 = Pitch.from_frequency(
            random.uniform(
                self._lowest_pitch.get_frequency(),
                self._highest_pitch.get_frequency()
            )
        )

        # Generate second random pitch
        output_interval = random.choice(
            self._scale.get_intervals()
        )
        pitch2 = pitch1.add_interval(
            output_interval
        )
        if pitch2 == Pitch.higher(
            self._highest_pitch,
            pitch2
        ):
            pitch2 = pitch1.copy(
                detune=-output_interval.get_cents()
            )
        if pitch2 == Pitch.lower(
            self._lowest_pitch,
            pitch2
        ):
            raise RuntimeError(
                '[MicrotonalIntervalGenerator:generate_interval()] ' +
                'Could not generate interval! ' +
                'Make sure that lowest_pitch is sufficiently lower than highest_pitch!'
            )

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
        return output_interval, output_pitch1, output_pitch2
