from PyQt6.QtWidgets import (QGridLayout, QVBoxLayout, QHBoxLayout, QWidget,
                             QLineEdit, QLabel, QGroupBox, QScrollArea,
                             QCheckBox, QPushButton, QComboBox, QSizePolicy,
                             QMessageBox)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

from menu.settings import Settings
from models.profile import create_profile, profile_name_exists
from shared.database_handler import get_grades, get_grade_subjects

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

    section_label_font = QFont(Settings.FONT, 16)
    combo_box_font = QFont(Settings.FONT, 14)
    check_box_font = QFont(Settings.FONT, 14)
    line_edit_font = QFont(Settings.FONT, 14)
    label_font = QFont(Settings.FONT, 12)

    self.success_label = QLabel(_('SUCCESS_SAVING_PROFILE_TEXT'))
    self.success_label.setFont(label_font)
    size_policy = self.success_label.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    self.success_label.setSizePolicy(size_policy)
    self.success_label.hide()
    self.success_label.setStyleSheet('QLabel { color: green }')

    name_widget = QGroupBox(_('PROFILE_NAME_TEXT'))
    name_widget.setFont(section_label_font)
    name_widget.layout = QHBoxLayout(name_widget)
    name_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.name_line_edit = QLineEdit()
    self.name_line_edit.setFont(line_edit_font)
    name_widget.layout.addWidget(self.name_line_edit)

    grade_selection_widget = QGroupBox(_('GRADE_SELECTION_TEXT'))
    grade_selection_widget.setFont(section_label_font)
    grade_selection_widget.layout = QHBoxLayout(grade_selection_widget)
    grade_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.grade_selector = QComboBox()
    self.grade_selector.setFont(combo_box_font)
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
    for i in range(len(grade_subjects)):
      check_box = QCheckBox(grade_subjects[i])
      check_box.setFont(check_box_font)
      self.check_boxes.append(check_box)
      self.subjects_selection_widget.layout.addWidget(check_box, i, 0)

    vspacer = QLabel('f')
    invisible_font = QFont(Settings.FONT, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    self.subjects_selection_widget.layout.addWidget(vspacer, 1000, 0)

    subjects_widget.layout.addWidget(scroll_area)

    save_button = QPushButton(_('SAVE_PROFILE_BUTTON_TEXT'))
    save_button.pressed.connect(self.save_profile)
    save_button.setAutoDefault(False)

    select_all_button = QPushButton(_('SELECT_ALL_SUBJECTS_TEXT'))
    select_all_button.pressed.connect(self.select_all)
    select_all_button.setAutoDefault(False)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.addWidget(select_all_button, alignment=Qt.AlignmentFlag.AlignLeft)
    buttons_widget.layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignRight)

    self.layout.addWidget(self.success_label, alignment=Qt.AlignmentFlag.AlignRight)
    self.layout.addWidget(name_widget)
    self.layout.addWidget(grade_selection_widget)
    self.layout.addWidget(subjects_widget)
    self.layout.addSpacing(10)
    self.layout.addWidget(buttons_widget)

  def grade_selector_activated(self, index):
    for check_box in self.check_boxes:
      self.subjects_selection_widget.layout.removeWidget(check_box)

    grade_subjects = get_grade_subjects(index + 1)

    check_box_font = QFont(Settings.FONT, 14)
    self.check_boxes = []
    for i in range(len(grade_subjects)):
      check_box = QCheckBox(grade_subjects[i])
      check_box.setFont(check_box_font)
      self.check_boxes.append(check_box)
      self.subjects_selection_widget.layout.addWidget(check_box, i, 0)

  def save_profile(self):
    is_invalid, text = self.profile_is_invalid()

    if is_invalid:
      title = _('ERROR_SAVING_PROFILE_TEXT')
      QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      return

    profile_name = self.name_line_edit.text()
    QTimer.singleShot(0, self.name_line_edit.clear)

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

  def select_all(self):
    for check_box in self.check_boxes:
      check_box.setChecked(True)

  def profile_is_invalid(self):
    profile_name = self.name_line_edit.text()
    if len(profile_name) == 0:
      return True, _('PROFILE_NAME_EMPTY_TEXT')

    if len(profile_name) > ProfileAdditionWIdget.MAXIMUM_NAME_LENGTH:
      return True, _('PROFILE_NAME_LENGTH_EXCEEDS_LIMIT_TEXT')

    if profile_name_exists(profile_name):
      return True, _('PROFILE_NAME_EXISTS_TEXT')

    checked_check_boxes_count = 0

    for check_box in self.check_boxes:
      if check_box.isChecked():
        checked_check_boxes_count += 1

    if checked_check_boxes_count == 0:
      return True, _('NO_SUBJECT_SELECTED_TEXT')
    elif checked_check_boxes_count == len(self.check_boxes):
      return True, self.construct_redundant_profile_message()
    else:
      return False, ''

  def construct_redundant_profile_message(self):
    return (
      'Το προφίλ δεν μπορεί να αποθηκευτεί καθώς τα μαθήματα του ταυτίζονται '
      'με αυτά του προκαθορισμένου προφίλ ' + self.grade_selector.currentText()
    )
