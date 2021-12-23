from PyQt6.QtGui import QFont, QIcon, QKeySequence, QShortcut
from PyQt6.QtWidgets import QCompleter, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from PyQt6.QtCore import QEvent, QRect, QStringListModel, QTimer, Qt

from databaseHandler import DBHandler
from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from settings import Settings

class SearchingWidget(QWidget):
  dictionaryWords = []

  lineEdit = QLineEdit()

  uninitializedStateText = "You have to select a grade first."
  unknownWordText = "This word is not contained in the dictionary. Please search for another word."

  def __init__(self):
    super().__init__()

    lineEditFont = QFont(Settings.font, 14)
    completerFont = QFont(Settings.font, 10)
    errorMessageFont = completerFont

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 0)
    self.layout.setSpacing(5)

    SearchingWidget.lineEdit.setFont(lineEditFont)
    SearchingWidget.lineEdit.setContentsMargins(0, 1, 0, 1)
    SearchingWidget.lineEdit.returnPressed.connect(self.searchWithEnter)
    SearchingWidget.lineEdit.textChanged.connect(self.searchTextChanged)
    self.showErrorMessage = False

    SearchingWidget.completer = QCompleter(SearchingWidget.dictionaryWords)
    SearchingWidget.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    SearchingWidget.completer.activated.connect(self.searchWithClick)
    SearchingWidget.completer.popup().setFont(completerFont)
    SearchingWidget.lineEdit.setCompleter(SearchingWidget.completer)
    SearchingWidget.lineEdit.setPlaceholderText("Please enter a word.")

    self.searchBarWidget = QWidget()
    self.searchBarWidget.layout = QHBoxLayout(self.searchBarWidget)
    self.searchBarWidget.layout.setContentsMargins(10, 0, 0, 0)

    self.clearSearchButton = QPushButton()
    self.clearSearchButton.setIcon(QIcon("Resources/clearSearch.png"))
    self.clearSearchButton.setFixedWidth(30)
    self.clearSearchButton.clicked.connect(self.clearSearch)
    self.hideClearSearchButton = True
    self.clearSearchButton.hide()

    self.searchButton = QPushButton()
    self.searchButton.setIcon(QIcon("Resources/search.png"))
    self.searchButton.setFixedWidth(30)
    self.searchButton.clicked.connect(self.searchWithEnter)

    self.searchBarWidget.layout.setSpacing(0)
    self.searchBarWidget.layout.addWidget(self.lineEdit)
    self.searchBarWidget.layout.addWidget(self.clearSearchButton)
    self.searchBarWidget.layout.addWidget(self.searchButton)
    self.searchBarWidget.layout.addSpacing(5)

    SearchingWidget.errorMessage = QLabel(SearchingWidget.uninitializedStateText, self)
    SearchingWidget.errorMessage.setFont(errorMessageFont)
    sizePolicy = SearchingWidget.errorMessage.sizePolicy()
    sizePolicy.setRetainSizeWhenHidden(True)
    SearchingWidget.errorMessage.setSizePolicy(sizePolicy)
    SearchingWidget.errorMessage.hide()
    SearchingWidget.errorMessage.setStyleSheet(
      "QLabel { color: red }\n"
      "QLabel { background-color: none }\n"
      "QLabel { border: none }\n"
      "QLabel { margin-left: 2px }"
    )

    self.layout.addWidget(self.searchBarWidget)
    self.layout.addWidget(SearchingWidget.errorMessage)

    self.searchBarFocusShortcut = QShortcut(QKeySequence('/'), self)
    self.searchBarFocusShortcut.activated.connect(SearchingWidget.setFocusToSearchBar)

    self.style()
    self.setFocusedStyleSheet()

  def style(self):
    SearchingWidget.lineEdit.setStyleSheet(
      "QLineEdit { color: blue }"
    )

  def setFocusedStyleSheet(self):
    self.setStyleSheet(
      "QWidget { background-color: white; border-radius: 10px; border: 1px solid blue }\n"
      "QLineEdit { border: none }"
      "QPushButton { border: none }\n"
      "QPushButton { padding-bottom: 5px }\n"
      "QPushButton { padding-top: 5px }"
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
    SearchingWidget.errorMessage.show()

  @staticmethod
  def modifyErrorMessage():
    SearchingWidget.errorMessage.setText(SearchingWidget.unknownWordText)

  @staticmethod
  def updateDictionaryWords():
    from MainWidget.currentSearch import CurrentSearch
    SearchingWidget.dictionaryWords = DBHandler.getWords(CurrentSearch.currentGrade)
    model = QStringListModel(SearchingWidget.dictionaryWords, SearchingWidget.completer)
    SearchingWidget.completer.setModel(model)

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
      SearchingWidget.errorMessage.hide()

  def searchWithEnter(self):
    if SearchingWidget.lineEdit.text() in SearchingWidget.dictionaryWords:
      print('a')
      self.addRecentSearch(SearchingWidget.lineEdit.text())
      SearchingWidget.lineEdit.clear()
    else:
      # Implement showing necessary message
      self.showErrorMessage = True
      self.setErrorStyleSheet()

  def searchWithClick(self, text):
    print('b')
    # self.addRecentSearch(text)
    QTimer.singleShot(0, SearchingWidget.lineEdit.clear)

  def clearSearch(self):
    SearchingWidget.lineEdit.clear()
    SearchingWidget.setFocusToSearchBar()

  def addRecentSearch(self, word):
    from MainWidget.mainWidget import MainWidget
    MainWidget.addWord(word)

    recentSearchExists = DBHandler.addRecentSearch(word)
    if recentSearchExists:
      RecentSearchesWidget.removeAndAddRecentSearch(word)
    else:
      RecentSearchesWidget.addRecentSearch(word, False)

  @staticmethod
  def setFocusToSearchBar():
    SearchingWidget.lineEdit.setFocus()
