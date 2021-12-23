from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QMainWindow, QSplitter, QSplitterHandle, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from databaseHandler import DBHandler

from MainWidget.mainWidget import MainWidget

from SideWidgets.recentActionsWidget import RecentActionsWidget
from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from SideWidgets.starredWordsWidget import StarredWordsWidget
from SideWidgets.subjectsWidget import SubjectsWidget
from titleBar import TitleBar

class MainWindow(QWidget):
  # DBHandler.init_db()
  recentSearchesWidget = RecentSearchesWidget()
  starredWordsWidget = StarredWordsWidget()
  # recentActionsWidget = RecentActionsWidget()
  # subjectsWidget = SubjectsWidget()
  mainWidget = MainWidget()

  def __init__(self):
    super().__init__()
    self.init_gui()

  def init_gui(self):
    self.layout = QGridLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)

    # margin between the title bar and the rest of the application
    self.layout.setSpacing(0)

    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    self.titleBar = TitleBar(self)

    self.centralWidget = QWidget(self)
    self.windowLayout = QHBoxLayout(self.centralWidget)

    # Left Horizontal Splitter
    self.splitterLeftHorizontal = QSplitter(self)
    self.splitterLeftHorizontal.setOrientation(Qt.Orientation.Horizontal)
    self.splitterLeftHorizontal.setChildrenCollapsible(False)

    # Splitter between "Recent Searches" and "Starred Words" widgets
    self.splitterLeftVertical = QSplitter(self.splitterLeftHorizontal)
    self.splitterLeftVertical.setOrientation(Qt.Orientation.Vertical)
    self.splitterLeftVertical.setChildrenCollapsible(False)

    # Recent Searches Scroll Area
    self.splitterLeftVertical.addWidget(MainWindow.recentSearchesWidget)
    MainWindow.recentSearchesWidget.initialize()

    # Starred Words Scroll Area
    self.splitterLeftVertical.addWidget(MainWindow.starredWordsWidget)
    MainWindow.starredWordsWidget.initialize()

    # Right Horizontal Splitter - Left Horizontal Splitter (Right Part)
    # self.splitterRightHorizontal = QSplitter(self.splitterLeftHorizontal)
    # self.splitterRightHorizontal.setOrientation(Qt.Orientation.Horizontal)
    # self.splitterRightHorizontal.setChildrenCollapsible(False)

    # Main Widget
    self.splitterLeftHorizontal.addWidget(MainWindow.mainWidget)

    # Splitter between "Recent Actions" and "Subjects" widgets
    # self.splitterRightVertical = QSplitter(self.splitterRightHorizontal)
    # self.splitterRightVertical.setOrientation(Qt.Orientation.Vertical)
    # self.splitterRightVertical.setChildrenCollapsible(False)

    # Recent Actions Scroll Area
    # self.splitterRightVertical.addWidget(MainWindow.recentActionsWidget)
    # MainWindow.recentActionsWidget.addRecentAction("RecentAction1")
    # MainWindow.recentActionsWidget.addRecentAction("RecentAction2")
    # MainWindow.recentActionsWidget.addRecentAction("RecentAction3")
    # MainWindow.recentActionsWidget.addRecentAction("RecentAction4")
    # MainWindow.recentActionsWidget.addRecentAction("RecentAction5")

    # Subjects Scroll Area
    # self.splitterRightVertical.addWidget(MainWindow.subjectsWidget)
    # MainWindow.subjectsWidget.addSubject("Φυσική")
    # MainWindow.subjectsWidget.addSubject("Μαθηματικά")
    # MainWindow.subjectsWidget.addSubject("Χημεία")
    # MainWindow.subjectsWidget.addSubject("Ιστορία")
    # MainWindow.subjectsWidget.addSubject("Αρχαία")

    self.line = QFrame()
    self.line.setFrameShape(QFrame.Shape.HLine)
    self.line.setFrameShadow(QFrame.Shadow.Plain)
    self.line.setFixedHeight(2)

    self.layout.addWidget(self.titleBar, 0, 0)
    self.layout.addWidget(self.line, 1, 0)
    self.layout.addWidget(self.splitterLeftHorizontal, 2, 0)

    self.style()

  def style(self):
    self.splitterLeftHorizontal.setStyleSheet(
      "QWidget { background-color: yellow }\n"
      "QPushButton { background-color: none }"
    )

    self.line.setStyleSheet(
      "QWidget { background-color: none }"
    )

    self.setStyleSheet(
      "QWidget { background-color: red }\n"
      "QPushButton { background-color: none }"
    )

  @staticmethod
  def updateWidgets(initial):
    from MainWidget.searchingWidget import SearchingWidget
    SearchingWidget.updateDictionaryWords()

    SearchingWidget.modifyErrorMessage()
      
    from MainWidget.resultsWidget import ResultsWidget
    ResultsWidget.showPlaceholder()
    MainWidget.currentSearch.searchedWord.setText("Enter a word.")

    RecentSearchesWidget.populate(initial)
    StarredWordsWidget.populate(initial)

  @staticmethod
  def closeEvent(event):
    DBHandler.closeConnection()
