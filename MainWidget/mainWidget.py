from PyQt6.QtWidgets import QCompleter, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt

from databaseHandler import DBHandler
from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from MainWidget.searchingWidget import SearchingWidget
from MainWidget.resultsWidget import ResultsWidget

class MainWidget(QWidget):
  middleMiddleWidget = SearchingWidget()
  
  def __init__(self):
    super().__init__()
    self.setFixedWidth(1200)
    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    widget_names = DBHandler.getAllWords()

    # Search bar.
    self.searchbar = QLineEdit()
    self.searchbar.setContentsMargins(0, 0, 0, 0)
    # self.searchbar.textChanged.connect(self.update_display)
    self.searchbar.returnPressed.connect(self.updateSearches)

    # Adding Completer.
    self.completer = QCompleter(widget_names)
    self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    self.completer.activated.connect(self.updateSearches1)
    self.searchbar.setCompleter(self.completer)

    self.searchbar.setPlaceholderText("Please enter a word.")
    self.layout.addWidget(self.searchbar)

    self.layout.addWidget(MainWidget.middleMiddleWidget)

    self.middleBottomWidget = ResultsWidget()
    self.layout.addWidget(self.middleBottomWidget)

  def updateSearches(self):
    self.addRecentSearch(self.searchbar.text())
    self.searchbar.clear()

  def updateSearches1(self):
    QTimer.singleShot(0, self.searchbar.clear)

  def addRecentSearch(self, word):
    MainWidget.addWord(word)

    addedNow = DBHandler.addRecentSearch(word, 0)
    if addedNow:
      RecentSearchesWidget.addRecentSearch(word, False)
    else:
      RecentSearchesWidget.removeAndAddWidget(word)

  @staticmethod
  def addWord(word):
    MainWidget.middleMiddleWidget.word.setText(word)
