from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from MainWidget.currentSearch import CurrentSearch

from databaseHandler import DBHandler
from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from MainWidget.searchingWidget import SearchingWidget
from MainWidget.resultsWidget import ResultsWidget

class MainWidget(QWidget):
  searchingWidget = SearchingWidget()
  currentSearch = CurrentSearch()
  resultsWidget = ResultsWidget()

  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.searchContainerWidget = QWidget()
    self.widgetLayout = QHBoxLayout(self.searchContainerWidget)
    self.searchContainerWidget.layout = self.widgetLayout
    self.searchContainerWidget.layout.addSpacing(10)
    self.searchContainerWidget.layout.addWidget(MainWidget.searchingWidget)
    self.searchContainerWidget.layout.addSpacing(10)

    self.layout.addWidget(self.searchContainerWidget)
    self.layout.addWidget(MainWidget.currentSearch)
    self.layout.addWidget(MainWidget.resultsWidget)

  @staticmethod
  def addWord(word):
    if (word != MainWidget.currentSearch.getCurrentWord()):
      MainWidget.currentSearch.word.setText(word)
      ResultsWidget.showResults(word)