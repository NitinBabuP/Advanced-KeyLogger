# Advanced Keylogger Monitoring System

## 📌 Project Overview

The Advanced Keylogger Monitoring System is a dual-mode logging application developed in Python. It supports two operational modes:

- **GUI Mode**: A user-friendly interface that displays real-time log updates and analytics.
- **Stealth Mode**: A hidden background monitoring mode that starts with system boot and can be terminated using a hotkey.

All logs (keystrokes, clipboard, screenshots, and mouse movements) are saved in a dedicated folder named after the current user and are also sent via email.

---

## 📁 Project Structure

```
advanced_keylogger/
│
├── main.py
├── stealth_main.py
├── /modules/
│   ├── keystroke_logger.py
│   ├── clipboard_logger.py
│   ├── screenshot_capture.py
│   ├── mouse_tracker.py
│   ├── email_sender.py
│   └── stealth_mode.py
├── /ui/
│   └── gui.py
├── /logs/
│   └── <username>/
│       ├── keystrokes.txt
│       ├── clipboard.txt
│       ├── mouse_log.txt
│       └── /screenshots/
│           └── *.png
```

---

## 🖥️ GUI Mode Instructions

1. Run the GUI:
   ```bash
   python ui/gui.py
   ```

2. Enter your username. This creates a new folder in `/logs/`.

3. Use the GUI to:
   - Start/Stop monitoring.
   - View real-time logs (Keystrokes, Clipboard, Screenshots).
   - Access the password-protected dashboard (`Password: admin`).
   - Export analytics to PDF or CSV.

4. All logs are saved locally and sent to the configured email automatically.

---

## 🕵️ Stealth Mode Instructions

1. Run:
   ```bash
   python stealth_main.py
   ```

2. The script will:
   - Pick the current Windows username automatically.
   - Hide the console window.
   - Start logging in background.
   - Send an email with logs on startup.
   - Save logs in `/logs/<username>/`.

3. To exit stealth mode, press:
   ```bash
   F12
   ```
   A message popup will confirm successful exit.

---

## 📬 Email Configuration

Edit `modules/email_sender.py`:
```python
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "recipient_email@gmail.com"
```

> ⚠️ Use App Password for Gmail if 2FA is enabled.

---

## 📦 Dependencies

Install all dependencies with:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pynput pywin32 pyautogui fpdf
```

---

## 🔒 Ethical Usage Notice

This application is strictly for educational purposes. Unauthorized logging of another person's activity is illegal. Use it only with proper consent.

---

## 📈 Features Summary

- Real-time GUI dashboard with live updates
- Stealth mode with hotkey termination
- Logs stored and emailed
- Keystrokes, clipboard, mouse events, screenshots
- Dashboard analytics with export to CSV/PDF

