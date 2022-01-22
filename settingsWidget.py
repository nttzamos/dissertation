from PyQt6.QtWidgets import QVBoxLayout, QDialog, QLabel

from settings import Settings

class SettingsWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Settings")
    self.setFixedSize(Settings.screenWidth / 2, Settings.screenHeight / 2)
    self.setContentsMargins(0, 0, 0, 0)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)

    settingLabel1 = QLabel("Setting 1")
    settingLabel2 = QLabel("Setting 2")
    self.layout.addWidget(settingLabel1)
    self.layout.addWidget(settingLabel2)
    # remember last grade picked when re opening app
    #

  def style(self):
    self.setStyleSheet(
      "QPushButton:hover { background-color: grey }\n"
      "QWidget { background-color: green }"
    )
