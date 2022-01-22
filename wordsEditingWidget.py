from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QComboBox, QDialog, QLabel, QCompleter, QCheckBox, QRadioButton, QWidget, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QStringListModel, QTimer, Qt
from PyQt6.QtGui import QFont

from settings import Settings
from databaseHandler import DBHandler

class WordsEditingWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Edit Dictionary Words')
    self.setFixedSize(Settings.screenWidth / 2, Settings.screenHeight / 2)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(10, 10, 10, 10)

    gradeSelectionLabel = QLabel('Grade Selection')
    comboBoxFont = QFont(Settings.font, 14)
    self.gradeSelector = QComboBox()
    self.gradeSelector.activated.connect(self.gradeSelectorActivated)
    self.gradeSelector.setFont(comboBoxFont)
    self.gradeSelector.addItems(DBHandler.getGrades())

    actionSelectionLabel = QLabel('Action Selection')
    self.updateSelectionButton = QRadioButton('Update Word')
    self.updateSelectionButton.setChecked(True)
    self.updateSelectionButton.toggled.connect(self.updateButtonClicked)
    self.deletionSelectionButton = QRadioButton('Delete Word')
    self.deletionSelectionButton.toggled.connect(self.deleteButtonClicked)
    self.actionSelectionWidget = QWidget()
    self.actionSelectionWidget.layout = QHBoxLayout(self.actionSelectionWidget)
    self.actionSelectionWidget.layout.setContentsMargins(0, 0, 0, 0)
    self.actionSelectionWidget.layout.addWidget(self.updateSelectionButton)
    self.actionSelectionWidget.layout.addWidget(self.deletionSelectionButton)

    actionEffectLabel = QLabel('Action Effect')
    self.updateAllGrades = QCheckBox('Update/Delete word for all grades?')

    wordSelectionLabel = QLabel('Word Selection')
    self.wordSelectionLineEdit = QLineEdit()
    self.wordSelectionLineEdit.returnPressed.connect(self.wordSelected)
    self.dictionaryWords = DBHandler.getWords(1)
    self.completer = QCompleter(self.dictionaryWords)
    self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completerFont = QFont(Settings.font, 10)
    self.completer.popup().setFont(completerFont)
    self.wordSelectionLineEdit.setCompleter(self.completer)
    self.wordSelectionLineEdit.setPlaceholderText('Please enter a word.')

    self.updateWordWidget = QWidget()
    self.updateWordWidget.layout = QVBoxLayout(self.updateWordWidget)
    self.updateWordWidget.layout.setContentsMargins(0, 0, 0, 0)
    updateFormLabel = QLabel('Editing Form')
    self.wordEditingLineEdit = QLineEdit()
    self.wordEditingLineEdit.returnPressed.connect(self.updateWordConfirmation)
    self.wordEditingLineEdit.setPlaceholderText('You have to select a word first.')
    self.wordEditingLineEdit.setDisabled(True)
    self.updateWordWidget.layout.addWidget(updateFormLabel)
    self.updateWordWidget.layout.addWidget(self.wordEditingLineEdit)

    self.layout.addWidget(gradeSelectionLabel)
    self.layout.addWidget(self.gradeSelector)
    self.layout.addSpacing(10)

    self.layout.addWidget(actionSelectionLabel)
    self.layout.addWidget(self.actionSelectionWidget)
    self.layout.addSpacing(10)

    self.layout.addWidget(actionEffectLabel)
    self.layout.addWidget(self.updateAllGrades)
    self.layout.addSpacing(10)

    self.layout.addWidget(wordSelectionLabel)
    self.layout.addWidget(self.wordSelectionLineEdit)
    self.layout.addSpacing(10)

    self.layout.addWidget(self.updateWordWidget)

  def style(self):
    self.setStyleSheet(
      "QPushButton:hover { background-color: grey }\n"
      "QWidget { background-color: green }"
    )

  def wordSelected(self):
    self.searchedWord = self.wordSelectionLineEdit.text()
    if self.searchedWord in self.dictionaryWords:
      if self.updateSelectionButton.isChecked():
        self.wordEditingLineEdit.setText(self.searchedWord)
        self.wordEditingLineEdit.setEnabled(True)
        self.wordEditingLineEdit.setFocus()
        QTimer.singleShot(0, self.wordSelectionLineEdit.clear)
      elif self.deletionSelectionButton.isChecked():
        self.deleteWordConfirmation()
    else:
      # handle case where word is not in dictionary
      pass

  def updateWordConfirmation(self):
    answer = QMessageBox.question(self, 'Update Word', 'Are you sure you want to update this word?', QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
    if answer == QMessageBox.StandardButton.Yes:
      newWord = self.wordEditingLineEdit.text()
      DBHandler.updateWord(self.searchedWord, newWord, self.getGrades())
      self.updateDictionaryWords(self.searchedWord, newWord)
      QTimer.singleShot(0, self.wordEditingLineEdit.clear)
      self.wordEditingLineEdit.setDisabled(True)
      self.wordSelectionLineEdit.setFocus()

  def deleteWordConfirmation(self):
    answer = QMessageBox.question(self, 'Delete Word', 'Are you sure you want to delete this word?', QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
    if answer == QMessageBox.StandardButton.Yes:
      DBHandler.deleteWord(self.searchedWord, self.getGrades())
      self.updateDictionaryWords(self.searchedWord)
      QTimer.singleShot(0, self.wordSelectionLineEdit.clear)

  def deleteButtonClicked(self):
    if self.deletionSelectionButton.isChecked():
      QTimer.singleShot(0, self.wordEditingLineEdit.clear)
      self.wordEditingLineEdit.setDisabled(True)
      self.updateWordWidget.hide()

  def updateButtonClicked(self):
    if self.updateSelectionButton.isChecked():
      self.updateWordWidget.show()

  def getGrades(self):
    grades = []
    if self.updateAllGrades.isChecked():
      grades = list(range(1, 7))
    else:
      grades.append(self.gradeSelector.currentIndex() + 1)

    return grades

  def gradeSelectorActivated(self, index):
    self.dictionaryWords = DBHandler.getWords(index + 1)
    model = QStringListModel(self.dictionaryWords, self.completer)
    self.completer.setModel(model)

  def updateDictionaryWords(self, oldWord, newWord=None):
    if not (newWord == None or newWord in self.dictionaryWords):
      self.dictionaryWords.append(newWord)

    self.dictionaryWords.remove(oldWord)
    model = QStringListModel(self.dictionaryWords, self.completer)
    self.completer.setModel(model)
