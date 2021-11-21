from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QCompleter, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QEvent, QTimer, Qt

from databaseHandler import DBHandler
from SideWidgets.recentSearchesWidget import RecentSearchesWidget

class SearchingWidget(QWidget):
  # Uncomment and change when complete
  # dictionary_words = DBHandler.getAllWords()
  dictionary_words = [
    "Balcony", "Balloon", "Barcelona", "Balcony Light",
    "Fan", "Room Light", "Brioche", "Basketball",
    "Bedroom Heater", "Wall Switch"]

  lineEdit = QLineEdit()
  
  def __init__(self):
    super().__init__()


    large_font = QFont()
    large_font.setPointSize(14)
    SearchingWidget.lineEdit.setFont(large_font)    
    SearchingWidget.lineEdit.setContentsMargins(0, 1, 0, 1)
    SearchingWidget.lineEdit.returnPressed.connect(self.searchWithEnter)
    SearchingWidget.lineEdit.textChanged.connect(self.searchTextChanged)
    self.showErrorMessage = False

    self.completer = QCompleter(SearchingWidget.dictionary_words)
    self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    self.completer.activated.connect(self.searchWithClick)
    smallFont = QFont()
    smallFont.setPointSize(10)
    self.completer.popup().setFont(smallFont)
    SearchingWidget.lineEdit.setCompleter(self.completer)
    SearchingWidget.lineEdit.setPlaceholderText("Please enter a word.")

    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.searchBarWidget = QWidget()
    self.searchBarWidget.layout = QHBoxLayout(self.searchBarWidget)
    self.searchBarWidget.layout.setContentsMargins(10, 0, 0, 0)

    
    self.clearSearchButton = QPushButton()
    self.clearSearchButton.setIcon(QIcon("Resources/restoreDownWindow.png"))
    self.clearSearchButton.setFixedWidth(30)
    self.clearSearchButton.clicked.connect(self.clearSearch)
    self.hideClearSearchButton = True
    self.clearSearchButton.hide()

    self.searchButton = QPushButton()
    self.searchButton.setIcon(QIcon("Resources/settings.png"))
    self.searchButton.setFixedWidth(30)
    self.searchButton.clicked.connect(self.searchWithEnter)

    self.searchBarWidget.layout.setSpacing(0)
    self.searchBarWidget.layout.addWidget(self.lineEdit)
    self.searchBarWidget.layout.addWidget(self.clearSearchButton)
    self.searchBarWidget.layout.addWidget(self.searchButton)
    self.searchBarWidget.layout.addSpacing(5)
    
    self.layout.addSpacing(20)
    self.layout.addWidget(self.searchBarWidget)
    self.layout.addSpacing(20)

    self.setFocusedStyleSheet()

  def setFocusedStyleSheet(self):
    self.setStyleSheet(
      "QWidget { background-color: white; border-radius: 10px; border: 1px solid blue }\n"
      "QLineEdit { border: none }"
      "QPushButton { border: none }\n"
      "QPushButton { padding-bottom: 5 }\n"
      "QPushButton { padding-top: 5 }"
    )

  def setUnfocusedStyleSheet(self):
    self.setStyleSheet(
      "QWidget { background-color: white; border-radius: 10px; border: none }\n"
      "QLineEdit { border: none }"
      "QPushButton { border: none }\n"
      "QPushButton { padding-bottom: 5 }\n"
      "QPushButton { padding-top: 5 }"
    )

  def setErrorStyleSheet(self):
    self.setStyleSheet(
      "QWidget { background-color: white; border-radius: 10px; border: 1px solid red }\n"
      "QLineEdit { border: none }"
      "QPushButton { border: none }\n"
      "QPushButton { padding-bottom: 5 }\n"
      "QPushButton { padding-top: 5 }"
    )

  def searchTextChanged(self):
    if not self.hideClearSearchButton and not SearchingWidget.lineEdit.text():
      self.clearSearchButton.hide()
      self.hideClearSearchButton = True
    elif self.hideClearSearchButton and SearchingWidget.lineEdit.text():
      self.clearSearchButton.show()
      self.hideClearSearchButton = False

    if self.showErrorMessage:
      self.showErrorMessage = False
      self.setFocusedStyleSheet()

  def searchWithEnter(self):
    if SearchingWidget.lineEdit.text() in SearchingWidget.dictionary_words:
      self.addRecentSearch(SearchingWidget.lineEdit.text())
      SearchingWidget.lineEdit.clear()
    else:
      # Implement showing necessary message
      self.showErrorMessage = True
      self.setErrorStyleSheet()

  def searchWithClick(self, text):
    self.addRecentSearch(text)
    QTimer.singleShot(0, SearchingWidget.lineEdit.clear)

  def clearSearch(self):
    SearchingWidget.lineEdit.clear()
    SearchingWidget.setFocusToSearchBar()

  def addRecentSearch(self, word):
    from MainWidget.mainWidget import MainWidget
    MainWidget.addWord(word)

    addedNow = DBHandler.addRecentSearch(word, 0)
    if addedNow:
      RecentSearchesWidget.addRecentSearch(word, False)
    else:
      RecentSearchesWidget.removeAndAddRecentSearch(word)

  @staticmethod
  def setFocusToSearchBar():
    SearchingWidget.lineEdit.setFocus()
