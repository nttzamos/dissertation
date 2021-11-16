from PyQt6.QtWidgets import QCompleter, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt

from databaseHandler import DBHandler
from SideWidgets.recentSearchesWidget import RecentSearchesWidget

class SearchingWidget(QLineEdit):
  # Uncomment and change when complete
  # dictionary_words = DBHandler.getAllWords()
  dictionary_words = [
    "Balcony", "Balloon", "Barcelona", "Balcony Light",
    "Fan", "Room Light", "Brioche", "Basketball",
    "Bedroom Heater", "Wall Switch"]
  
  def __init__(self):
    super().__init__()

    # Search bar.
    # self.searchbar.textChanged.connect(self.update_display)
    self.returnPressed.connect(self.searchWithEnter)

    # Adding Completer.
    self.completer = QCompleter(SearchingWidget.dictionary_words)
    self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    self.completer.activated.connect(self.searchWithClick)
    self.setCompleter(self.completer)
    self.setPlaceholderText("Please enter a word.")

  def searchWithEnter(self):
    if self.text() in SearchingWidget.dictionary_words:
      self.addRecentSearch(self.text())
      self.clear()
    else:
      # Implement showing necessary message
      pass

  def searchWithClick(self, text):
    self.addRecentSearch(text)
    QTimer.singleShot(0, self.clear)

  def addRecentSearch(self, word):
    from MainWidget.mainWidget import MainWidget
    MainWidget.addWord(word)

    addedNow = DBHandler.addRecentSearch(word, 0)
    if addedNow:
      RecentSearchesWidget.addRecentSearch(word, False)
    else:
      RecentSearchesWidget.removeAndAddRecentSearch(word)
