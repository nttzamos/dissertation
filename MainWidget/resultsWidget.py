from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from MainWidget.result import Result
from MenuBar.settings import Settings

# import enchant
from queue import PriorityQueue

class ResultsWidget(QWidget):
  scroll_area_widget_contents = QWidget()
  grid_layout = QGridLayout(scroll_area_widget_contents)
  widget_list = []
  counter = 1000000
  show_placeholder_label = True
  placeholder_label = QLabel('The results of your search will be displayed here.')
  grid_columns = Settings.get_results_widget_columns()
  single_result_width = Settings.get_single_result_width()

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    font = QFont(Settings.font, 14)
    ResultsWidget.placeholder_label.setFont(font)
    ResultsWidget.grid_layout.addWidget(ResultsWidget.placeholder_label)

    ResultsWidget.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)
    self.scroll_area.setWidget(ResultsWidget.scroll_area_widget_contents)
    self.layout.addWidget(self.scroll_area)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.results_widget_style)

  @staticmethod
  def show_results(word):
    ResultsWidget.hide_placeholder()
    ResultsWidget.clear_previous_results()
    ResultsWidget.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    results_words = ResultsWidget.getResults(word)

    for i in range(len(results_words)):
      row = i // ResultsWidget.grid_columns
      column = i % ResultsWidget.grid_columns
      result = Result(results_words[i], widget_width=ResultsWidget.single_result_width)
      ResultsWidget.widget_list.append(result)
      ResultsWidget.grid_layout.addWidget(result, row, column)

  @staticmethod
  def getResults(word):
    from MainWidget.searchingWidget import SearchingWidget
    dictionary_words = SearchingWidget.dictionary_words
    maximum_size = Settings.get_maximum_results() + 1

    queue = PriorityQueue()
    for i in range(len(dictionary_words)):
      # distance = enchant.utils.levenshtein(word, dictionary_words[i]) * -1
      distance = 5
      if queue.qsize() < maximum_size:
        queue.put((distance, dictionary_words[i]))
      else:
        tmp = queue.get()
        if tmp[0] < distance:
          queue.put((distance, dictionary_words[i]))
        else:
          queue.put(tmp)

    results_words = []
    for i in range(maximum_size):
      results_words.append(queue.get()[1])

    if word in results_words:
      results_words.remove(word)

    results_words.sort()
    return results_words

  @staticmethod
  def clear_previous_results():
    for result in ResultsWidget.widget_list:
      result.hide()
      result.deleteLater()
    ResultsWidget.widget_list = []

  @staticmethod
  def show_placeholder():
    ResultsWidget.clear_previous_results()
    if not ResultsWidget.show_placeholder_label:
      ResultsWidget.show_placeholder_label = True
      ResultsWidget.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
      ResultsWidget.placeholder_label.show()

  @staticmethod
  def hide_placeholder():
    if ResultsWidget.show_placeholder_label:
      ResultsWidget.show_placeholder_label = False
      ResultsWidget.placeholder_label.hide()
