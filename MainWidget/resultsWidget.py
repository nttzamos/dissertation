from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QScrollArea, QVBoxLayout, QWidget

from MainWidget.result import Result

class ResultsWidget(QWidget):
  scrollAreaWidgetContents = QWidget()
  # self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(1200, 700))
  # self.gridLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
  gridLayout = QGridLayout(scrollAreaWidgetContents)
  widgetList = []
  counter = 1000000

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)

    self.layout.setContentsMargins(0, 0, 0, 0)

    ResultsWidget.gridLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)

    self.scrollArea.setWidget(ResultsWidget.scrollAreaWidgetContents)
    self.layout.addWidget(self.scrollArea)

  @staticmethod
  def showResults(word):
    resultsWords = []
    for obj in ResultsWidget.widgetList:
      ResultsWidget.widgetList.remove(obj)  
    ResultsWidget.widgetList = []
    print(ResultsWidget.widgetList)
    for i in range(15):
      resultsWords.append(word + str(i))
    
    for i in range(len(resultsWords)):
      print(resultsWords[i])
      row = i // 3
      column = i % 3
      result = Result(resultsWords[i])
      ResultsWidget.widgetList.append(result)
      ResultsWidget.gridLayout.addWidget(result, row, column)
    
