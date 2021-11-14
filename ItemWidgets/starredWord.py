from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

from databaseHandler import DBHandler

class StarredWord(QWidget):
  def __init__(self, word):
    super().__init__()

    self.setMinimumSize(QSize(200, 100))
    self.layout = QHBoxLayout(self)
    self.word = QLabel(word)
    self.starButton = QPushButton()
    self.starButton.setIcon(QIcon("Resources/starred.svg"))
    self.starButton.clicked.connect(self.toggleStarred)

    self.layout.addWidget(self.word)
    self.layout.addWidget(self.starButton)
    
  def toggleStarred(self):
    from SideWidgets.recentSearchesWidget import RecentSearchesWidget
    word = self.word.text()
    DBHandler.deleteStarredWord(word)
    RecentSearchesWidget.toggleStarredUpper(word)
    self.removeWord()

  def removeWord(self):
    from SideWidgets.starredWordsWidget import StarredWordsWidget
    self.hide()
    StarredWordsWidget.removeWidget(self)
    self.deleteLater()