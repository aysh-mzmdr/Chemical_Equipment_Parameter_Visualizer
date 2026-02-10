import requests
from PyQt5.QtCore import QThread, pyqtSignal
from StyleSheetManager import * 
import matplotlib

matplotlib.use('Qt5Agg')

class DownloadWorker(QThread):
    finished = pyqtSignal(bool, str) 

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
            response = requests.post(self.url, json=self.payload, headers=headers)

            if response.status_code == 200:
                with open(self.save_path, 'wb') as f:
                    f.write(response.content)
                self.finished.emit(True, "PDF Downloaded Successfully!")
            else:
                self.finished.emit(False, f"Server Error: {response.status_code}")
        except Exception as e:
            self.finished.emit(False, str(e))

if __name__ == "__main__":
    print("Error: Run Main.py to start the application!")