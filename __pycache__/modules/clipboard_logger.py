import time
import os
try:
    import win32clipboard
except ImportError:
    print("Install pywin32 using: pip install pywin32")
    exit()

def get_clipboard_data():
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data
    except Exception:
        return ""

def start_logger(folder_path):
    log_file = os.path.join(folder_path, "clipboard.txt")
    open(log_file, "a").close()
    previous_data = ""
    while True:
        data = get_clipboard_data()
        if data != previous_data and data.strip() != "":
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"\n[{time.ctime()}] {data}\n")
            previous_data = data
        time.sleep(5)