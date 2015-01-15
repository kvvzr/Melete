class TimeSignature:
    def __init__(self, nn, dd):
        self.nn = nn
        self.dd = dd
        self.simple = nn / 2.0 ** dd

    def to_dict(self):
        return {
            'nn': self.nn,
            'dd': self.dd,
            'simple': self.simple
        }

    @classmethod
    def from_dict(self, data):
        return TimeSignature(data['nn'], data['dd'])

class RhythmTree:
    def __init__(self, division, time, rhythm, patterns):
        self.division = division
        self.time = time
        self.rhythm = rhythm
        self.patterns = map(lambda pattern: map(lambda p: float(p) / (division * 4 * time * rhythm.simple), pattern), patterns)

        lens = map(lambda r: len(r), self.patterns)
        self.min_mora = min(lens)
        self.max_mora = max(lens)

    def to_dict(self):
        return {
            'division': self.division,
            'time': self.time,
            'rhythm': self.rhythm.to_dict(),
            'patterns': self.patterns
        }

    @classmethod
    def from_dict(self, data):
        return RhythmTree(data['division'], data['time'], data['rhythm'], data['patterns'])

class Beats:
    def __init__(self, division, time, pairs):
        self.division = division
        self.time = time
        self.pairs = pairs

    def to_dict(self):
        return {
            'division': self.division,
            'time': self.time,
            'pairs': self.pairs
        }

    @classmethod
    def from_dict(self, data):
        return Beats(data['division'], data['time'], data['pairs'])
