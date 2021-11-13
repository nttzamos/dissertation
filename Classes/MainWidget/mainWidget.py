from PyQt6.QtWidgets import QCompleter, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt
# from PyQt6.QtGui import QFont
from Classes.databaseHandler import DBHandler
from searchingWidget import SearchingWidget
from resultsWidget import ResultsWidget

class MainWidget(QWidget):
  def __init__(self):
    super().__init__()
    # self.parent = parent
    # self.database = DBHandler()
    self.setFixedWidth(1200)
    # self.setStyleSheet("QFrame {border-right : 2px solid black}")
    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    # widget_names = [
    #   "Balcony", "Balloon", "Barcelona", "Balcony Light",
    #   "Fan", "Room Light", "Brioche", "Basketball",
    #   "Bedroom Heater", "Wall Switch"
    # ]
    widget_names = DBHandler.getAllWords()

    # Search bar.
    self.searchbar = QLineEdit()
    self.searchbar.setContentsMargins(0, 0, 0, 0)
    # self.searchbar.textChanged.connect(self.update_display)
    self.searchbar.returnPressed.connect(self.updateSearches)

    # Adding Completer.
    self.completer = QCompleter(widget_names)
    self.completer.setCaseSensitivity(Qt.CaseInsensitive)
    self.completer.activated.connect(self.updateSearches1)
    self.searchbar.setCompleter(self.completer)

    self.searchbar.setPlaceholderText("Please enter a word.")
    self.layout.addWidget(self.searchbar)

    self.middleMiddleWidget = SearchingWidget()
    self.layout.addWidget(self.middleMiddleWidget)

    self.middleBottomWidget = ResultsWidget()
    self.layout.addWidget(self.middleBottomWidget)

  def updateSearches(self):
    # addWidget(self.searchbar.text())
    self.addRecentSearch(self.searchbar.text())
    self.searchbar.clear()
    # print("Hello1")

  def updateSearches1(self):
    # print("Hello2")
    QTimer.singleShot(0, self.searchbar.clear)

  def addRecentSearch(self, word):
    self.parent.addRecentSearch(word)
    self.addWord(word)

  def addWord(self, word):
    self.middleMiddleWidget.word.setText(word)
