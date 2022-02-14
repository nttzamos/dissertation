from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QSplitter, QWidget
from PyQt6.QtCore import Qt

from MainWidget.mainWidget import MainWidget

from SideWidgets.recentSearchesWidget import RecentSearchesWidget
from SideWidgets.starredWordsWidget import StarredWordsWidget
from MenuBar.menuBar import MenuBar

from models.profile import get_profile_name
class MainWindow(QWidget):
  recent_searches_widget = RecentSearchesWidget()
  starred_words_widget = StarredWordsWidget()
  main_widget = MainWidget()

  def __init__(self):
    super().__init__()

    self.layout = QGridLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)

    # Margin between the title bar and the rest of the application
    self.layout.setSpacing(0)

    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    self.menuBar = MenuBar(self)

    # Left Horizontal Splitter
    self.splitter_left_horizontal = QSplitter(self)
    self.splitter_left_horizontal.setOrientation(Qt.Orientation.Horizontal)
    self.splitter_left_horizontal.setChildrenCollapsible(False)

    # Splitter between 'Recent Searches' and 'Starred Words' widgets
    self.splitter_left_vertical = QSplitter(self.splitter_left_horizontal)
    self.splitter_left_vertical.setOrientation(Qt.Orientation.Vertical)
    self.splitter_left_vertical.setChildrenCollapsible(False)

    # Recent Searches Scroll Area
    self.splitter_left_vertical.addWidget(MainWindow.recent_searches_widget)
    MainWindow.recent_searches_widget.initialize()

    # Starred Words Scroll Area
    self.splitter_left_vertical.addWidget(MainWindow.starred_words_widget)
    MainWindow.starred_words_widget.initialize()

    # Main Widget
    self.splitter_left_horizontal.addWidget(MainWindow.main_widget)

    self.line = QFrame()
    self.line.setFrameShape(QFrame.Shape.HLine)
    self.line.setFrameShadow(QFrame.Shadow.Plain)
    self.line.setFixedHeight(2)

    self.layout.addWidget(self.menuBar, 0, 0)
    self.layout.addWidget(self.line, 1, 0)
    self.layout.addWidget(self.splitter_left_horizontal, 2, 0)

    self.style()

  def style(self):
    self.line.setStyleSheet('QWidget { background-color: none }')

    from Common.styles import Styles
    self.splitter_left_horizontal.setStyleSheet(Styles.main_window_background_style)
    self.setStyleSheet(Styles.main_window_style)

  @staticmethod
  def update_widgets(profile_id, grade_id, subject_name):
    from MainWidget.searchingWidget import SearchingWidget
    SearchingWidget.update_dictionary_words(profile_id, grade_id, subject_name)

    if subject_name == 'All Subjects':
      SearchingWidget.modify_error_message(get_profile_name(profile_id), False)
    else:
      SearchingWidget.modify_error_message(subject_name, True)

    from MainWidget.resultsWidget import ResultsWidget
    ResultsWidget.show_placeholder()
    MainWidget.current_search.searched_word.setText('Enter a word.')

    RecentSearchesWidget.populate()
    StarredWordsWidget.populate()

  @staticmethod
  def clear_previous_subject_details():
    from MainWidget.currentSearch import CurrentSearch
    if not CurrentSearch.subject_selector_active: return

    from MainWidget.searchingWidget import SearchingWidget
    SearchingWidget.set_initial_error_message()

    from MainWidget.resultsWidget import ResultsWidget
    ResultsWidget.show_placeholder()
    CurrentSearch.subject_selector_active = False

    RecentSearchesWidget.clear_previous_recent_searches()
    StarredWordsWidget.clear_previous_starred_words()
