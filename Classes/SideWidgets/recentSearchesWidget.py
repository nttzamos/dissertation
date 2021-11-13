from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from Classes.ItemWidgets.recentSearch import RecentSearch
from Classes.databaseHandler import DBHandler

class RecentSearchesWidget(QWidget):
  title = "Recent Searches"
  
  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.title = QLabel(RecentSearchesWidget.title)
    self.title.setStyleSheet("QLabel {border : 2px solid black}")
    self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont()
    font.setPointSize(14)
    self.title.setFont(font)
    self.title.setContentsMargins(25, 0, 25, 0)
    self.layout.addWidget(self.title)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.counter = 1000000
    self.placeholderLabel = QLabel("You do not have any " + self.title)
    self.placeholderLabelShow = False
    self.placeholderLabel.setFont(font)

    self.type = type
    self.widgetList = []

    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)

    self.scrollAreaWidgetContents = QWidget()
    self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
    self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.scrollArea.setWidget(self.scrollAreaWidgetContents)
    self.layout.addWidget(self.scrollArea)
  
  def onClick(self, obj):
    print("It works again!")
    print(obj.label.text())
    self.gridLayout.removeWidget(obj)

  def initialRecentSearchesAdding(self, wordsList, starredWordsList):
    for word in wordsList:
      if word in starredWordsList:
        condition=True
      else:
        condition=False
      widget = RecentSearch(word, condition, self)
      self.widgetList.append(widget)
      self.gridLayout.addWidget(widget, self.counter, 0)
      self.counter -= 1

  def addRecentSearch(self, word, condition):
    if self.placeholderLabelShow == True:
      self.placeholderLabel.hide()
    # self.database = DBHandler()
    condition = DBHandler.isStarredWord(word)
    # condition = self.database.isStarredWord(word)
    widget = RecentSearch(word, condition, self)
    self.widgetList.append(widget)
    self.gridLayout.addWidget(widget, self.counter, 0)
    self.counter -= 1
    # length = len(self.widgetList)
    # self.gridLayout.addWidget(self.widgetList[length-1])

  def addWidget(self, word):
    if self.placeholderLabelShow == True:
      self.placeholderLabel.hide()
    widget = RecentSearch(word, True, self)
    self.widgetList.append(widget)
    self.gridLayout.addWidget(widget, self.counter, 0)
    self.counter -= 1
    # length = len(self.widgetList)
    # self.gridLayout.addWidget(self.widgetList[length-1])

  def removeAndAddWidget(self, word):
    for obj in self.widgetList:
      if obj.label.text()==word:
        self.gridLayout.removeWidget(obj)
        self.gridLayout.addWidget(obj, self.counter, 0)
        self.counter -=1
        return

  def removeWidget(self, obj):
    self.widgetList.remove(obj)
    if len(self.widgetList)==0:
      self.addPlaceholder()

  def addPlaceholder(self):
    self.placeholderLabelShow = True
    self.gridLayout.addWidget(self.placeholderLabel)
    self.placeholderLabel.show()

  def reloadWord(self, word):
    self.parent.reloadWord(word)
    