from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from MainWidget.result import Result
from MenuBar.settings import Settings

from models.family import get_family_id, get_family_words
from models.word import get_word_id, word_exists
from Common.wiktionary_parser import fetch_word_details

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
    offline_result_words, online_saved_result_words, online_result_words, show_error = ResultsWidget.get_results(word)

    i = 0
    for word in offline_result_words:
      row = i // ResultsWidget.grid_columns
      column = i % ResultsWidget.grid_columns
      result = Result(word, widget_width=ResultsWidget.single_result_width, state = 1)
      ResultsWidget.widget_list.append(result)
      ResultsWidget.grid_layout.addWidget(result, row, column)
      i += 1

    for word in online_saved_result_words:
      row = i // ResultsWidget.grid_columns
      column = i % ResultsWidget.grid_columns
      result = Result(word, widget_width=ResultsWidget.single_result_width, state = 2)
      ResultsWidget.widget_list.append(result)
      ResultsWidget.grid_layout.addWidget(result, row, column)
      i += 1

    for word in online_result_words:
      row = i // ResultsWidget.grid_columns
      column = i % ResultsWidget.grid_columns
      result = Result(word, widget_width = ResultsWidget.single_result_width, state = 3)
      ResultsWidget.widget_list.append(result)
      ResultsWidget.grid_layout.addWidget(result, row, column)
      i += 1

    if show_error:
      ResultsWidget.show_no_internet_message()

  @staticmethod
  def get_results(word):
    from MainWidget.currentSearch import CurrentSearch
    grade_id = CurrentSearch.grade_id
    word_id = get_word_id(grade_id, word)
    family_id = get_family_id(grade_id, word_id)
    offline_result_words = get_family_words(grade_id, family_id)
    offline_result_words.remove(word)
    offline_result_words.sort()

    if Settings.get_setting('word_family_discovery') == 'online_wiktionary':
      try:
        online_family_words, unused = fetch_word_details(word)
      except RuntimeError:
        return offline_result_words, [], [], True

      online_family_words = list(set(online_family_words) - set(offline_result_words))
      online_saved_family_words = []
      for online_word in online_family_words:
        if word_exists(grade_id, online_word):
          online_saved_family_words.append(online_word)

      online_family_words = list(set(online_family_words) - set(online_saved_family_words))
      online_family_words.sort()
      online_saved_family_words.sort()

      return offline_result_words, online_saved_family_words, online_family_words, False
    else:
      return offline_result_words, [], [], False

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

  @staticmethod
  def show_no_internet_message():
    title = 'No Internet Connection'
    text = 'The online wiktionary setting is enabled but you have no internet connection.'
    answer = QMessageBox.critical(None, title, text, QMessageBox.StandardButton.Ok)
    if answer == QMessageBox.StandardButton.Ok:
      return
