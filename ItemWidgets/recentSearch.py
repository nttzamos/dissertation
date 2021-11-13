from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

from databaseHandler import DBHandler

class RecentSearch(QWidget):
  def __init__(self, word, condition):
    super().__init__()

    self.setMinimumSize(QSize(200, 100))
    self.layout = QHBoxLayout(self)

    self.label = QLabel(word)
    self.button1 = QPushButton()
    self.button1.setIcon(QIcon("Resources/reload.svg"))
    self.button1.clicked.connect(self.reloadWord)

    self.button2 = QPushButton()
    self.button2.clicked.connect(self.notifyStarred)
    self.starredCondition = condition
    if condition:
      self.button2.setIcon(QIcon("Resources/starred.svg"))
    else:
      self.button2.setIcon(QIcon("Resources/unstarred.svg"))

    self.button3 = QPushButton()
    self.button3.setIcon(QIcon("Resources/delete2.svg"))
    self.button3.clicked.connect(self.removeWord)

    self.layout.addWidget(self.label)
    self.layout.addWidget(self.button1)
    self.layout.addWidget(self.button2)
    self.layout.addWidget(self.button3)
    
  def reloadWord(self):
    # from mainWindow import MainWindow
    # MainWindow.reloadWord(self.label.text())
    from MainWidget.mainWidget import MainWidget
    MainWidget.addWord(self.label.text())

  def notifyStarred(self):
    from SideWidgets.starredWordsWidget import StarredWordsWidget
    word = self.label.text
    addedNow = DBHandler.addStarredWord(0, word)
    if addedNow:
      StarredWordsWidget.addStarredWord(word)
    else:
      StarredWordsWidget.toggleStarredBottom(word)
      DBHandler.deleteStarredWord(word)

    StarredWordsWidget.notifyStarredBottom(self)
    self.toggleStarredIcon()

  def toggleStarredIcon(self):
    if self.starredCondition:
      self.starredCondition = False
      self.button2.setIcon(QIcon("Resources/unstarred.svg"))
    else:
      self.starredCondition = True
      self.button2.setIcon(QIcon("Resources/starred.svg"))

  def removeWord(self):
    from SideWidgets.recentSearchesWidget import RecentSearchesWidget
    DBHandler.deleteRecentSearch(self.label.text())
    self.hide()
    RecentSearchesWidget.removeWidget(self)
    self.deleteLater()
