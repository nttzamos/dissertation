from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class Result(QWidget):
  def __init__(self, word, widgetWidth=None):
    super().__init__()

    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 10, 10)

    if widgetWidth != None:
      self.setFixedWidth(widgetWidth)

    dataWidget = QWidget()
    dataWidget.layout = QVBoxLayout(dataWidget)
    dataWidget.layout.setContentsMargins(0, 25, 0, 25)

    # Word
    self.wordLabel = QLabel(self, text=word)
    self.wordLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    from MenuBar.settings import Settings
    font = QFont(Settings.font, 20)
    self.wordLabel.setFont(font)

    # Buttons
    self.buttonsWidget = QWidget()
    self.buttonsWidget.layout = QHBoxLayout(self.buttonsWidget)
    self.buttonsWidget.layout.setContentsMargins(0, 0, 0, 0)

    self.searchButton = QPushButton()
    # self.searchButton.setIcon(QIcon("Resources/reload.svg"))
    self.searchButton.setIcon(QIcon("Resources/search.png"))
    self.searchButton.clicked.connect(self.searchWord)
    self.searchButton.setFixedWidth(30)

    self.starButton = QPushButton()
    self.starButton.clicked.connect(self.notifyStarred)
    self.starButton.setFixedWidth(30)
    from Common.databaseHandler import DBHandler
    if DBHandler.starredWordExists(word):
      self.starButton.setIcon(QIcon("Resources/starred.svg"))
      self.isStarred = True
    else:
      self.starButton.setIcon(QIcon("Resources/unstarred.svg"))
      self.isStarred = False

    self.buttonsWidget.layout.addWidget(self.searchButton)
    self.buttonsWidget.layout.addWidget(self.starButton)

    dataWidget.layout.addWidget(self.wordLabel)
    dataWidget.layout.addWidget(self.buttonsWidget)

    self.layout.addWidget(dataWidget)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.resultStyle)

  def searchWord(self):
    from MainWidget.mainWidget import MainWidget
    from SideWidgets.recentSearchesWidget import RecentSearchesWidget
    from Common.databaseHandler import DBHandler
    word = self.wordLabel.text()

    MainWidget.addWord(word)

    recentSearchExists = DBHandler.addRecentSearch(word)
    if recentSearchExists:
      RecentSearchesWidget.removeAndAddRecentSearch(word)
    else:
      RecentSearchesWidget.addRecentSearch(word, False)

  def notifyStarred(self):
    from SideWidgets.starredWordsWidget import StarredWordsWidget
    from Common.databaseHandler import DBHandler
    word = self.wordLabel.text()

    if DBHandler.starredWordExists(word):
      DBHandler.removeStarredWord(word)
      StarredWordsWidget.toggleStarredBottom(word)
    else:
      DBHandler.addStarredWord(word)
      StarredWordsWidget.addStarredWord(word)

    self.toggleStarredIcon()

  def toggleStarredIcon(self):
    if self.isStarred:
      self.isStarred = False
      self.starButton.setIcon(QIcon("Resources/unstarred.svg"))
    else:
      self.isStarred = True
      self.starButton.setIcon(QIcon("Resources/starred.svg"))
