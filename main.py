from PyQt6.QtWidgets import QApplication

import sys

app = QApplication(sys.argv)

# Imports must be below here
from settings import Settings
Settings.screenWidth = app.primaryScreen().size().width()
Settings.calculateSizeSettings()
print("Hello")

from mainWindow import MainWindow
from MainWidget.searchingWidget import SearchingWidget

window = MainWindow()
window.showMaximized()

SearchingWidget.setFocusToSearchBar()

sys.exit(app.exec())
