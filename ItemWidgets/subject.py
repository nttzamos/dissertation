from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import QSize
# from PyQt6.QtGui import QFont

class Subject(QWidget):
  def __init__(self, word):
    super().__init__()
    self.setMinimumSize(QSize(200, 100))
    self.layout = QHBoxLayout(self)

    self.label = QLabel(word)
    self.button1 = QPushButton()
    self.button1.setText("Add")
    self.button2 = QPushButton()
    self.button2.setText("Remove")
    
    # TO-DO
    # self.button2.clicked.connect(parent.onClick)

    self.layout.addWidget(self.label)
    self.layout.addWidget(self.button1)
    self.layout.addWidget(self.button2)
  