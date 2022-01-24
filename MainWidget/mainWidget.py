from PyQt6.QtWidgets import QVBoxLayout, QWidget

from MainWidget.currentSearch import CurrentSearch
from MainWidget.searchingWidget import SearchingWidget
from MainWidget.resultsWidget import ResultsWidget
from MainWidget.result import Result
from MenuBar.settings import Settings

class MainWidget(QWidget):
  searchingWidget = SearchingWidget()
  currentSearch = CurrentSearch()
  resultsWidget = ResultsWidget()

  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.layout.addWidget(MainWidget.searchingWidget)
    self.layout.addWidget(MainWidget.currentSearch)
    self.layout.addWidget(MainWidget.resultsWidget)

    self.setMinimumWidth(Settings.getRightWidgetWidth())

  def findMinimumSize(self):
    longResult = Result("123456789012345678901234")
    return longResult.sizeHint().width()

  @staticmethod
  def addWord(word):
    if (word != MainWidget.currentSearch.getCurrentWord()):
      MainWidget.currentSearch.searchedWord.setText(word)
      ResultsWidget.showResults(word)