#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from scipy import signal

from notes.height import Height
from notes.interval import Interval

class TriangleSynthesizer:
    def __init__(self, sampling_frequency:int):
        """
        Class for sine signal generation.

        :sampling_frequency: Sampling rate in hertz.
        """
        self._sampling_frequency = sampling_frequency

    def generate_frequency(self, frequency:float, time:float, volume=0.2) -> np.array:
        """
        Generate triangle signal of given frequency and length.

        :frequency: Output signal frequency.
        :time: Length of signal in seconds.
        :volume: Gain of output signal.

        :returns: Triangle signal.
        """
        assert frequency < 2*self._sampling_frequency, \
                "[TriangleSynthesizer::generate(" \
                + str(frequency) \
                + ", " \
                + str(time) \
                + ")] Frequency of the fundamental frequency must be lower than half of sampling frequency!"
        signal_length = int(self._sampling_frequency*time)
        
        time = np.arange(
            int(self._sampling_frequency*time)
        ) / self._sampling_frequency
        triangle_signal = signal.sawtooth(2*np.pi*frequency*time, 0.5)
        return volume*triangle_signal
