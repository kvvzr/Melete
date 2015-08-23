# -*- coding: utf-8 -*-

import re
from flask import jsonify

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
        if chord_type == '-5':
            self.sounds.extend([root, root + 4, root + 6])
        if chord_type == 'dim':
            self.sounds.extend([root, root + 3, root + 6])
        if chord_type == 'sus4':
            self.sounds.extend([root, root + 5, root + 7])
        if chord_type == 'aug':
            self.sounds.extend([root, root + 4, root + 8])
        if chord_type == '6':
            self.sounds.extend([root, root + 4, root + 7, root + 9])
        if chord_type == 'm6':
            self.sounds.extend([root, root + 3, root + 7, root + 9])
        if chord_type == '7':
            self.sounds.extend([root, root + 4, root + 7, root + 10])
        if chord_type == 'M7':
            self.sounds.extend([root, root + 4, root + 7, root + 11])
        if chord_type == 'm7':
            self.sounds.extend([root, root + 3, root + 7, root + 10])
        if chord_type == '7-5':
            self.sounds.extend([root, root + 4, root + 6, root + 10])
        if chord_type == 'dim7':
            self.sounds.extend([root, root + 3, root + 6, root + 9])
        if chord_type == '7sus4':
            self.sounds.extend([root, root + 5, root + 7, root + 10])
        if chord_type == 'aug7':
            self.sounds.extend([root, root + 4, root + 8, root + 10])
        if chord_type == 'augM7':
            self.sounds.extend([root, root + 4, root + 8, root + 11])
        if chord_type == 'add9':
            self.sounds.extend([root, root + 4, root + 7, root + 14])
        if chord_type == 'mM7':
            self.sounds.extend([root, root + 3, root + 7, root + 11])
        if chord_type == 'add2':
            self.sounds.extend([root, root + 2, root + 4, root + 7])
        if chord_type == 'add4':
            self.sounds.extend([root, root + 4, root + 5, root + 7])

    def inversion(self, count):
        for i in range(count):
            sound = self.sounds.pop()
            self.sounds.insert(0, sound - 12)

    def to_dict(self):
        return {
            'root': self.root,
            'chord_type': self.chord_type,
            'sounds': self.sounds
        }

    @classmethod
    def from_dict(self, data):
        chord = Chord(data['root'], data['chord_type'])
        chord.sounds = data['sounds']
        return chord

    @classmethod
    def from_name(self, name):
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
    def __init__(self, division, time, pairs):
        self.division = division
        self.time = time
        self.pairs = map(lambda p: (p[0], float(p[1]) / (division * 4)), pairs)

    def current(self, elapsed):
        elapsed = elapsed % self.time
        for (chord, offset) in reversed(self.pairs):
            if offset <= elapsed:
                return chord
        return None

    def to_dict(self):
        return {
            'division': self.division,
            'time': self.time,
            'chords': map(lambda p: p[0].to_dict(), self.pairs),
            'offsets': map(lambda p: p[1], self.pairs)
        }

    @classmethod
    def from_dict(self, data):
        chords = map(lambda c: Chord.from_dict(c), data['chords'])
        pairs = zip(chords, data['offsets'])
        prog =  ChordProg(data['division'], data['time'], [])
        prog.pairs = pairs
        return prog

class Scale:
    def __init__(self, note):
        self.note = note

    def to_dict(self):
        return {
            'note': self.note
        }

    @classmethod
    def from_dict(self, data):
        return Scale(data['note'])

    @classmethod
    def from_name(self, name):
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
