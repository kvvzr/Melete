# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

import sure
import orpheus.chord as Chord

test1 = Chord.Chord.fromName(u'C')
test1.root.should.be.equal(0)
test1.chord_type.should.be.equal(None)

test2 = Chord.Chord.fromName(u'D♯')
test2.root.should.be.equal(3)
test2.chord_type.should.be.equal(None)

test3 = Chord.Chord.fromName(u'A♯dim')
test3.root.should.be.equal(10)
test3.chord_type.should.be.equal(u'dim')

test4 = Chord.Chord.fromName(u'B')
test4.root.should.be.equal(11)
test4.chord_type.should.be.equal(None)

Chord.Chord.fromName(u'NYAN').should.be.equal(None)
