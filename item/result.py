from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from models.family import update_word_family
from models.word import create_word
from shared.database_handler import get_grade_subjects
from shared.styles import Styles

class Result(QWidget):
  ADD_BUTTON_TEXT = 'Προσθήκη στις λέξεις των επιλεγμένων μαθήματων'
  REMOVE_BUTTON_TEXT = 'Αφαίρεση από τις συγγενικές λέξεις'

  def __init__(self, word, widget_width=None, saved=True):
    super().__init__()

    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 10, 10)

    from menu.settings import Settings
    font = QFont(Settings.font, 20)

    self.saved = saved

    if widget_width != None:
      self.setFixedWidth(widget_width)

    data_widget = QWidget()
    data_widget.layout = QVBoxLayout(data_widget)
    data_widget.layout.setContentsMargins(0, 25, 0, 25)

    self.word_label = QLabel(self, text=word)
    self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.word_label.setFont(font)

    self.buttons_widget = QWidget()
    self.buttons_widget.layout = QHBoxLayout(self.buttons_widget)
    self.buttons_widget.layout.setContentsMargins(0, 0, 0, 0)

    self.add_to_family_button = QPushButton()
    self.add_to_family_button.setToolTip(Result.ADD_BUTTON_TEXT)
    self.add_to_family_button.setIcon(QIcon('resources/plus.png'))
    self.add_to_family_button.clicked.connect(self.add_word_to_family)
    self.add_to_family_button.setFixedWidth(30)

    self.remove_from_family_button = QPushButton()
    self.remove_from_family_button.setToolTip(Result.REMOVE_BUTTON_TEXT)
    self.remove_from_family_button.setIcon(QIcon('resources/delete.svg'))
    self.remove_from_family_button.clicked.connect(self.remove_word_from_family)
    self.remove_from_family_button.setFixedWidth(30)

    if self.saved:
      self.buttons_widget.layout.addWidget(self.remove_from_family_button)
    else:
      self.buttons_widget.layout.addWidget(self.add_to_family_button)

    data_widget.layout.addWidget(self.word_label)
    data_widget.layout.addSpacing(5)
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
    x, y, z, subject_names = CurrentSearch.get_current_selection_details()
    subject_names = [subject_names]

    if subject_names[0] == CurrentSearch.ALL_SUBJECTS_TEXT:
      subject_names = get_grade_subjects(CurrentSearch.grade_id)
    create_word(word, CurrentSearch.grade_id, subject_names)

    from search.searching_widget import SearchingWidget
    SearchingWidget.add_or_remove_dictionary_words([word], [])

    update_word_family(CurrentSearch.grade_id, CurrentSearch.searched_word_label.text(), [word], [])
    self.saved = True
    self.setStyleSheet(Styles.offline_result_style)
    self.add_to_family_button.hide()
    self.add_to_family_button.deleteLater()
    self.buttons_widget.layout.addWidget(self.remove_from_family_button)

  def remove_word_from_family(self):
    from search.current_search import CurrentSearch
    word = self.word_label.text()
    update_word_family(CurrentSearch.grade_id, CurrentSearch.searched_word_label.text(), [], [word])
    self.hide()

    from central.results_widget import ResultsWidget
    ResultsWidget.remove_result(self)

  def update_word(self, new_word):
    self.word_label.setText(new_word)
