class RhythmTree:
    def __init__(self, division, bar_count, rhythms):
        self.division = division
        self.bar_count = bar_count
        self.rhythms = rhythms

        lens = map(lambda r: len(r), self.rhythms)
        self.min_mora = min(lens)
        self.max_mora = max(lens)
