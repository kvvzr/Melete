# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

import sure
import orpheus.rhythm as Rhythm

Rhythm.TimeSignature(4, 2).simple.should.be.equal(4 / 4)
Rhythm.TimeSignature(3, 3).simple.should.be.equal(3 / 8)

rhythms = [[], [0], [0, 24], [0, 12, 24], [0, 12, 24, 36]]
tree = Rhythm.RhythmTree(48, 1, Rhythm.TimeSignature(4, 2), rhythms)
tree.min_mora.should.be.equal(0)
tree.max_mora.should.be.equal(4)
