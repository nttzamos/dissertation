from PyQt6.QtWidgets import QWidget, QMessageBox

import os

class ResourcesManager(QWidget):
  resources_files = [
    'book.png', 'clear_search.png', 'close_window.png', 'database_backup.db',
    'database.db', 'delete.svg', 'edit.svg', 'minimize_window.png',
    'plus.png', 'question.png', 'search.png', 'settings.png', 'starred.svg',
    'undo.png', 'unstarred.svg', 'window_icon.ico', 'window_icon.png' # 'settings.json'
  ]

  def __init__(self):
    if not os.path.isdir('resources'):
      text = (
        'The \"resources\" folder is missing from the folder where the '
        'executable file is in. This folder is essential for the application '
        'execution. The application will be terminated.'
      )

      self.show_message('Missing Folder', text)
      quit()

    current_resources_files = os.listdir('resources')
    missing_resources_files = list(set(ResourcesManager.resources_files) - set(current_resources_files))

    if len(missing_resources_files) > 0:
      text = (
        'Files from the \"resources\" folder that are essential for the '
        'application execution are missing. This may lead to serious problems '
        'and the application may terminate unexpectedly, possibly destroying '
        'your data. Files missing are:'
      )

      self.show_message('Missng Files', text + '\n\n' + str(missing_resources_files))

  def show_message(self, title, text):
    answer = QMessageBox()
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(text)
    answer.setWindowTitle(title)
    answer.setStandardButtons(QMessageBox.StandardButton.Ok)
    answer.exec()
