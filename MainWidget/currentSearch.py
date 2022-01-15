from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from settings import Settings

class CurrentSearch(QWidget):
  currentGrade = -1

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

    self.studentSelector = QComboBox()
    self.studentSelector.setFont(comboBoxFont)
    self.studentSelector.addItems(self.getAvailableStudents())

    self.gradeSelector = QComboBox()
    self.gradeSelector.setFont(comboBoxFont)
    self.gradeSelector.addItems(self.getAvailableGrades())

    self.subjectSelector = QComboBox()
    self.subjectSelector.setFont(comboBoxFont)
    self.subjectSelector.addItems(self.getAvailableSubjects())

    self.gradeSelector.setEnabled(False)
    self.subjectSelector.setEnabled(False)

    self.searchDetails.layout.addWidget(self.studentSelector)
    self.searchDetails.layout.addWidget(self.gradeSelector)
    self.searchDetails.layout.addWidget(self.subjectSelector)

    self.layout.addWidget(self.searchedWord)
    self.layout.addSpacing(100)
    self.layout.addWidget(self.searchDetails)

    self.searchDetails.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
    self.searchedWord.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    self.studentSelector.activated.connect(self.studentSelectorActivated)

    self.style()

  def style(self):
    self.searchedWord.setStyleSheet(
      "QLabel { border: 1px solid black; border-radius: 50%; padding: 0px 50px; background-color: green; color: white }"
    )

    from styles import Styles
    self.setStyleSheet(Styles.currentSearchStyle)

  def getCurrentWord(self):
    return self.searchedWord.text()

  def getAvailableStudents(self):
    return [
      "Please select a student...",
      "Νίκος", "Στάθης", "Γιώργος", "Δημήτρης", "Ευριπίδης"]

  def getAvailableGrades(self):
    from databaseHandler import DBHandler
    grades = DBHandler.getGrades()
    grades[0:0] = ["You have to select a student.", "Please select a grade..."]
    return grades

  def getAvailableSubjects(self):
    if CurrentSearch.currentGrade == -1:
      return ["You have to select a student and a grade.", "You have to select a grade."]
    else:
      from databaseHandler import DBHandler
      currentGradeSubjects = DBHandler.getGradeSubjects(CurrentSearch.currentGrade)
      currentGradeSubjects.insert(0, "Please select a subject...")
      return currentGradeSubjects

  def studentSelectorActivated(self, index):
    if index != 0:
      self.studentSelector.removeItem(0)
      self.studentSelector.activated.disconnect()
      self.gradeSelector.removeItem(0)
      self.subjectSelector.removeItem(0)
      self.gradeSelector.activated.connect(self.gradeSelectorActivated)
      self.gradeSelector.setEnabled(True)

  def gradeSelectorActivated(self, index):
    offset = 1
    if CurrentSearch.currentGrade == -1 and index != 0:
      # self.subjectSelector.setEnabled(True)
      self.gradeSelector.removeItem(0)
      offset = 0

    grade = index + offset
    if grade != CurrentSearch.currentGrade:
      previousGrade = CurrentSearch.currentGrade
      CurrentSearch.currentGrade = grade
      Settings.modifyLastGradePicked(grade)
      self.subjectSelector.clear()
      self.subjectSelector.addItems(self.getAvailableSubjects())
      from mainWindow import MainWindow
      MainWindow.updateWidgets(previousGrade == -1)

  def subjectSelectorActivated(self, index):
    if index != 0:
      self.subjectSelector.removeItem(0)
      self.subjectSelector.activated.disconnect()
