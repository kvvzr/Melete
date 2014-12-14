# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

import sure
import orpheus.lyrics as Lyrics
import orpheus.rhythm as Rhythm

Lyrics.split_by_mora(u'ニャーンカッパ').should.be.equal([u'ニャ', u'ー', u'ン', u'カ', u'ッ', u'パ'])

Lyrics.insert_accent(u'ハシ', 1).should.be.equal(u'ハ_シ')
Lyrics.insert_accent(u'ハシ', 2).should.be.equal(u'ハ^シ_')
Lyrics.insert_accent(u'ハシ', 0).should.be.equal(u'ハ^シ')

Lyrics.analyze(u'矢澤にこ===星空凛').should.be.equal([u'ヤ^ザワ/ニ^コ_/', u'ホ^シゾラ/リ_ン/'])

rhythms = [
    [],
    [0],
    [0, 12],
    [0, 12, 24],
    [0, 12, 24, 36],
    [0, 6, 12, 24, 36],
    [0, 6, 12, 18, 24, 36],
    [0, 6, 12, 18, 24, 30, 36],
    [0, 6, 12, 18, 24, 30, 36, 42]
]
rhythm_tree = Rhythm.RhythmTree(48, 1, Rhythm.TimeSignature(4, 2), rhythms)
lyric = u'ア^イウ/ア^イウエ/ア^イウエ_オ/ /カキク/ / /'
bars = Lyrics.divide(lyric, rhythm_tree)
bars.should.be.equal([[u'ア^イウ', u'ア^イウエ'], [u'ア^イウエ_オ'], [u'カキク'], []])

pair = Lyrics.pair(bars, rhythm_tree)
answer = [
    (u'ア^', 0),
    (u'イ', 6),
    (u'ウ', 12),
    (u'ア^', 18),
    (u'イ', 24),
    (u'ウ', 30),
    (u'エ', 36),
    (u'ア^', 48),
    (u'イ', 54),
    (u'ウ', 60),
    (u'エ_', 72),
    (u'オ', 84),
    (u'カ', 96),
    (u'キ', 108),
    (u'ク', 120),
]
pair.should.be.equal(answer)
