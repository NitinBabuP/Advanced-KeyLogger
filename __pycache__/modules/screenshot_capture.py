import os
import time
import pyautogui
from datetime import datetime

def start_logger(user_folder):
    screenshot_dir = os.path.join(user_folder, "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            time.sleep(30)  # capture every 30 seconds
        except Exception as e:
            print(f"[Screenshot Error] {e}")
