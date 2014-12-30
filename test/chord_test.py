# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

import sure
import orpheus.chord as Chord

test1 = Chord.Chord.fromName(u'C')
test1.root.should.be.equal(0)
test1.chord_type.should.be.equal(None)
test1.sounds.should.be.equal([0, 4, 7])

test2 = Chord.Chord.fromName(u'D♯')
test2.root.should.be.equal(3)
test2.chord_type.should.be.equal(None)
test2.sounds.should.be.equal([3, 7, 10])

test3 = Chord.Chord.fromName(u'A♯dim')
test3.root.should.be.equal(10)
test3.chord_type.should.be.equal(u'dim')
test3.sounds.should.be.equal([10, 13, 16])

test4 = Chord.Chord.fromName(u'B')
test4.root.should.be.equal(11)
test4.chord_type.should.be.equal(None)
test4.sounds.should.be.equal([11, 15, 18])

Chord.Chord.fromName(u'NYAN').should.be.equal(None)

f7 = Chord.Chord.fromName('FM7')
gd7 = Chord.Chord.fromName('G7')
em7 = Chord.Chord.fromName('Em7')
am = Chord.Chord.fromName('Am')
prog = Chord.ChordProg(48, 4, [(f7, 0), (gd7, 48), (em7, 96), (am, 144)])
prog.current(0).root.should.be.equal(5)
prog.current(24).root.should.be.equal(5)
prog.current(48).root.should.be.equal(7)
prog.current(96).root.should.be.equal(4)
prog.current(144).root.should.be.equal(9)
prog.current(192).root.should.be.equal(5)
prog.current(-24).root.should.be.equal(9)

Chord.Scale.fromName(u'C4').note.should.be.equal(60)
Chord.Scale.fromName(u'C♯4').note.should.be.equal(61)
Chord.Scale.fromName(u'C-1').note.should.be.equal(0)
Chord.Scale.fromName(u'NYAN').should.be.equal(None)
