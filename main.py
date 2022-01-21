from PyQt6.QtWidgets import QApplication

import sys

app = QApplication(sys.argv)

# Imports must be below here
from databaseHandler import DBHandler
DBHandler.initializeDatabases()

from settings import Settings
screenWidth = app.primaryScreen().size().width()
screenHeight = app.primaryScreen().size().height()
Settings.initializeSettingsDatabase(screenWidth, screenHeight)

from mainWindow import MainWindow
from MainWidget.searchingWidget import SearchingWidget

window = MainWindow()
window.showMaximized()

SearchingWidget.setFocusToSearchBar()

sys.exit(app.exec())
