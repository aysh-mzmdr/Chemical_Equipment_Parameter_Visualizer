import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget, 
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont
import qtawesome as qta
from StyleSheetManager import *
from Thread import APIWorker

class LoginWindow(QMainWindow,StyleSheetManager,APIWorker):
    
    def __init__(self,theme='dark'):
        super().__init__('','')
        self.current_theme = theme
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer - Login")
        self.setFixedSize(720,680)
        
        # Central Widget
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)
        
        # Layouts
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setAlignment(Qt.AlignCenter)

        # --- Theme Toggle (Top Right) ---
        self.toggle_btn = QPushButton()
        self.toggle_btn.setIcon(qta.icon('fa5s.sun' if self.current_theme == 'dark' else 'fa5s.moon', color='#94a3b8'))
        self.toggle_btn.setFixedSize(40, 40)
        self.toggle_btn.setStyleSheet("background: transparent; border: 1px solid #1e293b; border-radius: 8px;")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_theme)
        
        # Absolute positioning for toggle isn't standard in layouts, so we use a top bar layout
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(self.toggle_btn)
        main_layout.addLayout(top_bar)
        main_layout.addStretch()

        # --- Login Card ---
        self.card = QFrame()
        self.card.setObjectName("GlassCard")
        self.card.setFixedSize(700,600)
        
        # Shadow Effect for Card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)

        # Logo Area
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

        # Form Area
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
        # Update Icon
        icon_name = 'fa5s.moon' if self.current_theme == 'light' else 'fa5s.sun'
        self.toggle_btn.setIcon(qta.icon(icon_name, color='#94a3b8'))
        
        # Update Logo Color
        # Note: In a real app, you'd keep a reference to the logo label to update it efficiently
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(StyleSheetManager.get_sheet(self.current_theme))

    def handle_login(self):
        # 1. Get data from inputs
        email = self.email_input.text()
        password = self.pass_input.text()
        
        # 2. Disable button to prevent double-clicks
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Logging in...")

        # 3. Setup the API URL
        url = "http://127.0.0.1:8000/login/"
        data = {"username": email, "password": password}

        # 4. Initialize and start the Worker
        self.worker = APIWorker(url, data)
        
        # Connect signals to slots (functions)
        self.worker.success.connect(self.on_login_success)
        self.worker.error.connect(self.on_login_error)
        self.worker.finished.connect(self.on_request_finished)
        
        self.worker.start()

    def on_login_success(self, response_data):
        print(f"Login Success! User ID: {response_data.get('user_id')}")
        
        # Pass the token/user info to the Dashboard
        self.dashboard = DashboardWindow(self.current_theme)
        self.dashboard.token = response_data['token']
        print(self.dashboard.token)
        self.dashboard.show()
        self.close()

    def on_login_error(self, error_message):
        # Show error in a message box or label
        print(f"Login Failed: {error_message}")
        # In a real app, use QMessageBox.warning(self, "Error", error_message)
        
        # Reset button text logic is handled in on_request_finished

    def on_request_finished(self):
        # Re-enable the button regardless of success/failure
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Sign In to Console")

