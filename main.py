from PyQt6.QtWidgets import QApplication
from Classes.mainWindow import MainWindow

import sys

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())