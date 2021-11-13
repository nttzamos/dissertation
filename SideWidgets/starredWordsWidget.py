from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ItemWidgets.starredWord import StarredWord
from databaseHandler import DBHandler

class StarredWordsWidget(QWidget):
  title = "Starred Words"
  placeholderLabelShow = False
  placeholderLabel = QLabel("You do not have any " + title)
  widgetList = []
  scrollAreaWidgetContents = QWidget()
  gridLayout = QGridLayout(scrollAreaWidgetContents)

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.title = QLabel(StarredWordsWidget.title)
    self.title.setStyleSheet("QLabel {border : 2px solid black}")
    self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont()
    font.setPointSize(14)
    self.title.setFont(font)
    self.title.setContentsMargins(25, 0, 25, 0)
    self.layout.addWidget(self.title)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.counter = 1000000
    StarredWordsWidget.placeholderLabel.setFont(font)

    self.type = type

    StarredWordsWidget.gridLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)

    self.scrollArea.setWidget(StarredWordsWidget.scrollAreaWidgetContents)
    self.layout.addWidget(self.scrollArea)
    
  def onClick(self, obj):
    print("It works again!")
    print(obj.label.text())
    StarredWordsWidget.gridLayout.removeWidget(obj)

  def initialStarredWordsAdding(self, starredWordsList):
    for word in starredWordsList:
      widget = StarredWord(word, self)
      StarredWordsWidget.widgetList.append(widget)
      StarredWordsWidget.gridLayout.addWidget(widget, DBHandler.getStarredWordPosition(word), 0)

  @staticmethod
  def addStarredWord(self, word):
    if StarredWordsWidget.placeholderLabelShow == True:
      StarredWordsWidget.placeholderLabel.hide()
      
    widget = StarredWord(word, self)
    StarredWordsWidget.widgetList.append(widget)
    length = len(StarredWordsWidget.widgetList)
    StarredWordsWidget.gridLayout.addWidget(StarredWordsWidget.widgetList[length-1], DBHandler.getStarredWordPosition(word), 0)

  def removeWidget(self, obj):
    StarredWordsWidget.widgetList.remove(obj)
    if len(StarredWordsWidget.widgetList)==0:
      self.addPlaceholder()

  def toggleStarredUpper(self, word):
    for obj in StarredWordsWidget.widgetList:
      if word==obj.label.text():
        obj.toggleStarredIcon()
        return

  @staticmethod
  def toggleStarredBottom(self, word):
    for obj in StarredWordsWidget.widgetList:
      if word==obj.label.text():
        obj.removeWord()
        return

  @staticmethod
  def notifyStarredBottom(self, obj):
    self.parent.toggleStarredBottom(obj)

  def notifyStarredUpper(self, obj):
    self.parent.toggleStarredUpper(obj)

  def addPlaceholder(self):
    StarredWordsWidget.placeholderLabelShow = True
    StarredWordsWidget.gridLayout.addWidget(StarredWordsWidget.placeholderLabel)
    StarredWordsWidget.placeholderLabel.show()
