import os, inspect, json
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

import melete.chord as Chord
import melete.rhythm as Rhythm

app = inspect.getmodule(inspect.stack()[1][0]).app
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def seed():
    "Import system data"

    admin = Users('admin', 'admin')
    db.session.add(admin)
    db.session.commit()

    pat = [[], [0], [0, 96], [0, 48, 96], [0, 48, 96, 144]]
    tree = Rhythm.RhythmTree(48, 1, Rhythm.TimeSignature(4, 2), pat)
    rhythm = Rhythms('Rhythm 1', json.dumps(tree.to_dict()), admin.id)

    f7 = Chord.Chord.from_name('FM7')
    gd7 = Chord.Chord.from_name('G7')
    em7 = Chord.Chord.from_name('Em7')
    am = Chord.Chord.from_name('Am')
    prog = Chord.ChordProg(48, 4, [(f7, 0), (gd7, 192), (em7, 384), (am, 576)])
    chord = Chords('Chord 1', json.dumps(prog.to_dict()), admin.id)

    db.session.add(rhythm)
    db.session.add(chord)
    db.session.commit()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    screen_name = db.Column(db.String(255), nullable=False)
    icon_path = db.Column(db.String(2047), nullable=True, default=None)
    created_at = db.Column(db.DateTime, nullable=True, default=None)
    bio = db.Column(db.String(1023), nullable=True, default=None)
    status = db.Column(db.String(255), nullable=True, default=None)
    twitter_id = db.Column(db.String(255), nullable=True, default=None)

    def __init__(self, name, screen_name):
        self.screen_name = screen_name
        self.name = name
        self.created_at = datetime.now()

class Rhythms(db.Model):
    __tablename__ = 'rhythms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=None)
    tag = db.Column(db.String(2047), nullable=True, default=None)
    desc = db.Column(db.String(1023), nullable=True, default=None)
    status = db.Column(db.String(255), nullable=True, default=None)
    media_path = db.Column(db.String(255), nullable=True, default=None)

    def __init__(self, name, data, user_id):
        self.name = name
        self.data = data
        self.user_id = user_id

class Chords(db.Model):
    __tablename__ = 'chords'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=None)
    tag = db.Column(db.String(2047), nullable=True, default=None)
    desc = db.Column(db.String(1023), nullable=True, default=None)
    status = db.Column(db.String(255), nullable=True, default=None)
    media_path = db.Column(db.String(255), nullable=True, default=None)

    def __init__(self, name, data, user_id):
        self.name = name
        self.data = data
        self.user_id = user_id

class Accoms(db.Model):
    __tablename__ = 'accoms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=None)
    tag = db.Column(db.String(2047), nullable=True, default=None)
    desc = db.Column(db.String(1023), nullable=True, default=None)
    status = db.Column(db.String(255), nullable=True, default=None)
    media_path = db.Column(db.String(255), nullable=True, default=None)

class Drums(db.Model):
    __tablename__ = 'drums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=None)
    tag = db.Column(db.String(2047), nullable=True, default=None)
    desc = db.Column(db.String(1023), nullable=True, default=None)
    status = db.Column(db.String(255), nullable=True, default=None)
    media_path = db.Column(db.String(255), nullable=True, default=None)

class Musics(db.Model):
    __tablename__ = 'musics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    media_path = db.Column(db.String(255), nullable=True, default=None)
    fork_count = db.Column(db.Integer, nullable=False, default=0)
    fork_from = db.Column(db.Integer, nullable=True, default=None)
    star_count = db.Column(db.Integer, nullable=False, default=0)
    play_count = db.Column(db.Integer, nullable=False, default=0)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=None)
    tag = db.Column(db.String(2047), nullable=True, default=None)
    desc = db.Column(db.String(1023), nullable=True, default=None)
    status = db.Column(db.String(255), nullable=True, default=None)

    def __init__(self, name, media_path, data, user_id):
        self.name = name
        self.media_path = media_path
        self.data = data
        self.user_id = user_id
        self.created_at = datetime.now()

class StaredUsers(db.Model):
    __tablename__ = 'stared_users'
    id = db.Column(db.Integer, primary_key=True)
    stared_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class StaredRhythms(db.Model):
    __tablename__ = 'stared_rhythms'
    id = db.Column(db.Integer, primary_key=True)
    rhythms_id = db.Column(db.Integer, db.ForeignKey('rhythms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    rhythms = db.relationship(Rhythms, foreign_keys='StaredRhythms.rhythms_id')

    def __init__(self, rhythms_id, user_id):
        self.rhythms_id = rhythms_id
        self.user_id = user_id

class StaredChords(db.Model):
    __tablename__ = 'stared_chords'
    id = db.Column(db.Integer, primary_key=True)
    chords_id = db.Column(db.Integer, db.ForeignKey('chords.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    chords = db.relationship(Chords, foreign_keys='StaredChords.chords_id')

class StaredAccoms(db.Model):
    __tablename__ = 'stared_accoms'
    id = db.Column(db.Integer, primary_key=True)
    accoms_id = db.Column(db.Integer, db.ForeignKey('accoms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class StaredDrums(db.Model):
    __tablename__ = 'stared_drums'
    id = db.Column(db.Integer, primary_key=True)
    drums_id = db.Column(db.Integer, db.ForeignKey('drums.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class StaredMusics(db.Model):
    __tablename__ = 'stared_musics'
    id = db.Column(db.Integer, primary_key=True)
    music_id = db.Column(db.Integer, db.ForeignKey('musics.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class RhythmComments(db.Model):
    __tablename__ = 'rhythm_comments'
    id = db.Column(db.Integer, primary_key=True)
    rhythms_id = db.Column(db.Integer, db.ForeignKey('rhythms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String(1023), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=None)

class ChordComments(db.Model):
    __tablename__ = 'chord_comments'
    id = db.Column(db.Integer, primary_key=True)
    chords_id = db.Column(db.Integer, db.ForeignKey('chords.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String(1023), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=None)

class AccomComments(db.Model):
    __tablename__ = 'accom_comments'
    id = db.Column(db.Integer, primary_key=True)
    accoms_id = db.Column(db.Integer, db.ForeignKey('accoms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String(1023), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=None)

class DrumComments(db.Model):
    __tablename__ = 'drum_comments'
    id = db.Column(db.Integer, primary_key=True)
    drums_id = db.Column(db.Integer, db.ForeignKey('drums.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String(1023), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=None)

class MusicComments(db.Model):
    __tablename__ = 'music_comments'
    id = db.Column(db.Integer, primary_key=True)
    music_id = db.Column(db.Integer, db.ForeignKey('musics.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String(1023), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=None)

