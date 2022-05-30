from menu.settings import Settings
from shared.pdf_parser import PdfParser

from os import path
from os import listdir

import sqlite3
import re
import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('search', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

DATABASE_FILE_PATH = 'resources/database.db'

def initialize_database(force_init=False):
  if path.isfile(DATABASE_FILE_PATH) and not force_init:
    return

  con, cur = connect_to_database()
  grade_names = [
    "Α' Δημοτικού", "Β' Δημοτικού", "Γ' Δημοτικού", "Δ' Δημοτικού",
    "Ε' Δημοτικού", "ΣΤ' Δημοτικού"
  ]

  cur.execute('CREATE TABLE grade (id INTEGER PRIMARY KEY, name TEXT)')
  cur.execute('CREATE TABLE subject (id INTEGER PRIMARY KEY AUTOINCREMENT, '
              'name TEXT, grade_id INTEGER)')
  cur.execute('CREATE TABLE student (id INTEGER PRIMARY KEY AUTOINCREMENT, '
              'name TEXT)')
  cur.execute('CREATE TABLE profile (id INTEGER PRIMARY KEY AUTOINCREMENT, '
              'name TEXT, grade_id INTEGER)')
  cur.execute('CREATE TABLE student_profile (id INTEGER PRIMARY KEY AUTOINCREMENT, '
              'student_id INTEGER, profile_id INTEGER)')
  cur.execute('CREATE TABLE profile_subject (id INTEGER PRIMARY KEY AUTOINCREMENT, '
              'profile_id INTEGER, subject_id INTEGER)')
  cur.execute('CREATE TABLE non_related_word (id INTEGER PRIMARY KEY AUTOINCREMENT, '
              'word_id_1 INTEGER, word_id_2 INTEGER)')
  cur.execute('CREATE TABLE recent_search (id INTEGER PRIMARY KEY AUTOINCREMENT, '
              'word_id INTEGER, profile_id INTEGER, student_id INTEGER, '
              'subject_id INTEGER, searched_at TIMESTAMP)')
  cur.execute('CREATE TABLE starred_word (id INTEGER PRIMARY KEY AUTOINCREMENT, '
              'word_id INTEGER, profile_id INTEGER, student_id INTEGER, subject_id INTEGER)')
  cur.execute('CREATE TABLE word (id INTEGER PRIMARY KEY, word TEXT, grade_id INTEGER)')
  cur.execute('CREATE TABLE subject_word (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER, subject_id INTEGER)')
  cur.execute('CREATE TABLE related_word (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id_1 INTEGER, word_id_2 INTEGER)')

  for grade in range(1, 7):
    query = 'INSERT INTO grade VALUES (?, ?) ON CONFLICT(id) DO NOTHING'
    cur.execute(query, (grade, grade_names[grade - 1]))

    subject_names = PdfParser.get_grade_subjects_names(grade)
    subjects = list(zip(subject_names, [grade] * len(subject_names)))

    query = 'INSERT INTO subject VALUES (null, ?, ?) ON CONFLICT(id) DO NOTHING'
    cur.executemany(query, subjects)

    con.commit()

  from models.profile import create_default_grade_profiles
  create_default_grade_profiles()
  con.close()

def get_grades():
  con, cur = connect_to_database()
  cur.execute('SELECT name FROM grade ORDER BY id')
  grades = list(map(lambda grade: grade[0], cur.fetchall()))

  con.close()
  return grades

# TODO: Modify according to new db schema
def initialize_grade_database(grade):
  con, cur = connect_to_database()

  subject_names = PdfParser.get_grade_subjects_names(grade)

  grade_directory_path = 'processed/subjects' + str(grade) + '/'
  files_list = listdir(grade_directory_path)
  files_list.sort()
  words_set = set()
  words_per_subject = dict()
  current_subject = 0
  current_subject_words = set()

  for file in files_list:
    if file == '.DS_Store' or 'processerror' in file:
      print('error' + str(file))
      continue

    file_contents = open(grade_directory_path + file, 'r')
    file_lines = file_contents.readlines()
    for i in range(len(file_lines)):
      line = file_lines[i]
      line = line.strip()
      if line.startswith('<types:Lemma'):
        result = re.search('value="(.*)"/>', line)
        current_subject_words.add(result.group(1))
        if result.group(1) == 'YOU_HAVE_REACHED_THE_END_OF_A_SUBJECT':
          current_subject_words = list(set(PdfParser.clean_words(list(current_subject_words))))
          current_subject_words = sort_words_alphabetically(current_subject_words)
          words_per_subject[subject_names[current_subject]] = current_subject_words
          words_set = words_set | set(current_subject_words)
          current_subject += 1
          current_subject_words = set()

  words_list = sort_words_alphabetically(list(words_set))
  words = list(zip(list(range(1, len(words_list) + 1)), words_list))
  cur.executemany('INSERT INTO word VALUES (?, ?)', words)
  con.commit()
  print('Grade words for grade ' + str(grade) + ' were created.')

  for i in range(len(subject_names)):
    if not subject_names[i] in words_per_subject:
      continue

    words_list_indeces = list()
    n = len(words_per_subject[subject_names[i]])

    for j in range(n):
      words_list_indeces.append(words_list.index(words_per_subject[subject_names[i]][j]))

    from models.subject import get_subject_id
    subject_id = get_subject_id(grade, subject_names[i])
    subjects_words = list(zip([subject_id] * n, words_list_indeces))

    query = ('INSERT INTO subject_word VALUES (null, ?, ?) ON CONFLICT(id) DO NOTHING')

    cur.executemany(query, subjects_words)
    con.commit()

  con.close()
  print('Subject words for grade ' + str(grade) + ' were created.')

  try:
    from models.family import create_families
    create_families(grade)
    print('Families for grade ' + str(grade) + ' were created.')
  except Exception as e:
    print('Some exception occurred.')

def sort_words_alphabetically(words):
  translation_table = {
    940: 945, 941: 949, 972: 959, 974: 969, 943: 953, 942: 951, 973: 965
  }

  normalized_words = list(map(lambda word: word.translate(translation_table), words))

  return [word for _, word in sorted(zip(normalized_words, words))]

def get_words(profile_id, grade_id, subject_name):
  if subject_name == _('ALL_SUBJECTS_TEXT'):
    from models.profile import get_profile_subject_ids
    subject_ids = get_profile_subject_ids(profile_id)
  else:
    from models.subject import get_subject_id
    subject_ids = [get_subject_id(grade_id, subject_name)]

  con, cur = connect_to_database()

  words_set = set()
  for subject_id in subject_ids:
    query = (
      'SELECT word FROM word INNER JOIN subject_word ON word.id = subject_word.word_id ' +
      'WHERE subject_word.subject_id = ? ORDER BY word.id'
    )

    cur.execute(query, (subject_id,))
    words = list(map(lambda word: word[0], cur.fetchall()))
    words_set = words_set | set(words)

  con.close()
  words = list(words_set)
  words.sort()

  return words

def get_grade_words(grade_id):
  con, cur = connect_to_database()
  cur.execute('SELECT word FROM word WHERE grade_id = ? ORDER BY word', (grade_id,))
  words = list(map(lambda word: word[0], cur.fetchall()))

  con.close()
  return words

def get_grade_subjects(grade):
  con, cur = connect_to_database()
  cur.execute('SELECT name FROM subject WHERE grade_id = ? ORDER BY name', (grade,))
  subjects = list(map(lambda subject: subject[0], cur.fetchall()))
  con.close()
  return subjects

def connect_to_database(database_file_path=None):
  if database_file_path == None:
    database_file_path = DATABASE_FILE_PATH

  con = sqlite3.connect(database_file_path)
  cur = con.cursor()
  return con, cur
