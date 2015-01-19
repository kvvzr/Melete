import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from sqlalchemy.dialects import mysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://orpheus:kumapanda@localhost/orpheus'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    screen_name = db.Column(db.String(255), nullable=False)
    passwd = db.Column(db.String(255), nullable=False)
    icon_path = db.Column(db.String(2048), nullable=True, default=None)

    def __init__(self, name, screen_name, passwd, icon_path):
        self.name = name
        self.screen_name = screen_name
        self.passwd = passwd
        self.icon_path = icon_path

class Rhythms(db.Model):
    __tablename__ = 'rhythms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Chords(db.Model):
    __tablename__ = 'chords'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Accoms(db.Model):
    __tablename__ = 'accoms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Drums(db.Model):
    __tablename__ = 'drums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Musics(db.Model):
    __tablename__ = 'musics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    raw_midi_path = db.Column(db.String(2048), nullable=True, default=None)
    fork_count = db.Column(db.Integer, nullable=False, default=0)
    fork_from = db.Column(db.Integer, nullable=True, default=None)
    star_count = db.Column(db.Integer, nullable=False, default=0)
    play_count = db.Column(db.Integer, nullable=False, default=0)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, raw_midi_path, data, user_id):
        self.name = name
        self.raw_midi_path = raw_midi_path
        self.data = data
        self.user_id = user_id

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

class StaredChords(db.Model):
    __tablename__ = 'stared_chords'
    id = db.Column(db.Integer, primary_key=True)
    chords_id = db.Column(db.Integer, db.ForeignKey('chords.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

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

class ChordComments(db.Model):
    __tablename__ = 'chord_comments'
    id = db.Column(db.Integer, primary_key=True)
    chords_id = db.Column(db.Integer, db.ForeignKey('chords.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String(1023), nullable=False)

class AccomComments(db.Model):
    __tablename__ = 'accom_comments'
    id = db.Column(db.Integer, primary_key=True)
    accoms_id = db.Column(db.Integer, db.ForeignKey('accoms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String(1023), nullable=False)

class DrumComments(db.Model):
    __tablename__ = 'drum_comments'
    id = db.Column(db.Integer, primary_key=True)
    drums_id = db.Column(db.Integer, db.ForeignKey('drums.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String(1023), nullable=False)

class MusicComments(db.Model):
    __tablename__ = 'music_comments'
    id = db.Column(db.Integer, primary_key=True)
    music_id = db.Column(db.Integer, db.ForeignKey('musics.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String(1023), nullable=False)

