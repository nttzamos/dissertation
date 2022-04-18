from PyQt6.QtWidgets import (QGridLayout, QVBoxLayout, QHBoxLayout, QWidget,
                             QLineEdit, QLabel, QGroupBox, QScrollArea,
                             QCheckBox, QPushButton, QComboBox, QSizePolicy,
                             QMessageBox, QCompleter)
from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtGui import QFont

from menu.settings import Settings
from models.word import get_word_subjects, word_exists, update_word, destroy_word
from shared.database_handler import get_grades, get_grade_words, get_grade_subjects

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class WordUpdateWidget(QWidget):
  MAXIMUM_NAME_LENGTH = 20
  GREEK_CHARACTERS = [
    'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο',
    'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω', 'ς', 'ά', 'έ', 'ί', 'ή', 'ύ',
    'ό', 'ώ', 'ϊ', 'ϋ', 'ΐ', 'ΰ']

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = QFont(Settings.FONT, 16)
    combo_box_font = QFont(Settings.FONT, 14)
    line_edit_font = QFont(Settings.FONT, 14)
    completer_font = QFont(Settings.FONT, 12)
    error_message_font = QFont(Settings.FONT, 10)

    self.check_boxes_modified = []

    WordUpdateWidget.just_searched_with_enter = False

    grade_selection_widget = QGroupBox(_('GRADE_SELECTION_TEXT'))
    grade_selection_widget.setFont(section_label_font)
    grade_selection_widget.layout = QHBoxLayout(grade_selection_widget)
    grade_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    WordUpdateWidget.grade_selector = QComboBox()
    WordUpdateWidget.grade_selector.setFont(combo_box_font)
    WordUpdateWidget.grade_selector.addItems(get_grades())
    WordUpdateWidget.grade_selector.activated.connect(self.grade_selector_activated)

    grade_selection_widget.layout.addWidget(WordUpdateWidget.grade_selector)

    word_selection_widget = QGroupBox(_('WORD_SELECTION_TEXT'))
    word_selection_widget.setFont(section_label_font)
    word_selection_widget.layout = QVBoxLayout(word_selection_widget)
    word_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.word_selection_line_edit = QLineEdit()
    self.word_selection_line_edit.setFont(line_edit_font)
    self.word_selection_line_edit.returnPressed.connect(self.search_with_enter)
    WordUpdateWidget.dictionary_words = get_grade_words(1)
    WordUpdateWidget.completer = QCompleter(WordUpdateWidget.dictionary_words)
    WordUpdateWidget.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    WordUpdateWidget.completer.activated.connect(self.search_with_click)
    WordUpdateWidget.completer.popup().setFont(completer_font)
    self.word_selection_line_edit.setCompleter(WordUpdateWidget.completer)
    self.word_selection_line_edit.setPlaceholderText(_('PLEASE_ENTER_WORD_TEXT'))
    self.selection_error_message_label = QLabel(_('PLEASE_ENTER_ANOTHER_WORD_TEXT'), self)
    self.selection_error_message_label.setFont(error_message_font)
    self.word_selection_line_edit.textChanged.connect(self.selection_error_message_label.hide)
    self.selection_error_message_label.hide()

    word_selection_widget.layout.addWidget(self.word_selection_line_edit)
    word_selection_widget.layout.addWidget(self.selection_error_message_label)

    self.word_widget = QGroupBox(_('WORD_MODIFICATION_TEXT'))
    self.word_widget.setFont(section_label_font)
    self.word_widget.layout = QVBoxLayout(self.word_widget)
    self.word_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.word_line_edit = QLineEdit()
    self.word_line_edit.setFont(line_edit_font)
    self.word_line_edit.textChanged.connect(self.update_save_button_state)

    self.error_message_label = QLabel(self)
    self.error_message_label.setFont(error_message_font)
    self.word_line_edit.textChanged.connect(self.error_message_label.hide)
    self.error_message_label.hide()

    self.word_widget.layout.addWidget(self.word_line_edit)
    self.word_widget.layout.addWidget(self.error_message_label)
    self.word_widget.hide()

    subjects_widget = QGroupBox(_('WORD_SUBJECT_SELECTION_TEXT'))
    subjects_widget.setFont(section_label_font)
    subjects_widget.layout = QHBoxLayout(subjects_widget)
    subjects_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.subjects_selection_widget = QWidget()
    self.subjects_selection_widget.layout = QGridLayout(self.subjects_selection_widget)
    self.subjects_selection_widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(self.subjects_selection_widget)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    self.check_boxes = []

    vspacer = QLabel('f')
    invisible_font = QFont(Settings.FONT, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    self.subjects_selection_widget.layout.addWidget(vspacer, 1000, 0)

    subjects_widget.layout.addWidget(scroll_area)

    self.save_button = QPushButton(_('UPDATE_WORD_BUTTON_TEXT'))
    self.save_button.pressed.connect(self.update_word)
    self.save_button.setDisabled(True)
    self.save_button.setAutoDefault(False)

    self.delete_button = QPushButton(_('DELETE_WORD_BUTTON_TEXT'))
    self.delete_button.pressed.connect(self.delete_word)
    self.delete_button.setDisabled(True)
    self.delete_button.setAutoDefault(False)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.setContentsMargins(0, 0, 0, 0)
    buttons_widget.layout.addWidget(self.delete_button)
    buttons_widget.layout.addSpacing(10)
    buttons_widget.layout.addWidget(self.save_button)

    self.layout.addWidget(grade_selection_widget)
    self.layout.addWidget(word_selection_widget)
    self.layout.addWidget(self.word_widget)
    self.layout.addWidget(subjects_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(buttons_widget, alignment=Qt.AlignmentFlag.AlignRight)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.selection_error_message_label.setStyleSheet(Styles.error_message_label_style)
    self.error_message_label.setStyleSheet(Styles.error_message_label_style)

  def set_word_to_update(self, word, grade_id):
    self.grade_selector.setCurrentIndex(grade_id - 1)

    WordUpdateWidget.dictionary_words = get_grade_words(grade_id)
    model = QStringListModel(WordUpdateWidget.dictionary_words, WordUpdateWidget.completer)
    WordUpdateWidget.completer.setModel(model)

    self.word_selection_line_edit.setText(word)

    self.searched_word = word
    self.search_valid_word_details()

  def search_with_enter(self):
    WordUpdateWidget.just_searched_with_enter = True

    self.searched_word = self.word_selection_line_edit.text()
    if self.searched_word in WordUpdateWidget.dictionary_words:
      self.search_valid_word_details()
    else:
      self.selection_error_message_label.show()

  def search_with_click(self, text):
    if WordUpdateWidget.just_searched_with_enter:
      WordUpdateWidget.just_searched_with_enter = False
      return

    self.searched_word = text
    self.search_valid_word_details()

  def search_valid_word_details(self):
    self.word_widget.show()
    self.word_line_edit.setText(self.searched_word)
    self.word_line_edit.setFocus()
    self.save_button.setDisabled(True)
    self.delete_button.setEnabled(True)

    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    grade_subjects = get_grade_subjects(WordUpdateWidget.grade_selector.currentIndex() + 1)
    self.word_subjects = get_word_subjects(
      WordUpdateWidget.grade_selector.currentIndex() + 1, self.searched_word
    )

    check_box_font = QFont(Settings.FONT, 14)
    self.check_boxes = []
    self.check_boxes_modified = []
    for i in range(len(grade_subjects)):
      check_box = QCheckBox(grade_subjects[i])
      check_box.clicked.connect(lambda ch, i=i: self.check_box_modified(grade_subjects[i]))
      check_box.setFont(check_box_font)
      if grade_subjects[i] in self.word_subjects: check_box.setChecked(True)

      self.check_boxes.append(check_box)
      self.subjects_selection_widget.layout.addWidget(check_box, i, 0)

  def grade_selector_activated(self, index):
    WordUpdateWidget.dictionary_words = get_grade_words(index + 1)
    model = QStringListModel(WordUpdateWidget.dictionary_words, WordUpdateWidget.completer)
    WordUpdateWidget.completer.setModel(model)

    QTimer.singleShot(0, self.word_selection_line_edit.clear)
    self.word_selection_line_edit.setFocus()

    self.save_button.setDisabled(True)
    self.delete_button.setDisabled(True)
    self.word_widget.hide()

    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    self.check_boxes = []

  @staticmethod
  def add_word_to_dictionary(grade, word):
    if grade == WordUpdateWidget.grade_selector.currentIndex() + 1:
      WordUpdateWidget.dictionary_words.append(word)
      model = QStringListModel(WordUpdateWidget.dictionary_words, WordUpdateWidget.completer)
      WordUpdateWidget.completer.setModel(model)

  def update_dictionary_words(self, old_word, new_word):
    WordUpdateWidget.dictionary_words.append(new_word)
    WordUpdateWidget.dictionary_words.remove(old_word)
    model = QStringListModel(WordUpdateWidget.dictionary_words, WordUpdateWidget.completer)
    WordUpdateWidget.completer.setModel(model)

  def update_word(self):
    is_invalid, text = self.word_is_invalid()

    if is_invalid:
      self.error_message_label.setText(text)
      self.error_message_label.show()
      return

    self.check_boxes_modified = []
    self.save_button.setDisabled(True)

    subjects_names = []
    for check_box in self.check_boxes:
      if check_box.isChecked():
        subjects_names.append(check_box.text())

    subjects_to_remove = list(set(self.word_subjects) - set(subjects_names))
    subjects_to_add = list(set(subjects_names) - set(self.word_subjects))
    self.word_subjects = subjects_names

    new_word = self.word_line_edit.text()
    grade_id = self.grade_selector.currentIndex() + 1

    from search.current_search import CurrentSearch

    if (len(subjects_to_remove) > 0 and
        grade_id == CurrentSearch.grade_id and
        CurrentSearch.last_subject_picked in subjects_to_remove):

      CurrentSearch.remove_searched_word(self.searched_word)

      from side.recent_searches_widget import RecentSearchesWidget
      RecentSearchesWidget.delete_word(self.searched_word)

      from side.starred_words_widget import StarredWordsWidget
      StarredWordsWidget.delete_word(self.searched_word)

      from central.results_widget import ResultsWidget
      ResultsWidget.delete_word(self.searched_word)

    update_word(self.searched_word, new_word, grade_id, subjects_to_add, subjects_to_remove)

    if self.searched_word != new_word:
      if grade_id == CurrentSearch.grade_id:
        CurrentSearch.update_searched_word(self.searched_word, new_word)

        from side.recent_searches_widget import RecentSearchesWidget
        RecentSearchesWidget.update_word(self.searched_word, new_word)

        from side.starred_words_widget import StarredWordsWidget
        StarredWordsWidget.update_word(self.searched_word, new_word)

        from central.results_widget import ResultsWidget
        ResultsWidget.update_word(self.searched_word, new_word)

      self.word_selection_line_edit.setText(new_word)

      self.update_dictionary_words(self.searched_word, new_word)

      from dialogs.word_family_update_widget import WordFamilyUpdateWidget
      WordFamilyUpdateWidget.update_dictionary_words(
        word_to_remove=self.searched_word, word_to_add=new_word, grade_id=grade_id
      )

      from dialogs.word_editing_widget import WordEditingWidget
      WordEditingWidget.update_word_family_update_widget(self.searched_word, grade_id)

      self.searched_word = new_word

  def delete_word(self):
    if not Settings.get_boolean_setting('hide_delete_word_message'):
      if not self.get_permission_to_delete():
        return

    self.save_button.setDisabled(True)
    self.delete_button.setDisabled(True)

    grade_id = self.grade_selector.currentIndex() + 1

    WordUpdateWidget.dictionary_words.remove(self.searched_word)
    model = QStringListModel(WordUpdateWidget.dictionary_words, WordUpdateWidget.completer)
    WordUpdateWidget.completer.setModel(model)
    from dialogs.word_family_update_widget import WordFamilyUpdateWidget
    WordFamilyUpdateWidget.update_dictionary_words(
      word_to_remove=self.searched_word, grade_id=grade_id
    )

    from search.current_search import CurrentSearch
    if grade_id == CurrentSearch.grade_id:
      CurrentSearch.remove_searched_word(self.searched_word)

      from side.recent_searches_widget import RecentSearchesWidget
      RecentSearchesWidget.delete_word(self.searched_word)

      from side.starred_words_widget import StarredWordsWidget
      StarredWordsWidget.delete_word(self.searched_word)

      from central.results_widget import ResultsWidget
      ResultsWidget.delete_word(self.searched_word)

    self.word_widget.hide()
    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    self.check_boxes = []
    destroy_word(self.searched_word, [self.grade_selector.currentIndex() + 1])

    QTimer.singleShot(0, self.word_selection_line_edit.clear)
    self.word_selection_line_edit.setFocus()

    from dialogs.word_editing_widget import WordEditingWidget
    WordEditingWidget.update_word_family_update_widget(self.searched_word, grade_id)

  def check_box_modified(self, text):
    if text in self.check_boxes_modified:
      self.check_boxes_modified.remove(text)
    else:
      self.check_boxes_modified.append(text)

    self.update_save_button_state()

  def update_save_button_state(self):
    fields_non_empty = len(self.word_line_edit.text()) > 0 and self.selected_check_box_exists()

    if fields_non_empty and (len(self.check_boxes_modified) or
       self.word_line_edit.text() != self.searched_word):
      self.save_button.setEnabled(True)
    else:
      self.save_button.setDisabled(True)

  def selected_check_box_exists(self):
    for check_box in self.check_boxes:
      if check_box.isChecked():
        return True

    return False

  def word_is_invalid(self):
    word = self.word_line_edit.text()

    if len(word) > WordUpdateWidget.MAXIMUM_NAME_LENGTH:
      return True, _('WORD_LENGTH_EXCEEDS_LIMIT_TEXT')

    if self.searched_word != word and word_exists(self.grade_selector.currentIndex() + 1, word):
      return True, _('WORD_EXISTS_TEXT')

    for character in word:
      if not character in WordUpdateWidget.GREEK_CHARACTERS:
        return True, _('ONLY_GREEK_CHARACTERS_ALLOWED_TEXT')

    return False, ''

  def get_permission_to_delete(self):
    title = _('DELETE_WORD_BUTTON_TEXT')
    question = _('DELETE_WORD_PERMISSION')

    answer = QMessageBox(self)
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(question)
    answer.setWindowTitle(title)

    yes_button = answer.addButton(_('YES'), QMessageBox.ButtonRole.YesRole)
    cancel_button = answer.addButton(_('CANCEL'), QMessageBox.ButtonRole.RejectRole)

    answer.setDefaultButton(cancel_button)

    check_box = QCheckBox(_('HIDE_MESSAGE_CHECKBOX'))
    check_box.clicked.connect(self.toggle_message_setting)
    check_box.setChecked(False)

    answer.setCheckBox(check_box)
    answer.exec()

    if answer.clickedButton() == yes_button:
      return True

    return False

  @staticmethod
  def toggle_message_setting(value):
    Settings.set_boolean_setting('hide_delete_word_message', value)
