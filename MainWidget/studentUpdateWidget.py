from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QComboBox, QLineEdit, QSizePolicy, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from Common.databaseHandler import DBHandler
from MenuBar.settings import Settings

class StudentUpdateWidget(QWidget):
  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    self.setFixedSize(Settings.getScreenWidth() / 2, Settings.getScreenHeight() / 2)

    sectionLabelFont = QFont(Settings.font, 16)
    comboBoxFont = QFont(Settings.font, 14)
    lineEditFont = QFont(Settings.font, 14)

    studentSelectionWidget = QGroupBox('Student Selection')
    studentSelectionWidget.setFont(sectionLabelFont)
    studentSelectionWidget.layout = QHBoxLayout(studentSelectionWidget)
    studentSelectionWidget.layout.setContentsMargins(10, 10, 10, 10)

    students = DBHandler.getStudents()

    StudentUpdateWidget.studentSelector = QComboBox()
    StudentUpdateWidget.studentSelector.setFont(comboBoxFont)

    if len(students) == 0:
      StudentUpdateWidget.studentSelector.addItem('There are no students')
      StudentUpdateWidget.studentSelector.setDisabled(True)
    else:
      students[0:0] = ['Please select a student...']
      StudentUpdateWidget.studentSelector.addItems(students)

    StudentUpdateWidget.studentSelector.activated.connect(self.studentSelectorActivatedInitial)

    studentSelectionWidget.layout.addWidget(StudentUpdateWidget.studentSelector)

    self.nameWidget = QGroupBox('Student Name')
    self.nameWidget.setFont(sectionLabelFont)
    self.nameWidget.layout = QHBoxLayout(self.nameWidget)
    self.nameWidget.layout.setContentsMargins(10, 0, 0, 0)
    self.nameWidget.hide()

    self.nameLineEdit = QLineEdit()
    self.nameLineEdit.setFont(lineEditFont)
    self.nameWidget.layout.addWidget(self.nameLineEdit)

    profilesWidget = QGroupBox('Profile Selection')
    profilesWidget.setFont(sectionLabelFont)
    profilesWidget.layout = QHBoxLayout(profilesWidget)
    profilesWidget.layout.setContentsMargins(10, 10, 10, 10)

    StudentUpdateWidget.profilesSelectionWidget = QWidget()
    StudentUpdateWidget.profilesSelectionWidget.layout = QGridLayout(StudentUpdateWidget.profilesSelectionWidget)
    StudentUpdateWidget.profilesSelectionWidget.setDisabled(True)

    scrollArea = QScrollArea()
    scrollArea.setWidgetResizable(True)
    scrollArea.setWidget(StudentUpdateWidget.profilesSelectionWidget)
    scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    StudentUpdateWidget.profilesSelectionWidget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    StudentUpdateWidget.checkBoxes = []

    vspacer = QLabel("f")
    invisibleFont = QFont(Settings.font, 1)
    vspacer.setFont(invisibleFont)
    sizePolicy = vspacer.sizePolicy()
    sizePolicy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(sizePolicy)
    StudentUpdateWidget.profilesSelectionWidget.layout.addWidget(vspacer, 1000, 0)

    profilesWidget.layout.addWidget(scrollArea)

    self.saveButton = QPushButton('Update Student')
    self.saveButton.pressed.connect(self.updateStudent)
    self.saveButton.setDisabled(True)

    self.deleteButton = QPushButton('Delete Student')
    self.deleteButton.pressed.connect(self.deleteStudent)
    self.deleteButton.setDisabled(True)

    buttonsWidget = QWidget()
    buttonsWidget.layout = QHBoxLayout(buttonsWidget)
    buttonsWidget.layout.addWidget(self.deleteButton)
    buttonsWidget.layout.addWidget(self.saveButton)

    self.layout.addWidget(studentSelectionWidget)
    self.layout.addWidget(self.nameWidget)
    self.layout.addWidget(profilesWidget)
    self.layout.addSpacing(20)
    self.layout.addWidget(buttonsWidget, alignment=Qt.AlignmentFlag.AlignRight)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.studentUpdateStyle)

  def studentSelectorActivatedInitial(self, index):
    if index != 0:
      StudentUpdateWidget.studentSelector.removeItem(0)
      StudentUpdateWidget.studentSelector.activated.disconnect()
      StudentUpdateWidget.studentSelector.activated.connect(self.studentSelectorActivated)
      self.studentSelectorActivated(index - 1)
      self.saveButton.setEnabled(True)
      self.deleteButton.setEnabled(True)
      StudentUpdateWidget.profilesSelectionWidget.setEnabled(True)
      self.nameWidget.show()

  def studentSelectorActivated(self, index):
    studentName = StudentUpdateWidget.studentSelector.currentText()
    self.studentId, self.studentProfiles = DBHandler.getStudentDetails(studentName)
    self.nameLineEdit.setText(studentName)
    profiles = DBHandler.getProfiles()

    for checkBox in StudentUpdateWidget.checkBoxes:
      StudentUpdateWidget.profilesSelectionWidget.layout.removeWidget(checkBox)

    checkBoxFont = QFont(Settings.font, 14)
    StudentUpdateWidget.checkBoxes = []
    for i in range(len(profiles)):
      checkBox = QCheckBox(profiles[i])
      checkBox.setFont(checkBoxFont)
      StudentUpdateWidget.checkBoxes.append(checkBox)

      if profiles[i] in self.studentProfiles:
        checkBox.setChecked(True)

      StudentUpdateWidget.profilesSelectionWidget.layout.addWidget(checkBox, i, 0)
      StudentUpdateWidget.lastIndexUsed = i

  def updateStudent(self):
    isInvalid, text = self.studentIsInvalid()

    if isInvalid:
      title = 'Error Saving Student'
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    newStudentName = self.nameLineEdit.text()
    self.studentSelector.setItemText(self.studentSelector.currentIndex(), newStudentName)
    DBHandler.updateStudentName(self.studentId, newStudentName)

    profileNames = []
    for checkBox in StudentUpdateWidget.checkBoxes:
      if checkBox.isChecked():
        profileNames.append(checkBox.text())

    profileToRemove = list(set(self.studentProfiles) - set(profileNames))
    profilesToAdd = list(set(profileNames) - set(self.studentProfiles))
    DBHandler.addStudentProfiles(self.studentId, profilesToAdd)
    DBHandler.removeStudentProfiles(self.studentId, profileToRemove)

  def deleteStudent(self):
    DBHandler.removeStudent(self.studentId)
    for checkbox in StudentUpdateWidget.checkBoxes:
      StudentUpdateWidget.profilesSelectionWidget.layout.removeWidget(checkbox)

    StudentUpdateWidget.studentSelector.removeItem(StudentUpdateWidget.studentSelector.currentIndex())
    if StudentUpdateWidget.studentSelector.count() == 0:
      StudentUpdateWidget.studentSelector.addItem('There are no students')
      StudentUpdateWidget.studentSelector.setDisabled(True)
      StudentUpdateWidget.studentSelector.activated.disconnect()
      StudentUpdateWidget.studentSelector.activated.connect(self.studentSelectorActivatedInitial)
      self.nameWidget.hide()
      return

    self.studentSelectorActivated(0)

  def studentIsInvalid(self):
    studentName = self.nameLineEdit.text()
    if len(studentName) == 0:
      return True, 'Student can not be saved because the profile name is empty.'

    if StudentUpdateWidget.studentSelector.currentText() != studentName and  DBHandler.studentNameExists(studentName):
      return True, 'Student can not be saved as this name is already used for another profile.'

    for checkBox in StudentUpdateWidget.checkBoxes:
      if checkBox.isChecked():
        return False, ''

    return True, 'Student can not be saved because none of the profiles have been selected.'

  @staticmethod
  def addStudent(studentName):
    if StudentUpdateWidget.studentSelector.currentText() == 'There are no students':
      StudentUpdateWidget.studentSelector.setItemText(0, 'Please select a student...')
      StudentUpdateWidget.studentSelector.setEnabled(True)

    StudentUpdateWidget.studentSelector.addItem(studentName)

  @staticmethod
  def addProfile(profileName):
    if StudentUpdateWidget.studentSelector.currentText() == 'There are no students':
      return

    if StudentUpdateWidget.studentSelector.currentText() == 'Please select a student...':
      return

    checkBox = QCheckBox(profileName)
    checkBoxFont = QFont(Settings.font, 14)
    checkBox.setFont(checkBoxFont)
    StudentUpdateWidget.checkBoxes.append(checkBox)
    print(StudentUpdateWidget.lastIndexUsed)
    StudentUpdateWidget.lastIndexUsed += 1
    StudentUpdateWidget.profilesSelectionWidget.layout.addWidget(checkBox, StudentUpdateWidget.lastIndexUsed, 0)

  @staticmethod
  def updateProfile(oldProfileName, newProfileName):
    if len(StudentUpdateWidget.checkBoxes) == 0:
      return

    for checkBox in StudentUpdateWidget.checkBoxes:
      if checkBox.text() == oldProfileName:
        checkBox.setText(newProfileName)
        return

  @staticmethod
  def removeProfile(profileName):
    if len(StudentUpdateWidget.checkBoxes) == 0:
      return

    for checkBox in StudentUpdateWidget.checkBoxes:
      if checkBox.text() == profileName:
        StudentUpdateWidget.profilesSelectionWidget.layout.removeWidget(checkBox)
        StudentUpdateWidget.checkBoxes.remove(checkBox)
        return
