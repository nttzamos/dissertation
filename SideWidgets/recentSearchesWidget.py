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
    self.title_label = QLabel(RecentSearchesWidget.title)
    self.title_label.setStyleSheet("QLabel {border : 2px solid black}")
    self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont()
    font.setPointSize(14)
    self.title_label.setFont(font)
    self.title_label.setContentsMargins(25, 0, 25, 0)
    self.layout.addWidget(self.title_label)
    self.layout.setContentsMargins(0, 0, 0, 0)

    RecentSearchesWidget.placeholderLabel.setFont(font)
    self.type = type
    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)
    RecentSearchesWidget.gridLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.scrollArea.setWidget(RecentSearchesWidget.scrollAreaWidgetContents)
    self.layout.addWidget(self.scrollArea)
  
  def initialize(self, wordsList, starredWordsList):
    for word in wordsList:
      if word in starredWordsList:
        condition=True
      else:
        condition=False
      widget = RecentSearch(word, condition)
      RecentSearchesWidget.widgetList.append(widget)
      RecentSearchesWidget.gridLayout.addWidget(widget, self.counter, 0)
      RecentSearchesWidget.counter -= 1

  @staticmethod
  def addRecentSearch(word, condition):
    if RecentSearchesWidget.placeholderLabelShow == True:
      RecentSearchesWidget.placeholderLabel.hide()
    condition = DBHandler.isStarredWord(word)
    widget = RecentSearch(word, condition)
    RecentSearchesWidget.widgetList.append(widget)
    RecentSearchesWidget.gridLayout.addWidget(widget, RecentSearchesWidget.counter, 0)
    RecentSearchesWidget.counter -= 1

  @staticmethod
  def removeAndAddRecentSearch(word):
    for obj in RecentSearchesWidget.widgetList:
      if obj.word.text()==word:
        RecentSearchesWidget.gridLayout.removeRecentSearch(obj)
        RecentSearchesWidget.gridLayout.addWidget(obj, RecentSearchesWidget.counter, 0)
        RecentSearchesWidget.counter -=1
        return

  @staticmethod
  def toggleStarredUpper(word):
    for obj in RecentSearchesWidget.widgetList:
      if word==obj.word.text():
        obj.toggleStarredIcon()
        return

  @staticmethod
  def removeRecentSearch(obj):
    RecentSearchesWidget.widgetList.remove(obj)
    if len(RecentSearchesWidget.widgetList)==0:
      RecentSearchesWidget.addPlaceholder()

  @staticmethod
  def addPlaceholder():
    RecentSearchesWidget.placeholderLabelShow = True
    RecentSearchesWidget.gridLayout.addWidget(RecentSearchesWidget.placeholderLabel)
    RecentSearchesWidget.placeholderLabel.show()
    