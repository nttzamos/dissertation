from PyQt6.QtWidgets import QGridLayout, QLabel, QListWidget, QListWidgetItem, QScrollArea, QVBoxLayout, QWidget
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
  # gridLayout = QGridLayout(scrollAreaWidgetContents)
  listWidget = QListWidget(scrollAreaWidgetContents)
  listWidget.setStyleSheet("QListWidget::item:hover { background: transparent }")


  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.title_label = QLabel(StarredWordsWidget.title)
    self.title_label.setStyleSheet("QLabel {border : 2px solid black}")
    self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont()
    font.setPointSize(14)
    self.title_label.setFont(font)
    self.title_label.setContentsMargins(25, 0, 25, 0)
    self.layout.addWidget(self.title_label)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.counter = 1000000
    StarredWordsWidget.placeholderLabel.setFont(font)

    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)

    self.scrollArea.setWidget(StarredWordsWidget.scrollAreaWidgetContents)
    self.layout.addWidget(self.scrollArea)
    
  def onClick(self, obj):
    # StarredWordsWidget.gridLayout.removeWidget(obj)
    StarredWordsWidget.listWidget.removeItemWidget(obj)

  def initialStarredWordsAdding(self, starredWordsList):
    for word in starredWordsList:
      widget = StarredWord(word)
      StarredWordsWidget.widgetList.append(widget)
      # StarredWordsWidget.gridLayout.addWidget(widget, DBHandler.getStarredWordPosition(word), 0)
      item = QListWidgetItem()
      StarredWordsWidget.listWidget.addItem(item)
      StarredWordsWidget.listWidget.setItemWidget(item, widget)

  @staticmethod
  def addStarredWord(word):
    if StarredWordsWidget.placeholderLabelShow == True:
      StarredWordsWidget.placeholderLabel.hide()
      
    widget = StarredWord(word)
    StarredWordsWidget.widgetList.append(widget)
    position = DBHandler.getStarredWordPosition(word)
    print("Position is: " + str(position))
    # StarredWordsWidget.gridLayout.addWidget(StarredWordsWidget.widgetList[length-1], position, 0)
    item = QListWidgetItem()
    # StarredWordsWidget.listWidget.addItem(item)
    StarredWordsWidget.listWidget.insertItem(position, item)
    StarredWordsWidget.listWidget.setItemWidget(item, widget)

  @staticmethod
  def removeWidget(obj):
    StarredWordsWidget.widgetList.remove(obj)
    if len(StarredWordsWidget.widgetList)==0:
      StarredWordsWidget.addPlaceholder()

  @staticmethod
  def toggleStarredBottom(word):
    for obj in StarredWordsWidget.widgetList:
      if word==obj.word.text():
        obj.removeWord()
        return

  @staticmethod
  def addPlaceholder():
    StarredWordsWidget.placeholderLabelShow = True
    # StarredWordsWidget.gridLayout.addWidget(StarredWordsWidget.placeholderLabel)
    item = QListWidgetItem()
    StarredWordsWidget.listWidget.addItem(item)
    StarredWordsWidget.listWidget.setItemWidget(item, StarredWordsWidget.placeholderLabel)
    StarredWordsWidget.placeholderLabel.show()
