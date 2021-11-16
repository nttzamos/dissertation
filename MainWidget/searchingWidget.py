from PyQt6.QtWidgets import QCompleter, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt

from databaseHandler import DBHandler
from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from MainWidget.currentSearch import CurrentSearch
from MainWidget.resultsWidget import ResultsWidget

class SearchingWidget(QWidget):
  currentSearch = CurrentSearch()
  # Uncomment and change when complete
  # dictionary_words = DBHandler.getAllWords()
  dictionary_words = [
    "Balcony", "Balloon", "Barcelona", "Balcony Light",
    "Fan", "Room Light", "Brioche", "Basketball",
    "Bedroom Heater", "Wall Switch"]
  
  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    # Search bar.
    self.searchbar = QLineEdit()
    self.searchbar.setContentsMargins(0, 0, 0, 0)
    # self.searchbar.textChanged.connect(self.update_display)
    self.searchbar.returnPressed.connect(self.searchWithEnter)

    # Adding Completer.
    self.completer = QCompleter(SearchingWidget.dictionary_words)
    self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    self.completer.activated.connect(self.searchWithClick)
    self.searchbar.setCompleter(self.completer)
    self.searchbar.setPlaceholderText("Please enter a word.")

    self.layout.addWidget(self.searchbar)
    self.layout.addWidget(SearchingWidget.currentSearch)

  def searchWithEnter(self):
    if self.searchbar.text() in SearchingWidget.dictionary_words:
      self.addRecentSearch(self.searchbar.text())
      self.searchbar.clear()
    else:
      # Implement showing necessary message
      pass

  def searchWithClick(self, text):
    self.addRecentSearch(text)
    QTimer.singleShot(0, self.searchbar.clear)

  def addRecentSearch(self, word):
    SearchingWidget.addWord(word)

    addedNow = DBHandler.addRecentSearch(word, 0)
    if addedNow:
      RecentSearchesWidget.addRecentSearch(word, False)
    else:
      RecentSearchesWidget.removeAndAddRecentSearch(word)

  @staticmethod
  def addWord(word):
    SearchingWidget.currentSearch.word.setText(word)
    ResultsWidget.showResults(word)