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
        elif scale_type == '12-TET':
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
        elif scale_type == '24-TET':
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
        elif scale_type == 'Pythagorean':
            self._heights.append(Height.from_midi(57))
            self._heights.append(Height.from_midi(58, -9.78))
            self._heights.append(Height.from_midi(59, 3.91))
            self._heights.append(Height.from_midi(60, -5.87))
            self._heights.append(Height.from_midi(61, 7.82))
            self._heights.append(Height.from_midi(62, -1.96))
            self._heights.append(Height.from_midi(63, -11.73))
            self._heights.append(Height.from_midi(63, 11.73))
            self._heights.append(Height.from_midi(64, 1.96))
            self._heights.append(Height.from_midi(65, -7.82))
            self._heights.append(Height.from_midi(66, 5.87))
            self._heights.append(Height.from_midi(67, -3.91))
            self._heights.append(Height.from_midi(68, 9.78))
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
        self._detune = detune

    def add_detune(self, detune:int) -> None:
        """
        Add detune to all heights of the scale.

        :detune: Detune from previous value.
        """
        self._detune += detune

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
