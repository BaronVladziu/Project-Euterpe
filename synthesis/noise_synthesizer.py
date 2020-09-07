#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy.signal

from notes.pitch import Pitch
from notes.interval import Interval

class NoiseSynthesizer:
    def __init__(self, sampling_frequency:int):
        """
        Class for sine signal generation.

        :sampling_frequency: Sampling rate in hertz.
        """
        self._sampling_frequency = sampling_frequency

    def generate_frequency(self, frequency:float, time:float, volume=10) -> np.array:
        """
        Generate noise signal of given frequency and length filtered with narrow bandpass filter.

        :frequency: Output signal frequency.
        :time: Length of signal in seconds.
        :volume: Gain of output signal.

        :returns: Noise signal filtered with narrow bandpass filter.
        """
        assert frequency < 2*self._sampling_frequency, \
                "[NoiseSynthesizer::generate(" \
                + str(frequency) \
                + ", " \
                + str(time) \
                + ")] Frequency of the fundamental frequency must be lower than half of sampling frequency!"
        
        # Generate white noise
        result = np.random.sample(int(self._sampling_frequency*time))

        # Create bandpass filter
        order = 3
        sos = scipy.signal.butter(
            order,
            [frequency/1.05,
            frequency*1.05],
            fs=self._sampling_frequency,
            btype='bandpass',
            output='sos')
        
        # Filter noise
        result = scipy.signal.sosfilt(sos, result)
        return volume*result
