from PyQt6.QtWidgets import QApplication

import sys

app = QApplication(sys.argv)

# Imports must be below here
# from shared.pdf_parser import PdfParser
# for grade in range(1, 7):
#   PdfParser.convert_books_to_text_files(grade)

from shared.database_handler import initialize_databases
initialize_databases()

from menu.settings import Settings
screen_width = app.primaryScreen().size().width()
screen_height = app.primaryScreen().size().height()
Settings.initialize_settings_database(screen_width, screen_height)

from central.main_window import MainWindow
from search.searching_widget import SearchingWidget

window = MainWindow()
window.showMaximized()

SearchingWidget.set_focus_to_search_bar()

if Settings.get_boolean_setting('show_tutorial_on_startup'):
  from dialogs.tutorial_widget import TutorialWidget
  tutorial_widget = TutorialWidget()
  tutorial_widget.exec()

sys.exit(app.exec())
