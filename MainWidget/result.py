from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon

class Result(QWidget):
  def __init__(self, word):
    super().__init__()

    self.layout = QGridLayout(self)

    self.word_label = QLabel(self, text=word)
    self.word_label.setStyleSheet("QLabel {border-radius: 100px \ 50px; border : 2px solid black}")
    self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    from settings import Settings
    font = QFont(Settings.font, 20)
    self.word_label.setFont(font)

    self.deleteButton = QPushButton(self)
    self.deleteButton.setStyleSheet(
      "QPushButton:hover { background-color: black }\n"
      "QPushButton {border-radius : 20; border : 2px solid black}")
    self.deleteButton.setIcon(QIcon("Resources/delete2.svg"))

    self.layout.addWidget(self.word_label, 0, 0)
    self.layout.addWidget(self.deleteButton, 1, 0)
