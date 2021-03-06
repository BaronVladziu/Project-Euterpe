#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

import numpy as np

from notes.chord import Chord
from notes.pitch import Pitch
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
        self._volume = 1.0

    def set_sampling_frequency(self, sampling_frequency:int):
        self._sampling_frequency = sampling_frequency
        self._base_synthesizer = self._base_synthesizer.__class__(
            sampling_frequency
        )

    def set_volume(self, volume:float):
        if 0.0 <= volume <= 1.0:
            self._volume = volume
        else:
            raise ValueError(
                '[Synthesizer::set_volume('\
                + str(volume)\
                + ')] Volume value must be between 1 and 0!'
            )

    def generate_frequency(
        self,
        frequency:float,
        time:float
    ) -> np.array:
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

        # Add fades
        fade_signal = np.concatenate([
            np.zeros(int(self._sampling_frequency/20)),
            np.arange(0, 1, step=100/self._sampling_frequency, dtype=float)
        ])
        result[:len(fade_signal)] = result[:len(fade_signal)] * fade_signal
        result[-len(fade_signal):] = result[-len(fade_signal):] * np.flip(fade_signal)

        # Apply volume
        result *= self._volume

        # Check for clipping
        if np.max(np.abs(result)) > 1.0:
            print('[Synthesizer] Clipping warning!')

        return result

    def generate_pitch(self, pitch:Pitch, time:float) -> np.array:
        """
        Generate signal of given length and pitch.

        :pitch: Pitch of output sound.
        :time: Length of sound in seconds.

        :returns: Output signal.
        """
        return self.generate_frequency(pitch.get_frequency(), time)

    def generate_memory_flush(
        self,
        lowest_pitch:Pitch,
        highest_pitch:Pitch,
        min_sounds=8,
        max_sounds=12,
        sound_play_time=0.2
    ) -> np.array:
        """
        Generate series of random frequencies and random length.

        :lowest_pitch: The lowest pitch
        :highest_pitch: The highest pitch
        :min_sounds: Minimal number of sounds in a series.
        :max_sounds: Maximal number of sounds in a series.
        :sound_play_time: Length of every sound in seconds.

        :returns: Output signal.
        """
        output = np.zeros(0)
        for i in range(random.randint(min_sounds, max_sounds)):
            output = np.concatenate([
                output,
                self.generate_frequency(
                    random.uniform(
                        lowest_pitch.get_frequency(),
                        highest_pitch.get_frequency()
                    ),
                    sound_play_time
                )
            ])
        return output

    def generate_interval_up(
        self,
        lower_pitch:Pitch,
        higher_pitch:Pitch,
        play_time=0.4,
        pause_time=0.2
    ) -> np.array:
        """
        Generate signal of given interval. Play order:
        - lower for <play_time>
        - pause for <pause_time>
        - higher for <play_time>

        :lower_pitch: The lower pitch
        :higher_pitch: The higher pitch
        :play_time: Length of both sounds in seconds.
        :pause_time: Length of pause between sounds in seconds.

        :returns: Output signal.
        """
        return np.concatenate([
            self.generate_pitch(lower_pitch, play_time),
            np.zeros(int(self._sampling_frequency*pause_time)),
            self.generate_pitch(higher_pitch, play_time)
        ])

    def generate_interval_down(
        self,
        lower_pitch:Pitch,
        higher_pitch:Pitch,
        play_time=0.4,
        pause_time=0.2
    ) -> np.array:
        """
        Generate signal of given interval. Play order:
        - higher for <play_time>
        - pause for <pause_time>
        - lower for <play_time>

        :lower_pitch: The lower pitch
        :higher_pitch: The higher pitch
        :play_time: Length of both sounds in seconds.
        :pause_time: Length of pause between sounds in seconds.

        :returns: Output signal.
        """
        return np.concatenate([
            self.generate_pitch(higher_pitch, play_time),
            np.zeros(int(self._sampling_frequency*pause_time)),
            self.generate_pitch(lower_pitch, play_time)
        ])

    def generate_interval_up_hold(
        self,
        lower_pitch:Pitch,
        higher_pitch:Pitch,
        play_time=0.5,
        pause_time=0
    ) -> np.array:
        """
        Generate signal of given interval. Play order:
        - lower for <play_time>
        - pause for <pause_time>
        - lower + higher for <play_time>

        :lower_pitch: The lower pitch
        :higher_pitch: The higher pitch
        :play_time: Length of both sounds in seconds.
        :pause_time: Length of pause between sounds in seconds.

        :returns: Output signal.
        """
        return np.concatenate([
            self.generate_pitch(lower_pitch, play_time),
            np.zeros(int(self._sampling_frequency*pause_time)),
            self.generate_pitch(
                lower_pitch,
                play_time
            ) + self.generate_pitch(
                higher_pitch,
                play_time
            )
        ])

    def generate_interval_down_hold(
        self,
        lower_pitch:Pitch,
        higher_pitch:Pitch,
        play_time=0.5,
        pause_time=0
    ) -> np.array:
        """
        Generate signal of given interval. Play order:
        - higher for <play_time>
        - pause for <pause_time>
        - lower + higher for <play_time>

        :lower_pitch: The lower pitch
        :higher_pitch: The higher pitch
        :play_time: Length of both sounds in seconds.
        :pause_time: Length of pause between sounds in seconds.

        :returns: Output signal.
        """
        return np.concatenate([
            self.generate_pitch(higher_pitch, play_time),
            np.zeros(int(self._sampling_frequency*pause_time)),
            self.generate_pitch(
                lower_pitch,
                play_time
            ) + self.generate_pitch(
                higher_pitch,
                play_time
            )
        ])

    def generate_interval_together(
        self,
        lower_pitch:Pitch,
        higher_pitch:Pitch,
        play_time=1
    ) -> np.array:
        """
        Generate signal of given interval. Play order:
        - lower + higher for <play_time>

        :lower_pitch: The lower pitch
        :higher_pitch: The higher pitch
        :play_time: Length of both sounds in seconds.

        :returns: Output signal.
        """
        return self.generate_pitch(
            lower_pitch,
            play_time
        ) + self.generate_pitch(
            higher_pitch,
            play_time
        )

    def generate_chords_up(
        self,
        chords:list,
        sound_play_time=0.4,
        sound_pause_time=0,
        chord_pause_time=0
    ) -> np.array:
        """
        Generate signal of given chords.
        Pitches will be played from the lowest to the highest
        each for <play_time> seconds
        with <pause_time> seconds of silence between.

        :chords: List of chords to play.
        :sound_play_time: Length of each sound in seconds.
        :sound_pause_time: Length of pause between sounds in seconds.
        :chord_pause_time: Length of pause between chords in seconds.

        :returns: Output signal.
        """
        output = np.zeros(0)
        for chord in chords:
            for i in range(chord.get_size()):
                output = np.concatenate([
                    output,
                    self.generate_pitch(
                        chord.get_pitch(i),
                        sound_play_time
                    ),
                    np.zeros(int(
                        self._sampling_frequency*sound_pause_time
                    ))
                ])
            output = np.concatenate([
                output,
                np.zeros(int(
                    self._sampling_frequency*chord_pause_time
                ))
            ])
        return output

    def generate_chords_down(
        self,
        chords:list,
        sound_play_time=0.4,
        sound_pause_time=0,
        chord_pause_time=0
    ) -> np.array:
        """
        Generate signal of given chords.
        Pitches will be played from the highest to the lowest
        each for <play_time> seconds
        with <pause_time> seconds of silence between.

        :chords: List of chords to play.
        :sound_play_time: Length of each sound in seconds.
        :sound_pause_time: Length of pause between sounds in seconds.
        :chord_pause_time: Length of pause between chords in seconds.

        :returns: Output signal.
        """
        output = np.zeros(0)
        for chord in chords:
            for i in range(chord.get_size()):
                output = np.concatenate([
                    output,
                    self.generate_pitch(
                        chord.get_pitch(chord.get_size() - i - 1),
                        sound_play_time
                    ),
                    np.zeros(int(
                        self._sampling_frequency*sound_pause_time
                    ))
                ])
            output = np.concatenate([
                output,
                np.zeros(int(
                    self._sampling_frequency*chord_pause_time
                ))
            ])
        return output

    def generate_chords_up_hold(
        self,
        chords:list,
        sound_delay=0.4,
        chord_pause_time=0
    ) -> np.array:
        """
        Generate signal of given chords.
        Pitches will be played from the lowest to the highest
        adding new one every <sound_delay> seconds.

        :chords: List of chords to play.
        :sound_delay: Delay of next pitch.
        :chord_pause_time: Length of pause between chords in seconds.

        :returns: Output signal.
        """
        output = np.zeros(0)
        for chord in chords:
            chord_signal = np.zeros(int(
                self._sampling_frequency*sound_delay*chord.get_size()
            ))
            for i in range(chord.get_size()):
                chord_signal += np.concatenate([
                    np.zeros(int(
                        self._sampling_frequency*sound_delay*i
                    )),
                    self.generate_pitch(
                        chord.get_pitch(i),
                        sound_delay*(chord.get_size() - i)
                    )
                ])
            output = np.concatenate([
                output,
                chord_signal,
                np.zeros(int(
                    self._sampling_frequency*chord_pause_time
                ))
            ])
        return output

    def generate_chords_down_hold(
        self,
        chords:list,
        sound_delay=0.4,
        chord_pause_time=0
    ) -> np.array:
        """
        Generate signal of given chords.
        Pitches will be played from the highest to the lowest
        adding new one every <sound_delay> seconds.

        :chords: List of chords to play.
        :sound_delay: Delay of next pitch.
        :chord_pause_time: Length of pause between chords in seconds.

        :returns: Output signal.
        """
        output = np.zeros(0)
        for chord in chords:
            chord_signal = np.zeros(int(
                self._sampling_frequency*sound_delay*chord.get_size()
            ))
            for i in range(chord.get_size()):
                chord_signal += np.concatenate([
                    np.zeros(int(
                        self._sampling_frequency*sound_delay*i
                    )),
                    self.generate_pitch(
                        chord.get_pitch(chord.get_size() - i - 1),
                        sound_delay*(chord.get_size() - i)
                    )
                ])
            output = np.concatenate([
                output,
                chord_signal,
                np.zeros(int(
                    self._sampling_frequency*chord_pause_time
                ))
            ])
        return output

    def generate_chords_together(
        self,
        chords:list,
        play_time_per_sound=0.4,
        chord_pause_time=0
    ) -> np.array:
        """
        Generate signal of given chords.
        Pitches will be played together for <play_time_per_sound>*<chords.get_size()> seconds.

        :chords: List of chords to play.
        :play_time_per_sound: Length of chord in seconds divided by the number of sounds in a chord.

        :returns: Output signal.
        """
        output = np.zeros(0)
        for chord in chords:
            chord_signal = np.zeros(int(
                self._sampling_frequency*play_time_per_sound*chord.get_size()
            ))
            for i in range(chord.get_size()):
                chord_signal += self.generate_pitch(
                        chord.get_pitch(i),
                        play_time_per_sound*chord.get_size()
                    )
            output = np.concatenate([
                output,
                chord_signal,
                np.zeros(int(
                    self._sampling_frequency*chord_pause_time
                ))
            ])
        return output
