# modules/mouse_tracker.py
from pynput import mouse
import os
from datetime import datetime
from threading import Thread
from modules import screenshot_capture

def start_logger(user_folder):
    mouse_file = os.path.join(user_folder, "mouse_log.txt")

    def on_move(x, y):
        with open(mouse_file, "a") as f:
            f.write(f"{datetime.now()}: Mouse moved to ({x}, {y})\n")

    def on_click(x, y, button, pressed):
        with open(mouse_file, "a") as f:
            action = "Pressed" if pressed else "Released"
            f.write(f"{datetime.now()}: Mouse {action} at ({x}, {y}) with {button}\n")

    def on_scroll(x, y, dx, dy):
        with open(mouse_file, "a") as f:
            f.write(f"{datetime.now()}: Scrolled at ({x}, {y}) with delta ({dx}, {dy})\n")

    # Start screenshot capture in a separate thread
    Thread(target=screenshot_capture.start_logger, args=(user_folder,), daemon=True).start()

    # Start mouse listener
    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()
