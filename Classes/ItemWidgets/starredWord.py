from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

from Classes.databaseHandler import DBHandler

class StarredWord(QWidget):
  def __init__(self, word):
    super().__init__()

    self.setMinimumSize(QSize(200, 100))
    self.layout = QHBoxLayout(self)
    self.label = QLabel(word)
    self.button = QPushButton()
    self.button.setIcon(QIcon("Resources/starred.svg"))
    self.button.clicked.connect(self.toggleStarred)

    self.layout.addWidget(self.label)
    self.layout.addWidget(self.button)
    
  def toggleStarred(self):
    from SideWidgets.recentSearchesWidget import RecentSearchesWidget
    word = self.label.text()
    DBHandler.deleteStarredWord(word)
    RecentSearchesWidget.toggleStarredUpper(word)
    self.removeWord()

  def removeWord(self):
    self.hide()
    self.parent.removeWidget(self)
    self.deleteLater()