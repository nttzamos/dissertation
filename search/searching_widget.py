from PyQt6.QtWidgets import (QCompleter, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QWidget, QSizePolicy)
from PyQt6.QtCore import QStringListModel, QTimer, Qt
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut

from menu.settings import Settings
from models.recent_search import create_recent_search
from shared.database_handler import get_words
from shared.font_settings import FontSettings
from shared.styles import Styles
from side.recent_searches_widget import RecentSearchesWidget

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('search', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class SearchingWidget(QWidget):
  def __init__(self):
    super().__init__()

    line_edit_font = FontSettings.get_font('text')
    completer_font = FontSettings.get_font('text')
    edit_words_button_font = FontSettings.get_font('button')
    error_message_font = FontSettings.get_font('error')

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 0)
    self.layout.setSpacing(0)

    SearchingWidget.just_searched_with_enter = False

    SearchingWidget.line_edit = QLineEdit()
    SearchingWidget.line_edit.setMaxLength(100)
    SearchingWidget.line_edit.setFont(line_edit_font)
    SearchingWidget.line_edit.setContentsMargins(0, 1, 0, 1)
    SearchingWidget.line_edit.returnPressed.connect(self.search_with_enter)
    SearchingWidget.line_edit.textChanged.connect(self.search_text_changed)
    self.show_error_message = False

    SearchingWidget.dictionary_words = []
    SearchingWidget.completer = QCompleter(SearchingWidget.dictionary_words)
    SearchingWidget.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    SearchingWidget.completer.activated.connect(self.search_with_click)
    SearchingWidget.completer.popup().setFont(completer_font)
    SearchingWidget.line_edit.setCompleter(SearchingWidget.completer)
    SearchingWidget.line_edit.setPlaceholderText(_('PLEASE_ENTER_WORD_TEXT'))

    self.search_bar_widget = QWidget()
    self.search_bar_widget.layout = QHBoxLayout(self.search_bar_widget)
    self.search_bar_widget.layout.setContentsMargins(10, 0, 0, 0)

    self.clear_search_button = QPushButton()
    self.clear_search_button.setToolTip(_('CLEAR_SEARCH_TEXT'))
    self.clear_search_button.setIcon(QIcon('resources/clear_search.png'))
    self.clear_search_button.clicked.connect(self.clear_search)
    self.hide_clear_search_button = True
    self.clear_search_button.hide()

    search_button = QPushButton()
    search_button.setToolTip(_('SEARCH_TEXT'))
    search_button.setIcon(QIcon('resources/search.png'))
    search_button.clicked.connect(self.search_with_button)

    self.search_bar_widget.layout.setSpacing(0)
    self.search_bar_widget.layout.addWidget(SearchingWidget.line_edit)
    self.search_bar_widget.layout.addWidget(self.clear_search_button)
    self.search_bar_widget.layout.addSpacing(5)
    self.search_bar_widget.layout.addWidget(search_button)
    self.search_bar_widget.layout.addSpacing(10)

    SearchingWidget.current_error_message_text = _('UNINITIALIZED_STATE_TEXT')
    SearchingWidget.error_message = QLabel(self)
    SearchingWidget.error_message.setFont(error_message_font)
    size_policy = SearchingWidget.error_message.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    SearchingWidget.error_message.setSizePolicy(size_policy)
    SearchingWidget.error_message.hide()

    SearchingWidget.edit_words_button = QPushButton(_('EDIT_WORDS_BUTTON_TEXT'))
    SearchingWidget.edit_words_button.setToolTip(_('EDIT_WORDS_TOOLTIP_TEXT'))
    SearchingWidget.edit_words_button.setFont(edit_words_button_font)
    SearchingWidget.edit_words_button.clicked.connect(self.open_words_editing_widget)
    SearchingWidget.edit_words_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    self.subwidget = QWidget()
    self.subwidget.layout = QHBoxLayout(self.subwidget)
    self.subwidget.layout.setContentsMargins(5, 10, 0, 0)
    self.subwidget.layout.addWidget(SearchingWidget.error_message, alignment=Qt.AlignmentFlag.AlignTop)
    self.subwidget.layout.addWidget(SearchingWidget.edit_words_button)
    size_policy = SearchingWidget.edit_words_button.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    SearchingWidget.edit_words_button.setSizePolicy(size_policy)

    if not Settings.get_boolean_setting('show_edit_dict_words_button'):
      SearchingWidget.edit_words_button.hide()

    self.layout.addWidget(self.search_bar_widget)
    self.layout.addWidget(self.subwidget)

    self.search_bar_focus_shortcut = QShortcut(QKeySequence('/'), self)
    self.search_bar_focus_shortcut.activated.connect(SearchingWidget.set_focus_to_search_bar)

    self.style()
    self.set_focused_styleSheet()

  def style(self):
    SearchingWidget.error_message.setStyleSheet(Styles.error_message_style)
    self.subwidget.setStyleSheet(Styles.subwidget_style)

  def set_focused_styleSheet(self):
    self.search_bar_widget.setStyleSheet(Styles.searching_widget_focused_style)

  def set_error_style_sheet(self):
    self.search_bar_widget.setStyleSheet(Styles.searching_widget_error_style)

    if (SearchingWidget.line_edit.text() == '' and
        SearchingWidget.current_error_message_text != _('UNINITIALIZED_STATE_TEXT')):
      SearchingWidget.error_message.setText(_('EMPTY_SEARCH_BAR_TEXT'))
    else:
      SearchingWidget.error_message.setText(SearchingWidget.current_error_message_text)

    SearchingWidget.error_message.show()

  @staticmethod
  def set_initial_error_message():
    SearchingWidget.current_error_message_text = _('UNINITIALIZED_STATE_TEXT')

  @staticmethod
  def modify_error_message(text, single):
    SearchingWidget.current_error_message_text = SearchingWidget.unknown_word_message(text, single)

  @staticmethod
  def unknown_word_message(text, single):
    if single:
      return _('WORD_NOT_INCLUDED_IN_BOOK') + text + _('SEARCH_ANOTHER_WORD')
    else:
      return _('WORD_NOT_INCLUDED_IN_PROFILE') + text + _('SEARCH_ANOTHER_WORD')

  @staticmethod
  def toggle_edit_words_button_visibility(new_visibility_status):
    if new_visibility_status:
      SearchingWidget.edit_words_button.show()
    else:
      SearchingWidget.edit_words_button.hide()

  @staticmethod
  def update_selected_dictionary():
    from search.current_search import CurrentSearch
    if CurrentSearch.subject_selector_active:
      subject_name = CurrentSearch.subject_selector.currentText()

      SearchingWidget.dictionary_words = get_words(
        CurrentSearch.profile_id, CurrentSearch.grade_id, subject_name
      )

      model = QStringListModel(SearchingWidget.dictionary_words, SearchingWidget.completer)
      SearchingWidget.completer.setModel(model)

  @staticmethod
  def add_or_remove_dictionary_words(words_to_add, words_to_remove):
    if len(words_to_add) > 0:
      SearchingWidget.dictionary_words.extend(words_to_add)

    if len(words_to_remove) > 0:
      for word in words_to_remove:
        SearchingWidget.dictionary_words.remove(word)

    model = QStringListModel(SearchingWidget.dictionary_words, SearchingWidget.completer)
    SearchingWidget.completer.setModel(model)

  def search_text_changed(self):
    if not self.hide_clear_search_button and not SearchingWidget.line_edit.text():
      self.clear_search_button.hide()
      self.hide_clear_search_button = True
    elif self.hide_clear_search_button and SearchingWidget.line_edit.text():
      self.clear_search_button.show()
      self.hide_clear_search_button = False

    if self.show_error_message:
      self.show_error_message = False
      self.set_focused_styleSheet()
      SearchingWidget.error_message.hide()

  def search_with_enter(self):
    SearchingWidget.just_searched_with_enter = True

    if SearchingWidget.line_edit.text() in SearchingWidget.dictionary_words:
      self.add_recent_search(SearchingWidget.line_edit.text())
      self.clear_search()
    else:
      self.show_error_message = True
      self.set_error_style_sheet()
      SearchingWidget.set_focus_to_search_bar()

  def search_with_button(self):
    if SearchingWidget.line_edit.text() in SearchingWidget.dictionary_words:
      self.add_recent_search(SearchingWidget.line_edit.text())
      self.clear_search()
    else:
      self.show_error_message = True
      self.set_error_style_sheet()
      SearchingWidget.set_focus_to_search_bar()

  def search_with_click(self, text):
    if SearchingWidget.just_searched_with_enter:
      SearchingWidget.just_searched_with_enter = False
      return

    self.add_recent_search(text)
    self.clear_search()

  def clear_search(self):
    QTimer.singleShot(0, SearchingWidget.line_edit.clear)
    SearchingWidget.set_focus_to_search_bar()

  def add_recent_search(self, word):
    from central.main_widget import MainWidget
    MainWidget.search_word(word)

    recent_search_exists = create_recent_search(word)
    if recent_search_exists:
      RecentSearchesWidget.remove_and_add_recent_search(word)
    else:
      RecentSearchesWidget.add_recent_search(word)

  @staticmethod
  def set_focus_to_search_bar():
    SearchingWidget.line_edit.setFocus()

  def open_words_editing_widget(self):
    from dialogs.word_editing_widget import WordEditingWidget
    word_editing_dialog = WordEditingWidget()
    word_editing_dialog.exec()
