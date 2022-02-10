from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from Common.databaseHandler import DBHandler

from MenuBar.settings import Settings

class CurrentSearch(QWidget):
  subject_selector_active = False

  def __init__(self):
    super().__init__()

    self.setFixedHeight(300)
    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(50, 50, 50, 50)

    searched_word_font = QFont(Settings.font, 20)
    combo_box_font = QFont(Settings.font, 14)

    self.searched_word = QLabel('Enter a word.')
    self.searched_word.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.searched_word.setMaximumHeight(100)
    self.searched_word.setFont(searched_word_font)

    self.search_details = QWidget()
    self.search_details.layout = QVBoxLayout(self.search_details)

    self.open_student_data_widget_button = QPushButton('Edit students/profiles list')
    self.open_student_data_widget_button.setFont(combo_box_font)
    self.open_student_data_widget_button.clicked.connect(self.open_student_data_widget)
    self.open_student_data_widget_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    CurrentSearch.student_selector = QComboBox()
    CurrentSearch.student_selector.setFont(combo_box_font)

    students = self.get_available_students()
    if len(students) > 0:
      students[0:0] = ['Please select a student...']
      CurrentSearch.student_selector.addItems(students)
    else:
      CurrentSearch.student_selector.addItem('There are no students.')
      CurrentSearch.student_selector.setDisabled(True)

    CurrentSearch.profile_selector = QComboBox()
    CurrentSearch.profile_selector.setFont(combo_box_font)
    CurrentSearch.profile_selector.addItem('You have to select a student.')

    CurrentSearch.subject_selector = QComboBox()
    CurrentSearch.subject_selector.setFont(combo_box_font)
    CurrentSearch.subject_selector.addItem('You have to select a student and a profile.')

    CurrentSearch.profile_selector.setDisabled(True)
    CurrentSearch.subject_selector.setDisabled(True)

    self.search_details.layout.addWidget(self.open_student_data_widget_button, alignment=Qt.AlignmentFlag.AlignRight)
    self.search_details.layout.addWidget(CurrentSearch.student_selector)
    self.search_details.layout.addWidget(CurrentSearch.profile_selector)
    self.search_details.layout.addWidget(CurrentSearch.subject_selector)

    self.layout.addWidget(self.searched_word)
    self.layout.addSpacing(100)
    self.layout.addWidget(self.search_details)

    self.search_details.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
    self.searched_word.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    CurrentSearch.student_selector.activated.connect(self.student_selector_activated_initial)
    CurrentSearch.profile_selector.activated.connect(CurrentSearch.profile_selector_activated_initial)
    CurrentSearch.subject_selector.activated.connect(CurrentSearch.subject_selector_activated_initial)

    CurrentSearch.initialize_selected_student = False
    remember_last_student_picked = Settings.get_boolean_setting('remember_last_student_picked')
    last_student_picked = Settings.get_setting('last_student_picked')
    if remember_last_student_picked and last_student_picked in students:
      CurrentSearch.student_selector.setCurrentText(last_student_picked)
      CurrentSearch.initialize_selected_student = True
      CurrentSearch.student_selector_activated_initial(1)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.current_search_style)
    self.searched_word.setStyleSheet(Styles.searched_word_style)

  def get_current_word(self): # got to change
    return self.searched_word.text()

  def open_student_data_widget(self):
    from MainWidget.studentsDataEditingWidget import StudentsDataEditingWidget
    students_editing_dialog = StudentsDataEditingWidget()
    students_editing_dialog.exec()

  def get_available_students(self):
    from Common.databaseHandler import DBHandler
    students = DBHandler.get_students()
    return students

  @staticmethod
  def student_selector_activated_initial(index):
    if index != 0:
      CurrentSearch.student_selector.removeItem(0)
      CurrentSearch.student_selector.activated.disconnect()
      CurrentSearch.student_selector.activated.connect(CurrentSearch.student_selector_activated)
      CurrentSearch.profile_selector.removeItem(0)
      CurrentSearch.subject_selector.removeItem(0)
      CurrentSearch.last_student_picked = 'Please select a student...'
      CurrentSearch.student_selector_activated(0)

  @staticmethod
  def student_selector_activated(index):
    if CurrentSearch.student_selector.currentText() == CurrentSearch.last_student_picked: return

    if not CurrentSearch.initialize_selected_student:
      from MainWidget.mainWindow import MainWindow
      MainWindow.clear_previous_subject_details()

    CurrentSearch.initialize_selected_student = False

    CurrentSearch.last_student_picked = CurrentSearch.student_selector.currentText()
    Settings.set_setting('last_student_picked', CurrentSearch.last_student_picked)

    student_name = CurrentSearch.student_selector.currentText()
    CurrentSearch.profile_selector.clear()
    from Common.databaseHandler import DBHandler
    CurrentSearch.student_id, student_profiles = DBHandler.get_student_details(student_name)
    if len(student_profiles) == 0:
      CurrentSearch.profile_selector.addItem('This student has no profiles.')
      CurrentSearch.profile_selector.setDisabled(True)
    else:
      student_profiles[0:0] = ['Please select a profile...']
      CurrentSearch.profile_selector.addItems(student_profiles)
      CurrentSearch.profile_selector.setEnabled(True)

      CurrentSearch.profile_selector.activated.disconnect()
      CurrentSearch.profile_selector.activated.connect(CurrentSearch.profile_selector_activated_initial)

    CurrentSearch.subject_selector.clear()
    CurrentSearch.subject_selector.addItem('You have to select a profile.')
    CurrentSearch.subject_selector.setDisabled(True)

  @staticmethod
  def profile_selector_activated_initial(index):
    if index != 0:
      CurrentSearch.profile_selector.removeItem(0)
      CurrentSearch.profile_selector.activated.disconnect()
      CurrentSearch.profile_selector.activated.connect(CurrentSearch.profile_selector_activated)
      CurrentSearch.last_profile_picked = 'Please select a profile...'
      CurrentSearch.profile_selector_activated(0)

  @staticmethod
  def profile_selector_activated(index):
    if CurrentSearch.profile_selector.currentText() == CurrentSearch.last_profile_picked: return

    CurrentSearch.last_profile_picked = CurrentSearch.profile_selector.currentText()

    from MainWidget.mainWindow import MainWindow
    MainWindow.clear_previous_subject_details()
    CurrentSearch.profile_id, CurrentSearch.grade_id, grade_name, profile_subjects = DBHandler.get_profile_details(CurrentSearch.profile_selector.currentText())
    CurrentSearch.subject_selector.clear()
    CurrentSearch.subject_selector.addItem('Please select a subject...')
    CurrentSearch.subject_selector.addItems(profile_subjects)

    if len(profile_subjects) > 1:
      CurrentSearch.subject_selector.addItem('All Subjects')

    CurrentSearch.subject_selector.activated.disconnect()
    CurrentSearch.subject_selector.activated.connect(CurrentSearch.subject_selector_activated_initial)
    CurrentSearch.subject_selector.setEnabled(True)

  @staticmethod
  def subject_selector_activated_initial(index):
    if index != 0:
      CurrentSearch.subject_selector.removeItem(0)
      CurrentSearch.subject_selector.activated.disconnect()
      CurrentSearch.subject_selector.activated.connect(CurrentSearch.subject_selector_activated)
      CurrentSearch.last_subject_picked = 'Please select a subject...'
      CurrentSearch.subject_selector_activated(CurrentSearch.subject_selector.currentIndex())

  @staticmethod
  def subject_selector_activated(index):
    if CurrentSearch.subject_selector.currentText() == CurrentSearch.last_subject_picked: return

    CurrentSearch.last_subject_picked = CurrentSearch.subject_selector.currentText()

    CurrentSearch.subject_selector_active = True
    from MainWidget.mainWindow import MainWindow
    MainWindow.update_widgets(CurrentSearch.profile_id, CurrentSearch.grade_id, CurrentSearch.subject_selector.currentText())

  @staticmethod
  def get_current_selection_details():
    return CurrentSearch.student_id, CurrentSearch.profile_id, CurrentSearch.grade_id, CurrentSearch.subject_selector.currentText()

  @staticmethod
  def add_student(student_name):
    if CurrentSearch.student_selector.currentText() == 'There are no students.':
      CurrentSearch.student_selector.setEnabled(True)
      CurrentSearch.student_selector.clear()
      CurrentSearch.student_selector.addItem('Please select a student...')
      CurrentSearch.student_selector.activated.disconnect()
      CurrentSearch.student_selector.activated.connect(CurrentSearch.student_selector_activated_initial)

    CurrentSearch.student_selector.addItem(student_name)

  @staticmethod
  def update_student(old_student_name, new_student_name):
    index = CurrentSearch.student_selector.findText(old_student_name)
    CurrentSearch.student_selector.setItemText(index, new_student_name)

  @staticmethod
  def remove_student(student_name):
    index = CurrentSearch.student_selector.findText(student_name)
    current_index = CurrentSearch.student_selector.currentIndex()
    CurrentSearch.student_selector.removeItem(index)

    if (CurrentSearch.student_selector.count() == 0
        or (CurrentSearch.student_selector.count() == 1 and CurrentSearch.student_selector.currentText() == 'Please select a student...')):
      CurrentSearch.student_selector.clear()
      CurrentSearch.student_selector.addItem('There are no students.')
      CurrentSearch.student_selector.setDisabled(True)
      CurrentSearch.profile_selector.setDisabled(True)
      CurrentSearch.profile_selector.clear()
      CurrentSearch.profile_selector.addItem('You have to select a student.')
      CurrentSearch.subject_selector.clear()
      CurrentSearch.subject_selector.setDisabled(True)
      CurrentSearch.subject_selector.addItem('You have to select a student and a profile.')
    elif index == current_index:
      CurrentSearch.student_selector_activated(CurrentSearch.student_selector.currentIndex())

  @staticmethod
  def add_profiles(profile_names):
    if len(profile_names) == 0: return

    if CurrentSearch.profile_selector.currentText() == 'This student has no profiles.':
      CurrentSearch.profile_selector.setEnabled(True)
      CurrentSearch.profile_selector.clear()
      CurrentSearch.profile_selector.addItem('Please select a profile...')
      CurrentSearch.profile_selector.activated.disconnect()
      CurrentSearch.profile_selector.activated.connect(CurrentSearch.profile_selector_activated_initial)

    CurrentSearch.profile_selector.addItems(profile_names)

  @staticmethod
  def update_profile(old_profile_name, new_profile_name):
    index = CurrentSearch.profile_selector.findText(old_profile_name)
    if index != -1:
      CurrentSearch.profile_selector.setItemText(index, new_profile_name)

  @staticmethod
  def remove_profiles(profile_names):
    if len(profile_names) == 0: return

    text = CurrentSearch.profile_selector.currentText()

    for profile_name in profile_names:
      index = CurrentSearch.profile_selector.findText(profile_name)
      if index != -1:
        CurrentSearch.profile_selector.removeItem(index)

    if (CurrentSearch.profile_selector.count() == 0
        or (CurrentSearch.profile_selector.count() == 1 and CurrentSearch.profile_selector.currentText() == 'Please select a profile...')):
      CurrentSearch.profile_selector.clear()
      CurrentSearch.profile_selector.addItem('This student has no profiles.')
      CurrentSearch.profile_selector.setDisabled(True)
      CurrentSearch.subject_selector.clear()
      CurrentSearch.subject_selector.setDisabled(True)
      CurrentSearch.subject_selector.addItem('You have to select a student and a profile.')
    elif text != CurrentSearch.profile_selector.currentText():
      CurrentSearch.profile_selector_activated(CurrentSearch.profile_selector.currentIndex())

  @staticmethod
  def add_subjects(subject_names):
    if CurrentSearch.subject_selector.findText('All Subjects') != -1:
      CurrentSearch.subject_selector.removeItem(CurrentSearch.subject_selector.count() - 1)

    subject_names.append('All Subjects')
    CurrentSearch.subject_selector.addItems(subject_names)

  @staticmethod
  def remove_subjects(subject_names):
    if len(subject_names) == 0: return

    text = CurrentSearch.subject_selector.currentText()

    for subject_name in subject_names:
      index = CurrentSearch.subject_selector.findText(subject_name)
      CurrentSearch.subject_selector.removeItem(index)

    if text != CurrentSearch.subject_selector.currentText():
      CurrentSearch.subject_selector_activated(CurrentSearch.subject_selector.currentIndex())
