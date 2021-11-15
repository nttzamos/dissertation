from PyQt6.QtWidgets import QApplication
from boxLayout import BoxLayout
from window import Window

import sys

# app = QApplication(sys.argv)
# window = Window()
# window.show()
# sys.exit(app.exec())

app = QApplication(sys.argv)
window = BoxLayout()
window.show()

BoxLayout.addRow()
BoxLayout.addRow()
BoxLayout.addRow()

sys.exit(app.exec())

