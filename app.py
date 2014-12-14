# -*- coding: utf-8 -*-

from flask import Flask, request, json, jsonify
from flaskext.mysql import MySQL
import orpheus.lyrics as Lyrics
import orpheus.rhythm as Rhythm

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/analyze_lyrics')
def analyze_lyrics():
    return jsonify({"lyrics": Lyrics.analyze(request.args.get('text', default=''))})

@app.route('/compose')
def compose():
    try:
        data = json.loads(request.args.get('data', default=''))
        if not isinstance(data, list):
            return 'Error'
        for tune in data:
            if not 'lyric' in tune: # and not 'rhythm_id' in tune
                return 'Error'
            # 本来はDBからTreeの情報を取ってくる
            rhythms = [[], [0], [0, 12], [0, 12, 24], [0, 12, 24, 36], [0, 6, 12, 24, 36], [0, 6, 12, 18, 24, 36], [0, 6, 12, 18, 24, 30, 36], [0, 6, 12, 18, 24, 30, 36, 42]]
            rhythm_tree = Rhythm.RhythmTree(48, 1, rhythms)
            Lyrics.divide(tune['lyric'], rhythm_tree)
    except ValueError:
        return 'Error'
    return 'Hello'

if __name__ == '__main__':
    app.debug = True
    app.run()
