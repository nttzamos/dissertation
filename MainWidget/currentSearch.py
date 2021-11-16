from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont

class CurrentSearch(QWidget):
  def __init__(self):
    super().__init__()
    self.setContentsMargins(10, 10, 10, 10)
    self.setFixedHeight(300)
    self.layout = QHBoxLayout(self)

    self.word = QLabel(self)
    self.word.setText("Enter a word.")
    self.word.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.word.setFixedSize(QSize(300, 200))
    self.word.setGeometry(50, 50, 300, 200)
    self.word.setStyleSheet("QLabel {border : 2px solid black}")

    font = QFont()
    font.setPointSize(20)
    self.word.setFont(font)

    self.layout.addWidget(self.word)

    self.subLayout = QVBoxLayout()
    self.pauseButton = QPushButton()
    self.pauseButton.setText("Pause")

    self.pauseButton.setFixedHeight(50)
    self.pauseButton.setFixedWidth(100)
    self.pauseButton.setContentsMargins(0, 50, 50, 0)
    self.pauseButton.setStyleSheet(
      "QPushButton:hover { background-color: grey; }\n"
      "QPushButton {border : 2px solid black}")

    self.disableButton = QPushButton()
    self.disableButton.setText("Disable")

    self.disableButton.setFixedHeight(50)
    self.disableButton.setFixedWidth(100)
    self.disableButton.setContentsMargins(50, 0, 0, 0)
    self.disableButton.setStyleSheet(
      "QPushButton:hover { background-color: red; }\n"
      "QPushButton {border : 2px solid black}")

    self.subLayout.addWidget(self.pauseButton)
    self.subLayout.addWidget(self.disableButton)

    self.layout.addLayout(self.subLayout)

  def getCurrentWord(self):
    return self.word.text()