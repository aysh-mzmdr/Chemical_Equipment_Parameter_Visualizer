import sys
import requests
import base64
import io
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget, 
    QGraphicsDropShadowEffect, QScrollArea, QGridLayout, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDateTime, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QFont
import qtawesome as qta

# Ensure you have these files in your directory or remove imports if testing in isolation
from StyleSheetManager import * 
from Thread import APIWorker

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')

class DownloadWorker(QThread):
    finished = pyqtSignal(bool, str) # Success/Fail, Message/Filename

    def __init__(self, url, token, payload, save_path):
        super().__init__()
        self.url = url
        self.token = token
        self.payload = payload
        self.save_path = save_path

    def run(self):
        try:
            headers = {
                "Authorization": f"Token {self.token}",
                "Content-Type": "application/json"
            }
            # Send Data to Backend
            response = requests.post(self.url, json=self.payload, headers=headers)

            if response.status_code == 200:
                # Write the binary PDF content to the selected file
                with open(self.save_path, 'wb') as f:
                    f.write(response.content)
                self.finished.emit(True, "PDF Downloaded Successfully!")
            else:
                self.finished.emit(False, f"Server Error: {response.status_code}")
        except Exception as e:
            self.finished.emit(False, str(e))

class LoginWindow(QMainWindow, StyleSheetManager):
    
    def __init__(self, theme='dark'):
        super().__init__()
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
        
        self.dashboard = DashboardWindow(self.current_theme)
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

