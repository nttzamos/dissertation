from models.subject import get_subject_id, get_subject_name
from shared.database_handler import connect_to_database, get_grade_table_name, get_subject_table_name, get_family_table_name

def create_word(word, grade_id, subject_names):
  if word_exists(grade_id, word):
    return

  con, cur = connect_to_database()
  cur.execute('SELECT name, id FROM subject WHERE grade_id = ?', (grade_id,))
  subject_dictionary = dict(cur.fetchall())

  subject_ids = []
  for subject in subject_names:
    subject_ids.append(subject_dictionary[subject])

  cur.execute('INSERT INTO ' + get_grade_table_name(grade_id) + ' VALUES (null, ?)', (word,))
  word_subjects = list(zip(subject_ids, [cur.lastrowid] * len(subject_ids)))
  cur.executemany('INSERT INTO ' + get_subject_table_name(grade_id) + ' VALUES (null, ?, ?)', word_subjects)

  con.commit()
  con.close()

def get_word_id(grade, word):
  con, cur = connect_to_database()
  cur.execute('SELECT id FROM ' + get_grade_table_name(grade) + ' WHERE word = ?', (word,))
  result = cur.fetchone()
  con.close()

  return -1 if result == None else result[0]

def update_word(old_word, new_word, grade_id, subjects_to_add, subjects_to_remove):
  con, cur = connect_to_database()

  word_id = get_word_id(grade_id, old_word)
  cur.execute('UPDATE ' + get_grade_table_name(grade_id) + ' SET word = ? WHERE word = ?', (new_word , old_word))
  cur.execute('DELETE FROM candidate WHERE word_id = ?', (word_id,))

  subjects_ids_to_add = []
  for subject in subjects_to_add:
    subjects_ids_to_add.append(get_subject_id(grade_id, subject))

  word_subjects = list(zip(subjects_ids_to_add, [word_id] * len(subjects_ids_to_add)))
  query = 'INSERT INTO ' + get_subject_table_name(grade_id) + ' VALUES (null, ?, ?)'
  cur.executemany(query, word_subjects)

  for subject in subjects_to_remove:
    subject_id = get_subject_id(grade_id, subject)

    query = 'DELETE FROM ' + get_subject_table_name(grade_id) + ' WHERE word_id = ? AND subject_id = ?'
    cur.execute(query, (word_id, subject_id))

    query = 'DELETE FROM recent_search WHERE word_id = ? AND subject_id = ?'
    cur.execute(query, (word_id, subject_id))

    query = 'DELETE FROM starred_word WHERE word_id = ? AND subject_id = ?'
    cur.execute(query, (word_id, subject_id))

  con.commit()
  con.close()

def destroy_word(word, grades):
  for grade in grades:
    con, cur = connect_to_database()

    if not word_exists(grade, word): continue

    word_id = get_word_id(grade, word)
    cur.execute('DELETE FROM ' + get_grade_table_name(grade) + ' WHERE id = ?', (word_id,))
    cur.execute('DELETE FROM ' + get_subject_table_name(grade) + ' WHERE word_id = ?', (word_id,))
    cur.execute('DELETE FROM ' + get_family_table_name(grade) + ' WHERE word_id = ?', (word_id,))
    cur.execute('DELETE FROM candidate WHERE word_id = ?', (word_id,))
    cur.execute('DELETE FROM recent_search WHERE word_id = ?', (word_id,))
    cur.execute('DELETE FROM starred_word WHERE word_id = ?', (word_id,))

    con.commit()
    con.close()

def word_exists(grade_id, word):
  con, cur = connect_to_database()
  cur.execute('SELECT COUNT(*) FROM ' + get_grade_table_name(grade_id) + ' WHERE word = ?', (word,))
  word_exists = cur.fetchone()[0] > 0
  con.close()
  return word_exists

def get_word_subjects(grade_id, word):
  word_id = get_word_id(grade_id, word)
  con, cur = connect_to_database()

  subject_table_name = get_subject_table_name(grade_id)
  grade_table_name = get_grade_table_name(grade_id)
  query = ('SELECT subject_id '
    'FROM ' + subject_table_name + ' '
    'INNER JOIN ' + grade_table_name + ' '
    'ON ' + subject_table_name + '.word_id = ' + grade_table_name + '.id '
    'WHERE ' + grade_table_name + '.id = ?')

  cur.execute(query, (word_id,))
  subject_ids = list(map(lambda subject_id: subject_id[0], cur.fetchall()))
  con.close()
  subject_names = []
  for subject_id in subject_ids:
    subject_names.append(get_subject_name(subject_id))

  return subject_names

def word_exists_in_subject(word_id, subject_id, grade_id):
  con, cur = connect_to_database()
  query = ('SELECT COUNT(*) FROM '
    '' + get_subject_table_name(grade_id) + ' '
    'WHERE word_id = ? AND subject_id = ?')
  cur.execute(query, (word_id, subject_id))
  word_exists_in_subject = cur.fetchone()[0] > 0
  con.close()
  return word_exists_in_subject
