# -*- coding: utf-8 -*-

import re

roots = 'C-D-EF-G-A-B'
chord_pattern = re.compile(u'(?P<root>[CDEFGAB])(?P<accidental>[♯♭])?(?P<type>\w+)?')
scale_pattern = re.compile(u'(?P<root>[CDEFGAB])(?P<accidental>[♯♭])?(?P<octave>[0-9\-]+)?')

class Chord:
    def __init__(self, root, chord_type):
        self.root = root
        self.chord_type = chord_type
        self.sounds = []
        if chord_type == None:
            self.sounds.extend([root, root + 4, root + 7])
        if chord_type == 'm':
            self.sounds.extend([root, root + 3, root + 7])
        if chord_type == 'dim':
            self.sounds.extend([root, root + 3, root + 6])
        if chord_type == '7':
            self.sounds.extend([root, root + 4, root + 7, root + 10])
        if chord_type == 'M7':
            self.sounds.extend([root, root + 4, root + 7, root + 11])

    def inversion(self, count):
        for i in range(count):
            sound = self.sounds.pop()
            self.sounds.insert(0, sound - 12)

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
    def __init__(self, division, time, pair):
        self.division = division
        self.time = time
        self.pair = map(lambda p: (p[0], float(p[1]) / (division * 4)), pair)

    def current(self, elapsed):
        elapsed = elapsed % self.time
        for (chord, offset) in reversed(self.pair):
            if offset <= elapsed:
                return chord
        return None

class Scale:
    def __init__(self, note):
        self.note = note

    @classmethod
    def fromName(self, name):
        match = re.match(scale_pattern, name)
        if not match:
            return None
        root = roots.find(match.group('root'))
        accidental = match.group('accidental')
        if accidental == u'♯':
            root += 1
        elif accidental == u'♭':
            root -= 1
        octave = int(match.group('octave')) + 2
        return Scale(root + octave * 12)