class DashboardWindow(QMainWindow):
    def __init__(self, theme='dark'):
        super().__init__()
        self.current_theme = theme
        self.is_sidebar_open = True
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer - Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        # Main Layout
        self.main_h_layout = QHBoxLayout(self.central_widget)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_h_layout.setSpacing(0)

        # --- Sidebar ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(260)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 20)
        sidebar_layout.setSpacing(10)

        # Logo Section
        logo_box = QHBoxLayout()
        self.logo_lbl = QLabel()
        self.logo_lbl.setPixmap(qta.icon('fa5s.flask', color=THEMES[self.current_theme]['accent']).pixmap(24, 24))
        logo_text = QLabel("Chemical Equipment Parameter Visualizer")
        logo_text.setObjectName("LogoText")
        logo_box.addWidget(self.logo_lbl)
        logo_box.addWidget(logo_text)
        logo_box.addStretch()
        sidebar_layout.addLayout(logo_box)
        sidebar_layout.addSpacing(30)

        # --- Navigation Menu Logic ---
        self.nav_buttons = [] # Store buttons to access them later
        
        # Define menus with their display name and icon
        menus = [
            ("Workspace", "fa5s.columns"), 
            ("History", "fa5s.history"), 
            ("Profile", "fa5s.user-circle")
        ]
        
        for i, (name, icon) in enumerate(menus):
            btn = QPushButton(f"  {name}")
            btn.setIcon(qta.icon(icon, color="#94a3b8"))
            btn.setObjectName("NavItem")
            btn.setCursor(Qt.PointingHandCursor)
            
            # Connect click to switch_tab, passing the index
            # We use lambda i=i: to capture the current value of i
            btn.clicked.connect(lambda checked, index=i: self.switch_tab(index))
            
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # Footer
        self.logout_btn = QPushButton("  Logout")
        self.logout_btn.setIcon(qta.icon('fa5s.sign-out-alt', color="#94a3b8"))
        self.logout_btn.setObjectName("NavItem")
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.clicked.connect(self.handle_logout)
        sidebar_layout.addWidget(self.logout_btn)

        self.main_h_layout.addWidget(self.sidebar)

        # --- Main Content Area ---
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 30, 30, 30)

        # Top Header
        header_layout = QHBoxLayout()
        self.menu_btn = QPushButton()
        self.menu_btn.setIcon(qta.icon('fa5s.bars', color=THEMES[self.current_theme]['text_primary']))
        self.menu_btn.setStyleSheet("background: transparent; border: none;")
        self.menu_btn.setCursor(Qt.PointingHandCursor)
        self.menu_btn.clicked.connect(self.toggle_sidebar)

        self.page_title = QLabel("Workspace")
        self.page_title.setObjectName("Title")

        header_layout.addWidget(self.menu_btn)
        header_layout.addSpacing(15)
        header_layout.addWidget(self.page_title)
        header_layout.addStretch()

        self.toggle_btn = QPushButton()
        self.toggle_btn.setIcon(qta.icon('fa5s.sun' if self.current_theme == 'dark' else 'fa5s.moon', color='#94a3b8'))
        self.toggle_btn.setFixedSize(40, 40)
        self.toggle_btn.setStyleSheet("background: transparent; border: 1px solid #1e293b; border-radius: 8px;")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.toggle_btn)

        content_layout.addLayout(header_layout)

        # --- Stacked Widget (Pages) ---
        self.stack = QStackedWidget()
        
        # Page 0: Workspace (Existing)
        workspace_page = self.create_workspace_page()
        self.stack.addWidget(workspace_page)
        
        # Page 1: History (Placeholder)
        history_page = self.create_placeholder_page("History Log", "fa5s.history")
        self.stack.addWidget(history_page)

        # Page 2: Profile (Placeholder)
        profile_page = self.create_placeholder_page("User Profile", "fa5s.user-circle")
        self.stack.addWidget(profile_page)

        content_layout.addWidget(self.stack)
        self.main_h_layout.addWidget(content_area)
        
        # Initialize default state (Index 0 = Workspace)
        self.switch_tab(0)
        self.apply_theme()

    def create_workspace_page(self):
        """Helper to create the Workspace layout"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        upload_card = QFrame()
        upload_card.setObjectName("GlassCard")
        upload_card.setFixedHeight(300)
        uc_layout = QVBoxLayout(upload_card)
        uc_layout.setAlignment(Qt.AlignCenter)
        
        cloud_icon = QLabel()
        cloud_icon.setPixmap(qta.icon('fa5s.cloud-upload-alt', color=THEMES[self.current_theme]['accent']).pixmap(64, 64))
        cloud_icon.setAlignment(Qt.AlignCenter)
        
        uc_text = QLabel("Drag and drop your CSV file here")
        uc_text.setAlignment(Qt.AlignCenter)
        uc_text.setStyleSheet("color: #94a3b8; font-size: 16px; margin-top: 10px;")

        uc_btn = QPushButton("Select File")
        uc_btn.setObjectName("PrimaryBtn")
        uc_btn.setFixedWidth(150)
        uc_btn.setCursor(Qt.PointingHandCursor)

        uc_layout.addWidget(cloud_icon)
        uc_layout.addWidget(uc_text)
        uc_layout.addWidget(uc_btn, 0, Qt.AlignCenter)

        layout.addWidget(upload_card)
        layout.addStretch()
        return page

    def create_placeholder_page(self, title, icon_name):
        """Helper to create dummy pages for History/Profile"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        
        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color="#94a3b8").pixmap(64, 64))
        icon.setAlignment(Qt.AlignCenter)
        
        lbl = QLabel(f"{title} Module")
        lbl.setObjectName("Title")
        lbl.setAlignment(Qt.AlignCenter)
        
        sub = QLabel("This module is currently under development.")
        sub.setObjectName("Subtitle")
        sub.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(icon)
        layout.addWidget(lbl)
        layout.addWidget(sub)
        return page

    def switch_tab(self, index):
        """Handles visual highlighting and page switching"""
        # 1. Update Stacked Widget Page
        self.stack.setCurrentIndex(index)
        
        # 2. Update Page Title
        titles = ["Workspace", "History", "Profile"]
        self.page_title.setText(titles[index])

        # 3. Update Visual Highlight
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                # Add 'active' property to true
                btn.setProperty("active", "true")
            else:
                # Remove or set to false
                btn.setProperty("active", "false")
            
            # FORCE STYLE REFRESH (Crucial for QSS to re-evaluate)
            self.style().unpolish(btn)
            self.style().polish(btn)

    # ... Rest of your existing methods (toggle_sidebar, toggle_theme, etc.) ...
    def toggle_sidebar(self):
        width = 0 if self.is_sidebar_open else 260
        self.anim = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.anim.setDuration(300)
        self.anim.setStartValue(self.sidebar.width())
        self.anim.setEndValue(width)
        self.anim.setEasingCurve(QEasingCurve.InOutQuart)
        self.anim.start()
        
        self.anim_max = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self.anim_max.setDuration(300)
        self.anim_max.setStartValue(self.sidebar.width())
        self.anim_max.setEndValue(width)
        self.anim_max.start()
        self.is_sidebar_open = not self.is_sidebar_open

    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        icon_name = 'fa5s.moon' if self.current_theme == 'light' else 'fa5s.sun'
        self.toggle_btn.setIcon(qta.icon(icon_name, color='#94a3b8'))
        self.logo_lbl.setPixmap(qta.icon('fa5s.flask', color=THEMES[self.current_theme]['accent']).pixmap(24, 24))
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(StyleSheetManager.get_sheet(self.current_theme))

    def handle_logout(self):
        self.login_win = LoginWindow() 
        self.login_win.current_theme = self.current_theme
        self.login_win.apply_theme()
        self.login_win.show()
        self.close()

    def closeEvent(self, event):
        # This function runs automatically when the user clicks the X button
        
        # Optional: Ask for confirmation
        # reply = QMessageBox.question(self, 'Exit', "Are you sure you want to quit?", 
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # if reply == QMessageBox.Yes:
        
        # 1. Stop any running threads if you have them stored
        # if hasattr(self, 'worker') and self.worker.isRunning():
        #     self.worker.quit()
        #     self.worker.wait()

        # 2. Force the entire application to quit
        QApplication.quit() 
        event.accept()
        
        # else:
        #     event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set global font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = LoginWindow()
    window.show()
    
    sys.exit(app.exec_())
