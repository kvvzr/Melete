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

text = u'ぽよぽよぽよぽよぽよぽよぽよぽよ===あるう ひ もりのな か くまさん に であっ た あるう ひ もりのな か くまさん に であっ た'
lyrics = Lyrics.analyze(text)
lyrics = map(lambda l: Lyrics.divide(l['phoneme'], tree), lyrics)
beats = map(lambda l: Lyrics.pair(l, tree), lyrics)

f7 = Chord.Chord.from_name('FM7')
gd7 = Chord.Chord.from_name('G7')
gd7.inversion(1)
em7 = Chord.Chord.from_name('E7')
am = Chord.Chord.from_name('Am')
am.inversion(1)
prog = Chord.ChordProg(48, 4, [(f7, 0), (gd7, 192), (em7, 384), (am, 576)])
print prog.to_dict()

note_range = range(Chord.Scale.from_name('C4').note, Chord.Scale.from_name('A5').note)

with mido.MidiFile(ticks_per_beat=48, charset='utf-8') as midi:
    for beat in beats:
        composer = Melody.Composer(ts, beat, prog, note_range, 0.5, 180)
        midi = Melody.concat_midi(midi, composer.compose())
savepath = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(16)]) + '.mid'
midi.save('log/' + savepath)
