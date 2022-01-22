from PyQt6.QtWidgets import QVBoxLayout, QDialog, QCheckBox

from settings import Settings

class SettingsWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Settings")

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 20, 20, 20)
    self.layout.setSpacing(20)

    self.rememberLastGradePicked = QCheckBox('Remember last grade picked when re-opening app?', objectName='rememberLastGradePicked')
    self.rememberLastGradePicked.clicked.connect(lambda: self.toggleSetting('rememberLastGradePicked'))
    self.rememberLastGradePicked.setChecked(Settings.getBooleanSetting('rememberLastGradePicked'))

    self.askBeforeActions = QCheckBox('Ask before updating/deleting words?', objectName='askBeforeActions')
    self.askBeforeActions.clicked.connect(lambda: self.toggleSetting('askBeforeActions'))
    self.askBeforeActions.setChecked(Settings.getBooleanSetting('askBeforeActions'))

    self.showEditDictWordsButton = QCheckBox("Show 'Edit Dictionary Words' button?", objectName='showEditDictWordsButton')
    self.showEditDictWordsButton.clicked.connect(lambda: self.toggleSetting('showEditDictWordsButton'))
    self.showEditDictWordsButton.setChecked(Settings.getBooleanSetting('showEditDictWordsButton'))

    self.layout.addWidget(self.rememberLastGradePicked)
    self.layout.addWidget(self.askBeforeActions)
    self.layout.addWidget(self.showEditDictWordsButton)

  def toggleSetting(self, settingName):
    settingCheckbox = self.findChild(QCheckBox, settingName)
    newValue = settingCheckbox.isChecked()
    Settings.setBooleanSetting(settingName, newValue)

    if settingName == 'showEditDictWordsButton':
      from MainWidget.searchingWidget import SearchingWidget
      SearchingWidget.toggleEditWordsButtonVisibility(newValue)

  def style(self):
    self.setStyleSheet(
      "QPushButton:hover { background-color: grey }\n"
      "QWidget { background-color: green }"
    )
