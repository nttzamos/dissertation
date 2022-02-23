from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget, QMessageBox, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from central.result import Result
from menu.settings import Settings

from models.family import get_family_id, get_family_words, update_word_family
from models.word import get_word_id, word_exists
from shared.wiktionary_parser import fetch_word_details

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

    font = QFont(Settings.font, 18)
    ResultsWidget.placeholder_label.setFont(font)
    ResultsWidget.grid_layout.addWidget(ResultsWidget.placeholder_label)

    ResultsWidget.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)
    self.scroll_area.setWidget(ResultsWidget.scroll_area_widget_contents)

    self.layout.addWidget(self.scroll_area)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.results_widget_style)

  @staticmethod
  def show_results(word):
    ResultsWidget.hide_placeholder()
    ResultsWidget.clear_previous_results()
    ResultsWidget.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    offline_result_words, online_result_words, show_error = ResultsWidget.get_results(word)

    i = 0
    for word in offline_result_words:
      row = i // ResultsWidget.grid_columns
      column = i % ResultsWidget.grid_columns
      result = Result(word, widget_width = ResultsWidget.single_result_width, saved = True)
      ResultsWidget.widget_list.append(result)
      ResultsWidget.grid_layout.addWidget(result, row, column)
      i += 1

    for word in online_result_words:
      row = i // ResultsWidget.grid_columns
      column = i % ResultsWidget.grid_columns
      result = Result(word, widget_width = ResultsWidget.single_result_width, saved = False)
      ResultsWidget.widget_list.append(result)
      ResultsWidget.grid_layout.addWidget(result, row, column)
      i += 1

    if show_error and Settings.get_boolean_setting('show_no_internet_message'):
      ResultsWidget.show_no_internet_message()

    if i == 0:
      ResultsWidget.show_placeholder('This search returned no results.')

  @staticmethod
  def get_results(word):
    from central.current_search import CurrentSearch
    grade_id = CurrentSearch.grade_id
    word_id = get_word_id(grade_id, word)
    family_id = get_family_id(grade_id, word_id)
    offline_result_words = get_family_words(grade_id, family_id)
    if word in offline_result_words:
      offline_result_words.remove(word)
    offline_result_words.sort()

    if Settings.get_setting('word_family_discovery') == 'online_wiktionary':
      try:
        online_family_words, unused = fetch_word_details(word)
      except RuntimeError:
        return offline_result_words, [], True

      online_family_words = list(set(online_family_words) - set(offline_result_words))
      for online_word in online_family_words:
        if word_exists(grade_id, online_word):
          update_word_family(CurrentSearch.grade_id, CurrentSearch.searched_word.text(), [online_word], [])
          offline_result_words.append(online_word)

      online_family_words = list(set(online_family_words) - set(offline_result_words))
      online_family_words.sort()
      offline_result_words.sort()

      return offline_result_words, online_family_words, False
    else:
      return offline_result_words, [], False

  @staticmethod
  def clear_previous_results():
    for result in ResultsWidget.widget_list:
      result.hide()
      result.deleteLater()
    ResultsWidget.widget_list = []

  @staticmethod
  def show_placeholder(text = 'The results of your search will be displayed here.'):
    ResultsWidget.placeholder_label.setText(text)
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
    answer = QMessageBox()
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(text)
    answer.setWindowTitle(title)
    answer.setStandardButtons(QMessageBox.StandardButton.Ok)

    check_box = QCheckBox("Don't show this message again, until closing the app")
    check_box.clicked.connect(ResultsWidget.toggle_message_setting)
    check_box.setChecked(True)

    answer.setCheckBox(check_box)
    answer.exec()

  @staticmethod
  def toggle_message_setting(value):
    Settings.set_boolean_setting('show_no_internet_message', value)
