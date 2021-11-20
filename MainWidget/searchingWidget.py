from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QCompleter, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt

from databaseHandler import DBHandler
from SideWidgets.recentSearchesWidget import RecentSearchesWidget

class SearchingWidget(QWidget):
  # Uncomment and change when complete
  # dictionary_words = DBHandler.getAllWords()
  dictionary_words = [
    "Balcony", "Balloon", "Barcelona", "Balcony Light",
    "Fan", "Room Light", "Brioche", "Basketball",
    "Bedroom Heater", "Wall Switch"]
  
  def __init__(self):
    super().__init__()

    self.lineEdit = QLineEdit()
    large_font = QFont()
    large_font.setPointSize(14)
    self.lineEdit.setFont(large_font)

    # Search bar.
    self.lineEdit.returnPressed.connect(self.searchWithEnter)

    # Adding Completer.
    self.completer = QCompleter(SearchingWidget.dictionary_words)
    self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    self.completer.activated.connect(self.searchWithClick)
    smallFont = QFont()
    smallFont.setPointSize(10)
    self.completer.popup().setFont(smallFont)
    self.lineEdit.setCompleter(self.completer)
    self.lineEdit.setPlaceholderText("Please enter a word.")

    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.searchBarWidget = QWidget()
    self.searchBarWidget.layout = QHBoxLayout(self.searchBarWidget)
    self.searchBarWidget.layout.setContentsMargins(10, 0, 0, 0)
    self.searchBarWidget.setStyleSheet(
      "QWidget { background-color: white; border-radius: 10px; }\n"
      "QPushButton { border: none }\n"
      "QPushButton { padding-bottom: 5 }\n"
      "QPushButton { padding-top: 5 }"
    )

    self.searchButton = QPushButton()
    self.searchButton.setIcon(QIcon("Resources/settings.png"))
    self.searchButton.setFixedWidth(30)
    self.searchButton.clicked.connect(self.searchWithButton)
    
    self.clearSearchButton = QPushButton()
    self.clearSearchButton.setIcon(QIcon("Resources/restoreDownWindow.png"))
    self.clearSearchButton.setFixedWidth(30)
    self.clearSearchButton.clicked.connect(self.clearSearch)

    self.searchBarWidget.layout.setSpacing(0)
    self.searchBarWidget.layout.addWidget(self.lineEdit)
    self.searchBarWidget.layout.addWidget(self.searchButton)
    self.searchBarWidget.layout.addWidget(self.clearSearchButton)
    
    self.layout.addSpacing(20)
    self.layout.addWidget(self.searchBarWidget)
    self.layout.addSpacing(20)

  def searchWithEnter(self):
    if self.lineEdit.text() in SearchingWidget.dictionary_words:
      self.addRecentSearch(self.lineEdit.text())
      self.lineEdit.clear()
    else:
      # Implement showing necessary message
      pass

  def searchWithClick(self, text):
    self.addRecentSearch(text)
    QTimer.singleShot(0, self.clear)

  def searchWithButton(self):
    pass

  def clearSearch(self):
    pass

  def addRecentSearch(self, word):
    from MainWidget.mainWidget import MainWidget
    MainWidget.addWord(word)

    addedNow = DBHandler.addRecentSearch(word, 0)
    if addedNow:
      RecentSearchesWidget.addRecentSearch(word, False)
    else:
      RecentSearchesWidget.removeAndAddRecentSearch(word)
