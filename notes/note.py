#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from note_height import NoteHeight, create_note_height


class Note:
    def __init__(self, q_value):
        self.height = create_note_height(q_value)
