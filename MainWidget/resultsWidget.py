from typing import Set
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from MainWidget.result import Result
from settings import Settings

class ResultsWidget(QWidget):
  scrollAreaWidgetContents = QWidget()
  gridLayout = QGridLayout(scrollAreaWidgetContents)
  widgetList = []
  counter = 1000000
  placeholderLabelShow = True
  placeholderLabel = QLabel("The results of your search will be displayed here.")
  gridColumns = Settings.resultsWidgetColumns

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    font = QFont(Settings.font, 14)
    ResultsWidget.placeholderLabel.setFont(font)
    ResultsWidget.gridLayout.addWidget(ResultsWidget.placeholderLabel)

    ResultsWidget.gridLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setWidget(ResultsWidget.scrollAreaWidgetContents)
    self.layout.addWidget(self.scrollArea)

    self.style()
    
  def style(self):
    self.setStyleSheet(
      "QWidget { background-color: blue }\n"
      "QScrollBar { background-color: none }"
    )

  @staticmethod
  def showResults(word):
    if ResultsWidget.placeholderLabelShow:
      ResultsWidget.placeholderLabel.hide()
    resultsWords = []
    for obj in ResultsWidget.widgetList:
      obj.hide()
      obj.deleteLater()
    ResultsWidget.widgetList = []
    for i in range(15):
      resultsWords.append(word + str(i))
    
    for i in range(len(resultsWords)):
      row = i // ResultsWidget.gridColumns
      column = i % ResultsWidget.gridColumns
      result = Result(resultsWords[i])
      ResultsWidget.widgetList.append(result)
      ResultsWidget.gridLayout.addWidget(result, row, column)
    
