from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QIcon

from Common.databaseHandler import DBHandler

class StarredWord(QWidget):
  def __init__(self, word):
    super().__init__()

    self.setFixedHeight(50)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    self.data_widget = QWidget()
    self.data_widget.layout = QHBoxLayout(self.data_widget)
    self.data_widget.layout.setContentsMargins(0, 0, 0, 0)

    self.word = QLabel(word)
    from MenuBar.settings import Settings
    font = QFont(Settings.font, 14)
    self.word.setFont(font)

    self.reload_button = QPushButton()
    self.reload_button.setIcon(QIcon('Resources/reload.svg'))
    self.reload_button.clicked.connect(self.reload_word)
    self.reload_button.setFixedWidth(30)

    self.star_button = QPushButton()
    self.star_button.clicked.connect(self.toggle_starred)
    self.star_button.setFixedWidth(30)
    self.star_button.setIcon(QIcon('Resources/starred.svg'))

    self.line = QFrame()
    self.line.setFrameShape(QFrame.Shape.HLine)
    self.line.setFrameShadow(QFrame.Shadow.Plain)

    self.data_widget.layout.addSpacing(5)
    self.data_widget.layout.addWidget(self.word)
    self.data_widget.layout.addWidget(self.reload_button)
    self.data_widget.layout.addWidget(self.star_button)
    self.data_widget.layout.addSpacing(5)

    self.layout.addWidget(self.data_widget)
    self.layout.addWidget(self.line)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.item_widgets_style)

  def toggle_starred(self):
    from SideWidgets.recentSearchesWidget import RecentSearchesWidget
    word = self.word.text()
    DBHandler.remove_starred_word(word)
    RecentSearchesWidget.toggle_starred_upper(word)
    self.removeWord()

  def removeWord(self):
    from SideWidgets.starredWordsWidget import StarredWordsWidget
    self.hide()
    StarredWordsWidget.remove_starred_word(self)
    self.deleteLater()

  def reload_word(self):
    from MainWidget.mainWidget import MainWidget
    MainWidget.add_word(self.word.text())