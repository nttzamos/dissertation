from PyQt6.QtWidgets import QApplication

import sys

app = QApplication(sys.argv)

# Imports must be below here
from settings import Settings
from mainWindow import MainWindow
from MainWidget.searchingWidget import SearchingWidget

window = MainWindow()
window.showMaximized()

Settings.screenWidth = app.primaryScreen().size().width()
SearchingWidget.setFocusToSearchBar()

sys.exit(app.exec())
