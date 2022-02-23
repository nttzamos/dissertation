from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QLabel, QGroupBox, QListWidget, QPushButton, QComboBox, QCompleter, QAbstractItemView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

from menu.settings import Settings

class TutorialWidget(QDialog):
  TITLES = [
    'Application Introduction', 'Students', 'Profiles', 'Subjects', 'Results'
  ]

  APPLICATION_INTRODUCTION = (
    'Welcome to Wordinary! This is an application that helps young elementary '
    'students learn the word family of words included in their school books.\n'
    '\nIn order to use the app you have to a choose student, a specific profil'
    'e of this student and one or all of the subjects of the specific profile.'
    '\n\nThis application uses Wiktionary to identify words that belong to the'
    ' word family of words you search for.\n\nThe results of your search will '
    'appear in the bottom part of the application.'

  )

  STUDENT_EXPLANATION = (
    'You can create students which correspond to your actual students in order'
    ' to differentiate their details such as profiles, recent searches and sta'
    'rred words.'
  )

  PROFILE_EXPLANATION = (
    'Profiles belong to a specific grade and contain a set of subjects of that'
    ' grade.\n\nThere are 6 default profiles (one for each grade), which conta'
    'in all the subjects of each grade and which can not be edited or deleted.'
    '\n\nYou can create new profiles or edit/delete existing ones by pressing '
    'the "Edit Data" button.'
  )

  SUBJECT_EXPLANATION = (
    'As you have already learned, the profiles consist of multiple subjects.\n'
    '\nThe subject(s) you select define(s) the dictionary of words which you c'
    'an search from in the search bar located in the upper area, as well as yo'
    'ur recent searches and starred words located in the leftmost area of the '
    'application.\n\nThe subject selection does not in any way limit the words'
    ' that are going to appear in your search results. These are only limited '
    'by the grade to which these subjects belong.\n\nAll in all, selecting a s'
    'ubject does not mean that results from other subjects will not appear in '
    'your search results.'
  )

  RESULT_EXPLANATION = (
    'Results are displayed in the bottom part of the application, after search'
    'ing for a word.\n\nWords that belong to the grade of the selected subject'
    ' are displayed without a frame.\n\nWords that Wiktionary believes belong '
    'to the family of the selected word but do not belong to any of the subjec'
    'ts of the profile grade, are displayed within a blue frame.'
  )

  TEXTS = [
    APPLICATION_INTRODUCTION, STUDENT_EXPLANATION, PROFILE_EXPLANATION,
    SUBJECT_EXPLANATION, RESULT_EXPLANATION
  ]

  def __init__(self):
    super().__init__()
    self.setWindowTitle('Tutorial')
    self.setWindowIcon(QIcon('resources/window_icon.png'))

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    self.setFixedHeight(400)
    self.setFixedWidth(750)

    section_label_font = QFont(Settings.font, 20)
    text_font = QFont(Settings.font, 16)

    self.current_tutorial = 0

    self.group_box_widget = QGroupBox()
    self.group_box_widget.setFont(section_label_font)
    self.group_box_widget.layout = QHBoxLayout(self.group_box_widget)
    self.group_box_widget.layout.setContentsMargins(0, 0, 0, 0)

    self.explanation = QLabel()
    self.explanation.setWordWrap(True)
    self.explanation.setFont(text_font)

    self.group_box_widget.layout.addWidget(self.explanation, alignment=Qt.AlignmentFlag.AlignTop)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.setSpacing(5)

    self.setting_check_box = QCheckBox('Show tutorial on startup')
    self.setting_check_box.clicked.connect(self.toggle_tutorial_setting)
    if Settings.get_setting('show_tutorial_on_startup'):
      self.setting_check_box.setChecked(True)

    self.next_tutorial_button = QPushButton('Next')
    self.next_tutorial_button.adjustSize()
    self.next_tutorial_button.pressed.connect(self.next_tutorial)

    self.previous_tutorial_button = QPushButton('Previous')
    self.previous_tutorial_button.adjustSize()
    self.previous_tutorial_button.pressed.connect(self.previous_tutorial)
    self.previous_tutorial_button.setDisabled(True)

    self.close_tutorial_button = QPushButton('Close')
    self.close_tutorial_button.adjustSize()
    self.close_tutorial_button.pressed.connect(self.close)

    buttons_widget.layout.addWidget(self.setting_check_box, alignment=Qt.AlignmentFlag.AlignLeft)
    buttons_widget.layout.addWidget(self.close_tutorial_button, alignment=Qt.AlignmentFlag.AlignRight)
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
    if self.current_tutorial < len(TutorialWidget.TEXTS) - 1:
      self.current_tutorial += 1
      self.update_tutorial()

    if self.current_tutorial == len(TutorialWidget.TEXTS) - 1:
      self.next_tutorial_button.setDisabled(True)
    elif self.current_tutorial == 1:
      self.previous_tutorial_button.setEnabled(True)

  def previous_tutorial(self):
    if self.current_tutorial > 0:
      self.current_tutorial -= 1
      self.update_tutorial()

    if self.current_tutorial == 0:
      self.previous_tutorial_button.setDisabled(True)
    elif self.current_tutorial == len(TutorialWidget.TEXTS) - 2:
      self.next_tutorial_button.setEnabled(True)

  def update_tutorial(self):
    counter_text = (' (' + str(self.current_tutorial + 1) + '/' +
      str(len(TutorialWidget.TEXTS)) + ')'
    )
    self.group_box_widget.setTitle(TutorialWidget.TITLES[self.current_tutorial] + counter_text)
    self.explanation.setText(TutorialWidget.TEXTS[self.current_tutorial])

  def toggle_tutorial_setting(self):
    Settings.set_boolean_setting('show_tutorial_on_startup', self.setting_check_box.isChecked())
