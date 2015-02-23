# -*- coding: utf-8 -*-

import os, config
from functools import wraps
from flask import Flask, request, json, jsonify, render_template, send_from_directory, g, session, url_for, redirect, flash
from flask_oauthlib.client import OAuth
import mido
import melete.lyrics as Lyrics
import melete.rhythm as Rhythm
import melete.chord as Chord
import melete.melody as Melody
import melete.util as Util

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri
app.config['TEMPLATE_FOLDER'] = config.dirs['template']
app.config['STATIC_FOLDER'] = config.dirs['static']
app.config['MEDIA_FOLDER'] = config.dirs['media']
app.config['ICONS_FOLDER'] = config.dirs['icons']
app.config['SECRET_KEY'] = config.secret_key

# init dirs
if not os.path.exists(app.config['MEDIA_FOLDER']):
    os.makedirs(app.config['MEDIA_FOLDER'])
if not os.path.exists(app.config['ICONS_FOLDER']):
    os.makedirs(app.config['ICONS_FOLDER'])

# models
from melete.models import *

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_icon(user_id):
    login_icon_path = None
    if user_id:
        login_user = Users.query.filter_by(id=user_id).first()
        if login_user and login_user.icon_path:
            login_icon_path = login_user.icon_path
    return login_icon_path

# oauth
oauth = OAuth(app)

twitter = oauth.remote_app(
    'twitter',
    consumer_key=config.twitter['consumer_key'],
    consumer_secret=config.twitter['consumer_secret'],
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
)

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        res = session['twitter_oauth']
        return res['oauth_token'], res['oauth_token_secret']

@app.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']

# router
@app.route('/')
def index():
    login_icon_path = None
    stared_rhythms = None
    stared_chords = None

    if 'user_id' in session:
        login_icon_path = get_icon(session['user_id'])
        stared_rhythms = StaredRhythms.query.filter_by(user_id=session['user_id']).all()
        stared_chords = StaredChords.query.filter_by(user_id=session['user_id']).all()
    return render_template(
        'index.html',
        login_icon_path=login_icon_path,
        user_name=session['user_name'] if 'user_name' in session else None,
        rhythms=stared_rhythms,
        chords=stared_chords
    )

@app.route('/watch/<int:id>')
def watch(id):
    music = Musics.query.filter_by(id=id).first()
    data = json.loads(music.data)
    lyrics = map(lambda t: t['lyric'], data)

    media_path = None
    if music.media_path:
        media_path = music.media_path + '.mp3'

    login_icon_path = None
    if 'user_id' in session:
        login_icon_path = get_icon(session['user_id'])

    icon_path = get_icon(music.user_id)

    return render_template(
        'watch.html',
        title=music.name,
        lyrics=lyrics,
        media_path=media_path,
        login_icon_path=login_icon_path,
        user_name=session['user_name'] if 'user_name' in session else None,
        icon_path=icon_path
    )

@app.route('/media/<path>')
def media(path):
    return send_from_directory(app.config['MEDIA_FOLDER'], path)

@app.route('/icons/<path>')
def icons(path):
    return send_from_directory(app.config['ICONS_FOLDER'], path)

@app.route('/users/<name>')
def users(name):
    login_icon_path = None

    user = Users.query.filter_by(name=name).first()

    if 'user_id' in session:
        login_icon_path = get_icon(session['user_id'])

    musics = Musics.query.order_by(Musics.id.desc()).filter_by(user_id=user.id).limit(20).all()
    return render_template(
        'user.html',
        login_icon_path=login_icon_path,
        user_name=session['user_name'] if 'user_name' in session else None,
        user=user,
        musics=musics
    )

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
    login_icon_path = None

    if 'user_id' in session:
        login_icon_path = get_icon(session['user_id'])
    musics = Musics.query.order_by(Musics.id.desc()).limit(20).all()

    return render_template(
        'new_entry.html',
        login_icon_path=login_icon_path,
        user_name=session['user_name'] if 'user_name' in session else None,
        musics=musics
    )

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/twitter')
def login_twitter():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if 'twitter_oauth' in session:
            res = session['twitter_oauth']

            user = Users.query.filter_by(twitter_id=res['user_id']).first()
            if user is not None:
                return redirect(url_for('index'))

            name = request.form['name']
            user = Users.query.filter_by(name=name).first()
            if user is not None:
                return redirect(url_for('sign_up'))

            user = Users(name, res['screen_name'])
            user.twitter_id = res['user_id']

            icon_path = Util.save_twitter_icon(
                twitter,
                app.config['ICONS_FOLDER'],
                res['screen_name'], res['user_id']
            )
            if icon_path:
                user.icon_path = icon_path

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id
        return redirect(url_for('index'))
    else:
        return render_template('sign_up.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('twitter_oauth', None)
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('index'))

@app.route('/oauthorized')
def oauthorized():
    res = twitter.authorized_response()
    if res is None:
        return redirect(url_for('index'))
    session['twitter_oauth'] = res

    user = Users.query.filter_by(twitter_id=res['user_id']).first()
    if user is None:
        return redirect(url_for('sign_up'))

    session['user_id'] = user.id
    session['user_name'] = user.name

    return redirect(url_for('index'))

@app.route('/analyze_lyrics', methods=['POST'])
@login_required
def analyze_lyrics():
    return jsonify({'tunes': Lyrics.analyze(request.form['text'])})

@app.route('/compose', methods=['POST'])
@login_required
def compose():
    try:
        user_id = session['user_id']
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

        savepath = Util.random_string(16)
        midi.save(app.config['MEDIA_FOLDER'] + '/' + savepath + '.mid')
        os.system('timidity %s.mid -Ow -o - | lame - -b 64 %s.mp3' % (app.config['MEDIA_FOLDER'] + '/' + savepath, app.config['MEDIA_FOLDER'] + '/' + savepath))

        music = Musics(title, savepath, request.form['data'], user_id)
        db.session.add(music)
        db.session.commit()
    except ValueError as e:
        return ('Error: %s' % e, 500)
    except KeyError as e:
        return ('Error: %s' % e, 500)
    return (jsonify({'music_id': music.id}), 200)

if __name__ == '__main__':
    manager.run()
