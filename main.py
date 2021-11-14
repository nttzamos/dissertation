from PyQt6.QtWidgets import QApplication

import sys

app = QApplication(sys.argv)
from mainWindow import MainWindow
window = MainWindow()
window.showMaximized()
sys.exit(app.exec())
