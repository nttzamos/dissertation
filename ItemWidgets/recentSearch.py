from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QIcon, QPalette

from databaseHandler import DBHandler

class RecentSearch(QWidget):
  def __init__(self, word, condition):
    super().__init__()

    self.setFixedHeight(50)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    self.dataWidget = QWidget()
    self.dataWidget.layout = QHBoxLayout(self.dataWidget)
    self.dataWidget.layout.setContentsMargins(0, 0, 0, 0)

    self.word = QLabel(word)
    from settings import Settings
    font = QFont(Settings.font, 14)
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

    self.dataWidget.layout.addSpacing(5)
    self.dataWidget.layout.addWidget(self.word)
    self.dataWidget.layout.addWidget(self.reloadButton)
    self.dataWidget.layout.addWidget(self.starButton)
    self.dataWidget.layout.addWidget(self.deleteButton)
    self.dataWidget.layout.addSpacing(5)
    
    self.layout.addWidget(self.dataWidget)
    self.layout.addWidget(self.line)

    self.style()
    
  def style(self):
    self.setStyleSheet(
      "QPushButton:hover { background-color: grey }\n"
      "QPushButton { border: 1px solid black }\n"
      "QPushButton { padding-bottom: 5px }\n"
      "QPushButton { padding-top: 5px }\n"
      "QLabel { color: white }\n"
      "QWidget { background-color: green }"
    )

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
