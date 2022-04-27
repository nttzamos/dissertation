from PyQt6.QtWidgets import (QGridLayout, QVBoxLayout, QHBoxLayout, QWidget,
                             QLineEdit, QLabel, QGroupBox, QScrollArea,
                             QCheckBox, QPushButton, QComboBox, QSizePolicy,
                             QMessageBox)
from PyQt6.QtCore import QTimer, Qt

from menu.settings import Settings
from models.profile import create_profile, profile_name_exists
from shared.database_handler import get_grades, get_grade_subjects
from shared.font_settings import FontSettings
from shared.spacer import Spacer

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class ProfileAdditionWIdget(QWidget):
  MAXIMUM_NAME_LENGTH = 20

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 0, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = FontSettings.get_font('heading')
    text_font = FontSettings.get_font('text')
    button_font = FontSettings.get_font('button')
    error_message_font = FontSettings.get_font('error')

    self.success_label = QLabel(_('SUCCESS_SAVING_PROFILE_TEXT'))
    self.success_label.setFont(text_font)
    size_policy = self.success_label.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    self.success_label.setSizePolicy(size_policy)
    self.success_label.hide()
    self.success_label.setStyleSheet('QLabel { color: green }')

    name_widget = QGroupBox(_('PROFILE_NAME_TEXT'))
    name_widget.setFont(section_label_font)
    name_widget.layout = QVBoxLayout(name_widget)
    name_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.name_line_edit = QLineEdit()
    self.name_line_edit.setFont(text_font)
    self.name_line_edit.textChanged.connect(self.update_save_button_state)

    self.error_message_label = QLabel(self)
    self.error_message_label.setFont(error_message_font)
    self.name_line_edit.textChanged.connect(self.error_message_label.hide)
    self.error_message_label.hide()

    name_widget.layout.addWidget(self.name_line_edit)
    name_widget.layout.addWidget(self.error_message_label)

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

    self.save_button = QPushButton(_('SAVE_PROFILE_BUTTON_TEXT'))
    self.save_button.setFont(button_font)
    self.save_button.pressed.connect(self.save_profile)
    self.save_button.setAutoDefault(False)
    self.save_button.setDisabled(True)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

    self.layout.addWidget(self.success_label, alignment=Qt.AlignmentFlag.AlignRight)
    self.layout.addWidget(name_widget)
    self.layout.addWidget(grade_selection_widget)
    self.layout.addWidget(subjects_widget)
    self.layout.addSpacing(10)
    self.layout.addWidget(buttons_widget)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.error_message_label.setStyleSheet(Styles.error_message_label_style)
    self.save_button.setStyleSheet(Styles.dialog_button_style)

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

  def save_profile(self):
    is_invalid, text = self.profile_is_invalid()

    if is_invalid:
      if text == self.construct_redundant_profile_message():
        title = _('ERROR_SAVING_PROFILE_TEXT')
        QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      else:
        self.error_message_label.setText(text)
        self.error_message_label.show()

      return

    profile_name = self.name_line_edit.text()
    QTimer.singleShot(0, self.name_line_edit.clear)
    self.check_boxes_selected = []

    subjects = []
    for check_box in self.check_boxes:
      if check_box.isChecked():
        subjects.append(check_box.text())
        check_box.setChecked(False)

    create_profile(profile_name, self.grade_selector.currentIndex() + 1, subjects)

    from dialogs.profile_update_widget import ProfileUpdateWidget
    ProfileUpdateWidget.add_profile(profile_name)

    from dialogs.student_addition_widget import StudentAdditionWidget
    StudentAdditionWidget.add_profile(profile_name)

    from dialogs.student_update_widget import StudentUpdateWidget
    StudentUpdateWidget.add_profile(profile_name)

    from dialogs.data_editing_widget import DataEditingWidget
    DataEditingWidget.update_student_update_widget()

    self.success_label.show()
    QTimer.singleShot(3500, self.success_label.hide)

  def check_box_modified(self, text):
    if text in self.check_boxes_selected:
      self.check_boxes_selected.remove(text)
    else:
      self.check_boxes_selected.append(text)

    self.update_save_button_state()

  def update_save_button_state(self):
    if len(self.name_line_edit.text()) > 0 and len(self.check_boxes_selected) > 0:
      self.save_button.setEnabled(True)
    else:
      self.save_button.setDisabled(True)

  def profile_is_invalid(self):
    profile_name = self.name_line_edit.text()

    if len(profile_name) > ProfileAdditionWIdget.MAXIMUM_NAME_LENGTH:
      return True, _('PROFILE_NAME_LENGTH_EXCEEDS_LIMIT_TEXT')

    if profile_name_exists(profile_name):
      return True, _('PROFILE_NAME_EXISTS_TEXT')

    for check_box in self.check_boxes:
      if not check_box.isChecked():
        return False, ''

    return True, self.construct_redundant_profile_message()

  def construct_redundant_profile_message(self):
    return _('REDUNDANT_PROFILE_MESSAGE') + self.grade_selector.currentText()
