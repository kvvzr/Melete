# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

from pprint import pprint
import uniout
import sure
import orpheus.lyrics as Lyrics
import orpheus.rhythm as Rhythm
import orpheus.chord as Chord
import orpheus.melody as Melody

rhythms = [[0], [0, 24], [12, 24, 36], [0, 12, 24, 36]]
tree = Rhythm.RhythmTree(48, 1, Rhythm.TimeSignature(4, 2), rhythms)

text = u'あるう ひ もりのな か くまさん に であっ た ' * 2
lyrics = Lyrics.analyze(text)
lyrics = map(lambda l: Lyrics.divide(l, tree), lyrics)
beats = map(lambda l: Lyrics.pair(l, tree), lyrics)

f7 = Chord.Chord.fromName('FM7')
gd7 = Chord.Chord.fromName('G7')
em7 = Chord.Chord.fromName('Em7')
am = Chord.Chord.fromName('Am')
prog = Chord.ChordProg(48, 4, [(f7, 0), (gd7, 48), (em7, 96), (am, 144)])

note_range = range(Chord.Scale.fromName('C4').note, Chord.Scale.fromName('A5').note)

for beat in beats:
    composer = Melody.Composer(beat, prog, note_range, 0.5)
    composer.compose()
