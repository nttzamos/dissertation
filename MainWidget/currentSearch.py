from PyQt6.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont

class CurrentSearch(QWidget):
  def __init__(self):
    super().__init__()
    
    self.setFixedHeight(300)
    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(50, 50, 50, 50)

    self.setStyleSheet("QComboBox { background-color: grey }")

    self.searchedWord = QLabel("Enter a word.")
    self.searchedWord.setFixedSize(200, 100)
    self.searchedWord.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.searchedWord.setStyleSheet("QLabel { border : 1px solid black; border-radius: 10px }")
    font = QFont()
    font.setPointSize(20)
    self.searchedWord.setFont(font)

    self.searchDetails = QWidget()
    self.searchDetails.layout = QGridLayout(self.searchDetails)

    self.classLabel = QLabel("Class:")
    self.classLabel.setStyleSheet("QLabel { margin-right: 10px }")
    font = QFont()
    font.setPointSize(14)
    self.classLabel.setFont(font)
    self.classLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.classSelector = QComboBox()
    self.classSelector.setFont(font)
    self.classSelector.addItems(self.getAvailableClasses())

    self.subjectLabel = QLabel("Subject:")
    self.subjectSelector = QComboBox()
    self.subjectSelector.addItems(self.getAvailableSubjects())

    self.studentLabel = QLabel("Student:")
    self.studentSelector = QComboBox()
    self.studentSelector.addItems(self.getAvailableStudents())
    self.studentName = QLabel("Νίκος")
    self.useStudentSelector = False

    self.searchDetails.layout.addWidget(self.classLabel, 0, 0)
    self.searchDetails.layout.addWidget(self.classSelector, 0, 1)
    self.searchDetails.layout.addWidget(self.subjectLabel, 1, 0)
    self.searchDetails.layout.addWidget(self.subjectSelector, 1, 1)
    self.searchDetails.layout.addWidget(self.studentLabel, 2, 0)
    
    if self.useStudentSelector:
      self.searchDetails.layout.addWidget(self.studentSelector, 2, 1)
    else:
      self.searchDetails.layout.addWidget(self.studentName, 2, 1)

    self.layout.addWidget(self.searchedWord)
    self.layout.addSpacing(100)
    self.layout.addWidget(self.searchDetails)

  def getCurrentWord(self):
    return self.searchedWord.text()

  def getAvailableClasses(self):
    return ["Α' Δημοτικού", "Β' Δημοτικού", "Γ' Δημοτικού", "Δ' Δημοτικού", "Ε' Δημοτικού", "ΣΤ' Δημοτικού"]

  def getAvailableSubjects(self):
    return ["Μαθηματικά", "Φυσική", "Γεωγραφία", "Ιστορία", "Γλώσσα"]

  def getAvailableStudents(self):
    return ["Νίκος", "Στάθης", "Γιώργος", "Δημήτρης", "Ευριπίδης"]