from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import QSize

class Subject(QWidget):
  def __init__(self, word):
    super().__init__()
    self.setMinimumSize(QSize(200, 100))
    self.layout = QHBoxLayout(self)

    self.label = QLabel(word)
    self.addButton = QPushButton()
    self.addButton.setText("Add")
    self.removeButton = QPushButton()
    self.removeButton.setText("Remove")
    
    # TO-DO
    # self.removeButton.clicked.connect(parent.onClick)

    self.layout.addWidget(self.label)
    self.layout.addWidget(self.addButton)
    self.layout.addWidget(self.removeButton)
  