# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import orpheus.lyrics as Lyrics

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/analyze_lyrics')
def analyze_lyrics():
    return jsonify({"lyrics": Lyrics.analyze(request.args.get('text', default=''))})

if __name__ == '__main__':
    app.debug = True
    app.run()
