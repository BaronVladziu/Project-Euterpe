#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


q_values = dict()
q_values['C'] = 48
q_values['D'] = 52
q_values['E'] = 56
q_values['F'] = 58
q_values['G'] = 62
q_values['A'] = 66
q_values['H'] = 70

shift_names = dict()
shift_names[-4] = 'bb'
shift_names[-3] = 'db'
shift_names[-2] = 'b'
shift_names[-1] = 'd'
shift_names[0] = ''
shift_names[1] = '$'
shift_names[2] = '#'
shift_names[3] = '#$'
shift_names[4] = '##'


class NoteHeight:
    def __init__(self, note_letter: str, shift_in_quatertones: int, octave: int):
        self.note_letter = note_letter.upper()
        self.shift_in_quatertones = shift_in_quatertones
        self.octave = octave

    def get_q_value(self) -> int:
        return q_values[self.note_letter] + self.octave*24 + self.shift_in_quatertones

    def get_midi_value(self) -> int:
        q_value = self.get_q_value()
        if q_value % 2 == 0:
            if q_value / 2 > 127 or q_value / 2 < 0:
                raise ValueError('Midi value out of range!')
            return int(q_value / 2)
        else:
            raise ValueError('Cannot get midi value of a quatertone!')

    def get_name(self) -> str:
        if self.note_letter == 'H' and self.shift_in_quatertones <= -2:
            note_letter = 'B'
            shift = self.shift_in_quatertones + 2
        else:
            note_letter = self.note_letter
            shift = self.shift_in_quatertones
        return note_letter + shift_names[shift] + str(self.octave)

    def get_frequency(self) -> float:
        return 440*np.power(2, (self.get_q_value() - 138) / 24)


def create_note_height(q_value: int) -> NoteHeight:
    octave = int(q_value / 24) - 2
    normalized_q_value = q_value - 24*octave
    keys = list(q_values.keys())
    for i in range(len(keys)):
        if q_values[keys[i]] > normalized_q_value:
            note_letter = keys[i-1]
            shift = normalized_q_value - q_values[keys[i-1]]
            return NoteHeight(note_letter, shift, octave)
    note_letter = 'H'
    shift = normalized_q_value - q_values['H']
    return NoteHeight(note_letter, shift, octave)
