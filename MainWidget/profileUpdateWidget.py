from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QGroupBox, QScrollArea, QCheckBox, QPushButton, QComboBox, QSizePolicy, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from Common.databaseHandler import DBHandler
from MenuBar.settings import Settings

class ProfileUpdateWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    self.setFixedSize(Settings.getScreenWidth() / 2, Settings.getScreenHeight() - 150) # got to change

    sectionLabelFont = QFont(Settings.font, 16)
    comboBoxFont = QFont(Settings.font, 14)
    labelFont = QFont(Settings.font, 14)
    lineEditFont = QFont(Settings.font, 14)

    profileSelectionWidget = QGroupBox('Profile Selection')
    profileSelectionWidget.setFont(sectionLabelFont)
    profileSelectionWidget.layout = QHBoxLayout(profileSelectionWidget)
    profileSelectionWidget.layout.setContentsMargins(10, 10, 10, 10)

    profiles = DBHandler.getProfiles()

    ProfileUpdateWidget.profileSelector = QComboBox()
    ProfileUpdateWidget.profileSelector.setFont(comboBoxFont)

    if len(profiles) == 0:
      ProfileUpdateWidget.profileSelector.addItem('There are no profiles')
      ProfileUpdateWidget.profileSelector.setDisabled(True)
    else:
      profiles[0:0] = ['Please select a profile...']
      ProfileUpdateWidget.profileSelector.addItems(profiles)

    ProfileUpdateWidget.profileSelector.activated.connect(self.profileSelectorActivatedInitial)

    profileSelectionWidget.layout.addWidget(ProfileUpdateWidget.profileSelector)

    self.nameWidget = QGroupBox('Profile Name')
    self.nameWidget.setFont(sectionLabelFont)
    self.nameWidget.layout = QHBoxLayout(self.nameWidget)
    self.nameWidget.layout.setContentsMargins(10, 0, 0, 0)

    self.nameLineEdit = QLineEdit()
    self.nameLineEdit.setFont(lineEditFont)
    self.nameWidget.layout.addWidget(self.nameLineEdit)
    self.nameWidget.hide()

    gradeLabelWidget = QGroupBox('Profile Grade')
    gradeLabelWidget.setFont(sectionLabelFont)
    gradeLabelWidget.layout = QHBoxLayout(gradeLabelWidget)
    gradeLabelWidget.layout.setContentsMargins(10, 10, 10, 10)

    ProfileUpdateWidget.gradeLabel = QLabel('Please select a profile...')
    ProfileUpdateWidget.gradeLabel.setFont(labelFont)

    gradeLabelWidget.layout.addWidget(ProfileUpdateWidget.gradeLabel)

    subjectsWidget = QGroupBox('Subject Selection')
    subjectsWidget.setFont(sectionLabelFont)
    subjectsWidget.layout = QHBoxLayout(subjectsWidget)
    subjectsWidget.layout.setContentsMargins(10, 0, 0, 0)

    self.subjectsSelectionWidget = QWidget()
    self.subjectsSelectionWidget.layout = QGridLayout(self.subjectsSelectionWidget)
    self.subjectsSelectionWidget.setDisabled(True)

    scrollArea = QScrollArea()
    scrollArea.setWidgetResizable(True)
    scrollArea.setWidget(self.subjectsSelectionWidget)
    scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.subjectsSelectionWidget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    self.checkBoxes = []

    vspacer = QLabel("f")
    invisibleFont = QFont(Settings.font, 1)
    vspacer.setFont(invisibleFont)
    sizePolicy = vspacer.sizePolicy()
    sizePolicy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(sizePolicy)
    self.subjectsSelectionWidget.layout.addWidget(vspacer, 1000, 0)

    subjectsWidget.layout.addWidget(scrollArea)

    self.saveButton = QPushButton('Update Existing Profile')
    self.saveButton.pressed.connect(self.updateProfile)
    self.saveButton.setDisabled(True)

    self.deleteButton = QPushButton('Delete Profile')
    self.deleteButton.pressed.connect(self.deleteProfile)
    self.deleteButton.setDisabled(True)

    buttonsWidget = QWidget()
    buttonsWidget.layout = QHBoxLayout(buttonsWidget)
    buttonsWidget.layout.addWidget(self.deleteButton)
    buttonsWidget.layout.addWidget(self.saveButton)

    self.layout.addWidget(profileSelectionWidget)
    self.layout.addWidget(self.nameWidget)
    self.layout.addWidget(gradeLabelWidget)
    self.layout.addWidget(subjectsWidget)
    self.layout.addSpacing(10)
    self.layout.addWidget(buttonsWidget, alignment=Qt.AlignmentFlag.AlignRight)
    self.layout.addSpacing(10)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.profileUpdateStyle)

  def profileSelectorActivatedInitial(self, index):
    if index != 0:
      ProfileUpdateWidget.profileSelector.removeItem(0)
      ProfileUpdateWidget.profileSelector.activated.disconnect()
      ProfileUpdateWidget.profileSelector.activated.connect(self.profileSelectorActivated)
      self.profileSelectorActivated(index - 1)
      self.saveButton.setEnabled(True)
      self.deleteButton.setEnabled(True)
      self.subjectsSelectionWidget.setEnabled(True)
      self.nameWidget.show()

  def profileSelectorActivated(self, index):
    profileName = ProfileUpdateWidget.profileSelector.currentText()
    self.profileId, gradeId, gradeName, self.profileSubjectsIds = DBHandler.getProfileDetails(profileName)
    ProfileUpdateWidget.gradeLabel.setText(gradeName)
    self.nameLineEdit.setText(profileName)
    gradeSubjects = DBHandler.getGradeSubjects(gradeId)

    for checkbox in self.checkBoxes:
      self.subjectsSelectionWidget.layout.removeWidget(checkbox)

    checkBoxFont = QFont(Settings.font, 14)
    self.checkBoxes = []
    for i in range(len(gradeSubjects)):
      checkBox = QCheckBox(gradeSubjects[i])
      checkBox.setFont(checkBoxFont)
      self.checkBoxes.append(checkBox)

      if i + 1 in self.profileSubjectsIds:
        checkBox.setChecked(True)

      self.subjectsSelectionWidget.layout.addWidget(checkBox, i, 0)

  def updateProfile(self):
    isInvalid, text = self.profileIsInvalid()

    if isInvalid:
      title = 'Error Saving Profile'
      answer = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)
      if answer == QMessageBox.StandardButton.Ok:
        return

    newProfileName = self.nameLineEdit.text()

    from MainWidget.studentAdditionWidget import StudentAdditionWidget
    StudentAdditionWidget.updateProfile(ProfileUpdateWidget.profileSelector.currentText(), newProfileName)

    from MainWidget.studentUpdateWidget import StudentUpdateWidget
    StudentUpdateWidget.updateProfile(ProfileUpdateWidget.profileSelector.currentText(), newProfileName)

    self.profileSelector.setItemText(self.profileSelector.currentIndex(), newProfileName)
    DBHandler.updateProfileName(self.profileId, newProfileName)

    subjectsIds = []
    for i in range(len(self.checkBoxes)):
      if self.checkBoxes[i].isChecked():
        subjectsIds.append(i + 1)

    subjectsToRemove = list(set(self.profileSubjectsIds) - set(subjectsIds))
    subjectsToAdd = list(set(subjectsIds) - set(self.profileSubjectsIds))
    DBHandler.addProfileSubjects(self.profileId, subjectsToAdd)
    DBHandler.removeProfileSubjects(self.profileId, subjectsToRemove)

  def deleteProfile(self):
    DBHandler.removeProfile(self.profileId)
    for checkbox in self.checkBoxes:
      self.subjectsSelectionWidget.layout.removeWidget(checkbox)

    from MainWidget.studentAdditionWidget import StudentAdditionWidget
    StudentAdditionWidget.removeProfile(ProfileUpdateWidget.profileSelector.currentText())

    from MainWidget.studentUpdateWidget import StudentUpdateWidget
    StudentUpdateWidget.removeProfile(ProfileUpdateWidget.profileSelector.currentText())

    ProfileUpdateWidget.profileSelector.removeItem(ProfileUpdateWidget.profileSelector.currentIndex())
    if ProfileUpdateWidget.profileSelector.count() == 0:
      ProfileUpdateWidget.profileSelector.addItem('There are no profiles')
      ProfileUpdateWidget.profileSelector.setDisabled(True)
      ProfileUpdateWidget.profileSelector.activated.disconnect()
      ProfileUpdateWidget.profileSelector.activated.connect(self.profileSelectorActivatedInitial)
      ProfileUpdateWidget.gradeLabel.setText('You have to add a profile...')
      self.nameWidget.hide()
      return

    self.profileSelectorActivated(0)

  def profileIsInvalid(self):
    profileName = self.nameLineEdit.text()
    if len(profileName) == 0:
      return True, 'Profile can not be updated because the profile name is empty.'

    if ProfileUpdateWidget.profileSelector.currentText() != profileName and DBHandler.profileNameExists(profileName):
      return True, 'Profile can not be updated as this name is already used for another profile.'

    for checkBox in self.checkBoxes:
      if checkBox.isChecked():
        return False, ''

    return True, 'Profile can not be updated because none of the grade subjects have been selected.'

  @staticmethod
  def addProfile(profileName):
    if ProfileUpdateWidget.profileSelector.currentText() == 'There are no profiles':
      ProfileUpdateWidget.profileSelector.setItemText(0, 'Please select a profile...')
      ProfileUpdateWidget.gradeLabel.setText('Please select a profile...')
      ProfileUpdateWidget.profileSelector.setEnabled(True)

    ProfileUpdateWidget.profileSelector.addItem(profileName)
