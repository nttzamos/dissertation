from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from menu.settings import Settings
from menu.settings_widget import SettingsWidget

class MenuBar(QWidget):
  SETTINGS_TEXT = 'Ρυθμίσεις'
  TUTORIAL_TEXT = 'Οδηγίες'
  MINIMIZE_APPLICATION_TEXT = 'Ελαχιστοποίηση εφαρμογής'
  EXIT_APPLICATION_TEXT = 'Κλείσιμο εφαρμογής'

  def __init__(self, parent):
    super().__init__()
    self.parent = parent

    self.setMaximumHeight(30)

    self.layout = QHBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.application_icon = QPushButton()
    self.application_icon.setIcon(QIcon('resources/window_icon.png'))
    self.application_icon.setFixedHeight(30)
    self.application_icon.setFixedWidth(30)

    font = QFont(Settings.FONT, 14)

    self.title = QLabel('Wordinary')
    self.title.setFont(font)

    self.settings_button = QPushButton()
    self.settings_button.setToolTip(MenuBar.SETTINGS_TEXT)
    self.settings_button.setIcon(QIcon('resources/settings.png'))
    self.settings_button.setFixedHeight(30)
    self.settings_button.setFixedWidth(30)
    self.settings_button.clicked.connect(self.open_settings)

    self.tutorial_button = QPushButton()
    self.tutorial_button.setToolTip(MenuBar.TUTORIAL_TEXT)
    self.tutorial_button.setIcon(QIcon('resources/question.png'))
    self.tutorial_button.setFixedHeight(30)
    self.tutorial_button.setFixedWidth(30)
    self.tutorial_button.clicked.connect(self.open_tutorial)

    self.minimize_window_button = QPushButton()
    self.minimize_window_button.setToolTip(MenuBar.MINIMIZE_APPLICATION_TEXT)
    self.minimize_window_button.setIcon(QIcon('resources/minimize_window.png'))
    self.minimize_window_button.setFixedHeight(30)
    self.minimize_window_button.setFixedWidth(30)
    self.minimize_window_button.clicked.connect(self.minimize_window)

    self.close_window_button = QPushButton()
    self.close_window_button.setToolTip(MenuBar.EXIT_APPLICATION_TEXT)
    self.close_window_button.setIcon(QIcon('resources/close_window.png'))
    self.close_window_button.setFixedHeight(30)
    self.close_window_button.setFixedWidth(30)
    self.close_window_button.clicked.connect(self.close_window)

    self.layout.addWidget(self.application_icon)
    self.layout.addSpacing(5)
    self.layout.addWidget(self.title)
    self.layout.addWidget(self.tutorial_button, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.minimize_window_button, alignment=Qt.AlignmentFlag.AlignTop)
    self.layout.addWidget(self.close_window_button, alignment=Qt.AlignmentFlag.AlignTop)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.menu_bar_style)
    self.application_icon.setStyleSheet(Styles.application_icon_style)
    self.close_window_button.setStyleSheet(Styles.close_window_button_style)

  def open_settings(self):
    settings_dialog = SettingsWidget()
    settings_dialog.exec()

  def open_tutorial(self):
    from dialogs.tutorial_widget import TutorialWidget
    tutorial_widget = TutorialWidget()
    tutorial_widget.exec()

  def minimize_window(self):
    self.parent.showMinimized()

  def close_window(self):
    self.parent.close()
