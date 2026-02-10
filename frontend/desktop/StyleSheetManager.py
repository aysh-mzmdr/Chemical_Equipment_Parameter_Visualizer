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
        'input_bg': "rgba(30, 41, 59, 0.5)",
        'btn_text': 'white'
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
        'input_bg': "#ffffff",
        'btn_text': 'black'
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
                font-size: 28px;
                font-weight: bold;
            }}
            QLabel#Subtitle {{
                color: {t['text_secondary']};
                font-size: 18px;
                min-height: 100px;
            }}
            QLabel#LogoText {{
                font-size: 18px;
                font-weight: bold;
            }}
            QLabel#Domain_name {{
                font-size: 20px;
                font-weight: bold;
            }}

            /* Input Fields */
            QLineEdit {{
                background-color: {t['input_bg']};
                border: 1px solid {t['border']};
                border-radius: 8px;
                padding: 10px;
                color: {t['text_primary']};
                font-size: 18px;
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
                font-size: 18px;
                border: none;
                margin-top: 25px;
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

            /* --- FIX: MESSAGE BOX STYLING --- */
            QMessageBox {{
                background-color: {t['bg_secondary']};
                border: 1px solid {t['border']};
            }}
            QMessageBox QLabel {{
                color: {t['text_primary']};
                background-color: transparent;
            }}
            QMessageBox QPushButton {{
                background-color: {t['input_bg']};
                color: {t['text_primary']};
                border: 1px solid {t['border']};
                border-radius: 6px;
                padding: 6px 15px;
                min-width: 80px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {t['accent']};
                color: white;
                border: 1px solid {t['accent']};
            }}
            QPushButton#PrimaryBtn {{
                background-color: {t['accent']};
                
                /* FIX: Use dynamic text color instead of hardcoded 'white' */
                color: {t['btn_text']}; 
                
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 18px;
                border: none;
                margin-top: 25px;
            }}
        """
    
if __name__ == "__main__":
    print("Error: Run Main.py to start the application!")