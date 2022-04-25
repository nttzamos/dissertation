from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget,
                             QCheckBox, QLabel, QGroupBox, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from menu.settings import Settings
from shared.font_settings import FontSettings

import gettext

class TutorialWidget(QDialog):
  def __init__(self):
    super().__init__()

    language_code = Settings.get_setting('language')
    language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
    language.install()
    _ = language.gettext

    self.TITLES = [
      _('APPLICATION_INTRODUCTION_TITLE'), _('STUDENT_EXPLANATION_TITLE'),
      _('PROFILE_EXPLANATION_TITLE'), _('SUBJECT_EXPLANATION_TITLE'),
      _('RESULT_EXPLANATION_TUTORIAL_TITLE'), _('VOCABULARY_EXPLANATION_TITLE')
    ]

    self.TEXTS = [
      _('APPLICATION_INTRODUCTION_TEXT'), _('STUDENT_EXPLANATION_TEXT'),
      _('PROFILE_EXPLANATION_TEXT'), _('SUBJECT_EXPLANATION_TEXT'),
      _('RESULT_EXPLANATION_TUTORIAL_TEXT'), _('VOCABULARY_EXPLANATION_TEXT')
    ]

    language_code = Settings.get_setting('language')
    language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
    language.install()
    _ = language.gettext

    self.setWindowTitle(_('TUTORIAL_DIALOG_TITLE'))
    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setFixedHeight(550)
    self.setFixedWidth(850)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    section_label_font = FontSettings.get_font('heading')
    text_font = FontSettings.get_font('text')

    self.current_tutorial = 0

    self.group_box_widget = QGroupBox()
    self.group_box_widget.setFont(section_label_font)
    self.group_box_widget.layout = QHBoxLayout(self.group_box_widget)
    self.group_box_widget.layout.setContentsMargins(0, 0, 0, 0)

    self.explanation = QLabel()
    self.explanation.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    self.explanation.setWordWrap(True)
    self.explanation.setFont(text_font)

    self.group_box_widget.layout.addWidget(self.explanation, alignment=Qt.AlignmentFlag.AlignTop)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.setSpacing(5)

    self.setting_check_box = QCheckBox(_('CHECK_BOX_TEXT'))
    self.setting_check_box.clicked.connect(self.toggle_tutorial_setting)
    if Settings.get_boolean_setting('show_tutorial_on_startup'):
      self.setting_check_box.setChecked(True)

    self.next_tutorial_button = QPushButton(_('NEXT_BUTTON_TEXT'))
    self.next_tutorial_button.adjustSize()
    self.next_tutorial_button.pressed.connect(self.next_tutorial)
    self.next_tutorial_button.setAutoDefault(False)

    self.previous_tutorial_button = QPushButton(_('PREVIOUS_BUTTON_TEXT'))
    self.previous_tutorial_button.adjustSize()
    self.previous_tutorial_button.pressed.connect(self.previous_tutorial)
    self.previous_tutorial_button.setDisabled(True)
    self.previous_tutorial_button.setAutoDefault(False)

    close_tutorial_button = QPushButton(_('CLOSE_BUTTON_TEXT'))
    close_tutorial_button.adjustSize()
    close_tutorial_button.pressed.connect(self.close)
    close_tutorial_button.setAutoDefault(False)

    buttons_widget.layout.addWidget(self.setting_check_box, alignment=Qt.AlignmentFlag.AlignLeft)
    buttons_widget.layout.addWidget(close_tutorial_button, alignment=Qt.AlignmentFlag.AlignRight)
    buttons_widget.layout.addWidget(self.previous_tutorial_button)
    buttons_widget.layout.addWidget(self.next_tutorial_button)

    self.layout.addWidget(self.group_box_widget)
    self.layout.addWidget(buttons_widget, alignment=Qt.AlignmentFlag.AlignBottom)

    self.update_tutorial()

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.tutorial_widget_style)

  def next_tutorial(self):
    if self.current_tutorial < len(self.TEXTS) - 1:
      self.current_tutorial += 1
      self.update_tutorial()

    if self.current_tutorial == len(self.TEXTS) - 1:
      self.next_tutorial_button.setDisabled(True)
    elif self.current_tutorial == 1:
      self.previous_tutorial_button.setEnabled(True)

  def previous_tutorial(self):
    if self.current_tutorial > 0:
      self.current_tutorial -= 1
      self.update_tutorial()

    if self.current_tutorial == 0:
      self.previous_tutorial_button.setDisabled(True)
    elif self.current_tutorial == len(self.TEXTS) - 2:
      self.next_tutorial_button.setEnabled(True)

  def update_tutorial(self):
    counter_text = (
      ' (' + str(self.current_tutorial + 1) + '/' + str(len(self.TEXTS)) + ')'
    )

    self.group_box_widget.setTitle(self.TITLES[self.current_tutorial] + counter_text)
    self.explanation.setText(self.TEXTS[self.current_tutorial])

  def toggle_tutorial_setting(self):
    Settings.set_boolean_setting('show_tutorial_on_startup', self.setting_check_box.isChecked())
