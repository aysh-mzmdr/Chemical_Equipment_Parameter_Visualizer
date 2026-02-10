import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QIcon
import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    try:
        from ctypes import windll
        myappid = 'mycompany.myproduct.subproduct.version'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass

    app.setWindowIcon(QIcon("../flask.svg"))

    window = LoginWindow.LoginWindow()
    window.show()
    
    sys.exit(app.exec_())