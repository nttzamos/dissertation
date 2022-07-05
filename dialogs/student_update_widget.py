from PyQt6.QtWidgets import (QGridLayout, QVBoxLayout, QHBoxLayout, QWidget,
                             QLabel, QGroupBox, QScrollArea, QCheckBox,
                             QPushButton, QComboBox, QLineEdit, QSizePolicy,
                             QMessageBox)
from PyQt6.QtCore import Qt

from menu.settings import Settings
from models.profile import get_profiles
from models.student import *
from shared.font_settings import FontSettings
from shared.spacer import Spacer

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class StudentUpdateWidget(QWidget):
  MAXIMUM_NAME_LENGTH = 50

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = FontSettings.get_font('heading')
    text_font = FontSettings.get_font('text')
    button_font = FontSettings.get_font('button')
    error_message_font = FontSettings.get_font('error')

    self.check_boxes_modified = []

    student_selection_widget = QGroupBox(_('STUDENT_SELECTION_TEXT'))
    student_selection_widget.setFont(section_label_font)
    student_selection_widget.layout = QHBoxLayout(student_selection_widget)
    student_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    students = get_students()

    StudentUpdateWidget.student_selector = QComboBox()
    StudentUpdateWidget.student_selector.setFont(text_font)

    if len(students) == 0:
      StudentUpdateWidget.student_selector.addItem(_('NO_STUDENTS_TEXT'))
      StudentUpdateWidget.student_selector.setDisabled(True)
    else:
      students[0:0] = [_('SELECT_STUDENT_TEXT')]
      StudentUpdateWidget.student_selector.addItems(students)

    StudentUpdateWidget.student_selector.activated.connect(
      self.student_selector_activated_initial
    )

    student_selection_widget.layout.addWidget(StudentUpdateWidget.student_selector)

    self.name_widget = QGroupBox(_('STUDENT_NAME_TEXT'))
    self.name_widget.setFont(section_label_font)
    self.name_widget.layout = QVBoxLayout(self.name_widget)
    self.name_widget.layout.setContentsMargins(10, 5, 10, 10)
    self.name_widget.hide()

    self.name_line_edit = QLineEdit()
    self.name_line_edit.setMaxLength(100)
    self.name_line_edit.setFont(text_font)
    self.name_line_edit.textChanged.connect(self.update_save_button_state)

    self.error_message_label = QLabel(self)
    self.error_message_label.setFont(error_message_font)
    self.name_line_edit.textChanged.connect(self.error_message_label.hide)
    self.error_message_label.hide()

    self.name_widget.layout.addWidget(self.name_line_edit)
    self.name_widget.layout.addWidget(self.error_message_label)

    profiles_widget = QGroupBox(_('PROFILE_SELECTION_TEXT'))
    profiles_widget.setFont(section_label_font)
    profiles_widget.layout = QHBoxLayout(profiles_widget)
    profiles_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)
    self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    self.initialize_scroll_area()

    profiles_widget.layout.addWidget(self.scroll_area)

    self.save_button = QPushButton(_('UPDATE_STUDENT_BUTTON_TEXT'))
    self.save_button.setFont(button_font)
    self.save_button.pressed.connect(self.update_student)
    self.save_button.setDisabled(True)
    self.save_button.setAutoDefault(False)

    self.delete_button = QPushButton(_('DELETE_STUDENT_BUTTON_TEXT'))
    self.delete_button.setFont(button_font)
    self.delete_button.pressed.connect(self.delete_student)
    self.delete_button.setDisabled(True)
    self.delete_button.setAutoDefault(False)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.setContentsMargins(0, 0, 0, 0)
    buttons_widget.layout.addWidget(self.delete_button)
    buttons_widget.layout.addSpacing(10)
    buttons_widget.layout.addWidget(self.save_button)

    self.layout.addWidget(student_selection_widget)
    self.layout.addWidget(self.name_widget)
    self.layout.addWidget(profiles_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(buttons_widget, alignment=Qt.AlignmentFlag.AlignRight)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.error_message_label.setStyleSheet(Styles.error_message_label_style)
    self.save_button.setStyleSheet(Styles.dialog_button_style)
    self.delete_button.setStyleSheet(Styles.dialog_button_style)

  def initialize_scroll_area(self):
    StudentUpdateWidget.profiles_selection_widget = QWidget()
    StudentUpdateWidget.profiles_selection_widget.layout = QGridLayout(StudentUpdateWidget.profiles_selection_widget)
    StudentUpdateWidget.profiles_selection_widget.setDisabled(True)
    StudentUpdateWidget.profiles_selection_widget.setSizePolicy(
      QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
    )

    StudentUpdateWidget.check_boxes = []

    StudentUpdateWidget.profiles_selection_widget.layout.addWidget(Spacer(), 1000, 0)

    self.scroll_area.setWidget(StudentUpdateWidget.profiles_selection_widget)

  def student_selector_activated_initial(self, index):
    if index != 0:
      StudentUpdateWidget.student_selector.removeItem(0)
      StudentUpdateWidget.student_selector.activated.disconnect()
      StudentUpdateWidget.student_selector.activated.connect(
        self.student_selector_activated
      )

      self.student_selector_activated(index - 1)
      self.delete_button.setEnabled(True)
      StudentUpdateWidget.profiles_selection_widget.setEnabled(True)
      self.name_widget.show()

  def student_selector_activated(self, index):
    student_name = StudentUpdateWidget.student_selector.currentText()
    self.student_id, self.student_profiles = get_student_details(student_name)
    self.name_line_edit.setText(student_name)
    self.save_button.setDisabled(True)

    profiles = get_profiles()

    for check_box in StudentUpdateWidget.check_boxes:
      StudentUpdateWidget.profiles_selection_widget.layout.removeWidget(check_box)

    check_box_font = FontSettings.get_font('text')
    StudentUpdateWidget.check_boxes = []
    self.check_boxes_modified = []
    for i in range(len(profiles)):
      check_box = QCheckBox(profiles[i])
      check_box.clicked.connect(lambda ch, i=i: self.check_box_modified(profiles[i]))
      check_box.setFont(check_box_font)
      StudentUpdateWidget.check_boxes.append(check_box)

      if profiles[i] in self.student_profiles:
        check_box.setChecked(True)

      StudentUpdateWidget.profiles_selection_widget.layout.addWidget(check_box, i, 0)
      StudentUpdateWidget.last_index_used = i

  def update_student(self):
    is_invalid, text = self.student_is_invalid()

    if is_invalid:
      self.error_message_label.setText(text)
      self.error_message_label.show()
      return

    self.check_boxes_modified = []
    self.save_button.setDisabled(True)

    new_student_name = self.name_line_edit.text()
    from search.current_search import CurrentSearch
    CurrentSearch.update_student(
      StudentUpdateWidget.student_selector.currentText(), new_student_name
    )

    self.student_selector.setItemText(
      self.student_selector.currentIndex(), new_student_name
    )

    update_student_name(self.student_id, new_student_name)

    profile_names = []
    for check_box in StudentUpdateWidget.check_boxes:
      if check_box.isChecked():
        profile_names.append(check_box.text())

    profiles_to_remove = list(set(self.student_profiles) - set(profile_names))
    profiles_to_add = list(set(profile_names) - set(self.student_profiles))
    self.student_profiles = profile_names
    add_student_profiles(self.student_id, profiles_to_add)
    remove_student_profiles(self.student_id, profiles_to_remove)

    if CurrentSearch.student_selector.currentText() == new_student_name:
      CurrentSearch.add_profiles(profiles_to_add)
      CurrentSearch.remove_profiles(profiles_to_remove)

  def delete_student(self):
    if not Settings.get_boolean_setting('hide_delete_student_message'):
      if not self.get_permission_to_delete():
        return

    self.save_button.setDisabled(True)

    destroy_student(self.student_id)
    for check_box in StudentUpdateWidget.check_boxes:
      StudentUpdateWidget.profiles_selection_widget.layout.removeWidget(check_box)

    from search.current_search import CurrentSearch
    CurrentSearch.remove_student(StudentUpdateWidget.student_selector.currentText())

    StudentUpdateWidget.student_selector.removeItem(
      StudentUpdateWidget.student_selector.currentIndex()
    )

    if StudentUpdateWidget.student_selector.count() == 0:
      self.initialize_scroll_area()
      self.name_widget.hide()
      self.delete_button.setDisabled(True)

      StudentUpdateWidget.student_selector.addItem(_('NO_STUDENTS_TEXT'))
      StudentUpdateWidget.student_selector.setDisabled(True)
      StudentUpdateWidget.student_selector.activated.disconnect()
      StudentUpdateWidget.student_selector.activated.connect(
        self.student_selector_activated_initial
      )
    else:
      self.student_selector_activated(0)

  def check_box_modified(self, text):
    if text in self.check_boxes_modified:
      self.check_boxes_modified.remove(text)
    else:
      self.check_boxes_modified.append(text)

    self.update_save_button_state()

  def update_save_button_state(self):
    if self.save_button_is_active():
      self.save_button.setEnabled(True)
    else:
      self.save_button.setDisabled(True)

  def save_button_is_active(self):
    fields_non_empty = len(self.name_line_edit.text()) > 0 and self.selected_check_box_exists()

    if fields_non_empty and (len(self.check_boxes_modified) or
       self.name_line_edit.text() != self.student_selector.currentText()):
      return True

    return False

  def selected_check_box_exists(self):
    for check_box in StudentUpdateWidget.check_boxes:
      if check_box.isChecked():
        return True

    return False

  def student_is_invalid(self):
    student_name = self.name_line_edit.text()

    if len(student_name) > StudentUpdateWidget.MAXIMUM_NAME_LENGTH:
      return True, _('STUDENT_NAME_LENGTH_EXCEEDS_LIMIT_TEXT')

    if (StudentUpdateWidget.student_selector.currentText() != student_name and
        student_name_exists(student_name)):
      return True, _('STUDENT_NAME_EXISTS_TEXT')

    return False, ''

  def update_student_update_widget(self):
    non_student_selections = [
      _('NO_STUDENTS_TEXT'), _('SELECT_STUDENT_TEXT')
    ]

    if StudentUpdateWidget.student_selector.currentText() in non_student_selections:
      return

    self.initialize_scroll_area()
    self.save_button.setDisabled(True)
    self.delete_button.setDisabled(True)
    self.name_widget.hide()

    students = get_students()

    StudentUpdateWidget.student_selector.clear()

    if len(students) == 0:
      StudentUpdateWidget.student_selector.addItem(_('NO_STUDENTS_TEXT'))
      StudentUpdateWidget.student_selector.setDisabled(True)
    else:
      students[0:0] = [_('SELECT_STUDENT_TEXT')]
      StudentUpdateWidget.student_selector.addItems(students)

    StudentUpdateWidget.student_selector.activated.disconnect()
    StudentUpdateWidget.student_selector.activated.connect(
      self.student_selector_activated_initial
    )

  @staticmethod
  def add_student(student_name):
    student_selector_current_text = StudentUpdateWidget.student_selector.currentText()

    if student_selector_current_text == _('NO_STUDENTS_TEXT'):
      StudentUpdateWidget.student_selector.setItemText(
        0, _('SELECT_STUDENT_TEXT')
      )

      StudentUpdateWidget.student_selector.setEnabled(True)

    StudentUpdateWidget.student_selector.addItem(student_name)

  @staticmethod
  def add_profile(profile_name):
    student_selector_current_text = StudentUpdateWidget.student_selector.currentText()

    if student_selector_current_text == _('NO_STUDENTS_TEXT'):
      return

    if student_selector_current_text == _('SELECT_STUDENT_TEXT'):
      return

    check_box = QCheckBox(profile_name)
    check_box_font = FontSettings.get_font('text')
    check_box.setFont(check_box_font)
    StudentUpdateWidget.check_boxes.append(check_box)
    StudentUpdateWidget.last_index_used += 1
    StudentUpdateWidget.profiles_selection_widget.layout.addWidget(
      check_box, StudentUpdateWidget.last_index_used, 0
    )

  @staticmethod
  def update_profile(old_profile_name, new_profile_name):
    if len(StudentUpdateWidget.check_boxes) == 0:
      return

    for check_box in StudentUpdateWidget.check_boxes:
      if check_box.text() == old_profile_name:
        check_box.setText(new_profile_name)
        return

  @staticmethod
  def remove_profile(profile_name):
    if len(StudentUpdateWidget.check_boxes) == 0:
      return

    for check_box in StudentUpdateWidget.check_boxes:
      if check_box.text() == profile_name:
        StudentUpdateWidget.profiles_selection_widget.layout.removeWidget(check_box)
        StudentUpdateWidget.check_boxes.remove(check_box)
        return

  def get_permission_to_delete(self):
    title = _('DELETE_STUDENT_BUTTON_TEXT')
    question = _('DELETE_STUDENT_PERMISSION')

    answer = QMessageBox()

    answer.setFont(FontSettings.get_font('text'))
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(question)
    answer.setWindowTitle(title)

    yes_button = answer.addButton(_('YES'), QMessageBox.ButtonRole.YesRole)
    yes_button.setFont(FontSettings.get_font('text'))
    cancel_button = answer.addButton(_('CANCEL'), QMessageBox.ButtonRole.RejectRole)
    cancel_button.setFont(FontSettings.get_font('text'))

    from shared.styles import Styles
    yes_button.setStyleSheet(Styles.dialog_button_style)
    cancel_button.setStyleSheet(Styles.dialog_default_button_style)

    answer.setDefaultButton(cancel_button)

    check_box = QCheckBox(_('HIDE_MESSAGE_CHECKBOX'))
    check_box.setFont(FontSettings.get_font('text'))
    check_box.clicked.connect(self.toggle_message_setting)
    check_box.setChecked(False)

    answer.setCheckBox(check_box)
    answer.exec()

    if answer.clickedButton() == yes_button:
      return True

    return False

  @staticmethod
  def toggle_message_setting(value):
    Settings.set_boolean_setting('hide_delete_student_message', value)
