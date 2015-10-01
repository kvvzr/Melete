# [WIP] Melete

Melete is a web service of automatic composition based on the way of [Orpheus](http://www.orpheus-music.org/v3/).

## Installation

```
$ git clone https://github.com/kvvzr/Melete
```

### OS X

#### Requirements

- Homebrew
- Python (2.7.x)

#### Install Mecab and UniDic

```
$ brew install mecab kvvzr/mecab-unidic/mecab-unidic
```

#### Install Python libraries

```
$ pip install -r requirements.txt
```

#### Edit config

```
$ vim config.py
```

#### Initialize DB

```
$ python app.py db init
$ python app.py db migrate
$ python app.py db upgrade
```

#### Run server

```
$ python app.py runserver
```
