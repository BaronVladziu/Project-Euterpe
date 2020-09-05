#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import sounddevice as sd

class Player:
    def __init__(self, sampling_frequency:int):
        self._sampling_frequency = sampling_frequency

    def set_sampling_frequency(self, sampling_frequency:int):
        self._sampling_frequency = sampling_frequency

    def play(self, signal:np.array):
        sd.play(signal, self._sampling_frequency)
