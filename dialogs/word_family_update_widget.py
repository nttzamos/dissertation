from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QGroupBox, QListWidget, QPushButton, QComboBox, QCompleter, QAbstractItemView
from PyQt6.QtCore import Qt, QTimer, QStringListModel
from PyQt6.QtGui import QFont

from shared.database_handler import get_grades, get_grade_words
from models.family import get_word_id, get_family_id, get_family_words, update_word_family
from menu.settings import Settings

class WordFamilyUpdateWidget(QWidget):
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

    WordFamilyUpdateWidget.grade_selector = QComboBox()
    WordFamilyUpdateWidget.grade_selector.setFont(combo_box_font)
    WordFamilyUpdateWidget.grade_selector.addItems(grades)
    WordFamilyUpdateWidget.grade_selector.activated.connect(self.grade_selector_activated)

    grade_selection_widget.layout.addWidget(WordFamilyUpdateWidget.grade_selector)

    word_selection_widget = QGroupBox('Word Selection')
    word_selection_widget.setFont(section_label_font)
    word_selection_widget.layout = QVBoxLayout(word_selection_widget)
    word_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.word_selection_line_edit = QLineEdit()
    self.word_selection_line_edit.setFont(line_edit_font)
    self.word_selection_line_edit.returnPressed.connect(self.word_selected)
    WordFamilyUpdateWidget.dictionary_words = get_grade_words(1)
    WordFamilyUpdateWidget.completer = QCompleter(WordFamilyUpdateWidget.dictionary_words)
    WordFamilyUpdateWidget.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    WordFamilyUpdateWidget.completer.popup().setFont(completer_font)
    self.word_selection_line_edit.setCompleter(WordFamilyUpdateWidget.completer)
    self.word_selection_line_edit.setPlaceholderText('Please enter a word.')
    self.error_message_label = QLabel('Please search for another word', self)
    self.error_message_label.setFont(error_message_font)
    self.word_selection_line_edit.textChanged.connect(self.error_message_label.hide)
    self.error_message_label.hide()

    word_selection_widget.layout.addWidget(self.word_selection_line_edit)
    word_selection_widget.layout.addWidget(self.error_message_label)

    word_family_selection_widget = QGroupBox('Family Selection')
    word_family_selection_widget.setFont(section_label_font)
    word_family_selection_widget.layout = QVBoxLayout(word_family_selection_widget)
    word_family_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.related_word_selection_line_edit = QLineEdit()
    self.related_word_selection_line_edit.setFont(line_edit_font)
    self.related_word_selection_line_edit.returnPressed.connect(self.related_word_selected)
    self.related_word_selection_line_edit.setCompleter(WordFamilyUpdateWidget.completer)
    self.related_word_selection_line_edit.setPlaceholderText('Select a word to be added.')
    self.related_word_selection_line_edit.hide()

    self.word_family_list = QListWidget()
    self.word_family_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    self.remove_words_button = QPushButton('Remove Selected Words')
    self.remove_words_button.pressed.connect(self.remove_selected_words)

    word_family_selection_widget.layout.addWidget(self.related_word_selection_line_edit)
    word_family_selection_widget.layout.addSpacing(5)
    word_family_selection_widget.layout.addWidget(self.word_family_list)
    word_family_selection_widget.layout.addSpacing(5)
    word_family_selection_widget.layout.addWidget(self.remove_words_button, alignment=Qt.AlignmentFlag.AlignRight)


    self.save_button = QPushButton('Save Family')
    self.save_button.pressed.connect(self.update_family)
    self.save_button.setDisabled(True)

    self.layout.addWidget(grade_selection_widget)
    self.layout.addWidget(word_selection_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(word_family_selection_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

    self.style()

  def style(self):
    from shared.styles import Styles
    # self.setStyleSheet(Styles.words_editing_widget_style)
    self.error_message_label.setStyleSheet(Styles.error_message_label_style)

  def grade_selector_activated(self, index):
    WordFamilyUpdateWidget.dictionary_words = get_grade_words(index + 1)
    model = QStringListModel(WordFamilyUpdateWidget.dictionary_words, WordFamilyUpdateWidget.completer)
    WordFamilyUpdateWidget.completer.setModel(model)
    self.related_word_selection_line_edit.hide()
    self.save_button.setDisabled(True)

  def word_selected(self):
    self.searched_word = self.word_selection_line_edit.text()
    if self.searched_word in WordFamilyUpdateWidget.dictionary_words:
      QTimer.singleShot(0, self.related_word_selection_line_edit.clear)

      grade_id = WordFamilyUpdateWidget.grade_selector.currentIndex() + 1
      word_id = get_word_id(grade_id, self.searched_word)
      family_id = get_family_id(grade_id, word_id)

      self.family_words = get_family_words(grade_id, family_id)
      self.famiy_list = get_family_words(grade_id, family_id)

      if len(self.famiy_list) > 0:
        self.family_words.remove(self.searched_word)
        self.famiy_list.remove(self.searched_word)
        self.related_word_selection_line_edit.show()
        self.related_word_selection_line_edit.setFocus()
        self.save_button.setEnabled(True)
      else:
        self.save_button.setDisabled(True)

      self.word_family_list.clear()
      self.word_family_list.addItems(self.family_words)
    else:
      self.error_message_label.show()

  def related_word_selected(self):
    related_word = self.related_word_selection_line_edit.text()
    if not self.related_word_is_invalid(related_word):
      QTimer.singleShot(0, self.related_word_selection_line_edit.clear)
      self.famiy_list.append(related_word)
      self.word_family_list.addItem(related_word)

  def related_word_is_invalid(self, related_word):
    if related_word == self.searched_word or related_word in self.famiy_list:
      return True

    if not related_word in WordFamilyUpdateWidget.dictionary_words:
      return True

    return False

  def remove_selected_words(self):
    for item in self.word_family_list.selectedItems():
      self.famiy_list.remove(item.text())
      self.word_family_list.takeItem(self.word_family_list.row(item))

  def update_family(self):
    word_list = []
    for i in range(self.word_family_list.count()):
      word_list.append(self.word_family_list.item(i).text())

    words_to_remove = list(set(self.family_words) - set(word_list))
    words_to_add = list(set(word_list) - set(self.family_words))
    self.word_subjects = word_list
    grade_id = WordFamilyUpdateWidget.grade_selector.currentIndex() + 1
    update_word_family(grade_id, self.searched_word, words_to_add, words_to_remove)

  @staticmethod
  def update_dictionary_words(word_to_remove = None, word_to_add = None):
    if word_to_add != None:
      WordFamilyUpdateWidget.dictionary_words.append(word_to_add)

    if word_to_remove != None:
      WordFamilyUpdateWidget.dictionary_words.remove(word_to_remove)
    model = QStringListModel(WordFamilyUpdateWidget.dictionary_words, WordFamilyUpdateWidget.completer)
    WordFamilyUpdateWidget.completer.setModel(model)
