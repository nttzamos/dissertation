from PyQt6.QtWidgets import QWidget, QMessageBox

from menu.settings import Settings

import os
import gettext

language_code = Settings.get_setting('language')
if language_code == False: language_code = 'el'
language = gettext.translation('shared', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class ResourcesManager(QWidget):
  resources_files = [
    'minimize_window.png', 'plus.png', 'book.png', 'window_icon.png',
    'settings.png', 'database.db', 'question.png', 'clear_search.png',
    'starred.svg', 'search.png', 'reload.svg', 'database_backup.db',
    'window_icon.ico', 'delete.svg', 'close_window.png', 'unstarred.svg',
    'edit.svg' # 'settings.json'
  ]

  def __init__(self):
    if not os.path.isdir('resources'):
      self.show_no_resources_folder_message()
      quit()

    current_resources_files = os.listdir('resources')
    missing_resources_files = list(set(ResourcesManager.resources_files) - set(current_resources_files))

    if len(missing_resources_files) > 0:
      self.show_missing_resources_files_message(missing_resources_files)

  def show_no_resources_folder_message(self):
    title = _('MISSING_FOLDER_TITLE')
    text = _('MISSING_FOLDER_MESSAGE')

    answer = QMessageBox()
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(text)
    answer.setWindowTitle(title)
    answer.setStandardButtons(QMessageBox.StandardButton.Ok)
    answer.exec()

  def show_missing_resources_files_message(self, files):
    title = _('MISSING_FILES_TITLE')
    text = _('MISSING_FILES_MESSAGE') + '\n\n' + str(files)

    answer = QMessageBox()
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(text)
    answer.setWindowTitle(title)
    answer.setStandardButtons(QMessageBox.StandardButton.Ok)
    answer.exec()
