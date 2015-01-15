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

class RhythmTree:
    def __init__(self, division, bar_count, rhythm, patterns):
        self.division = division
        self.bar_count = bar_count
        self.rhythm = rhythm
        self.patterns = map(lambda pattern: map(lambda p: float(p) / (division * 4 * bar_count * rhythm.simple), pattern), patterns)

        lens = map(lambda r: len(r), self.patterns)
        self.min_mora = min(lens)
        self.max_mora = max(lens)

    def to_dict(self):
        return {
            'division': self.division,
            'bar_count': self.bar_count,
            'rhythm': self.rhythm.to_dict(),
            'patterns': self.patterns
        }

class Beats:
    def __init__(self, division, time, pair):
        self.division = division
        self.time = time
        self.pair = pair

    def to_dict(self):
        return {
            'division': self.division,
            'time': self.time,
            'pair': self.pair
        }
