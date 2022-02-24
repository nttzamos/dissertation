from models.profile import get_profile_subject_ids
from models.subject import get_subject_id
from models.word import get_word_id, word_exists_in_subject
from shared.database_handler import connect_to_database, get_grade_table_name

def create_starred_word(word):
  from search.current_search import CurrentSearch
  student_id, profile_id, grade_id, subject_name = CurrentSearch.get_current_selection_details()
  if subject_name == 'All Subjects':
    subject_ids = get_profile_subject_ids(profile_id)
  else:
    subject_ids = [get_subject_id(grade_id, subject_name)]

  word_id = get_word_id(grade_id, word)
  con, cur = connect_to_database()

  for subject_id in subject_ids:
    if word_exists_in_subject(word_id, subject_id, grade_id):
      values = (word_id, profile_id, student_id, subject_id)
      cur.execute('INSERT INTO starred_word VALUES (null, ?, ?, ?, ?)', values)
  con.commit()
  con.close()

def starred_word_exists(word):
  from search.current_search import CurrentSearch
  student_id, profile_id, grade_id, subject_name = CurrentSearch.get_current_selection_details()
  if subject_name == 'All Subjects':
    subject_ids = get_profile_subject_ids(profile_id)
  else:
    subject_ids = [get_subject_id(grade_id, subject_name)]

  con, cur = connect_to_database()
  word_id = get_word_id(grade_id, word)

  for subject_id in subject_ids:
    if word_exists_in_subject(word_id, subject_id, grade_id):
      query = ('SELECT COUNT(*) FROM starred_word WHERE word_id = ? '
        'AND profile_id = ? AND student_id = ? AND subject_id = ?')
      cur.execute(query, (word_id, profile_id, student_id, subject_id))
      if cur.fetchone()[0] > 0:
        con.close()
        return True

  con.close()
  return False

def destroy_starred_word(word):
  from search.current_search import CurrentSearch
  student_id, profile_id, grade_id, subject_name = CurrentSearch.get_current_selection_details()
  if subject_name == 'All Subjects':
    subject_ids = get_profile_subject_ids(profile_id)
  else:
    subject_ids = [get_subject_id(grade_id, subject_name)]

  word_id = get_word_id(grade_id, word)
  con, cur = connect_to_database()
  for subject_id in subject_ids:
    if word_exists_in_subject(word_id, subject_id, grade_id):
      query = ('DELETE FROM starred_word WHERE word_id = ? '
        'AND profile_id = ? AND student_id = ? AND subject_id = ?')
      cur.execute(query, (word_id, profile_id, student_id, subject_id))

  con.commit()
  con.close()

def get_starred_words():
  from search.current_search import CurrentSearch
  student_id, profile_id, grade_id, subject_name = CurrentSearch.get_current_selection_details()

  con, cur = connect_to_database()

  grade_table_name = get_grade_table_name(grade_id)
  if subject_name == 'All Subjects':
    values = (profile_id, student_id)
    query = ('SELECT DISTINCT word '
      'FROM ' + grade_table_name + ' ' +
      'INNER JOIN starred_word '
      'ON ' + grade_table_name + '.id = starred_word.word_id '
      'WHERE starred_word.profile_id = ? '
      'AND starred_word.student_id = ? '
      'ORDER BY ' + grade_table_name + '.id DESC')
  else:
    values = (get_subject_id(grade_id, subject_name), profile_id, student_id)
    query = ('SELECT word '
      'FROM ' + grade_table_name + ' ' +
      'INNER JOIN starred_word '
      'ON ' + grade_table_name + '.id = starred_word.word_id '
      'WHERE starred_word.subject_id = ? '
      'AND starred_word.profile_id = ? '
      'AND starred_word.student_id = ? '
      'ORDER BY ' + grade_table_name + '.id DESC')

  cur.execute(query, values)
  starred_words = list(map(lambda starredWord: starredWord[0], cur.fetchall()))
  con.close()
  return starred_words
