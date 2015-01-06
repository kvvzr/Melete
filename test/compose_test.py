# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

from datetime import datetime as dt
import mido
import sure
import orpheus.lyrics as Lyrics
import orpheus.rhythm as Rhythm
import orpheus.chord as Chord
import orpheus.melody as Melody

ts = Rhythm.TimeSignature(4, 2)
rhythms = [[0], [0, 96], [48, 96, 144], [0, 48, 96, 144]]
tree = Rhythm.RhythmTree(48, 1, ts, rhythms)

text = u'ぽよぽよぽよぽよぽよぽよぽよぽよ===あるう ひ もりのな か くまさん に であっ た'
lyrics = Lyrics.analyze(text)
lyrics = map(lambda l: Lyrics.divide(l, tree), lyrics)
beats = map(lambda l: Lyrics.pair(l, tree), lyrics)

f7 = Chord.Chord.fromName('FM7')
gd7 = Chord.Chord.fromName('G7')
gd7.inversion(1)
em7 = Chord.Chord.fromName('E7')
am = Chord.Chord.fromName('Am')
am.inversion(1)
prog = Chord.ChordProg(48, 4, [(f7, 0), (gd7, 192), (em7, 384), (am, 576)])

note_range = range(Chord.Scale.fromName('C4').note, Chord.Scale.fromName('A5').note)

with mido.MidiFile(ticks_per_beat=48, charset='utf-8') as midi:
    for beat in beats:
        composer = Melody.Composer(ts, beat, prog, note_range, 0.5, 180)
        midi = Melody.concatMidi(midi, composer.compose())

midi.save('log/test_' + dt.now().strftime('%Y-%m-%d_%H:%M:%S') + '.mid')
