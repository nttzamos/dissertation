from PyQt6.QtWidgets import QWidget, QMessageBox, QCheckBox

from menu.settings import Settings

import os

class ResourcesManager(QWidget):
  resources_files = [
    'minimize_window.png', 'plus.png', 'book.png', 'window_icon.png',
    'settings.png', 'database.db', 'question.png', 'clear_search.png',
    'starred.svg', 'search.png', 'reload.svg', 'database_backup.db',
    'window_icon.ico', 'delete.svg', 'close_window.png', 'unstarred.svg'
    # 'settings.json'
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
    title = 'Απουσία Φακέλου Αρχείων'
    text = ('Ο φάκελος "resources" απουσιάζει από τον φάκελο που βρίσκεται το '
            'αρχείο του εκτελέσιμου προγράμματος. Ο φάκελος αυτός είναι '
            'αναγκαίος για την εκτέλεση της εφαρμογής. Η λειτουργία της '
            'εφαρμογής θα τερματιστεί.')

    answer = QMessageBox()
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(text)
    answer.setWindowTitle(title)
    answer.setStandardButtons(QMessageBox.StandardButton.Ok)
    answer.exec()

  def show_missing_resources_files_message(self, files):
    title = 'Απουσία Αρχείων'
    text = ('Απουσιάζουν από τον φάκελο "resources" αρχεία που είναι αναγκαία '
            'για την εκτέλεση της εφαρμογής. Αυτό μπορεί να οδηγήσει σε '
            'πολύ σοβαρά προβλήματα και η εφαρμογή μπορεί να τερματιστεί '
            'αναπάντεχα, πιθανώς καταστρέφοντας τα δεδομένα σας. Τα αρχεία που '
            'απουσιάζουν είναι τα εξής:\n\n' + str(files))

    answer = QMessageBox()
    answer.setIcon(QMessageBox.Icon.Critical)
    answer.setText(text)
    answer.setWindowTitle(title)
    answer.setStandardButtons(QMessageBox.StandardButton.Ok)

    answer.exec()
