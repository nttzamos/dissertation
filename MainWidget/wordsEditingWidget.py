from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QComboBox, QDialog, QLabel, QCompleter, QCheckBox, QRadioButton, QWidget, QHBoxLayout, QMessageBox, QGroupBox
from PyQt6.QtCore import QStringListModel, QTimer, Qt
from PyQt6.QtGui import QFont, QIcon

from MenuBar.settings import Settings
from Common.databaseHandler import DBHandler

class WordsEditingWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Edit Dictionary Words')
    self.setWindowIcon(QIcon('Resources/windowIcon.svg'))

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 0, 20, 15)
    self.layout.setSpacing(0)

    label_font = QFont(Settings.font, 12)
    combo_box_font = QFont(Settings.font, 14)
    radio_button_font = QFont(Settings.font, 14)
    check_box_font = QFont(Settings.font, 14)
    line_edit_font = QFont(Settings.font, 14)
    completer_font = QFont(Settings.font, 12)
    section_label_font = QFont(Settings.font, 16)
    error_message_font = QFont(Settings.font, 10)

    self.grade_selector = QComboBox()
    self.grade_selector.activated.connect(self.update_words_list)
    self.grade_selector.setFont(combo_box_font)
    self.grade_selector.addItems(DBHandler.get_grades())

    grade_selection_widget = QGroupBox('Grade Selection')
    grade_selection_widget.setFont(section_label_font)
    grade_selection_widget.layout = QVBoxLayout(grade_selection_widget)
    grade_selection_widget.layout.setContentsMargins(10, 10, 10, 10)
    grade_selection_widget.layout.addWidget(self.grade_selector)

    self.update_selection_button = QRadioButton('Update Word')
    self.update_selection_button.setFont(radio_button_font)
    self.deletion_selection_button = QRadioButton('Delete Word')
    self.deletion_selection_button.setFont(radio_button_font)
    if Settings.get_setting('default_editing_action') == 'update':
      self.update_selection_button.setChecked(True)
    else:
      self.deletion_selection_button.setChecked(True)

    self.update_selection_button.toggled.connect(self.update_button_toggled)
    self.deletion_selection_button.toggled.connect(self.delete_button_toggled)

    action_selection_buttons = QWidget()
    action_selection_buttons.layout = QHBoxLayout(action_selection_buttons)
    action_selection_buttons.layout.setContentsMargins(0, 0, 0, 0)
    action_selection_buttons.layout.addWidget(self.update_selection_button)
    action_selection_buttons.layout.addWidget(self.deletion_selection_button)

    action_selection_widget = QGroupBox('Action Selection')
    action_selection_widget.setFont(section_label_font)
    action_selection_widget.layout = QVBoxLayout(action_selection_widget)
    action_selection_widget.layout.setContentsMargins(10, 10, 10, 10)
    action_selection_widget.layout.addWidget(action_selection_buttons)

    self.update_all_grades = QCheckBox('Update/Delete word for all grades?')
    self.update_all_grades.setFont(check_box_font)

    self.show_candidates = QCheckBox('Show only candidate words for update/deletion?')
    self.show_candidates.setFont(check_box_font)
    self.show_candidates.toggled.connect(self.update_words_list)

    parameters_configuration_widget = QGroupBox('Parameter Configuration')
    parameters_configuration_widget.setFont(section_label_font)
    parameters_configuration_widget.layout = QVBoxLayout(parameters_configuration_widget)
    parameters_configuration_widget.layout.setContentsMargins(10, 10, 10, 10)
    parameters_configuration_widget.layout.addWidget(self.update_all_grades)
    parameters_configuration_widget.layout.addWidget(self.show_candidates)

    word_selection_label = QLabel('Word Selection')
    word_selection_label.setFont(label_font)
    self.word_selection_line_edit = QLineEdit()
    self.word_selection_line_edit.setFont(line_edit_font)
    self.word_selection_line_edit.returnPressed.connect(self.word_selected)
    self.dictionary_words = DBHandler.get_grade_words(1)
    self.completer = QCompleter(self.dictionary_words)
    self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    self.completer.popup().setFont(completer_font)
    self.word_selection_line_edit.setCompleter(self.completer)
    self.word_selection_line_edit.setPlaceholderText('Please enter a word.')
    self.word_selection_line_edit.textChanged.connect(self.search_text_changed)
    self.error_message_label = QLabel('Please search for another word', self)
    self.error_message_label.setFont(error_message_font)
    size_policy = self.error_message_label.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    self.error_message_label.setSizePolicy(size_policy)
    self.show_error_message = False

    self.update_word_widget = QWidget()
    self.update_word_widget.layout = QVBoxLayout(self.update_word_widget)
    self.update_word_widget.layout.setContentsMargins(0, 0, 0, 0)
    update_form_label = QLabel('Editing Form')
    update_form_label.setFont(label_font)
    self.word_editing_line_edit = QLineEdit()
    self.word_editing_line_edit.setFont(line_edit_font)
    self.word_editing_line_edit.returnPressed.connect(self.update_word_confirmation)
    self.word_editing_line_edit.setPlaceholderText('You have to select a word first.')
    self.word_editing_line_edit.setDisabled(True)
    self.update_word_widget.layout.setSpacing(5)
    self.update_word_widget.layout.addWidget(update_form_label)
    self.update_word_widget.layout.addWidget(self.word_editing_line_edit)

    word_editing_widget = QGroupBox('Word Editing')
    word_editing_widget.setFont(section_label_font)
    word_editing_widget.layout = QVBoxLayout(word_editing_widget)
    word_editing_widget.layout.setContentsMargins(10, 10, 10, 10)
    word_editing_widget.layout.setSpacing(0)
    word_editing_widget.layout.addWidget(word_selection_label)
    word_editing_widget.layout.addSpacing(5)
    word_editing_widget.layout.addWidget(self.word_selection_line_edit)
    word_editing_widget.layout.addWidget(self.error_message_label, alignment=Qt.AlignmentFlag.AlignRight)
    self.error_message_label.hide()
    word_editing_widget.layout.addWidget(self.update_word_widget)
    if self.deletion_selection_button.isChecked():
      self.update_word_widget.hide()

    self.layout.addWidget(grade_selection_widget)
    self.layout.addSpacing(15)

    self.layout.addWidget(action_selection_widget)
    self.layout.addSpacing(15)

    self.layout.addWidget(parameters_configuration_widget)
    self.layout.addSpacing(15)

    self.layout.addWidget(word_editing_widget)

    self.word_selection_line_edit.setFocus()

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.words_editing_widget_style)
    self.error_message_label.setStyleSheet(Styles.error_message_labelStyle)

  def word_selected(self):
    self.searched_word = self.word_selection_line_edit.text()
    if self.searched_word in self.dictionary_words:
      if self.update_selection_button.isChecked():
        self.word_editing_line_edit.setText(self.searched_word)
        self.word_editing_line_edit.setEnabled(True)
        self.word_editing_line_edit.setFocus()
      elif self.deletion_selection_button.isChecked():
        self.delete_word_confirmation()
    else:
      self.show_error_message = True
      self.error_message_label.show()

  def search_text_changed(self):
    if self.show_error_message:
      self.show_error_message = False
      self.error_message_label.hide()

  def update_word_confirmation(self):
    if Settings.get_boolean_setting('ask_before_actions'):
      new_word = self.word_editing_line_edit.text()
      title = 'Update Word'
      question = "Are you sure you want to update '" + self.searched_word + "' to '" + new_word + "'?"
      answer = QMessageBox.question(self, title, question, QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
      if answer == QMessageBox.StandardButton.Yes:
        self.update_word()
    else:
      self.update_word()

  def update_words_list(self, unusedVariable):
    if self.show_candidates.isChecked():
      self.dictionary_words = DBHandler.get_candidate_words(self.grade_selector.currentIndex() + 1)
    else:
      self.dictionary_words = DBHandler.get_grade_words(self.grade_selector.currentIndex() + 1)

    model = QStringListModel(self.dictionary_words, self.completer)
    self.completer.setModel(model)

  def update_word(self):
    new_word = self.word_editing_line_edit.text()
    DBHandler.update_word(self.searched_word, new_word, self.get_grades())
    self.update_dictionary_words(self.searched_word, new_word)
    QTimer.singleShot(0, self.word_selection_line_edit.clear)
    QTimer.singleShot(0, self.word_editing_line_edit.clear)
    self.word_editing_line_edit.setDisabled(True)
    self.word_selection_line_edit.setFocus()

  def delete_word_confirmation(self):
    if Settings.get_boolean_setting('ask_before_actions'):
      title = 'Delete Word'
      question = "Are you sure you want to delete '" + self.searched_word + "'?"
      answer = QMessageBox.question(self, title, question, QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
      if answer == QMessageBox.StandardButton.Yes:
        self.delete_word()
    else:
      self.delete_word()

  def delete_word(self):
    DBHandler.delete_word(self.searched_word, self.get_grades())
    self.update_dictionary_words(self.searched_word)
    QTimer.singleShot(0, self.word_selection_line_edit.clear)

  def delete_button_toggled(self):
    if self.deletion_selection_button.isChecked():
      QTimer.singleShot(0, self.word_editing_line_edit.clear)
      self.word_editing_line_edit.setDisabled(True)
      self.update_word_widget.hide()

  def update_button_toggled(self):
    if self.update_selection_button.isChecked():
      self.update_word_widget.show()

  def get_grades(self):
    grades = []
    if self.update_all_grades.isChecked():
      grades = list(range(1, 7))
    else:
      grades.append(self.grade_selector.currentIndex() + 1)

    return grades

  def update_dictionary_words(self, oldWord, new_word=None):
    if not (new_word == None or new_word in self.dictionary_words or self.show_candidates.isChecked()):
      self.dictionary_words.append(new_word)

    self.dictionary_words.remove(oldWord)
    model = QStringListModel(self.dictionary_words, self.completer)
    self.completer.setModel(model)
