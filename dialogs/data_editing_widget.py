from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QDialog
from PyQt6.QtGui import QIcon

from dialogs.profile_addition_widget import ProfileAdditionWIdget
from dialogs.profile_update_widget import ProfileUpdateWidget
from dialogs.student_addition_widget import StudentAdditionWidget
from dialogs.student_update_widget import StudentUpdateWidget
from menu.settings import Settings

class DataEditingWidget(QDialog):
  EDIT_DATA_TEXT = 'Επεξεργασία Δεδομένων'
  ADD_STUDENT_TEXT = 'Προσθήκη Μαθητή'
  EDIT_STUDENT_TEXT = 'Επεξεργασία Μαθητή'
  ADD_PROFILE_TEXT = 'Προσθήκη Προφίλ'
  EDIT_PROFILE_TEXT = 'Επεξεργασία Προφίλ'

  def __init__(self):
    super().__init__()
    self.setWindowTitle(DataEditingWidget.EDIT_DATA_TEXT)
    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setFixedWidth(Settings.get_setting('screen_width') / 2)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    add_student_widget = StudentAdditionWidget()
    DataEditingWidget.edit_student_widget = StudentUpdateWidget()
    add_profile_widget = ProfileAdditionWIdget()
    edit_profiles_widget = ProfileUpdateWidget()

    tab_widget = QTabWidget()
    tab_widget.addTab(add_student_widget, DataEditingWidget.ADD_STUDENT_TEXT)
    tab_widget.addTab(DataEditingWidget.edit_student_widget, DataEditingWidget.EDIT_STUDENT_TEXT)
    tab_widget.addTab(add_profile_widget, DataEditingWidget.ADD_PROFILE_TEXT)
    tab_widget.addTab(edit_profiles_widget, DataEditingWidget.EDIT_PROFILE_TEXT)

    self.layout.addWidget(tab_widget)

  @staticmethod
  def update_student_update_widget():
    DataEditingWidget.edit_student_widget.update_student_update_widget()