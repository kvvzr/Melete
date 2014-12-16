# -*- coding: utf-8 -*-

import re

roots = 'C-D-EF-G-A-B'
chord_pattern = re.compile(u'(?P<root>[CDEFGAB])(?P<accidental>[♯♭])?(?P<type>\w+)?')

class Chord:
    def __init__(self, root, chord_type):
        self.root = root
        self.chord_type = chord_type

    @classmethod
    def fromName(self, name):
        match = re.match(chord_pattern, name)
        if not match:
            return None
        root = roots.find(match.group('root'))
        accidental = match.group('accidental')
        if accidental == u'♯':
            root += 1
        elif accidental == u'♭':
            root -= 1
        chord_type = match.group('type')
        return Chord(root, chord_type)

class ChordProg:
    def __init__(self, division, pair):
        self.division = division
        self.pair = pair
