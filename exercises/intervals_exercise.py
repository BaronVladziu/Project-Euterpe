#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from notes.height import Height
from notes.interval import Interval
from notes.interval_generator import IntervalGenerator
from notes.scale import Scale
from synthesis.player import Player
from synthesis.synthesizer import Synthesizer

class IntervalExample:
    def __init__(self, generator_output:(Interval, Height, Height)):
        self.interval = generator_output[0]
        self.lower_height = generator_output[1]
        self.higher_height = generator_output[2]


class IntervalsExercise:
    def __init__(self, sampling_frequency:int):
        # exercise settings
        self._sampling_frequency = sampling_frequency
        self._play_type = None
        self._scale = None
        self._lowest_height = None
        self._highest_height = None
        self._smallest_interval = None
        self._largest_interval = None
        self._possible_detune = None
        self._synthesizer = Synthesizer(sampling_frequency)
        self._possible_error = None

        # other variables
        self._actual_example = None
        self._player = Player(sampling_frequency)

    def set_sampling_frequency(self, sampling_frequency:int):
        self._sampling_frequency = sampling_frequency
        self._synthesizer.set_sampling_frequency(sampling_frequency)
        self._player.set_sampling_frequency(sampling_frequency)

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

    def get_possible_error(self):
        return self._possible_error

    def set_possible_error(self, possible_error:float):
        self._possible_error = possible_error

    def generate_new_example(self):
        interval_generator = IntervalGenerator(
            scale=self._scale,
            lowest_height=self._lowest_height,
            highest_height=self._highest_height,
            possible_detune=self._possible_detune,
            smallest_interval=self._smallest_interval,
            largest_interval=self._largest_interval
        )
        self._actual_example = IntervalExample(
            interval_generator.generate_interval()
        )

    def play_example(self):
        if self._actual_example is None:
            raise RuntimeError(
                '[IntervalsExercise::play_example()] No example to play!'
            )
        if self._play_type is None:
            raise RuntimeError(
                '[IntervalsExercise::play_example()] No play type chosen!'
            )
        elif self._play_type == 'Upwards':
            self._player.play(
                self._synthesizer.generate_interval_up(
                    self._actual_example.lower_height,
                    self._actual_example.higher_height
                )
            )
        elif self._play_type == 'Downwards':
            self._player.play(
                self._synthesizer.generate_interval_down(
                    self._actual_example.lower_height,
                    self._actual_example.higher_height
                )
            )
        elif self._play_type == 'Upwards with hold':
            self._player.play(
                self._synthesizer.generate_interval_up_hold(
                    self._actual_example.lower_height,
                    self._actual_example.higher_height
                )
            )
        elif self._play_type == 'Downwards with hold':
            self._player.play(
                self._synthesizer.generate_interval_down_hold(
                    self._actual_example.lower_height,
                    self._actual_example.higher_height
                )
            )
        elif self._play_type == 'Together':
            self._player.play(
                self._synthesizer.generate_interval_together(
                    self._actual_example.lower_height,
                    self._actual_example.higher_height
                )
            )
        else:
            raise RuntimeError(
                '[IntervalsExercise::play_example()] Unknown play type!'
            )

    def answer_example(self, answer) -> (bool, float):
        if self._actual_example.interval.get_cents()\
                + self._possible_error\
                >= answer\
                >= self._actual_example.interval.get_cents()\
                - self._possible_error:
            return True, self._actual_example.interval.get_cents()
        else:
            return False, self._actual_example.interval.get_cents()
