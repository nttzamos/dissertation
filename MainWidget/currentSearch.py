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

    self.addStudentButton = QPushButton('Edit students/profiles list')
    self.addStudentButton.setFont(comboBoxFont)
    self.addStudentButton.clicked.connect(self.addStudent)
    self.addStudentButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    self.studentSelector = QComboBox()
    self.studentSelector.setFont(comboBoxFont)
    self.studentSelector.addItems(self.getAvailableStudents())

    CurrentSearch.profileSelector = QComboBox()
    CurrentSearch.profileSelector.setFont(comboBoxFont)
    CurrentSearch.profileSelector.addItem('You have to select a student.')

    CurrentSearch.subjectSelector = QComboBox()
    CurrentSearch.subjectSelector.setFont(comboBoxFont)
    CurrentSearch.subjectSelector.addItem('You have to select a student and a profile.')

    CurrentSearch.profileSelector.setDisabled(True)
    CurrentSearch.subjectSelector.setDisabled(True)

    self.searchDetails.layout.addWidget(self.addStudentButton, alignment=Qt.AlignmentFlag.AlignRight)
    self.searchDetails.layout.addWidget(self.studentSelector)
    self.searchDetails.layout.addWidget(CurrentSearch.profileSelector)
    self.searchDetails.layout.addWidget(CurrentSearch.subjectSelector)

    self.layout.addWidget(self.searchedWord)
    self.layout.addSpacing(100)
    self.layout.addWidget(self.searchDetails)

    self.searchDetails.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
    self.searchedWord.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    self.studentSelector.activated.connect(self.studentSelectorActivatedInitial)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.currentSearchStyle)
    self.searchedWord.setStyleSheet(Styles.searchedWordStyle)

  def getCurrentWord(self): # got to change
    return self.searchedWord.text()

  def addStudent(self):
    from MainWidget.studentsDataEditingWidget import StudentsDataEditingWidget
    studentsEditingDialog = StudentsDataEditingWidget()
    studentsEditingDialog.exec()

  def getAvailableStudents(self):
    from Common.databaseHandler import DBHandler
    students = DBHandler.getStudents()
    students[0:0] = ['Please select a student...']
    return students

  def studentSelectorActivatedInitial(self, index):
    if index != 0:
      self.studentSelector.removeItem(0)
      self.studentSelector.activated.disconnect()
      self.studentSelector.activated.connect(self.studentSelectorActivated)
      CurrentSearch.profileSelector.removeItem(0)
      CurrentSearch.subjectSelector.removeItem(0)
      self.studentSelectorActivated(0)

  def studentSelectorActivated(self, index):
    studentName = self.studentSelector.currentText()
    CurrentSearch.profileSelector.clear()
    from Common.databaseHandler import DBHandler
    studentId, studentProfiles = DBHandler.getStudentDetails(studentName)
    if len(studentProfiles) == 0:
      CurrentSearch.profileSelector.addItem('This student has no profiles.')
      CurrentSearch.profileSelector.setDisabled(True)
    else:
      studentProfiles[0:0] = ['Please select a profile...']
      CurrentSearch.profileSelector.addItems(studentProfiles)
      CurrentSearch.profileSelector.setEnabled(True)
      CurrentSearch.profileSelector.activated.connect(self.profileSelectorActivatedInitial)

    CurrentSearch.subjectSelector.clear()
    CurrentSearch.subjectSelector.addItem('You have to select a profile.')
    CurrentSearch.subjectSelector.setDisabled(True)

  def profileSelectorActivatedInitial(self, index):
    if index != 0:
      CurrentSearch.profileSelector.removeItem(0)
      CurrentSearch.profileSelector.activated.disconnect()
      CurrentSearch.profileSelector.activated.connect(self.profileSelectorActivated)
      self.profileSelectorActivated(0)

  def profileSelectorActivated(self, index):
    CurrentSearch.profileId, CurrentSearch.gradeId, gradeName, profileSubjectsIds = DBHandler.getProfileDetails(CurrentSearch.profileSelector.currentText())
    CurrentSearch.subjectSelector.clear()
    CurrentSearch.subjectSelector.addItem('Please select a subject...')
    for subjectId in profileSubjectsIds:
      CurrentSearch.subjectSelector.addItem(DBHandler.getSubjectName(subjectId))

    if len(profileSubjectsIds) > 1:
      CurrentSearch.subjectSelector.addItem('All Subjects')

    CurrentSearch.subjectSelector.activated.connect(self.subjectSelectorActivatedInitial)
    CurrentSearch.subjectSelector.setEnabled(True)

  def subjectSelectorActivatedInitial(self, index):
    if index != 0:
      CurrentSearch.subjectSelector.removeItem(0)
      CurrentSearch.subjectSelector.activated.disconnect()
      CurrentSearch.subjectSelector.activated.connect(self.subjectSelectorActivated)
      self.subjectSelectorActivated(CurrentSearch.subjectSelector.currentIndex())

  def subjectSelectorActivated(self, index):
    from MainWidget.mainWindow import MainWindow
    MainWindow.updateWidgets(CurrentSearch.initialSearch, self.profileId, self.gradeId, CurrentSearch.subjectSelector.currentText())
    CurrentSearch.initialSearch = False

  @staticmethod
  def getCurrentSelectionDetails():
    subjectName = CurrentSearch.subjectSelector.currentText()
    if subjectName == 'All Subjects':
      subjectName = -1

    return CurrentSearch.profileId, CurrentSearch.gradeId, subjectName
