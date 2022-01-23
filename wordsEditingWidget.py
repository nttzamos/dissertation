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
    self.layout.setContentsMargins(20, 20, 20, 10)
    self.layout.setSpacing(0)

    labelFont = QFont(Settings.font, 16)
    comboBoxFont = QFont(Settings.font, 14)
    radioButtonFont = QFont(Settings.font, 14)
    checkBoxFont = QFont(Settings.font, 14)
    lineEditFont = QFont(Settings.font, 14)
    completerFont = QFont(Settings.font, 12)

    gradeSelectionLabel = QLabel('Grade Selection')
    gradeSelectionLabel.setFont(labelFont)
    self.gradeSelector = QComboBox()
    self.gradeSelector.activated.connect(self.gradeSelectorActivated)
    self.gradeSelector.setFont(comboBoxFont)
    self.gradeSelector.addItems(DBHandler.getGrades())

    actionSelectionLabel = QLabel('Action Selection')
    actionSelectionLabel.setFont(labelFont)
    self.updateSelectionButton = QRadioButton('Update Word')
    self.updateSelectionButton.setFont(radioButtonFont)
    self.updateSelectionButton.setChecked(True)
    self.updateSelectionButton.toggled.connect(self.updateButtonClicked)
    self.deletionSelectionButton = QRadioButton('Delete Word')
    self.deletionSelectionButton.setFont(radioButtonFont)
    self.deletionSelectionButton.toggled.connect(self.deleteButtonClicked)
    self.actionSelectionWidget = QWidget()
    self.actionSelectionWidget.layout = QHBoxLayout(self.actionSelectionWidget)
    self.actionSelectionWidget.layout.setContentsMargins(0, 0, 0, 0)
    self.actionSelectionWidget.layout.addWidget(self.updateSelectionButton)
    self.actionSelectionWidget.layout.addWidget(self.deletionSelectionButton)

    actionEffectLabel = QLabel('Action Effect')
    actionEffectLabel.setFont(labelFont)
    self.updateAllGrades = QCheckBox('Update/Delete word for all grades?')
    self.updateAllGrades.setFont(checkBoxFont)

    wordSelectionLabel = QLabel('Word Selection')
    wordSelectionLabel.setFont(labelFont)
    self.wordSelectionLineEdit = QLineEdit()
    self.wordSelectionLineEdit.setFont(lineEditFont)
    self.wordSelectionLineEdit.returnPressed.connect(self.wordSelected)
    self.dictionaryWords = DBHandler.getWords(1)
    self.completer = QCompleter(self.dictionaryWords)
    self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    self.completer.popup().setFont(completerFont)
    self.wordSelectionLineEdit.setCompleter(self.completer)
    self.wordSelectionLineEdit.setPlaceholderText('Please enter a word.')
    self.wordSelectionLineEdit.setContentsMargins(0, 0, 0, 0)
    self.wordSelectionLineEdit.textChanged.connect(self.searchTextChanged)
    self.errorMessageLabel = QLabel("Please search for another word", self)
    sizePolicy = self.errorMessageLabel.sizePolicy()
    sizePolicy.setRetainSizeWhenHidden(True)
    self.errorMessageLabel.setSizePolicy(sizePolicy)
    self.showErrorMessage = False
    self.errorMessageLabel.setStyleSheet(
      "QLabel { color: red }"
    )

    self.updateWordWidget = QWidget()
    self.updateWordWidget.layout = QVBoxLayout(self.updateWordWidget)
    self.updateWordWidget.layout.setContentsMargins(0, 0, 0, 0)
    updateFormLabel = QLabel('Editing Form')
    updateFormLabel.setFont(labelFont)
    self.wordEditingLineEdit = QLineEdit()
    self.wordEditingLineEdit.setFont(lineEditFont)
    self.wordEditingLineEdit.returnPressed.connect(self.updateWordConfirmation)
    self.wordEditingLineEdit.setPlaceholderText('You have to select a word first.')
    self.wordEditingLineEdit.setDisabled(True)
    self.updateWordWidget.layout.addWidget(updateFormLabel)
    self.updateWordWidget.layout.addWidget(self.wordEditingLineEdit)

    self.layout.addWidget(gradeSelectionLabel)
    self.layout.addSpacing(5)
    self.layout.addWidget(self.gradeSelector)
    self.layout.addSpacing(15)

    self.layout.addWidget(actionSelectionLabel)
    self.layout.addSpacing(5)
    self.layout.addWidget(self.actionSelectionWidget)
    self.layout.addSpacing(15)

    self.layout.addWidget(actionEffectLabel)
    self.layout.addSpacing(5)
    self.layout.addWidget(self.updateAllGrades)
    self.layout.addSpacing(15)

    self.layout.addWidget(wordSelectionLabel)
    self.layout.addSpacing(5)
    self.layout.addWidget(self.wordSelectionLineEdit)
    self.layout.addSpacing(2)
    self.layout.addWidget(self.errorMessageLabel, alignment=Qt.AlignmentFlag.AlignRight)
    self.errorMessageLabel.hide()
    self.layout.addSpacing(5)

    self.layout.addWidget(self.updateWordWidget)
    self.style()

  def style(self):
    from styles import Styles
    self.setStyleSheet(Styles.wordsEditingWidgetStyle)

  def wordSelected(self):
    self.searchedWord = self.wordSelectionLineEdit.text()
    if self.searchedWord in self.dictionaryWords:
      if self.updateSelectionButton.isChecked():
        self.wordEditingLineEdit.setText(self.searchedWord)
        self.wordEditingLineEdit.setEnabled(True)
        self.wordEditingLineEdit.setFocus()
      elif self.deletionSelectionButton.isChecked():
        self.deleteWordConfirmation()
    else:
      self.showErrorMessage = True
      self.errorMessageLabel.show()

  def searchTextChanged(self):
    if self.showErrorMessage:
      self.showErrorMessage = False
      self.errorMessageLabel.hide()

  def updateWordConfirmation(self):
    if Settings.getBooleanSetting('askBeforeActions'):
      newWord = self.wordEditingLineEdit.text()
      title = 'Update Word'
      question = "Are you sure you want to update '" + self.searchedWord + "' to '" + newWord + "'?"
      answer = QMessageBox.question(self, title, question, QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
      if answer == QMessageBox.StandardButton.Yes:
        self.updateWord()
    else:
      self.updateWord()

  def updateWord(self):
    newWord = self.wordEditingLineEdit.text()
    DBHandler.updateWord(self.searchedWord, newWord, self.getGrades())
    self.updateDictionaryWords(self.searchedWord, newWord)
    QTimer.singleShot(0, self.wordSelectionLineEdit.clear)
    QTimer.singleShot(0, self.wordEditingLineEdit.clear)
    self.wordEditingLineEdit.setDisabled(True)
    self.wordSelectionLineEdit.setFocus()

  def deleteWordConfirmation(self):
    if Settings.getBooleanSetting('askBeforeActions'):
      title = 'Delete Word'
      question = "Are you sure you want to delete '" + self.searchedWord + "'?"
      answer = QMessageBox.question(self, title, question, QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
      if answer == QMessageBox.StandardButton.Yes:
        self.deleteWord()
    else:
      self.deleteWord()

  def deleteWord(self):
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
