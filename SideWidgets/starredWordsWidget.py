from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ItemWidgets.starredWord import StarredWord
from databaseHandler import DBHandler
from settings import Settings

class StarredWordsWidget(QWidget):
  title = "Starred Words"

  scrollAreaWidgetContents = QWidget()
  gridLayout = QGridLayout(scrollAreaWidgetContents)
  gridLayout.setSpacing(0)
  gridLayout.setContentsMargins(0, 0, 0, 0)
  
  counter = 1000000
  widgetList = []
  
  placeholderLabel = QLabel("You do not have any " + title)
  showPlaceholderLabel = True

  vspacer = QLabel("f")

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.titleLabel = QLabel(StarredWordsWidget.title)
    self.titleLabel.setStyleSheet("QLabel {border : 1px solid black; padding: 10px 0px}")
    self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont(Settings.font, 18)
    self.titleLabel.setFont(font)
    self.layout.addWidget(self.titleLabel)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    StarredWordsWidget.placeholderLabel.setFont(font)
    StarredWordsWidget.placeholderLabel.setWordWrap(True)
    StarredWordsWidget.placeholderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    invisibleFont = QFont(Settings.font, 1)
    StarredWordsWidget.vspacer.setFont(invisibleFont)
    sizePolicy = StarredWordsWidget.vspacer.sizePolicy()
    sizePolicy.setRetainSizeWhenHidden(True)
    StarredWordsWidget.vspacer.setSizePolicy(sizePolicy)
    
    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setWidget(StarredWordsWidget.scrollAreaWidgetContents)
    self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.layout.addWidget(self.scrollArea)

    self.setMinimumWidth(Settings.leftWidgetWidth)
    
  def initialize(self, starredWordsList):
    if len(starredWordsList) == 0:
      StarredWordsWidget.showPlaceholder()
      return
    else:
      StarredWordsWidget.hidePlaceholder()

    for word in starredWordsList:
      widget = StarredWord(word)
      StarredWordsWidget.widgetList.append(widget)
      StarredWordsWidget.gridLayout.addWidget(widget, StarredWordsWidget.counter, 0)
      StarredWordsWidget.counter -= 1

  @staticmethod
  def addStarredWord(word):
    if StarredWordsWidget.showPlaceholderLabel == True:
      StarredWordsWidget.hidePlaceholder()
      
    widget = StarredWord(word)
    StarredWordsWidget.widgetList.append(widget)
    length = len(StarredWordsWidget.widgetList)
    StarredWordsWidget.gridLayout.addWidget(StarredWordsWidget.widgetList[length-1], StarredWordsWidget.counter, 0)
    StarredWordsWidget.counter -= 1

  @staticmethod
  def removeStarredWord(obj):
    StarredWordsWidget.widgetList.remove(obj)
    if len(StarredWordsWidget.widgetList)==0:
      StarredWordsWidget.showPlaceholder()

  @staticmethod
  def toggleStarredBottom(word):
    for obj in StarredWordsWidget.widgetList:
      if word==obj.word.text():
        obj.removeWord()
        return

  @staticmethod
  def showPlaceholder():
    StarredWordsWidget.showPlaceholderLabel = True
    StarredWordsWidget.gridLayout.addWidget(StarredWordsWidget.placeholderLabel)
    StarredWordsWidget.gridLayout.removeWidget(StarredWordsWidget.vspacer)
    StarredWordsWidget.placeholderLabel.show()

  @staticmethod
  def hidePlaceholder():
    StarredWordsWidget.showPlaceholderLabel = False
    StarredWordsWidget.gridLayout.addWidget(StarredWordsWidget.vspacer, 1000001, 0, 1, -1)
    StarredWordsWidget.placeholderLabel.hide()
