#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from notes.pitch import Pitch

class Chord:
    def __init__(self, pitches=list()):
        """
        Set of pitches used as a whole.
        """
        self._pitches = pitches
        self._pitches.sort(
            key=lambda x: x.get_cents_from_a()
        )

    def get_size(self) -> int:
        return len(self._pitches)

    def add_pitch(self, pitch:Pitch):
        self._pitches.append(pitch)
        self._pitches.sort(
            key=lambda x: x.get_cents_from_a()
        )

    def get_pitch(self, voice_num:int) -> Pitch:
        if voice_num < 0:
            raise ValueError(
                '[Chord::get_pitch('\
                + str(voice_num)\
                + ')] Voice number cannot be negative!'
            )
        elif voice_num >= len(self._pitches):
            raise ValueError(
                '[Chord::get_pitch('\
                + str(voice_num)\
                + ')] There is no pitch for this voice number!'
            )
        return self._pitches[voice_num]
