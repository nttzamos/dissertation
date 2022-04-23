from PyQt6.QtWidgets import QVBoxLayout, QWidget

from central.results_widget import ResultsWidget
from search.current_search import CurrentSearch
from search.searching_widget import SearchingWidget

class MainWidget(QWidget):
  def __init__(self):
    super().__init__()

    MainWidget.searching_widget = SearchingWidget()
    MainWidget.current_search = CurrentSearch()
    MainWidget.results_widget = ResultsWidget()

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.layout.addWidget(MainWidget.searching_widget)
    self.layout.addWidget(MainWidget.current_search)
    self.layout.addWidget(MainWidget.results_widget)

  @staticmethod
  def add_word(word):
    CurrentSearch.searched_word_label.setText(word)
    ResultsWidget.show_results(word)
