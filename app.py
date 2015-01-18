# -*- coding: utf-8 -*-

from orpheus.models import *

import os
import string
import random
from datetime import datetime as dt
from flask import request, json, jsonify, render_template
import mido
import orpheus.lyrics as Lyrics
import orpheus.rhythm as Rhythm
import orpheus.chord as Chord
import orpheus.melody as Melody

# router
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/watch/<int:id>')
def watch(id):
    pass

@app.route('/users/<name>')
def users(name):
    pass

@app.route('/rhythms/<int:id>')
def rhythms(id):
    pass

@app.route('/chords/<int:id>')
def chords(id):
    pass

@app.route('/accoms/<int:id>')
def accoms(id):
    pass

@app.route('/ranking')
def ranking():
    pass

@app.route('/new_entry')
def new_entry():
    pass

@app.route('/login')
def login():
    pass

@app.route('/sign_up')
def sign_up():
    pass

@app.route('/analyze_lyrics', methods=['POST'])
def analyze_lyrics():
    return jsonify({'tunes': Lyrics.analyze(request.form['text'])})

@app.route('/compose', methods=['POST'])
def compose():
    try:
        user_id = 1
        title = request.form['title']
        data = json.loads(request.form['data'])

        if not isinstance(data, list):
            return 'Error'

        with mido.MidiFile(ticks_per_beat=48, charset='utf-8') as midi:
            for tune in data:
                pass
                ts = Rhythm.TimeSignature(int(tune['nn']), int(tune['dd']))
                chord_id = tune['chord_id']
                chords_db = Chords.query.filter_by(id=chord_id).first()
                if not chords_db:
                    return ('Chords DB Error', 500)
                prog = Chord.ChordProg.from_dict(json.loads(chords_db.data))

                rhythm_id = tune['rhythm_id']
                rhythms_db = Rhythms.query.filter_by(id=rhythm_id).first()
                if not rhythms_db:
                    return ('Rhythms DB Error', 500)
                rhythm_tree = Rhythm.RhythmTree.from_dict(json.loads(rhythms_db.data))

                note_range = range(int(tune['min_note']), int(tune['max_note']))
                skip_prob = float(tune['skip_prob'])
                bpm = int(tune['bpm'])

                bars = Lyrics.divide(tune['phoneme'], rhythm_tree)
                beats = Lyrics.pair(bars, rhythm_tree)

                composer = Melody.Composer(ts, beats, prog, note_range, skip_prob, bpm)
                midi = Melody.concat_midi(midi, composer.compose())
        savepath = 'log/' + ''.join([random.choice(string.ascii_letters + string.digits) for i in range(16)]) + '.mid'
        midi.save(savepath)
        music = Musics(title, savepath, request.form['data'], user_id)
        db.session.add(music)
        db.session.commit()
    except ValueError:
        return ('Unknown Error', 500)
    except KeyError:
        return ('Unknown Error', 500)
    return ('', 204)

if __name__ == '__main__':
    app.debug = True
    app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    manager.run()
