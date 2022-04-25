from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont


class Spacer(QLabel):
  def __init__(self):
    super().__init__('f')

    invisible_font = QFont(QFont().family(), 1)
    self.setFont(invisible_font)

    size_policy = self.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)

    self.setSizePolicy(size_policy)
