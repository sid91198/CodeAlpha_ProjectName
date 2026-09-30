# CodeAlpha AI Mini Projects

Four beginner-friendly AI projects built in Python, one script per task.

| Task | File | What it does |
|------|------|--------------|
| 1 | `task1_translator.py` | Language translation tool with a Tkinter UI, copy button and text-to-speech |
| 2 | `task2_faq_chatbot.py` | FAQ chatbot using NLTK preprocessing and TF-IDF cosine similarity |
| 3 | `task3_music_generation.py` | LSTM model that learns from MIDI files and generates new music |
| 4 | `task4_object_detection_tracking.py` | Real-time object detection and tracking with YOLOv8 and OpenCV |

Extra: `make_test_midi.py` creates simple sample MIDI files in `midi_data/` for testing Task 3.

## Setup

Python 3.10 or 3.11 is recommended (TensorFlow for Task 3 may not install on newer versions).

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## How to run

- Task 1: `python task1_translator.py`
- Task 2: `python task2_faq_chatbot.py` (type `quit` to exit)
- Task 3: `python make_test_midi.py` then `python task3_music_generation.py` (output: `generated_music.mid`)
- Task 4: `python task4_object_detection_tracking.py` (press `q` or `Esc` to quit)

## Tech stack

Python, Tkinter, deep-translator, NLTK, scikit-learn, music21, TensorFlow/Keras, Ultralytics YOLOv8, OpenCV

## Author

Neeraj Rana
