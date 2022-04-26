from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QDialog, QMessageBox, QCheckBox
from PyQt6.QtGui import QIcon

from dialogs.word_addition_widget import WordAdditionWIdget
from dialogs.word_family_update_widget import WordFamilyUpdateWidget
from dialogs.word_update_widget import WordUpdateWidget
from menu.settings import Settings
from shared.font_settings import FontSettings

import gettext

class WordEditingWidget(QDialog):
  def __init__(self):
    super().__init__()

    language_code = Settings.get_setting('language')
    language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
    language.install()
    self._ = language.gettext

    self.setWindowTitle(self._('EDIT_WORDS_TEXT'))
    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setFixedWidth(Settings.get_setting('screen_width') / 2)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    add_word_widget = WordAdditionWIdget()
    self.edit_word_widget = WordUpdateWidget()
    WordEditingWidget.edit_word_family_widget = WordFamilyUpdateWidget()

    self.tab_widget = QTabWidget()
    self.tab_widget.setFont(FontSettings.get_font('text'))

    self.tab_widget.addTab(add_word_widget, self._('ADD_WORD_TEXT'))
    self.tab_widget.addTab(self.edit_word_widget, self._('EDIT_WORD_TEXT'))
    self.tab_widget.addTab(
      WordEditingWidget.edit_word_family_widget, self._('EDIT_FAMILY_TEXT')
    )

    self.layout.addWidget(self.tab_widget)

  def reject(self):
    if self.edit_word_widget.save_button_is_active():
      close_widget = self.show_unsaved_changes_message()

      if not close_widget:
        return

    self.done(1)

  def closeEvent(self, event):
    if self.edit_word_widget.save_button_is_active():
      close_widget = self.show_unsaved_changes_message()

      if not close_widget:
        event.ignore()

  def hideEvent(self, event):
    from search.searching_widget import SearchingWidget
    SearchingWidget.update_selected_dictionary()

  def set_current_tab_index(self, index):
    self.tab_widget.setCurrentIndex(index)

  def set_word_to_update(self, word, grade_id):
    self.edit_word_widget.set_word_to_update(word, grade_id)

  def show_unsaved_changes_message(self):
    if not Settings.get_boolean_setting('show_unsaved_changes_message'): return True

    title = self._('UNSAVED_CHANGES_TITLE')
    question = self._('UNSAVED_CHANGES_TEXT')

    answer = QMessageBox(self)
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(question)
    answer.setWindowTitle(title)

    yes_button = answer.addButton(self._('YES'), QMessageBox.ButtonRole.YesRole)
    cancel_button = answer.addButton(self._('CANCEL'), QMessageBox.ButtonRole.RejectRole)

    answer.setDefaultButton(cancel_button)

    check_box = QCheckBox(self._('UNSAVED_CHANGES_MESSAGE_VISIBILITY'))
    check_box.clicked.connect(self.toggle_unsaved_changes_setting)
    check_box.setChecked(True)

    answer.setCheckBox(check_box)
    answer.exec()

    if answer.clickedButton() == yes_button:
      return True

    return False

  def toggle_unsaved_changes_setting(self, value):
    Settings.set_boolean_setting('show_unsaved_changes_message', value)

  @staticmethod
  def update_word_family_update_widget(word, grade_id):
    WordEditingWidget.edit_word_family_widget.update_word_family_update_widget(word, grade_id)
