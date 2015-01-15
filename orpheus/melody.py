import re
import mido

class Composer:
    def __init__(self, rhythm, beats, chord_prog, pitch_range, skip_prob, bpm):
        self.rhythm = rhythm
        self.beats = beats
        self.chords = chord_prog
        self.pitch_range = pitch_range
        self.skip_prob = skip_prob
        self.bpm = bpm

    def compose(self):
        notes = self.create_melody()
        tempo = int(1000000 / (self.bpm / 60.0))
        elapsed = 0

        with mido.MidiFile(ticks_per_beat=48, charset='utf-8') as midi:
            melody = mido.MidiTrack()
            melody.append(mido.MetaMessage('set_tempo', tempo=tempo))
            for t in range(len(self.beats.pairs)):
                time = int(self.beats.pairs[t][1] * 48 * 4 * self.rhythm.simple)
                note_off = int(48 * 4 * self.rhythm.simple)
                note_off = ((time + note_off) / note_off) * note_off - time
                if t + 1 < len(self.beats.pairs):
                    note_off = min(note_off, int(self.beats.pairs[t + 1][1] * 48 * 4 * self.rhythm.simple - time))
                melody.append(mido.Message('note_on', note=notes[t], time=time - elapsed))
                melody.append(mido.Message('note_off', note=notes[t], time=note_off))
                elapsed = time + note_off
            midi.tracks.append(melody)

            accom = mido.MidiTrack()
            for t in range(self.beats.time):
                for i, s in enumerate(self.chords.current(t).sounds):
                    accom.append(mido.Message('note_on', note=s + 12 * 5, time=0))
                for i, s in enumerate(self.chords.current(t).sounds):
                    offset = 0
                    if i == 0:
                        offset = int(48 * 4 * self.rhythm.simple)
                    accom.append(mido.Message('note_off', note=s + 12 * 5, time=offset))
            midi.tracks.append(accom)
        return midi

    def create_melody(self):
        dp = dict((p, [0.0] * len(self.beats.pairs)) for p in self.pitch_range)
        trace = dict((p, [None] * len(self.beats.pairs)) for p in self.pitch_range)

        sounds = self.chords.current(0).sounds
        for sound in sounds:
            for pitch in self.pitch_range:
                if pitch % 12 == sound % 12:
                    dp[pitch][0] = 1.0

        for t in range(len(self.beats.pairs) - 1):
            for p in self.pitch_range:
                for np in range(p - 5, p + 5):
                    if np not in self.pitch_range:
                        continue

                    pair = self.beats.pairs[t]
                    word = re.findall('\^|_', pair[0])
                    chord = self.chords.current(pair[1])
                    prob = dp[p][t]

                    if p % 12 in map(lambda s: s % 12, chord.sounds):
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

        last_chord = self.chords.current(self.beats.pairs[-1][1])
        last_probs = dict((p, dp[p][-1]) for p in self.pitch_range if p % 12 == last_chord.root)
        last_pitch = min(last_probs, key=last_probs.get)

        notes = [last_pitch]
        for t in range(len(self.beats.pairs) - 1, 0, -1):
            notes.append(trace[last_pitch][t])
            last_pitch = trace[last_pitch][t]

        return list(reversed(notes))

def concat_midi(head, tail):
    time = 0
    for i, track in enumerate(head.tracks):
        track_time = 0
        for message in track:
            if hasattr(message, 'time'):
                track_time += message.time
        time = max(track_time, time)

    with mido.MidiFile(ticks_per_beat=48, charset='utf-8') as midi:
        for i in range(max(len(head.tracks), len(tail.tracks))):
            track = mido.MidiTrack()
            elapsed = 0

            if i < len(head.tracks):
                for message in head.tracks[i]:
                    if message.type in ['note_on', 'note_off', 'set_tempo']:
                        track.append(message)
                        elapsed += message.time

            if i < len(tail.tracks):
                for j, message in enumerate(tail.tracks[i]):
                    if message.type in ['note_on', 'note_off', 'set_tempo']:
                        if j == 0:
                            message.time += (time - elapsed)
                        track.append(message)
            midi.tracks.append(track)

    return midi
