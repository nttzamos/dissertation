from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QComboBox, QDialog, QLabel, QCompleter, QCheckBox, QRadioButton
from PyQt6.QtCore import QStringListModel, QTimer, Qt
from PyQt6.QtGui import QFont

from settings import Settings
from databaseHandler import DBHandler

class WordsEditingWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Edit Dictionary Words")
    self.setFixedSize(Settings.screenWidth / 2, Settings.screenHeight / 2)
    self.setContentsMargins(0, 0, 0, 0)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.lineEdit = QLineEdit()
    self.lineEdit.returnPressed.connect(self.showWord)
    self.dictionaryWords = DBHandler.getWords(1)
    self.completer = QCompleter(self.dictionaryWords)
    self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completerFont = QFont(Settings.font, 10)
    self.completer.popup().setFont(completerFont)
    self.lineEdit.setCompleter(self.completer)
    self.lineEdit.setPlaceholderText("Please enter a word.")
    comboBoxFont = QFont(Settings.font, 14)
    self.gradeSelector = QComboBox()
    self.gradeSelector.activated.connect(self.gradeSelectorActivated)
    self.gradeSelector.setFont(comboBoxFont)
    self.gradeSelector.addItems(DBHandler.getGrades())
    self.activeWord = QLabel('Please select a word')
    self.updateAllGrades = QCheckBox('Update/Delete word for all grades?')
    self.updateSelectionButton = QRadioButton('Update Word')
    self.updateSelectionButton.setChecked(True)
    self.deletionSelectionButton = QRadioButton('Delete Word')
    self.layout.addWidget(self.gradeSelector)
    self.layout.addWidget(self.updateSelectionButton)
    self.layout.addWidget(self.deletionSelectionButton)
    self.layout.addWidget(self.updateAllGrades)
    self.layout.addWidget(self.lineEdit)
    self.layout.addWidget(self.activeWord)

  def style(self):
    self.setStyleSheet(
      "QPushButton:hover { background-color: grey }\n"
      "QWidget { background-color: green }"
    )

  def showWord(self):
    searchedWord = self.lineEdit.text()

    if searchedWord in self.dictionaryWords:
      self.activeWord.setText(searchedWord)
      grades = []
      if self.updateAllGrades.isChecked():
        grades = list(range(1, 7))
      else:
        grades.append(self.gradeSelector.currentIndex() + 1)

      if self.updateSelectionButton.isChecked():
        DBHandler.updateWord(searchedWord, grades)
      elif self.deletionSelectionButton.isChecked():
        DBHandler.deleteWord(searchedWord, grades)
    else:
      self.activeWord.setText('Word not in active grade.')

    QTimer.singleShot(0, self.lineEdit.clear)

  def gradeSelectorActivated(self, index):
    self.dictionaryWords = DBHandler.getWords(index + 1)
    model = QStringListModel(self.dictionaryWords, self.completer)
    self.completer.setModel(model)
