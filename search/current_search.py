from PyQt6.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QSizePolicy,
                             QVBoxLayout, QWidget, QPushButton)
from PyQt6.QtCore import Qt

from menu.settings import Settings
from models.profile import get_profile_details
from models.student import get_students, get_student_details
from shared.font_settings import FontSettings
from shared.spacer import Spacer

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('search', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class CurrentSearch(QWidget):
  def __init__(self):
    super().__init__()

    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(50, 50, 50, 50)

    CurrentSearch.subject_selector_active = False
    CurrentSearch.grade_id = -1

    searched_word_font = FontSettings.get_font('heading')
    combo_box_font = FontSettings.get_font('text')
    button_font = FontSettings.get_font('button')

    searched_word_label_container = QWidget()
    searched_word_label_container.layout = QHBoxLayout(searched_word_label_container)
    searched_word_label_container.layout.setContentsMargins(0, 0, 0, 0)
    searched_word_label_container.layout.setSpacing(0)

    CurrentSearch.searched_word_label = QLabel(_('UNINITIALIZED_STATE_TEXT'))
    CurrentSearch.searched_word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    CurrentSearch.searched_word_label.setWordWrap(True)
    CurrentSearch.searched_word_label.setFont(searched_word_font)
    CurrentSearch.searched_word_label.setTextInteractionFlags(
      Qt.TextInteractionFlag.TextSelectableByMouse
    )
    CurrentSearch.searched_word_label.setSizePolicy(
      QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
    )

    spacer1 = Spacer()
    spacer1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    spacer2 = Spacer()
    spacer2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    searched_word_label_container.layout.addWidget(spacer1)
    searched_word_label_container.layout.addWidget(CurrentSearch.searched_word_label)
    searched_word_label_container.layout.addWidget(spacer2)

    search_details = QWidget()
    search_details.layout = QVBoxLayout(search_details)

    open_data_editing_widget_button = QPushButton(_('EDIT_DATA_BUTTON_TEXT'))
    open_data_editing_widget_button.setToolTip(_('EDIT_DATA_TOOLTIP_TEXT'))
    open_data_editing_widget_button.setFont(button_font)
    open_data_editing_widget_button.clicked.connect(self.open_data_editing_widget)
    open_data_editing_widget_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    CurrentSearch.student_selector = QComboBox()
    CurrentSearch.student_selector.setFont(combo_box_font)

    students = get_students()
    if len(students) > 0:
      students[0:0] = [_('SELECT_STUDENT_TEXT')]
      CurrentSearch.student_selector.addItems(students)
    else:
      CurrentSearch.student_selector.addItem(_('NO_STUDENTS_TEXT'))
      CurrentSearch.student_selector.setDisabled(True)

    CurrentSearch.profile_selector = QComboBox()
    CurrentSearch.profile_selector.setFont(combo_box_font)
    CurrentSearch.profile_selector.addItem(_('SELECT_PROFILE_TEXT'))

    CurrentSearch.subject_selector = QComboBox()
    CurrentSearch.subject_selector.setFont(combo_box_font)
    CurrentSearch.subject_selector.addItem(_('SELECT_SUBJECT_TEXT'))

    CurrentSearch.profile_selector.setDisabled(True)
    CurrentSearch.subject_selector.setDisabled(True)

    search_details.layout.addWidget(open_data_editing_widget_button, alignment=Qt.AlignmentFlag.AlignRight)
    search_details.layout.addWidget(CurrentSearch.student_selector)
    search_details.layout.addWidget(CurrentSearch.profile_selector)
    search_details.layout.addWidget(CurrentSearch.subject_selector)
    search_details.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    self.layout.addWidget(searched_word_label_container)
    self.layout.addWidget(search_details)

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
    from shared.styles import Styles
    self.setStyleSheet(Styles.current_search_style)
    CurrentSearch.searched_word_label.setStyleSheet(Styles.searched_word_style)

  def open_data_editing_widget(self):
    from dialogs.data_editing_widget import DataEditingWidget
    students_editing_dialog = DataEditingWidget()
    students_editing_dialog.exec()

  @staticmethod
  def clear_current_search_details():
    CurrentSearch.searched_word_label.setText(_('UNINITIALIZED_STATE_TEXT'))

    CurrentSearch.student_selector.clear()
    CurrentSearch.student_selector.addItem(_('NO_STUDENTS_TEXT'))
    CurrentSearch.student_selector.setDisabled(True)

    CurrentSearch.profile_selector.clear()
    CurrentSearch.profile_selector.addItem(_('SELECT_PROFILE_TEXT'))
    CurrentSearch.profile_selector.setDisabled(True)

    CurrentSearch.subject_selector.clear()
    CurrentSearch.subject_selector.addItem(_('SELECT_SUBJECT_TEXT'))
    CurrentSearch.subject_selector.setDisabled(True)

  @staticmethod
  def student_selector_activated_initial(index):
    if index != 0:
      CurrentSearch.student_selector.removeItem(0)
      CurrentSearch.student_selector.activated.disconnect()
      CurrentSearch.student_selector.activated.connect(CurrentSearch.student_selector_activated)
      CurrentSearch.profile_selector.removeItem(0)
      CurrentSearch.subject_selector.removeItem(0)
      CurrentSearch.last_student_picked = _('SELECT_STUDENT_TEXT')
      CurrentSearch.student_selector_activated(0)

  @staticmethod
  def student_selector_activated(index):
    if CurrentSearch.student_selector.currentText() == CurrentSearch.last_student_picked: return

    if not CurrentSearch.initialize_selected_student:
      from central.main_window import MainWindow
      MainWindow.clear_previous_subject_details()
      CurrentSearch.searched_word_label.setText(_('UNINITIALIZED_STATE_TEXT'))

    CurrentSearch.initialize_selected_student = False

    CurrentSearch.last_student_picked = CurrentSearch.student_selector.currentText()
    Settings.set_setting('last_student_picked', CurrentSearch.last_student_picked)

    student_name = CurrentSearch.student_selector.currentText()

    CurrentSearch.profile_selector.clear()
    CurrentSearch.student_id, student_profiles = get_student_details(student_name)

    if len(student_profiles) == 0:
      CurrentSearch.profile_selector.addItem(_('STUDENT_NO_PROFILES_TEXT'))
      CurrentSearch.profile_selector.setDisabled(True)
    else:
      student_profiles[0:0] = [_('SELECT_PROFILE_TEXT')]
      CurrentSearch.profile_selector.addItems(student_profiles)
      CurrentSearch.profile_selector.setEnabled(True)

      CurrentSearch.profile_selector.activated.disconnect()
      CurrentSearch.profile_selector.activated.connect(
        CurrentSearch.profile_selector_activated_initial
      )

    CurrentSearch.subject_selector.clear()
    CurrentSearch.subject_selector.addItem(_('SELECT_SUBJECT_TEXT'))
    CurrentSearch.subject_selector.setDisabled(True)

  @staticmethod
  def profile_selector_activated_initial(index):
    if index != 0:
      CurrentSearch.profile_selector.removeItem(0)
      CurrentSearch.profile_selector.activated.disconnect()
      CurrentSearch.profile_selector.activated.connect(CurrentSearch.profile_selector_activated)
      CurrentSearch.last_profile_picked = _('SELECT_PROFILE_TEXT')
      CurrentSearch.profile_selector_activated(0)

  @staticmethod
  def profile_selector_activated(index):
    if CurrentSearch.profile_selector.currentText() == CurrentSearch.last_profile_picked: return

    CurrentSearch.last_profile_picked = CurrentSearch.profile_selector.currentText()

    from central.main_window import MainWindow
    MainWindow.clear_previous_subject_details()
    CurrentSearch.searched_word_label.setText(_('UNINITIALIZED_STATE_TEXT'))
    CurrentSearch.profile_id, CurrentSearch.grade_id, grade_name, profile_subjects = (
      get_profile_details(CurrentSearch.profile_selector.currentText())
    )

    CurrentSearch.subject_selector.clear()
    CurrentSearch.subject_selector.addItem(_('SELECT_SUBJECT_TEXT'))
    CurrentSearch.subject_selector.addItems(profile_subjects)

    if len(profile_subjects) > 1:
      CurrentSearch.subject_selector.addItem(_('ALL_SUBJECTS_TEXT'))

    CurrentSearch.subject_selector.activated.disconnect()
    CurrentSearch.subject_selector.activated.connect(
      CurrentSearch.subject_selector_activated_initial
    )

    CurrentSearch.subject_selector.setEnabled(True)

  @staticmethod
  def subject_selector_activated_initial(index):
    if index != 0:
      CurrentSearch.subject_selector.removeItem(0)
      CurrentSearch.subject_selector.activated.disconnect()
      CurrentSearch.subject_selector.activated.connect(CurrentSearch.subject_selector_activated)
      CurrentSearch.last_subject_picked = _('SELECT_SUBJECT_TEXT')
      CurrentSearch.subject_selector_activated(CurrentSearch.subject_selector.currentIndex())

  @staticmethod
  def subject_selector_activated(index):
    if CurrentSearch.subject_selector.currentText() == CurrentSearch.last_subject_picked: return

    CurrentSearch.last_subject_picked = CurrentSearch.subject_selector.currentText()

    CurrentSearch.subject_selector_active = True
    from central.main_window import MainWindow
    MainWindow.update_widgets(
      CurrentSearch.profile_id, CurrentSearch.subject_selector.currentText()
    )

  @staticmethod
  def update_searched_word(word, new_word):
    if CurrentSearch.searched_word_label.text() == word:
      CurrentSearch.searched_word_label.setText(new_word)

  @staticmethod
  def remove_searched_word(word):
    if CurrentSearch.searched_word_label.text() == word:
      CurrentSearch.searched_word_label.setText(_('UNINITIALIZED_STATE_TEXT'))
      from central.results_widget import ResultsWidget
      ResultsWidget.show_placeholder()

  @staticmethod
  def remove_searched_word():
    CurrentSearch.searched_word_label.setText(_('UNINITIALIZED_STATE_TEXT'))
    from central.results_widget import ResultsWidget
    ResultsWidget.show_placeholder()

  @staticmethod
  def get_current_selection_details():
    return (
      CurrentSearch.student_id, CurrentSearch.profile_id,
      CurrentSearch.grade_id, CurrentSearch.subject_selector.currentText()
    )

  @staticmethod
  def add_student(student_name):
    if CurrentSearch.student_selector.currentText() == _('NO_STUDENTS_TEXT'):
      CurrentSearch.student_selector.setEnabled(True)
      CurrentSearch.student_selector.clear()
      CurrentSearch.student_selector.addItem(_('SELECT_STUDENT_TEXT'))
      CurrentSearch.student_selector.activated.disconnect()
      CurrentSearch.student_selector.activated.connect(
        CurrentSearch.student_selector_activated_initial
      )

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

    if (CurrentSearch.student_selector.count() == 0 or
        (CurrentSearch.student_selector.count() == 1 and
         CurrentSearch.student_selector.currentText() == _('SELECT_STUDENT_TEXT'))):

      CurrentSearch.student_selector.clear()
      CurrentSearch.student_selector.addItem(_('NO_STUDENTS_TEXT'))
      CurrentSearch.student_selector.setDisabled(True)
      CurrentSearch.profile_selector.setDisabled(True)
      CurrentSearch.profile_selector.clear()
      CurrentSearch.profile_selector.addItem(_('SELECT_PROFILE_TEXT'))
      CurrentSearch.subject_selector.clear()
      CurrentSearch.subject_selector.setDisabled(True)
      CurrentSearch.subject_selector.addItem(_('SELECT_SUBJECT_TEXT'))
    elif index == current_index:
      CurrentSearch.student_selector_activated(CurrentSearch.student_selector.currentIndex())

  @staticmethod
  def add_profiles(profile_names):
    if len(profile_names) == 0: return

    if CurrentSearch.profile_selector.currentText() == _('STUDENT_NO_PROFILES_TEXT'):
      CurrentSearch.profile_selector.setEnabled(True)
      CurrentSearch.profile_selector.clear()
      CurrentSearch.profile_selector.addItem(_('SELECT_PROFILE_TEXT'))
      CurrentSearch.profile_selector.activated.disconnect()
      CurrentSearch.profile_selector.activated.connect(
        CurrentSearch.profile_selector_activated_initial
      )

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

    if (CurrentSearch.profile_selector.count() == 0 or
        (CurrentSearch.profile_selector.count() == 1 and
         CurrentSearch.profile_selector.currentText() == _('SELECT_PROFILE_TEXT'))):

      CurrentSearch.profile_selector.clear()
      CurrentSearch.profile_selector.addItem(_('STUDENT_NO_PROFILES_TEXT'))
      CurrentSearch.profile_selector.setDisabled(True)
      CurrentSearch.subject_selector.clear()
      CurrentSearch.subject_selector.setDisabled(True)
      CurrentSearch.subject_selector.addItem(_('SELECT_SUBJECT_TEXT'))
    elif text != CurrentSearch.profile_selector.currentText():
      CurrentSearch.profile_selector_activated(CurrentSearch.profile_selector.currentIndex())

  @staticmethod
  def add_subjects(subject_names):
    if CurrentSearch.subject_selector.findText(_('ALL_SUBJECTS_TEXT')) != -1:
      CurrentSearch.subject_selector.removeItem(CurrentSearch.subject_selector.count() - 1)

    subject_names.append(_('ALL_SUBJECTS_TEXT'))
    CurrentSearch.subject_selector.addItems(subject_names)

  @staticmethod
  def remove_subjects(subject_names):
    if len(subject_names) == 0: return

    text = CurrentSearch.subject_selector.currentText()

    for subject_name in subject_names:
      index = CurrentSearch.subject_selector.findText(subject_name)
      CurrentSearch.subject_selector.removeItem(index)

    if CurrentSearch.subject_selector.count() == 2:
      index = CurrentSearch.subject_selector.findText(_('ALL_SUBJECTS_TEXT'))
      CurrentSearch.subject_selector.removeItem(index)

    if text != CurrentSearch.subject_selector.currentText():
      CurrentSearch.subject_selector_activated(CurrentSearch.subject_selector.currentIndex())
