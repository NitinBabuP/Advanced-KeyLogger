import pyperclip
import time
import os
from config import LOG_PATH

def monitor_clipboard():
    log_file = os.path.join(LOG_PATH, "clipboard.log")
    last_content = ""
    
    while True:
        try:
            current_content = pyperclip.paste()
            if current_content and current_content != last_content:
                last_content = current_content
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp}] Clipboard Update:\n{current_content}\n\n")
        except Exception as e:
            print(f"Clipboard Error: {e}")
        
        time.sleep(2)