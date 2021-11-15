from PyQt6.QtWidgets import QSplitter, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt

from databaseHandler import DBHandler
from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from MainWidget.searchingWidget import SearchingWidget
from MainWidget.resultsWidget import ResultsWidget

class MainWidget(QWidget):
  searchingWidget = SearchingWidget()
  resultsWidget = ResultsWidget()

  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    # self.splitter = QSplitter(self)
    # self.splitter.setOrientation(Qt.Orientation.Vertical)
    # self.splitter.setChildrenCollapsible(False)
    # self.splitter.addWidget(MainWidget.searchingWidget)
    # self.splitter.addWidget(MainWidget.resultsWidget)

    self.layout.addWidget(MainWidget.searchingWidget)
    self.layout.addWidget(MainWidget.resultsWidget)
