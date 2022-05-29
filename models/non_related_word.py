from shared.database_handler import connect_to_database
from models.word import get_word_id

def get_non_related_words(word, grade_id):
  word_id = get_word_id(grade_id, word)
  con, cur = connect_to_database()
  query = ('SELECT word FROM word INNER JOIN non_related_word '
    'ON word.id = non_related_word.word_id_1 WHERE word_id_2 = ?')
  cur.execute(query, (word_id,))
  non_related_words_1 = \
    list(map(lambda non_related_word: non_related_word[0], cur.fetchall()))

  query = ('SELECT word FROM word INNER JOIN non_related_word '
    'ON word.id = non_related_word.word_id_2 WHERE word_id_1 = ?')
  cur.execute(query, (word_id,))
  non_related_words_2 = \
    list(map(lambda non_related_word: non_related_word[0], cur.fetchall()))

  con.close()

  return non_related_words_1 + non_related_words_2

def non_related_word_exists(word, non_related_word, grade_id):
  word_id = get_word_id(grade_id, word)
  non_related_word_id = get_word_id(grade_id, non_related_word)
  con, cur = connect_to_database()
  query = 'SELECT COUNT(*) FROM non_related_word WHERE word_id_1 = ? AND word_id_2 = ?'

  cur.execute(query, (word_id, non_related_word_id))
  non_related_word_exists_1 = cur.fetchone()[0] > 0

  cur.execute(query, (non_related_word_id, word_id))
  non_related_word_exists_2 = cur.fetchone()[0] > 0
  con.close()

  return non_related_word_exists_1 or non_related_word_exists_2

def destroy_non_related_word(word, non_related_word, grade_id):
  word_id = get_word_id(grade_id, word)
  non_related_word_id = get_word_id(grade_id, non_related_word)
  con, cur = connect_to_database()
  query = 'DELETE FROM non_related_word WHERE word_id_1 = ? AND word_id_2 = ?'

  cur.execute(query, (word_id, non_related_word_id))
  cur.execute(query, (non_related_word_id, word_id))

  con.commit()
  con.close()

def create_non_related_word(word, non_related_word, grade_id):
  word_id = get_word_id(grade_id, word)
  non_related_word_id = get_word_id(grade_id, non_related_word)
  con, cur = connect_to_database()
  query = 'INSERT INTO non_related_word VALUES (null, ?, ?)'
  cur.execute(query, (word_id, non_related_word_id))

  con.commit()
  con.close()
