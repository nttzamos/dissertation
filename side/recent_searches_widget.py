from PyQt6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from item.recent_search import RecentSearch
from menu.settings import Settings
from models.recent_search import get_recent_searches
from models.starred_word import starred_word_exists, get_starred_words
from shared.font_settings import FontSettings
from shared.spacer import Spacer

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('side', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class RecentSearchesWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    RecentSearchesWidget.recent_searches_list = QWidget()
    RecentSearchesWidget.recent_searches_list.layout = QVBoxLayout(RecentSearchesWidget.recent_searches_list)
    RecentSearchesWidget.recent_searches_list.layout.setSpacing(0)
    RecentSearchesWidget.recent_searches_list.layout.setContentsMargins(0, 0, 0, 0)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(RecentSearchesWidget.recent_searches_list)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    RecentSearchesWidget.widget_list = []

    font = FontSettings.get_font('heading')

    title_label = QLabel(_('RECENT_SEARCHES_TITLE'))
    title_label.setFont(font)
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    from shared.styles import Styles
    title_label.setStyleSheet(Styles.side_widgets_title_label_style)

    RecentSearchesWidget.placeholder_label = QLabel()
    RecentSearchesWidget.placeholder_label.setFont(font)
    RecentSearchesWidget.placeholder_label.setWordWrap(True)
    RecentSearchesWidget.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    RecentSearchesWidget.show_placeholder_label = False

    RecentSearchesWidget.spacer = Spacer()

    self.layout.addWidget(title_label)
    self.layout.addWidget(scroll_area)

    self.setMinimumWidth(Settings.get_setting('left_widget_width'))

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.side_widgets_style)

  @staticmethod
  def initialize():
    RecentSearchesWidget.recent_searches_list.layout.insertWidget(0, RecentSearchesWidget.spacer)
    RecentSearchesWidget.show_placeholder()

  @staticmethod
  def populate():
    RecentSearchesWidget.clear_previous_recent_searches()

    recent_searches = get_recent_searches()
    starred_words = get_starred_words()

    if len(recent_searches) == 0:
      RecentSearchesWidget.show_placeholder(_('NO_RECENT_SEARCHES_TEXT'))
      return
    else:
      RecentSearchesWidget.hide_placeholder()

    for word in recent_searches:
      recent_search = RecentSearch(word, word in starred_words)
      RecentSearchesWidget.widget_list.append(recent_search)
      RecentSearchesWidget.recent_searches_list.layout.insertWidget(0, recent_search)

  @staticmethod
  def add_recent_search(word):
    if RecentSearchesWidget.show_placeholder_label:
      RecentSearchesWidget.hide_placeholder()

    recent_search = RecentSearch(word, starred_word_exists(word))
    RecentSearchesWidget.widget_list.append(recent_search)
    RecentSearchesWidget.recent_searches_list.layout.insertWidget(0, recent_search)

  @staticmethod
  def remove_and_add_recent_search(word):
    for recent_search in RecentSearchesWidget.widget_list:
      if recent_search.word.text()==word:
        RecentSearchesWidget.recent_searches_list.layout.removeWidget(recent_search)
        RecentSearchesWidget.recent_searches_list.layout.insertWidget(0, recent_search)
        return

  @staticmethod
  def toggle_recent_search_starred_icon(word):
    for recent_search in RecentSearchesWidget.widget_list:
      if word == recent_search.word.text():
        recent_search.toggle_starred_icon()
        return

  @staticmethod
  def remove_recent_search(recent_search):
    RecentSearchesWidget.widget_list.remove(recent_search)
    if len(RecentSearchesWidget.widget_list)==0:
      RecentSearchesWidget.show_placeholder(_('NO_RECENT_SEARCHES_TEXT'))

  @staticmethod
  def clear_previous_recent_searches():
    for recentSearch in RecentSearchesWidget.widget_list:
      recentSearch.hide()
      recentSearch.deleteLater()

    RecentSearchesWidget.widget_list = []
    RecentSearchesWidget.show_placeholder()

  @staticmethod
  def show_placeholder(text=None):
    if text == None: text = _('RECENT_SEARCHES_SHOWN_HERE')

    RecentSearchesWidget.placeholder_label.setText(text)

    if not RecentSearchesWidget.show_placeholder_label:
      RecentSearchesWidget.show_placeholder_label = True
      RecentSearchesWidget.recent_searches_list.layout.insertWidget(0, RecentSearchesWidget.placeholder_label)
      RecentSearchesWidget.recent_searches_list.layout.removeWidget(RecentSearchesWidget.spacer)
      RecentSearchesWidget.placeholder_label.show()

  @staticmethod
  def hide_placeholder():
    if RecentSearchesWidget.show_placeholder_label:
      RecentSearchesWidget.show_placeholder_label = False
      RecentSearchesWidget.recent_searches_list.layout.insertWidget(0, RecentSearchesWidget.spacer)
      RecentSearchesWidget.placeholder_label.hide()

  @staticmethod
  def update_word(word, new_word):
    for recent_search in RecentSearchesWidget.widget_list:
      if word == recent_search.word.text():
        recent_search.update_word(new_word)
        return

  @staticmethod
  def delete_word(word):
    for recent_search in RecentSearchesWidget.widget_list:
      if word == recent_search.word.text():
        recent_search.hide()
        recent_search.deleteLater()
        RecentSearchesWidget.remove_recent_search(recent_search)
        return
