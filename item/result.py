from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from models.family import update_word_family
from models.word import create_word
from shared.database_handler import get_grade_subjects
from shared.styles import Styles

import gettext

class Result(QWidget):
  def __init__(self, word, widget_width=None, saved=True):
    super().__init__()

    from menu.settings import Settings
    self.language_code = Settings.get_setting('language')
    language = gettext.translation('item', localedir='resources/locale', languages=[self.language_code])
    language.install()
    _ = language.gettext

    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 10, 10)
    self.layout.setSpacing(0)

    font = QFont(Settings.FONT, 20)

    self.saved = saved

    if widget_width != None:
      self.setFixedWidth(widget_width)

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
    self.buttons_widget.layout.setContentsMargins(0, 0, 0, 0)

    self.add_to_family_button = QPushButton()
    self.add_to_family_button.setToolTip(_('ADD_BUTTON_TEXT'))
    self.add_to_family_button.setIcon(QIcon('resources/plus.png'))
    self.add_to_family_button.clicked.connect(self.add_word_to_family)
    self.add_to_family_button.setFixedWidth(30)

    self.remove_from_family_button = QPushButton()
    self.remove_from_family_button.setToolTip(_('REMOVE_BUTTON_TEXT'))
    self.remove_from_family_button.setIcon(QIcon('resources/delete.svg'))
    self.remove_from_family_button.clicked.connect(self.remove_word_from_family)
    self.remove_from_family_button.setFixedWidth(30)

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

    x, y, z, current_subject_name = CurrentSearch.get_current_selection_details()
    subject_names = [current_subject_name]

    language = gettext.translation('search', localedir='resources/locale', languages=[self.language_code])
    language.install()
    if subject_names[0] == language.gettext('ALL_SUBJECTS_TEXT'):
      subject_names = get_grade_subjects(CurrentSearch.grade_id)

    create_word(word, CurrentSearch.grade_id, subject_names)

    from search.searching_widget import SearchingWidget
    SearchingWidget.add_or_remove_dictionary_words([word], [])

    self.add_word()

  def remove_word_from_family(self):
    from search.current_search import CurrentSearch
    word = self.word_label.text()
    self.hide()

    update_word_family(
      CurrentSearch.grade_id,
      CurrentSearch.searched_word_label.text(), [], [word]
    )

    from central.results_widget import ResultsWidget
    ResultsWidget.remove_result(self)

  def add_word(self):
    from search.current_search import CurrentSearch
    update_word_family(
      CurrentSearch.grade_id,
      CurrentSearch.searched_word_label.text(), [self.word_label.text()], []
    )

    self.saved = True
    self.setStyleSheet(Styles.offline_result_style)
    self.add_to_family_button.hide()
    self.add_to_family_button.deleteLater()
    self.buttons_widget.layout.addWidget(self.remove_from_family_button)

  def update_word(self, new_word):
    self.word_label.setText(new_word)
