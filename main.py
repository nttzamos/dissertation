from PyQt6.QtWidgets import QApplication

import sys

app = QApplication(sys.argv)

# Imports must be below here
from central.main_window import MainWindow
from dialogs.tutorial_widget import TutorialWidget
from menu.settings import Settings
from shared.database_handler import initialize_databases
from shared.pdf_parser import PdfParser
from search.searching_widget import SearchingWidget

# for grade in range(1, 7):
#   PdfParser.convert_books_to_text_files(grade)

# initialize_databases()

screen_width = app.primaryScreen().size().width()
screen_height = app.primaryScreen().size().height()
Settings.initialize_settings_database(screen_width, screen_height)

window = MainWindow()
window.showMaximized()

SearchingWidget.set_focus_to_search_bar()

if Settings.get_boolean_setting('show_tutorial_on_startup'):
  tutorial_widget = TutorialWidget()
  tutorial_widget.exec()

sys.exit(app.exec())
