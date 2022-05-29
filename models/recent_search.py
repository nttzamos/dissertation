from menu.settings import Settings
from models.profile import get_profile_subject_ids
from models.subject import get_subject_id
from models.word import get_word_id, word_exists_in_subject
from shared.database_handler import connect_to_database

import datetime
import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('search', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

def create_recent_search(word):
  from search.current_search import CurrentSearch
  student_id, profile_id, grade_id, subject_name = \
    CurrentSearch.get_current_selection_details()

  if subject_name == _('ALL_SUBJECTS_TEXT'):
    subject_ids = get_profile_subject_ids(profile_id)
  else:
    subject_ids = [get_subject_id(grade_id, subject_name)]

  word_id = get_word_id(grade_id, word)
  con, cur = connect_to_database()

  recent_search_exists = False
  for subject_id in subject_ids:
    if word_exists_in_subject(word_id, subject_id):
      query = ('SELECT COUNT(*) FROM recent_search WHERE word_id = ? '
               'AND profile_id = ? AND student_id = ? AND subject_id = ?')

      cur.execute(query, (word_id, profile_id, student_id, subject_id))
      recent_search_exists_in_subject = cur.fetchone()[0] > 0

      date_time_now = datetime.datetime.now()

      if recent_search_exists_in_subject:
        recent_search_exists = True
        values = (word_id, profile_id, student_id, subject_id)
        query = ('UPDATE recent_search SET searched_at = ? '
                 'WHERE word_id = ? AND profile_id = ? '
                 'AND student_id = ? AND subject_id = ?')

        cur.execute(query, (date_time_now, word_id, profile_id, student_id, subject_id))
      else:
        values = (word_id, profile_id, student_id, subject_id, date_time_now)
        query = 'INSERT INTO recent_search VALUES (null, ?, ?, ?, ?, ?)'

        cur.execute(query, values)

  con.commit()
  con.close()

  return recent_search_exists

def destroy_recent_search(word):
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
      query = ('DELETE FROM recent_search WHERE word_id = ? '
               'AND profile_id = ? AND student_id = ? AND subject_id = ?')

      cur.execute(query, (word_id, profile_id, student_id, subject_id))

  con.commit()
  con.close()

def get_recent_searches():
  from search.current_search import CurrentSearch
  student_id, profile_id, grade, subject_name = \
    CurrentSearch.get_current_selection_details()

  if subject_name == _('ALL_SUBJECTS_TEXT'):
    values = (profile_id, student_id)
    query = ('SELECT DISTINCT word '
             'FROM word INNER JOIN recent_search '
             'ON word.id = recent_search.word_id '
             'WHERE recent_search.profile_id = ? '
             'AND recent_search.student_id = ? '
             'ORDER BY recent_search.searched_at')
  else:
    values = (get_subject_id(grade, subject_name), profile_id, student_id)
    query = ('SELECT word '
             'FROM word INNER JOIN recent_search '
             'ON word.id = recent_search.word_id '
             'WHERE recent_search.subject_id = ? '
             'AND recent_search.profile_id = ? '
             'AND recent_search.student_id = ? '
             'ORDER BY recent_search.searched_at')

  con, cur = connect_to_database()

  cur.execute(query, values)
  recent_searches = list(map(lambda recent_search: recent_search[0], cur.fetchall()))
  con.close()

  return recent_searches
