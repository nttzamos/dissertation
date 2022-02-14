import timeit

from Common.wiktionary_parser import fetch_word_details
from Common.database_handler import connect_to_database, get_family_table_name, get_grade_words, get_subject_table_name, get_grade_table_name
from models.profile import get_profile_subject_ids
from models.subject import get_subject_id
from models.word import get_word_id

def create_families(grade):
  con, cur = connect_to_database()
  family_table_name = get_family_table_name(grade)
  words_list = get_grade_words(grade)
  family_counter = 0

  grade_start = timeit.default_timer()
  print(len(words_list))
  for i in range(len(words_list)):
    if i % 100 == 0 and i > 0:
      print(timeit.default_timer() - grade_start)

    family_words, is_candidate = fetch_word_details(words_list[i])

    current_word_id = get_word_id(grade, words_list[i])
    if is_candidate:
      cur.execute('INSERT INTO candidate VALUES (null, ?, ?)', (grade, current_word_id))
      continue

    words_in_dict = []
    for word in family_words:
      word_id = get_word_id(grade, word)
      if word_id != -1:
        words_in_dict.append(word_id)

    if len(words_in_dict) == 0: continue

    family_counter += 1
    cur.execute('INSERT INTO ' + family_table_name + ' VALUES (null, ?, ?)', (current_word_id, family_counter))
    for word_id in words_in_dict:
      cur.execute('INSERT INTO ' + family_table_name + ' VALUES (null, ?, ?)', (word_id, family_counter))

    con.commit()

def create_family(grade_id, word_id):
  con, cur = connect_to_database()
  query = 'INSERT INTO ' + get_family_table_name(grade_id) + ' VALUES (null, ?, ?)'
  new_family_id = get_last_family_id(grade_id) + 1
  cur.execute(query, (word_id, new_family_id))

  con.commit()
  con.close()

  return new_family_id

def get_family_id(grade, word_id):
  con, cur = connect_to_database()
  family_table_name = get_family_table_name(grade)

  query = 'SELECT family_id FROM ' + family_table_name + ' WHERE word_id = ?'
  cur.execute(query, (word_id,))
  object = cur.fetchone()
  con.close()
  if object == None:
    return -1
  else:
    return object[0]

def get_last_family_id(grade_id):
  con, cur = connect_to_database()
  family_table_name = get_family_table_name(grade_id)
  cur.execute(('SELECT MAX(family_id) FROM ' + family_table_name))
  last_family_id = cur.fetchone()[0]
  con.close()
  return last_family_id

def get_family_words(grade, family_id):
  con, cur = connect_to_database()
  grade_table_name = get_grade_table_name(grade)
  family_table_name = get_family_table_name(grade)

  query = ('SELECT word FROM ' + grade_table_name + ' '
    'INNER JOIN ' + family_table_name + ' ON ' + grade_table_name + '.id = '
    '' + family_table_name + '.word_id WHERE family_id = ?')

  cur.execute(query, (family_id,))
  family_words = list(map(lambda word: word[0], cur.fetchall()))
  con.close()
  return family_words

def get_words_with_family(profile_id, grade_id, subject_name):
  if subject_name == 'All Subjects':
    subject_ids = get_profile_subject_ids(profile_id)
  else:
    subject_ids = [get_subject_id(grade_id, subject_name)]

  con, cur = connect_to_database()

  words_set = set()
  for subject_id in subject_ids:
    grade_table_name = get_grade_table_name(grade_id)
    subject_table_name = get_subject_table_name(grade_id)
    family_table_name = get_family_table_name(grade_id)
    query = ('SELECT word '
      'FROM ' + grade_table_name + ' INNER JOIN ' + subject_table_name + ' '
      'ON ' + grade_table_name + '.id = ' + subject_table_name + '.word_id '
      'INNER JOIN ' + family_table_name + ' '
      'ON ' + subject_table_name + '.word_id = ' + family_table_name + '.word_id '
      'WHERE ' + subject_table_name + '.subject_id = ?')

    cur.execute(query, (subject_id,))
    subject_words = list(map(lambda word: word[0], cur.fetchall()))
    words_set = words_set | set(subject_words)

  con.close()
  words = list(words_set)
  words.sort()

  return words

def update_word_family(grade_id, word, words_to_add, words_to_remove):
  con, cur = connect_to_database()

  word_id = get_word_id(grade_id, word)
  family_id = get_family_id(grade_id, word_id)

  if family_id == -1:
    if len(words_to_add) == 0: return
    family_id = create_family(grade_id, word_id)

  words_ids_to_add = []
  for family_word in words_to_add:
    words_ids_to_add.append(get_word_id(grade_id, family_word))

  family_words = list(zip(words_ids_to_add, [family_id] * len(words_ids_to_add)))
  query = 'INSERT INTO ' + get_family_table_name(grade_id) + ' VALUES (null, ?, ?)'
  cur.executemany(query, family_words)

  for family_word in words_to_remove:
    query = 'DELETE FROM ' + get_family_table_name(grade_id) + ' WHERE word_id = ? AND family_id = ?'
    cur.execute(query, (get_word_id(grade_id, family_word), family_id))

  con.commit()
  con.close()
