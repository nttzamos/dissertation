from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont

from menu.settings import Settings

class Spacer(QLabel):
  def __init__(self):
    super().__init__('f')

    invisible_font = QFont(Settings.FONT, 1)
    self.setFont(invisible_font)

    size_policy = self.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)

    self.setSizePolicy(size_policy)
