from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

from databaseHandler import DBHandler

class RecentSearch(QWidget):
  def __init__(self, word, condition):
    super().__init__()

    self.setMinimumSize(QSize(200, 100))
    self.layout = QHBoxLayout(self)

    self.word = QLabel(word)
    self.reloadButton = QPushButton()
    self.reloadButton.setIcon(QIcon("Resources/reload.svg"))
    self.reloadButton.clicked.connect(self.reloadWord)

    self.starButton = QPushButton()
    self.starButton.clicked.connect(self.notifyStarred)
    self.isStarred = condition
    if condition:
      self.starButton.setIcon(QIcon("Resources/starred.svg"))
    else:
      self.starButton.setIcon(QIcon("Resources/unstarred.svg"))

    self.deleteButton = QPushButton()
    self.deleteButton.setIcon(QIcon("Resources/delete2.svg"))
    self.deleteButton.clicked.connect(self.removeWord)

    self.layout.addWidget(self.word)
    self.layout.addWidget(self.reloadButton)
    self.layout.addWidget(self.starButton)
    self.layout.addWidget(self.deleteButton)
    
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
    RecentSearchesWidget.removeWidget(self)
    self.deleteLater()