class AnalysisResultWidget(QFrame):
    download_requested = pyqtSignal(object, object)
    
    def __init__(self, data, theme_colors):
        super().__init__()
        self.setObjectName("GlassCard")
        self.data = data
        self.theme_colors = theme_colors # CRITICAL: Save colors for create_stat_block
        
        self.setStyleSheet(f"""
            #GlassCard {{
                background-color: {theme_colors['bg_secondary']};
                border: 2px solid {theme_colors['border']};
                border-radius: 16px;
            }}
            QLabel {{ color: {theme_colors['text_primary']}; }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # --- Header ---
        created_at = data.get('created_at', None)
        if created_at:
            dt = QDateTime.fromString(created_at, Qt.ISODate)
        else:
            dt = QDateTime.currentDateTime()

        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        date_lbl = QLabel(dt.toString("MMM d, yyyy"))
        date_lbl.setStyleSheet(f"color: {theme_colors['text_primary']}; font-weight: bold; font-size: 18px;")

        sep_lbl = QLabel("•")
        sep_lbl.setStyleSheet(f"color: {theme_colors['accent']}; font-size: 20px; line-height: 1;")

        time_lbl = QLabel(dt.toString("h:mm AP"))
        time_lbl.setStyleSheet(f"color: {theme_colors['text_secondary']}; font-size: 14px; font-weight: 500;")

        header_layout.addWidget(date_lbl)
        header_layout.addWidget(sep_lbl)
        header_layout.addWidget(time_lbl)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        layout.addSpacing(20)

        # --- Stats ---
        stats_layout = QHBoxLayout()
        stats = data.get('averages', {})
        total = data.get('total_count', 0)

        stats_layout.addWidget(self.create_stat_block("Total Units", total))
        stats_layout.addWidget(self.create_stat_block("Avg Pressure", stats.get('pressure', 0), "bar"))
        stats_layout.addWidget(self.create_stat_block("Avg Temp", stats.get('temperature', 0), "°C"))
        
        layout.addLayout(stats_layout)
        layout.addSpacing(30)

        # --- Chart & Button ---
        chart_data = data.get('distribution', {})
        if chart_data:
            labels = chart_data.get('labels', [])
            values = chart_data.get('values', [])
            
            self.chart = MplBarChart(labels, values, theme_colors, width=5, height=4)
            layout.addWidget(self.chart)
            
            # Button Container
            btn_container = QHBoxLayout()
            btn_container.addStretch()
            
            self.dl_btn = QPushButton(" Download PDF")
            self.dl_btn.setIcon(qta.icon('fa5s.file-pdf', color=theme_colors['accent']))
            self.dl_btn.setCursor(Qt.PointingHandCursor)
            self.dl_btn.setStyleSheet(f"""
                QPushButton {{
                    color: {theme_colors['accent']};
                    border: 1px solid {theme_colors['accent']};
                    border-radius: 6px;
                    padding: 6px 12px;
                    background: transparent;
                }}
                QPushButton:hover {{
                    background-color: {theme_colors['accent_glow']};
                }}
            """)
            self.dl_btn.clicked.connect(self.on_download_click)
            btn_container.addWidget(self.dl_btn)
            btn_container.addStretch()
            
            layout.addLayout(btn_container)
    
    def create_stat_block(self, title, value, unit=""):
        container = QFrame()
        container.setStyleSheet(f"background-color: {self.theme_colors['input_bg']}; border-radius: 10px; padding: 10px;")
        v_layout = QVBoxLayout(container)
        v_layout.setAlignment(Qt.AlignCenter)
        
        t_label = QLabel(title.upper())
        t_label.setStyleSheet(f"color: {self.theme_colors['text_secondary']}; font-size: 12px; font-weight: bold;")
        
        v_label = QLabel(f"{value} {unit}")
        v_label.setStyleSheet(f"color: {self.theme_colors['accent']}; font-size: 24px; font-weight: bold;")
        
        v_layout.addWidget(t_label, 0, Qt.AlignCenter)
        v_layout.addWidget(v_label, 0, Qt.AlignCenter)

        return container

    def on_download_click(self):
        self.download_requested.emit(self.data, self.chart)

class DashboardWindow(QMainWindow):
    def __init__(self, theme='dark'):
        super().__init__()
        self.current_theme = theme
        self.is_sidebar_open = True
        self.inputs = {}
        self.init_ui()
    
    def display_results(self, data):
        if hasattr(self, 'upload_card'):
            self.upload_card.hide()
            self.workspace_layout.removeWidget(self.upload_card)

        theme_data = THEMES[self.current_theme]
        
        # Create Widget
        self.result_widget = AnalysisResultWidget(data, theme_data)
        
        # Connect Signals
        self.result_widget.download_requested.connect(self.handle_pdf_download)
        
        # Add to Layout
        self.workspace_layout.insertWidget(0, self.result_widget)
        
        # Add Reset Button
        self.reset_btn = QPushButton("Analyze New File")
        self.reset_btn.setCursor(Qt.PointingHandCursor)
        self.reset_btn.setStyleSheet(f"color: {theme_data['accent']}; background: transparent; border: 1px solid {theme_data['accent']}; padding: 10px; border-radius: 8px;")
        self.reset_btn.clicked.connect(self.reset_workspace)
        
        self.workspace_layout.insertWidget(1, self.reset_btn)

    def reset_workspace(self):
        if hasattr(self, 'result_widget'): self.result_widget.deleteLater()
        if hasattr(self, 'reset_btn'): self.reset_btn.deleteLater()
        
        self.upload_card.show()
        self.workspace_layout.insertWidget(0, self.upload_card)
    
    def upload_csv(self, file_path):
        # FIX: Ensure URL is correct
        url = "http://127.0.0.1:8000/upload/"

        if not hasattr(self, 'token') or not self.token:
            QMessageBox.critical(self, "Error", "You must be logged in to upload files.")
            return

        headers = { "Authorization": f"Token {self.token}" }

        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                print(f"Uploading {file_path} to {url}...")
                response = requests.post(url, headers=headers, files=files)

            if response.status_code == 200:
                print("Success:", response.json())
                QMessageBox.information(self, "Success", "File uploaded and analyzed successfully!")
                self.display_results(response.json())
            else:
                try:
                    error_msg = response.json().get('error', 'Unknown Error')
                except:
                    error_msg = f"Error {response.status_code}"
                print(f"Upload Failed: {error_msg}")
                QMessageBox.warning(self, "Upload Failed", str(error_msg))

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Connection Error", "Could not connect to the server. Is Django running?")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")
    
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.upload_csv(file_path)

    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer - Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        self.main_h_layout = QHBoxLayout(self.central_widget)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_h_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(260)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 20)
        sidebar_layout.setSpacing(10)

        logo_box = QHBoxLayout()
        self.logo_lbl = QLabel()
        self.logo_lbl.setPixmap(qta.icon('fa5s.flask', color=THEMES[self.current_theme]['accent']).pixmap(24, 24))
        logo_text = QLabel("Chemical Visualizer")
        logo_text.setObjectName("LogoText")
        logo_box.addWidget(self.logo_lbl)
        logo_box.addWidget(logo_text)
        logo_box.addStretch()
        sidebar_layout.addLayout(logo_box)
        sidebar_layout.addSpacing(30)

        self.nav_buttons = [] 
        menus = [("Workspace", "fa5s.columns"), ("History", "fa5s.history"), ("Profile", "fa5s.user-circle")]
        
        for i, (name, icon) in enumerate(menus):
            btn = QPushButton(f"  {name}")
            btn.setIcon(qta.icon(icon, color="#94a3b8"))
            btn.setObjectName("NavItem")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, index=i: self.switch_tab(index))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        self.logout_btn = QPushButton("  Logout")
        self.logout_btn.setIcon(qta.icon('fa5s.sign-out-alt', color="#94a3b8"))
        self.logout_btn.setObjectName("NavItem")
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.clicked.connect(self.handle_logout)
        sidebar_layout.addWidget(self.logout_btn)

        self.main_h_layout.addWidget(self.sidebar)

        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 30, 30, 30)

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

        self.stack = QStackedWidget()
        
        workspace_page = self.create_workspace_page()
        self.stack.addWidget(workspace_page)
        
        history_page = self.create_history_page("History Log", "fa5s.history")
        self.stack.addWidget(history_page)

        profile_page = self.create_profile_page() 
        self.stack.addWidget(profile_page)

        content_layout.addWidget(self.stack)
        self.main_h_layout.addWidget(content_area)
        
        self.switch_tab(0)
        self.apply_theme()

    def refresh_profile_ui(self):
        if not self.user_data: return
        self.name_lbl.setText(f"{self.user_data.get('first_name', '')} {self.user_data.get('last_name', '')}")
        self.role_lbl.setText(self.user_data.get('role', 'User'))
        self.inputs['first_name'].setText(self.user_data.get('first_name', ''))
        self.inputs['last_name'].setText(self.user_data.get('last_name', ''))
        self.inputs['email'].setText(self.user_data.get('email', ''))
        self.inputs['company'].setText(self.user_data.get('company', ''))
        self.inputs['role'].setText(self.user_data.get('role', ''))

    def create_workspace_page(self):
        page = QWidget()
        self.workspace_layout = QVBoxLayout(page) 
        
        self.upload_card = QFrame() 
        self.upload_card.setObjectName("GlassCard")
        self.upload_card.setFixedHeight(300)
        
        uc_layout = QVBoxLayout(self.upload_card)
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
        uc_btn.clicked.connect(self.open_file_dialog)

        uc_layout.addWidget(cloud_icon)
        uc_layout.addWidget(uc_text)
        uc_layout.addWidget(uc_btn, 0, Qt.AlignCenter)

        self.workspace_layout.addWidget(self.upload_card)
        self.workspace_layout.addStretch()
        return page
    
    def fetch_history(self):
        # 1. Clear Grid
        for i in reversed(range(self.history_grid.count())): 
            self.history_grid.itemAt(i).widget().setParent(None)

        # Ensure this URL matches your Django urls.py exactly! 
        # (e.g. if you have path('api/', include(...)), it might be /api/record/)
        url = "http://127.0.0.1:8000/record/" 
        
        if not hasattr(self, 'token'): return

        try:
            response = requests.get(url, headers={"Authorization": f"Token {self.token}"})
            
            if response.status_code == 200:
                # --- FIX START ---
                response_data = response.json()
                
                # Extract the actual list from the "resultData" key
                records = response_data.get('resultData', [])
                
                if not records:
                    self.history_grid.addWidget(QLabel("No history found."), 0, 0)
                    return
                # --- FIX END ---

                theme = THEMES[self.current_theme]
                COLUMNS = 2
                row, col = 0, 0
                
                for record in records:
                    card = HistoryCard(record, theme)
                    # Connect signal
                    card.download_requested.connect(self.handle_pdf_download)
                    
                    self.history_grid.addWidget(card, row, col)
                    col += 1
                    if col >= COLUMNS:
                        col = 0
                        row += 1
            else:
                self.history_grid.addWidget(QLabel("Failed to load history."), 0, 0)

        except Exception as e:
            print(f"History Error: {e}")
            self.history_grid.addWidget(QLabel("Connection Error"), 0, 0)

    def create_history_page(self, title, icon_name):
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        self.history_content_widget = QWidget()
        self.history_grid = QGridLayout(self.history_content_widget)
        self.history_grid.setContentsMargins(30, 30, 30, 30)
        self.history_grid.setSpacing(30)
        self.history_grid.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.loading_lbl = QLabel("Loading History...")
        self.loading_lbl.setStyleSheet("color: #94a3b8; font-size: 16px;")
        self.history_grid.addWidget(self.loading_lbl, 0, 0)

        scroll.setWidget(self.history_content_widget)
        page_layout.addWidget(scroll)

        refresh_btn = QPushButton(" Refresh")
        refresh_btn.setIcon(qta.icon('fa5s.sync-alt', color=THEMES[self.current_theme]['text_secondary']))
        refresh_btn.setStyleSheet("background: transparent; border: none; text-align: right; padding: 10px;")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.fetch_history)
        
        page_layout.insertWidget(0, refresh_btn, 0, Qt.AlignRight)
        return page
    
    def handle_pdf_download(self, data, chart_obj):
        default_name = f"Report_{data.get('created_at', 'data').replace(':', '-')}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", default_name, "PDF Files (*.pdf)")
        
        if not file_path: return

        chart_b64 = chart_obj.get_image_base64()
        payload = {
            "chartImage": chart_b64,
            "stats": data.get('averages', {}),
            "created_at": data.get('created_at', '')
        }

        # FIX: Ensure URL includes /api/
        url = "http://127.0.0.1:8000/download/" 
        
        self.dl_worker = DownloadWorker(url, self.token, payload, file_path)
        self.dl_worker.finished.connect(self.on_download_finished)
        self.dl_worker.start()
        QApplication.setOverrideCursor(Qt.WaitCursor)

    def on_download_finished(self, success, message):
        QApplication.restoreOverrideCursor()
        if success:
            QMessageBox.information(self, "Success", f"{message}\n\nNote: File is password protected (Use your email).")
        else:
            QMessageBox.warning(self, "Download Failed", message)

    def create_profile_page(self):
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content_widget = QWidget()
        self.profile_layout = QVBoxLayout(content_widget)
        self.profile_layout.setContentsMargins(20, 0, 20, 20)
        self.profile_layout.setSpacing(20)

        header_card = QFrame()
        header_card.setObjectName("GlassCard")
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(20, 20, 20, 20)

        avatar = QLabel("JD")
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFixedSize(64, 64)
        avatar.setStyleSheet(f"background-color: {THEMES[self.current_theme]['accent']}; color: white; font-size: 24px; font-weight: bold; border-radius: 32px;")
        
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

        form_card = QFrame()
        form_card.setObjectName("GlassCard")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(20)

        sec_title = QHBoxLayout()
        sec_icon = QLabel()
        sec_icon.setPixmap(qta.icon('fa5s.user', color=THEMES[self.current_theme]['accent']).pixmap(20, 20))
        sec_lbl = QLabel("Personal Information")
        sec_lbl.setStyleSheet("font-weight: bold; font-size: 16px;")
        sec_title.addWidget(sec_icon)
        sec_title.addWidget(sec_lbl)
        sec_title.addStretch()
        form_layout.addLayout(sec_title)

        def create_input_group(label_text, key, placeholder="", is_password=False):
            group = QVBoxLayout()
            lbl = QLabel(label_text)
            lbl.setStyleSheet(f"color: {THEMES[self.current_theme]['text_secondary']}; font-size: 13px;")
            inp = QLineEdit()
            inp.setText(placeholder)
            inp.setReadOnly(True)
            if is_password: inp.setEchoMode(QLineEdit.Password)
            self.inputs[key] = inp
            group.addWidget(lbl)
            group.addWidget(inp)
            return group 

        row1 = QHBoxLayout()
        row1.addLayout(create_input_group("First Name", "first_name", "John"))
        row1.addLayout(create_input_group("Last Name", "last_name", "Doe"))
        form_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addLayout(create_input_group("Email Address", "email", "john.doe@company.com"))
        row2.addLayout(create_input_group("Company", "company", "TechSol Industries"))
        form_layout.addLayout(row2)

        form_layout.addLayout(create_input_group("Role / Designation", "role", "Senior Engineer"))

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {THEMES[self.current_theme]['border']};")
        form_layout.addSpacing(10)
        form_layout.addWidget(line)
        form_layout.addSpacing(10)

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
        icon_color = 'black' if self.current_theme == 'light' else 'white'
        self.save_btn.setIcon(qta.icon('fa5s.save', color=icon_color))
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

    def toggle_edit_mode(self):
        is_editing = self.edit_btn.isChecked()
        for key, inp in self.inputs.items():
            inp.setReadOnly(not is_editing)
            if is_editing:
                inp.setStyleSheet(f"border: 1px solid {THEMES[self.current_theme]['accent']};")
            else:
                inp.setStyleSheet("")

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
        self.user_data['first_name'] = self.inputs['first_name'].text()
        self.user_data['last_name'] = self.inputs['last_name'].text()
        self.user_data['role'] = self.inputs['role'].text()
        self.refresh_profile_ui()
        self.edit_btn.setChecked(False)
        self.toggle_edit_mode()
        self.current_pass_input.clear()
        self.inputs['new_password'].clear()
        self.current_pass_input.setStyleSheet("")

    def on_update_error(self, err_msg):
        print(f"Update Failed: {err_msg}")
        QMessageBox.warning(self, "Error", "Incorrect Password or Server Error")
        self.current_pass_input.setStyleSheet("border: 1px solid red;")
        self.current_pass_input.setText("")
        self.current_pass_input.setPlaceholderText("Incorrect Password")

    def on_update_finished(self):
        self.save_btn.setText(" Save Changes")
        self.save_btn.setEnabled(True)

    def handle_save_profile(self):
        current_password = self.current_pass_input.text()
        if not current_password:
            self.current_pass_input.setStyleSheet("border: 1px solid red;")
            self.current_pass_input.setPlaceholderText("PASSWORD REQUIRED!")
            return

        payload = {
            "first_name": self.inputs['first_name'].text(),
            "last_name": self.inputs['last_name'].text(),
            "email": self.inputs['email'].text(),
            "company": self.inputs['company'].text(),
            "role": self.inputs['role'].text(),
            "currentPassword":  current_password,
            "newPassword": self.inputs['new_password'].text()
        }

        self.save_btn.setText("Saving...")
        self.save_btn.setEnabled(False)

        # FIX: Ensure URL includes /api/
        url = "http://127.0.0.1:8000/update/" 
        headers = { "Authorization": f"Token {self.token}", "Content-Type": "application/json" }

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
            
        if index == 1:
            self.fetch_history()

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
        if hasattr(self, 'save_btn'):
            icon_color = 'black' if self.current_theme == 'light' else 'white'
            self.save_btn.setIcon(qta.icon('fa5s.save', color=icon_color))

    def handle_logout(self):
        self.login_win = LoginWindow() 
        self.login_win.current_theme = self.current_theme
        self.login_win.apply_theme()
        self.login_win.show()
        self.close()

class MplBarChart(FigureCanvas):
   
    def __init__(self, labels, values, theme_colors, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor('none')
        super().__init__(self.fig)
        
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('none')
        
        bar_colors = ['#38bdf8', '#818cf8', '#f472b6']
        bars = self.axes.bar(labels, values, color=bar_colors, alpha=0.7, width=0.5)
        
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['left'].set_visible(False)
        self.axes.spines['bottom'].set_color(theme_colors['text_secondary'])
        
        self.axes.tick_params(axis='x', colors=theme_colors['text_secondary'])
        self.axes.tick_params(axis='y', colors=theme_colors['text_secondary'])
       
        for bar in bars:
            height = bar.get_height()
            self.axes.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                ha='center', va='bottom', color=theme_colors['text_primary'], fontsize=9)
        
        self.fig.tight_layout()
    
    def get_image_base64(self):
        buffer = io.BytesIO()
        self.fig.savefig(buffer, format='png', transparent=True)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png)
        return graphic.decode('utf-8')

class HistoryCard(QFrame):
    download_requested = pyqtSignal(object, object)
    def __init__(self, record, theme_colors):
        super().__init__()
        self.setObjectName("GlassCard")
        self.setFixedSize(350, 320)
        self.record = record
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        dt = QDateTime.fromString(record['created_at'], Qt.ISODate)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        date_lbl = QLabel(dt.toString("MMM d, yyyy"))
        date_lbl.setStyleSheet(f"color: {theme_colors['text_primary']}; font-weight: bold; font-size: 16px;")
        
        sep_lbl = QLabel("•")
        sep_lbl.setStyleSheet(f"color: {theme_colors['accent']}; font-size: 18px; line-height: 1;")

        time_lbl = QLabel(dt.toString("h:mm AP"))
        time_lbl.setStyleSheet(f"color: {theme_colors['text_secondary']}; font-size: 13px;")

        header_layout.addWidget(date_lbl)
        header_layout.addWidget(sep_lbl)
        header_layout.addWidget(time_lbl)
        header_layout.addStretch()
        
        dl_btn = QPushButton()
        dl_btn.setIcon(qta.icon('fa5s.download', color=theme_colors['text_secondary']))
        dl_btn.setToolTip("Download Report")
        dl_btn.setCursor(Qt.PointingHandCursor)
        dl_btn.setStyleSheet("background: transparent; border: none;")
        dl_btn.clicked.connect(self.on_download_click)
        header_layout.addWidget(dl_btn) 
        
        layout.addLayout(header_layout) # Added only once now
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {theme_colors['border']}; margin: 5px 0;")
        layout.addWidget(line)

        labels = record['distribution']['labels']
        values = record['distribution']['values']
        
        self.chart = MplBarChart(labels, values, theme_colors, width=3.2, height=2.2)
        layout.addWidget(self.chart)

    def on_download_click(self):
        self.download_requested.emit(self.record, self.chart)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = LoginWindow()
    window.show()
    
    sys.exit(app.exec_())