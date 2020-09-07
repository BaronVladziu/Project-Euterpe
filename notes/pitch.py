#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class Pitch:
    def __init__(self, cents:float):
        """
        Musical pitch.

        :cents: Number of cents away from A4 (midi 69, 440Hz).
        """
        self._cents = cents

    @staticmethod
    def from_frequency(frequency:float, detune=0) -> 'Pitch':
        """
        Create new Pitch object.

        :frequency: Frequency in hertz.
        :detune: Number of cents away from given frequency.
        """
        return Pitch(1200*np.log2(frequency/440) + detune)

    @staticmethod
    def from_midi(midi_pitch_id:int, detune=0) -> 'Pitch':
        """
        Create new Pitch object.

        :midi_pitch_id: Midi note pitch value.
        :detune: Number of cents away from normal frequency.
        """
        return Pitch((midi_pitch_id - 69)*100 + detune)

    @staticmethod
    def from_name(pitch_name:str, detune=0) -> 'Pitch':
        """
        Create new Pitch object.

        :pitch_name: Note name in midi notation.
        :detune: Number of cents away from normal frequency.
        """
        octave = int(pitch_name[-1])
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
        midi_id = 12*(1 + octave) + possible_names[pitch_name[:-1]]
        return Pitch.from_midi(midi_id, detune)

    @staticmethod
    def from_cents_from_a(cents:float) -> 'Pitch':
        """
        Create new Pitch object.

        :cents: Number of cents away from A4 (midi 69, 440Hz).
        """
        return Pitch(cents)

    @staticmethod
    def from_pitch(pitch:'Pitch', detune=0) -> 'Pitch':
        """
        Create new Pitch object.

        :pitch: Pitch object.
        :detune: Number of cents away from normal frequency.
        """
        return Pitch(pitch.get_cents_from_a() + detune)

    def get_cents_from_a(self) -> float:
        """
        Get distance from A4 (midi 69, 440Hz) in cents.

        :returns: Distance from A4 in cents.
        """
        return self._cents

    def get_midi_pitch(self) -> (int, float):
        """
        Get mini value + detune.

        :returns: Midi value, Detune in cents in range <-50, 50).
        """
        pitch_id = 69 + int(self._cents/100)
        detune = self._cents - 100*(pitch_id - 69)
        while detune >= 50:
            pitch_id += 1
            detune -= 100
        while detune < -50:
            pitch_id -= 1
            detune += 100
        return (pitch_id, detune)

    def get_frequency(self, detune=0) -> float:
        """
        Get frequency in hertz from the pitch.

        :detune: Number of cents away from original frequency.
        
        :returns: Frequency in hertz.
        """
        return np.power(2, (self._cents + detune)/1200) * 440

    def copy(self, detune=0) -> 'Pitch':
        return Pitch(self._cents + detune)

    def add_interval(self, interval:'Interval', detune=0) -> 'Pitch':
        return Pitch(self._cents + interval.get_cents() + detune)

    @staticmethod
    def lower(pitch1:'Pitch', pitch2:'Pitch'):
        if pitch1._cents <= pitch2._cents:
            return pitch1
        else:
            return pitch2

    @staticmethod
    def higher(pitch1:'Pitch', pitch2:'Pitch'):
        if pitch1._cents >= pitch2._cents:
            return pitch1
        else:
            return pitch2
