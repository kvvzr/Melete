# [WIP] Melete

Melete is a web service of automatic composition based on the way of [Orpheus](http://www.orpheus-music.org/v3/).

## Instration

```
$ git clone https://github.com/kvvzr/Melete
```

### OS X

#### Requirements

- Homebrew
- Python (2.7.x)

#### Install MySQL

```
$ brew install mysql55
$ brew link mysql55 --force
```

#### Install Mecab and UniDic

```
$ brew install mecab kvvzr/mecab-unidic/mecab-unidic
$ vim $(brew --cellar)/mecab/0.996/lib/mecab/dic/unidic/dicrc
```

Assign `f[9]\t%f[23]\t%f[24]\n` to `node-format-unidic`

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
