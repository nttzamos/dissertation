from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QComboBox, QSizePolicy, QMessageBox, QCompleter
from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtGui import QFont

from menu.settings import Settings

from shared.database_handler import get_grades, get_grade_words, get_grade_subjects
from models.word import get_word_subjects, word_exists, update_word, destroy_word

class WordUpdateWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = QFont(Settings.font, 16)
    combo_box_font = QFont(Settings.font, 14)
    line_edit_font = QFont(Settings.font, 14)
    completer_font = QFont(Settings.font, 12)
    error_message_font = QFont(Settings.font, 10)

    grade_selection_widget = QGroupBox('Grade Selection')
    grade_selection_widget.setFont(section_label_font)
    grade_selection_widget.layout = QHBoxLayout(grade_selection_widget)
    grade_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    grades = get_grades()

    WordUpdateWidget.grade_selector = QComboBox()
    WordUpdateWidget.grade_selector.setFont(combo_box_font)
    WordUpdateWidget.grade_selector.addItems(grades)
    WordUpdateWidget.grade_selector.activated.connect(self.grade_selector_activated)

    grade_selection_widget.layout.addWidget(WordUpdateWidget.grade_selector)

    word_selection_widget = QGroupBox('Word Selection')
    word_selection_widget.setFont(section_label_font)
    word_selection_widget.layout = QVBoxLayout(word_selection_widget)
    word_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.word_selection_line_edit = QLineEdit()
    self.word_selection_line_edit.setFont(line_edit_font)
    self.word_selection_line_edit.returnPressed.connect(self.word_selected)
    WordUpdateWidget.dictionary_words = get_grade_words(1)
    WordUpdateWidget.completer = QCompleter(WordUpdateWidget.dictionary_words)
    WordUpdateWidget.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    WordUpdateWidget.completer.popup().setFont(completer_font)
    self.word_selection_line_edit.setCompleter(WordUpdateWidget.completer)
    self.word_selection_line_edit.setPlaceholderText('Please enter a word.')
    self.error_message_label = QLabel('Please search for another word', self)
    self.error_message_label.setFont(error_message_font)
    self.word_selection_line_edit.textChanged.connect(self.error_message_label.hide)
    self.error_message_label.hide()

    word_selection_widget.layout.addWidget(self.word_selection_line_edit)
    word_selection_widget.layout.addWidget(self.error_message_label)

    self.word_widget = QGroupBox('Word')
    self.word_widget.setFont(section_label_font)
    self.word_widget.layout = QHBoxLayout(self.word_widget)
    self.word_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.word_line_edit = QLineEdit()
    self.word_line_edit.setFont(line_edit_font)
    self.word_widget.layout.addWidget(self.word_line_edit)
    self.word_widget.hide()

    subjects_widget = QGroupBox('Subject Selection')
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
    invisible_font = QFont(Settings.font, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    self.subjects_selection_widget.layout.addWidget(vspacer, 1000, 0)

    subjects_widget.layout.addWidget(scroll_area)

    self.save_button = QPushButton('Update Existing Word')
    self.save_button.pressed.connect(self.update_word)
    self.save_button.setDisabled(True)

    self.delete_button = QPushButton('Delete Word')
    self.delete_button.pressed.connect(self.delete_word)
    self.delete_button.setDisabled(True)

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
    # self.setStyleSheet(Styles.words_editing_widget_style)
    self.error_message_label.setStyleSheet(Styles.error_message_label_style)

  def word_selected(self):
    self.searched_word = self.word_selection_line_edit.text()
    if self.searched_word in WordUpdateWidget.dictionary_words:
      self.word_widget.show()
      self.word_line_edit.setText(self.searched_word)
      self.word_line_edit.setFocus()
      self.save_button.setEnabled(True)
      self.delete_button.setEnabled(True)

      for check_box in self.check_boxes:
        self.subjects_selection_widget.layout.removeWidget(check_box)

      grade_subjects = get_grade_subjects(WordUpdateWidget.grade_selector.currentIndex() + 1)
      self.word_subjects = get_word_subjects(WordUpdateWidget.grade_selector.currentIndex() + 1, self.searched_word)

      check_box_font = QFont(Settings.font, 14)
      self.check_boxes = []
      for i in range(len(grade_subjects)):
        check_box = QCheckBox(grade_subjects[i])
        check_box.setFont(check_box_font)
        if grade_subjects[i] in self.word_subjects: check_box.setChecked(True)

        self.check_boxes.append(check_box)
        self.subjects_selection_widget.layout.addWidget(check_box, i, 0)
    else:
      self.error_message_label.show()

  def grade_selector_activated(self, index):
    WordUpdateWidget.dictionary_words = get_grade_words(index + 1)
    model = QStringListModel(WordUpdateWidget.dictionary_words, WordUpdateWidget.completer)
    WordUpdateWidget.completer.setModel(model)
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
      title = 'Error Updating Word'
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    subjects_names = []
    for check_box in self.check_boxes:
      if check_box.isChecked():
        subjects_names.append(check_box.text())

    subjects_to_remove = list(set(self.word_subjects) - set(subjects_names))
    subjects_to_add = list(set(subjects_names) - set(self.word_subjects))
    self.word_subjects = subjects_names

    new_word = self.word_line_edit.text()
    grade_id = self.grade_selector.currentIndex() + 1
    if self.searched_word != new_word:
      self.update_dictionary_words(self.searched_word, new_word)
      from dialogs.word_family_update_widget import WordFamilyUpdateWidget
      WordFamilyUpdateWidget.update_dictionary_words(self.searched_word, new_word)

    update_word(self.searched_word, new_word, grade_id, subjects_to_add, subjects_to_remove)

  def delete_word(self):
    word = self.word_line_edit.text()
    WordUpdateWidget.dictionary_words.remove(word)
    model = QStringListModel(WordUpdateWidget.dictionary_words, WordUpdateWidget.completer)
    WordUpdateWidget.completer.setModel(model)
    from dialogs.word_family_update_widget import WordFamilyUpdateWidget
    WordFamilyUpdateWidget.update_dictionary_words(word_to_remove = self.searched_word)

    self.word_widget.hide()
    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    self.check_boxes = []
    destroy_word(word, [self.grade_selector.currentIndex() + 1])

  def word_is_invalid(self):
    word = self.word_line_edit.text()
    if len(word) == 0:
      return True, 'Word can not be saved because it is empty.'

    if self.searched_word != word and word_exists(self.grade_selector.currentIndex() + 1, word):
      return True, 'Word can not be saved as it already exists.'

    for check_box in self.check_boxes:
      if check_box.isChecked():
        return False, ''

    return True, 'Word can not be saved because none of the grade subjects have been selected.'
