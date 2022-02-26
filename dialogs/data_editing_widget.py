from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QDialog
from PyQt6.QtGui import QIcon

from dialogs.profile_addition_widget import ProfileAdditionWIdget
from dialogs.profile_update_widget import ProfileUpdateWidget
from dialogs.student_addition_widget import StudentAdditionWidget
from dialogs.student_update_widget import StudentUpdateWidget
from menu.settings import Settings

class DataEditingWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Edit Data')
    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setFixedWidth(Settings.get_setting('screen_width') / 2)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    add_student_widget = StudentAdditionWidget()
    edit_student_widget = StudentUpdateWidget()
    add_profile_widget = ProfileAdditionWIdget()
    edit_profiles_widget = ProfileUpdateWidget()

    tab_widget = QTabWidget()
    tab_widget.addTab(add_student_widget, 'Add a new student')
    tab_widget.addTab(edit_student_widget, 'Update existing student')
    tab_widget.addTab(add_profile_widget, 'Add a new profile')
    tab_widget.addTab(edit_profiles_widget, 'Update existing profile')

    self.layout.addWidget(tab_widget)
