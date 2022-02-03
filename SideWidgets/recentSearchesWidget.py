from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ItemWidgets.recentSearch import RecentSearch
from MenuBar.settings import Settings
from Common.databaseHandler import DBHandler

class RecentSearchesWidget(QWidget):
  scrollAreaWidgetContents = QWidget()
  gridLayout = QGridLayout(scrollAreaWidgetContents)
  gridLayout.setSpacing(0)
  gridLayout.setContentsMargins(0, 0, 0, 0)

  counter = 1000000
  widgetList = []

  placeholderLabel = QLabel()
  showPlaceholderLabel = False

  vspacer = QLabel('f')

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.titleLabel = QLabel('Recent Searches')
    self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont(Settings.font, 18)
    self.titleLabel.setFont(font)
    self.layout.addWidget(self.titleLabel)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    RecentSearchesWidget.placeholderLabel.setFont(font)
    RecentSearchesWidget.placeholderLabel.setWordWrap(True)
    RecentSearchesWidget.placeholderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    invisibleFont = QFont(Settings.font, 1)
    RecentSearchesWidget.vspacer.setFont(invisibleFont)
    sizePolicy = RecentSearchesWidget.vspacer.sizePolicy()
    sizePolicy.setRetainSizeWhenHidden(True)
    RecentSearchesWidget.vspacer.setSizePolicy(sizePolicy)

    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setWidget(RecentSearchesWidget.scrollAreaWidgetContents)
    self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.layout.addWidget(self.scrollArea)

    self.setMinimumWidth(Settings.getLeftWidgetWidth())

    self.style()

  def style(self):
    from Common.styles import Styles
    self.titleLabel.setStyleSheet(Styles.sideWidgetsTitleLabelStyle)
    self.setStyleSheet(Styles.sideWidgetsStyle)

  @staticmethod
  def initialize():
    RecentSearchesWidget.gridLayout.addWidget(RecentSearchesWidget.vspacer, 1000001, 0, 1, -1)
    RecentSearchesWidget.showPlaceholder()

  @staticmethod
  def populate():
    RecentSearchesWidget.clearPreviousRecentSearches()

    recentSearches = DBHandler.getRecentSearches()
    starredWords = DBHandler.getStarredWords()

    if len(recentSearches) == 0:
      RecentSearchesWidget.showPlaceholder(text = 'You do not have any Recent Searches')
      return
    else:
      RecentSearchesWidget.hidePlaceholder()

    for word in recentSearches:
      widget = RecentSearch(word, word in starredWords)
      RecentSearchesWidget.widgetList.append(widget)
      RecentSearchesWidget.gridLayout.addWidget(widget, RecentSearchesWidget.counter, 0)
      RecentSearchesWidget.counter -= 1

  @staticmethod
  def addRecentSearch(word, condition):
    if RecentSearchesWidget.showPlaceholderLabel == True:
      RecentSearchesWidget.hidePlaceholder()

    condition = DBHandler.starredWordExists(word)
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
      RecentSearchesWidget.showPlaceholder(text = 'You do not have any Recent Searches')

  @staticmethod
  def clearPreviousRecentSearches():
    for recentSearch in RecentSearchesWidget.widgetList:
      recentSearch.hide()
      recentSearch.deleteLater()

    RecentSearchesWidget.widgetList = []
    RecentSearchesWidget.counter = 1000000
    RecentSearchesWidget.showPlaceholder()

  @staticmethod
  def showPlaceholder(text = 'Please select a subject first.'):
    RecentSearchesWidget.placeholderLabel.setText(text)
    if not RecentSearchesWidget.showPlaceholderLabel:
      RecentSearchesWidget.showPlaceholderLabel = True
      RecentSearchesWidget.gridLayout.addWidget(RecentSearchesWidget.placeholderLabel)
      RecentSearchesWidget.gridLayout.removeWidget(RecentSearchesWidget.vspacer)
      RecentSearchesWidget.placeholderLabel.show()

  @staticmethod
  def hidePlaceholder():
    if RecentSearchesWidget.showPlaceholderLabel:
      RecentSearchesWidget.showPlaceholderLabel = False
      RecentSearchesWidget.gridLayout.addWidget(RecentSearchesWidget.vspacer, 1000001, 0, 1, -1)
      RecentSearchesWidget.placeholderLabel.hide()
