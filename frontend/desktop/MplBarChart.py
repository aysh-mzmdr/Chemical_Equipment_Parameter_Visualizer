import base64
import io
from StyleSheetManager import * 
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')

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