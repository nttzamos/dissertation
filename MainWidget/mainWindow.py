from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QSplitter, QWidget
from PyQt6.QtCore import Qt

from MainWidget.mainWidget import MainWidget

from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from SideWidgets.starredWordsWidget import StarredWordsWidget
from MenuBar.menuBar import MenuBar

class MainWindow(QWidget):
  recentSearchesWidget = RecentSearchesWidget()
  starredWordsWidget = StarredWordsWidget()
  mainWidget = MainWidget()

  def __init__(self):
    super().__init__()

    self.layout = QGridLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)

    # Margin between the title bar and the rest of the application
    self.layout.setSpacing(0)

    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    self.menuBar = MenuBar(self)

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

    # Main Widget
    self.splitterLeftHorizontal.addWidget(MainWindow.mainWidget)

    self.line = QFrame()
    self.line.setFrameShape(QFrame.Shape.HLine)
    self.line.setFrameShadow(QFrame.Shadow.Plain)
    self.line.setFixedHeight(2)

    self.layout.addWidget(self.menuBar, 0, 0)
    self.layout.addWidget(self.line, 1, 0)
    self.layout.addWidget(self.splitterLeftHorizontal, 2, 0)

    self.style()

  def style(self):
    self.line.setStyleSheet("QWidget { background-color: none }")

    from Common.styles import Styles
    self.splitterLeftHorizontal.setStyleSheet(Styles.mainWindowBackgroundStyle)
    self.setStyleSheet(Styles.mainWindowStyle)

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
