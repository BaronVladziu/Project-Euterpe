#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from notes.interval import Interval

class IntervalScale:
    def __init__(self, scale_type=None):
        """
        List of avaliable musical intervals.
        """
        self._intervals = list()
        self._detune = 0

        if scale_type == None:
            pass

        elif scale_type == 'Whole Tone Fractions':
            self._intervals.append(Interval.from_cents(100.00))  # 1/2
            self._intervals.append(Interval.from_cents(50.00))  # 1/4
            self._intervals.append(Interval.from_cents(25.00))  # 1/8
            self._intervals.append(Interval.from_cents(12.50))  # 1/16
            self._intervals.append(Interval.from_cents(6.25))  # 1/32
            self._intervals.append(Interval.from_cents(3.125))  # 1/64
            self._intervals.append(Interval.from_cents(0))
        elif scale_type == 'Thirds':
            self._intervals.append(Interval.from_cents(400.00))  # 12-TET M3
            self._intervals.append(Interval.from_cents(386.31))  # 5:4
            self._intervals.append(Interval.from_cents(315.64))  # 6:5
            self._intervals.append(Interval.from_cents(300.00))  # 12-TET m3
            self._intervals.append(Interval.from_cents(266.87))  # 7:6
        elif scale_type == 'Fifths':
            self._intervals.append(Interval.from_cents(701.96))  # 3:2
            self._intervals.append(Interval.from_cents(700.00))  # TET-12 P5
            self._intervals.append(Interval.from_cents(696.77))  # TET-31 P5

        # Raise error
        else:
            raise RuntimeError(
                '[Scale::__init__()] Unknown scale type "'\
                + scale_type\
                + '"!'
            )

    def add_interval(self, interval:Interval) -> None:
        """
        Add new interval to scale.

        :interval: Interval to add to scale.
        """
        self._intervals.append(heaight)
        self._intervals.sort(key=lambda x: x.cents, reverse=True)

    def set_detune(self, detune:int) -> None:
        """
        Set detune to all intervals of the scale.

        :detune: Detune from 440Hz.
        """
        self._detune = abs(detune)

    def add_detune(self, detune:int) -> None:
        """
        Add detune to all heights of the scale.

        :detune: Detune from previous value.
        """
        self._detune = abs(self._detune + detune)

    def get_intervals(self, detune=0) -> list:
        return self._intervals
