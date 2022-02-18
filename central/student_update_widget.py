from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QComboBox, QLineEdit, QSizePolicy, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from menu.settings import Settings

from models.student import *
from models.profile import get_profiles

class StudentUpdateWidget(QWidget):
  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = QFont(Settings.font, 16)
    combo_box_font = QFont(Settings.font, 14)
    line_edit_font = QFont(Settings.font, 14)

    student_selection_widget = QGroupBox('Student Selection')
    student_selection_widget.setFont(section_label_font)
    student_selection_widget.layout = QHBoxLayout(student_selection_widget)
    student_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    students = get_students()

    StudentUpdateWidget.student_selector = QComboBox()
    StudentUpdateWidget.student_selector.setFont(combo_box_font)

    if len(students) == 0:
      StudentUpdateWidget.student_selector.addItem('There are no students')
      StudentUpdateWidget.student_selector.setDisabled(True)
    else:
      students[0:0] = ['Please select a student...']
      StudentUpdateWidget.student_selector.addItems(students)

    StudentUpdateWidget.student_selector.activated.connect(self.student_selector_activated_initial)

    student_selection_widget.layout.addWidget(StudentUpdateWidget.student_selector)

    self.name_widget = QGroupBox('Student Name')
    self.name_widget.setFont(section_label_font)
    self.name_widget.layout = QHBoxLayout(self.name_widget)
    self.name_widget.layout.setContentsMargins(10, 5, 10, 10)
    self.name_widget.hide()

    self.name_line_edit = QLineEdit()
    self.name_line_edit.setFont(line_edit_font)
    self.name_widget.layout.addWidget(self.name_line_edit)

    profiles_widget = QGroupBox('Profile Selection')
    profiles_widget.setFont(section_label_font)
    profiles_widget.layout = QHBoxLayout(profiles_widget)
    profiles_widget.layout.setContentsMargins(10, 5, 10, 10)

    StudentUpdateWidget.profiles_selection_widget = QWidget()
    StudentUpdateWidget.profiles_selection_widget.layout = QGridLayout(StudentUpdateWidget.profiles_selection_widget)
    StudentUpdateWidget.profiles_selection_widget.setDisabled(True)
    StudentUpdateWidget.profiles_selection_widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(StudentUpdateWidget.profiles_selection_widget)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    StudentUpdateWidget.check_boxes = []

    vspacer = QLabel('f')
    invisible_font = QFont(Settings.font, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    StudentUpdateWidget.profiles_selection_widget.layout.addWidget(vspacer, 1000, 0)

    profiles_widget.layout.addWidget(scroll_area)

    self.save_button = QPushButton('Update Student')
    self.save_button.pressed.connect(self.update_student)
    self.save_button.setDisabled(True)

    self.delete_button = QPushButton('Delete Student')
    self.delete_button.pressed.connect(self.delete_student)
    self.delete_button.setDisabled(True)

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
    self.setStyleSheet(Styles.student_update_style)

  def student_selector_activated_initial(self, index):
    if index != 0:
      StudentUpdateWidget.student_selector.removeItem(0)
      StudentUpdateWidget.student_selector.activated.disconnect()
      StudentUpdateWidget.student_selector.activated.connect(self.student_selector_activated)
      self.student_selector_activated(index - 1)
      self.save_button.setEnabled(True)
      self.delete_button.setEnabled(True)
      StudentUpdateWidget.profiles_selection_widget.setEnabled(True)
      self.name_widget.show()

  def student_selector_activated(self, index):
    student_name = StudentUpdateWidget.student_selector.currentText()
    self.student_id, self.student_profiles = get_student_details(student_name)
    self.name_line_edit.setText(student_name)
    profiles = get_profiles()

    for check_box in StudentUpdateWidget.check_boxes:
      StudentUpdateWidget.profiles_selection_widget.layout.removeWidget(check_box)

    check_box_font = QFont(Settings.font, 14)
    StudentUpdateWidget.check_boxes = []
    for i in range(len(profiles)):
      check_box = QCheckBox(profiles[i])
      check_box.setFont(check_box_font)
      StudentUpdateWidget.check_boxes.append(check_box)

      if profiles[i] in self.student_profiles:
        check_box.setChecked(True)

      StudentUpdateWidget.profiles_selection_widget.layout.addWidget(check_box, i, 0)
      StudentUpdateWidget.last_index_used = i

  def update_student(self):
    is_invalid, text = self.student_is_invalid()

    if is_invalid:
      title = 'Error Saving Student'
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    new_student_name = self.name_line_edit.text()
    from central.current_search import CurrentSearch
    CurrentSearch.update_student(StudentUpdateWidget.student_selector.currentText(), new_student_name)
    self.student_selector.setItemText(self.student_selector.currentIndex(), new_student_name)
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
    destroy_student(self.student_id)
    for check_box in StudentUpdateWidget.check_boxes:
      StudentUpdateWidget.profiles_selection_widget.layout.removeWidget(check_box)

    from central.current_search import CurrentSearch
    CurrentSearch.remove_student(StudentUpdateWidget.student_selector.currentText())

    StudentUpdateWidget.student_selector.removeItem(StudentUpdateWidget.student_selector.currentIndex())
    if StudentUpdateWidget.student_selector.count() == 0:
      StudentUpdateWidget.student_selector.addItem('There are no students')
      StudentUpdateWidget.student_selector.setDisabled(True)
      StudentUpdateWidget.student_selector.activated.disconnect()
      StudentUpdateWidget.student_selector.activated.connect(self.student_selector_activated_initial)
      self.name_widget.hide()
      return

    self.student_selector_activated(0)

  def student_is_invalid(self):
    student_name = self.name_line_edit.text()
    if len(student_name) == 0:
      return True, 'Student can not be saved because the profile name is empty.'

    if StudentUpdateWidget.student_selector.currentText() != student_name and  student_name_exists(student_name):
      return True, 'Student can not be saved as this name is already used for another profile.'

    for check_box in StudentUpdateWidget.check_boxes:
      if check_box.isChecked():
        return False, ''

    return True, 'Student can not be saved because none of the profiles have been selected.'

  @staticmethod
  def add_student(student_name):
    if StudentUpdateWidget.student_selector.currentText() == 'There are no students':
      StudentUpdateWidget.student_selector.setItemText(0, 'Please select a student...')
      StudentUpdateWidget.student_selector.setEnabled(True)

    StudentUpdateWidget.student_selector.addItem(student_name)

  @staticmethod
  def add_profile(profile_name):
    if StudentUpdateWidget.student_selector.currentText() == 'There are no students':
      return

    if StudentUpdateWidget.student_selector.currentText() == 'Please select a student...':
      return

    check_box = QCheckBox(profile_name)
    check_box_font = QFont(Settings.font, 14)
    check_box.setFont(check_box_font)
    StudentUpdateWidget.check_boxes.append(check_box)
    StudentUpdateWidget.last_index_used += 1
    StudentUpdateWidget.profiles_selection_widget.layout.addWidget(check_box, StudentUpdateWidget.last_index_used, 0)

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
