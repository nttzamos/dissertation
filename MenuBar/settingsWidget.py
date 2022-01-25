from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog, QCheckBox, QWidget, QRadioButton, QSpinBox, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from MenuBar.settings import Settings

class SettingsWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Settings")
    self.setWindowIcon(QIcon("Resources/windowIcon.svg"))

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 20, 20, 20)
    self.layout.setSpacing(20)

    maximumResultsLabel = QLabel('Maximum Results:')
    self.maximumResultsSpinBox = QSpinBox()
    self.maximumResultsSpinBox.valueChanged.connect(self.maximumResultsChanged)
    self.maximumResultsSpinBox.setValue(Settings.getMaximumResults())
    self.maximumResultsSpinBox.setMinimum(1)
    self.maximumResultsSpinBox.setMaximum(50)

    self.maximumResultsSelectionWidget = QWidget()
    self.maximumResultsSelectionWidget.layout = QHBoxLayout(self.maximumResultsSelectionWidget)
    self.maximumResultsSelectionWidget.layout.setContentsMargins(0, 0, 0, 0)
    self.maximumResultsSelectionWidget.layout.addWidget(maximumResultsLabel)
    self.maximumResultsSelectionWidget.layout.addWidget(self.maximumResultsSpinBox)

    self.rememberLastGradePicked = QCheckBox('Remember last grade picked when re-opening app?', objectName='rememberLastGradePicked')
    self.rememberLastGradePicked.clicked.connect(lambda: self.toggleSetting('rememberLastGradePicked'))
    self.rememberLastGradePicked.setChecked(Settings.getBooleanSetting('rememberLastGradePicked'))

    self.askBeforeActions = QCheckBox('Ask before updating/deleting words?', objectName='askBeforeActions')
    self.askBeforeActions.clicked.connect(lambda: self.toggleSetting('askBeforeActions'))
    self.askBeforeActions.setChecked(Settings.getBooleanSetting('askBeforeActions'))

    self.showEditDictWordsButton = QCheckBox("Show 'Edit Dictionary Words' button?", objectName='showEditDictWordsButton')
    self.showEditDictWordsButton.clicked.connect(lambda: self.toggleSetting('showEditDictWordsButton'))
    self.showEditDictWordsButton.setChecked(Settings.getBooleanSetting('showEditDictWordsButton'))

    self.themeSelectionWidget = QWidget()
    self.themeSelectionWidget.layout = QHBoxLayout(self.themeSelectionWidget)
    self.lightThemeButton = QRadioButton('Light Theme')
    self.lightThemeButton.toggled.connect(self.lightThemeButtonClicked)
    self.darkThemeButton = QRadioButton('Dark Theme')
    self.darkThemeButton.toggled.connect(self.darkThemeButtonClicked)

    if Settings.getTheme() == 'light':
      self.lightThemeButton.setChecked(True)
    else:
      self.darkThemeButton.setChecked(True)

    self.themeSelectionWidget.layout.setContentsMargins(0, 0, 0, 0)
    self.themeSelectionWidget.layout.addWidget(self.lightThemeButton, alignment=Qt.AlignmentFlag.AlignLeft)
    self.themeSelectionWidget.layout.addWidget(self.darkThemeButton, alignment=Qt.AlignmentFlag.AlignLeft)

    self.defaultEditingActionWidget = QWidget()
    self.defaultEditingActionWidget.layout = QHBoxLayout(self.defaultEditingActionWidget)
    self.updateButton = QRadioButton('Update')
    self.updateButton.toggled.connect(self.updateButtonClicked)
    self.deleteButton = QRadioButton('Delete')
    self.deleteButton.toggled.connect(self.deleteButtonClicked)

    if Settings.getDefaultEditingAction() == 'update':
      self.updateButton.setChecked(True)
    else:
      self.deleteButton.setChecked(True)

    self.defaultEditingActionWidget.layout.setContentsMargins(0, 0, 0, 0)
    self.defaultEditingActionWidget.layout.addWidget(self.updateButton, alignment=Qt.AlignmentFlag.AlignLeft)
    self.defaultEditingActionWidget.layout.addWidget(self.deleteButton, alignment=Qt.AlignmentFlag.AlignLeft)

    self.layout.addWidget(self.maximumResultsSelectionWidget)
    self.layout.addWidget(self.rememberLastGradePicked)
    self.layout.addWidget(self.askBeforeActions)
    self.layout.addWidget(self.showEditDictWordsButton)
    self.layout.addWidget(self.themeSelectionWidget)
    # self.layout.addWidget(self.defaultEditingActionWidget)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.settingsWidgetStyle)

  def maximumResultsChanged(self):
    Settings.setMaximumResults(self.maximumResultsSpinBox.value())

  def toggleSetting(self, settingName):
    settingCheckbox = self.findChild(QCheckBox, settingName)
    newValue = settingCheckbox.isChecked()
    Settings.setBooleanSetting(settingName, newValue)

    if settingName == 'showEditDictWordsButton':
      from MainWidget.searchingWidget import SearchingWidget
      SearchingWidget.toggleEditWordsButtonVisibility(newValue)

  def lightThemeButtonClicked(self):
    if self.lightThemeButton.isChecked():
      Settings.setTheme('light')

  def darkThemeButtonClicked(self):
    if self.darkThemeButton.isChecked():
      Settings.setTheme('dark')

  def updateButtonClicked(self):
    if self.updateButton.isChecked():
      Settings.setDefaultEditingAction('update')

  def deleteButtonClicked(self):
    if self.deleteButton.isChecked():
      Settings.setDefaultEditingAction('delete')
