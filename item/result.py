from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
                             QWidget, QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from models.word import create_word, destroy_word
from models.related_word import update_related_words
from shared.database_handler import get_grade_subjects
from shared.font_settings import FontSettings
from shared.styles import Styles

import gettext

class Result(QWidget):
  def __init__(self, word, saved):
    super().__init__()

    from menu.settings import Settings
    self.language_code = Settings.get_setting('language')
    language = gettext.translation('item', localedir='resources/locale', languages=[self.language_code])
    language.install()
    Result._ = language.gettext

    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 20, 20)
    self.layout.setSpacing(0)

    font = FontSettings.get_font('result')

    self.saved = saved

    data_widget = QWidget()
    data_widget.layout = QVBoxLayout(data_widget)
    data_widget.layout.setContentsMargins(0, 25, 0, 25)
    data_widget.layout.setSpacing(0)

    self.word_label = QLabel(word)
    self.word_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.word_label.setFont(font)

    self.buttons_widget = QWidget()
    self.buttons_widget.layout = QHBoxLayout(self.buttons_widget)
    self.buttons_widget.layout.setContentsMargins(10, 0, 10, 0)
    self.buttons_widget.layout.setSpacing(0)

    self.add_to_family_button = QPushButton()
    self.add_to_family_button.setToolTip(Result._('ADD_BUTTON_TEXT'))
    self.add_to_family_button.setIcon(QIcon('resources/plus.png'))
    self.add_to_family_button.clicked.connect(self.add_word_to_family)
    self.add_to_family_button.setFixedWidth(30)

    self.remove_from_family_button = QPushButton()
    self.remove_from_family_button.setToolTip(Result._('REMOVE_BUTTON_TEXT'))
    self.remove_from_family_button.setIcon(QIcon('resources/delete.svg'))
    self.remove_from_family_button.clicked.connect(self.remove_word_from_family)
    self.remove_from_family_button.setFixedWidth(30)

    self.remove_from_subjects_button = QPushButton()
    self.remove_from_subjects_button.setToolTip(Result._('UNDO_ACTION'))
    self.remove_from_subjects_button.setIcon(QIcon('resources/undo.png'))
    self.remove_from_subjects_button.clicked.connect(self.undo_word_addition)
    self.remove_from_subjects_button.setFixedWidth(30)

    if self.saved:
      self.buttons_widget.layout.addWidget(self.remove_from_family_button)
    else:
      self.buttons_widget.layout.addWidget(self.add_to_family_button)

    data_widget.layout.addWidget(self.word_label)
    data_widget.layout.addSpacing(12)
    data_widget.layout.addWidget(self.buttons_widget)

    self.layout.addWidget(data_widget)

    self.style()

  def style(self):
    if self.saved:
      self.setStyleSheet(Styles.offline_result_style)
    else:
      self.setStyleSheet(Styles.online_result_style)

    self.buttons_widget.setStyleSheet(Styles.result_buttons_style)

  def add_word_to_family(self):
    from search.current_search import CurrentSearch

    word = self.word_label.text()

    create_word(word, CurrentSearch.grade_id, self.get_current_subjects())

    from search.searching_widget import SearchingWidget
    SearchingWidget.add_or_remove_dictionary_words([word], [])

    self.add_word()

  def remove_word_from_family(self):
    from menu.settings import Settings
    if not Settings.get_boolean_setting('hide_remove_word_from_family_message'):
      if not self.get_permission_to_remove():
        return

    from search.current_search import CurrentSearch
    self.hide()

    update_related_words(
      CurrentSearch.grade_id,
      CurrentSearch.searched_word_label.text(), [], [self.word_label.text()]
    )

    from central.results_widget import ResultsWidget
    ResultsWidget.remove_result(self)

  def add_word(self):
    from search.current_search import CurrentSearch
    update_related_words(
      CurrentSearch.grade_id,
      CurrentSearch.searched_word_label.text(), [self.word_label.text()], []
    )

    self.saved = True
    self.setStyleSheet(Styles.offline_result_style)
    self.add_to_family_button.hide()
    self.remove_from_family_button.show()
    self.remove_from_subjects_button.show()
    self.buttons_widget.layout.addWidget(self.remove_from_family_button)
    self.buttons_widget.layout.addWidget(self.remove_from_subjects_button)

  def update_word(self, new_word):
    self.word_label.setText(new_word)

  def undo_word_addition(self):
    from search.current_search import CurrentSearch
    destroy_word(self.word_label.text(), [CurrentSearch.grade_id])

    from search.searching_widget import SearchingWidget
    SearchingWidget.add_or_remove_dictionary_words([], [self.word_label.text()])

    self.saved = False
    self.setStyleSheet(Styles.online_result_style)
    self.remove_from_family_button.hide()
    self.remove_from_subjects_button.hide()
    self.add_to_family_button.show()
    self.buttons_widget.layout.addWidget(self.add_to_family_button)

  def get_current_subjects(self):
    from search.current_search import CurrentSearch

    x, y, z, current_subject_name = CurrentSearch.get_current_selection_details()
    subject_names = [current_subject_name]

    language = gettext.translation('search', localedir='resources/locale', languages=[self.language_code])
    language.install()
    if subject_names[0] == language.gettext('ALL_SUBJECTS_TEXT'):
      subject_names = get_grade_subjects(CurrentSearch.grade_id)

    return subject_names

  def get_permission_to_remove(self):
    title = Result._('REMOVE_BUTTON_TEXT')
    question = Result._('REMOVE_WORD_FROM_FAMILY_PERMISSION')

    answer = QMessageBox()

    answer.setFont(FontSettings.get_font('text'))
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(question)
    answer.setWindowTitle(title)

    yes_button = answer.addButton(Result._('YES'), QMessageBox.ButtonRole.YesRole)
    yes_button.setFont(FontSettings.get_font('text'))
    cancel_button = answer.addButton(Result._('CANCEL'), QMessageBox.ButtonRole.RejectRole)
    cancel_button.setFont(FontSettings.get_font('text'))

    from shared.styles import Styles
    yes_button.setStyleSheet(Styles.dialog_button_style)
    cancel_button.setStyleSheet(Styles.dialog_default_button_style)

    answer.setDefaultButton(cancel_button)

    check_box = QCheckBox(Result._('HIDE_MESSAGE_CHECKBOX'))
    check_box.setFont(FontSettings.get_font('text'))
    check_box.clicked.connect(self.toggle_message_setting)
    check_box.setChecked(False)

    answer.setCheckBox(check_box)
    answer.exec()

    if answer.clickedButton() == yes_button:
      return True

    return False

  @staticmethod
  def toggle_message_setting(value):
    from menu.settings import Settings
    Settings.set_boolean_setting('hide_remove_word_from_family_message', value)
