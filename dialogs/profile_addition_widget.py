from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QComboBox, QSizePolicy, QMessageBox
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

from menu.settings import Settings
from models.profile import create_profile, profile_name_exists
from shared.database_handler import get_grades, get_grade_subjects

class ProfileAdditionWIdget(QWidget):
  PROFILE_NAME_TEXT = 'Όνομα Προφίλ'
  GRADE_SELECTION_TEXT = 'Επιλογή Τάξης'
  SUBJECT_SELECTION_TEXT = 'Επιλογή Μαθημάτων'
  SAVE_PROFILE_BUTTON_TEXT = 'Αποθήκευση Προφίλ'
  ERROR_SAVING_PROFILE_TEXT = 'Αδυναμία αποθήκευσης προφίλ'
  PROFILE_NAME_EMPTY_TEXT = ('Το προφίλ δεν μπορεί να αποθηκευτεί καθώς δεν '
                             'έχετε συμπληρώσει το όνομα του')
  PROFILE_NAME_EXISTS_TEXT = ('Το προφίλ δεν μπορεί να αποθηκευτεί καθώς '
                              'υπάρχει ήδη άλλο προφίλ με το ίδιο όνομα')
  NO_SUBJECT_SELECTED_TEXT = ('Το προφίλ δεν μπορεί να αποθηκευτεί καθώς δεν '
                              'έχετε επιλέξει κάποια μαθήματα για αυτό')

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = QFont(Settings.font, 16)
    combo_box_font = QFont(Settings.font, 14)
    check_box_font = QFont(Settings.font, 14)
    line_edit_font = QFont(Settings.font, 14)

    name_widget = QGroupBox(ProfileAdditionWIdget.PROFILE_NAME_TEXT)
    name_widget.setFont(section_label_font)
    name_widget.layout = QHBoxLayout(name_widget)
    name_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.name_line_edit = QLineEdit()
    self.name_line_edit.setFont(line_edit_font)
    name_widget.layout.addWidget(self.name_line_edit)

    grade_selection_widget = QGroupBox(ProfileAdditionWIdget.GRADE_SELECTION_TEXT)
    grade_selection_widget.setFont(section_label_font)
    grade_selection_widget.layout = QHBoxLayout(grade_selection_widget)
    grade_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.grade_selector = QComboBox()
    self.grade_selector.setFont(combo_box_font)
    self.grade_selector.addItems(get_grades())
    self.grade_selector.activated.connect(self.grade_selector_activated)

    grade_selection_widget.layout.addWidget(self.grade_selector)

    subjects_widget = QGroupBox(ProfileAdditionWIdget.SUBJECT_SELECTION_TEXT)
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

    self.save_button = QPushButton(ProfileAdditionWIdget.SAVE_PROFILE_BUTTON_TEXT)
    self.save_button.pressed.connect(self.save_profile)
    self.save_button.setAutoDefault(False)

    self.layout.addWidget(name_widget)
    self.layout.addWidget(grade_selection_widget)
    self.layout.addWidget(subjects_widget)
    self.layout.addSpacing(15)
    self.layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

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

  def save_profile(self):
    is_invalid, text = self.profile_is_invalid()

    if is_invalid:
      title = ProfileAdditionWIdget.ERROR_SAVING_PROFILE_TEXT
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
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

  def profile_is_invalid(self):
    profile_name = self.name_line_edit.text()
    if len(profile_name) == 0:
      return True, ProfileAdditionWIdget.PROFILE_NAME_EMPTY_TEXT

    if profile_name_exists(profile_name):
      return True, ProfileAdditionWIdget.PROFILE_NAME_EXISTS_TEXT

    for check_box in self.check_boxes:
      if check_box.isChecked():
        return False, ''

    return True, ProfileAdditionWIdget.NO_SUBJECT_SELECTED_TEXT
