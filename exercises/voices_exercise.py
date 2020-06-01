#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from notes.chord import Chord
from notes.chord_generator import ChordGenerator
from notes.height import Height
from notes.interval import Interval
from notes.scale import Scale
from synthesis.player import Player
from synthesis.synthesizer import Synthesizer

class VoicesExample:
    def __init__(self):
        self.chords = list()

    def add_chord(self, chord:Chord):
        if len(self.chords) > 0\
                and chord.get_size() != self.chords[0].get_size():
            raise RuntimeError(
                '[VoicesExample::add_chord()] Inconsistent chord sizes!'
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


class VoicesAnswer:
    def __init__(self, example:VoicesExample, answers:list):
        # Check dimention correctness
        if len(answers) != example.get_voice_length():
            raise RuntimeError(
                '[VoicesAnswer::__init__()] Inconsistent voice lengths!'
            )
        for i in range(len(answers)):
            if example.get_chord(i).get_size() != len(answers[i]):
                raise RuntimeError(
                    '[VoicesAnswer::__init__()] Inconsistent chord sizes!'
                )

        self.example = example
        self.answers = answers

    def get_height(self, chord_num:int, voice_num:int) -> (bool, Height):
        return self.answers[chord_num][voice_num], self.example.get_chord(chord_num).get_height(voice_num)


class VoicesExercise:
    def __init__(self, sampling_frequency:int):
        # exercise settings
        self._sampling_frequency = sampling_frequency
        self._volume = None
        self._play_type = None
        self._scale = None
        self._lowest_height = None
        self._highest_height = None
        self._smallest_interval = None
        self._largest_interval = None
        self._possible_detune = None
        self._synthesizer = Synthesizer(sampling_frequency)
        self._possible_error = None
        self._chord_size = None
        self._voice_length = None
        self._if_first_note_provided = None

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

    def set_lowest_height(self, lowest_height:Height):
        self._lowest_height = lowest_height

    def set_highest_height(self, highest_height:Height):
        self._highest_height = highest_height

    def set_smallest_interval(self, smallest_interval:Interval):
        self._smallest_interval = smallest_interval

    def set_largest_interval(self, largest_interval:Interval):
        self._largest_interval = largest_interval

    def set_possible_detune(self, possible_detune:float):
        self._possible_detune = possible_detune

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

    def set_if_first_note_provided(self, if_first_note_provided:bool):
        self._if_first_note_provided = if_first_note_provided

    def generate_new_example(self):
        chord_generator = ChordGenerator(
            scale=self._scale,
            lowest_height=self._lowest_height,
            highest_height=self._highest_height,
            possible_detune=self._possible_detune,
            smallest_interval=self._smallest_interval,
            largest_interval=self._largest_interval,
            chord_size=self._chord_size
        )
        self._actual_example = VoicesExample()
        for i in range(self._voice_length):
            self._actual_example.add_chord(
                chord_generator.generate_chord()
            )

    def get_first_note(self):
        if self._if_first_note_provided:
            return self._actual_example.get_height(0, 0)

    def play_example(self, memory_flush=False):
        # Check exercise state
        if self._actual_example is None:
            raise RuntimeError(
                '[VoicesExercise::play_example()] No example to play!'
            )
        if self._play_type is None:
            raise RuntimeError(
                '[VoicesExercise::play_example()] No play type chosen!'
            )
    
        # Generate memory flush
        signal = np.zeros(0)
        if memory_flush:
            signal = np.concatenate([
                signal,
                self._synthesizer.generate_memory_flush(
                    lowest_height=self._lowest_height,
                    highest_height=self._highest_height
                ),
                np.zeros(self._sampling_frequency)
            ])

        # Play
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

    def answer_example(self, user_answers:list) -> VoicesAnswer:
        # Prepare correct answers matrix
        correct_answers = list()
        for chord_id in range(self._actual_example.get_voice_length()):
            correct_answers.append(list())
            for voice_id in range(self._actual_example.get_chord_size()):
                correct_answers[-1].append(False)

        # Set hit answers to true
        for chord_id in range(self._actual_example.get_voice_length()):
            for voice_id in range(self._actual_example.get_chord_size()):
                for user_answer in user_answers[chord_id]:
                    if self._actual_example.get_height(
                        chord_id,
                        voice_id
                    ).get_cents_from_a() + self._possible_error\
                    >= user_answer\
                    >= self._actual_example.get_height(
                        chord_id,
                        voice_id
                    ).get_cents_from_a() - self._possible_error:
                        correct_answers[chord_id][voice_id] = True
                        break

        # Return answer object
        return VoicesAnswer(self._actual_example, correct_answers)
