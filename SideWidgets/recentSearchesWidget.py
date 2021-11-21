from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ItemWidgets.recentSearch import RecentSearch
from databaseHandler import DBHandler

class RecentSearchesWidget(QWidget):
  title = "Recent Searches"

  scrollAreaWidgetContents = QWidget()
  gridLayout = QGridLayout(scrollAreaWidgetContents)
  gridLayout.setSpacing(0)
  counter = 1000000
  widgetList = []
  placeholderLabel = QLabel("You do not have any " + title)
  placeholderLabelShow = False

  def __init__(self):
    super().__init__()

    # self.setStyleSheet(
    #   "QScrollBar { border: none; background: rgb(45, 45, 68); width: 14px; margin: 15px 0 15px 0; border-radius: 0px; }\n"
    #   "QScrollBar::handle:vertical { background-color: rgb(80, 80, 122); min-height: 30px; border-radius: 7px; }\n"
    #   "QScrollBar::handle:vertical:hover{ background-color: rgb(255, 0, 127); }\n"
    #   "QScrollBar::handle:vertical:pressed { background-color: rgb(185, 0, 92); }\n"
    #   # "QScrollBar::sub-line:vertical { border: none; background-color: rgb(59, 59, 90); height: 15px; border-top-left-radius: 7px; border-top-right-radius: 7px; subcontrol-position: top; subcontrol-origin: margin; }\n"
    #   # "QScrollBar::sub-line:vertical:hover { background-color: rgb(255, 0, 127); }\n"
    #   # "QScrollBar::sub-line:vertical:pressed { background-color: rgb(185, 0, 92); }\n"
    #   # "QScrollBar::add-line:vertical { border: none; background-color: rgb(59, 59, 90); height: 15px; border-bottom-left-radius: 7px; border-bottom-right-radius: 7px; subcontrol-position: bottom; subcontrol-origin: margin; }\n"
    #   # "QScrollBar::add-line:vertical:hover { background-color: rgb(255, 0, 127); }\n"
    #   # "QScrollBar::add-line:vertical:pressed { background-color: rgb(185, 0, 92); }\n"
    #   "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { background: none; }\n"
    #   "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }\n"
    # )

    self.layout = QVBoxLayout(self)
    self.title_label = QLabel(RecentSearchesWidget.title)
    self.title_label.setStyleSheet("QLabel {border : 2px solid black}")
    self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont()
    font.setPointSize(14)
    self.title_label.setFont(font)
    self.layout.addWidget(self.title_label)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    RecentSearchesWidget.placeholderLabel.setFont(font)
    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setWidget(RecentSearchesWidget.scrollAreaWidgetContents)
    self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
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
        RecentSearchesWidget.gridLayout.removeWidget(obj)
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
    