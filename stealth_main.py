# stealth_main.py

import os
from modules import stealth_mode

def main():
    print("Enter your username for logging:")
    username = input("Username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    user_folder = os.path.join("logs", username)
    os.makedirs(user_folder, exist_ok=True)

    stealth_mode.start_stealth_mode(user_folder)

if __name__ == "__main__":
    main()
