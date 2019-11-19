#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from notes.note_height import NoteHeight, create_note_height
import random


def main():
    for i in range(256):
        random_note = create_note_height(i)
        print(i, random_note.get_q_value(), random_note.get_name())
        assert i == random_note.get_q_value()


if __name__ == "__main__":
    main()
