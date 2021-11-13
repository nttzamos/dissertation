from PyQt6.QtWidgets import QGridLayout, QMainWindow, QWidget
from button import Button
from word import Word

class Window(QWidget):
  grid = QGridLayout()
  counter = 0

  def __init__(self):
    super().__init__()

    self.setGeometry(200, 200, 700, 400)
    self.setWindowTitle("I hope this works!")

    Window.addRow("Word 1")

    self.setLayout(Window.grid)

  @staticmethod
  def addRow(word):
    Window.grid.addWidget(Word(word), Window.counter, 0)
    Window.grid.addWidget(Button(Window.counter), Window.counter, 1)
    Window.counter += 1
