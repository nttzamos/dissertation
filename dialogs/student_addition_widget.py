from PyQt6.QtWidgets import (QGridLayout, QVBoxLayout, QHBoxLayout, QWidget,
                             QLineEdit, QLabel, QGroupBox, QScrollArea,
                             QCheckBox, QPushButton, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from menu.settings import Settings
from models.profile import get_profiles
from models.student import create_student, student_name_exists

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class StudentAdditionWidget(QWidget):
  MAXIMUM_NAME_LENGTH = 20

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 0, 20, 10)
    self.layout.setSpacing(0)

    StudentAdditionWidget.last_index_used = -1

    section_label_font = QFont(Settings.FONT, 16)
    check_box_font = QFont(Settings.FONT, 14)
    line_edit_font = QFont(Settings.FONT, 14)
    label_font = QFont(Settings.FONT, 12)
    error_message_font = QFont(Settings.FONT, 10)

    self.success_label = QLabel(_('SUCCESS_SAVING_STUDENT_TEXT'))
    self.success_label.setFont(label_font)
    size_policy = self.success_label.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    self.success_label.setSizePolicy(size_policy)
    self.success_label.hide()
    self.success_label.setStyleSheet('QLabel { color: green }')

    name_widget = QGroupBox(_('STUDENT_NAME_TEXT'))
    name_widget.setFont(section_label_font)
    name_widget.layout = QVBoxLayout(name_widget)
    name_widget.layout.setContentsMargins(10, 5, 10, 10)

    StudentAdditionWidget.name_line_edit = QLineEdit()
    StudentAdditionWidget.name_line_edit.setFont(line_edit_font)
    StudentAdditionWidget.name_line_edit.textChanged.connect(
      StudentAdditionWidget.update_save_button_state
    )

    self.error_message_label = QLabel(self)
    self.error_message_label.setFont(error_message_font)
    StudentAdditionWidget.name_line_edit.textChanged.connect(self.error_message_label.hide)
    self.error_message_label.hide()

    name_widget.layout.addWidget(StudentAdditionWidget.name_line_edit)
    name_widget.layout.addWidget(self.error_message_label)

    profiles_widget = QGroupBox(_('PROFILE_SELECTION_TEXT'))
    profiles_widget.setFont(section_label_font)
    profiles_widget.layout = QHBoxLayout(profiles_widget)
    profiles_widget.layout.setContentsMargins(10, 5, 10, 10)

    StudentAdditionWidget.profiles_selection_widget = QWidget()
    StudentAdditionWidget.profiles_selection_widget.layout = \
      QGridLayout(StudentAdditionWidget.profiles_selection_widget)

    StudentAdditionWidget.profiles_selection_widget.setSizePolicy(
      QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
    )

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(StudentAdditionWidget.profiles_selection_widget)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    profiles = get_profiles()

    StudentAdditionWidget.check_boxes_selected = []
    StudentAdditionWidget.check_boxes = []
    for i in range(len(profiles)):
      check_box = QCheckBox(profiles[i])
      check_box.clicked.connect(lambda ch, i=i: StudentAdditionWidget.check_box_modified(profiles[i]))
      check_box.setFont(check_box_font)
      StudentAdditionWidget.check_boxes.append(check_box)
      StudentAdditionWidget.profiles_selection_widget.layout.addWidget(check_box, i, 0)
      StudentAdditionWidget.last_index_used = i

    vspacer = QLabel('f')
    invisible_font = QFont(Settings.FONT, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    StudentAdditionWidget.profiles_selection_widget.layout.addWidget(vspacer, 1000, 0)

    profiles_widget.layout.addWidget(scroll_area)

    StudentAdditionWidget.save_button = QPushButton(_('SAVE_STUDENT_BUTTON_TEXT'))
    StudentAdditionWidget.save_button.pressed.connect(self.save_student)
    StudentAdditionWidget.save_button.setAutoDefault(False)
    StudentAdditionWidget.save_button.setDisabled(True)

    select_all_button = QPushButton(_('SELECT_ALL_PROFILES_TEXT'))
    select_all_button.pressed.connect(self.select_all)
    select_all_button.setAutoDefault(False)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.addWidget(select_all_button, alignment=Qt.AlignmentFlag.AlignLeft)
    buttons_widget.layout.addWidget(StudentAdditionWidget.save_button, alignment=Qt.AlignmentFlag.AlignRight)

    self.layout.addWidget(self.success_label, alignment=Qt.AlignmentFlag.AlignRight)
    self.layout.addWidget(name_widget)
    self.layout.addWidget(profiles_widget)
    self.layout.addSpacing(10)
    self.layout.addWidget(buttons_widget)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.error_message_label.setStyleSheet(Styles.error_message_label_style)

  def save_student(self):
    is_invalid, text = self.student_is_invalid()

    if is_invalid:
      self.error_message_label.setText(text)
      self.error_message_label.show()
      return

    student_name = StudentAdditionWidget.name_line_edit.text()
    QTimer.singleShot(0, StudentAdditionWidget.name_line_edit.clear)
    StudentAdditionWidget.check_boxes_selected = []

    checked_profiles = []
    for check_box in StudentAdditionWidget.check_boxes:
      if check_box.isChecked():
        checked_profiles.append(check_box.text())
        check_box.setChecked(False)

    create_student(student_name, checked_profiles)

    from dialogs.student_update_widget import StudentUpdateWidget
    StudentUpdateWidget.add_student(student_name)

    from search.current_search import CurrentSearch
    CurrentSearch.add_student(student_name)

    self.success_label.show()
    QTimer.singleShot(3500, self.success_label.hide)

  @staticmethod
  def check_box_modified(text):
    if text in StudentAdditionWidget.check_boxes_selected:
      StudentAdditionWidget.check_boxes_selected.remove(text)
    else:
      StudentAdditionWidget.check_boxes_selected.append(text)

    StudentAdditionWidget.update_save_button_state()

  @staticmethod
  def update_save_button_state():
    if (len(StudentAdditionWidget.name_line_edit.text()) > 0 and
        len(StudentAdditionWidget.check_boxes_selected) > 0):
      StudentAdditionWidget.save_button.setEnabled(True)
    else:
      StudentAdditionWidget.save_button.setDisabled(True)

  def select_all(self):
    StudentAdditionWidget.check_boxes_selected = []

    for check_box in StudentAdditionWidget.check_boxes:
      check_box.setChecked(True)
      StudentAdditionWidget.check_boxes_selected.append(check_box.text())

    StudentAdditionWidget.update_save_button_state()

  def student_is_invalid(self):
    student_name = StudentAdditionWidget.name_line_edit.text()

    if len(student_name) > StudentAdditionWidget.MAXIMUM_NAME_LENGTH:
      return True, _('STUDENT_NAME_LENGTH_EXCEEDS_LIMIT_TEXT')

    if student_name_exists(student_name):
      return True, _('STUDENT_NAME_EXISTS_TEXT')

    return False, ''

  @staticmethod
  def add_profile(profile_name):
    check_box = QCheckBox(profile_name)
    check_box_font = QFont(Settings.FONT, 14)
    check_box.clicked.connect(lambda ch, i=1: StudentAdditionWidget.check_box_modified(profile_name))
    check_box.setFont(check_box_font)
    StudentAdditionWidget.check_boxes.append(check_box)
    StudentAdditionWidget.last_index_used += 1
    StudentAdditionWidget.profiles_selection_widget.layout.addWidget(
      check_box, StudentAdditionWidget.last_index_used, 0
    )

  @staticmethod
  def update_profile(old_profile_name, new_profile_name):
    for check_box in StudentAdditionWidget.check_boxes:
      if check_box.text() == old_profile_name:
        check_box.setText(new_profile_name)
        return

  @staticmethod
  def remove_profile(profile_name):
    for check_box in StudentAdditionWidget.check_boxes:
      if check_box.text() == profile_name:
        StudentAdditionWidget.profiles_selection_widget.layout.removeWidget(check_box)
        StudentAdditionWidget.check_boxes.remove(check_box)

        if profile_name in StudentAdditionWidget.check_boxes_selected:
          StudentAdditionWidget.check_boxes_selected.remove(profile_name)
          StudentAdditionWidget.update_save_button_state()

        return
