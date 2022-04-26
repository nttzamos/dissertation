from PyQt6.QtWidgets import (QGridLayout, QVBoxLayout, QHBoxLayout, QWidget,
                             QLineEdit, QLabel, QGroupBox, QScrollArea,
                             QCheckBox, QPushButton, QComboBox, QSizePolicy)
from PyQt6.QtCore import QTimer, Qt

from menu.settings import Settings
from models.word import create_word, word_exists
from shared.database_handler import get_grades, get_grade_subjects
from shared.font_settings import FontSettings
from shared.spacer import Spacer

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class WordAdditionWIdget(QWidget):
  MAXIMUM_NAME_LENGTH = 20
  GREEK_CHARACTERS = [
    'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο',
    'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω', 'ς', 'ά', 'έ', 'ί', 'ή', 'ύ',
    'ό', 'ώ', 'ϊ', 'ϋ', 'ΐ', 'ΰ']

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 0, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = FontSettings.get_font('heading')
    text_font = FontSettings.get_font('text')
    button_font = FontSettings.get_font('button')
    error_message_font = FontSettings.get_font('error')

    self.success_label = QLabel(_('SUCCESS_SAVING_WORD_TEXT'))
    self.success_label.setFont(text_font)
    size_policy = self.success_label.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    self.success_label.setSizePolicy(size_policy)
    self.success_label.hide()
    self.success_label.setStyleSheet('QLabel { color: green }')

    word_widget = QGroupBox(_('WORD_TEXT'))
    word_widget.setFont(section_label_font)
    word_widget.layout = QVBoxLayout(word_widget)
    word_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.word_line_edit = QLineEdit()
    self.word_line_edit.setFont(text_font)
    self.word_line_edit.textChanged.connect(self.update_save_button_state)

    self.error_message_label = QLabel(self)
    self.error_message_label.setFont(error_message_font)
    self.word_line_edit.textChanged.connect(self.error_message_label.hide)
    self.error_message_label.hide()

    word_widget.layout.addWidget(self.word_line_edit)
    word_widget.layout.addWidget(self.error_message_label)

    grade_selection_widget = QGroupBox(_('GRADE_SELECTION_TEXT'))
    grade_selection_widget.setFont(section_label_font)
    grade_selection_widget.layout = QHBoxLayout(grade_selection_widget)
    grade_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.grade_selector = QComboBox()
    self.grade_selector.setFont(text_font)
    self.grade_selector.addItems(get_grades())
    self.grade_selector.activated.connect(self.grade_selector_activated)

    grade_selection_widget.layout.addWidget(self.grade_selector)

    subjects_widget = QGroupBox(_('SUBJECT_SELECTION_TEXT'))
    subjects_widget.setFont(section_label_font)
    subjects_widget.layout = QHBoxLayout(subjects_widget)
    subjects_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.subjects_selection_widget = QWidget()
    self.subjects_selection_widget.layout = QGridLayout(self.subjects_selection_widget)
    self.subjects_selection_widget.setSizePolicy(
      QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
    )

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(self.subjects_selection_widget)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    grade_subjects = get_grade_subjects(1)

    self.check_boxes = []
    self.check_boxes_selected = []
    for i in range(len(grade_subjects)):
      check_box = QCheckBox(grade_subjects[i])
      check_box.clicked.connect(lambda ch, i=i: self.check_box_modified(grade_subjects[i]))
      check_box.setFont(text_font)
      self.check_boxes.append(check_box)
      self.subjects_selection_widget.layout.addWidget(check_box, i, 0)

    self.subjects_selection_widget.layout.addWidget(Spacer(), 1000, 0)

    subjects_widget.layout.addWidget(scroll_area)

    self.save_button = QPushButton(_('SAVE_WORD_BUTTON_TEXT'))
    self.save_button.setFont(button_font)
    self.save_button.pressed.connect(self.save_word)
    self.save_button.setAutoDefault(False)
    self.save_button.setDisabled(True)

    self.select_all_button = QPushButton(_('SELECT_ALL_SUBJECTS_TEXT'))
    self.select_all_button.setFont(button_font)
    self.select_all_button.pressed.connect(self.select_all)
    self.select_all_button.setAutoDefault(False)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.addWidget(self.select_all_button, alignment=Qt.AlignmentFlag.AlignLeft)
    buttons_widget.layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

    self.layout.addWidget(self.success_label, alignment=Qt.AlignmentFlag.AlignRight)
    self.layout.addWidget(word_widget)
    self.layout.addWidget(grade_selection_widget)
    self.layout.addWidget(subjects_widget)
    self.layout.addSpacing(10)
    self.layout.addWidget(buttons_widget)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.error_message_label.setStyleSheet(Styles.error_message_label_style)
    self.save_button.setStyleSheet(Styles.result_dialog_style)
    self.select_all_button.setStyleSheet(Styles.result_dialog_style)

  def grade_selector_activated(self, index):
    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    grade_subjects = get_grade_subjects(index + 1)

    self.save_button.setDisabled(True)

    text_font = FontSettings.get_font('text')
    self.check_boxes = []
    self.check_boxes_selected = []
    for i in range(len(grade_subjects)):
      check_box = QCheckBox(grade_subjects[i])
      check_box.clicked.connect(lambda ch, i=i: self.check_box_modified(grade_subjects[i]))
      check_box.setFont(text_font)
      self.check_boxes.append(check_box)
      self.subjects_selection_widget.layout.addWidget(check_box, i, 0)

  def save_word(self):
    is_invalid, text = self.word_is_invalid()

    if is_invalid:
      self.error_message_label.setText(text)
      self.error_message_label.show()
      return

    word = self.word_line_edit.text().strip()
    QTimer.singleShot(0, self.word_line_edit.clear)
    self.check_boxes_selected = []

    subjects = []
    for check_box in self.check_boxes:
      if check_box.isChecked():
        subjects.append(check_box.text())
        check_box.setChecked(False)

    grade_id = self.grade_selector.currentIndex() + 1
    create_word(word, grade_id, subjects)

    from central.results_widget import ResultsWidget
    ResultsWidget.add_word(word)

    from dialogs.word_update_widget import WordUpdateWidget
    WordUpdateWidget.add_word_to_dictionary(grade_id, word)

    from dialogs.word_family_update_widget import WordFamilyUpdateWidget
    WordFamilyUpdateWidget.update_dictionary_words(word_to_add=word, grade_id=grade_id)

    self.success_label.show()
    QTimer.singleShot(3500, self.success_label.hide)

  def select_all(self):
    self.check_boxes_selected = []

    for check_box in self.check_boxes:
      check_box.setChecked(True)
      self.check_boxes_selected.append(check_box.text())

    self.update_save_button_state()

  def check_box_modified(self, text):
    if text in self.check_boxes_selected:
      self.check_boxes_selected.remove(text)
    else:
      self.check_boxes_selected.append(text)

    self.update_save_button_state()

  def update_save_button_state(self):
    if len(self.word_line_edit.text()) > 0 and len(self.check_boxes_selected) > 0:
      self.save_button.setEnabled(True)
    else:
      self.save_button.setDisabled(True)

  def word_is_invalid(self):
    word = self.word_line_edit.text().strip()

    if len(word) > WordAdditionWIdget.MAXIMUM_NAME_LENGTH:
      return True, _('WORD_LENGTH_EXCEEDS_LIMIT_TEXT')

    if word_exists(self.grade_selector.currentIndex() + 1, word):
      return True, _('WORD_EXISTS_TEXT')

    for character in word:
      if not character in WordAdditionWIdget.GREEK_CHARACTERS:
        return True, _('ONLY_GREEK_CHARACTERS_ALLOWED_TEXT')

    return False, ''
