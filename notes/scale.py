#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from notes.height import Height

class Scale:
    def __init__(self, scale_type=None):
        """
        Musical scale interpreted as the list of musical heights.
        """
        self._heights = list()
        self._detune = 0

        if scale_type == None:
            pass

        elif scale_type == '12-TET (A=440Hz)':
            self._heights.append(Height.from_midi(60))
            self._heights.append(Height.from_midi(61))
            self._heights.append(Height.from_midi(62))
            self._heights.append(Height.from_midi(63))
            self._heights.append(Height.from_midi(64))
            self._heights.append(Height.from_midi(65))
            self._heights.append(Height.from_midi(66))
            self._heights.append(Height.from_midi(67))
            self._heights.append(Height.from_midi(68))
            self._heights.append(Height.from_midi(69))
            self._heights.append(Height.from_midi(70))
            self._heights.append(Height.from_midi(71))
        elif scale_type == '24-TET (A=440Hz)':
            self._heights.append(Height.from_midi(60))
            self._heights.append(Height.from_midi(60, 50))
            self._heights.append(Height.from_midi(61))
            self._heights.append(Height.from_midi(61, 50))
            self._heights.append(Height.from_midi(62))
            self._heights.append(Height.from_midi(62, 50))
            self._heights.append(Height.from_midi(63))
            self._heights.append(Height.from_midi(63, 50))
            self._heights.append(Height.from_midi(64))
            self._heights.append(Height.from_midi(64, 50))
            self._heights.append(Height.from_midi(65))
            self._heights.append(Height.from_midi(65, 50))
            self._heights.append(Height.from_midi(66))
            self._heights.append(Height.from_midi(66, 50))
            self._heights.append(Height.from_midi(67))
            self._heights.append(Height.from_midi(67, 50))
            self._heights.append(Height.from_midi(68))
            self._heights.append(Height.from_midi(68, 50))
            self._heights.append(Height.from_midi(69))
            self._heights.append(Height.from_midi(69, 50))
            self._heights.append(Height.from_midi(70))
            self._heights.append(Height.from_midi(70, 50))
            self._heights.append(Height.from_midi(71))
            self._heights.append(Height.from_midi(71, 50))
        elif scale_type == '31-TET (A=440Hz)':
            self._heights.append(Height.from_midi(57))
            self._heights.append(Height.from_midi(57, 1*38.71))
            self._heights.append(Height.from_midi(57, 2*38.71))
            self._heights.append(Height.from_midi(57, 3*38.71))
            self._heights.append(Height.from_midi(57, 4*38.71))
            self._heights.append(Height.from_midi(57, 5*38.71))
            self._heights.append(Height.from_midi(57, 6*38.71))
            self._heights.append(Height.from_midi(57, 7*38.71))
            self._heights.append(Height.from_midi(57, 8*38.71))
            self._heights.append(Height.from_midi(57, 9*38.71))
            self._heights.append(Height.from_midi(57, 10*38.71))
            self._heights.append(Height.from_midi(57, 11*38.71))
            self._heights.append(Height.from_midi(57, 12*38.71))
            self._heights.append(Height.from_midi(57, 13*38.71))
            self._heights.append(Height.from_midi(57, 14*38.71))
            self._heights.append(Height.from_midi(57, 15*38.71))
            self._heights.append(Height.from_midi(57, 16*38.71))
            self._heights.append(Height.from_midi(57, 17*38.71))
            self._heights.append(Height.from_midi(57, 18*38.71))
            self._heights.append(Height.from_midi(57, 19*38.71))
            self._heights.append(Height.from_midi(57, 20*38.71))
            self._heights.append(Height.from_midi(57, 21*38.71))
            self._heights.append(Height.from_midi(57, 22*38.71))
            self._heights.append(Height.from_midi(57, 23*38.71))
            self._heights.append(Height.from_midi(57, 24*38.71))
            self._heights.append(Height.from_midi(57, 25*38.71))
            self._heights.append(Height.from_midi(57, 26*38.71))
            self._heights.append(Height.from_midi(57, 27*38.71))
            self._heights.append(Height.from_midi(57, 28*38.71))
            self._heights.append(Height.from_midi(57, 29*38.71))
            self._heights.append(Height.from_midi(57, 30*38.71))
        elif scale_type == 'Pythagorean (C-based) (A=440Hz)':
            self._heights.append(Height.from_midi(57))
            self._heights.append(Height.from_midi(58, -5.87-3.91))
            self._heights.append(Height.from_midi(59, -5.87+9.78))
            self._heights.append(Height.from_midi(60, -5.87))
            self._heights.append(Height.from_midi(61, -5.87-9.78))
            self._heights.append(Height.from_midi(62, -5.87+3.91))
            self._heights.append(Height.from_midi(63, -5.87-5.87))
            self._heights.append(Height.from_midi(64, -5.87+7.82))
            self._heights.append(Height.from_midi(65, -5.87-1.96))
            self._heights.append(Height.from_midi(66, -5.87-11.73))
            self._heights.append(Height.from_midi(66, -5.87+11.73))
            self._heights.append(Height.from_midi(67, -5.87+1.96))
            self._heights.append(Height.from_midi(68, -5.87-7.82))
        elif scale_type == 'Just (C-based) (A=440Hz)':
            self._heights.append(Height.from_midi(57))
            self._heights.append(Height.from_midi(58, +15.64-3.91))
            self._heights.append(Height.from_midi(59, +15.64-11.73))
            self._heights.append(Height.from_midi(60, +15.64))
            self._heights.append(Height.from_midi(61, +15.64+11.73))
            self._heights.append(Height.from_midi(62, +15.64+3.91))
            self._heights.append(Height.from_midi(63, +15.64+15.64))
            self._heights.append(Height.from_midi(64, +15.64-13.96))
            self._heights.append(Height.from_midi(65, +15.64-1.96))
            self._heights.append(Height.from_midi(66, +15.64-17.49))
            self._heights.append(Height.from_midi(66, +15.64+17.49))
            self._heights.append(Height.from_midi(67, +15.64+1.96))
            self._heights.append(Height.from_midi(68, +15.64+13.96))
        elif scale_type == 'Quarter-comma meantone (C-based) (A=440Hz)':
            self._heights.append(Height.from_midi(57))
            self._heights.append(Height.from_midi(58, +10.3+6.8))
            self._heights.append(Height.from_midi(59, +10.3-17.1))
            self._heights.append(Height.from_midi(60, +10.3))
            self._heights.append(Height.from_midi(61, +10.3+17.1))
            self._heights.append(Height.from_midi(62, +10.3-6.8))
            self._heights.append(Height.from_midi(63, +10.3+10.3))
            self._heights.append(Height.from_midi(64, +10.3-13.7))
            self._heights.append(Height.from_midi(65, +10.3+3.4))
            self._heights.append(Height.from_midi(66, +10.3-20.5))
            self._heights.append(Height.from_midi(66, +10.3+20.5))
            self._heights.append(Height.from_midi(67, +10.3-3.4))
            self._heights.append(Height.from_midi(68, +10.3+13.7))
        elif scale_type == 'Bach\'s (according to Werckmeister)':
            self._heights.append(Height.from_frequency(263.38))
            self._heights.append(Height.from_frequency(276.91))
            self._heights.append(Height.from_frequency(294.37))
            self._heights.append(Height.from_frequency(311.72))
            self._heights.append(Height.from_frequency(329.23))
            self._heights.append(Height.from_frequency(351.17))
            self._heights.append(Height.from_frequency(369.22))
            self._heights.append(Height.from_frequency(393.52))
            self._heights.append(Height.from_frequency(415.37))
            self._heights.append(Height.from_frequency(440.0))
            self._heights.append(Height.from_frequency(467.97))
            self._heights.append(Height.from_frequency(492.29))        

        # Raise error
        else:
            raise RuntimeError(
                '[Scale::__init__()] Unknown scale type "'\
                + scale_type\
                + '"!'
            )

    def add_height(self, height:Height) -> None:
        """
        Add new height to scale.

        :height: Height to add to scale.
        """
        self._heights.append(heaight)
        self._heights.sort(key=lambda x: x.cents, reverse=True)

    def set_detune(self, detune:int) -> None:
        """
        Set detune to all heights of the scale.

        :detune: Detune from 440Hz.
        """
        self._detune = abs(detune)

    def add_detune(self, detune:int) -> None:
        """
        Add detune to all heights of the scale.

        :detune: Detune from previous value.
        """
        self._detune = abs(self._detune + detune)

    def get_heights(
        self,
        from_height:Height,
        to_height:Height,
        detune=0
    ) -> list:
        octave_shift = 0
        while self._heights[-1].get_cents_from_a()\
                + 1200*octave_shift\
                + self._detune\
                + detune\
                > from_height.get_cents_from_a():
            octave_shift -= 1
        possible_heights = list()
        while self._heights[0].get_cents_from_a()\
                + 1200*octave_shift\
                + self._detune\
                + detune\
                < to_height.get_cents_from_a():
            for height in self._heights:
                if from_height.get_cents_from_a()\
                        <= height.get_cents_from_a()\
                        + 1200*octave_shift\
                        + self._detune\
                        + detune\
                        <= to_height.get_cents_from_a():
                    possible_heights.append(
                        height.copy(
                            detune=1200*octave_shift + self._detune + detune
                        )
                    )
            octave_shift += 1
        return possible_heights
