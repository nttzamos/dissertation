from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QIcon, QPalette

from databaseHandler import DBHandler

class RecentSearch(QWidget):
  def __init__(self, word, condition):
    super().__init__()

    self.setFixedHeight(50)

    self.setContentsMargins(0, 0, 0, 0)
    self.layout = QGridLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.setStyleSheet(
      "QPushButton:hover { background-color: grey }\n"
      "QPushButton { border-radius: 30px }\n"
      "QPushButton { border: 1px solid black }\n"
      "QPushButton { padding-bottom: 5px }\n"
      "QPushButton { padding-top: 5px }"
    )

    self.word = QLabel(word)
    font = QFont()
    font.setPointSize(14)
    self.word.setFont(font)

    self.reloadButton = QPushButton()
    self.reloadButton.setIcon(QIcon("Resources/reload.svg"))
    self.reloadButton.clicked.connect(self.reloadWord)
    self.reloadButton.setFixedWidth(30)

    self.starButton = QPushButton()
    self.starButton.clicked.connect(self.notifyStarred)
    self.starButton.setFixedWidth(30)
    
    self.isStarred = condition
    if condition:
      self.starButton.setIcon(QIcon("Resources/starred.svg"))
    else:
      self.starButton.setIcon(QIcon("Resources/unstarred.svg"))

    self.deleteButton = QPushButton()
    self.deleteButton.setIcon(QIcon("Resources/delete2.svg"))
    self.deleteButton.clicked.connect(self.removeWord)
    self.deleteButton.setFixedWidth(30)

    self.line = QFrame()
    self.line.setFrameShape(QFrame.Shape.HLine)
    self.line.setFrameShadow(QFrame.Shadow.Plain)
    self.line.setLineWidth(5)

    self.layout.addWidget(self.word, 0, 0)
    self.layout.addWidget(self.reloadButton, 0, 1)
    self.layout.addWidget(self.starButton, 0, 2)
    self.layout.addWidget(self.deleteButton, 0, 3)
    self.layout.addWidget(self.line, 1, 0, 1, 4)
    
  def reloadWord(self):
    from MainWidget.mainWidget import MainWidget
    MainWidget.addWord(self.word.text())

  def notifyStarred(self):
    from SideWidgets.starredWordsWidget import StarredWordsWidget
    word = self.word.text()
    addedNow = DBHandler.addStarredWord(0, word)
    if addedNow:
      StarredWordsWidget.addStarredWord(word)
    else:
      StarredWordsWidget.toggleStarredBottom(word)
      DBHandler.deleteStarredWord(word)

    self.toggleStarredIcon()

  def toggleStarredIcon(self):
    if self.isStarred:
      self.isStarred = False
      self.starButton.setIcon(QIcon("Resources/unstarred.svg"))
    else:
      self.isStarred = True
      self.starButton.setIcon(QIcon("Resources/starred.svg"))

  def removeWord(self):
    from SideWidgets.recentSearchesWidget import RecentSearchesWidget
    DBHandler.deleteRecentSearch(self.word.text())
    self.hide()
    RecentSearchesWidget.removeRecentSearch(self)
    self.deleteLater()
