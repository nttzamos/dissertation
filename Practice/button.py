from PyQt6.QtWidgets import QPushButton

class Button(QPushButton):
  def __init__(self, id):
    super().__init__()
    self.setText("Push me")
    self.id = id
    self.clicked.connect(self.clickme)

  def clickme(self):
    from window import Window
    Window.addRow("Word" + str(self.id))