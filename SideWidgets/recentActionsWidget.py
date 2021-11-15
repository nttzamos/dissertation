from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ItemWidgets.recentAction import RecentAction

class RecentActionsWidget(QWidget):
  title = "Recent Actions"
  
  def __init__(self):
    super().__init__()
    
    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.title_label = QLabel(RecentActionsWidget.title)
    self.title_label.setStyleSheet("QLabel {border : 2px solid black}")
    self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont()
    font.setPointSize(14)
    self.title_label.setFont(font)
    self.title_label.setContentsMargins(25, 0, 25, 0)
    self.layout.addWidget(self.title_label)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.counter = 1000000
    self.placeholderLabel = QLabel("You do not have any " + RecentActionsWidget.title)
    self.placeholderLabelShow = False
    self.placeholderLabel.setFont(font)

    self.widgetList = []

    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)

    self.scrollAreaWidgetContents = QWidget()
    self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
    self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.scrollArea.setWidget(self.scrollAreaWidgetContents)
    self.layout.addWidget(self.scrollArea)

  def addRecentAction(self, word):
    if self.placeholderLabelShow == True:
      self.placeholderLabel.hide()
    
    widget = RecentAction(word)
    self.widgetList.append(widget)
    length = len(self.widgetList)
    self.gridLayout.addWidget(self.widgetList[length-1])

  def removeRecentAction(self, obj):
    self.widgetList.remove(obj)
    if len(self.widgetList)==0:
      self.addPlaceholder()

  def addPlaceholder(self):
    self.placeholderLabelShow = True
    self.gridLayout.addWidget(self.placeholderLabel)
    self.placeholderLabel.show()
