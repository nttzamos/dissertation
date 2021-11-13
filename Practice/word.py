from PyQt6.QtWidgets import QLabel

class Word(QLabel):
  def __init__(self, word):
    super().__init__()
    self.setText(word)
