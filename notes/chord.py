#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from notes.height import Height

class Chord:
    def __init__(self, heights:list):
        """
        Set of heights used as a whole.
        """
        self._heights = heights
        self._heights.sort(
            key=lambda x: x.get_cents_from_a()
        )

    def get_size(self) -> int:
        return len(self._heights)

    def add_height(self, height:Height):
        self._heights.append(height)
        self._heights.sort(
            key=lambda x: x.get_cents_from_a()
        )

    def get_height(self, voice_num:int) -> Height:
        if voice_num < 0:
            raise ValueError(
                '[Chord::get_height('\
                + str(voice_num)\
                + ')] Voice number cannot be negative!'
            )
        elif voice_num >= len(self._heights):
            raise ValueError(
                '[Chord::get_height('\
                + str(voice_num)\
                + ')] There is no height for this voice number!'
            )
        return self._heights[voice_num]
