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
                chord_id = tune['chord_id']
                chords_db = Chords.query.filter_by(id=chord_id).first()
                if not chords_db:
                    return 'Chords DB Error'
                prog = Chord.ChordProg.from_dict(json.loads(chords_db.data))

                rhythm_id = tune['rhythm_id']
                rhythms_db = Rhythms.query.filter_by(id=rhythm_id).first()
                if not rhythms_db:
                    return 'Rhythms DB Error'
                rhythm_tree = Rhythm.RhythmTree.from_dict(json.loads(rhythms_db.data))

                note_range = range(int(tune['min_note']), int(tune['max_note']))

                skip_prob = float(tune['skip_prob'])
                bpm = int(tune['bpm'])

                bars = Lyrics.divide(tune['lyric'], rhythm_tree)
                beats = Lyrics.pair(bars, rhythm_tree)

                composer = Melody.Composer(ts, beats, prog, note_range, skip_prob, bpm)
                midi = Melody.concat_midi(midi, composer.compose())
        midi.save('log/test_' + dt.now().strftime('%Y-%m-%d_%H:%M:%S') + '.mid')
    except ValueError as e:
        return 'ValueError %s' % e
    except KeyError as e:
        return 'KeyError %s' % e
    return 'Hello'

if __name__ == '__main__':
    app.debug = True
    manager.run()
