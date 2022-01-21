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
  showPlaceholderLabel = True
  placeholderLabel = QLabel("The results of your search will be displayed here.")
  gridColumns = Settings.getResultsWidgetColumns()

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
    from styles import Styles
    self.setStyleSheet(Styles.resultsWidgetStyle)

  @staticmethod
  def showResults(word):
    ResultsWidget.hidePlaceholder()
    ResultsWidget.clearPreviousResults()
    resultsWords = ResultsWidget.getResults(word)

    for i in range(len(resultsWords)):
      row = i // ResultsWidget.gridColumns
      column = i % ResultsWidget.gridColumns
      result = Result(resultsWords[i])
      ResultsWidget.widgetList.append(result)
      ResultsWidget.gridLayout.addWidget(result, row, column)

  @staticmethod
  def getResults(word):
    resultsWords = []
    for i in range(15):
      resultsWords.append(word + str(i))

    return resultsWords

  @staticmethod
  def clearPreviousResults():
    for result in ResultsWidget.widgetList:
      result.hide()
      result.deleteLater()
    ResultsWidget.widgetList = []

  @staticmethod
  def showPlaceholder():
    ResultsWidget.clearPreviousResults()
    if not ResultsWidget.showPlaceholderLabel:
      ResultsWidget.showPlaceholderLabel = True
      ResultsWidget.placeholderLabel.show()

  @staticmethod
  def hidePlaceholder():
    if ResultsWidget.showPlaceholderLabel:
      ResultsWidget.showPlaceholderLabel = False
      ResultsWidget.placeholderLabel.hide()
