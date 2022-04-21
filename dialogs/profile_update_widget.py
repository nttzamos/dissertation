from PyQt6.QtWidgets import (QGridLayout, QVBoxLayout, QHBoxLayout, QWidget,
                             QLineEdit, QLabel, QGroupBox, QScrollArea,
                             QCheckBox, QPushButton, QComboBox, QSizePolicy,
                             QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from menu.settings import Settings
from models.profile import *
from shared.database_handler import get_grades, get_grade_subjects
from shared.spacer import Spacer

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class ProfileUpdateWidget(QWidget):
  MAXIMUM_NAME_LENGTH = 20

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = QFont(Settings.FONT, 16)
    combo_box_font = QFont(Settings.FONT, 14)
    label_font = QFont(Settings.FONT, 14)
    line_edit_font = QFont(Settings.FONT, 14)
    error_message_font = QFont(Settings.FONT, 10)

    self.check_boxes_modified = []

    profile_selection_widget = QGroupBox(_('PROFILE_SELECTION_TEXT'))
    profile_selection_widget.setFont(section_label_font)
    profile_selection_widget.layout = QHBoxLayout(profile_selection_widget)
    profile_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    profiles = get_profiles()

    ProfileUpdateWidget.profile_selector = QComboBox()
    ProfileUpdateWidget.profile_selector.setFont(combo_box_font)

    if len(profiles) == 0:
      ProfileUpdateWidget.profile_selector.addItem(_('NO_PROFILES_TEXT'))
      ProfileUpdateWidget.profile_selector.setDisabled(True)
    else:
      profiles[0:0] = [_('SELECT_PROFILE_TEXT')]
      ProfileUpdateWidget.profile_selector.addItems(profiles)

    ProfileUpdateWidget.profile_selector.activated.connect(
      self.profile_selector_activated_initial
    )

    profile_selection_widget.layout.addWidget(ProfileUpdateWidget.profile_selector)

    self.name_widget = QGroupBox(_('PROFILE_NAME_TEXT'))
    self.name_widget.setFont(section_label_font)
    self.name_widget.layout = QVBoxLayout(self.name_widget)
    self.name_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.name_line_edit = QLineEdit()
    self.name_line_edit.setFont(line_edit_font)
    self.name_line_edit.textChanged.connect(self.update_save_button_state)

    self.error_message_label = QLabel(self)
    self.error_message_label.setFont(error_message_font)
    self.name_line_edit.textChanged.connect(self.error_message_label.hide)
    self.error_message_label.hide()

    self.name_widget.layout.addWidget(self.name_line_edit)
    self.name_widget.layout.addWidget(self.error_message_label)

    self.name_widget.hide()

    grade_label_widget = QGroupBox(_('PROFILE_GRADE_TEXT'))
    grade_label_widget.setFont(section_label_font)
    grade_label_widget.layout = QHBoxLayout(grade_label_widget)
    grade_label_widget.layout.setContentsMargins(10, 5, 10, 10)

    ProfileUpdateWidget.grade_label = QLabel(_('MUST_SELECT_PROFILE_TEXT'))
    ProfileUpdateWidget.grade_label.setFont(label_font)

    grade_label_widget.layout.addWidget(ProfileUpdateWidget.grade_label)

    subjects_widget = QGroupBox(_('SUBJECT_SELECTION_TEXT'))
    subjects_widget.setFont(section_label_font)
    subjects_widget.layout = QHBoxLayout(subjects_widget)
    subjects_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.subjects_selection_widget = QWidget()
    self.subjects_selection_widget.layout = QGridLayout(self.subjects_selection_widget)
    self.subjects_selection_widget.setDisabled(True)
    self.subjects_selection_widget.setSizePolicy(
      QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
    )

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(self.subjects_selection_widget)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    self.check_boxes = []

    self.subjects_selection_widget.layout.addWidget(Spacer(), 1000, 0)

    subjects_widget.layout.addWidget(scroll_area)

    self.save_button = QPushButton(_('UPDATE_PROFILE_BUTTON_TEXT'))
    self.save_button.pressed.connect(self.update_profile)
    self.save_button.setDisabled(True)
    self.save_button.setAutoDefault(False)

    self.delete_button = QPushButton(_('DELETE_PROFILE_BUTTON_TEXT'))
    self.delete_button.pressed.connect(self.delete_profile)
    self.delete_button.setDisabled(True)
    self.delete_button.setAutoDefault(False)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.setContentsMargins(0, 0, 0, 0)
    buttons_widget.layout.addWidget(self.delete_button)
    buttons_widget.layout.addSpacing(10)
    buttons_widget.layout.addWidget(self.save_button)

    self.layout.addWidget(profile_selection_widget)
    self.layout.addWidget(self.name_widget)
    self.layout.addWidget(grade_label_widget)
    self.layout.addWidget(subjects_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(buttons_widget, alignment=Qt.AlignmentFlag.AlignRight)
    self.style()

  def style(self):
    from shared.styles import Styles
    self.error_message_label.setStyleSheet(Styles.error_message_label_style)

  def profile_selector_activated_initial(self, index):
    if index != 0:
      ProfileUpdateWidget.profile_selector.removeItem(0)
      ProfileUpdateWidget.profile_selector.activated.disconnect()
      ProfileUpdateWidget.profile_selector.activated.connect(self.profile_selector_activated)
      self.profile_selector_activated(index - 1)

      if self.profile_selector.currentText() in get_grades():
        self.delete_button.setDisabled(True)
      else:
        self.delete_button.setEnabled(True)

      self.subjects_selection_widget.setEnabled(True)
      self.name_widget.show()

  def profile_selector_activated(self, index):
    profile_name = ProfileUpdateWidget.profile_selector.currentText()
    self.profile_id, self.grade_id, grade_name, self.profile_subjects = get_profile_details(profile_name)
    ProfileUpdateWidget.grade_label.setText(grade_name)
    self.name_line_edit.setText(profile_name)
    self.save_button.setDisabled(True)

    grade_subjects = get_grade_subjects(self.grade_id)

    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    check_box_font = QFont(Settings.FONT, 14)
    self.check_boxes = []
    self.check_boxes_modified = []
    for i in range(len(grade_subjects)):
      check_box = QCheckBox(grade_subjects[i])
      check_box.clicked.connect(lambda ch, i=i: self.check_box_modified(grade_subjects[i]))
      check_box.setFont(check_box_font)
      self.check_boxes.append(check_box)

      if grade_subjects[i] in self.profile_subjects:
        check_box.setChecked(True)

      self.subjects_selection_widget.layout.addWidget(check_box, i, 0)

  def update_profile(self):
    if self.profile_selector.currentText() in get_grades():
      is_invalid, text = True, _('GRADE_PROFILE_UPDATE_ERROR_TEXT')
    else:
      is_invalid, text = self.profile_is_invalid()

    message_box_values = [
      _('GRADE_PROFILE_UPDATE_ERROR_TEXT'), self.construct_redundant_profile_message()
    ]

    if is_invalid:
      if text in message_box_values:
        title = _('ERROR_SAVING_PROFILE_TEXT')
        QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      else:
        self.error_message_label.setText(text)
        self.error_message_label.show()

      return

    self.check_boxes_modified = []
    self.save_button.setDisabled(True)

    old_profile_name = ProfileUpdateWidget.profile_selector.currentText()
    new_profile_name = self.name_line_edit.text()

    from search.current_search import CurrentSearch
    if old_profile_name != new_profile_name:
      CurrentSearch.update_profile(old_profile_name, new_profile_name)

      from dialogs.student_addition_widget import StudentAdditionWidget
      StudentAdditionWidget.update_profile(old_profile_name, new_profile_name)

      self.profile_selector.setItemText(self.profile_selector.currentIndex(), new_profile_name)
      update_profile_name(self.profile_id, new_profile_name)

      from dialogs.data_editing_widget import DataEditingWidget
      DataEditingWidget.update_student_update_widget()

    subjects_names = []
    for check_box in self.check_boxes:
      if check_box.isChecked():
        subjects_names.append(check_box.text())

    subjects_to_remove = list(set(self.profile_subjects) - set(subjects_names))
    subjects_to_add = list(set(subjects_names) - set(self.profile_subjects))
    self.profile_subjects = subjects_names

    add_profile_subjects(self.grade_id, self.profile_id, subjects_to_add)
    remove_profile_subjects(self.grade_id, self.profile_id, subjects_to_remove)

    if CurrentSearch.profile_selector.currentText() == new_profile_name:
      CurrentSearch.add_subjects(subjects_to_add)
      CurrentSearch.remove_subjects(subjects_to_remove)

  def delete_profile(self):
    if self.profile_selector.currentText() in get_grades():
      title = _('ERROR_DELETING_PROFILE_TEXT')
      text = _('GRADE_PROFILE_DELETE_ERROR_TEXT')
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    if not Settings.get_boolean_setting('hide_delete_profile_message'):
      if not self.get_permission_to_delete():
        return

    destroy_profile(self.profile_id)
    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    from dialogs.student_addition_widget import StudentAdditionWidget
    StudentAdditionWidget.remove_profile(ProfileUpdateWidget.profile_selector.currentText())

    from dialogs.student_update_widget import StudentUpdateWidget
    StudentUpdateWidget.remove_profile(ProfileUpdateWidget.profile_selector.currentText())

    from search.current_search import CurrentSearch
    CurrentSearch.remove_profiles([ProfileUpdateWidget.profile_selector.currentText()])

    ProfileUpdateWidget.profile_selector.removeItem(
      ProfileUpdateWidget.profile_selector.currentIndex()
    )

    if ProfileUpdateWidget.profile_selector.count() == 0:
      ProfileUpdateWidget.profile_selector.addItem(_('NO_PROFILES_TEXT'))
      ProfileUpdateWidget.profile_selector.setDisabled(True)
      ProfileUpdateWidget.profile_selector.activated.disconnect()
      ProfileUpdateWidget.profile_selector.activated.connect(
        self.profile_selector_activated_initial
      )

      ProfileUpdateWidget.grade_label.setText(_('MUST_SELECT_PROFILE_TEXT'))
      self.name_widget.hide()
      return

    self.profile_selector_activated(0)

    from dialogs.data_editing_widget import DataEditingWidget
    DataEditingWidget.update_student_update_widget()

  def check_box_modified(self, text):
    if text in self.check_boxes_modified:
      self.check_boxes_modified.remove(text)
    else:
      self.check_boxes_modified.append(text)

    self.update_save_button_state()

  def update_save_button_state(self):
    if self.profile_selector.currentText() in get_grades():
      self.save_button.setDisabled(True)
      return

    fields_non_empty = len(self.name_line_edit.text()) > 0 and self.selected_check_box_exists()

    if fields_non_empty and (len(self.check_boxes_modified) or
       self.name_line_edit.text() != self.profile_selector.currentText()):
      self.save_button.setEnabled(True)
    else:
      self.save_button.setDisabled(True)

  def selected_check_box_exists(self):
    for check_box in self.check_boxes:
      if check_box.isChecked():
        return True

    return False

  def profile_is_invalid(self):
    profile_name = self.name_line_edit.text()

    if len(profile_name) > ProfileUpdateWidget.MAXIMUM_NAME_LENGTH:
      return True, _('PROFILE_NAME_LENGTH_EXCEEDS_LIMIT_TEXT')

    if (ProfileUpdateWidget.profile_selector.currentText() != profile_name and
        profile_name_exists(profile_name)):
      return True, _('PROFILE_NAME_EXISTS_TEXT')

    for check_box in self.check_boxes:
      if not check_box.isChecked():
        return False, ''

    return True, self.construct_redundant_profile_message()

  def construct_redundant_profile_message(self):
    return _('REDUNDANT_PROFILE_MESSAGE') + ProfileUpdateWidget.grade_label.text()

  @staticmethod
  def add_profile(profile_name):
    if ProfileUpdateWidget.profile_selector.currentText() == _('NO_PROFILES_TEXT'):
      ProfileUpdateWidget.profile_selector.setItemText(0, _('SELECT_PROFILE_TEXT'))
      ProfileUpdateWidget.grade_label.setText(_('SELECT_PROFILE_TEXT'))
      ProfileUpdateWidget.profile_selector.setEnabled(True)

    ProfileUpdateWidget.profile_selector.addItem(profile_name)

  def get_permission_to_delete(self):
    title = _('DELETE_PROFILE_BUTTON_TEXT')
    question = _('DELETE_PROFILE_PERMISSION')

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
    Settings.set_boolean_setting('hide_delete_profile_message', value)
