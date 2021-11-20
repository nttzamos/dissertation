from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from recentSearch import RecentSearch

class BoxLayout(QListWidget):
  def __init__(self):
    super().__init__()

    self.setStyleSheet("QListWidget::item:hover { background: transparent }")

    self.itemN1 = QListWidgetItem()
    self.itemN2 = QListWidgetItem()
    self.itemN3 = QListWidgetItem()
    
    #Create widget
    # self.widget = QWidget()
    # self.widgetText =  QLabel("I love PyQt!")
    # self.widgetButton =  QPushButton("Push Me")
    # self.widgetLayout = QHBoxLayout()
    # self.widgetLayout.addWidget(self.widgetText)
    # self.widgetLayout.addWidget(self.widgetButton)
    # self.widgetLayout.addStretch()

    self.widget1 = RecentSearch("word1", True)
    self.widget2 = RecentSearch("word2", True)
    self.widget3 = RecentSearch("word3", True)

    # widgetLayout.setSizeConstraint(QLayout.setSizeConstraint())
    # widgetLayout.setSizeConstraint(f)
    # self.widget.setLayout(self.widgetLayout)  
    self.itemN1.setSizeHint(self.widget1.sizeHint())
    self.itemN2.setSizeHint(self.widget2.sizeHint())
    self.itemN3.setSizeHint(self.widget3.sizeHint())

    self.setSpacing(20)
    #Add widget to QListWidget funList
    # funList.addItem(itemN)
    # funList.setItemWidget(itemN, widget)
    self.addItem(self.itemN1)
    self.setItemWidget(self.itemN1, self.widget1)

    self.addItem(self.itemN2)
    self.setItemWidget(self.itemN2, self.widget2)

    self.addItem(self.itemN3)
    self.setItemWidget(self.itemN3, self.widget3)

  def addRow():
    pass
