from PyQt5.QtCore import QThread, pyqtSignal
import requests

class APIWorker(QThread):
    success = pyqtSignal(dict)
    error = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, url, data=None, method="POST", headers=None):
        super().__init__()
        self.url = url
        self.data = data
        self.method = method
        self.headers = headers or {}

    def run(self):
        try:
            if self.method == "POST":
                response = requests.post(self.url, json=self.data, headers=self.headers)
            elif self.method == "PATCH":
                response = requests.patch(self.url, json=self.data, headers=self.headers)
            elif self.method == "GET":
                response = requests.get(self.url, headers=self.headers)
            
            if 200 <= response.status_code < 300:
                try:
                    data = response.json()
                except:
                    data = {"message": "Success"} 
                self.success.emit(data)
            else:
                self.error.emit(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            self.error.emit("Connection failed. Check server.")
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

if __name__ == "__main__":
    print("Error: Run Main.py to start the application!")