from PyQt6.QtGui import QFont, QIcon, QKeySequence, QShortcut
from PyQt6.QtWidgets import QCompleter, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtCore import QStringListModel, QTimer, Qt

from side.recent_searches_widget import RecentSearchesWidget
from menu.settings import Settings
from shared.database_handler import get_grades, get_words
from shared.styles import Styles

from models.recent_search import create_recent_search
from models.family import get_words_with_family

class SearchingWidget(QWidget):
  dictionary_words = []

  line_edit = QLineEdit()

  grades = get_grades()
  grades_mapping = {}
  for i in range(len(grades)):
    grades_mapping[i + 1] = grades[i]

  uninitialized_state_text = 'You have to select a subject first.'
  most_recently_searched_word = ''

  def __init__(self):
    super().__init__()

    line_edit_font = QFont(Settings.font, 14)
    completer_font = QFont(Settings.font, 12)
    error_message_font = completer_font

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 0)
    self.layout.setSpacing(0)

    SearchingWidget.line_edit.setFont(line_edit_font)
    SearchingWidget.line_edit.setContentsMargins(0, 1, 0, 1)
    SearchingWidget.line_edit.returnPressed.connect(self.search_with_enter)
    SearchingWidget.line_edit.textChanged.connect(self.search_text_changed)
    self.show_error_message = False

    SearchingWidget.completer = QCompleter(SearchingWidget.dictionary_words)
    SearchingWidget.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    SearchingWidget.completer.activated.connect(self.search_with_click)
    SearchingWidget.completer.popup().setFont(completer_font)
    SearchingWidget.line_edit.setCompleter(SearchingWidget.completer)
    SearchingWidget.line_edit.setPlaceholderText('Please enter a word.')

    self.search_bar_widget = QWidget()
    self.search_bar_widget.layout = QHBoxLayout(self.search_bar_widget)
    self.search_bar_widget.layout.setContentsMargins(10, 0, 0, 0)

    self.clear_search_button = QPushButton()
    self.clear_search_button.setIcon(QIcon('resources/clear_search.png'))
    self.clear_search_button.clicked.connect(self.clear_search)
    self.hide_clear_search_button = True
    self.clear_search_button.hide()

    self.search_button = QPushButton()
    self.search_button.setIcon(QIcon('resources/search.png'))
    self.search_button.clicked.connect(self.search_with_enter)

    self.search_bar_widget.layout.setSpacing(0)
    self.search_bar_widget.layout.addWidget(self.line_edit)
    self.search_bar_widget.layout.addWidget(self.clear_search_button)
    self.search_bar_widget.layout.addSpacing(5)
    self.search_bar_widget.layout.addWidget(self.search_button)
    self.search_bar_widget.layout.addSpacing(10)

    SearchingWidget.error_message = QLabel(SearchingWidget.uninitialized_state_text, self)
    SearchingWidget.error_message.setFont(error_message_font)
    size_policy = SearchingWidget.error_message.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    SearchingWidget.error_message.setSizePolicy(size_policy)
    SearchingWidget.error_message.hide()

    edit_words_button_font = QFont(Settings.font, 14)
    SearchingWidget.edit_words_button = QPushButton('Edit Dictionary Words')
    SearchingWidget.edit_words_button.setToolTip('You can edit the words of each grade here. You can also edit their families.')
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

  def setUnfocusedStyleSheet(self):
    self.search_bar_widget.setStyleSheet(Styles.searching_widget_unfocused_style)

  def set_error_style_sheet(self):
    self.search_bar_widget.setStyleSheet(Styles.searching_widget_error_style)
    SearchingWidget.error_message.show()

  @staticmethod
  def set_initial_error_message():
    SearchingWidget.error_message.setText(SearchingWidget.uninitialized_state_text)

  @staticmethod
  def modify_error_message(text, single):
    SearchingWidget.error_message.setText(SearchingWidget.unknown_word_message(text, single))

  @staticmethod
  def unknown_word_message(text, single):
    if single:
      return 'This word is not contained in the book ' + \
        text + '. Please search for another word.'
    else:
      return "This word is not contained in the books of the profile '" + \
        text + "'. Please search for another word."

  @staticmethod
  def toggle_edit_words_button_visibility(new_visibility_status):
    SearchingWidget.edit_words_button.show() if new_visibility_status else SearchingWidget.edit_words_button.hide()

  @staticmethod
  def update_dictionary_words(profile_id, grade_id, subject_name):
    SearchingWidget.dictionary_words = get_words_with_family(profile_id, grade_id, subject_name)
    # SearchingWidget.dictionary_words = get_words(profile_id, grade_id, subject_name)
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
    SearchingWidget.most_recently_searched_word = SearchingWidget.line_edit.text()

    if SearchingWidget.line_edit.text() in SearchingWidget.dictionary_words:
      self.add_recent_search(SearchingWidget.line_edit.text())
      self.clear_search()
    else:
      self.show_error_message = True
      self.set_error_style_sheet()
      SearchingWidget.set_focus_to_search_bar()

  def search_with_click(self, text):
    if not text == SearchingWidget.most_recently_searched_word:
      self.add_recent_search(text)

    self.clear_search()

  def clear_search(self):
    QTimer.singleShot(0, SearchingWidget.line_edit.clear)
    SearchingWidget.set_focus_to_search_bar()

  def add_recent_search(self, word):
    from central.main_widget import MainWidget
    MainWidget.add_word(word)

    recent_search_exists = create_recent_search(word)
    if recent_search_exists:
      RecentSearchesWidget.remove_and_add_recent_search(word)
    else:
      RecentSearchesWidget.add_recent_search(word)

  @staticmethod
  def set_focus_to_search_bar():
    SearchingWidget.line_edit.setFocus()

  def open_words_editing_widget(self):
    from central.word_editing_widget import WordEditingWidget
    students_editing_dialog = WordEditingWidget()
    students_editing_dialog.exec()
