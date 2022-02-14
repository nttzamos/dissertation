from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QDialog, QStackedWidget, QLabel, QCompleter
from PyQt6.QtCore import QStringListModel, QTimer, Qt
from PyQt6.QtGui import QFont

from menu.settings import Settings

import sqlite3

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()

    self.layout = QGridLayout(self)
    self.layout.setContentsMargins(20, 20, 20, 20)

    # Row 0
    self.line_edit = QLineEdit()
    self.line_edit.returnPressed.connect(self.show_word)
    self.completer = QCompleter(self.get_words(1))
    self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completer_font = QFont(Settings.font, 14)
    self.completer.popup().setFont(completer_font)
    self.line_edit.setCompleter(self.completer)
    self.line_edit.setPlaceholderText('Please enter a word.')
    combo_box_font = QFont(Settings.font, 14)
    grade_selector = QComboBox()
    grade_selector.activated.connect(self.grade_selector_activated)
    grade_selector.setFont(combo_box_font)
    grade_selector.addItems(['Α', 'Β', 'Γ'])
    self.layout.addWidget(self.line_edit, 0, 0)
    self.layout.addWidget(grade_selector, 0, 1)

    # Row 1
    self.active_word = QLabel('Please select a word')
    active_word_font = QFont(Settings.font, 20)
    self.active_word.setFont(active_word_font)
    self.layout.addWidget(self.active_word, 1, 0)

    # Row 2
    words_label = QLabel('Words')
    metric_label1 = QLabel('Metric1')
    metric_label2 = QLabel('Metric2')
    metric_label3 = QLabel('Metric3')
    self.layout.addWidget(words_label, 2, 0)
    self.layout.addWidget(metric_label1, 2, 1)
    self.layout.addWidget(metric_label2, 2, 2)
    self.layout.addWidget(metric_label3, 2, 3)

    vspacer = QLabel('f')
    invisible_font = QFont(Settings.font, 1)
    vspacer.setFont(invisible_font)
    size_policy = vspacer.sizePolicy()
    size_policy.setRetainSizeWhenHidden(True)
    vspacer.setSizePolicy(size_policy)
    self.layout.addWidget(vspacer, 1000, 0)

    self.words_list = []

  def show_word(self):
    self.active_word.setText(self.line_edit.text())
    QTimer.singleShot(0, self.line_edit.clear)
    self.calculate_results()

  def grade_selector_activated(self, index):
    model = QStringListModel(self.get_words(index + 1), self.completer)
    self.completer.setModel(model)

  def get_words(self, grade):
    databases_directory_path = 'Databases/'
    database_file = 'database_clarin.db'

    con = sqlite3.connect(databases_directory_path + database_file)
    cur = con.cursor()
    grade_table_name = 'grade_' + str(grade) + '_word'
    cur.execute('SELECT word FROM ' + grade_table_name)
    words_list = list(map(lambda word: word[0], cur.fetchall()))
    con.close()
    return words_list

  def get_word(self, word_id):
    databases_directory_path = 'Databases/'; database_file = 'database_clarin.db'
    con = sqlite3.connect(databases_directory_path + database_file); cur = con.cursor()

    cur.execute('SELECT word FROM grade_1_word WHERE word_id =  ?', (word_id,))
    word = cur.fetchone()[0]
    con.close()
    return word

  def get_word_id(self, word):
    databases_directory_path = 'Databases/'; database_file = 'database_clarin.db'
    con = sqlite3.connect(databases_directory_path + database_file); cur = con.cursor()

    cur.execute('SELECT id FROM grade_1_word WHERE word = ?', (word,))
    object = cur.fetchone()
    con.close()
    if object == None:
      return -1
    else:
      return object[0]

  def get_family_id(self, word_id):
    databases_directory_path = 'Databases/'; database_file = 'database_clarin.db'
    con = sqlite3.connect(databases_directory_path + database_file); cur = con.cursor()

    cur.execute('SELECT family_id FROM grade_1_family WHERE word_id = ?', (word_id,))
    object = cur.fetchone()
    con.close()
    if object == None:
      return -1
    else:
      return object[0]

  def get_family_words(self, family_id):
    databases_directory_path = 'Databases/'; database_file = 'database_clarin.db'
    con = sqlite3.connect(databases_directory_path + database_file); cur = con.cursor()

    query = 'SELECT word FROM grade_1_word INNER JOIN grade_1_family ON grade_1_word.id = grade_1_family.word_id WHERE family_id = ?'
    cur.execute(query, (family_id,))
    family_words = list(map(lambda word: word[0], cur.fetchall()))
    con.close()
    return family_words

  def calculate_results(self):
    if len(self.words_list) > 0:
      for result in self.words_list:
        result.hide()
        result.deleteLater()

    self.words_list = []

    word = self.line_edit.text()
    word_id = self.get_word_id(word)
    family_id = self.get_family_id(word_id)
    if family_id == -1: return

    family_words = self.get_family_words(family_id)
    print(family_words)
    index = 3
    for family_word in family_words:
      new_label = QLabel(family_word)
      self.words_list.append(new_label)
      self.layout.addWidget(new_label, index, 0)
      index += 1

import sys

app = QApplication(sys.argv)

window = MainWindow()
window.showMaximized()

sys.exit(app.exec())
