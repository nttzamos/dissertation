from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ItemWidgets.starredWord import StarredWord
from MenuBar.settings import Settings

class StarredWordsWidget(QWidget):
  scroll_area_widget_contents = QWidget()
  grid_layout = QGridLayout(scroll_area_widget_contents)
  grid_layout.setSpacing(0)
  grid_layout.setContentsMargins(0, 0, 0, 0)

  counter = 1000000
  widget_list = []

  placeholder_label = QLabel()
  show_placeholder_label = False

  vspacer = QLabel('f')

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.title_label = QLabel('Starred Words')
    self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont(Settings.font, 18)
    self.title_label.setFont(font)
    self.layout.addWidget(self.title_label)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    StarredWordsWidget.placeholder_label.setFont(font)
    StarredWordsWidget.placeholder_label.setWordWrap(True)
    StarredWordsWidget.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    invisible_font = QFont(Settings.font, 1)
    StarredWordsWidget.vspacer.setFont(invisible_font)
    size_policy = StarredWordsWidget.vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    StarredWordsWidget.vspacer.setSizePolicy(size_policy)

    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)
    self.scroll_area.setWidget(StarredWordsWidget.scroll_area_widget_contents)
    self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.layout.addWidget(self.scroll_area)

    self.setMinimumWidth(Settings.get_left_widget_width())

    self.style()

  def style(self):
    from Common.styles import Styles
    self.title_label.setStyleSheet(Styles.side_widgets_title_label_style)
    self.setStyleSheet(Styles.side_widgets_style)

  @staticmethod
  def initialize():
    StarredWordsWidget.grid_layout.addWidget(StarredWordsWidget.vspacer, 1000001, 0, 1, -1)
    StarredWordsWidget.show_placeholder()

  @staticmethod
  def populate():
    StarredWordsWidget.clear_previous_starred_words()

    from Common.databaseHandler import DBHandler
    starred_words = DBHandler.get_starred_words()

    if len(starred_words) == 0:
      StarredWordsWidget.show_placeholder(text = 'You do not have any Starred Words')
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
    StarredWordsWidget.grid_layout.addWidget(StarredWordsWidget.widget_list[length-1], StarredWordsWidget.counter, 0)
    StarredWordsWidget.counter -= 1

  @staticmethod
  def remove_starred_word(obj):
    StarredWordsWidget.widget_list.remove(obj)
    if len(StarredWordsWidget.widget_list)==0:
      StarredWordsWidget.show_placeholder(text = 'You do not have any Starred Words')

  @staticmethod
  def toggle_starred_word_starred_state(word):
    for obj in StarredWordsWidget.widget_list:
      if word==obj.word.text():
        obj.remove_word()
        return

  @staticmethod
  def clear_previous_starred_words():
    for starred_word in StarredWordsWidget.widget_list:
      starred_word.hide()
      starred_word.deleteLater()

    StarredWordsWidget.widget_list = []
    StarredWordsWidget.counter = 1000000
    StarredWordsWidget.show_placeholder()

  @staticmethod
  def show_placeholder(text = 'Please select a subject first.'):
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
      StarredWordsWidget.grid_layout.addWidget(StarredWordsWidget.vspacer, 1000001, 0, 1, -1)
      StarredWordsWidget.placeholder_label.hide()
