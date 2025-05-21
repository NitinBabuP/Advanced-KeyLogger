from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.username = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("User Login")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Enter your username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter unique identifier")
        self.submit_btn = QPushButton("Start Monitoring")
        self.submit_btn.clicked.connect(self.submit)
        
        layout.addWidget(self.label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

    def submit(self):
        username = self.username_input.text().strip()
        if username:
            self.username = username
            self.accept()