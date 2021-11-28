from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout, QWidget
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

    self.layout.addWidget(MainWidget.searchingWidget)
    self.layout.addWidget(MainWidget.currentSearch)
    self.layout.addWidget(MainWidget.resultsWidget)
    self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

  @staticmethod
  def addWord(word):
    if (word != MainWidget.currentSearch.getCurrentWord()):
      MainWidget.currentSearch.searchedWord.setText(word)
      ResultsWidget.showResults(word)