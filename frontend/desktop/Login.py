import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget, 
    QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QColor, QFont, QIcon
import qtawesome as qta

# --- Theme Configuration ---
THEMES = {
    'dark': {
        'bg_primary': "#020617",
        'bg_secondary': "#0f172a",
        'text_primary': "#f1f5f9",
        'text_secondary': "#94a3b8",
        'accent': "#38bdf8",
        'accent_glow': "rgba(56, 189, 248, 0.25)",
        'glass_bg': "rgba(15, 23, 42, 0.85)",
        'border': "#1e293b",
        'input_bg': "rgba(30, 41, 59, 0.5)"
    },
    'light': {
        'bg_primary': "#f8fafc",
        'bg_secondary': "#ffffff",
        'text_primary': "#0f172a",
        'text_secondary': "#64748b",
        'accent': "#0ea5e9",
        'accent_glow': "rgba(14, 165, 233, 0.2)",
        'glass_bg': "rgba(255, 255, 255, 0.9)",
        'border': "#e2e8f0",
        'input_bg': "#ffffff"
    }
}

class StyleSheetManager:
    @staticmethod
    def get_sheet(theme_name):
        t = THEMES[theme_name]
        return f"""
            QMainWindow, QWidget#CentralWidget {{
                background-color: {t['bg_primary']};
            }}
            /* Glass Card Styling */
            QFrame#GlassCard {{
                background-color: {t['glass_bg']};
                border: 1px solid {t['border']};
                border-radius: 16px;
            }}
            /* Text Styling */
            QLabel {{
                color: {t['text_primary']};
                font-family: 'Segoe UI', sans-serif;
            }}
            QLabel#Title {{
                font-size: 24px;
                font-weight: bold;
            }}
            QLabel#Subtitle {{
                color: {t['text_secondary']};
                font-size: 13px;
            }}
            QLabel#LogoText {{
                font-size: 18px;
                font-weight: bold;
            }}
            
            /* Input Fields */
            QLineEdit {{
                background-color: {t['input_bg']};
                border: 1px solid {t['border']};
                border-radius: 8px;
                padding: 10px;
                color: {t['text_primary']};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 1px solid {t['accent']};
            }}
            
            /* Buttons */
            QPushButton#PrimaryBtn {{
                background-color: {t['accent']};
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }}
            QPushButton#PrimaryBtn:hover {{
                background-color: {t['accent']};
                opacity: 0.9;
            }}
            
            QPushButton#GhostBtn {{
                background-color: transparent;
                color: {t['text_secondary']};
                border: none;
                text-align: left;
                padding: 8px;
            }}
            QPushButton#GhostBtn:hover {{
                color: {t['text_primary']};
                background-color: {t['bg_secondary']};
                border-radius: 6px;
            }}

            /* Sidebar */
            QFrame#Sidebar {{
                background-color: {t['glass_bg']};
                border-right: 1px solid {t['border']};
            }}
            QPushButton#NavItem {{
                text-align: left;
                padding: 12px 15px;
                border-radius: 8px;
                color: {t['text_secondary']};
                background-color: transparent;
                border: none;
                font-size: 14px;
            }}
            QPushButton#NavItem:hover {{
                color: {t['text_primary']};
                background-color: {t['input_bg']};
            }}
            QPushButton#NavItem[active="true"] {{
                color: {t['accent']};
                background-color: {t['accent_glow']};
                font-weight: bold;
            }}
        """

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = 'dark'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ChemVis.io - Login")
        self.setGeometry(100, 100, 1000, 700)
        
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
        self.card.setFixedSize(400, 500)
        
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

        card_layout.addWidget(QLabel("Work Email"))
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(QLabel("Password"))
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
        # Simplified Login Logic
        print(f"Logging in with: {self.email_input.text()}")
        self.dashboard = DashboardWindow(self.current_theme)
        self.dashboard.show()
        self.close()

class DashboardWindow(QMainWindow):
    def __init__(self, theme='dark'):
        super().__init__()
        self.current_theme = theme
        self.is_sidebar_open = True
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ChemVis.io - Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        # Main Layout (Horizontal: Sidebar + Content)
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
        
        logo_text = QLabel("ChemVis.io")
        logo_text.setObjectName("LogoText")
        
        logo_box.addWidget(self.logo_lbl)
        logo_box.addWidget(logo_text)
        logo_box.addStretch()
        sidebar_layout.addLayout(logo_box)
        
        sidebar_layout.addSpacing(30)

        # Nav Menu
        self.nav_items = []
        menus = [("Workspace", "fa5s.columns"), ("History", "fa5s.history"), ("Profile", "fa5s.user-circle")]
        
        for name, icon in menus:
            btn = QPushButton(f"  {name}")
            btn.setIcon(qta.icon(icon, color="#94a3b8"))
            btn.setObjectName("NavItem")
            btn.setCursor(Qt.PointingHandCursor)
            
            # Highlight first item
            if name == "Workspace":
                btn.setProperty("active", "true")
            
            sidebar_layout.addWidget(btn)
            self.nav_items.append(btn)

        sidebar_layout.addStretch()

        # Footer
        self.logout_btn = QPushButton("  Logout")
        self.logout_btn.setIcon(qta.icon('fa5s.sign-out-alt', color="#94a3b8"))
        self.logout_btn.setObjectName("NavItem")
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

        # Theme Toggle in Dashboard
        self.dash_theme_btn = QPushButton()
        self.dash_theme_btn.setIcon(qta.icon('fa5s.moon', color='#94a3b8'))
        self.dash_theme_btn.setFixedSize(36, 36)
        self.dash_theme_btn.setStyleSheet("border: 1px solid #1e293b; border-radius: 8px;")
        self.dash_theme_btn.clicked.connect(self.toggle_dashboard_theme)
        header_layout.addWidget(self.dash_theme_btn)

        content_layout.addLayout(header_layout)

        # Dashboard Content (Upload Card Placeholder)
        self.stack = QStackedWidget()
        
        # View 1: Workspace
        workspace = QWidget()
        ws_layout = QVBoxLayout(workspace)
        
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

        ws_layout.addWidget(upload_card)
        ws_layout.addStretch()
        
        self.stack.addWidget(workspace)
        content_layout.addWidget(self.stack)

        self.main_h_layout.addWidget(content_area)
        
        self.apply_theme()

    def toggle_sidebar(self):
        width = 0 if self.is_sidebar_open else 260
        
        # Animation
        self.anim = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.anim.setDuration(300)
        self.anim.setStartValue(self.sidebar.width())
        self.anim.setEndValue(width)
        self.anim.setEasingCurve(QEasingCurve.InOutQuart)
        self.anim.start()
        
        # Also animate maximum width to prevent layout issues
        self.anim_max = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self.anim_max.setDuration(300)
        self.anim_max.setStartValue(self.sidebar.width())
        self.anim_max.setEndValue(width)
        self.anim_max.start()

        self.is_sidebar_open = not self.is_sidebar_open

    def toggle_dashboard_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.apply_theme()
        # Refresh icons manually (PyQt doesn't auto-update icons on stylesheet change)
        self.logo_lbl.setPixmap(qta.icon('fa5s.flask', color=THEMES[self.current_theme]['accent']).pixmap(24, 24))

    def apply_theme(self):
        self.setStyleSheet(StyleSheetManager.get_sheet(self.current_theme))

    def handle_logout(self):
        self.login_win = LoginWindow()
        self.login_win.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set global font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = LoginWindow()
    window.show()
    
    sys.exit(app.exec_())