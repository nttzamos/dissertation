from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QLineEdit,
                             QLabel, QGroupBox, QListWidget, QPushButton,
                             QComboBox, QCompleter, QAbstractItemView)
from PyQt6.QtCore import Qt, QTimer, QStringListModel

from menu.settings import Settings
from models.word import get_word_id
from models.related_word import get_related_words, update_related_words
from shared.database_handler import get_grades, get_grade_words
from shared.font_settings import FontSettings

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class WordFamilyUpdateWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = FontSettings.get_font('heading')
    text_font = FontSettings.get_font('text')
    button_font = FontSettings.get_font('button')
    error_message_font = FontSettings.get_font('error')

    WordFamilyUpdateWidget.just_searched_with_enter = False
    WordFamilyUpdateWidget.just_searched_related_with_enter = False

    self.searched_word = ''
    self.word_current_related_words = []
    self.word_initial_related_words = []

    grade_selection_widget = QGroupBox(_('GRADE_SELECTION_TEXT'))
    grade_selection_widget.setFont(section_label_font)
    grade_selection_widget.layout = QHBoxLayout(grade_selection_widget)
    grade_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    WordFamilyUpdateWidget.grade_selector = QComboBox()
    WordFamilyUpdateWidget.grade_selector.setFont(text_font)
    WordFamilyUpdateWidget.grade_selector.addItems(get_grades())
    WordFamilyUpdateWidget.grade_selector.activated.connect(self.grade_selector_activated)

    grade_selection_widget.layout.addWidget(WordFamilyUpdateWidget.grade_selector)

    word_selection_widget = QGroupBox(_('WORD_SELECTION_TEXT'))
    word_selection_widget.setFont(section_label_font)
    word_selection_widget.layout = QVBoxLayout(word_selection_widget)
    word_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.word_selection_line_edit = QLineEdit()
    self.word_selection_line_edit.setFont(text_font)
    self.word_selection_line_edit.returnPressed.connect(self.search_with_enter)
    WordFamilyUpdateWidget.dictionary_words = get_grade_words(1)
    WordFamilyUpdateWidget.completer = QCompleter(WordFamilyUpdateWidget.dictionary_words)
    WordFamilyUpdateWidget.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    WordFamilyUpdateWidget.completer.activated.connect(self.search_with_click)
    WordFamilyUpdateWidget.completer.popup().setFont(text_font)
    self.word_selection_line_edit.setCompleter(WordFamilyUpdateWidget.completer)
    self.word_selection_line_edit.setPlaceholderText(_('PLEASE_ENTER_WORD_TEXT'))
    self.error_message_label = QLabel(_('PLEASE_ENTER_ANOTHER_WORD_TEXT'), self)
    self.error_message_label.setFont(error_message_font)
    self.word_selection_line_edit.textChanged.connect(self.error_message_label.hide)
    self.error_message_label.hide()

    word_selection_widget.layout.addWidget(self.word_selection_line_edit)
    word_selection_widget.layout.addWidget(self.error_message_label)

    self.word_family_selection_widget = QGroupBox(_('FAMILY_SELECTION_TEXT'))
    self.word_family_selection_widget.setFont(section_label_font)
    self.word_family_selection_widget.layout = QVBoxLayout(self.word_family_selection_widget)
    self.word_family_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.related_word_selection_line_edit = QLineEdit()
    self.related_word_selection_line_edit.setFont(text_font)
    self.related_word_selection_line_edit.returnPressed.connect(
      self.search_related_with_enter
    )

    WordFamilyUpdateWidget.related_completer = \
      QCompleter(WordFamilyUpdateWidget.dictionary_words)

    WordFamilyUpdateWidget.related_completer.setCaseSensitivity(
      Qt.CaseSensitivity.CaseInsensitive
    )

    WordFamilyUpdateWidget.related_completer.activated.connect(
      self.search_related_with_click
    )

    WordFamilyUpdateWidget.related_completer.popup().setFont(text_font)
    self.related_word_selection_line_edit.setCompleter(
      WordFamilyUpdateWidget.related_completer
    )

    self.related_word_selection_line_edit.setPlaceholderText(_('SELECT_WORD_TO_BE_ADDED_TEXT'))

    self.related_word_selection_line_edit.hide()

    self.word_related_words_list = QListWidget()
    self.word_related_words_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
    self.word_related_words_list.addItem(_('FAMILY_WORDS_APPEAR_HERE_TEXT'))

    self.remove_words_button = QPushButton(_('REMOVE_SELECTED_WORDS_TEXT'))
    self.remove_words_button.setFont(button_font)
    self.remove_words_button.pressed.connect(self.remove_selected_words)

    self.word_family_selection_widget.layout.addWidget(self.related_word_selection_line_edit)
    self.word_family_selection_widget.layout.addSpacing(5)
    self.word_family_selection_widget.layout.addWidget(self.word_related_words_list)
    self.word_family_selection_widget.layout.addSpacing(5)
    self.word_family_selection_widget.layout.addWidget(
      self.remove_words_button, alignment=Qt.AlignmentFlag.AlignRight
    )

    self.save_button = QPushButton(_('SAVE_FAMILY_BUTTON_TEXT'))
    self.save_button.setFont(button_font)
    self.save_button.pressed.connect(self.update_related_words)
    self.save_button.setDisabled(True)

    self.layout.addWidget(grade_selection_widget)
    self.layout.addWidget(word_selection_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(self.word_family_selection_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.error_message_label.setStyleSheet(Styles.error_message_label_style)
    self.save_button.setStyleSheet(Styles.dialog_button_style)
    self.remove_words_button.setStyleSheet(Styles.dialog_button_style)

  def disable_save_button(self):
    self.save_button.setDisabled(True)
    self.word_family_selection_widget.setTitle(
      _('FAMILY_SELECTION_TEXT')
    )

  def grade_selector_activated(self, index):
    WordFamilyUpdateWidget.dictionary_words = get_grade_words(index + 1)
    model = QStringListModel(
      WordFamilyUpdateWidget.dictionary_words, WordFamilyUpdateWidget.completer
    )

    WordFamilyUpdateWidget.completer.setModel(model)
    WordFamilyUpdateWidget.related_completer.setModel(model)
    self.clear_previous_search()

  def search_with_enter(self):
    WordFamilyUpdateWidget.just_searched_with_enter = True

    self.searched_word = self.word_selection_line_edit.text()
    if self.searched_word in WordFamilyUpdateWidget.dictionary_words:
      self.search_valid_word_details()
    else:
      self.error_message_label.show()

  def search_with_click(self, text):
    if WordFamilyUpdateWidget.just_searched_with_enter:
      WordFamilyUpdateWidget.just_searched_with_enter = False
      return

    self.searched_word = text
    self.search_valid_word_details()

  def search_valid_word_details(self):
    QTimer.singleShot(0, self.related_word_selection_line_edit.clear)

    grade_id = WordFamilyUpdateWidget.grade_selector.currentIndex() + 1
    word_id = get_word_id(grade_id, self.searched_word)

    self.word_initial_related_words = get_related_words(grade_id, word_id)
    self.word_current_related_words = list(self.word_initial_related_words)

    self.word_related_words_list.clear()

    if len(self.word_current_related_words) > 0:
      self.word_initial_related_words.sort()
      self.word_related_words_list.addItems(self.word_initial_related_words)
    else:
      self.word_related_words_list.addItem(_('NO_FAMILY_WORDS_TEXT'))

    self.disable_save_button()
    self.related_word_selection_line_edit.show()
    self.related_word_selection_line_edit.setFocus()

  def search_related_with_enter(self):
    WordFamilyUpdateWidget.just_searched_related_with_enter = True

    related_word = self.related_word_selection_line_edit.text()
    self.search_related(related_word)

  def search_related_with_click(self, text):
    if WordFamilyUpdateWidget.just_searched_related_with_enter:
      WordFamilyUpdateWidget.just_searched_related_with_enter = False
      return

    self.search_related(text)

  def search_related(self, word):
    if not self.related_word_is_invalid(word):
      QTimer.singleShot(0, self.related_word_selection_line_edit.clear)

      if self.word_related_words_list.item(0).text() == _('NO_FAMILY_WORDS_TEXT'):
        self.word_related_words_list.clear()

      self.word_current_related_words.append(word)
      self.word_related_words_list.addItem(word)
      self.save_button.setEnabled(True)

      if set(self.word_initial_related_words) == set(self.word_current_related_words):
        self.disable_save_button()
      else:
        self.save_button.setEnabled(True)
        self.word_family_selection_widget.setTitle(
          _('FAMILY_SELECTION_TEXT_WITH_CHANGES')
        )

  def related_word_is_invalid(self, related_word):
    if related_word == self.searched_word or related_word in self.word_current_related_words:
      return True

    if not related_word in WordFamilyUpdateWidget.dictionary_words:
      return True

    return False

  def remove_selected_words(self):
    if len(self.word_related_words_list.selectedItems()) == 0: return

    for item in self.word_related_words_list.selectedItems():
      if item.text() == _('NO_FAMILY_WORDS_TEXT'): return
      if item.text() == _('FAMILY_WORDS_APPEAR_HERE_TEXT'): return

      self.word_current_related_words.remove(item.text())
      self.word_related_words_list.takeItem(self.word_related_words_list.row(item))

    if self.word_related_words_list.count() == 0:
      self.word_related_words_list.addItem(_('NO_FAMILY_WORDS_TEXT'))

    if set(self.word_initial_related_words) == set(self.word_current_related_words):
      self.disable_save_button()
    else:
      self.save_button.setEnabled(True)
      self.word_family_selection_widget.setTitle(
        _('FAMILY_SELECTION_TEXT_WITH_CHANGES')
      )

  def update_related_words(self):
    words_to_remove = list(set(self.word_initial_related_words) - set(self.word_current_related_words))
    words_to_add = list(set(self.word_current_related_words) - set(self.word_initial_related_words))

    grade_id = WordFamilyUpdateWidget.grade_selector.currentIndex() + 1
    update_related_words(grade_id, self.searched_word, words_to_add, words_to_remove)

    self.word_initial_related_words = list(self.word_current_related_words)
    self.disable_save_button()

    from search.current_search import CurrentSearch
    language = gettext.translation('search', localedir='resources/locale', languages=[language_code])
    language.install()
    if (self.searched_word == CurrentSearch.searched_word_label.text() and
        grade_id == CurrentSearch.grade_id):
      from central.results_widget import ResultsWidget
      ResultsWidget.show_placeholder()
      CurrentSearch.searched_word_label.setText(language.gettext('ENTER_WORD_TEXT'))

  def update_word_family_update_widget(self, word, grade_id):
    if grade_id != WordFamilyUpdateWidget.grade_selector.currentIndex() + 1: return

    if word == self.searched_word or word in self.word_current_related_words:
      self.clear_previous_search()

  def clear_previous_search(self):
    self.related_word_selection_line_edit.hide()
    self.searched_word = ''
    self.word_current_related_words = []

    self.disable_save_button()

    QTimer.singleShot(0, self.word_selection_line_edit.clear)

    self.word_related_words_list.clear()
    self.word_related_words_list.addItem(_('FAMILY_WORDS_APPEAR_HERE_TEXT'))

  @staticmethod
  def update_dictionary_words(word_to_remove=None, word_to_add=None, grade_id=None):
    if grade_id != WordFamilyUpdateWidget.grade_selector.currentIndex() + 1: return

    if word_to_add != None:
      WordFamilyUpdateWidget.dictionary_words.append(word_to_add)

    if word_to_remove != None:
      WordFamilyUpdateWidget.dictionary_words.remove(word_to_remove)

    model = QStringListModel(
      WordFamilyUpdateWidget.dictionary_words, WordFamilyUpdateWidget.completer
    )

    WordFamilyUpdateWidget.completer.setModel(model)
    WordFamilyUpdateWidget.related_completer.setModel(model)
