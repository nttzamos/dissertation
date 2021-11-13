from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QSplitter, QWidget
from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont

from databaseHandler import DBHandler

from MainWidget.mainWidget import MainWidget

from SideWidgets.recentActionsWidget import RecentActionsWidget
from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from SideWidgets.starredWordsWidget import StarredWordsWidget
from SideWidgets.subjectsWidget import SubjectsWidget

class MainWindow(QMainWindow):
  recentSearchesWidget = RecentSearchesWidget()
  starredWordsWidget = StarredWordsWidget()
  recentActionsWidget = RecentActionsWidget()
  subjectsWidget = SubjectsWidget()

  def __init__(self):
    super().__init__()
    # self.database = DBHandler()
    DBHandler.init_db()
    # self.database.init_db()    
    self.init_gui()

  def init_gui(self):
    self.centralWidget = QWidget(self)
    self.windowLayout = QHBoxLayout(self.centralWidget)

    # Left Horizontal Splitter
    self.splitterLeftHorizontal = QSplitter(self.centralWidget)
    self.splitterLeftHorizontal.setOrientation(Qt.Horizontal)
    self.splitterLeftHorizontal.setChildrenCollapsible(False)

    # Left Vertical Splitter - Left Horizontal Splitter (Left Part)
    self.splitterLeftVertical = QSplitter(self.splitterLeftHorizontal)
    self.splitterLeftVertical.setOrientation(Qt.Vertical)
    self.splitterLeftVertical.setChildrenCollapsible(False)

    # Left Upper Scroll Area
    # self.recentSearches = SideWidget("Searched Words", "searchedWord", self.splitterLeftVertical)
    # self.recentSearches = RecentSearchesWidget("Recent Searches", "searchedWord", self)
    self.splitterLeftVertical.addWidget(MainWindow.recentSearchesWidget)
    # self.recentSearches = self.database.getAllRecentSearches()
    self.recentSearches = DBHandler.getAllRecentSearches()
    # self.starredWords = set(self.database.getAllStarredWords())
    self.starredWords = set(DBHandler.getAllStarredWords())
    MainWindow.recentSearchesWidget.initialRecentSearchesAdding(self.recentSearches, self.starredWords)
    if len(self.recentSearches)==0:
      MainWindow.recentSearchesWidget.addPlaceholder()

    # Left Bottom Scroll Area
    # self.starredWordsWidget = StarredWordsWidget("Starred Words", "starredWord", self)
    # self.starredWords.addWidget("Φωτεινός")
    self.splitterLeftVertical.addWidget(MainWindow.starredWordsWidget)
    # self.starredWords = self.database.getAllStarredWords()
    MainWindow.starredWordsWidget = DBHandler.getAllStarredWords()
    MainWindow.starredWordsWidget.initialStarredWordsAdding(self.starredWords)
    if len(self.starredWords)==0:
      self.starredWords.addPlaceholder()

    # Right Horizontal Splitter - Left Horizontal Splitter (Right Part)
    self.splitterRightHorizontal = QSplitter(self.splitterLeftHorizontal)
    self.splitterRightHorizontal.setOrientation(Qt.Horizontal)
    self.splitterRightHorizontal.setChildrenCollapsible(False)

    # Middle Widget - Right Horizontal Splitter (Left Part)
    self.middleWidget = MainWidget(self)
    self.splitterRightHorizontal.addWidget(self.middleWidget)

    # Right Vertical Splitter - Right Horizontal Splitter (Right Part)
    self.splitterRightVertical = QSplitter(self.splitterRightHorizontal)
    self.splitterRightVertical.setOrientation(Qt.Vertical)
    self.splitterRightVertical.setChildrenCollapsible(False)

    # Right Vertical Splitter - Upper Scroll Area
    # self.recentActions = RecentActionsWidget("Recent Actions", "recentAction", self)
    self.splitterRightVertical.addWidget(MainWindow.recentActionsWidget)
    MainWindow.recentActionsWidget.addWidget("RecentAction1")
    MainWindow.recentActionsWidget.addWidget("RecentAction2")
    MainWindow.recentActionsWidget.addWidget("RecentAction3")
    MainWindow.recentActionsWidget.addWidget("RecentAction4")
    MainWindow.recentActionsWidget.addWidget("RecentAction5")

    # Right Vertical Splitter - Bottom Scroll Area
    # self.subjects = SubjectsWidget("Subjects", "subject", self)
    self.splitterRightVertical.addWidget(MainWindow.subjectsWidget)
    MainWindow.subjectsWidget.addSubject("Φυσική")
    MainWindow.subjectsWidget.addSubject("Μαθηματικά")
    MainWindow.subjectsWidget.addSubject("Χημεία")
    MainWindow.subjectsWidget.addSubject("Ιστορία")
    MainWindow.subjectsWidget.addSubject("Αρχαία")

    self.windowLayout.addWidget(self.splitterLeftHorizontal)
    self.setCentralWidget(self.centralWidget)

  @staticmethod
  def closeEvent(self, event):
    # self.database.closeConnection()
    DBHandler.closeConnection()

  @staticmethod
  def toggleStarred(self, obj):
    word = obj.label.text()
    newCondition=1
    if newCondition==1:
      self.starredWords.addWidget(word)

  @staticmethod
  def toggleStarredUpper(self, obj):
    word = obj.label.text()
    self.recentSearches.toggleStarredUpper(word)

  @staticmethod
  def toggleStarredBottom(self, obj):
    word = obj.label.text()
    # addedNow = self.database.addStarredWord(0, word)
    addedNow = DBHandler.addStarredWord(0, word)
    if addedNow:
      self.starredWords.addWidget(word)
    else:
      self.starredWords.toggleStarredBottom(word)
      # self.database.deleteStarredWord(word)
      DBHandler.deleteStarredWord(word)

  @staticmethod
  def addRecentSearch(self, word):
    # addedNow = self.database.addRecentSearch(word, 0)
    addedNow = DBHandler.addRecentSearch(word, 0)
    if addedNow:
      self.recentSearches.add(word, False)
    else:
      self.recentSearches.removeAndAddWidget(word)

  @staticmethod
  def reloadWord(self, word):
    self.middleWidget.addWord(word)
    