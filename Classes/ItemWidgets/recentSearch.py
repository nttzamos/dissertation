from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

class RecentSearch(QWidget):
  def __init__(self, word, condition):
    super().__init__()

    # self.parent = parent
    # self.database = DBHandler()

    self.setMinimumSize(QSize(200, 100))
    self.layout = QHBoxLayout(self)

    self.label = QLabel(word)
    self.button1 = QPushButton()
    # self.button1.setText("Reload")
    self.button1.setIcon(QIcon("resources/reload.svg"))
    self.button1.clicked.connect(self.reloadWord)

    self.button2 = QPushButton()
    # self.button2.setText("Star")
    self.button2.clicked.connect(self.notifyStarred)
    self.starredCondition = condition
    if condition:
      self.button2.setIcon(QIcon("resources/starred.svg"))
    else:
      self.button2.setIcon(QIcon("resources/unstarred.svg"))

    # self.button3 = QtWidgets.QAction(self)
    # self.button3.setText("&New")
    # self.button3.setIcon(QtGui.QIcon("file-new.svg"))

    self.button3 = QPushButton()
    # self.button3.setText("Remove")
    self.button3.setIcon(QIcon("resources/delete2.svg"))
    self.button3.clicked.connect(self.removeWord)

    self.layout.addWidget(self.label)
    self.layout.addWidget(self.button1)
    self.layout.addWidget(self.button2)
    self.layout.addWidget(self.button3)
    