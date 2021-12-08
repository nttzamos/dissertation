from PyQt6.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont

from settings import Settings

class CurrentSearch(QWidget):
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

    self.classSelector = QComboBox()
    self.classSelector.setFont(comboBoxFont)
    self.classSelector.addItems(self.getAvailableClasses())

    self.subjectSelector = QComboBox()
    self.subjectSelector.setFont(comboBoxFont)
    self.subjectSelector.addItems(self.getAvailableSubjects())

    self.classSelector.setEnabled(False)
    self.subjectSelector.setEnabled(False)

    self.searchDetails.layout.addWidget(self.studentSelector)
    self.searchDetails.layout.addWidget(self.classSelector)
    self.searchDetails.layout.addWidget(self.subjectSelector)

    self.layout.addWidget(self.searchedWord)
    self.layout.addSpacing(100)
    self.layout.addWidget(self.searchDetails)
    
    self.searchDetails.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
    self.searchedWord.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    self.studentSelector.activated.connect(self.studentSelectorActivated)

    self.style()

  def style(self):
    self.searchedWord.setStyleSheet("QLabel { border: 1px solid black; border-radius: 50%; padding: 0px 50px }")
    
    self.setStyleSheet(
      "QComboBox { background-color: none }\n"
      "QWidget { background-color: none }\n"
      "QLabel { background-color: green }"
    )

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
