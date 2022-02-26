from PyQt6.QtWidgets import QFrame, QGridLayout, QSplitter, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from central.main_widget import MainWidget
from menu.menu_bar import MenuBar
from models.profile import get_profile_name
from side.recent_searches_widget import RecentSearchesWidget
from side.starred_words_widget import StarredWordsWidget

class MainWindow(QWidget):
  recent_searches_widget = RecentSearchesWidget()
  starred_words_widget = StarredWordsWidget()
  main_widget = MainWidget()

  def __init__(self):
    super().__init__()

    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    self.layout = QGridLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

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

    from shared.styles import Styles
    self.splitter_left_horizontal.setStyleSheet(Styles.main_window_background_style)
    self.setStyleSheet(Styles.main_window_style)

  @staticmethod
  def update_widgets(profile_id, subject_name):
    from search.searching_widget import SearchingWidget
    from central.results_widget import ResultsWidget

    if subject_name == 'All Subjects':
      SearchingWidget.modify_error_message(get_profile_name(profile_id), False)
    else:
      SearchingWidget.modify_error_message(subject_name, True)

    SearchingWidget.update_selected_dictionary()
    ResultsWidget.show_placeholder()
    MainWidget.current_search.searched_word.setText('Enter a word.')
    RecentSearchesWidget.populate()
    StarredWordsWidget.populate()

  @staticmethod
  def clear_previous_subject_details():
    from search.current_search import CurrentSearch
    if not CurrentSearch.subject_selector_active: return

    from search.searching_widget import SearchingWidget
    from central.results_widget import ResultsWidget

    SearchingWidget.set_initial_error_message()
    ResultsWidget.show_placeholder()
    CurrentSearch.subject_selector_active = False
    RecentSearchesWidget.clear_previous_recent_searches()
    StarredWordsWidget.clear_previous_starred_words()
