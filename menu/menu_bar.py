from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from menu.settings import Settings
from menu.settings_widget import SettingsWidget

import gettext

class MenuBar(QWidget):
  def __init__(self):
    super().__init__()

    language_code = Settings.get_setting('language')
    language = gettext.translation('menu', localedir='resources/locale', languages=[language_code])
    language.install()
    _ = language.gettext

    self.setMaximumHeight(30)

    self.layout = QHBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    self.settings_button = QPushButton()
    self.settings_button.setToolTip(_('SETTINGS_TEXT'))
    self.settings_button.setIcon(QIcon('resources/settings.png'))
    self.settings_button.setFixedHeight(30)
    self.settings_button.setFixedWidth(30)
    self.settings_button.clicked.connect(self.open_settings)

    self.tutorial_button = QPushButton()
    self.tutorial_button.setToolTip(_('TUTORIAL_TEXT'))
    self.tutorial_button.setIcon(QIcon('resources/question.png'))
    self.tutorial_button.setFixedHeight(30)
    self.tutorial_button.setFixedWidth(30)
    self.tutorial_button.clicked.connect(self.open_tutorial)

    self.layout.addWidget(self.settings_button)
    self.layout.addWidget(self.tutorial_button, alignment=Qt.AlignmentFlag.AlignLeft)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.menu_bar_style)

  def open_settings(self):
    settings_dialog = SettingsWidget()
    settings_dialog.exec()

  def open_tutorial(self):
    from dialogs.tutorial_widget import TutorialWidget
    tutorial_widget = TutorialWidget()
    tutorial_widget.exec()
