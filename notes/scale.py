#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from notes.pitch import Pitch

class Scale:
    def __init__(self, scale_type=None):
        """
        Musical scale interpreted as the list of musical pitches.
        """
        self._pitches = list()
        self._detune = 0.0

        if scale_type == None:
            pass

        elif scale_type == '12-TET (A=440Hz)':
            self._pitches.append(Pitch.from_midi(60))
            self._pitches.append(Pitch.from_midi(61))
            self._pitches.append(Pitch.from_midi(62))
            self._pitches.append(Pitch.from_midi(63))
            self._pitches.append(Pitch.from_midi(64))
            self._pitches.append(Pitch.from_midi(65))
            self._pitches.append(Pitch.from_midi(66))
            self._pitches.append(Pitch.from_midi(67))
            self._pitches.append(Pitch.from_midi(68))
            self._pitches.append(Pitch.from_midi(69))
            self._pitches.append(Pitch.from_midi(70))
            self._pitches.append(Pitch.from_midi(71))
        elif scale_type == '24-TET (A=440Hz)':
            self._pitches.append(Pitch.from_midi(60))
            self._pitches.append(Pitch.from_midi(60, 50))
            self._pitches.append(Pitch.from_midi(61))
            self._pitches.append(Pitch.from_midi(61, 50))
            self._pitches.append(Pitch.from_midi(62))
            self._pitches.append(Pitch.from_midi(62, 50))
            self._pitches.append(Pitch.from_midi(63))
            self._pitches.append(Pitch.from_midi(63, 50))
            self._pitches.append(Pitch.from_midi(64))
            self._pitches.append(Pitch.from_midi(64, 50))
            self._pitches.append(Pitch.from_midi(65))
            self._pitches.append(Pitch.from_midi(65, 50))
            self._pitches.append(Pitch.from_midi(66))
            self._pitches.append(Pitch.from_midi(66, 50))
            self._pitches.append(Pitch.from_midi(67))
            self._pitches.append(Pitch.from_midi(67, 50))
            self._pitches.append(Pitch.from_midi(68))
            self._pitches.append(Pitch.from_midi(68, 50))
            self._pitches.append(Pitch.from_midi(69))
            self._pitches.append(Pitch.from_midi(69, 50))
            self._pitches.append(Pitch.from_midi(70))
            self._pitches.append(Pitch.from_midi(70, 50))
            self._pitches.append(Pitch.from_midi(71))
            self._pitches.append(Pitch.from_midi(71, 50))
        elif scale_type == '31-TET (A=440Hz)':
            self._pitches.append(Pitch.from_midi(57))
            self._pitches.append(Pitch.from_midi(57, 1*38.71))
            self._pitches.append(Pitch.from_midi(57, 2*38.71))
            self._pitches.append(Pitch.from_midi(57, 3*38.71))
            self._pitches.append(Pitch.from_midi(57, 4*38.71))
            self._pitches.append(Pitch.from_midi(57, 5*38.71))
            self._pitches.append(Pitch.from_midi(57, 6*38.71))
            self._pitches.append(Pitch.from_midi(57, 7*38.71))
            self._pitches.append(Pitch.from_midi(57, 8*38.71))
            self._pitches.append(Pitch.from_midi(57, 9*38.71))
            self._pitches.append(Pitch.from_midi(57, 10*38.71))
            self._pitches.append(Pitch.from_midi(57, 11*38.71))
            self._pitches.append(Pitch.from_midi(57, 12*38.71))
            self._pitches.append(Pitch.from_midi(57, 13*38.71))
            self._pitches.append(Pitch.from_midi(57, 14*38.71))
            self._pitches.append(Pitch.from_midi(57, 15*38.71))
            self._pitches.append(Pitch.from_midi(57, 16*38.71))
            self._pitches.append(Pitch.from_midi(57, 17*38.71))
            self._pitches.append(Pitch.from_midi(57, 18*38.71))
            self._pitches.append(Pitch.from_midi(57, 19*38.71))
            self._pitches.append(Pitch.from_midi(57, 20*38.71))
            self._pitches.append(Pitch.from_midi(57, 21*38.71))
            self._pitches.append(Pitch.from_midi(57, 22*38.71))
            self._pitches.append(Pitch.from_midi(57, 23*38.71))
            self._pitches.append(Pitch.from_midi(57, 24*38.71))
            self._pitches.append(Pitch.from_midi(57, 25*38.71))
            self._pitches.append(Pitch.from_midi(57, 26*38.71))
            self._pitches.append(Pitch.from_midi(57, 27*38.71))
            self._pitches.append(Pitch.from_midi(57, 28*38.71))
            self._pitches.append(Pitch.from_midi(57, 29*38.71))
            self._pitches.append(Pitch.from_midi(57, 30*38.71))
        elif scale_type == 'Pythagorean (C-based) (A=440Hz)':
            self._pitches.append(Pitch.from_midi(60, -5.87))
            self._pitches.append(Pitch.from_midi(61, 7.82))
            self._pitches.append(Pitch.from_midi(62, -1.96))
            self._pitches.append(Pitch.from_midi(63, 11.73))
            self._pitches.append(Pitch.from_midi(64, 1.96))
            self._pitches.append(Pitch.from_midi(65, 15.64))
            self._pitches.append(Pitch.from_midi(66, 5.87))
            self._pitches.append(Pitch.from_midi(67, -3.91))
            self._pitches.append(Pitch.from_midi(68, 9.78))
            self._pitches.append(Pitch.from_midi(69))
            self._pitches.append(Pitch.from_midi(70, 13.69))
            self._pitches.append(Pitch.from_midi(71, 3.91))
        elif scale_type == 'Just (C-based) (A=440Hz)':
            self._pitches.append(Pitch.from_midi(60, 15.64))
            self._pitches.append(Pitch.from_midi(61, 27.37))
            self._pitches.append(Pitch.from_midi(62, 19.55))
            self._pitches.append(Pitch.from_midi(63, 31.28))
            self._pitches.append(Pitch.from_midi(64, 1.96))
            self._pitches.append(Pitch.from_midi(65, 13.69))
            self._pitches.append(Pitch.from_midi(66, 5.87))
            self._pitches.append(Pitch.from_midi(67, 17.60))
            self._pitches.append(Pitch.from_midi(68, 29.33))
            self._pitches.append(Pitch.from_midi(69))
            self._pitches.append(Pitch.from_midi(70, 11.73))
            self._pitches.append(Pitch.from_midi(71, 3.91))
        elif scale_type == 'Quarter-comma meantone (C-based) (A=440Hz)':
            self._pitches.append(Pitch.from_midi(60, 10.26))
            self._pitches.append(Pitch.from_midi(61, -13.68))
            self._pitches.append(Pitch.from_midi(62, 3.42))
            self._pitches.append(Pitch.from_midi(63, -20.53))
            self._pitches.append(Pitch.from_midi(64, -3.42))
            self._pitches.append(Pitch.from_midi(65, -27.37))
            self._pitches.append(Pitch.from_midi(66, -10.26))
            self._pitches.append(Pitch.from_midi(67, 6.84))
            self._pitches.append(Pitch.from_midi(68, -17.11))
            self._pitches.append(Pitch.from_midi(69))
            self._pitches.append(Pitch.from_midi(70, 23.95))
            self._pitches.append(Pitch.from_midi(71, -6.84))
        elif scale_type == 'Bach\'s (Werckmeister III) (A=440Hz)':
            self._pitches.append(Pitch.from_midi(60, 11.73))
            self._pitches.append(Pitch.from_midi(61, 1.96))
            self._pitches.append(Pitch.from_midi(62, 3.91))
            self._pitches.append(Pitch.from_midi(63, 5.87))
            self._pitches.append(Pitch.from_midi(64, 1.96))
            self._pitches.append(Pitch.from_midi(65, 9.78))
            self._pitches.append(Pitch.from_midi(66))
            self._pitches.append(Pitch.from_midi(67, 7.82))
            self._pitches.append(Pitch.from_midi(68, 3.91))
            self._pitches.append(Pitch.from_midi(69))
            self._pitches.append(Pitch.from_midi(70, 7.82))
            self._pitches.append(Pitch.from_midi(71, 3.91))

        # Raise error
        else:
            raise RuntimeError(
                '[Scale::__init__()] Unknown scale type "'\
                + scale_type\
                + '"!'
            )

    def add_pitch(self, pitch:Pitch) -> None:
        """
        Add new pitch to scale.

        :pitch: Pitch to add to scale.
        """
        self._pitches.append(heaight)
        self._pitches.sort(key=lambda x: x.cents, reverse=True)

    def set_detune(self, detune:float) -> None:
        """
        Set detune to all pitches of the scale.

        :detune: Detune from 440Hz.
        """
        self._detune = abs(detune)

    def add_detune(self, detune:float) -> None:
        """
        Add detune to all pitches of the scale.

        :detune: Detune from previous value.
        """
        self._detune = abs(self._detune + detune)

    def get_pitches(
        self,
        from_pitch:Pitch,
        to_pitch:Pitch,
        detune=0.0
    ) -> list:
        octave_shift = 0
        while self._pitches[-1].get_cents_from_a()\
                + 1200*octave_shift\
                + self._detune\
                + detune\
                > from_pitch.get_cents_from_a():
            octave_shift -= 1
        possible_pitches = list()
        while self._pitches[0].get_cents_from_a()\
                + 1200*octave_shift\
                + self._detune\
                + detune\
                < to_pitch.get_cents_from_a():
            for pitch in self._pitches:
                if from_pitch.get_cents_from_a()\
                        <= pitch.get_cents_from_a()\
                        + 1200*octave_shift\
                        + self._detune\
                        + detune\
                        <= to_pitch.get_cents_from_a():
                    possible_pitches.append(
                        pitch.copy(
                            detune=1200*octave_shift + self._detune + detune
                        )
                    )
            octave_shift += 1
        return possible_pitches
