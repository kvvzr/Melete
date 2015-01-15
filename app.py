# -*- coding: utf-8 -*-

from orpheus.models import *

from datetime import datetime as dt
from flask import request, json, jsonify
import mido
import orpheus.lyrics as Lyrics
import orpheus.rhythm as Rhythm
import orpheus.chord as Chord
import orpheus.melody as Melody

# router
@app.route('/analyze_lyrics')
def analyze_lyrics():
    return jsonify({'lyrics': Lyrics.analyze(request.args.get('text', default=''))})

@app.route('/compose')
def compose():
    try:
        data = json.loads(request.args.get('data', default=''))
        if not isinstance(data, list):
            return 'Error'
        with mido.MidiFile(ticks_per_beat=48, charset='utf-8') as midi:
            for tune in data:
                pass
                ts = Rhythm.TimeSignature(int(tune['nn']), int(tune['dd']))
                # 本来はDBから情報を取ってくる
                # chord_id = tune['chord_id']
                f7 = Chord.Chord.fromName('FM7')
                gd7 = Chord.Chord.fromName('G7')
                gd7.inversion(1)
                em7 = Chord.Chord.fromName('E7')
                am = Chord.Chord.fromName('Am')
                am.inversion(1)
                prog = Chord.ChordProg(48, 4, [(f7, 0), (gd7, 192), (em7, 384), (am, 576)])

                # rhythm_id = tune['rhythm_id']
                rhythms = [[], [0], [0, 12], [0, 12, 24], [0, 12, 24, 36], [0, 6, 12, 24, 36], [0, 6, 12, 18, 24, 36], [0, 6, 12, 18, 24, 30, 36], [0, 6, 12, 18, 24, 30, 36, 42]]
                rhythm_tree = Rhythm.RhythmTree(12, 1, ts, rhythms)

                note_range = range(int(tune['min_note']), int(tune['max_note']))

                skip_prob = float(tune['skip_prob'])
                bpm = int(tune['bpm'])

                bars = Lyrics.divide(tune['lyric'], rhythm_tree)
                beats = Lyrics.pair(bars, rhythm_tree)

                composer = Melody.Composer(ts, beats, prog, note_range, skip_prob, bpm)
                midi = Melody.concatMidi(midi, composer.compose())
        midi.save('log/test_' + dt.now().strftime('%Y-%m-%d_%H:%M:%S') + '.mid')
    except ValueError:
        return 'ValueError'
    except KeyError:
        return 'KeyError'
    return 'Hello'

if __name__ == '__main__':
    app.debug = True
    manager.run()
