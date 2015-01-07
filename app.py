# -*- coding: utf-8 -*-

from flask import Flask, request, json, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from datetime import datetime as dt
import mido
import orpheus.lyrics as Lyrics
import orpheus.rhythm as Rhythm
import orpheus.chord as Chord
import orpheus.melody as Melody

app = Flask(__name__)

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

# db setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://orpheus:kumapanda@localhost/orpheus'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    screen_name = db.Column(db.String(255), nullable=False)
    passwd = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.LargeBinary, nullable=True, default=None)

class Rhythms(db.Model):
    __tablename__ = 'rhythms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)

class Chords(db.Model):
    __tablename__ = 'chords'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)

class Accoms(db.Model):
    __tablename__ = 'accoms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)

class Drums(db.Model):
    __tablename__ = 'drums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)

class Musics(db.Model):
    __tablename__ = 'musics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    raw_midi = db.Column(db.LargeBinary, nullable=True, default=None)
    fork_count = db.Column(db.Integer, nullable=False, default=0)
    fork_from = db.Column(db.Integer, nullable=True, default=None)
    star_count = db.Column(db.Integer, nullable=False, default=0)
    play_count = db.Column(db.Integer, nullable=False, default=0)
    data = db.Column(db.Text, nullable=False)

class StaredUsers(db.Model):
    __tablename__ = 'stared_users'
    id = db.Column(db.Integer, primary_key=True)
    stared_user_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

class StaredRhythms(db.Model):
    __tablename__ = 'stared_rhythms'
    id = db.Column(db.Integer, primary_key=True)
    rhythms_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

class StaredChords(db.Model):
    __tablename__ = 'stared_chords'
    id = db.Column(db.Integer, primary_key=True)
    chords_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

class StaredAccoms(db.Model):
    __tablename__ = 'stared_accoms'
    id = db.Column(db.Integer, primary_key=True)
    accoms_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

class StaredDrums(db.Model):
    __tablename__ = 'stared_drums'
    id = db.Column(db.Integer, primary_key=True)
    drums_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

class StaredMusics(db.Model):
    __tablename__ = 'stared_musics'
    id = db.Column(db.Integer, primary_key=True)
    music_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

class RhythmComments(db.Model):
    __tablename__ = 'rhythm_comments'
    id = db.Column(db.Integer, primary_key=True)
    rhythms_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1023), nullable=False)

class ChordComments(db.Model):
    __tablename__ = 'chord_comments'
    id = db.Column(db.Integer, primary_key=True)
    chords_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1023), nullable=False)

class AccomComments(db.Model):
    __tablename__ = 'accom_comments'
    id = db.Column(db.Integer, primary_key=True)
    accoms_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1023), nullable=False)

class DrumComments(db.Model):
    __tablename__ = 'drum_comments'
    id = db.Column(db.Integer, primary_key=True)
    drums_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1023), nullable=False)

class MusicComments(db.Model):
    __tablename__ = 'music_comments'
    id = db.Column(db.Integer, primary_key=True)
    music_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1023), nullable=False)

if __name__ == '__main__':
    app.debug = True
    manager.run()
