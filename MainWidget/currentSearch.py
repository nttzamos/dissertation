from PyQt6.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont

class CurrentSearch(QWidget):
  def __init__(self):
    super().__init__()
    
    self.setFixedHeight(300)
    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(50, 50, 50, 50)

    self.searchedWord = QLabel("Enter a word.")
    self.searchedWord.setFixedSize(200, 100)
    self.searchedWord.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.searchedWord.setStyleSheet("QLabel { border : 1px solid black; border-radius: 10px }")
    font = QFont()
    font.setPointSize(20)
    self.searchedWord.setFont(font)

    self.searchDetails = QWidget()
    self.searchDetails.layout = QVBoxLayout(self.searchDetails)

    font.setPointSize(14)

    self.studentSelector = QComboBox()
    self.studentSelector.setFont(font)
    self.studentSelector.addItems(self.getAvailableStudents())
    self.useStudentSelector = True

    self.classSelector = QComboBox()
    self.classSelector.setFont(font)
    self.classSelector.addItems(self.getAvailableClasses())

    self.subjectSelector = QComboBox()
    self.subjectSelector.setFont(font)
    self.subjectSelector.addItems(self.getAvailableSubjects())

    self.classSelector.setEnabled(False)
    self.subjectSelector.setEnabled(False)

    maximumWidth = 300
    # self.studentSelector.setMaximumWidth(maximumWidth)
    # self.classSelector.setMaximumWidth(maximumWidth)
    # self.subjectSelector.setMaximumWidth(maximumWidth)
    self.searchDetails.setFixedWidth(maximumWidth)

    self.searchDetails.layout.addWidget(self.studentSelector)
    self.searchDetails.layout.addWidget(self.classSelector)
    self.searchDetails.layout.addWidget(self.subjectSelector)
    

    self.layout.addWidget(self.searchedWord)
    self.layout.addSpacing(100)
    self.layout.addWidget(self.searchDetails)

    self.studentSelector.activated.connect(self.studentSelectorActivated)

    # https://stackoverflow.com/questions/3151798/how-do-i-set-the-qcombobox-width-to-fit-the-largest-item
    # Maybe use this ^

  def getCurrentWord(self):
    return self.searchedWord.text()

  def getAvailableStudents(self):
    return [
      "Please select a student...",
      "Νίκος", "Στάθης", "Γιώργος", "Δημήτρης", "Ευριπίδης"]
  
  def getAvailableClasses(self):
    return [
      "You have to select a student.", "Please select a class...",
      "Α' Δημοτικού", "Β' Δημοτικού", "Γ' Δημοτικού", "Δ' Δημοτικού", "Ε' Δημοτικού", "ΣΤ' Δημοτικού"]

  def getAvailableSubjects(self):
    return [
      "You have to select a student and a class.", "You have to select a class.", "Please select a subject...",
      "Μαθηματικά", "Φυσική", "Γεωγραφία", "Ιστορία", "Γλώσσα"]

  def studentSelectorActivated(self, index):
    if index != 0:
      self.studentSelector.removeItem(0)
      self.studentSelector.activated.disconnect()
      self.classSelector.removeItem(0)
      self.subjectSelector.removeItem(0)
      self.classSelector.activated.connect(self.classSelectorActivated)
      self.classSelector.setEnabled(True)
  
  def classSelectorActivated(self, index):
    if index != 0:
      self.classSelector.removeItem(0)
      self.classSelector.activated.disconnect()
      self.subjectSelector.removeItem(0)
      self.subjectSelector.activated.connect(self.subjectSelectorActivated)
      self.subjectSelector.setEnabled(True)

  def subjectSelectorActivated(self, index):
    if index != 0:
      self.subjectSelector.removeItem(0)
      self.subjectSelector.activated.disconnect()
