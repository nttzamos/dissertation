from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QDialog, QMessageBox, QCheckBox
from PyQt6.QtGui import QIcon

from dialogs.profile_addition_widget import ProfileAdditionWIdget
from dialogs.profile_update_widget import ProfileUpdateWidget
from dialogs.student_addition_widget import StudentAdditionWidget
from dialogs.student_update_widget import StudentUpdateWidget
from menu.settings import Settings
from shared.font_settings import FontSettings

import gettext

class DataEditingWidget(QDialog):
  def __init__(self):
    super().__init__()

    language_code = Settings.get_setting('language')
    language = gettext.translation('dialogs', localedir='resources/locale', languages=[language_code])
    language.install()
    self._ = language.gettext

    self.setWindowTitle(self._('EDIT_DATA_TEXT'))
    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setFixedWidth(Settings.get_setting('screen_width') / 2)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    add_student_widget = StudentAdditionWidget()
    DataEditingWidget.edit_student_widget = StudentUpdateWidget()
    add_profile_widget = ProfileAdditionWIdget()
    self.edit_profiles_widget = ProfileUpdateWidget()

    tab_widget = QTabWidget()
    tab_widget.setFont(FontSettings.get_font('text'))

    tab_widget.addTab(add_student_widget, self._('ADD_STUDENT_TEXT'))
    tab_widget.addTab(DataEditingWidget.edit_student_widget, self._('EDIT_STUDENT_TEXT'))
    tab_widget.addTab(add_profile_widget, self._('ADD_PROFILE_TEXT'))
    tab_widget.addTab(self.edit_profiles_widget, self._('EDIT_PROFILE_TEXT'))

    self.layout.addWidget(tab_widget)

  def reject(self):
    if (DataEditingWidget.edit_student_widget.save_button_is_active() or
        self.edit_profiles_widget.save_button_is_active()):
      close_widget = self.show_unsaved_changes_message()

      if not close_widget:
        return

    self.done(1)

  def closeEvent(self, event):
    if (DataEditingWidget.edit_student_widget.save_button_is_active() or
        self.edit_profiles_widget.save_button_is_active()):
      close_widget = self.show_unsaved_changes_message()

      if not close_widget:
        event.ignore()

  def show_unsaved_changes_message(self):
    if not Settings.get_boolean_setting('show_unsaved_changes_message'): return True

    title = self._('UNSAVED_CHANGES_TITLE')
    question = self._('UNSAVED_CHANGES_TEXT')

    answer = QMessageBox()

    answer.setFont(FontSettings.get_font('text'))
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(question)
    answer.setWindowTitle(title)

    yes_button = answer.addButton(self._('YES'), QMessageBox.ButtonRole.YesRole)
    yes_button.setFont(FontSettings.get_font('text'))
    cancel_button = answer.addButton(self._('CANCEL'), QMessageBox.ButtonRole.RejectRole)
    cancel_button.setFont(FontSettings.get_font('text'))

    from shared.styles import Styles
    yes_button.setStyleSheet(Styles.result_dialog_style)
    cancel_button.setStyleSheet(Styles.result_dialog_default_button_style)

    answer.setDefaultButton(cancel_button)

    check_box = QCheckBox(self._('UNSAVED_CHANGES_MESSAGE_VISIBILITY'))
    check_box.setFont(FontSettings.get_font('text'))
    check_box.clicked.connect(self.toggle_unsaved_changes_setting)
    check_box.setChecked(True)

    answer.setCheckBox(check_box)
    answer.exec()

    if answer.clickedButton() == yes_button:
      return True

    return False

  def toggle_unsaved_changes_setting(self, value):
    Settings.set_boolean_setting('show_unsaved_changes_message', value)

  @staticmethod
  def update_student_update_widget():
    DataEditingWidget.edit_student_widget.update_student_update_widget()
