from PyQt6.QtWidgets import QGridLayout, QWidget
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont

from result import Result

class ResultsWidget(QWidget):
  def __init__(self):
    super().__init__()
    # self.layout = QtWidgets.QHBoxLayout(self)
    # self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
    #                                              QtWidgets.QSizePolicy.MinimumExpanding))

    self.setWidgetResizable(True)
    # self.scrollArea.setMinimumSize(QtCore.QSize(1200, 700))
    # self.setFixedSize(QtCore.QSize(1200, 700))
    # self.setGeometry(0, 0, 1200, 700)

    self.scrollAreaWidgetContents = QWidget()
    # self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(1200, 700))
    # self.gridLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
    self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)

    self.word1 = Result(self.scrollAreaWidgetContents)
    self.word2 = Result(self.scrollAreaWidgetContents)
    self.word3 = Result(self.scrollAreaWidgetContents)
    # self.word4 = Result(self.scrollAreaWidgetContents)
    self.word5 = Result(self.scrollAreaWidgetContents)
    self.word6 = Result(self.scrollAreaWidgetContents)
    self.word7 = Result(self.scrollAreaWidgetContents)
    # self.word8 = Result(self.scrollAreaWidgetContents)
    self.word9 = Result(self.scrollAreaWidgetContents)
    self.word10 = Result(self.scrollAreaWidgetContents)
    self.word11 = Result(self.scrollAreaWidgetContents)
    # self.word12 = Result(self.scrollAreaWidgetContents)
    self.word13 = Result(self.scrollAreaWidgetContents)
    self.word14 = Result(self.scrollAreaWidgetContents)
    self.word15 = Result(self.scrollAreaWidgetContents)
    # self.word16 = Result(self.scrollAreaWidgetContents)
    self.word17 = Result(self.scrollAreaWidgetContents)
    self.word18 = Result(self.scrollAreaWidgetContents)
    self.word19 = Result(self.scrollAreaWidgetContents)
    # self.word20 = Result(self.scrollAreaWidgetContents)

    # self.word1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
    # self.word2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
    # self.word3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
    # self.word4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
    # self.word5 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
    # self.word1.setText("hello")
    # self.word2.setText("hello")
    # self.word3.setText("hello")
    # self.word4.setText("hello")
    # self.word5.setText("hello")


    self.gridLayout.addWidget(self.word1, 0, 0)
    self.gridLayout.addWidget(self.word2, 0, 1)
    self.gridLayout.addWidget(self.word3, 0, 2)
    self.gridLayout.addWidget(self.word5, 1, 0)
    self.gridLayout.addWidget(self.word6, 1, 1)
    self.gridLayout.addWidget(self.word7, 1, 2)
    self.gridLayout.addWidget(self.word9, 2, 0)
    self.gridLayout.addWidget(self.word10, 2, 1)
    self.gridLayout.addWidget(self.word11, 2, 2)
    self.gridLayout.addWidget(self.word13, 3, 0)
    self.gridLayout.addWidget(self.word14, 3, 1)
    self.gridLayout.addWidget(self.word15, 3, 2)
    self.gridLayout.addWidget(self.word17, 4, 0)
    self.gridLayout.addWidget(self.word18, 4, 1)
    self.gridLayout.addWidget(self.word19, 4, 2)
    