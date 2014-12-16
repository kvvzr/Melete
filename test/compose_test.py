# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

import sure
import orpheus.lyrics as Lyrics
import orpheus.rhythm as Rhythm
import orpheus.chord as Chord

fm7 = Chord.Chord.fromName('FM7')
g7 = Chord.Chord.fromName('G7')
em7 = Chord.Chord.fromName('Em7')
am = Chord.Chord.fromName('Am')

Chord.ChordProg(48, [(fm7, 0), (g7, 48), (em7, 96), (am, 144)])
