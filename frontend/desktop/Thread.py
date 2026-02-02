import requests
from PyQt5.QtCore import QThread, pyqtSignal

class APIWorker(QThread):
    # Signals to update the UI from the background thread
    success = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, url, data):
        super().__init__()
        self.url = url
        self.data = data

    def run(self):
        try:
            # This happens in the background
            response = requests.post(self.url, json=self.data)
            
            if response.status_code == 200:
                # Emit the JSON dictionary to the main thread
                self.success.emit(response.json())
            else:
                # Handle 401/403/500 errors
                err_msg = response.json().get('error', 'Unknown Error')
                self.error.emit(err_msg)
                
        except requests.exceptions.ConnectionError:
            self.error.emit("Failed to connect to server.")
        except Exception as e:
            self.error.emit(str(e))