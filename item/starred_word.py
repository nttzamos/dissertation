from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QIcon

from models.recent_search import create_recent_search
from models.starred_word import destroy_starred_word

class StarredWord(QWidget):
  def __init__(self, word):
    super().__init__()

    self.setFixedHeight(50)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    self.data_widget = QWidget()
    self.data_widget.layout = QHBoxLayout(self.data_widget)
    self.data_widget.layout.setContentsMargins(0, 0, 0, 0)

    self.word = QLabel(word)
    from menu.settings import Settings
    font = QFont(Settings.font, 14)
    self.word.setFont(font)

    self.reload_button = QPushButton()
    self.reload_button.setIcon(QIcon('resources/reload.svg'))
    self.reload_button.clicked.connect(self.reload_word)
    self.reload_button.setFixedWidth(30)

    self.star_button = QPushButton()
    self.star_button.clicked.connect(self.toggle_starred_state)
    self.star_button.setFixedWidth(30)
    self.star_button.setIcon(QIcon('resources/starred.svg'))

    self.line = QFrame()
    self.line.setFrameShape(QFrame.Shape.HLine)
    self.line.setFrameShadow(QFrame.Shadow.Plain)

    self.data_widget.layout.addSpacing(5)
    self.data_widget.layout.addWidget(self.word)
    self.data_widget.layout.addWidget(self.reload_button)
    self.data_widget.layout.addWidget(self.star_button)
    self.data_widget.layout.addSpacing(5)

    self.layout.addWidget(self.data_widget)
    self.layout.addWidget(self.line)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.item_widgets_style)

  def toggle_starred_state(self):
    from side.recent_searches_widget import RecentSearchesWidget
    word = self.word.text()
    destroy_starred_word(word)
    RecentSearchesWidget.toggle_recent_search_starred_icon(word)
    self.remove_word()

  def remove_word(self):
    from side.starred_words_widget import StarredWordsWidget
    self.hide()
    StarredWordsWidget.remove_starred_word(self)
    self.deleteLater()

  def reload_word(self):
    word = self.word.text()
    from central.main_widget import MainWidget
    from side.recent_searches_widget import RecentSearchesWidget
    MainWidget.add_word(word)
    recent_search_exists = create_recent_search(word)
    if recent_search_exists:
      RecentSearchesWidget.remove_and_add_recent_search(word)
    else:
      RecentSearchesWidget.add_recent_search(word)
