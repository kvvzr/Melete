# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

import sure
import melete.chord as Chord

test1 = Chord.Chord.from_name(u'C')
test1.root.should.be.equal(0)
test1.chord_type.should.be.equal(None)
test1.sounds.should.be.equal([0, 4, 7])
td1 = Chord.Chord.from_dict(test1.to_dict())
td1.root.should.be.equal(0)
td1.chord_type.should.be.equal(None)
td1.sounds.should.be.equal([0, 4, 7])

test2 = Chord.Chord.from_name(u'D♯')
test2.root.should.be.equal(3)
test2.chord_type.should.be.equal(None)
test2.sounds.should.be.equal([3, 7, 10])

test3 = Chord.Chord.from_name(u'A♯dim')
test3.root.should.be.equal(10)
test3.chord_type.should.be.equal(u'dim')
test3.sounds.should.be.equal([10, 13, 16])

test4 = Chord.Chord.from_name(u'B')
test4.root.should.be.equal(11)
test4.chord_type.should.be.equal(None)
test4.sounds.should.be.equal([11, 15, 18])

test5 = Chord.Chord.from_name(u'G7')
test5.root.should.be.equal(7)
test5.chord_type.should.be.equal(u'7')
test5.sounds.should.be.equal([7, 11, 14, 17])

test5.inversion(3)
test5.sounds.should.be.equal([-1, 2, 5, 7])
(-1 % 12).should.be.equal(11)

Chord.Chord.from_name(u'NYAN').should.be.equal(None)

f7 = Chord.Chord.from_name('FM7')
gd7 = Chord.Chord.from_name('G7')
em7 = Chord.Chord.from_name('Em7')
am = Chord.Chord.from_name('Am')
prog = Chord.ChordProg(48, 4, [(f7, 0), (gd7, 192), (em7, 384), (am, 576)])
prog.pairs.should.be.equal([(f7, 0.0), (gd7, 1.0), (em7, 2.0), (am, 3.0)])
prog.current(0).root.should.be.equal(5)
prog.current(0.5).root.should.be.equal(5)
prog.current(1.0).root.should.be.equal(7)
prog.current(2.0).root.should.be.equal(4)
prog.current(3.0).root.should.be.equal(9)
prog.current(4.0).root.should.be.equal(5)
prog.current(-1.0).root.should.be.equal(9)

pd = Chord.ChordProg.from_dict(prog.to_dict())
pd.current(0).root.should.be.equal(5)
pd.current(0.5).root.should.be.equal(5)
pd.current(1.0).root.should.be.equal(7)
pd.current(2.0).root.should.be.equal(4)
pd.current(3.0).root.should.be.equal(9)
pd.current(4.0).root.should.be.equal(5)
pd.current(-1.0).root.should.be.equal(9)

Chord.Scale.from_name(u'C4').note.should.be.equal(72)
Chord.Scale.from_name(u'C♯4').note.should.be.equal(73)
Chord.Scale.from_name(u'C-1').note.should.be.equal(12)
Chord.Scale.from_name(u'NYAN').should.be.equal(None)
cd = Chord.Scale.from_dict(Chord.Scale.from_name(u'C4').to_dict())
cd.note.should.be.equal(72)
