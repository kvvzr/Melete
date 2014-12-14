class TimeSignature:
    def __init__(self, nn, dd):
        self.nn = nn
        self.dd = dd
        self.simple = nn / 2 ** dd

class RhythmTree:
    def __init__(self, division, bar_count, rhythm, patterns):
        self.division = division
        self.bar_count = bar_count
        self.rhythm = rhythm
        self.patterns = patterns

        lens = map(lambda r: len(r), self.patterns)
        self.min_mora = min(lens)
        self.max_mora = max(lens)
