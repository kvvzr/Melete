# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

import sure
import melete.rhythm as Rhythm

Rhythm.TimeSignature(4, 2).simple.should.be.equal(4.0 / 4)
Rhythm.TimeSignature(3, 3).simple.should.be.equal(3.0 / 8)
Rhythm.TimeSignature(4, 2).to_dict()

rhythms = [[], [0], [0, 96], [0, 48, 96], [0, 48, 96, 144]]
tree = Rhythm.RhythmTree(48, 1, Rhythm.TimeSignature(4, 2), rhythms)
tree.min_mora.should.be.equal(0)
tree.max_mora.should.be.equal(4)
tree.patterns.should.be.equal([[], [0.0], [0.0, 0.5], [0.0, 0.25, 0.5], [0.0, 0.25, 0.5, 0.75]])
rhythms = [[], [0], [0, 48], [0, 24, 48], [0, 24, 48, 72]]
tree = Rhythm.RhythmTree(48, 1, Rhythm.TimeSignature(2, 2), rhythms)
tree.min_mora.should.be.equal(0)
tree.max_mora.should.be.equal(4)
tree.patterns.should.be.equal([[], [0.0], [0.0, 0.5], [0.0, 0.25, 0.5], [0.0, 0.25, 0.5, 0.75]])
