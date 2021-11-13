from PyQt6.QtWidgets import QLabel, QPushButton, QWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon

class Result(QWidget):
  def __init__(self):
    super().__init__()

    self.setFixedSize(QSize(300, 200))
    self.word = QLabel(self)
    self.word.setGeometry(50, 50, 200, 100)
    # self.pushButton_3.setStyleSheet("QLabel {border-top-left-radius: 100px 50px;\
    #    border-top-right-radius: 100px 50px; border-bottom-right-radius: 100px 50px;\
    #       border-bottom-left-radius: 100px 50px; border : 2px solid black}")
    self.word.setStyleSheet("QLabel {border-radius: 100px \ 50px; border : 2px solid black}")
    self.word.setText("Test")
    # self.p = self.palette()
    # self.p.setColor(self.backgroundRole(), QtCore.Qt.red)
    # self.setPalette(self.p)
    # self.setAutoFillBackground(True)
    self.word.setAlignment(Qt.AlignmentFlag.AlignCenter)
    font = QFont()
    font.setPointSize(20)
    self.word.setFont(font)

    self.deleteButton = QPushButton(self)
    self.deleteButton.setGeometry(200, 45, 40, 40)
    self.deleteButton.setStyleSheet(
      "QPushButton:hover { background-color: black; }\n"
      "QPushButton {border-radius : 20; border : 2px solid black}")
    self.deleteButton.setIcon(QIcon("resources/delete2.svg"))
    self.deleteButton.pressed.connect(self.testing)
    # self.deleteButton.setText("D")
    