#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random

from notes.chord import Chord
from notes.chord_generator import ChordGenerator
from notes.height import Height
from notes.interval import Interval
from notes.scale import Scale
from synthesis.player import Player
from synthesis.synthesizer import Synthesizer

class DetuningExample:
    def __init__(self, detuning:float):
        self.chords = list()
        self.detuning = detuning

    def add_chord(self, chord:Chord):
        if len(self.chords) > 0\
                and chord.get_size() != self.chords[0].get_size():
            raise RuntimeError(
                '[DetuningExample::add_chord()] Inconsistent chord sizes!'
            )
        self.chords.append(chord)

    def get_chord_size(self) -> int:
        return self.chords[0].get_size()

    def get_voice_length(self) -> int:
        return len(self.chords)

    def get_chord(self, i:int) -> Chord:
        return self.chords[i]

    def get_height(self, chord_num:int, voice_num:int) -> Height:
        return self.chords[chord_num].get_height(voice_num)

    def get_detuning(self) -> float:
        return self.detuning


class DetuningExercise:
    def __init__(self, sampling_frequency:int):
        # exercise settings
        self._sampling_frequency = sampling_frequency
        self._volume = None
        self._play_type = None
        self._scale = None
        self._max_detuning = None
        self._lowest_height = None
        self._highest_height = None
        self._smallest_interval = None
        self._largest_interval = None
        self._synthesizer = Synthesizer(sampling_frequency)
        self._possible_error = None
        self._chord_size = None
        self._voice_length = None

        # other variables
        self._actual_example = None
        self._player = Player(sampling_frequency)

    def set_sampling_frequency(self, sampling_frequency:int):
        self._sampling_frequency = sampling_frequency
        self._synthesizer.set_sampling_frequency(sampling_frequency)
        self._player.set_sampling_frequency(sampling_frequency)

    def set_volume(self, volume:float):
        self._volume = volume
        self._synthesizer.set_volume(volume)

    def set_play_type(self, play_type:str):
        self._play_type = play_type

    def set_scale(self, scale:Scale):
        self._scale = scale

    def set_max_detuning(self, max_detuning:float):
        self._max_detuning = max_detuning

    def set_lowest_height(self, lowest_height:Height):
        self._lowest_height = lowest_height

    def set_highest_height(self, highest_height:Height):
        self._highest_height = highest_height

    def set_smallest_interval(self, smallest_interval:Interval):
        self._smallest_interval = smallest_interval

    def set_largest_interval(self, largest_interval:Interval):
        self._largest_interval = largest_interval

    def set_synthesizer(self, synthesizer:type):
        self._synthesizer = Synthesizer(
            self._sampling_frequency,
            synthesizer
        )

    def get_possible_error(self) -> float:
        return self._possible_error

    def set_possible_error(self, possible_error:float):
        self._possible_error = possible_error

    def get_chord_size(self) -> int:
        return self._chord_size

    def set_chord_size(self, chord_size:int):
        self._chord_size = chord_size

    def get_voice_length(self) -> int:
        return self._voice_length

    def set_voice_length(self, voice_length:int):
        self._voice_length = voice_length

    def generate_new_example(self):
        # Choose detuning
        actual_detuning = random.uniform(
            0,
            min(
                self._max_detuning,
                1200/2/len(self._scale._heights)
            )
        )

        # Generate melody
        chord_generator = ChordGenerator(
            scale=self._scale,
            lowest_height=self._lowest_height,
            highest_height=self._highest_height,
            possible_detune=0,
            smallest_interval=self._smallest_interval,
            largest_interval=self._largest_interval,
            chord_size=self._chord_size
        )
        tuned_chords = list()
        for i in range(self._voice_length):
            tuned_chords.append(
                chord_generator.generate_chord()
            )

        # Create even detuning
        number_of_sounds = len(tuned_chords) * tuned_chords[0].get_size()
        if number_of_sounds < 2:
            raise ValueError(
                '[DetuningExercise::generate_new_example()] '\
                + 'Cannot properly apply detuning to less than 2 sounds!'
            )
        number_of_lowered_sounds = int(np.ceil(number_of_sounds/3))
        
        lowered_or_unchanged_indices = np.random.choice(
            np.arange(number_of_sounds),
            2*number_of_lowered_sounds,
            replace=False
        )
        lowered_indices = lowered_or_unchanged_indices[:number_of_lowered_sounds]
        unchanged_indices = lowered_or_unchanged_indices[number_of_lowered_sounds:]
        highened_indices = np.setdiff1d(
            np.setdiff1d(
                np.arange(number_of_sounds),
                lowered_indices,
                assume_unique=True
            ),
            unchanged_indices,
            assume_unique=True
        )

        # Detune chords
        for i in range(len(tuned_chords)):
            for j in range(tuned_chords[i].get_size()):
                if i*tuned_chords[i].get_size() + j in lowered_indices:
                    tuned_chords[i]._heights[j] = tuned_chords[i]._heights[j].copy(
                        detune=-actual_detuning
                    )
                elif i*tuned_chords[i].get_size() + j in highened_indices:
                    tuned_chords[i]._heights[j] = tuned_chords[i]._heights[j].copy(
                        detune=actual_detuning
                    )

        # Add chords to example
        self._actual_example = DetuningExample(actual_detuning)
        for i in range(len(tuned_chords)):
            self._actual_example.add_chord(tuned_chords[i])

    def play_example(self):
        # Check exercise state
        if self._actual_example is None:
            raise RuntimeError(
                '[VoicesExercise::play_example()] No example to play!'
            )
        if self._play_type is None:
            raise RuntimeError(
                '[VoicesExercise::play_example()] No play type chosen!'
            )

        # Play
        signal = np.zeros(0)
        if self._play_type == 'Upwards':
            self._player.play(
                np.concatenate([
                    signal,
                    self._synthesizer.generate_chords_up(
                        self._actual_example.chords
                    )
                ])
            )
        elif self._play_type == 'Downwards':
            self._player.play(
                np.concatenate([
                    signal,
                    self._synthesizer.generate_chords_down(
                        self._actual_example.chords
                    )
                ])
            )
        elif self._play_type == 'Upwards with hold':
            self._player.play(
                np.concatenate([
                    signal,
                    self._synthesizer.generate_chords_up_hold(
                        self._actual_example.chords
                    )
                ])
            )
        elif self._play_type == 'Downwards with hold':
            self._player.play(
                np.concatenate([
                    signal,
                    self._synthesizer.generate_chords_down_hold(
                        self._actual_example.chords
                    )
                ])
            )
        elif self._play_type == 'Together':
            self._player.play(
                np.concatenate([
                    signal,
                    self._synthesizer.generate_chords_together(
                        self._actual_example.chords
                    )
                ])
            )
        else:
            raise RuntimeError(
                '[VoicesExercise::play_example()] Unknown play type!'
            )

    def answer_example(self, answer:float) -> (bool, float):
        if self._actual_example.detuning\
                + self._possible_error\
                >= answer\
                >= self._actual_example.detuning\
                - self._possible_error:
            return True, self._actual_example.detuning
        else:
            return False, self._actual_example.detuning
