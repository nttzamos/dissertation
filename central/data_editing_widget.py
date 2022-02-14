from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QDialog
from PyQt6.QtGui import QIcon

from menu.settings import Settings
from central.student_addition_widget import StudentAdditionWidget
from central.student_update_widget import StudentUpdateWidget
from central.profile_addition_widget import ProfileAdditionWIdget
from central.profile_update_widget import ProfileUpdateWidget

class DataEditingWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Edit Data')
    self.setWindowIcon(QIcon('resources/windowIcon.svg'))
    self.setFixedWidth(Settings.get_setting('screen_width') / 2)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    # Add a new student widget
    add_student_widget = StudentAdditionWidget()

    # Edit existing students widget
    edit_student_widget = StudentUpdateWidget()

    # Add a new profile widget
    add_profile_widget = ProfileAdditionWIdget()

    # Edit existing profiles widget
    edit_profiles_widget = ProfileUpdateWidget()

    tab_widget = QTabWidget()
    tab_widget.addTab(add_student_widget, 'Add a new student')
    tab_widget.addTab(edit_student_widget, 'Update existing student')
    tab_widget.addTab(add_profile_widget, 'Add a new profile')
    tab_widget.addTab(edit_profiles_widget, 'Update existing profile')

    self.layout.addWidget(tab_widget)
