import os, inspect, config
from functools import wraps
from flask import (
        request, 
        g, session, url_for, redirect
    )
from flask_oauthlib.client import OAuth
from melete.models import *

app = inspect.getmodule(inspect.stack()[1][0]).app
oauth = OAuth(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

twitter = oauth.remote_app(
    'twitter',
    consumer_key=os.environ.get('TWITTER_API_KEY') if 'TWITTER_API_KEY' in os.environ else config.twitter['consumer_key'],
    consumer_secret=os.environ.get('TWITTER_API_SECRET') if 'TWITTER_API_SECRET' in os.environ else config.twitter['consumer_secret'],
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

@app.route('/login/twitter')
def login_twitter():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)

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


