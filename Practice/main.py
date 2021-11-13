from PyQt6.QtWidgets import QApplication
from window import Window

import sys

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())