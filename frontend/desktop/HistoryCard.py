from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal
import qtawesome as qta
from StyleSheetManager import * 
import MplBarChart

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
        
        layout.addLayout(header_layout)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {theme_colors['border']}; margin: 5px 0;")
        layout.addWidget(line)

        labels = record['distribution']['labels']
        values = record['distribution']['values']
        
        self.chart = MplBarChart.MplBarChart(labels, values, theme_colors, width=3.2, height=2.2)
        layout.addWidget(self.chart)

    def on_download_click(self):
        self.download_requested.emit(self.record, self.chart)

if __name__ == "__main__":
    print("Error: Run Main.py to start the application!")