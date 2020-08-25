#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Interval:
    def __init__(self, cents:float):
        """
        Musical interval (distance between heights).

        :cents: Distance between heights in cents.
        """
        self._cents = cents

    @staticmethod
    def from_cents(cents:float) -> 'Interval':
        return Interval(cents)

    @staticmethod
    def from_heights(
        from_height:'Height',
        to_height:'Height',
        detune=0
    ) -> 'Interval':
        return Interval(to_height.get_cents_from_a()
            - from_height.get_cents_from_a()
            + detune
        )

    @staticmethod
    def from_name(name:str) -> 'Interval':
        if name == 'unison':
            return Interval(0)
        elif name == 'octave':
            return Interval(1200)
        else:
            raise NotImplementedError('[Interval::from_name(' +
                name +
                ')] Unknown name!'
            )

    def get_cents(self) -> float:
        """
        Get interval value in cents.

        :returns: Interval value in cents.
        """
        return self._cents

    def get_halfsteps(self) -> (int, float):
        """
        Get interval value in halfsteps + detune.

        :returns: Number of halfsteps, Detune in cents in range <-50, 50).
        """
        halfsteps = int(self._cents/100)
        detune = self._cents - 100*halfsteps
        while detune >= 50:
            halfsteps += 1
            detune -= 100
        while detune < -50:
            halfsteps -= 1
            detune += 100
        return halfsteps, detune
