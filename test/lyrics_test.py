# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.getcwd())

import sure
import orpheus.lyrics as Lyrics

Lyrics.split_by_mora(u'ニャーンカッパ').should.be.equal([u'ニャ', u'ー', u'ン', u'カ', u'ッ', u'パ'])

Lyrics.insert_accent(u'ハシ', 1).should.be.equal(u'ハ_シ')
Lyrics.insert_accent(u'ハシ', 2).should.be.equal(u'ハ^シ_')
Lyrics.insert_accent(u'ハシ', 0).should.be.equal(u'ハ^シ')

Lyrics.analyze(u'矢澤にこ===星空凛').should.be.equal([u'ヤ^ザワ/ニ^コ_/', u'ホ^シゾラ/リ_ン/'])
