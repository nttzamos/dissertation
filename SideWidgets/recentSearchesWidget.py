from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ItemWidgets.recentSearch import RecentSearch
from databaseHandler import DBHandler

class RecentSearchesWidget(QWidget):
  title = "Recent Searches"

  scrollAreaWidgetContents = QWidget()
  gridLayout = QGridLayout(scrollAreaWidgetContents)
  counter = 1000000
  widgetList = []
  placeholderLabel = QLabel("You do not have any " + title)
  placeholderLabelShow = False

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

    RecentSearchesWidget.placeholderLabel.setFont(font)
    self.type = type
    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)
    RecentSearchesWidget.gridLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.scrollArea.setWidget(RecentSearchesWidget.scrollAreaWidgetContents)
    self.layout.addWidget(self.scrollArea)
  
  def onClick(self, obj):
    print("It works again!")
    print(obj.label.text())
    RecentSearchesWidget.gridLayout.removeWidget(obj)

  def initialRecentSearchesAdding(self, wordsList, starredWordsList):
    for word in wordsList:
      if word in starredWordsList:
        condition=True
      else:
        condition=False
      widget = RecentSearch(word, condition, self)
      RecentSearchesWidget.widgetList.append(widget)
      RecentSearchesWidget.gridLayout.addWidget(widget, self.counter, 0)
      RecentSearchesWidget.counter -= 1

  @staticmethod
  def addRecentSearch(self, word, condition):
    if RecentSearchesWidget.placeholderLabelShow == True:
      RecentSearchesWidget.placeholderLabel.hide()
    condition = DBHandler.isStarredWord(word)
    widget = RecentSearch(word, condition, self)
    RecentSearchesWidget.widgetList.append(widget)
    RecentSearchesWidget.gridLayout.addWidget(widget, self.counter, 0)
    RecentSearchesWidget.counter -= 1

  def addWidget(self, word):
    if RecentSearchesWidget.placeholderLabelShow == True:
      RecentSearchesWidget.placeholderLabel.hide()
    widget = RecentSearch(word, True, self)
    RecentSearchesWidget.widgetList.append(widget)
    RecentSearchesWidget.gridLayout.addWidget(widget, self.counter, 0)
    RecentSearchesWidget.counter -= 1

  @staticmethod
  def removeAndAddWidget(self, word):
    for obj in self.widgetList:
      if obj.label.text()==word:
        RecentSearchesWidget.gridLayout.removeWidget(obj)
        RecentSearchesWidget.gridLayout.addWidget(obj, RecentSearchesWidget.counter, 0)
        RecentSearchesWidget.counter -=1
        return

  @staticmethod
  def toggleStarredUpper(word):
    for obj in RecentSearchesWidget.widgetList:
      if word==obj.label.text():
        obj.toggleStarredIcon()
        return

  @staticmethod
  def removeWidget(obj):
    RecentSearchesWidget.widgetList.remove(obj)
    if len(RecentSearchesWidget.widgetList)==0:
      RecentSearchesWidget.addPlaceholder()

  def addPlaceholder(self):
    RecentSearchesWidget.placeholderLabelShow = True
    RecentSearchesWidget.gridLayout.addWidget(RecentSearchesWidget.placeholderLabel)
    RecentSearchesWidget.placeholderLabel.show()
    