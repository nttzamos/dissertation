from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ItemWidgets.recentSearch import RecentSearch
from MenuBar.settings import Settings
from Common.databaseHandler import DBHandler

class RecentSearchesWidget(QWidget):
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
    self.title_label = QLabel('Recent Searches')
    self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont(Settings.font, 18)
    self.title_label.setFont(font)
    self.layout.addWidget(self.title_label)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    RecentSearchesWidget.placeholder_label.setFont(font)
    RecentSearchesWidget.placeholder_label.setWordWrap(True)
    RecentSearchesWidget.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    invisible_font = QFont(Settings.font, 1)
    RecentSearchesWidget.vspacer.setFont(invisible_font)
    size_policy = RecentSearchesWidget.vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    RecentSearchesWidget.vspacer.setSizePolicy(size_policy)

    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)
    self.scroll_area.setWidget(RecentSearchesWidget.scroll_area_widget_contents)
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
    RecentSearchesWidget.grid_layout.addWidget(RecentSearchesWidget.vspacer, 1000001, 0, 1, -1)
    RecentSearchesWidget.show_placeholder()

  @staticmethod
  def populate():
    RecentSearchesWidget.clear_previous_recent_searches()

    recent_searches = DBHandler.get_recent_searches()
    starred_words = DBHandler.get_starred_words()

    if len(recent_searches) == 0:
      RecentSearchesWidget.show_placeholder(text = 'You do not have any Recent Searches')
      return
    else:
      RecentSearchesWidget.hide_placeholder()

    for word in recent_searches:
      widget = RecentSearch(word, word in starred_words)
      RecentSearchesWidget.widget_list.append(widget)
      RecentSearchesWidget.grid_layout.addWidget(widget, RecentSearchesWidget.counter, 0)
      RecentSearchesWidget.counter -= 1

  @staticmethod
  def add_recent_search(word, condition):
    if RecentSearchesWidget.show_placeholder_label:
      RecentSearchesWidget.hide_placeholder()

    condition = DBHandler.starred_word_exists(word)
    widget = RecentSearch(word, condition)
    RecentSearchesWidget.widget_list.append(widget)
    RecentSearchesWidget.grid_layout.addWidget(widget, RecentSearchesWidget.counter, 0)
    RecentSearchesWidget.counter -= 1

  @staticmethod
  def remove_and_add_recent_search(word):
    for obj in RecentSearchesWidget.widget_list:
      if obj.word.text()==word:
        RecentSearchesWidget.grid_layout.removeWidget(obj)
        RecentSearchesWidget.grid_layout.addWidget(obj, RecentSearchesWidget.counter, 0)
        RecentSearchesWidget.counter -=1
        return

  @staticmethod
  def toggle_recent_search_starred_icon(word):
    for obj in RecentSearchesWidget.widget_list:
      if word == obj.word.text():
        obj.toggle_starred_icon()
        return

  @staticmethod
  def remove_recent_search(obj):
    RecentSearchesWidget.widget_list.remove(obj)
    if len(RecentSearchesWidget.widget_list)==0:
      RecentSearchesWidget.show_placeholder(text = 'You do not have any Recent Searches')

  @staticmethod
  def clear_previous_recent_searches():
    for recentSearch in RecentSearchesWidget.widget_list:
      recentSearch.hide()
      recentSearch.deleteLater()

    RecentSearchesWidget.widget_list = []
    RecentSearchesWidget.counter = 1000000
    RecentSearchesWidget.show_placeholder()

  @staticmethod
  def show_placeholder(text = 'Please select a subject first.'):
    RecentSearchesWidget.placeholder_label.setText(text)
    if not RecentSearchesWidget.show_placeholder_label:
      RecentSearchesWidget.show_placeholder_label = True
      RecentSearchesWidget.grid_layout.addWidget(RecentSearchesWidget.placeholder_label)
      RecentSearchesWidget.grid_layout.removeWidget(RecentSearchesWidget.vspacer)
      RecentSearchesWidget.placeholder_label.show()

  @staticmethod
  def hide_placeholder():
    if RecentSearchesWidget.show_placeholder_label:
      RecentSearchesWidget.show_placeholder_label = False
      RecentSearchesWidget.grid_layout.addWidget(RecentSearchesWidget.vspacer, 1000001, 0, 1, -1)
      RecentSearchesWidget.placeholder_label.hide()
