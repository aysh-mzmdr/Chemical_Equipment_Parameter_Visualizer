from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFrame,
    QGraphicsDropShadowEffect, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon
import qtawesome as qta
from StyleSheetManager import * 
from Thread import APIWorker
import Main

class LoginWindow(QMainWindow, StyleSheetManager):
    
    def __init__(self, theme='dark'):
        super().__init__()
        self.setWindowIcon(QIcon("../flask.svg"))
        self.current_theme = theme
        self.inputs = {}
        self.token = None      
        self.user_data = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer - Login")
        self.setFixedSize(720,680)

        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setAlignment(Qt.AlignCenter)

        self.toggle_btn = QPushButton()
        self.toggle_btn.setIcon(qta.icon('fa5s.sun' if self.current_theme == 'dark' else 'fa5s.moon', color='#94a3b8'))
        self.toggle_btn.setFixedSize(40, 40)
        self.toggle_btn.setStyleSheet("background: transparent; border: 1px solid #1e293b; border-radius: 8px;")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_theme)
        
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(self.toggle_btn)
        main_layout.addLayout(top_bar)
        main_layout.addStretch()

        self.card = QFrame()
        self.card.setObjectName("GlassCard")
        self.card.setFixedSize(700,600)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)

        logo_layout = QVBoxLayout()
        logo_icon = QLabel()
        logo_pixmap = qta.icon('fa5s.flask', color=THEMES[self.current_theme]['accent']).pixmap(48, 48)
        logo_icon.setPixmap(logo_pixmap)
        logo_icon.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Welcome Back")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Enter your credentials to access the equipment parameters dashboard.")
        subtitle.setObjectName("Subtitle")
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignCenter)

        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(title)
        logo_layout.addWidget(subtitle)
        card_layout.addLayout(logo_layout)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("eng.name@company.com")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter your password")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Sign In to Console")
        self.login_btn.setObjectName("PrimaryBtn")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)

        domain_name1=QLabel("Work Email")
        domain_name1.setObjectName("Domain_name")
        domain_name2=QLabel("Password")
        domain_name2.setObjectName("Domain_name")
        card_layout.addWidget(domain_name1)
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(domain_name2)
        card_layout.addWidget(self.pass_input)
        card_layout.addWidget(self.login_btn)
        card_layout.addStretch()

        main_layout.addWidget(self.card)
        main_layout.addStretch()

        self.apply_theme()

    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        
        icon_name = 'fa5s.moon' if self.current_theme == 'light' else 'fa5s.sun'
        self.toggle_btn.setIcon(qta.icon(icon_name, color='#94a3b8'))
        
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(StyleSheetManager.get_sheet(self.current_theme))

    def handle_login(self):
        email = self.email_input.text()
        password = self.pass_input.text()
        
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Logging in...")

        url = "http://127.0.0.1:8000/login/"
        data = {"username": email, "password": password}

        self.worker = APIWorker(url, data)
        self.worker.success.connect(self.on_login_success)
        self.worker.error.connect(self.on_login_error)
        self.worker.finished.connect(self.on_request_finished)
        self.worker.start()

    def on_login_success(self, response_data):
        print("Login Success!")
        
        self.dashboard = Main.DashboardWindow(self.current_theme)
        self.dashboard.token = response_data.get('token')
        self.dashboard.user_data = response_data.get('user', {}) 
        self.dashboard.refresh_profile_ui() 
        self.dashboard.show()
        self.close()

    def on_login_error(self, error_message):
        print(f"Update Failed: {error_message}")
        QMessageBox.warning(self, "Error", str(error_message))

    def on_request_finished(self):
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Sign In to Console")

    def closeEvent(self, event):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        event.accept()

if __name__ == "__main__":
    print("Error: Run Main.py to start the application!")