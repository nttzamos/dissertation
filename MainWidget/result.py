from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from Common.styles import Styles
from Common.database_handler import get_grade_subjects
from models.recent_search import create_recent_search
from models.starred_word import create_starred_word, starred_word_exists, destroy_starred_word
from models.word import create_word, word_exists
from models.family import update_word_family

class Result(QWidget):
  def __init__(self, word, widget_width = None, initial = False, state = 1):
    super().__init__()

    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 10, 10)

    self.state = state

    if widget_width != None:
      self.setFixedWidth(widget_width)

    data_widget = QWidget()
    data_widget.layout = QVBoxLayout(data_widget)
    data_widget.layout.setContentsMargins(0, 25, 0, 25)

    # Word
    self.word_label = QLabel(self, text=word)
    self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    from MenuBar.settings import Settings
    font = QFont(Settings.font, 20)
    self.word_label.setFont(font)

    # Buttons
    self.buttons_widget = QWidget()
    self.buttons_widget.layout = QHBoxLayout(self.buttons_widget)
    self.buttons_widget.layout.setContentsMargins(0, 0, 0, 0)

    self.add_to_dict_button = QPushButton()
    self.add_to_dict_button.setToolTip('Add this word to the selected subjects.')
    self.add_to_dict_button.setIcon(QIcon('Resources/book1.png'))
    self.add_to_dict_button.clicked.connect(self.add_word_to_dictionary)
    self.add_to_dict_button.setFixedWidth(30)

    self.add_to_family_button = QPushButton()
    self.add_to_family_button.setToolTip('Add this word to the family of the searched word.')
    self.add_to_family_button.setIcon(QIcon('Resources/plus1.png'))
    self.add_to_family_button.clicked.connect(self.add_word_to_family)
    self.add_to_family_button.setFixedWidth(30)

    self.remove_from_family_button = QPushButton()
    self.remove_from_family_button.setToolTip('Remove this word from the family of this word.')
    self.remove_from_family_button.setIcon(QIcon('Resources/delete2.svg'))
    self.remove_from_family_button.clicked.connect(self.remove_word_from_family)
    self.remove_from_family_button.setFixedWidth(30)

    if self.state == 1:
      self.buttons_widget.layout.addWidget(self.remove_from_family_button)
    elif self.state == 2:
      self.buttons_widget.layout.addWidget(self.add_to_family_button)
    else:
      self.buttons_widget.layout.addWidget(self.add_to_dict_button)
      self.buttons_widget.layout.addWidget(self.add_to_family_button)

    data_widget.layout.addWidget(self.word_label)
    data_widget.layout.addSpacing(5)
    data_widget.layout.addWidget(self.buttons_widget)

    self.layout.addWidget(data_widget)

    self.style()

  def style(self):
    if self.state == 1:
      self.setStyleSheet(Styles.offline_result_style)
    elif self.state == 2:
      self.setStyleSheet(Styles.online_saved_result_style)
    else:
      self.setStyleSheet(Styles.online_result_style)

    self.buttons_widget.setStyleSheet(Styles.result_buttons_style)

  def add_word_to_dictionary(self):
    from MainWidget.currentSearch import CurrentSearch
    word = self.word_label.text()
    x, y, z, subject_names = CurrentSearch.get_current_selection_details()
    subject_names = [subject_names]

    if subject_names[0] == 'All Subjects':
      subject_names = get_grade_subjects(CurrentSearch.grade_id)
    create_word(word, CurrentSearch.grade_id, subject_names)
    self.state = 2
    self.setStyleSheet(Styles.online_saved_result_style)
    self.add_to_dict_button.hide()
    self.add_to_dict_button.deleteLater()

  def add_word_to_family(self):
    if self.state == 3:
      self.add_word_to_dictionary()

    from MainWidget.currentSearch import CurrentSearch
    word = self.word_label.text()
    update_word_family(CurrentSearch.grade_id, CurrentSearch.searched_word.text(), [word], [])
    self.state = 1
    self.setStyleSheet(Styles.offline_result_style)
    self.add_to_family_button.hide()
    self.add_to_family_button.deleteLater()
    self.buttons_widget.layout.addWidget(self.remove_from_family_button)

  def remove_word_from_family(self):
    from MainWidget.currentSearch import CurrentSearch
    word = self.word_label.text()
    update_word_family(CurrentSearch.grade_id, CurrentSearch.searched_word.text(), [], [word])
    self.hide()

  def toggle_starred_state(self):
    from SideWidgets.starredWordsWidget import StarredWordsWidget
    from SideWidgets.recentSearchesWidget import RecentSearchesWidget
    word = self.word_label.text()

    RecentSearchesWidget.toggle_recent_search_starred_icon(word)
    if self.is_starred:
      self.is_starred = False
      self.star_button.setIcon(QIcon('Resources/unstarred.svg'))
      destroy_starred_word(word)
      StarredWordsWidget.toggle_starred_word_starred_state(word)
    else:
      self.is_starred = True
      self.star_button.setIcon(QIcon('Resources/starred.svg'))
      create_starred_word(word)
      StarredWordsWidget.add_starred_word(word)
