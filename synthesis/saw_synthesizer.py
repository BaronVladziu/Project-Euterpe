#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from notes.height import Height
from notes.interval import Interval

class SawSynthesizer:
    def __init__(self, sampling_frequency:int):
        """
        Class for sine signal generation.

        :sampling_frequency: Sampling rate in hertz.
        """
        self._sampling_frequency = sampling_frequency

    def generate_frequency(self, frequency:float, time:float, volume=0.2) -> np.array:
        """
        Generate saw signal of given frequency and length.

        :frequency: Output signal frequency.
        :time: Length of signal in seconds.
        :volume: Gain of output signal.

        :returns: Saw signal.
        """
        assert frequency < 2*self._sampling_frequency, \
                "[SawSynthesizer::generate(" \
                + str(frequency) \
                + ", " \
                + str(time) \
                + ")] Frequency of the fundamental frequency must be lower than half of sampling frequency!"
        time = np.arange(
            int(self._sampling_frequency*time)
        ) / self._sampling_frequency
        return volume*2*((frequency*time % 1.0) - 0.5)
