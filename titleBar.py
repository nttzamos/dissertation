from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from settings import Settings

class TitleBar(QWidget):
  title = "My Dissertation Title"

  def __init__(self, parent):
    super().__init__()
    self.parent = parent

    self.layout = QHBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.setMaximumHeight(30)

    self.applicationIcon = QPushButton()
    self.applicationIcon.setIcon(QIcon("Resources/windowIcon.svg"))
    self.applicationIcon.setFixedWidth(30)

    self.title = QLabel(TitleBar.title)
    font = QFont(Settings.font, 14)
    self.title.setFont(font)

    self.settingsButton = QPushButton()
    self.settingsButton.setIcon(QIcon("Resources/settings.png"))
    self.settingsButton.setFixedWidth(30)
    self.settingsButton.clicked.connect(self.openSettings)

    self.minimizeWindowButton = QPushButton()
    self.minimizeWindowButton.setIcon(QIcon("Resources/minimizeWindow.png"))
    self.minimizeWindowButton.setFixedWidth(30)
    self.minimizeWindowButton.clicked.connect(self.minimizeWindow)

    self.restoreDownWindowButton = QPushButton()
    self.restoreDownWindowButton.setIcon(QIcon("Resources/restoreDownWindow.png"))
    self.restoreDownWindowButton.setFixedWidth(30)
    self.restoreDownWindowButton.clicked.connect(self.restoreDownWindow)
    
    self.closeWindowButton = QPushButton()
    self.closeWindowButton.setIcon(QIcon("Resources/closeWindow.png"))
    self.closeWindowButton.setFixedWidth(30)
    self.closeWindowButton.clicked.connect(self.closeWindow)

    self.layout.addWidget(self.applicationIcon)
    self.layout.addSpacing(5)
    self.layout.addWidget(self.title)
    self.layout.addWidget(self.settingsButton, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.minimizeWindowButton, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.restoreDownWindowButton, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.closeWindowButton, alignment=Qt.AlignmentFlag.AlignTop)

    self.style()

  def style(self):
    self.setStyleSheet(
      "QPushButton:hover { background-color: grey }\n"
      "QPushButton { border: none }\n"
      "QPushButton { padding-bottom: 5px }\n"
      "QPushButton { padding-top: 5px }\n"
      "QLabel { color: white }"
    )
    
    self.applicationIcon.setStyleSheet(
      "QPushButton:hover { background-color: none }\n"
    )
    
    self.closeWindowButton.setStyleSheet(
      "QPushButton:hover { background-color: #D11A2A }"
    )


  def openSettings(self):
    pass
  
  def minimizeWindow(self):
    self.parent.showMinimized()

  def restoreDownWindow(self):
    pass

  def maximizeWindow(self):
    pass

  def closeWindow(self):
    self.parent.close()