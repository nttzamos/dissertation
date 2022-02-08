from os import path
from Common.pdfParser import PdfParser

import timeit
import sqlite3
import datetime

class DBHandler():
  databases_directory_path = 'Databases/'
  database_file = 'database.db'

  @staticmethod
  def initialize_databases():
    if path.isfile(DBHandler.databases_directory_path + DBHandler.database_file):
      return

    DBHandler.initialize_common_database()
    for grade in range(1, 7):
      DBHandler.initialize_grade_database(grade)

  @staticmethod
  def initialize_common_database():
    database_file_path = DBHandler.databases_directory_path + DBHandler.database_file

    if path.isfile(database_file_path):
      return

    con = sqlite3.connect(database_file_path)
    cur = con.cursor()
    grades_names = ["Α' Δημοτικού", "Β' Δημοτικού", "Γ' Δημοτικού", "Δ' Δημοτικού", "Ε' Δημοτικού", "ΣΤ' Δημοτικού"]

    cur.execute('''CREATE TABLE grade (id INTEGER PRIMARY KEY, name TEXT)''')
    cur.execute('''CREATE TABLE subject (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, grade_id INTEGER)''')
    cur.execute('''CREATE TABLE student (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
    cur.execute('''CREATE TABLE profile (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, grade_id INTEGER)''')
    cur.execute('''CREATE TABLE student_profile (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, profile_id INTEGER)''')
    cur.execute('''CREATE TABLE profile_subject (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, subject_id INTEGER)''')
    cur.execute('''CREATE TABLE candidate (id INTEGER PRIMARY KEY AUTOINCREMENT, grade_id INTEGER, word_id INTEGER)''')

    # Should we maybe remove profile_id?
    cur.execute('''CREATE TABLE recent_search (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER, profile_id INTEGER, student_id INTEGER, subject_id INTEGER, searched_at TIMESTAMP)''')
    cur.execute('''CREATE TABLE starred_word (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER, profile_id INTEGER, student_id INTEGER, subject_id INTEGER)''')

    for i in range(6):
      cur.execute('INSERT INTO grade VALUES (?, ?) ON CONFLICT(id) DO NOTHING', (i + 1, grades_names[i]))
    con.commit()
    con.close()

  @staticmethod
  def add_student(name, profiles):
    con, cur = DBHandler.connect_to_database()

    cur.execute('INSERT INTO student VALUES (null, ?)', (name,))
    con.commit()
    con.close()

    DBHandler.add_student_profiles(cur.lastrowid, profiles)

  @staticmethod
  def update_student_name(student_id, new_student_name):
    con, cur = DBHandler.connect_to_database()

    cur.execute('UPDATE student SET name = ? WHERE id = ?', (new_student_name, student_id))
    con.commit()
    con.close()

  @staticmethod
  def remove_student(id):
    con, cur = DBHandler.connect_to_database()

    cur.execute('DELETE FROM student WHERE id = ?', (id,))
    cur.execute('DELETE FROM student_profile WHERE student_id = ?', (id,))
    con.commit()
    con.close()

  @staticmethod
  def get_students():
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT name FROM student ORDER BY name')
    students = list(map(lambda student: student[0], cur.fetchall()))

    con.close()
    return students

  @staticmethod
  def get_student_id(student_name):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT id FROM student WHERE name = ?', (student_name,))
    student_id = cur.fetchone()[0]
    con.close()
    return student_id

  @staticmethod
  def get_student_details(student_name):
    student_id = DBHandler.get_student_id(student_name)
    return student_id, DBHandler.get_student_profiles(student_id)

  @staticmethod
  def student_name_exists(student_name):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT COUNT(*) FROM student WHERE name = ?', (student_name,))
    student_name_exists = cur.fetchone()[0] > 0
    con.close()

    return student_name_exists

  @staticmethod
  def add_student_profiles(student_id, profiles):
    con, cur = DBHandler.connect_to_database()
    for profile in profiles:
      profile_id = DBHandler.get_profile_id(profile)
      cur.execute('INSERT INTO student_profile VALUES (null, ?, ?)', (student_id, profile_id))

    con.commit()
    con.close()

  @staticmethod
  def remove_student_profiles(student_id, profiles):
    con, cur = DBHandler.connect_to_database()

    for profile in profiles:
      profile_id = DBHandler.get_profile_id(profile)
      cur.execute('DELETE FROM student_profile WHERE student_id = ? AND profile_id = ?', (student_id, profile_id))

    con.commit()
    con.close()

  @staticmethod
  def get_student_profiles(student_id):
    con, cur = DBHandler.connect_to_database()

    query = ('SELECT name '
      'FROM profile '
      'INNER JOIN student_profile '
      'ON profile.id = student_profile.profile_id '
      'WHERE student_profile.student_id = ? '
      'ORDER BY name')

    cur.execute(query, (student_id,))
    profile_names = list(map(lambda profile_name: profile_name[0], cur.fetchall()))

    con.close()

    return profile_names

  @staticmethod
  def add_profile(name, grade, subjects):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT name, id FROM subject WHERE grade_id = ?', (grade,))
    subject_dictionary = dict(cur.fetchall())
    con.close()

    subject_ids = []
    for subject in subjects:
      subject_ids.append(subject_dictionary[subject])

    con, cur = DBHandler.connect_to_database()
    cur.execute('INSERT INTO profile VALUES (null, ?, ?)', (name, grade))
    profile_subjects = list(zip([cur.lastrowid] * len(subject_ids), subject_ids))
    cur.executemany('INSERT INTO profile_subject VALUES (null, ?, ?)', profile_subjects)

    con.commit()
    con.close()

  @staticmethod
  def update_profile_name(profile_id, new_profile_name):
    con, cur = DBHandler.connect_to_database()
    cur.execute('UPDATE profile SET name = ? WHERE id = ?', (new_profile_name, profile_id))

    con.commit()
    con.close()

  @staticmethod
  def remove_profile(id):
    con, cur = DBHandler.connect_to_database()
    cur.execute('DELETE FROM profile WHERE id = ?', (id,))
    cur.execute('DELETE FROM profile_subject WHERE profile_id = ?', (id,))
    cur.execute('DELETE FROM student_profile WHERE profile_id = ?', (id,))

    con.commit()
    con.close()

  @staticmethod
  def get_profiles():
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT name FROM profile ORDER BY name')
    profiles = list(map(lambda profile: profile[0], cur.fetchall()))

    con.close()
    return profiles

  @staticmethod
  def get_profile_id(profile_name):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT id FROM profile WHERE name = ?', (profile_name,))
    profile_id = cur.fetchone()[0]
    con.close()

    return profile_id

  @staticmethod
  def get_profile_name(profile_id):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT name FROM profile WHERE id = ?', (profile_id,))
    profile_name = cur.fetchone()[0]
    con.close()

    return profile_name

  @staticmethod
  def get_profile_grade(profile_id):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT grade_id FROM profile WHERE id = ?', (profile_id,))
    profile_grade = cur.fetchone()[0]
    con.close()

    return profile_grade

  @staticmethod
  def get_profile_details(profile_name):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT id, grade_id FROM profile WHERE name = ?', (profile_name,))
    profile_id, grade_id = cur.fetchone()

    cur.execute('SELECT name FROM grade WHERE id = ?', (grade_id,))
    grade_name = cur.fetchone()[0]

    query = ('SELECT name '
      'FROM subject '
      'INNER JOIN profile_subject '
      'ON subject.id = profile_subject.subject_id '
      'WHERE profile_subject.profile_id = ? '
      'ORDER BY name')

    cur.execute(query, (profile_id,))
    profile_subjects = list(map(lambda word: word[0], cur.fetchall()))

    con.close()
    return profile_id, grade_id, grade_name, profile_subjects

  @staticmethod
  def profile_name_exists(profile_name):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT COUNT(*) FROM profile WHERE name = ?', (profile_name,))
    profile_name_exists = cur.fetchone()[0] > 0
    con.close()

    return profile_name_exists

  @staticmethod
  def add_profile_subjects(grade_id, profile_id, subjects):
    con, cur = DBHandler.connect_to_database()

    subjects_ids = []
    for subject in subjects:
      subjects_ids.append(DBHandler.get_subject_id(grade_id, subject))

    profile_subjects = list(zip([profile_id] * len(subjects_ids), subjects_ids))
    cur.executemany('INSERT INTO profile_subject VALUES (null, ?, ?)', profile_subjects)

    con.commit()
    con.close()

  @staticmethod
  def remove_profile_subjects(grade_id, profile_id, subjects):
    con, cur = DBHandler.connect_to_database()

    for subject in subjects:
      cur.execute('DELETE FROM profile_subject WHERE profile_id = ? AND subject_id = ?', (profile_id, DBHandler.get_subject_id(grade_id, subject)))

    con.commit()
    con.close()

  @staticmethod
  def get_profile_subjects(profile_id):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT subject_id FROM profile_subject WHERE profile_id = ?', (profile_id,))

    profile_subjects = list(map(lambda subject: subject[0], cur.fetchall()))

    con.close()
    return profile_subjects

  @staticmethod
  def get_grades():
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT name FROM grade ORDER BY id')
    grades = list(map(lambda grade: grade[0], cur.fetchall()))

    con.close()
    return grades

  @staticmethod
  def initialize_grade_database(grade):
    database_file_path = DBHandler.databases_directory_path + DBHandler.database_file

    grade_table_name = DBHandler.get_grade_table_name(grade)
    subject_table_name = DBHandler.get_subject_table_name(grade)

    con = sqlite3.connect(database_file_path)
    cur = con.cursor()

    cur.execute('CREATE TABLE ' + grade_table_name + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)')
    cur.execute('CREATE TABLE ' + subject_table_name + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, subject_id INTEGER, word_id INTEGER)')

    subject_names = PdfParser.get_grade_subjects_names(grade)
    DBHandler.initialize_subjects_table(cur, grade, subject_names)
    con.commit()

    # grade_start = timeit.default_timer()

    # subject_files = PdfParser.get_grade_subjects_files(grade)
    words_set = set()
    words_per_subject = dict()
    for i in range(len(subject_names)):
      # current_subject_words = list(set(PdfParser.read_subject_words(grade, subject_files[i])))
      current_subject_words = ['Νίκος1', 'Νίκος2', 'Νίκος3']
      for j in range(len(current_subject_words)):
        current_subject_words[j] = 'subject' + str(i) + str(grade) + current_subject_words[j]
      words_per_subject[subject_names[i]] = current_subject_words
      words_set = words_set | set(current_subject_words)

    words_list = DBHandler.sort_words_alphabetically(list(words_set))
    # print()
    # print('Grade: ' + str(grade))
    # grade_middle_1 = timeit.default_timer()
    # print('Creating lists: ' + str(grade_middle_1 - grade_start))

    words = list(zip(list(range(1, len(words_list) + 1)), words_list))
    cur.executemany('INSERT INTO ' + grade_table_name + ' VALUES (?, ?)', words)
    con.commit()

    # grade_middle_2 = timeit.default_timer()
    # print('Creating words table: ' + str(grade_middle_2 - grade_middle_1))

    for i in range(len(subject_names)):
      # Implementation 1
      # for j in range(len(words_per_subject[subject_names[i]])):
      #   currentWord = words_per_subject[subject_names[i]][j]
      #   words_list_index = words_list.index(currentWord)
      #   cur.execute('INSERT INTO subject_words VALUES (null, ?, ?) ON CONFLICT(id) DO NOTHING', (i + 1, words_list_index))
      # con.commit()

      # Implementation 2
      words_list_indeces = list()

      n = len(words_per_subject[subject_names[i]])

      for j in range(n):
        words_list_indeces.append(words_list.index(words_per_subject[subject_names[i]][j]))

      subject_id = DBHandler.get_subject_id(grade, subject_names[i])
      subjects_words = list(zip([subject_id] * n, words_list_indeces))
      cur.executemany('INSERT INTO ' + subject_table_name + ' VALUES (null, ?, ?) ON CONFLICT(id) DO NOTHING', subjects_words)
      con.commit()

    # grade_end = timeit.default_timer()
    # print('Creating subject_word table: ' + str(grade_end - grade_middle_2))
    # print('Total: ' + str(grade_end - grade_start))

    con.close()

  @staticmethod
  def sort_words_alphabetically(words):
    translation_table = {
      940: 945, 941: 949, 972: 959, 974: 969, 943: 953, 942: 951, 973: 965
    }

    normalized_words = list(map(lambda word: word.translate(translation_table), words))

    return [word for _, word in sorted(zip(normalized_words, words))]

  @staticmethod
  def initialize_subjects_table(cur, grade, subject_names):
    subjects = list(zip(subject_names, [grade] * len(subject_names)))

    cur.executemany('INSERT INTO subject VALUES (null, ?, ?) ON CONFLICT(id) DO NOTHING', subjects)

  @staticmethod
  def get_words(profile_id, grade_id, subject_name):
    if subject_name == 'All Subjects':
      subject_ids = DBHandler.get_profile_subjects(profile_id)
    else:
      subject_ids = [DBHandler.get_subject_id(grade_id, subject_name)]

    con, cur = DBHandler.connect_to_database()

    words_set = set()
    for subject_id in subject_ids:
      query = ('SELECT word '
        'FROM ' + DBHandler.get_grade_table_name(grade_id) + ' ' +
        'INNER JOIN ' + DBHandler.get_subject_table_name(grade_id) + ' ' +
        'ON ' + DBHandler.get_grade_table_name(grade_id) + '.id = ' + DBHandler.get_subject_table_name(grade_id) + '.word_id '
        'WHERE ' + DBHandler.get_subject_table_name(grade_id) + '.subject_id = ?')

      cur.execute(query, (subject_id,))
      subject_words = list(map(lambda word: word[0], cur.fetchall()))
      words_set = words_set | set(subject_words)

    con.close()
    words = list(words_set)
    words.sort()

    return words

  @staticmethod
  def get_grade_words(grade_id):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT word FROM ' + DBHandler.get_grade_table_name(grade_id) + ' ORDER BY word')
    words = list(map(lambda word: word[0], cur.fetchall()))

    con.close()
    return words

  @staticmethod
  def get_candidate_words(grade_id):
    con, cur = DBHandler.connect_to_database()
    query = ('SELECT word '
      'FROM ' + DBHandler.get_grade_table_name(grade_id) + ' ' +
      'INNER JOIN candidate '
      'ON ' + DBHandler.get_grade_table_name(grade_id) + '.id = candidate.word_id '
      'WHERE candidate.grade_id = ?')

    cur.execute(query, (grade_id,))
    words = list(map(lambda word: word[0], cur.fetchall()))

    con.close()
    return words

  @staticmethod
  def add_recent_search(word):
    from MainWidget.currentSearch import CurrentSearch
    student_id, profile_id, grade, subject_name = CurrentSearch.get_current_selection_details()
    if subject_name == 'All Subjects':
      return

    subject_id = DBHandler.get_subject_id(grade, subject_name)

    word_id = DBHandler.get_word_id(grade, word)
    recent_search_exists = DBHandler.recent_search_exists(word_id, profile_id, student_id, subject_id)
    date_time_now = datetime.datetime.now()
    con, cur = DBHandler.connect_to_database()

    if recent_search_exists:
      query = ('UPDATE recent_search SET searched_at = ? '
        'WHERE word_id = ? AND profile_id = ? '
        'AND student_id = ? AND subject_id = ?')
      cur.execute(query, (date_time_now, word_id, profile_id, student_id, subject_id))
    else:
      values = (word_id, profile_id, student_id, subject_id, date_time_now)
      cur.execute('INSERT INTO recent_search VALUES (null, ?, ?, ?, ?, ?)', values)

    con.commit()
    con.close()
    return recent_search_exists

  @staticmethod
  def recent_search_exists(word_id, profile_id, student_id, subject_id):
    con, cur = DBHandler.connect_to_database()
    query = ('SELECT COUNT(*) FROM recent_search WHERE word_id = ? '
      'AND profile_id = ? AND student_id = ? AND subject_id = ?')
    cur.execute(query, (word_id, profile_id, student_id, subject_id))
    recent_search_exists = cur.fetchone()[0] > 0
    con.close()
    return recent_search_exists

  @staticmethod
  def remove_recent_search(word):
    from MainWidget.currentSearch import CurrentSearch
    student_id, profile_id, grade, subject_name = CurrentSearch.get_current_selection_details()

    subject_id = DBHandler.get_subject_id(grade, subject_name)
    word_id = DBHandler.get_word_id(grade, word)
    con, cur = DBHandler.connect_to_database()

    query = ('DELETE FROM recent_search WHERE word_id = ? '
      'AND profile_id = ? AND student_id = ? AND subject_id = ?')
    cur.execute(query, (word_id, profile_id, student_id, subject_id))
    con.commit()
    con.close()

  @staticmethod
  def get_recent_searches():
    from MainWidget.currentSearch import CurrentSearch
    student_id, profile_id, grade, subject_name = CurrentSearch.get_current_selection_details()
    if subject_name == 'All Subjects':
      values = (profile_id, student_id)
      query = ('SELECT word '
        'FROM ' + DBHandler.get_grade_table_name(grade) + ' ' +
        'INNER JOIN recent_search '
        'ON ' + DBHandler.get_grade_table_name(grade) + '.id = recent_search.word_id '
        'WHERE recent_search.profile_id = ? '
        'AND recent_search.student_id = ? '
        'ORDER BY recent_search.searched_at')
    else:
      values = (DBHandler.get_subject_id(grade, subject_name), profile_id, student_id)
      query = ('SELECT word '
        'FROM ' + DBHandler.get_grade_table_name(grade) + ' ' +
        'INNER JOIN recent_search '
        'ON ' + DBHandler.get_grade_table_name(grade) + '.id = recent_search.word_id '
        'WHERE recent_search.subject_id = ? '
        'AND recent_search.profile_id = ? '
        'AND recent_search.student_id = ? '
        'ORDER BY recent_search.searched_at')

    con, cur = DBHandler.connect_to_database()

    cur.execute(query, values)
    recent_searches = list(map(lambda recent_search: recent_search[0], cur.fetchall()))
    con.close()
    return recent_searches

  @staticmethod
  def add_starred_word(word):
    from MainWidget.currentSearch import CurrentSearch
    student_id, profile_id, grade, subject_name = CurrentSearch.get_current_selection_details()
    if subject_name == 'All Subjects':
      return

    subject_id = DBHandler.get_subject_id(grade, subject_name)
    word_id = DBHandler.get_word_id(grade, word)
    con, cur = DBHandler.connect_to_database()

    values = (word_id, profile_id, student_id, subject_id)
    cur.execute('INSERT INTO starred_word VALUES (null, ?, ?, ?, ?)', values)
    con.commit()
    con.close()

  @staticmethod
  def starred_word_exists(word):
    from MainWidget.currentSearch import CurrentSearch
    student_id, profile_id, grade, subject_name = CurrentSearch.get_current_selection_details()

    subject_id = DBHandler.get_subject_id(grade, subject_name)
    word_id = DBHandler.get_word_id(grade, word)
    con, cur = DBHandler.connect_to_database()

    query = ('SELECT COUNT(*) FROM starred_word WHERE word_id = ? '
      'AND profile_id = ? AND student_id = ? AND subject_id = ?')
    cur.execute(query, (word_id, profile_id, student_id, subject_id))
    starred_word_exists = cur.fetchone()[0] > 0
    con.close()
    return starred_word_exists

  @staticmethod
  def remove_starred_word(word):
    from MainWidget.currentSearch import CurrentSearch
    student_id, profile_id, grade, subject_name = CurrentSearch.get_current_selection_details()

    subject_id = DBHandler.get_subject_id(grade, subject_name)
    word_id = DBHandler.get_word_id(grade, word)
    con, cur = DBHandler.connect_to_database()

    query = ('DELETE FROM starred_word WHERE word_id = ? '
      'AND profile_id = ? AND student_id = ? AND subject_id = ?')
    cur.execute(query, (word_id, profile_id, student_id, subject_id))
    con.commit()
    con.close()

  @staticmethod
  def get_starred_words():
    from MainWidget.currentSearch import CurrentSearch
    student_id, profile_id, grade, subject_name = CurrentSearch.get_current_selection_details()

    con, cur = DBHandler.connect_to_database()

    if subject_name == 'All Subjects':
      values = (profile_id, student_id)
      query = ('SELECT word '
        'FROM ' + DBHandler.get_grade_table_name(grade) + ' ' +
        'INNER JOIN starred_word '
        'ON ' + DBHandler.get_grade_table_name(grade) + '.id = starred_word.word_id '
        'WHERE starred_word.profile_id = ? '
        'AND starred_word.student_id = ? '
        'ORDER BY ' + DBHandler.get_grade_table_name(grade) + '.id DESC')
    else:
      values = (DBHandler.get_subject_id(grade, subject_name), profile_id, student_id)
      query = ('SELECT word '
        'FROM ' + DBHandler.get_grade_table_name(grade) + ' ' +
        'INNER JOIN starred_word '
        'ON ' + DBHandler.get_grade_table_name(grade) + '.id = starred_word.word_id '
        'WHERE starred_word.subject_id = ? '
        'AND starred_word.profile_id = ? '
        'AND starred_word.student_id = ? '
        'ORDER BY ' + DBHandler.get_grade_table_name(grade) + '.id DESC')

    cur.execute(query, values)
    starred_words = list(map(lambda starredWord: starredWord[0], cur.fetchall()))
    con.close()
    return starred_words

  @staticmethod
  def get_subject_id(grade, subject):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT id FROM subject WHERE grade_id = ? AND name = ?', (grade, subject))
    subject_id = cur.fetchone()[0]
    cur.close()
    con.close()
    return subject_id

  @staticmethod
  def get_subject_name(subject_id):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT name FROM subject WHERE id = ?', (subject_id,))
    subject_name = cur.fetchone()[0]
    cur.close()
    con.close()
    return subject_name

  @staticmethod
  def get_word_id(grade, word):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT id FROM ' + DBHandler.get_grade_table_name(grade) + ' WHERE word = ?', (word,))
    word_id = cur.fetchone()[0]
    cur.close()
    con.close()
    return word_id

  @staticmethod
  def update_word(old_word, new_word, grades):
    for grade in grades:
      con, cur = DBHandler.connect_to_database()

      if DBHandler.word_exists(cur, grade, new_word):
        DBHandler.remove_word_from_grade(cur, old_word)
      else:
        cur.execute('UPDATE ' + DBHandler.get_grade_table_name(grade) + ' SET word = ? WHERE word = ?', (new_word , old_word))

      con.commit()
      con.close()

  @staticmethod
  def delete_word(word, grades):
    for grade in grades:
      con, cur = DBHandler.connect_to_database()

      DBHandler.remove_word_from_grade(cur, grade, word)

      con.commit()
      con.close()

  @staticmethod
  def remove_word_from_grade(cur, grade, word):
    if not DBHandler.word_exists(cur, grade, word): return

    word_id = DBHandler.get_word_id(cur, word)
    cur.execute('DELETE FROM ' + DBHandler.get_grade_table_name(grade) + ' WHERE id = ?', (word_id,))
    cur.execute('DELETE FROM subject_word WHERE word_id = ?', (word_id,))
    cur.execute('DELETE FROM recent_search WHERE word_id = ?', (word_id,))
    cur.execute('DELETE FROM starred_word WHERE word_id = ?', (word_id,))

  @staticmethod
  def word_exists(cur, grade, word):
    cur.execute('SELECT COUNT(*) FROM ' + DBHandler.get_grade_table_name(grade) + ' WHERE word = ?', (word,))
    return cur.fetchone()[0] > 0

  @staticmethod
  def get_grade_subjects(grade):
    con, cur = DBHandler.connect_to_database()
    cur.execute('SELECT name FROM subject WHERE grade_id = ? ORDER BY name', (grade,))
    subjects = list(map(lambda subject: subject[0], cur.fetchall()))
    con.close()
    return subjects

  @staticmethod
  def get_grade_table_name(grade):
    return 'grade_' + str(grade) + '_word'

  @staticmethod
  def get_subject_table_name(grade):
    return 'subject_' + str(grade) + '_word'

  @staticmethod
  def connect_to_database():
    con = sqlite3.connect(DBHandler.databases_directory_path + DBHandler.database_file)
    cur = con.cursor()
    return con, cur
