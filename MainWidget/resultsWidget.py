from PyQt6.QtWidgets import QGridLayout, QScrollArea, QWidget

from MainWidget.result import Result

class ResultsWidget(QScrollArea):
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

    self.word1 = Result()
    self.word2 = Result()
    self.word3 = Result()
    # self.word4 = Result()
    self.word5 = Result()
    self.word6 = Result()
    self.word7 = Result()
    # self.word8 = Result()
    self.word9 = Result()
    self.word10 = Result()
    self.word11 = Result()
    # self.word12 = Result()
    self.word13 = Result()
    self.word14 = Result()
    self.word15 = Result()
    # self.word16 = Result()
    self.word17 = Result()
    self.word18 = Result()
    self.word19 = Result()
    # self.word20 = Result()

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

    self.setWidget(self.scrollAreaWidgetContents)
    