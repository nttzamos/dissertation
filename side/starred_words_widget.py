from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from item.starred_word import StarredWord
from menu.settings import Settings
from models.starred_word import get_starred_words

class StarredWordsWidget(QWidget):
  TITLE = 'Αγαπημένες Λέξεις'
  NO_STARRED_WORDS_TEXT = 'Δεν έχετε αγαπημένες λέξεις'
  SELECT_A_SUBJECT_TEXT = 'Επιλέξτε κάποιο μάθημα πρώτα.'
  MAX_ROW = 1000000

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    scroll_area_widget_contents = QWidget()

    StarredWordsWidget.grid_layout = QGridLayout(scroll_area_widget_contents)
    StarredWordsWidget.grid_layout.setSpacing(0)
    StarredWordsWidget.grid_layout.setContentsMargins(0, 0, 0, 0)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(scroll_area_widget_contents)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    StarredWordsWidget.counter = StarredWordsWidget.MAX_ROW
    StarredWordsWidget.widget_list = []

    font = QFont(Settings.FONT, 18)
    invisible_font = QFont(Settings.FONT, 1)

    self.title_label = QLabel(StarredWordsWidget.TITLE)
    self.title_label.setFont(font)
    self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    StarredWordsWidget.placeholder_label = QLabel()
    StarredWordsWidget.placeholder_label.setFont(font)
    StarredWordsWidget.placeholder_label.setWordWrap(True)
    StarredWordsWidget.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    StarredWordsWidget.show_placeholder_label = False

    StarredWordsWidget.vspacer = QLabel('f')
    StarredWordsWidget.vspacer.setFont(invisible_font)
    size_policy = StarredWordsWidget.vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    StarredWordsWidget.vspacer.setSizePolicy(size_policy)

    self.layout.addWidget(self.title_label)
    self.layout.addWidget(scroll_area)

    self.setMinimumWidth(Settings.get_setting('left_widget_width'))

    self.style()

  def style(self):
    from shared.styles import Styles
    self.title_label.setStyleSheet(Styles.side_widgets_title_label_style)
    self.setStyleSheet(Styles.side_widgets_style)

  @staticmethod
  def initialize():
    StarredWordsWidget.show_placeholder()
    StarredWordsWidget.grid_layout.addWidget(
      StarredWordsWidget.vspacer, StarredWordsWidget.MAX_ROW + 1, 0, 1, -1
    )

  @staticmethod
  def populate():
    StarredWordsWidget.clear_previous_starred_words()

    starred_words = get_starred_words()

    if len(starred_words) == 0:
      StarredWordsWidget.show_placeholder(StarredWordsWidget.NO_STARRED_WORDS_TEXT)
      return
    else:
      StarredWordsWidget.hide_placeholder()

    for word in starred_words:
      widget = StarredWord(word)
      StarredWordsWidget.widget_list.append(widget)
      StarredWordsWidget.grid_layout.addWidget(widget, StarredWordsWidget.counter, 0)
      StarredWordsWidget.counter -= 1

  @staticmethod
  def add_starred_word(word):
    if StarredWordsWidget.show_placeholder_label:
      StarredWordsWidget.hide_placeholder()

    widget = StarredWord(word)
    StarredWordsWidget.widget_list.append(widget)
    length = len(StarredWordsWidget.widget_list)

    StarredWordsWidget.grid_layout.addWidget(
      StarredWordsWidget.widget_list[length-1], StarredWordsWidget.counter, 0
    )

    StarredWordsWidget.counter -= 1

  @staticmethod
  def remove_starred_word(starred_word):
    StarredWordsWidget.widget_list.remove(starred_word)
    if len(StarredWordsWidget.widget_list)==0:
      StarredWordsWidget.show_placeholder(StarredWordsWidget.NO_STARRED_WORDS_TEXT)

  @staticmethod
  def toggle_starred_word_starred_state(word):
    for starred_word in StarredWordsWidget.widget_list:
      if word == starred_word.word.text():
        starred_word.remove_word()
        return

  @staticmethod
  def clear_previous_starred_words():
    for starred_word in StarredWordsWidget.widget_list:
      starred_word.hide()
      starred_word.deleteLater()

    StarredWordsWidget.widget_list = []
    StarredWordsWidget.counter = StarredWordsWidget.MAX_ROW
    StarredWordsWidget.show_placeholder()

  @staticmethod
  def show_placeholder(text=SELECT_A_SUBJECT_TEXT):
    StarredWordsWidget.placeholder_label.setText(text)

    if not StarredWordsWidget.show_placeholder_label:
      StarredWordsWidget.show_placeholder_label = True
      StarredWordsWidget.grid_layout.addWidget(StarredWordsWidget.placeholder_label)
      StarredWordsWidget.grid_layout.removeWidget(StarredWordsWidget.vspacer)
      StarredWordsWidget.placeholder_label.show()

  @staticmethod
  def hide_placeholder():
    if StarredWordsWidget.show_placeholder_label:
      StarredWordsWidget.show_placeholder_label = False
      StarredWordsWidget.placeholder_label.hide()
      StarredWordsWidget.grid_layout.addWidget(
        StarredWordsWidget.vspacer, StarredWordsWidget.MAX_ROW + 1, 0, 1, -1
      )

  @staticmethod
  def update_word(word, new_word):
    for starred_word in StarredWordsWidget.widget_list:
      if word == starred_word.word.text():
        starred_word.update_word(new_word)
        return

  @staticmethod
  def delete_word(word):
    for starred_word in StarredWordsWidget.widget_list:
      if word == starred_word.word.text():
        starred_word.hide()
        starred_word.deleteLater()
        StarredWordsWidget.remove_starred_word(starred_word)
        return
