from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class Result(QWidget):
  def __init__(self, word, widget_width=None, initial=False):
    super().__init__()

    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 10, 10)

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

    self.search_button = QPushButton()
    # self.search_button.setIcon(QIcon('Resources/reload.svg'))
    self.search_button.setIcon(QIcon('Resources/search.png'))
    self.search_button.clicked.connect(self.searchWord)
    self.search_button.setFixedWidth(30)

    self.star_button = QPushButton()
    self.star_button.clicked.connect(self.notify_starred)
    self.star_button.setFixedWidth(30)
    from Common.databaseHandler import DBHandler
    if (not initial) and DBHandler.starred_word_exists(word):
      self.star_button.setIcon(QIcon('Resources/starred.svg'))
      self.is_starred = True
    else:
      self.star_button.setIcon(QIcon('Resources/unstarred.svg'))
      self.is_starred = False

    self.buttons_widget.layout.addWidget(self.search_button)
    self.buttons_widget.layout.addWidget(self.star_button)

    data_widget.layout.addWidget(self.word_label)
    data_widget.layout.addWidget(self.buttons_widget)

    self.layout.addWidget(data_widget)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.result_style)

  def searchWord(self):
    from MainWidget.mainWidget import MainWidget
    from SideWidgets.recentSearchesWidget import RecentSearchesWidget
    from Common.databaseHandler import DBHandler
    word = self.word_label.text()

    MainWidget.add_word(word)

    recent_search_exists = DBHandler.add_recent_search(word)
    if recent_search_exists:
      RecentSearchesWidget.remove_and_add_recent_search(word)
    else:
      RecentSearchesWidget.add_recent_search(word, False)

  def notify_starred(self):
    from SideWidgets.starredWordsWidget import StarredWordsWidget
    from Common.databaseHandler import DBHandler
    word = self.word_label.text()

    if DBHandler.starred_word_exists(word):
      DBHandler.remove_starred_word(word)
      StarredWordsWidget.toggle_starred_bottom(word)
    else:
      DBHandler.add_starred_word(word)
      StarredWordsWidget.add_starred_word(word)

    self.toggle_starred_icon()

  def toggle_starred_icon(self):
    if self.is_starred:
      self.is_starred = False
      self.star_button.setIcon(QIcon('Resources/unstarred.svg'))
    else:
      self.is_starred = True
      self.star_button.setIcon(QIcon('Resources/starred.svg'))
