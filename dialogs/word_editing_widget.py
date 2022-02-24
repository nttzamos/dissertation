from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QDialog
from PyQt6.QtGui import QIcon

from dialogs.word_addition_widget import WordAdditionWIdget
from dialogs.word_family_update_widget import WordFamilyUpdateWidget
from dialogs.word_update_widget import WordUpdateWidget
from menu.settings import Settings

class WordEditingWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Edit Words')
    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setFixedWidth(Settings.get_setting('screen_width') / 2)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    # Add a new word
    add_word_widget = WordAdditionWIdget()

    # Edit existing words widget
    edit_word_widget = WordUpdateWidget()

    # Edit existing word family widget
    edit_word_family_widget = WordFamilyUpdateWidget()

    tab_widget = QTabWidget()
    tab_widget.addTab(add_word_widget, 'Add a new word')
    tab_widget.addTab(edit_word_widget, 'Update existing word')
    tab_widget.addTab(edit_word_family_widget, 'Update family of existing word')

    self.layout.addWidget(tab_widget)

  def closeEvent(self, event):
    from search.searching_widget import SearchingWidget
    SearchingWidget.update_selected_dictionary()

  def hideEvent(self, event):
    from search.searching_widget import SearchingWidget
    SearchingWidget.update_selected_dictionary()
