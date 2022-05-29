import sqlite3

from shared.database_handler import get_grade_words_old, get_words_old, connect_to_database
from models.subject import get_subject_name
from models.family import get_family_ids, get_family_word_ids
import itertools
import os
from os import path

DATABASE_FILE_PATH = 'resources/database.db'

def get_subject_ids(grade_id):
  con, cur = connect_to_database()
  query = 'SELECT id FROM subject WHERE grade_id = ?'
  cur.execute(query, (grade_id, ))
  subject_ids = list(map(lambda subject: subject[0], cur.fetchall()))
  con.close()

  return subject_ids

# Remove previous database migration file
if path.isfile(DATABASE_FILE_PATH):
  os.remove(DATABASE_FILE_PATH)

con, cur = connect_to_database()

# Create other tables
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

for grade in range(1, 7):
  query = 'INSERT INTO grade VALUES (?, ?) ON CONFLICT(id) DO NOTHING'
  cur.execute(query, (grade, grade_names[grade - 1]))

con_old, cur_old = connect_to_database('resources/database_old.db')
cur_old.execute('SELECT name, grade_id FROM subject')
data = cur_old.fetchall()
names = list(map(lambda subject: subject[0], data))
grade_ids = list(map(lambda subject: subject[1], data))
subjects_details = list(zip(names, grade_ids))

query = 'INSERT INTO subject VALUES (null, ?, ?)'
cur.executemany(query, subjects_details)
con.commit()

from models.profile import create_default_grade_profiles
create_default_grade_profiles()

con.commit()

# Words per grade

word_ids_offset = [0, 6307, 14086, 26910, 41630, 62763, 82631]

cur.execute('CREATE TABLE word (id INTEGER PRIMARY KEY, word TEXT, grade_id INTEGER)')

for grade_id in range(1, 7):
  grade_ids, grade_words = get_grade_words_old(grade_id, True)
  grade_ids = list(map(lambda x: x + word_ids_offset[grade_id - 1], grade_ids))

  grade_words_details = list(zip(grade_ids, grade_words, [grade_id] * len(grade_words)))
  cur.executemany('INSERT INTO word VALUES (?, ?, ?)', grade_words_details)
  con.commit()

# Words per subject
cur.execute('CREATE TABLE subject_word (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER, subject_id INTEGER)')

for grade_id in range(1, 7):
  subject_ids = get_subject_ids(grade_id)

  for subject_id in subject_ids:
    subject_name = get_subject_name(subject_id)
    subject_words_ids = get_words_old(-1, grade_id, subject_name, True)

    subject_words_ids = list(map(lambda x: x + word_ids_offset[grade_id - 1], subject_words_ids))

    subject_words_details = list(zip(subject_words_ids, [subject_id] * len(subject_words_ids)))

    cur.executemany('INSERT INTO subject_word VALUES (null, ?, ?)', subject_words_details)
    con.commit()

# Related words
cur.execute('CREATE TABLE related_word (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id_1 INTEGER, word_id_2 INTEGER)')

for grade_id in range(1, 7):
  family_ids = get_family_ids(grade_id)

  for family_id in family_ids:
    family_word_ids = get_family_word_ids(grade_id, family_id)
    family_word_ids = list(map(lambda x: x + word_ids_offset[grade_id - 1], family_word_ids))
    print(family_word_ids)
    word_ids_combinations = list(itertools.combinations(family_word_ids, 2))

    for combination in word_ids_combinations:
      cur.execute('INSERT INTO related_word VALUES (null, ?, ?)', (combination[0], combination[1]))

    con.commit()

# Close database connection
con.close()
