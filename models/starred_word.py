from menu.settings import Settings
from models.profile import get_profile_subject_ids
from models.subject import get_subject_id
from models.word import get_word_id, word_exists_in_subject
from shared.database_handler import connect_to_database

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('search', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

def create_starred_word(word):
  from search.current_search import CurrentSearch
  student_id, profile_id, grade_id, subject_name = \
    CurrentSearch.get_current_selection_details()

  if subject_name == _('ALL_SUBJECTS_TEXT'):
    subject_ids = get_profile_subject_ids(profile_id)
  else:
    subject_ids = [get_subject_id(grade_id, subject_name)]

  word_id = get_word_id(grade_id, word)
  con, cur = connect_to_database()

  for subject_id in subject_ids:
    if word_exists_in_subject(word_id, subject_id):
      values = (word_id, profile_id, student_id, subject_id)
      query = 'INSERT INTO starred_word VALUES (null, ?, ?, ?, ?)'

      cur.execute(query, values)

  con.commit()
  con.close()

def starred_word_exists(word):
  from search.current_search import CurrentSearch
  student_id, profile_id, grade_id, subject_name = \
    CurrentSearch.get_current_selection_details()

  if subject_name == _('ALL_SUBJECTS_TEXT'):
    subject_ids = get_profile_subject_ids(profile_id)
  else:
    subject_ids = [get_subject_id(grade_id, subject_name)]

  con, cur = connect_to_database()
  word_id = get_word_id(grade_id, word)

  for subject_id in subject_ids:
    if word_exists_in_subject(word_id, subject_id):
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
  student_id, profile_id, grade_id, subject_name = \
    CurrentSearch.get_current_selection_details()

  if subject_name == _('ALL_SUBJECTS_TEXT'):
    subject_ids = get_profile_subject_ids(profile_id)
  else:
    subject_ids = [get_subject_id(grade_id, subject_name)]

  word_id = get_word_id(grade_id, word)
  con, cur = connect_to_database()
  for subject_id in subject_ids:
    if word_exists_in_subject(word_id, subject_id):
      query = ('DELETE FROM starred_word WHERE word_id = ? '
               'AND profile_id = ? AND student_id = ? AND subject_id = ?')

      cur.execute(query, (word_id, profile_id, student_id, subject_id))

  con.commit()
  con.close()

def get_starred_words():
  from search.current_search import CurrentSearch
  student_id, profile_id, grade_id, subject_name = \
    CurrentSearch.get_current_selection_details()

  con, cur = connect_to_database()

  if subject_name == _('ALL_SUBJECTS_TEXT'):
    values = (profile_id, student_id)
    query = ('SELECT DISTINCT word FROM word INNER JOIN starred_word '
             'ON word.id = starred_word.word_id '
             'WHERE starred_word.profile_id = ? AND starred_word.student_id = ? '
             'ORDER BY word.id DESC')
  else:
    values = (get_subject_id(grade_id, subject_name), profile_id, student_id)
    query = ('SELECT word FROM word INNER JOIN starred_word '
             'ON word.id = starred_word.word_id '
             'WHERE starred_word.subject_id = ? AND starred_word.profile_id = ? '
             'AND starred_word.student_id = ? ORDER BY word.id DESC')

  cur.execute(query, values)
  starred_words = list(map(lambda starredWord: starredWord[0], cur.fetchall()))
  con.close()

  return starred_words
