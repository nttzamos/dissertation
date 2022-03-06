from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QComboBox, QSizePolicy, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from menu.settings import Settings
from models.profile import *
from shared.database_handler import get_grades, get_grade_subjects

class ProfileUpdateWidget(QWidget):
  PROFILE_SELECTION_TEXT = 'Επιλογή Προφίλ'
  SUBJECT_SELECTION_TEXT = 'Επιλογή Μαθημάτων'
  PROFILE_NAME_TEXT = 'Όνομα Προφίλ'
  PROFILE_GRADE_TEXT = 'Τάξη Προφίλ'
  UPDATE_PROFILE_BUTTON_TEXT = 'Αποθήκευση Προφίλ'
  DELETE_PROFILE_BUTTON_TEXT = 'Διαγραφή Προφίλ'
  ERROR_SAVING_PROFILE_TEXT = 'Αδυναμία αποθήκευσης προφίλ'
  ERROR_DELETING_PROFILE_TEXT = 'Αδυναμία διαγραφή προφίλ'
  SELECT_PROFILE_TEXT = 'Επιλέξτε ένα προφίλ...'
  NO_PROFILES_TEXT = 'Δεν υπάρχουν προφίλ'
  MUST_SELECT_PROFILE_TEXT = 'Πρέπει να επιλέξετε ένα προφίλ'
  GRADE_PROFILE_UPDATE_ERROR_TEXT = 'Τα προφίλ των τάξεων δεν μπορούν να μεταβληθούν'
  GRADE_PROFILE_DELETE_ERROR_TEXT = 'Τα προφίλ των τάξεων δεν μπορούν να διαγραφούν'
  PROFILE_NAME_EMPTY_TEXT = ('Το προφίλ δεν μπορεί να αποθηκευτεί καθώς δεν '
                             'έχετε συμπληρώσει το όνομα του')
  NAME_LENGTH_EXCEEDS_LIMIT_TEXT = ('Το προφίλ δεν μπορεί να αποθηκευτεί καθώς '
                                    'το μήκος του ονόματος του υπερβαίνει το '
                                    'όριο των 20 χαρακτήρων')
  PROFILE_NAME_EXISTS_TEXT = ('Το προφίλ δεν μπορεί να αποθηκευτεί καθώς '
                              'υπάρχει ήδη άλλο προφίλ με το ίδιο όνομα')
  NO_SUBJECT_SELECTED_TEXT = ('Το προφίλ δεν μπορεί να αποθηκευτεί καθώς δεν '
                              'έχετε επιλέξει κάποια μαθήματα για αυτό')

  MAXIMUM_NAME_LENGTH = 20

  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = QFont(Settings.font, 16)
    combo_box_font = QFont(Settings.font, 14)
    label_font = QFont(Settings.font, 14)
    line_edit_font = QFont(Settings.font, 14)

    self.check_boxes_modified = []

    profile_selection_widget = QGroupBox(ProfileUpdateWidget.PROFILE_SELECTION_TEXT)
    profile_selection_widget.setFont(section_label_font)
    profile_selection_widget.layout = QHBoxLayout(profile_selection_widget)
    profile_selection_widget.layout.setContentsMargins(10, 5, 10, 10)

    profiles = get_profiles()

    ProfileUpdateWidget.profile_selector = QComboBox()
    ProfileUpdateWidget.profile_selector.setFont(combo_box_font)

    if len(profiles) == 0:
      ProfileUpdateWidget.profile_selector.addItem(ProfileUpdateWidget.NO_PROFILES_TEXT)
      ProfileUpdateWidget.profile_selector.setDisabled(True)
    else:
      profiles[0:0] = [ProfileUpdateWidget.SELECT_PROFILE_TEXT]
      ProfileUpdateWidget.profile_selector.addItems(profiles)

    ProfileUpdateWidget.profile_selector.activated.connect(self.profile_selector_activated_initial)

    profile_selection_widget.layout.addWidget(ProfileUpdateWidget.profile_selector)

    self.name_widget = QGroupBox(ProfileUpdateWidget.PROFILE_NAME_TEXT)
    self.name_widget.setFont(section_label_font)
    self.name_widget.layout = QHBoxLayout(self.name_widget)
    self.name_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.name_line_edit = QLineEdit()
    self.name_line_edit.setFont(line_edit_font)
    self.name_line_edit.textChanged.connect(self.profile_name_changed)
    self.name_widget.layout.addWidget(self.name_line_edit)
    self.name_widget.hide()

    grade_label_widget = QGroupBox(ProfileUpdateWidget.PROFILE_GRADE_TEXT)
    grade_label_widget.setFont(section_label_font)
    grade_label_widget.layout = QHBoxLayout(grade_label_widget)
    grade_label_widget.layout.setContentsMargins(10, 5, 10, 10)

    ProfileUpdateWidget.grade_label = QLabel(ProfileUpdateWidget.MUST_SELECT_PROFILE_TEXT)
    ProfileUpdateWidget.grade_label.setFont(label_font)

    grade_label_widget.layout.addWidget(ProfileUpdateWidget.grade_label)

    subjects_widget = QGroupBox(ProfileUpdateWidget.SUBJECT_SELECTION_TEXT)
    subjects_widget.setFont(section_label_font)
    subjects_widget.layout = QHBoxLayout(subjects_widget)
    subjects_widget.layout.setContentsMargins(10, 5, 10, 10)

    self.subjects_selection_widget = QWidget()
    self.subjects_selection_widget.layout = QGridLayout(self.subjects_selection_widget)
    self.subjects_selection_widget.setDisabled(True)
    self.subjects_selection_widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(self.subjects_selection_widget)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    self.check_boxes = []

    vspacer = QLabel('f')
    invisible_font = QFont(Settings.font, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    self.subjects_selection_widget.layout.addWidget(vspacer, 1000, 0)

    subjects_widget.layout.addWidget(scroll_area)

    self.save_button = QPushButton(ProfileUpdateWidget.UPDATE_PROFILE_BUTTON_TEXT)
    self.save_button.pressed.connect(self.update_profile)
    self.save_button.setDisabled(True)
    self.save_button.setAutoDefault(False)

    self.delete_button = QPushButton(ProfileUpdateWidget.DELETE_PROFILE_BUTTON_TEXT)
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

  def profile_selector_activated_initial(self, index):
    if index != 0:
      ProfileUpdateWidget.profile_selector.removeItem(0)
      ProfileUpdateWidget.profile_selector.activated.disconnect()
      ProfileUpdateWidget.profile_selector.activated.connect(self.profile_selector_activated)
      self.profile_selector_activated(index - 1)
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

    check_box_font = QFont(Settings.font, 14)
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
      is_invalid, text = True, ProfileUpdateWidget.GRADE_PROFILE_UPDATE_ERROR_TEXT
    else:
      is_invalid, text = self.profile_is_invalid()

    if is_invalid:
      title = ProfileUpdateWidget.ERROR_SAVING_PROFILE_TEXT
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    self.check_boxes_modified = []
    self.save_button.setDisabled(True)

    old_profile_name = ProfileUpdateWidget.profile_selector.currentText()
    new_profile_name = self.name_line_edit.text()

    from search.current_search import CurrentSearch
    CurrentSearch.update_profile(old_profile_name, new_profile_name)

    from dialogs.student_addition_widget import StudentAdditionWidget
    StudentAdditionWidget.update_profile(old_profile_name, new_profile_name)

    from dialogs.student_update_widget import StudentUpdateWidget
    StudentUpdateWidget.update_profile(old_profile_name, new_profile_name)

    self.profile_selector.setItemText(self.profile_selector.currentIndex(), new_profile_name)
    update_profile_name(self.profile_id, new_profile_name)

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
      title = ProfileUpdateWidget.ERROR_DELETING_PROFILE_TEXT
      text = ProfileUpdateWidget.GRADE_PROFILE_DELETE_ERROR_TEXT
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

    ProfileUpdateWidget.profile_selector.removeItem(ProfileUpdateWidget.profile_selector.currentIndex())
    if ProfileUpdateWidget.profile_selector.count() == 0:
      ProfileUpdateWidget.profile_selector.addItem(ProfileUpdateWidget.NO_PROFILES_TEXT)
      ProfileUpdateWidget.profile_selector.setDisabled(True)
      ProfileUpdateWidget.profile_selector.activated.disconnect()
      ProfileUpdateWidget.profile_selector.activated.connect(self.profile_selector_activated_initial)
      ProfileUpdateWidget.grade_label.setText(ProfileUpdateWidget.MUST_SELECT_PROFILE_TEXT)
      self.name_widget.hide()
      return

    self.profile_selector_activated(0)

  def profile_name_changed(self):
    if self.name_line_edit.text() != self.profile_selector.currentText():
      self.save_button.setEnabled(True)
    elif len(self.check_boxes_modified) == 0:
      self.save_button.setDisabled(True)

  def check_box_modified(self, text):
    if text in self.check_boxes_modified:
      self.check_boxes_modified.remove(text)
    else:
      self.check_boxes_modified.append(text)

    if len(self.check_boxes_modified) > 0:
      self.save_button.setEnabled(True)
    elif self.name_line_edit.text() == self.profile_selector.currentText():
      self.save_button.setDisabled(True)

  def profile_is_invalid(self):
    profile_name = self.name_line_edit.text()
    if len(profile_name) == 0:
      return True, ProfileUpdateWidget.PROFILE_NAME_EMPTY_TEXT

    if len(profile_name) > ProfileUpdateWidget.MAXIMUM_NAME_LENGTH:
      return True, ProfileUpdateWidget.NAME_LENGTH_EXCEEDS_LIMIT_TEXT

    if ProfileUpdateWidget.profile_selector.currentText() != profile_name and profile_name_exists(profile_name):
      return True, ProfileUpdateWidget.PROFILE_NAME_EXISTS_TEXT

    for check_box in self.check_boxes:
      if check_box.isChecked():
        return False, ''

    return True, ProfileUpdateWidget.NO_SUBJECT_SELECTED_TEXT

  @staticmethod
  def add_profile(profile_name):
    if ProfileUpdateWidget.profile_selector.currentText() == ProfileUpdateWidget.NO_PROFILES_TEXT:
      ProfileUpdateWidget.profile_selector.setItemText(0, ProfileUpdateWidget.SELECT_PROFILE_TEXT)
      ProfileUpdateWidget.grade_label.setText(ProfileUpdateWidget.SELECT_PROFILE_TEXT)
      ProfileUpdateWidget.profile_selector.setEnabled(True)

    ProfileUpdateWidget.profile_selector.addItem(profile_name)

  def get_permission_to_delete(self):
    title = 'Διαγραφή Προφίλ'
    question = ('Είστε σίγουροι ότι θέλετε να διαγράψετε το επιλεγμένο προφίλ; '
                'Τα δεδομένα των μαθητών για το προφίλ αυτό θα διαγραφούν. '
                'Επίσης, μαθητές που έχουν μόνο το συγκεκριμένο προφίλ θα '
                'μείνουν χωρίς προφίλ.')

    answer = QMessageBox(self)
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(question)
    answer.setWindowTitle(title)

    yes_button = answer.addButton('Ναι', QMessageBox.ButtonRole.YesRole)
    cancel_button = answer.addButton('Ακύρωση', QMessageBox.ButtonRole.RejectRole)

    answer.setDefaultButton(cancel_button)

    check_box = QCheckBox('Να μην εμφανιστεί ξανά, μέχρι να κλείσει η εφαρμογή')
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
