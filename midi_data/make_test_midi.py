"""
Test ke liye simple MIDI files banata hai -> midi_data/ folder me.
Run: python make_test_midi.py
(Ye asli music nahi hai, sirf pipeline test karne ke liye hai.)
"""
import os
import random
from music21 import stream, note, instrument, chord

OUT_DIR = "midi_data"
os.makedirs(OUT_DIR, exist_ok=True)
random.seed(42)

SCALES = {
    "C_major": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
    "A_minor": ["A3", "B3", "C4", "D4", "E4", "F4", "G4", "A4"],
    "G_major": ["G3", "A3", "B3", "C4", "D4", "E4", "F#4", "G4"],
    "D_minor": ["D4", "E4", "F4", "G4", "A4", "B-4", "C5", "D5"],
}


def make_song(scale, n=300):
    s = stream.Stream()
    s.append(instrument.Piano())
    motif = [random.randrange(len(scale)) for _ in range(4)]
    idx = random.randrange(len(scale))
    for i in range(n):
        if i % 8 < 4:                       # motif repeat (pattern jo model seekh sake)
            idx = motif[i % 4]
        else:                               # baaki hissa random walk
            idx = max(0, min(len(scale) - 1, idx + random.choice([-2, -1, 0, 1, 2])))
        if i % 16 == 15:                    # har 16 note baad ek chord
            s.append(chord.Chord([scale[0], scale[2], scale[4]], quarterLength=1))
        else:
            s.append(note.Note(scale[idx], quarterLength=random.choice([0.5, 0.5, 1])))
    return s


count = 0
for name, scale in SCALES.items():
    for k in range(1, 3):                   # har scale ki 2 files = total 8
        path = os.path.join(OUT_DIR, f"{name}_{k}.mid")
        make_song(scale).write("midi", fp=path)
        count += 1
        print("Created:", path)

print(f"\nDone! {count} MIDI files '{OUT_DIR}/' me ban gayi.")
