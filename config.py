import os

db_uri = 'sqlite:///app.db'
dirs = dict(
    template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
    static = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
    media = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads/media'),
    icons = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads/icons')
)
secret_key = 'melete random string'
twitter = dict(
    consumer_key = 'xxx',
    consumer_secret = 'xxx'
)
