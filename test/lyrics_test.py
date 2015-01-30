# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

import sure
import melete.lyrics as Lyrics
import melete.rhythm as Rhythm

Lyrics.split_by_mora(u'ニャーンカッパ').should.be.equal([u'ニャ', u'ー', u'ン', u'カ', u'ッ', u'パ'])
Lyrics.split_by_mora(u'ニャ_ーン^カッ_パ').should.be.equal([u'ニャ_', u'ー', u'ン^', u'カ', u'ッ_', u'パ'])

Lyrics.insert_accent(u'ハシ', 1).should.be.equal(u'ハ_シ')
Lyrics.insert_accent(u'ハシ', 2).should.be.equal(u'ハ^シ_')
Lyrics.insert_accent(u'ハシ', 0).should.be.equal(u'ハ^シ')

Lyrics.analyze(u'お釣り') #アクセント型がない
l = Lyrics.analyze(u'矢澤にこ===星空凛')
l[0]['phoneme'].should.be.equal(u'ヤ^ザワ/ニ^コ_/')
l[1]['phoneme'].should.be.equal(u'ホ^シゾラ/リ_ン/')

rhythms = [
    [],
    [0],
    [0, 12],
    [12, 24, 36],
    [0, 12, 24, 36],
    [0, 6, 12, 24, 36],
    [0, 6, 12, 18, 24, 36],
    [0, 6, 12, 18, 24, 30, 36],
    [0, 6, 12, 18, 24, 30, 36, 42]
]
rhythm_tree = Rhythm.RhythmTree(12, 1, Rhythm.TimeSignature(4, 2), rhythms)
lyric = u'ア^イウ/ア^イウエ/ア^イウエ_オ/ /カキク/ / /'
bars = Lyrics.divide(lyric, rhythm_tree)
bars.should.be.equal([[u'ア^イウ', u'ア^イウエ'], [u'ア^イウエ_オ'], [u'カキク'], []])

pairs = [
    (u'ア^', 0.0),
    (u'イ', 0.125),
    (u'ウ', 0.25),
    (u'ア^', 0.375),
    (u'イ', 0.5),
    (u'ウ', 0.625),
    (u'エ', 0.75),
    (u'ア^', 1.0),
    (u'イ', 1.125),
    (u'ウ', 1.25),
    (u'エ_', 1.5),
    (u'オ', 1.75),
    (u'カ', 2.25),
    (u'キ', 2.5),
    (u'ク', 2.75),
]
beats = Lyrics.pair(bars, rhythm_tree)
beats.division.should.be.equal(rhythm_tree.division)
beats.time.should.be.equal(4)
beats.pairs.should.be.equal(pairs)
