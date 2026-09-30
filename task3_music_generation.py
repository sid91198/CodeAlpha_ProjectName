
import glob
import pickle
import numpy as np
try:
    from music21 import converter, instrument, note, chord, stream  
except ImportError as exc:
    raise SystemExit(
        "music21 is required. Install it with: python -m pip install music21"
    ) from exc
try:
    from tensorflow.keras.layers import LSTM, Dense, Dropout  # type: ignore[reportMissingModuleSource]
    from tensorflow.keras.models import Sequential  # type: ignore[reportMissingModuleSource]
    from tensorflow.keras.utils import to_categorical  # type: ignore[reportMissingImports]
except ImportError as exc:
    raise SystemExit(
        "TensorFlow/Keras is required. Install it with: python -m pip install tensorflow"
    ) from exc

MIDI_DIR = "midi_data/*.mid"
SEQ_LEN = 50
EPOCHS = 30
BATCH = 64
GEN_NOTES = 200



def load_notes():
    notes = []
    for file in glob.glob(MIDI_DIR):
        midi = converter.parse(file)
        parts = instrument.partitionByInstrument(midi)
        elements = parts.parts[0].recurse() if parts else midi.flat.notes
        for el in elements:
            if isinstance(el, note.Note):
                notes.append(str(el.pitch))
            elif isinstance(el, chord.Chord):
                notes.append(".".join(str(n) for n in el.normalOrder))
    if not notes:
        raise SystemExit("midi_data/ folder me .mid files nahi mili.")
    return notes


def prepare_sequences(notes, vocab):
    note_to_int = {n: i for i, n in enumerate(vocab)}
    X, y = [], []
    for i in range(len(notes) - SEQ_LEN):
        X.append([note_to_int[n] for n in notes[i:i + SEQ_LEN]])
        y.append(note_to_int[notes[i + SEQ_LEN]])
    X = np.reshape(X, (len(X), SEQ_LEN, 1)) / float(len(vocab))
    return X, to_categorical(y, num_classes=len(vocab))



def build_model(vocab_size):
    model = Sequential([
        LSTM(256, input_shape=(SEQ_LEN, 1), return_sequences=True),
        Dropout(0.3),
        LSTM(256),
        Dropout(0.3),
        Dense(256, activation="relu"),
        Dense(vocab_size, activation="softmax"),
    ])
    model.compile(loss="categorical_crossentropy", optimizer="adam")
    return model



def generate(model, notes, vocab):
    int_to_note = {i: n for i, n in enumerate(vocab)}
    note_to_int = {n: i for i, n in enumerate(vocab)}
    seq = [note_to_int[n] for n in notes]
    start = np.random.randint(0, len(seq) - SEQ_LEN)
    pattern = seq[start:start + SEQ_LEN]
    output = []
    for _ in range(GEN_NOTES):
        x = np.reshape(pattern, (1, SEQ_LEN, 1)) / float(len(vocab))
        idx = np.argmax(model.predict(x, verbose=0))
        output.append(int_to_note[idx])
        pattern = pattern[1:] + [idx]
    return output


def to_midi(pred, path="generated_music.mid"):
    offset, out = 0, []
    for p in pred:
        if "." in p or p.isdigit():
            chord_notes = []
            for n in p.split("."):
                nn = note.Note(int(n))
                nn.storedInstrument = instrument.Piano()
                chord_notes.append(nn)
            c = chord.Chord(chord_notes)
            c.offset = offset
            out.append(c)
        else:
            n = note.Note(p)
            n.offset = offset
            n.storedInstrument = instrument.Piano()
            out.append(n)
        offset += 0.5
    stream.Stream(out).write("midi", fp=path)
    print(f"Saved: {path}")


if __name__ == "__main__":
    notes = load_notes()
    vocab = sorted(set(notes))
    pickle.dump((notes, vocab), open("notes.pkl", "wb"))
    X, y = prepare_sequences(notes, vocab)
    model = build_model(len(vocab))
    model.fit(X, y, epochs=EPOCHS, batch_size=BATCH)   # 4. Train
    model.save("music_model.h5")
    to_midi(generate(model, notes, vocab))
