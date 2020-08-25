#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class Height:
    def __init__(self, cents:float):
        """
        Musical height.

        :cents: Number of cents away from A4 (midi 69, 440Hz).
        """
        self._cents = cents

    @staticmethod
    def from_frequency(frequency:float, detune=0) -> 'Height':
        """
        Create new Height object.

        :frequency: Frequency in hertz.
        :detune: Number of cents away from given frequency.
        """
        return Height(1200*np.log2(frequency/440) + detune)

    @staticmethod
    def from_midi(midi_height_id:int, detune=0) -> 'Height':
        """
        Create new Height object.

        :midi_height_id: Midi note height value.
        :detune: Number of cents away from normal frequency.
        """
        return Height((midi_height_id - 69)*100 + detune)

    @staticmethod
    def from_name(height_name:str, detune=0) -> 'Height':
        """
        Create new Height object.

        :height_name: Note name in midi notation.
        :detune: Number of cents away from normal frequency.
        """
        octave = int(height_name[-1])
        possible_names = {
           'C': 0,
           'C#': 1,
           'ces': -1,
           'c': 0,
           'cis': 1,
           'D': 2,
           'D#': 3,
           'des': 1,
           'd': 2,
           'dis': 3,
           'E': 4,
           'E#': 5,
           'es': 3,
           'e': 4,
           'eis': 5,
           'F': 5,
           'F#': 6,
           'fes': 4,
           'f': 5,
           'fis': 6,
           'G': 7,
           'G#': 8,
           'ges': 6,
           'g': 7,
           'gis': 8,
           'A': 9,
           'A#': 10,
           'as': 8,
           'a': 9,
           'ais': 10,
           'B': 11,
           'H': 11,
           'B#': 12,
           'H#': 12,
           'b': 10,
           'h': 11,
           'his': 12
        }
        midi_id = 12*(1 + octave) + possible_names[height_name[:-1]]
        return Height.from_midi(midi_id, detune)

    @staticmethod
    def from_cents_from_a(cents:float) -> 'Height':
        """
        Create new Height object.

        :cents: Number of cents away from A4 (midi 69, 440Hz).
        """
        return Height(cents)

    @staticmethod
    def from_height(height:'Height', detune=0) -> 'Height':
        """
        Create new Height object.

        :height: Height object.
        :detune: Number of cents away from normal frequency.
        """
        return Height(height.get_cents_from_a() + detune)

    def get_cents_from_a(self) -> float:
        """
        Get distance from A4 (midi 69, 440Hz) in cents.

        :returns: Distance from A4 in cents.
        """
        return self._cents

    def get_midi_height(self) -> (int, float):
        """
        Get mini value + detune.

        :returns: Midi value, Detune in cents in range <-50, 50).
        """
        height_id = 69 + int(self._cents/100)
        detune = self._cents - 100*(height_id - 69)
        while detune >= 50:
            height_id += 1
            detune -= 100
        while detune < -50:
            height_id -= 1
            detune += 100
        return (height_id, detune)

    def get_frequency(self, detune=0) -> float:
        """
        Get frequency in hertz from the height.

        :detune: Number of cents away from original frequency.
        
        :returns: Frequency in hertz.
        """
        return np.power(2, (self._cents + detune)/1200) * 440

    def copy(self, detune=0) -> 'Height':
        return Height(self._cents + detune)

    def add_interval(self, interval:'Interval', detune=0) -> 'Height':
        return Height(self._cents + interval.get_cents() + detune)

    @staticmethod
    def lower(height1:'Height', height2:'Height'):
        if height1._cents <= height2._cents:
            return height1
        else:
            return height2

    @staticmethod
    def higher(height1:'Height', height2:'Height'):
        if height1._cents >= height2._cents:
            return height1
        else:
            return height2
