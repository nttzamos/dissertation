from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QIcon

from models.recent_search import create_recent_search, destroy_recent_search
from models.starred_word import create_starred_word, destroy_starred_word

class RecentSearch(QWidget):
  RELOAD_TEXT = 'Αναζήτηση'
  STAR_TEXT = 'Προσθήκη στα Αγαπημένα'
  DELETE_TEXT = 'Αφαίρεση από τις Πρόσφατες Αναζητήσεις'

  def __init__(self, word, is_starred):
    super().__init__()

    self.setFixedHeight(50)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    from menu.settings import Settings
    font = QFont(Settings.font, 14)

    data_widget = QWidget()
    data_widget.layout = QHBoxLayout(data_widget)
    data_widget.layout.setContentsMargins(0, 0, 0, 0)

    self.word = QLabel(word)
    self.word.setFont(font)

    reload_button = QPushButton()
    reload_button.setIcon(QIcon('resources/reload.svg'))
    reload_button.setToolTip(RecentSearch.RELOAD_TEXT)
    reload_button.clicked.connect(self.reload_word)
    reload_button.setFixedWidth(30)

    self.star_button = QPushButton()
    self.star_button.setToolTip(RecentSearch.STAR_TEXT)
    self.star_button.clicked.connect(self.toggle_starred_state)
    self.star_button.setFixedWidth(30)

    self.is_starred = is_starred
    if self.is_starred:
      self.star_button.setIcon(QIcon('resources/starred.svg'))
    else:
      self.star_button.setIcon(QIcon('resources/unstarred.svg'))

    delete_button = QPushButton()
    delete_button.setIcon(QIcon('resources/delete.svg'))
    delete_button.setToolTip(RecentSearch.DELETE_TEXT)
    delete_button.clicked.connect(self.remove_word)
    delete_button.setFixedWidth(30)

    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Plain)

    data_widget.layout.addSpacing(5)
    data_widget.layout.addWidget(self.word)
    data_widget.layout.addWidget(reload_button)
    data_widget.layout.addWidget(self.star_button)
    data_widget.layout.addWidget(delete_button)
    data_widget.layout.addSpacing(5)

    self.layout.addWidget(data_widget)
    self.layout.addWidget(line)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.item_widgets_style)

  def reload_word(self):
    word = self.word.text()
    from central.main_widget import MainWidget
    from side.recent_searches_widget import RecentSearchesWidget
    MainWidget.add_word(word)
    create_recent_search(word)
    RecentSearchesWidget.remove_and_add_recent_search(word)

  def toggle_starred_state(self):
    from side.starred_words_widget import StarredWordsWidget
    word = self.word.text()

    if self.is_starred:
      destroy_starred_word(word)
      StarredWordsWidget.toggle_starred_word_starred_state(word)
    else:
      create_starred_word(word)
      StarredWordsWidget.add_starred_word(word)

    self.toggle_starred_icon()

  def toggle_starred_icon(self):
    if self.is_starred:
      self.is_starred = False
      self.star_button.setIcon(QIcon('resources/unstarred.svg'))
    else:
      self.is_starred = True
      self.star_button.setIcon(QIcon('resources/starred.svg'))

  def remove_word(self):
    from side.recent_searches_widget import RecentSearchesWidget
    destroy_recent_search(self.word.text())
    self.hide()
    RecentSearchesWidget.remove_recent_search(self)
    self.deleteLater()

  def update_word(self, new_word):
    self.word.setText(new_word)
