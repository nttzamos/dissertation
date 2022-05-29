from models.subject import get_subject_id, get_subject_name
from shared.database_handler import connect_to_database

def create_word(word, grade_id, subject_names):
  if word_exists(grade_id, word): return

  con, cur = connect_to_database()
  cur.execute('SELECT name, id FROM subject WHERE grade_id = ?', (grade_id,))
  subject_dictionary = dict(cur.fetchall())

  subject_ids = []
  for subject in subject_names:
    subject_ids.append(subject_dictionary[subject])

  cur.execute('INSERT INTO word VALUES (null, ?, ?)', (word, grade_id))
  word_subjects = list(zip([cur.lastrowid] * len(subject_ids), subject_ids))

  query = 'INSERT INTO subject_word VALUES (null, ?, ?)'
  cur.executemany(query, word_subjects)

  con.commit()
  con.close()

def get_word_id(grade_id, word):
  con, cur = connect_to_database()
  cur.execute('SELECT id FROM word WHERE word = ? AND grade_id = ?', (word, grade_id))
  result = cur.fetchone()
  con.close()

  return -1 if result == None else result[0]

def update_word(old_word, new_word, grade_id, subjects_to_add, subjects_to_remove):
  con, cur = connect_to_database()

  word_id = get_word_id(grade_id, old_word)

  query = 'UPDATE word SET word = ? WHERE word = ? AND grade_id = ?'

  cur.execute(query, (new_word , old_word, grade_id))

  subjects_ids_to_add = []
  for subject in subjects_to_add:
    subjects_ids_to_add.append(get_subject_id(grade_id, subject))

  word_subjects = list(zip([word_id] * len(subjects_ids_to_add), subjects_ids_to_add))
  query = 'INSERT INTO subject_word VALUES (null, ?, ?)'
  cur.executemany(query, word_subjects)

  for subject in subjects_to_remove:
    subject_id = get_subject_id(grade_id, subject)

    query = ('DELETE FROM subject_word WHERE word_id = ? AND subject_id = ?')
    cur.execute(query, (word_id, subject_id))

    query = 'DELETE FROM recent_search WHERE word_id = ? AND subject_id = ?'
    cur.execute(query, (word_id, subject_id))

    query = 'DELETE FROM starred_word WHERE word_id = ? AND subject_id = ?'
    cur.execute(query, (word_id, subject_id))

  con.commit()
  con.close()

def destroy_word(word, grade_ids):
  for grade_id in grade_ids:
    con, cur = connect_to_database()

    if not word_exists(grade_id, word): continue

    word_id = get_word_id(grade_id, word)

    query = 'DELETE FROM word WHERE id = ?'
    cur.execute(query, (word_id,))

    query = 'DELETE FROM subject_word WHERE word_id = ?'
    cur.execute(query, (word_id,))

    query = 'DELETE FROM related_word WHERE word_id_1 = ? OR word_id_2 = ?'
    cur.execute(query, (word_id, word_id))

    query = 'DELETE FROM recent_search WHERE word_id = ?'
    cur.execute(query, (word_id,))

    query = 'DELETE FROM starred_word WHERE word_id = ?'
    cur.execute(query, (word_id,))

    query = 'DELETE FROM non_related_word WHERE word_id_1 = ? OR word_id_2 = ?'
    cur.execute(query, (word_id, word_id))

    con.commit()
    con.close()

def word_exists(grade_id, word):
  con, cur = connect_to_database()

  query = 'SELECT COUNT(*) FROM word WHERE word = ? AND grade_id = ?'
  cur.execute(query, (word, grade_id))

  word_exists = cur.fetchone()[0] > 0
  con.close()

  return word_exists

def get_word_subjects(grade_id, word):
  word_id = get_word_id(grade_id, word)
  con, cur = connect_to_database()

  query = (
    'SELECT subject_id FROM subject_word INNER JOIN word '
    'ON subject_word.word_id = word.id WHERE word.id = ?'
  )

  cur.execute(query, (word_id,))
  subject_ids = list(map(lambda subject_id: subject_id[0], cur.fetchall()))
  con.close()
  subject_names = []
  for subject_id in subject_ids:
    subject_names.append(get_subject_name(subject_id))

  return subject_names

def word_exists_in_subject(word_id, subject_id):
  con, cur = connect_to_database()
  query = 'SELECT COUNT(*) FROM subject_word WHERE word_id = ? AND subject_id = ?'

  cur.execute(query, (word_id, subject_id))
  word_exists_in_subject = cur.fetchone()[0] > 0
  con.close()

  return word_exists_in_subject
