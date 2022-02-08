from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog, QCheckBox, QWidget, QRadioButton, QSpinBox, QLabel, QGroupBox
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

from MenuBar.settings import Settings

class SettingsWidget(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Settings')
    self.setWindowIcon(QIcon('Resources/windowIcon.svg'))

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 20, 20, 20)
    self.layout.setSpacing(20)

    section_label_font = QFont(Settings.font, 16)
    spin_box_font = QFont(Settings.font, 12)

    maximum_results_label = QLabel('Maximum Results:')
    self.maximum_results_spin_box = QSpinBox()
    self.maximum_results_spin_box.setFont(spin_box_font)
    self.maximum_results_spin_box.valueChanged.connect(self.maximum_results_changed)
    self.maximum_results_spin_box.setValue(Settings.get_maximum_results())
    self.maximum_results_spin_box.setMinimum(1)
    self.maximum_results_spin_box.setMaximum(50)

    maximum_results_selection_widget = QGroupBox('Maximum results')
    maximum_results_selection_widget.setFont(section_label_font)
    maximum_results_selection_widget.layout = QHBoxLayout(maximum_results_selection_widget)
    maximum_results_selection_widget.layout.setContentsMargins(10, 0, 0, 0)
    maximum_results_selection_widget.layout.addWidget(maximum_results_label)
    maximum_results_selection_widget.layout.addWidget(self.maximum_results_spin_box)

    general_settings_widget = QGroupBox('General Settings')
    general_settings_widget.setFont(section_label_font)
    general_settings_widget.layout = QVBoxLayout(general_settings_widget)
    general_settings_widget.layout.setContentsMargins(10, 0, 0, 0)

    self.remember_last_student_picked = QCheckBox('Remember last student picked when re-opening app?', objectName='remember_last_student_picked')
    self.remember_last_student_picked.clicked.connect(lambda: self.toggle_setting('remember_last_student_picked'))
    self.remember_last_student_picked.setChecked(Settings.get_boolean_setting('remember_last_student_picked'))

    self.ask_before_actions = QCheckBox('Ask before updating/deleting words?', objectName='ask_before_actions')
    self.ask_before_actions.clicked.connect(lambda: self.toggle_setting('ask_before_actions'))
    self.ask_before_actions.setChecked(Settings.get_boolean_setting('ask_before_actions'))

    self.show_edit_dict_words_button = QCheckBox("Show 'Edit Dictionary Words' button?", objectName='show_edit_dict_words_button')
    self.show_edit_dict_words_button.clicked.connect(lambda: self.toggle_setting('show_edit_dict_words_button'))
    self.show_edit_dict_words_button.setChecked(Settings.get_boolean_setting('show_edit_dict_words_button'))

    general_settings_widget.layout.addWidget(self.remember_last_student_picked)
    general_settings_widget.layout.addWidget(self.ask_before_actions)
    general_settings_widget.layout.addWidget(self.show_edit_dict_words_button)

    theme_selection_widget = QGroupBox('Theme Section')
    theme_selection_widget.setFont(section_label_font)
    theme_selection_widget.layout = QHBoxLayout(theme_selection_widget)
    self.light_theme_button = QRadioButton('Light Theme')
    self.light_theme_button.toggled.connect(self.light_theme_button_clicked)
    self.dark_theme_button = QRadioButton('Dark Theme')
    self.dark_theme_button.toggled.connect(self.dark_theme_button_clicked)

    if Settings.get_theme() == 'light':
      self.light_theme_button.setChecked(True)
    else:
      self.dark_theme_button.setChecked(True)

    theme_selection_widget.layout.setContentsMargins(10, 0, 0, 0)
    theme_selection_widget.layout.addWidget(self.light_theme_button, alignment=Qt.AlignmentFlag.AlignLeft)
    theme_selection_widget.layout.addWidget(self.dark_theme_button, alignment=Qt.AlignmentFlag.AlignLeft)

    self.default_editing_action_widget = QWidget()
    self.default_editing_action_widget.layout = QHBoxLayout(self.default_editing_action_widget)
    self.update_button = QRadioButton('Update')
    self.update_button.toggled.connect(self.update_button_clicked)
    self.delete_button = QRadioButton('Delete')
    self.delete_button.toggled.connect(self.delete_button_clicked)

    if Settings.get_default_editing_action() == 'update':
      self.update_button.setChecked(True)
    else:
      self.delete_button.setChecked(True)

    self.default_editing_action_widget.layout.setContentsMargins(30, 0, 0, 0)
    self.default_editing_action_widget.layout.addWidget(self.update_button, alignment=Qt.AlignmentFlag.AlignLeft)
    self.default_editing_action_widget.layout.addWidget(self.delete_button, alignment=Qt.AlignmentFlag.AlignLeft)

    self.layout.addWidget(maximum_results_selection_widget)
    self.layout.addWidget(general_settings_widget)
    self.layout.addWidget(theme_selection_widget)
    # self.layout.addWidget(self.default_editing_action_widget)

    self.style()

  def style(self):
    from Common.styles import Styles
    self.setStyleSheet(Styles.settings_widget_style)

  def maximum_results_changed(self):
    Settings.set_maximum_results(self.maximum_results_spin_box.value())

  def toggle_setting(self, setting_name):
    setting_check_box = self.findChild(QCheckBox, setting_name)
    new_value = setting_check_box.isChecked()
    Settings.set_boolean_setting(setting_name, new_value)

    if setting_name == 'show_edit_dict_words_button':
      from MainWidget.searchingWidget import SearchingWidget
      SearchingWidget.toggle_edit_words_button_visibility(new_value)

  def light_theme_button_clicked(self):
    if self.light_theme_button.isChecked():
      Settings.set_theme('light')

  def dark_theme_button_clicked(self):
    if self.dark_theme_button.isChecked():
      Settings.set_theme('dark')

  def update_button_clicked(self):
    if self.update_button.isChecked():
      Settings.set_default_editing_action('update')

  def delete_button_clicked(self):
    if self.delete_button.isChecked():
      Settings.set_default_editing_action('delete')
