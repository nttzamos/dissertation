from PyQt6.QtWidgets import QApplication

import sys

app = QApplication(sys.argv)

# Imports must be below here
from Common.databaseHandler import DBHandler
DBHandler.initialize_databases()

from MenuBar.settings import Settings
screen_width = app.primaryScreen().size().width()
screen_height = app.primaryScreen().size().height()
Settings.initialize_settings_database(screen_width, screen_height)

from MainWidget.mainWindow import MainWindow
from MainWidget.searchingWidget import SearchingWidget

window = MainWindow()
window.showMaximized()

SearchingWidget.set_focus_to_search_bar()

sys.exit(app.exec())
