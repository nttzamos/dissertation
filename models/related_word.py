from shared.database_handler import connect_to_database, get_grade_words
from shared.wiktionary_parser import fetch_online_results
from models.word import get_word_id
from models.non_related_word import (non_related_word_exists, destroy_non_related_word,
                                     create_non_related_word)

import timeit

def get_related_words(grade_id, word_id):
  con, cur = connect_to_database()

  query = (
    'SELECT word.word FROM word INNER JOIN related_word ' +
    'ON word.id = related_word.word_id_1 ' +
    'WHERE related_word.word_id_2 = ? AND word.grade_id = ?'
  )

  cur.execute(query, (word_id, grade_id))
  related_words_1 = list(map(lambda word: word[0], cur.fetchall()))

  query = (
    'SELECT word.word FROM word INNER JOIN related_word ' +
    'ON word.id = related_word.word_id_2 ' +
    'WHERE related_word.word_id_1 = ? AND word.grade_id = ?'
  )

  cur.execute(query, (word_id, grade_id))
  related_words_2 = list(map(lambda word: word[0], cur.fetchall()))

  con.close()

  return list(set(related_words_1) | set(related_words_2))

def update_related_words(grade_id, word, words_to_add, words_to_remove):
  con, cur = connect_to_database()
  word_id = get_word_id(grade_id, word)

  words_ids_to_add = []
  for related_word in words_to_add:
    words_ids_to_add.append(get_word_id(grade_id, related_word))

    if non_related_word_exists(word, related_word, grade_id):
      destroy_non_related_word(word, related_word, grade_id)

  related_words = list(zip([word_id] * len(words_ids_to_add), words_ids_to_add))
  query = 'INSERT INTO related_word VALUES (null, ?, ?)'
  cur.executemany(query, related_words)
  con.commit()

  for non_related_word in words_to_remove:
    non_related_word_id = get_word_id(grade_id, non_related_word)
    query = ('DELETE FROM related_word WHERE word_id_1 = ? AND word_id_2 = ?')

    cur.execute(query, (word_id, non_related_word_id))
    cur.execute(query, (non_related_word_id, word_id))
    con.commit()

    create_non_related_word(word, non_related_word, grade_id)

  con.close()

def calculate_related_words(grade_id):
  con, cur = connect_to_database()
  words_list = get_grade_words(grade_id)

  grade_start = timeit.default_timer()
  for i in range(len(words_list)):
    if i % 100 == 0 and i > 0:
      print(timeit.default_timer() - grade_start)

    related_words = fetch_online_results(words_list[i])
    current_word_id = get_word_id(grade_id, words_list[i])

    related_words_ids = []
    for word in related_words:
      word_id = get_word_id(grade_id, word)

      if word_id != -1:
        related_words_ids.append(word_id)

    if len(related_words_ids) == 0: continue

    for word_id in related_words_ids:
      query = 'INSERT INTO related_word VALUES (null, ?, ?)'
      if current_word_id != word_id:
        cur.execute(query, (current_word_id, word_id))

    con.commit()
