import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget, 
    QGraphicsDropShadowEffect, QScrollArea
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont
import qtawesome as qta
from StyleSheetManager import *
from Thread import APIWorker

class LoginWindow(QMainWindow,StyleSheetManager):
    
    def __init__(self, theme='dark'):
        super().__init__()
        self.current_theme = theme
        self.inputs = {}
        self.token = None      # <--- Store Token
        self.user_data = {}    # <--- Store User Data
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
        print("Login Success!")
        
        # 1. Initialize Dashboard
        self.dashboard = DashboardWindow(self.current_theme)
        
        # 2. Pass Token AND User Data
        # Assuming your Django Login returns: 
        # { 'token': '...', 'user': {'first_name': '...', 'company': '...'} }
        self.dashboard.token = response_data.get('token')
        self.dashboard.user_data = response_data.get('user', {}) 
        
        # 3. Refresh the dashboard UI with this new data
        self.dashboard.refresh_profile_ui() 

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

    def closeEvent(self, event):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        event.accept()

class DashboardWindow(QMainWindow):
    def __init__(self, theme='dark'):
        super().__init__()
        self.current_theme = theme
        self.is_sidebar_open = True
        self.inputs = {} # Store form inputs here
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
        self.nav_buttons = [] 
        
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
        
        # Page 0: Workspace
        workspace_page = self.create_workspace_page()
        self.stack.addWidget(workspace_page)
        
        # Page 1: History (Placeholder)
        history_page = self.create_history_page("History Log", "fa5s.history")
        self.stack.addWidget(history_page)

        # Page 2: Profile (Full Form)
        # ✅ FIX: Calling the correct method name (snake_case)
        profile_page = self.create_profile_page() 
        self.stack.addWidget(profile_page)

        content_layout.addWidget(self.stack)
        self.main_h_layout.addWidget(content_area)
        
        self.switch_tab(0)
        self.apply_theme()

    # ---------------------------------------------------------
    # PAGE CREATION HELPERS
    # ---------------------------------------------------------
    def refresh_profile_ui(self):
        """Fills the inputs with data passed from Login"""
        if not self.user_data:
            return

        # Update Header Labels
        full_name = f"{self.user_data.get('first_name', '')} {self.user_data.get('last_name', '')}"
        self.name_lbl.setText(full_name)
        self.role_lbl.setText(self.user_data.get('role', 'User'))

        # Update Input Fields (Safe get in case key is missing)
        self.inputs['first_name'].setText(self.user_data.get('first_name', ''))
        self.inputs['last_name'].setText(self.user_data.get('last_name', ''))
        self.inputs['email'].setText(self.user_data.get('email', '')) # Django uses username/email
        # Note: Your Django view expects 'company' and 'role' inside a profile relation.
        # Ensure your Login response sends them flattened or adjust here.
        self.inputs['company'].setText(self.user_data.get('company', ''))
        self.inputs['role'].setText(self.user_data.get('role', ''))

    def create_workspace_page(self):
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

    def create_history_page(self, title, icon_name):
        """Creates a dummy placeholder page"""
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

    def create_profile_page(self):
        """Creates the Full Profile Edit Form"""
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)

        # 1. Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content_widget = QWidget()
        self.profile_layout = QVBoxLayout(content_widget)
        self.profile_layout.setContentsMargins(20, 0, 20, 20)
        self.profile_layout.setSpacing(20)

        # --- Header Card ---
        header_card = QFrame()
        header_card.setObjectName("GlassCard")
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(20, 20, 20, 20)

        avatar = QLabel("JD")
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFixedSize(64, 64)
        avatar.setStyleSheet(f"""
            background-color: {THEMES[self.current_theme]['accent']};
            color: white; font-size: 24px; font-weight: bold; border-radius: 32px;
        """)
        
        info_layout = QVBoxLayout()
        self.name_lbl = QLabel("John Doe")
        self.name_lbl.setObjectName("Title")
        self.role_lbl = QLabel("Senior Engineer")
        self.role_lbl.setObjectName("Subtitle")
        info_layout.addWidget(self.name_lbl)
        info_layout.addWidget(self.role_lbl)
        info_layout.addStretch()

        self.edit_btn = QPushButton(" Edit Profile")
        self.edit_btn.setIcon(qta.icon('fa5s.pen', color=THEMES[self.current_theme]['text_primary']))
        self.edit_btn.setObjectName("GhostBtn")
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.setCheckable(True)
        self.edit_btn.clicked.connect(self.toggle_edit_mode)

        header_layout.addWidget(avatar)
        header_layout.addSpacing(10)
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.edit_btn)

        self.profile_layout.addWidget(header_card)

        # --- Form Card ---
        form_card = QFrame()
        form_card.setObjectName("GlassCard")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(20)

        # Personal Info Header
        sec_title = QHBoxLayout()
        sec_icon = QLabel()
        sec_icon.setPixmap(qta.icon('fa5s.user', color=THEMES[self.current_theme]['accent']).pixmap(20, 20))
        sec_lbl = QLabel("Personal Information")
        sec_lbl.setStyleSheet("font-weight: bold; font-size: 16px;")
        sec_title.addWidget(sec_icon)
        sec_title.addWidget(sec_lbl)
        sec_title.addStretch()
        form_layout.addLayout(sec_title)

        # Helper to create inputs (Nested function)
        def create_input_group(label_text, key, placeholder="", is_password=False):
            group = QVBoxLayout()
            lbl = QLabel(label_text)
            lbl.setStyleSheet(f"color: {THEMES[self.current_theme]['text_secondary']}; font-size: 13px;")
            
            inp = QLineEdit()
            inp.setText(placeholder)
            inp.setReadOnly(True)
            if is_password:
                inp.setEchoMode(QLineEdit.Password)
            
            self.inputs[key] = inp # Save reference
            
            group.addWidget(lbl)
            group.addWidget(inp)
            return group 

        # Form Rows
        row1 = QHBoxLayout()
        row1.addLayout(create_input_group("First Name", "first_name", "John"))
        row1.addLayout(create_input_group("Last Name", "last_name", "Doe"))
        form_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addLayout(create_input_group("Email Address", "email", "john.doe@company.com"))
        row2.addLayout(create_input_group("Company", "company", "TechSol Industries"))
        form_layout.addLayout(row2)

        form_layout.addLayout(create_input_group("Role / Designation", "role", "Senior Engineer"))

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {THEMES[self.current_theme]['border']};")
        form_layout.addSpacing(10)
        form_layout.addWidget(line)
        form_layout.addSpacing(10)

        # Security Section
        sec_title_2 = QHBoxLayout()
        sec_icon_2 = QLabel()
        sec_icon_2.setPixmap(qta.icon('fa5s.shield-alt', color=THEMES[self.current_theme]['accent']).pixmap(20, 20))
        sec_lbl_2 = QLabel("Security & Password")
        sec_lbl_2.setStyleSheet("font-weight: bold; font-size: 16px;")
        sec_title_2.addWidget(sec_icon_2)
        sec_title_2.addWidget(sec_lbl_2)
        sec_title_2.addStretch()
        form_layout.addLayout(sec_title_2)

        form_layout.addLayout(create_input_group("New Password", "new_password", "", is_password=True))
        hint = QLabel("Leave blank to keep current password")
        hint.setStyleSheet("color: #64748b; font-size: 11px; margin-top: -5px;")
        form_layout.addWidget(hint)

        # Save/Verify Area
        self.save_container = QWidget()
        self.save_container.setVisible(False)
        save_layout = QVBoxLayout(self.save_container)
        save_layout.setContentsMargins(0, 20, 0, 0)
        save_layout.setSpacing(10)
        
        v_head = QHBoxLayout()
        v_icon = QLabel()
        v_icon.setPixmap(qta.icon('fa5s.key', color=THEMES[self.current_theme]['accent']).pixmap(18, 18))
        v_lbl = QLabel("Confirm Changes")
        v_lbl.setStyleSheet("font-weight: bold;")
        v_head.addWidget(v_icon)
        v_head.addWidget(v_lbl)
        v_head.addStretch()
        
        v_desc = QLabel("To save these updates, please enter your current password.")
        v_desc.setStyleSheet(f"color: {THEMES[self.current_theme]['text_secondary']};")

        self.current_pass_input = QLineEdit()
        self.current_pass_input.setPlaceholderText("Current Password (Required)")
        self.current_pass_input.setEchoMode(QLineEdit.Password)

        self.save_btn = QPushButton(" Save Changes")
        self.save_btn.setIcon(qta.icon('fa5s.save', color='white'))
        self.save_btn.setObjectName("PrimaryBtn")
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.handle_save_profile)

        save_layout.addLayout(v_head)
        save_layout.addWidget(v_desc)
        save_layout.addWidget(self.current_pass_input)
        save_layout.addWidget(self.save_btn)

        form_layout.addWidget(self.save_container)
        
        self.profile_layout.addWidget(form_card)
        self.profile_layout.addStretch()

        scroll.setWidget(content_widget)
        page_layout.addWidget(scroll)
        
        return page

    # ---------------------------------------------------------
    # INTERACTION LOGIC
    # ---------------------------------------------------------

    def toggle_edit_mode(self):
        is_editing = self.edit_btn.isChecked()

        for key, inp in self.inputs.items():
            inp.setReadOnly(not is_editing)
            # Optional visual cue for editable fields
            if is_editing:
                inp.setStyleSheet(f"border: 1px solid {THEMES[self.current_theme]['accent']};")
            else:
                inp.setStyleSheet("") # Revert to stylesheet default

        if is_editing:
            self.edit_btn.setText(" Cancel")
            self.edit_btn.setIcon(qta.icon('fa5s.times', color='#ef4444'))
            self.save_container.setVisible(True)
            self.inputs['first_name'].setFocus()
        else:
            self.edit_btn.setText(" Edit Profile")
            self.edit_btn.setIcon(qta.icon('fa5s.pen', color=THEMES[self.current_theme]['text_primary']))
            self.save_container.setVisible(False)
            self.inputs['new_password'].clear()
            self.current_pass_input.clear()

    def on_update_success(self, response):
        print("Update Success")
        
        # 1. Update Local Data (So if we cancel later, it reverts to this)
        self.user_data['first_name'] = self.inputs['first_name'].text()
        self.user_data['last_name'] = self.inputs['last_name'].text()
        self.user_data['role'] = self.inputs['role'].text()
        
        # 2. Update UI Header
        self.refresh_profile_ui()

        # 3. Close Edit Mode
        self.edit_btn.setChecked(False)
        self.toggle_edit_mode()
        
        # 4. Clear Password fields for security
        self.current_pass_input.clear()
        self.inputs['new_password'].clear()
        self.current_pass_input.setStyleSheet("") # Reset red border if any

    def on_update_error(self, err_msg):
        print(f"Update Failed: {err_msg}")
        # In a real app, use QMessageBox.warning(self, "Error", "Incorrect Password or Server Error")
        self.current_pass_input.setStyleSheet("border: 1px solid red;")
        self.current_pass_input.setText("")
        self.current_pass_input.setPlaceholderText("Incorrect Password")

    def on_update_finished(self):
        self.save_btn.setText(" Save Changes")
        self.save_btn.setEnabled(True)

    def handle_save_profile(self):
        current_password = self.current_pass_input.text()
        print(current_password)
        
        if not current_password:
            # Visual feedback
            self.current_pass_input.setStyleSheet("border: 1px solid red;")
            self.current_pass_input.setPlaceholderText("PASSWORD REQUIRED!")
            return

        # 1. Prepare Data for API matches your Django View keys
        payload = {
            "first_name": self.inputs['first_name'].text(),
            "last_name": self.inputs['last_name'].text(),
            "email": self.inputs['email'].text(), # Your Django view sets username = email
            "company": self.inputs['company'].text(),
            "role": self.inputs['role'].text(),
            "currentPassword":  current_password,
            "newPassword": self.inputs['new_password'].text()
        }

        # 2. Disable Button
        self.save_btn.setText("Saving...")
        self.save_btn.setEnabled(False)

        # 3. Configure Worker
        # URL = Your Django Patch URL
        url = "http://127.0.0.1:8000/update/" 
        
        # Headers = Token Auth
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }

        self.worker = APIWorker(url, payload, method="PATCH", headers=headers)
        self.worker.success.connect(self.on_update_success)
        self.worker.error.connect(self.on_update_error)
        self.worker.finished.connect(self.on_update_finished)
        self.worker.start()

    def switch_tab(self, index):
        self.stack.setCurrentIndex(index)
        titles = ["Workspace", "History", "Profile"]
        self.page_title.setText(titles[index])

        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.setProperty("active", "true")
            else:
                btn.setProperty("active", "false")
            
            self.style().unpolish(btn)
            self.style().polish(btn)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set global font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = LoginWindow()
    window.show()
    
    sys.exit(app.exec_())
