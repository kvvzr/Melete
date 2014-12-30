import re
import mido

class Composer:
    def __init__(self, beats, chord_prog, pitch_range, skip_prob):
        self.beats = beats
        self.chords = chord_prog
        self.pitch_range = pitch_range
        self.skip_prob = skip_prob

    def compose(self):
        notes = self.createMelody()

        with mido.MidiFile(ticks_per_beat=48, charset='utf-8') as midi:
            track = mido.MidiTrack()
            track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(240)))
            elapsed = 0
            for t in range(len(self.beats.pair)):
                track.append(mido.Message('note_on', note=notes[t], time=self.beats.pair[t][1] - elapsed))
                track.append(mido.Message('note_off', note=notes[t], time=12))
                elapsed = self.beats.pair[t][1] + 12

            midi.tracks.append(track)
            midi.save('log/test5.mid')

        return

    def createMelody(self):
        dp = dict((p, [0.0] * len(self.beats.pair)) for p in self.pitch_range)
        trace = dict((p, [None] * len(self.beats.pair)) for p in self.pitch_range)

        sounds = self.chords.current(0).sounds
        for sound in sounds:
            for pitch in self.pitch_range:
                if pitch % 12 == sound % 12:
                    dp[pitch][0] = 1.0

        for t in range(len(self.beats.pair) - 1):
            for p in self.pitch_range:
                for np in range(p - 5, p + 5):
                    if np not in self.pitch_range:
                        continue

                    pair = self.beats.pair[t]
                    word = re.findall('\^|_', pair[0])
                    chord = self.chords.current(pair[1])
                    prob = dp[p][t]

                    if np in chord.sounds:
                        prob *= 0.9
                    else:
                        prob *= 0.1

                    if len(word) > 0 and word[0] == '^':
                        if np > p:
                            prob *= 0.8
                        else:
                            prob *= 0.2
                    elif len(word) > 0 and word[0] == '_':
                        if np > p:
                            prob *= 0.2
                        else:
                            prob *= 0.8
                    else:
                        if np == p:
                            prob *= 0.9
                        else:
                            prob *= 0.1

                    if prob > dp[np][t + 1]:
                        dp[np][t + 1] = prob
                        trace[np][t + 1] = p

        last_chord = self.chords.current(self.beats.pair[-1][1])
        last_probs = dict((p, dp[p][-1]) for p in self.pitch_range if p % 12 == last_chord.root)
        last_pitch = min(last_probs, key=last_probs.get)

        notes = [last_pitch]
        for t in range(len(self.beats.pair) - 1, 0, -1):
            notes.append(trace[last_pitch][t])
            last_pitch = trace[last_pitch][t]

        return list(reversed(notes))
