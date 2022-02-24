from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QComboBox, QSizePolicy, QMessageBox
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

from shared.database_handler import get_grades, get_grade_subjects
from menu.settings import Settings
from models.word import create_word, word_exists

class WordAdditionWIdget(QWidget):
  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = QFont(Settings.font, 16)
    combo_box_font = QFont(Settings.font, 14)
    check_box_font = QFont(Settings.font, 14)
    line_edit_font = QFont(Settings.font, 14)

    word_widget = QGroupBox('Word')
    word_widget.setFont(section_label_font)
    word_widget.layout = QHBoxLayout(word_widget)
    word_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.word_line_edit = QLineEdit()
    self.word_line_edit.setFont(line_edit_font)
    word_widget.layout.addWidget(self.word_line_edit)

    grade_selection_widget = QGroupBox('Grade Selection')
    grade_selection_widget.setFont(section_label_font)
    grade_selection_widget.layout = QHBoxLayout(grade_selection_widget)
    grade_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    grades = get_grades()

    self.grade_selector = QComboBox()
    self.grade_selector.setFont(combo_box_font)
    self.grade_selector.addItems(grades)
    self.grade_selector.activated.connect(self.grade_selector_activated)

    grade_selection_widget.layout.addWidget(self.grade_selector)

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

    grade_subjects = get_grade_subjects(1)

    self.check_boxes = []
    for i in range(len(grade_subjects)):
      check_box = QCheckBox(grade_subjects[i])
      check_box.setFont(check_box_font)
      self.check_boxes.append(check_box)
      self.subjects_selection_widget.layout.addWidget(check_box, i, 0)

    vspacer = QLabel('f')
    invisible_font = QFont(Settings.font, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    self.subjects_selection_widget.layout.addWidget(vspacer, 1000, 0)

    subjects_widget.layout.addWidget(scroll_area)

    self.save_button = QPushButton('Save New Word')
    self.save_button.pressed.connect(self.save_word)

    self.layout.addWidget(word_widget)
    self.layout.addWidget(grade_selection_widget)
    self.layout.addWidget(subjects_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.word_addition_style)

  def grade_selector_activated(self, index):
    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    grade_subjects = get_grade_subjects(index + 1)

    check_box_font = QFont(Settings.font, 14)
    self.check_boxes = []
    for i in range(len(grade_subjects)):
      check_box = QCheckBox(grade_subjects[i])
      check_box.setFont(check_box_font)
      self.check_boxes.append(check_box)
      self.subjects_selection_widget.layout.addWidget(check_box, i, 0)

  def save_word(self):
    is_invalid, text = self.word_is_invalid()

    if is_invalid:
      title = 'Error Saving Word'
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    word = self.word_line_edit.text()
    QTimer.singleShot(0, self.word_line_edit.clear)

    subjects = []
    for check_box in self.check_boxes:
      if check_box.isChecked():
        subjects.append(check_box.text())
        check_box.setChecked(False)

    grade_id = self.grade_selector.currentIndex() + 1
    create_word(word, grade_id, subjects)
    from dialogs.word_update_widget import WordUpdateWidget
    WordUpdateWidget.add_word_to_dictionary(grade_id, word)
    from dialogs.word_family_update_widget import WordFamilyUpdateWidget
    WordFamilyUpdateWidget.update_dictionary_words(word_to_add = word)

  def word_is_invalid(self):
    word = self.word_line_edit.text()
    if len(word) == 0:
      return True, 'Word can not be saved because it is empty.'

    if word_exists(self.grade_selector.currentIndex() + 1, word):
      return True, 'Word can not be saved as it already exists.'

    for check_box in self.check_boxes:
      if check_box.isChecked():
        return False, ''

    return True, 'Word can not be saved because none of the grade subjects have been selected.'
