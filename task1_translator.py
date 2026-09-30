
import tkinter as tk
from tkinter import ttk, messagebox
import importlib

try:
    _deep_translator = importlib.import_module("deep_translator")
    GoogleTranslator = _deep_translator.GoogleTranslator
    MyMemoryTranslator = _deep_translator.MyMemoryTranslator
    _TRANSLATOR_ERROR = None
except ImportError as e:
    GoogleTranslator = None
    MyMemoryTranslator = None
    _TRANSLATOR_ERROR = e

try:
    import pyttsx3
    TTS = pyttsx3.init()
except Exception:
    TTS = None

if GoogleTranslator is not None:
    _raw = GoogleTranslator().get_supported_languages(as_dict=True)
else:
    _raw = {"english": "en", "hindi": "hi"}

if _raw and all(len(str(k)) <= 6 for k in _raw) and any(len(str(v)) > 6 for v in _raw.values()):
    _raw = {v: k for k, v in _raw.items()}
LANGS = {str(k).lower(): v for k, v in _raw.items()}  # {'english': 'en', ...}
NAMES = ["auto detect"] + sorted(LANGS.keys())
DEFAULT_TGT = "hindi" if "hindi" in LANGS else NAMES[1]


def translate():
    if _TRANSLATOR_ERROR is not None:
        messagebox.showerror(
            "Missing package",
            "Install the required package first:\n\npip install deep-translator",
        )
        return
    text = input_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Empty", "Pehle text enter karein.")
        return
    src = "auto" if src_var.get() == "auto detect" else LANGS[src_var.get()]
    tgt = LANGS[tgt_var.get()]
    try:
        try:
            result = GoogleTranslator(source=src, target=tgt).translate(text)
        except Exception:
            
            s = "english" if src == "auto" else src_var.get()
            result = MyMemoryTranslator(source=s, target=tgt_var.get()).translate(text)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)
    output_box.config(state="disabled")


def copy_text():
    root.clipboard_clear()
    root.clipboard_append(output_box.get("1.0", tk.END).strip())
    messagebox.showinfo("Copied", "Translated text copy ho gaya.")


def speak():
    if TTS is None:
        messagebox.showinfo("TTS", "pip install pyttsx3 karein.")
        return
    TTS.say(output_box.get("1.0", tk.END).strip())
    TTS.runAndWait()


root = tk.Tk()
root.title("Language Translation Tool")
root.geometry("600x520")

top = tk.Frame(root)
top.pack(pady=10)
src_var = tk.StringVar(value="auto detect")
tgt_var = tk.StringVar(value=DEFAULT_TGT)
ttk.Combobox(top, textvariable=src_var, values=NAMES, width=18, state="readonly").grid(row=0, column=0, padx=5)
tk.Label(top, text="→").grid(row=0, column=1)
ttk.Combobox(top, textvariable=tgt_var, values=NAMES[1:], width=18, state="readonly").grid(row=0, column=2, padx=5)

tk.Label(root, text="Input text").pack(anchor="w", padx=15)
input_box = tk.Text(root, height=8, wrap="word")
input_box.pack(fill="x", padx=15)

tk.Button(root, text="Translate", command=translate, bg="#2563eb", fg="white").pack(pady=10)

tk.Label(root, text="Translated text").pack(anchor="w", padx=15)
output_box = tk.Text(root, height=8, wrap="word", state="disabled", bg="#f3f4f6")
output_box.pack(fill="x", padx=15)

btns = tk.Frame(root)
btns.pack(pady=10)
tk.Button(btns, text="Copy", command=copy_text).pack(side="left", padx=5)
tk.Button(btns, text="Speak", command=speak).pack(side="left", padx=5)

root.mainloop()