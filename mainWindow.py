from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QSplitter, QWidget
from PyQt6.QtCore import Qt

from databaseHandler import DBHandler
from MainWidget.mainWidget import MainWidget
from SideWidgets.recentActionsWidget import RecentActionsWidget
from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from SideWidgets.starredWordsWidget import StarredWordsWidget
from SideWidgets.subjectsWidget import SubjectsWidget

class MainWindow(QMainWindow):
  DBHandler.init_db()
  recentSearchesWidget = RecentSearchesWidget()
  starredWordsWidget = StarredWordsWidget()
  recentActionsWidget = RecentActionsWidget()
  subjectsWidget = SubjectsWidget()
  mainWidget = MainWidget()

  def __init__(self):
    super().__init__()
    self.init_gui()

  def init_gui(self):
    self.centralWidget = QWidget(self)
    self.windowLayout = QHBoxLayout(self.centralWidget)

    # Left Horizontal Splitter
    self.splitterLeftHorizontal = QSplitter(self.centralWidget)
    self.splitterLeftHorizontal.setOrientation(Qt.Orientation.Horizontal)
    self.splitterLeftHorizontal.setChildrenCollapsible(False)

    # Left Vertical Splitter - Left Horizontal Splitter (Left Part)
    self.splitterLeftVertical = QSplitter(self.splitterLeftHorizontal)
    self.splitterLeftVertical.setOrientation(Qt.Orientation.Vertical)
    self.splitterLeftVertical.setChildrenCollapsible(False)

    # Left Upper Scroll Area
    self.splitterLeftVertical.addWidget(MainWindow.recentSearchesWidget)
    self.recentSearches = DBHandler.getAllRecentSearches()
    self.starredWords = DBHandler.getAllStarredWords()
    MainWindow.recentSearchesWidget.initialRecentSearchesAdding(self.recentSearches, self.starredWords)
    if len(self.recentSearches)==0:
      MainWindow.recentSearchesWidget.addPlaceholder()

    # Left Bottom Scroll Area
    self.splitterLeftVertical.addWidget(MainWindow.starredWordsWidget)
    self.starredWords = DBHandler.getAllStarredWords()
    MainWindow.starredWordsWidget.initialStarredWordsAdding(self.starredWords)
    if len(self.starredWords)==0:
      MainWindow.starredWordsWidget.addPlaceholder()

    # Right Horizontal Splitter - Left Horizontal Splitter (Right Part)
    self.splitterRightHorizontal = QSplitter(self.splitterLeftHorizontal)
    self.splitterRightHorizontal.setOrientation(Qt.Orientation.Horizontal)
    self.splitterRightHorizontal.setChildrenCollapsible(False)

    # Middle Widget - Right Horizontal Splitter (Left Part)
    self.splitterRightHorizontal.addWidget(MainWindow.mainWidget)

    # Right Vertical Splitter - Right Horizontal Splitter (Right Part)
    self.splitterRightVertical = QSplitter(self.splitterRightHorizontal)
    self.splitterRightVertical.setOrientation(Qt.Orientation.Vertical)
    self.splitterRightVertical.setChildrenCollapsible(False)

    # Right Vertical Splitter - Upper Scroll Area
    self.splitterRightVertical.addWidget(MainWindow.recentActionsWidget)
    MainWindow.recentActionsWidget.addRecentAction("RecentAction1")
    MainWindow.recentActionsWidget.addRecentAction("RecentAction2")
    MainWindow.recentActionsWidget.addRecentAction("RecentAction3")
    MainWindow.recentActionsWidget.addRecentAction("RecentAction4")
    MainWindow.recentActionsWidget.addRecentAction("RecentAction5")

    # Right Vertical Splitter - Bottom Scroll Area
    self.splitterRightVertical.addWidget(MainWindow.subjectsWidget)
    MainWindow.subjectsWidget.addSubject("Φυσική")
    MainWindow.subjectsWidget.addSubject("Μαθηματικά")
    MainWindow.subjectsWidget.addSubject("Χημεία")
    MainWindow.subjectsWidget.addSubject("Ιστορία")
    MainWindow.subjectsWidget.addSubject("Αρχαία")

    self.windowLayout.addWidget(self.splitterLeftHorizontal)
    self.setCentralWidget(self.centralWidget)

  @staticmethod
  def closeEvent(event):
    DBHandler.closeConnection()
    