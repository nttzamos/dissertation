from PyQt6.QtWidgets import QLayout
from PyQt6.QtCore import QPoint, QRect, QSize, Qt

class FlowLayout(QLayout):
  def __init__(self):
    super(FlowLayout, self).__init__(None)

    self.item_list = []

  def __del__(self):
    item = self.takeAt(0)
    while item:
      item = self.takeAt(0)

  def addItem(self, item):
    self.item_list.append(item)

  def count(self):
    return len(self.item_list)

  def itemAt(self, index):
    if index >= 0 and index < len(self.item_list):
      return self.item_list[index]

    return None

  def takeAt(self, index):
    if index >= 0 and index < len(self.item_list):
      return self.item_list.pop(index)

    return None

  def expandingDirections(self):
    return Qt.Orientation(Qt.Orientation(0))

  def hasHeightForWidth(self):
    return True

  def heightForWidth(self, width):
    height = self.doLayout(QRect(0, 0, width, 0), True)
    return height

  def setGeometry(self, rect):
    super(FlowLayout, self).setGeometry(rect)
    self.doLayout(rect, False)

  def sizeHint(self):
    return self.minimumSize()

  def minimumSize(self):
    size = QSize()

    for item in self.item_list:
      size = size.expandedTo(item.minimumSize())

    margin, _, _, _ = self.getContentsMargins()

    size += QSize(2 * margin, 2 * margin)
    return size

  def doLayout(self, rect, test_only):
    x = rect.x()
    y = rect.y()
    line_height = 0

    for item in self.item_list:
      nextX = x + item.sizeHint().width()
      if nextX > rect.right() and line_height > 0:
        x = rect.x()
        y = y + line_height
        nextX = x + item.sizeHint().width()
        line_height = 0

      if not test_only:
        item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

      x = nextX
      line_height = max(line_height, item.sizeHint().height())

    return y + line_height + 10 - rect.y()
