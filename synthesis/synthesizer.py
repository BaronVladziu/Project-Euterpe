#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy.signal

from notes.height import Height
from notes.interval import Interval
from synthesis.sine_synthesizer import SineSynthesizer

class Synthesizer:
    def __init__(
        self,
        sampling_frequency:int,
        base_synthesizer=SineSynthesizer
    ):
        """
        Class for signal generation from hights and intervals.

        :sampling_frequency: Sampling rate in hertz.
        :base_synthesizer: Any other 'synthesizer' class.
        """
        self._sampling_frequency = sampling_frequency
        self._base_synthesizer = base_synthesizer(sampling_frequency)

    def set_sampling_frequency(self, sampling_frequency:int):
        self._sampling_frequency = sampling_frequency
        self._base_synthesizer = self._base_synthesizer.__class__(
            sampling_frequency
        )

    def generate_frequency(self, frequency:float, time:float, antialiasing_order=20) -> np.array:
        """
        Generate signal of given frequency and length.

        :frequency: Output signal frequency.
        :time: Length of signal in seconds.

        :returns: Output signal.
        """
        # Generate base signal
        result = self._base_synthesizer.generate_frequency(
            frequency=frequency,
            time=time
        )

        # Create lowpass filter
        sos = scipy.signal.butter(
            antialiasing_order,
            self._sampling_frequency/2.2,
            fs=self._sampling_frequency,
            btype='lowpass',
            output='sos')
        
        # Filter base signal
        result = scipy.signal.sosfilt(sos, result)

        # Add fades
        fade_signal = np.concatenate([
            np.zeros(int(self._sampling_frequency/20)),
            np.arange(0, 1, step=100/self._sampling_frequency, dtype=float)
        ])
        result[:len(fade_signal)] = result[:len(fade_signal)] * fade_signal
        result[-len(fade_signal):] = result[-len(fade_signal):] * np.flip(fade_signal)

        return result

    def generate_height(self, height:Height, time:float) -> np.array:
        """
        Generate signal of given length and height.

        :height: Height of output sound.
        :time: Length of sound in seconds.

        :returns: Output signal.
        """
        return self.generate_frequency(height.get_frequency(), time)

    def generate_interval_up(
        self,
        lower_height:Height,
        higher_height:Height,
        play_time=0.4,
        pause_time=0.2
    ) -> np.array:
        """
        Generate signal of given interval. Play order:
        - lower for <play_time>
        - pause for <pause_time>
        - higher for <play_time>

        :interval: Interval to play.
        :play_time: Length of both sounds in seconds.
        :pause_time: Length of pause between sounds in seconds.

        :returns: Output signal.
        """
        return np.concatenate([
            self.generate_height(lower_height, play_time),
            np.zeros(int(self._sampling_frequency*pause_time)),
            self.generate_height(higher_height, play_time)
        ])

    def generate_interval_down(
        self,
        lower_height:Height,
        higher_height:Height,
        play_time=0.4,
        pause_time=0.2
    ) -> np.array:
        """
        Generate signal of given interval. Play order:
        - higher for <play_time>
        - pause for <pause_time>
        - lower for <play_time>

        :interval: Interval to play.
        :play_time: Length of both sounds in seconds.
        :pause_time: Length of pause between sounds in seconds.

        :returns: Output signal.
        """
        return np.concatenate([
            self.generate_height(higher_height, play_time),
            np.zeros(int(self._sampling_frequency*pause_time)),
            self.generate_height(lower_height, play_time)
        ])

    def generate_interval_up_hold(
        self,
        lower_height:Height,
        higher_height:Height,
        play_time=0.5,
        pause_time=0
    ) -> np.array:
        """
        Generate signal of given interval. Play order:
        - lower for <play_time>
        - pause for <pause_time>
        - lower + higher for <play_time>

        :interval: Interval to play.
        :play_time: Length of both sounds in seconds.
        :pause_time: Length of pause between sounds in seconds.

        :returns: Output signal.
        """
        return np.concatenate([
            self.generate_height(lower_height, play_time),
            np.zeros(int(self._sampling_frequency*pause_time)),
            self.generate_height(
                lower_height,
                play_time
            ) + self.generate_height(
                higher_height,
                play_time
            )
        ])

    def generate_interval_down_hold(
        self,
        lower_height:Height,
        higher_height:Height,
        play_time=0.5,
        pause_time=0
    ) -> np.array:
        """
        Generate signal of given interval. Play order:
        - higher for <play_time>
        - pause for <pause_time>
        - lower + higher for <play_time>

        :interval: Interval to play.
        :play_time: Length of both sounds in seconds.
        :pause_time: Length of pause between sounds in seconds.

        :returns: Output signal.
        """
        return np.concatenate([
            self.generate_height(higher_height, play_time),
            np.zeros(int(self._sampling_frequency*pause_time)),
            self.generate_height(
                lower_height,
                play_time
            ) + self.generate_height(
                higher_height,
                play_time
            )
        ])

    def generate_interval_together(
        self,
        lower_height:Height,
        higher_height:Height,
        play_time=1
    ) -> np.array:
        """
        Generate signal of given interval. Play order:
        - lower + higher for <play_time>

        :interval: Interval to play.
        :play_time: Length of both sounds in seconds.

        :returns: Output signal.
        """
        return self.generate_height(
            lower_height,
            play_time
        ) + self.generate_height(
            higher_height,
            play_time
        )
