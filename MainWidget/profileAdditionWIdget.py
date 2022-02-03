from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QComboBox, QSizePolicy, QMessageBox
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

from Common.databaseHandler import DBHandler
from MenuBar.settings import Settings

class ProfileAdditionWIdget(QWidget):
  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    self.setFixedSize(Settings.getScreenWidth() / 2, Settings.getScreenHeight() / 2)

    sectionLabelFont = QFont(Settings.font, 16)
    comboBoxFont = QFont(Settings.font, 14)
    checkBoxFont = QFont(Settings.font, 14)
    lineEditFont = QFont(Settings.font, 14)

    nameWidget = QGroupBox('Profile Name')
    nameWidget.setFont(sectionLabelFont)
    nameWidget.layout = QHBoxLayout(nameWidget)
    nameWidget.layout.setContentsMargins(10, 0, 0, 0)

    self.nameLineEdit = QLineEdit()
    self.nameLineEdit.setFont(lineEditFont)
    nameWidget.layout.addWidget(self.nameLineEdit)

    gradeSelectionWidget = QGroupBox('Grade Selection')
    gradeSelectionWidget.setFont(sectionLabelFont)
    gradeSelectionWidget.layout = QHBoxLayout(gradeSelectionWidget)
    gradeSelectionWidget.layout.setContentsMargins(10, 10, 10, 10)

    grades = DBHandler.getGrades()

    self.gradeSelector = QComboBox()
    self.gradeSelector.setFont(comboBoxFont)
    self.gradeSelector.addItems(grades)
    self.gradeSelector.activated.connect(self.gradeSelectorActivated)

    gradeSelectionWidget.layout.addWidget(self.gradeSelector)

    subjectsWidget = QGroupBox('Subject Selection')
    subjectsWidget.setFont(sectionLabelFont)
    subjectsWidget.layout = QHBoxLayout(subjectsWidget)
    subjectsWidget.layout.setContentsMargins(10, 0, 0, 0)

    self.subjectsSelectionWidget = QWidget()
    self.subjectsSelectionWidget.layout = QGridLayout(self.subjectsSelectionWidget)

    scrollArea = QScrollArea()
    scrollArea.setWidgetResizable(True)
    scrollArea.setWidget(self.subjectsSelectionWidget)
    scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.subjectsSelectionWidget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    gradeSubjects = DBHandler.getGradeSubjects(1)

    self.checkBoxes = []
    for i in range(len(gradeSubjects)):
      checkBox = QCheckBox(gradeSubjects[i])
      checkBox.setFont(checkBoxFont)
      self.checkBoxes.append(checkBox)
      self.subjectsSelectionWidget.layout.addWidget(checkBox, i, 0)

    vspacer = QLabel("f")
    invisibleFont = QFont(Settings.font, 1)
    vspacer.setFont(invisibleFont)
    sizePolicy = vspacer.sizePolicy()
    sizePolicy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(sizePolicy)
    self.subjectsSelectionWidget.layout.addWidget(vspacer, 1000, 0)

    subjectsWidget.layout.addWidget(scrollArea)

    self.saveButton = QPushButton('Save New Profile')
    self.saveButton.pressed.connect(self.saveProfile)

    self.layout.addWidget(nameWidget)
    self.layout.addWidget(gradeSelectionWidget)
    self.layout.addWidget(subjectsWidget)
    self.layout.addSpacing(10)
    self.layout.addWidget(self.saveButton, alignment=Qt.AlignmentFlag.AlignRight)
    self.layout.addSpacing(10)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.profileAdditionStyle)

  def gradeSelectorActivated(self, index):
    for checkbox in self.checkBoxes:
      self.subjectsSelectionWidget.layout.removeWidget(checkbox)

    gradeSubjects = DBHandler.getGradeSubjects(index + 1)

    checkBoxFont = QFont(Settings.font, 14)
    self.checkBoxes = []
    for i in range(len(gradeSubjects)):
      checkBox = QCheckBox(gradeSubjects[i])
      checkBox.setFont(checkBoxFont)
      self.checkBoxes.append(checkBox)
      self.subjectsSelectionWidget.layout.addWidget(checkBox, i, 0)

  def saveProfile(self):
    isInvalid, text = self.profileIsInvalid()

    if isInvalid:
      title = 'Error Saving Profile'
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    profileName = self.nameLineEdit.text()
    QTimer.singleShot(0, self.nameLineEdit.clear)

    subjects = []
    for checkBox in self.checkBoxes:
      if checkBox.isChecked():
        subjects.append(checkBox.text())
        checkBox.setChecked(False)

    DBHandler.addProfile(profileName, self.gradeSelector.currentIndex() + 1, subjects)

    from MainWidget.profileUpdateWidget import ProfileUpdateWidget
    ProfileUpdateWidget.addProfile(profileName)

    from MainWidget.studentAdditionWidget import StudentAdditionWidget
    StudentAdditionWidget.addProfile(profileName)

    from MainWidget.studentUpdateWidget import StudentUpdateWidget
    StudentUpdateWidget.addProfile(profileName)

  def profileIsInvalid(self):
    profileName = self.nameLineEdit.text()
    if len(profileName) == 0:
      return True, 'Profile can not be saved because the profile name is empty.'

    if DBHandler.profileNameExists(profileName):
      return True, 'Profile can not be saved as this name is already used for another profile.'

    for checkBox in self.checkBoxes:
      if checkBox.isChecked():
        return False, ''

    return True, 'Profile can not be saved because none of the grade subjects have been selected.'
