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
  single_result_width = Settings.get_setting('single_result_width')

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
    results_words = ResultsWidget.get_results(word)

    for i in range(len(results_words)):
      row = i // ResultsWidget.grid_columns
      column = i % ResultsWidget.grid_columns
      result = Result(results_words[i], widget_width=ResultsWidget.single_result_width)
      ResultsWidget.widget_list.append(result)
      ResultsWidget.grid_layout.addWidget(result, row, column)

  @staticmethod
  def get_results(word):
    from MainWidget.currentSearch import CurrentSearch
    grade_id = CurrentSearch.grade_id
    from Common.databaseHandler import DBHandler
    word_id = DBHandler.get_word_id(grade_id, word)
    family_id = DBHandler.get_family_id(grade_id, word_id)
    family_words = DBHandler.get_family_words(grade_id, family_id)
    family_words.remove(word)
    return family_words

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
