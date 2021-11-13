from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from Classes.ItemWidgets.starredWord import StarredWord
from Classes.databaseHandler import DBHandler

class StarredWordsWidget(QWidget):
  title = "Starred Words"

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


  def initialStarredWordsAdding(self, starredWordsList):
    for word in starredWordsList:
      widget = StarredWord(word, self)
      self.widgetList.append(widget)
      # self.database = DBHandler()
      # self.gridLayout.addWidget(widget, self.database.getStarredWordPosition(word), 0)
      self.gridLayout.addWidget(widget, DBHandler.getStarredWordPosition(word), 0)

  def addStarredWord(self, word):
    if self.placeholderLabelShow == True:
      self.placeholderLabel.hide()
      
    widget = StarredWord(word, self)
    self.widgetList.append(widget)
    length = len(self.widgetList)
    # self.database = DBHandler()
    self.gridLayout.addWidget(self.widgetList[length-1], DBHandler.getStarredWordPosition(word), 0)

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

  def toggleStarredUpper(self, word):
    for obj in self.widgetList:
      if word==obj.label.text():
        obj.toggleStarredIcon()
        return

  def toggleStarredBottom(self, word):
    for obj in self.widgetList:
      if word==obj.label.text():
        obj.removeWord()
        return

  def notifyStarredBottom(self, obj):
    self.parent.toggleStarredBottom(obj)

  def notifyStarredUpper(self, obj):
    self.parent.toggleStarredUpper(obj)

  def addPlaceholder(self):
    self.placeholderLabelShow = True
    self.gridLayout.addWidget(self.placeholderLabel)
    self.placeholderLabel.show()
