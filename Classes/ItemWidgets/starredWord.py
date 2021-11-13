from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

class StarredWord(QWidget):
  def __init__(self, word):
    super().__init__()

    # self.parent = parent
    self.setMinimumSize(QSize(200, 100))
    self.layout = QHBoxLayout(self)

    self.label = QLabel(word)

    # Old Version
    # self.button1 = QtWidgets.QPushButton()
    # self.button1.clicked.connect(self.unstarWord)
    # self.button1.setText("Unstar")

    # New Version
    self.button = QPushButton()
    # self.button2.setText("Star")
    self.button.setIcon(QIcon("resources/starred.svg"))
    self.button.clicked.connect(self.toggleStarred)

    self.layout.addWidget(self.label)
    self.layout.addWidget(self.button)
    