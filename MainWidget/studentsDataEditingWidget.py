from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QDialog
# from PyQt6.QtCore import QStringListModel, QTimer, Qt
from PyQt6.QtGui import QIcon, QFont

from MenuBar.settings import Settings
from MainWidget.studentAdditionWidget import StudentAdditionWidget
from MainWidget.studentUpdateWidget import StudentUpdateWidget
from MainWidget.profileAdditionWIdget import ProfileAdditionWIdget
from MainWidget.profileUpdateWidget import ProfileUpdateWidget

class StudentsDataEditingWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Edit Students List')
    self.setWindowIcon(QIcon('Resources/windowIcon.svg'))
    self.setFixedWidth(Settings.get_screen_width() / 2)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    combo_box_font = QFont(Settings.font, 14)

    # Add a new student widget
    add_studentWidget = StudentAdditionWidget()

    # Edit existing students widget
    editStudentWidget = StudentUpdateWidget()

    # Add a new profile widget
    add_profileWidget = ProfileAdditionWIdget()

    # Edit existing profiles widget
    editprofiles_widget = ProfileUpdateWidget()

    tabwidget = QTabWidget()
    tabwidget.addTab(add_studentWidget, 'Add a new student')
    tabwidget.addTab(editStudentWidget, 'Update existing student')
    tabwidget.addTab(add_profileWidget, 'Add a new profile')
    tabwidget.addTab(editprofiles_widget, 'Update Existing profile')

    self.layout.addWidget(tabwidget)
