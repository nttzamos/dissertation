from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from Common.databaseHandler import DBHandler
from MenuBar.settings import Settings

class StudentAdditionWidget(QWidget):
  lastIndexUsed = -1

  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    sectionLabelFont = QFont(Settings.font, 16)
    checkBoxFont = QFont(Settings.font, 14)
    lineEditFont = QFont(Settings.font, 14)

    nameWidget = QGroupBox('Student Name')
    nameWidget.setFont(sectionLabelFont)
    nameWidget.layout = QHBoxLayout(nameWidget)
    nameWidget.layout.setContentsMargins(10, 5, 10, 10)

    self.nameLineEdit = QLineEdit()
    self.nameLineEdit.setFont(lineEditFont)
    nameWidget.layout.addWidget(self.nameLineEdit)

    profilesWidget = QGroupBox('Profile Selection')
    profilesWidget.setFont(sectionLabelFont)
    profilesWidget.layout = QHBoxLayout(profilesWidget)
    profilesWidget.layout.setContentsMargins(10, 5, 10, 10)

    StudentAdditionWidget.profilesSelectionWidget = QWidget()
    StudentAdditionWidget.profilesSelectionWidget.layout = QGridLayout(StudentAdditionWidget.profilesSelectionWidget)

    scrollArea = QScrollArea()
    scrollArea.setWidgetResizable(True)
    scrollArea.setWidget(StudentAdditionWidget.profilesSelectionWidget)
    scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    profiles = DBHandler.getProfiles()

    StudentAdditionWidget.checkBoxes = []
    for i in range(len(profiles)):
      checkBox = QCheckBox(profiles[i])
      checkBox.setFont(checkBoxFont)
      StudentAdditionWidget.checkBoxes.append(checkBox)
      StudentAdditionWidget.profilesSelectionWidget.layout.addWidget(checkBox, i, 0)
      StudentAdditionWidget.lastIndexUsed = i

    vspacer = QLabel("f")
    invisibleFont = QFont(Settings.font, 1)
    vspacer.setFont(invisibleFont)
    sizePolicy = vspacer.sizePolicy()
    sizePolicy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(sizePolicy)
    StudentAdditionWidget.profilesSelectionWidget.layout.addWidget(vspacer, 1000, 0)

    profilesWidget.layout.addWidget(scrollArea)

    saveButton = QPushButton('Save New Student')
    saveButton.pressed.connect(self.saveStudent)

    self.layout.addWidget(nameWidget)
    self.layout.addWidget(profilesWidget)
    self.layout.addSpacing(15)
    self.layout.addWidget(saveButton, alignment=Qt.AlignmentFlag.AlignRight)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.studentAdditionStyle)

  def saveStudent(self):
    isInvalid, text = self.studentIsInvalid()

    if isInvalid:
      title = 'Error Saving Student'
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    studentName = self.nameLineEdit.text()
    QTimer.singleShot(0, self.nameLineEdit.clear)

    checkedProfiles = []
    for checkBox in StudentAdditionWidget.checkBoxes:
      if checkBox.isChecked():
        checkedProfiles.append(checkBox.text())
        checkBox.setChecked(False)

    DBHandler.addStudent(studentName, checkedProfiles)

    from MainWidget.studentUpdateWidget import StudentUpdateWidget
    StudentUpdateWidget.addStudent(studentName)

    from MainWidget.currentSearch import CurrentSearch
    CurrentSearch.addStudent(studentName)

  def studentIsInvalid(self):
    studentName = self.nameLineEdit.text()
    if len(studentName) == 0:
      return True, 'Student can not be saved because the profile name is empty.'

    if DBHandler.studentNameExists(studentName):
      return True, 'Student can not be saved as this name is already used for another profile.'

    for checkBox in StudentAdditionWidget.checkBoxes:
      if checkBox.isChecked():
        return False, ''

    return True, 'Student can not be saved because none of the profiles have been selected.'

  @staticmethod
  def addProfile(profileName):
    checkBox = QCheckBox(profileName)
    checkBoxFont = QFont(Settings.font, 14)
    checkBox.setFont(checkBoxFont)
    StudentAdditionWidget.checkBoxes.append(checkBox)
    StudentAdditionWidget.lastIndexUsed += 1
    StudentAdditionWidget.profilesSelectionWidget.layout.addWidget(checkBox, StudentAdditionWidget.lastIndexUsed, 0)

  @staticmethod
  def updateProfile(oldProfileName, newProfileName):
    for checkBox in StudentAdditionWidget.checkBoxes:
      if checkBox.text() == oldProfileName:
        checkBox.setText(newProfileName)
        return

  @staticmethod
  def removeProfile(profileName):
    for checkBox in StudentAdditionWidget.checkBoxes:
      if checkBox.text() == profileName:
        StudentAdditionWidget.profilesSelectionWidget.layout.removeWidget(checkBox)
        StudentAdditionWidget.checkBoxes.remove(checkBox)
        return
