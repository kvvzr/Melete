# -*- coding: utf-8 -*-

import re, unicodedata
from operator import add
import MeCab
import melete.rhythm as Rhythm

# kana = u'アイウエオカ-モヤユヨラ-ロワヲンヴー' # \u30c3は1モーラとカウントされるのでこちら
kana = u'\u30a2\u30a4\u30a6\u30a8\u30aa-\u30e2\u30e4\u30e6\u30e8-\u30ed\u30ef-\u30f4\u30fc' # \u30c3は1モーラとカウントされるのでこちら
# small_kana = u'ァィゥェォャュョヮ'
small_kana = u'\u30a1\u30a3\u30a5\u30a7\u30a7\u30e3\u30e5\u30e7\u30ee'
phrase_split_chars_uni = re.compile(u'[。、,.]')
ok_chars = re.compile(u'[' + kana + small_kana + ']')
mora_pattern = re.compile(u'([' + kana + ']?[' + small_kana + ']?[\^_]?)')

def split_by_mora(kana):
    return filter(lambda i: i, re.split(mora_pattern, kana))

def count_mora(kana):
    return len(split_by_mora(kana))

def insert_accent(kana, atype):
    words = split_by_mora(kana)
    if atype == 1:
        words.insert(1, '_')
    else:
        words.insert(1, '^')
        if atype != 0 and len(words) > atype:
            words.insert(atype + 1, '_')
    return ''.join(words)

def analyze(text):
    results = []
    mecab = MeCab.Tagger('-Ounidic')

    # 小節単位に分割
    text = text.strip()
    text = re.sub(phrase_split_chars_uni, ' ', text)
    text = text.encode('utf-8').replace('\r\n', '\n').replace('\n', ' ')
    text = text.split('===')
    text = map(lambda p: p.strip(), text)
    lyrics = map(lambda p: p.split(' '), text)

    # 読みとアクセントの解析
    for i, phrases in enumerate(lyrics):
        temp = []
        for phrase in phrases:
            for word in mecab.parse(phrase).decode('utf-8').split('\n'):
                features = word.split('\t')
                if len(features) == 10:
                    atypes = []
                    acons = []
                    try:
                        # アクセント型
                        atypes = map(lambda n: unicodedata.decimal(n), features[-2].split(','))
                        acons = features[-1].split(',')
                    except TypeError:
                        # アクセントが不明
                        pass

                    prono = features[1] # 読み
                    if not prono or not re.match(ok_chars, prono):
                        continue

                    if len(atypes) > 0:
                        prono = insert_accent(prono, atypes[0])
                    temp.append(prono)
            temp.append(' ')
        results.append({'lyric': text[i], 'phoneme': '/'.join(temp).rstrip()})
    return results

def divide(lyric, rhythm_tree):
    bars = []

    bar_mora = 0
    bar = []

    for word in lyric.split('/'):
        if not word:
            continue

        if word == ' ':
            bars.append(bar)
            bar_mora = 0
            bar = []
            continue

        mora = count_mora(word)
        if bar_mora + mora > rhythm_tree.max_mora:
            bars.append(bar)
            bar_mora = mora
            bar = [word]
            continue
        bar_mora += mora
        bar.append(word)

    if bar: bars.append(bar)

    return bars

def pair(bars, rhythm_tree):
    result = []
    offset = 0
    for bar in bars:
        moras = split_by_mora(''.join(bar))
        pattern = filter(lambda p: len(p) == len(moras), rhythm_tree.patterns)
        if len(pattern) != 1:
            raise ValueError('This rhythm pattern does not match this lyric')
        pattern = map(lambda o: o + offset, pattern[0])
        result.append(zip(moras, pattern))
        offset += 1
    return Rhythm.Beats(rhythm_tree.division, offset, reduce(add, result))
