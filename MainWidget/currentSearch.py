from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from Common.databaseHandler import DBHandler

from MenuBar.settings import Settings

class CurrentSearch(QWidget):
  initialSearch = True

  def __init__(self):
    super().__init__()

    self.setFixedHeight(300)
    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(50, 50, 50, 50)

    searchedWordFont = QFont(Settings.font, 20)
    comboBoxFont = QFont(Settings.font, 14)

    self.searchedWord = QLabel("Enter a word.")
    self.searchedWord.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.searchedWord.setMaximumHeight(100)
    self.searchedWord.setFont(searchedWordFont)

    self.searchDetails = QWidget()
    self.searchDetails.layout = QVBoxLayout(self.searchDetails)

    self.openStudentDataWidgetButton = QPushButton('Edit students/profiles list')
    self.openStudentDataWidgetButton.setFont(comboBoxFont)
    self.openStudentDataWidgetButton.clicked.connect(self.openStudentDataWidget)
    self.openStudentDataWidgetButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    CurrentSearch.studentSelector = QComboBox()
    CurrentSearch.studentSelector.setFont(comboBoxFont)

    students = self.getAvailableStudents()
    if len(students) > 0:
      students[0:0] = ['Please select a student...']
      CurrentSearch.studentSelector.addItems(students)
    else:
      CurrentSearch.studentSelector.addItem('There are no students.')
      CurrentSearch.studentSelector.setDisabled(True)

    CurrentSearch.profileSelector = QComboBox()
    CurrentSearch.profileSelector.setFont(comboBoxFont)
    CurrentSearch.profileSelector.addItem('You have to select a student.')

    CurrentSearch.subjectSelector = QComboBox()
    CurrentSearch.subjectSelector.setFont(comboBoxFont)
    CurrentSearch.subjectSelector.addItem('You have to select a student and a profile.')

    CurrentSearch.profileSelector.setDisabled(True)
    CurrentSearch.subjectSelector.setDisabled(True)

    self.searchDetails.layout.addWidget(self.openStudentDataWidgetButton, alignment=Qt.AlignmentFlag.AlignRight)
    self.searchDetails.layout.addWidget(CurrentSearch.studentSelector)
    self.searchDetails.layout.addWidget(CurrentSearch.profileSelector)
    self.searchDetails.layout.addWidget(CurrentSearch.subjectSelector)

    self.layout.addWidget(self.searchedWord)
    self.layout.addSpacing(100)
    self.layout.addWidget(self.searchDetails)

    self.searchDetails.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
    self.searchedWord.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    CurrentSearch.studentSelector.activated.connect(self.studentSelectorActivatedInitial)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.currentSearchStyle)
    self.searchedWord.setStyleSheet(Styles.searchedWordStyle)

  def getCurrentWord(self): # got to change
    return self.searchedWord.text()

  def openStudentDataWidget(self):
    from MainWidget.studentsDataEditingWidget import StudentsDataEditingWidget
    studentsEditingDialog = StudentsDataEditingWidget()
    studentsEditingDialog.exec()

  def getAvailableStudents(self):
    from Common.databaseHandler import DBHandler
    students = DBHandler.getStudents()
    return students

  @staticmethod
  def studentSelectorActivatedInitial(index):
    if index != 0:
      CurrentSearch.studentSelector.removeItem(0)
      CurrentSearch.studentSelector.activated.disconnect()
      CurrentSearch.studentSelector.activated.connect(CurrentSearch.studentSelectorActivated)
      CurrentSearch.profileSelector.removeItem(0)
      CurrentSearch.subjectSelector.removeItem(0)
      CurrentSearch.studentSelectorActivated(0)

  @staticmethod
  def studentSelectorActivated(index):
    studentName = CurrentSearch.studentSelector.currentText()
    CurrentSearch.profileSelector.clear()
    from Common.databaseHandler import DBHandler
    CurrentSearch.studentId, studentProfiles = DBHandler.getStudentDetails(studentName)
    if len(studentProfiles) == 0:
      CurrentSearch.profileSelector.addItem('This student has no profiles.')
      CurrentSearch.profileSelector.setDisabled(True)
    else:
      studentProfiles[0:0] = ['Please select a profile...']
      CurrentSearch.profileSelector.addItems(studentProfiles)
      CurrentSearch.profileSelector.setEnabled(True)
      CurrentSearch.profileSelector.activated.connect(CurrentSearch.profileSelectorActivatedInitial)

    CurrentSearch.subjectSelector.clear()
    CurrentSearch.subjectSelector.addItem('You have to select a profile.')
    CurrentSearch.subjectSelector.setDisabled(True)

  @staticmethod
  def profileSelectorActivatedInitial(index):
    if index != 0:
      CurrentSearch.profileSelector.removeItem(0)
      CurrentSearch.profileSelector.activated.disconnect()
      CurrentSearch.profileSelector.activated.connect(CurrentSearch.profileSelectorActivated)
      CurrentSearch.profileSelectorActivated(0)

  @staticmethod
  def profileSelectorActivated(index):
    CurrentSearch.profileId, CurrentSearch.gradeId, gradeName, profileSubjectsIds = DBHandler.getProfileDetails(CurrentSearch.profileSelector.currentText())
    CurrentSearch.subjectSelector.clear()
    CurrentSearch.subjectSelector.addItem('Please select a subject...')
    for subjectId in profileSubjectsIds:
      CurrentSearch.subjectSelector.addItem(DBHandler.getSubjectName(subjectId))

    if len(profileSubjectsIds) > 1:
      CurrentSearch.subjectSelector.addItem('All Subjects')

    CurrentSearch.subjectSelector.activated.connect(CurrentSearch.subjectSelectorActivatedInitial)
    CurrentSearch.subjectSelector.setEnabled(True)

  @staticmethod
  def subjectSelectorActivatedInitial(index):
    if index != 0:
      CurrentSearch.subjectSelector.removeItem(0)
      CurrentSearch.subjectSelector.activated.disconnect()
      CurrentSearch.subjectSelector.activated.connect(CurrentSearch.subjectSelectorActivated)
      CurrentSearch.subjectSelectorActivated(CurrentSearch.subjectSelector.currentIndex())

  @staticmethod
  def subjectSelectorActivated(index):
    from MainWidget.mainWindow import MainWindow
    MainWindow.updateWidgets(CurrentSearch.initialSearch, CurrentSearch.profileId, CurrentSearch.gradeId, CurrentSearch.subjectSelector.currentText())
    CurrentSearch.initialSearch = False

  @staticmethod
  def getCurrentSelectionDetails():
    subjectName = CurrentSearch.subjectSelector.currentText()
    if subjectName == 'All Subjects':
      subjectName = -1

    return CurrentSearch.studentId, CurrentSearch.profileId, CurrentSearch.gradeId, subjectName

  @staticmethod
  def addStudent(studentName):
    if CurrentSearch.studentSelector.currentText() == 'There are no students.':
      CurrentSearch.studentSelector.setEnabled(True)
      CurrentSearch.studentSelector.clear()
      CurrentSearch.studentSelector.addItem('Please select a student...')
      CurrentSearch.studentSelector.activated.disconnect()
      CurrentSearch.studentSelector.activated.connect(CurrentSearch.studentSelectorActivatedInitial)

    CurrentSearch.studentSelector.addItem(studentName)

  @staticmethod
  def updateStudent(oldStudentName, newStudentName):
    index = CurrentSearch.studentSelector.findText(oldStudentName)
    CurrentSearch.studentSelector.setItemText(index, newStudentName)

  @staticmethod
  def removeStudent(studentName):
    index = CurrentSearch.studentSelector.findText(studentName)
    currentIndex = CurrentSearch.studentSelector.currentIndex()
    CurrentSearch.studentSelector.removeItem(index)

    if CurrentSearch.studentSelector.count() == 0 or CurrentSearch.studentSelector.currentText() == 'Please select a profile...':
      CurrentSearch.studentSelector.clear()
      CurrentSearch.studentSelector.addItem('There are no students.')
      CurrentSearch.studentSelector.setDisabled(True)
      CurrentSearch.profileSelector.setDisabled(True)
      CurrentSearch.profileSelector.clear()
      CurrentSearch.profileSelector.addItem('You have to select a student.')
      CurrentSearch.subjectSelector.clear()
      CurrentSearch.subjectSelector.setDisabled(True)
      CurrentSearch.subjectSelector.addItem('You have to select a student and a profile.')
    elif index == currentIndex:
      CurrentSearch.studentSelectorActivated(CurrentSearch.studentSelector.currentIndex())

  @staticmethod
  def addProfiles(profileNames):
    if len(profileNames) == 0: return

    if CurrentSearch.profileSelector.currentText() == 'This student has no profiles.':
      CurrentSearch.profileSelector.setEnabled(True)
      CurrentSearch.profileSelector.clear()
      CurrentSearch.profileSelector.addItem('Please select a profile...')
      CurrentSearch.profileSelector.activated.disconnect()
      CurrentSearch.profileSelector.activated.connect(CurrentSearch.profileSelectorActivatedInitial)

    CurrentSearch.profileSelector.addItems(profileNames)

  @staticmethod
  def updateProfile(oldProfileName, newProfileName):
    index = CurrentSearch.profileSelector.findText(oldProfileName)
    if index != -1:
      CurrentSearch.profileSelector.setItemText(index, newProfileName)

  @staticmethod
  def removeProfiles(profileNames):
    if len(profileNames) == 0: return

    text = CurrentSearch.profileSelector.currentText()

    for profileName in profileNames:
      index = CurrentSearch.profileSelector.findText(profileName)
      if index != -1:
        CurrentSearch.profileSelector.removeItem(index)
    if CurrentSearch.profileSelector.count() == 0:
      CurrentSearch.profileSelector.clear()
      CurrentSearch.profileSelector.addItem('This student has no profiles.')
      CurrentSearch.profileSelector.setDisabled(True)
      CurrentSearch.subjectSelector.clear()
      CurrentSearch.subjectSelector.setDisabled(True)
      CurrentSearch.subjectSelector.addItem('You have to select a student and a profile.')
    elif text != CurrentSearch.profileSelector.currentText():
      CurrentSearch.profileSelectorActivated(CurrentSearch.profileSelector.currentIndex())

  @staticmethod
  def addSubjects(subjectNames):
    CurrentSearch.subjectSelector.addItems(subjectNames)

  @staticmethod
  def removeSubjects(subjectNames):
    if len(subjectNames) == 0: return

    text = CurrentSearch.subjectSelector.currentText()

    for subjectName in subjectNames:
      index = CurrentSearch.subjectSelector.findText(subjectName)
      CurrentSearch.subjectSelector.removeItem(index)

    if text != CurrentSearch.subjectSelector.currentText():
      CurrentSearch.subjectSelectorActivated(CurrentSearch.subjectSelector.currentIndex())
