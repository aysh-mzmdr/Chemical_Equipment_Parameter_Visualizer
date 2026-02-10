from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame,
)
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal
import qtawesome as qta
from StyleSheetManager import * 
import MplBarChart

class AnalysisResultWidget(QFrame):
    download_requested = pyqtSignal(object, object)
    
    def __init__(self, data, theme_colors):
        super().__init__()
        self.setObjectName("GlassCard")
        self.data = data
        self.theme_colors = theme_colors
        
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

        stats_layout = QHBoxLayout()
        stats = data.get('averages', {})
        total = data.get('total_count', 0)

        stats_layout.addWidget(self.create_stat_block("Total Units", total))
        stats_layout.addWidget(self.create_stat_block("Avg Pressure", stats.get('pressure', 0), "bar"))
        stats_layout.addWidget(self.create_stat_block("Avg Temp", stats.get('temperature', 0), "°C"))
        
        layout.addLayout(stats_layout)
        layout.addSpacing(30)

        chart_data = data.get('distribution', {})
        if chart_data:
            labels = chart_data.get('labels', [])
            values = chart_data.get('values', [])
            
            self.chart = MplBarChart.MplBarChart(labels, values, theme_colors, width=5, height=4)
            layout.addWidget(self.chart)

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
