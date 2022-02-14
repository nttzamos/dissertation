from PyQt6.QtWidgets import QVBoxLayout, QWidget

from MainWidget.currentSearch import CurrentSearch
from MainWidget.searchingWidget import SearchingWidget
from MainWidget.resultsWidget import ResultsWidget
from MenuBar.settings import Settings

class MainWidget(QWidget):
  searching_widget = SearchingWidget()
  current_search = CurrentSearch()
  results_widget = ResultsWidget()

  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.layout.addWidget(MainWidget.searching_widget)
    self.layout.addWidget(MainWidget.current_search)
    self.layout.addWidget(MainWidget.results_widget)

    self.setMinimumWidth(Settings.get_setting('right_widget_width'))

  @staticmethod
  def add_word(word):
    CurrentSearch.searched_word.setText(word)
    ResultsWidget.show_results(word)
