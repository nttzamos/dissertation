from shared.database_handler import (get_grade_words_old, get_grade_words,
                                     get_words_old, get_words, connect_to_database,
                                     get_grade_table_name)
from models.subject import get_subject_name
from models.family import get_family_id, get_family_words
from models.related_word import get_related_words

def get_word_ids(grade_id):
  con, cur = connect_to_database('resources/database_old.db')
  cur.execute('SELECT id FROM ' + get_grade_table_name(grade_id) + ' ORDER BY id')
  ids = list(map(lambda id: id[0], cur.fetchall()))
  con.close()
  return ids

def get_word(grade_id, word_id):
  con, cur = connect_to_database('resources/database_old.db')
  cur.execute('SELECT word FROM ' + get_grade_table_name(grade_id) + ' WHERE id = ?', (word_id,))
  word = cur.fetchone()[0]
  con.close()
  return word

def get_subject_ids(grade_id):
  con, cur = connect_to_database()
  query = 'SELECT id FROM subject WHERE grade_id = ?'
  cur.execute(query, (grade_id, ))
  subject_ids = list(map(lambda subject: subject[0], cur.fetchall()))
  con.close()

  return subject_ids

word_ids_offset = [0, 6307, 14086, 26910, 41630, 62763, 82631]

# Words per grade
for grade_id in range(1, 7):
  print('Grade ' + str(grade_id))
  grade_words_old = get_grade_words_old(grade_id)
  grade_words = get_grade_words(grade_id)

  if len(grade_words_old) != len(grade_words):
    print('Different length')

  different_words_count = 0
  for i in range(len(grade_words)):
    if grade_words_old[i] != grade_words[i]:
      different_words_count += 1

  print('Number of words: ' + str(len(grade_words_old)))
  print('Number of different words: ' + str(different_words_count))
  print()

# quit()

# Words per subject
for grade_id in range(1, 7):
  print('Grade ' + str(grade_id))

  subject_ids = get_subject_ids(grade_id)
  for subject_id in subject_ids:
    subject_name = get_subject_name(subject_id)
    print('Subject: ' + subject_name)

    subject_words_old = get_words_old(-1, grade_id, subject_name)
    subject_words = get_words(-1, grade_id, subject_name)
    # print(len(subject_words_old))
    # print(len(subject_words))
    # print(subject_words_old)
    # print(); print(); print()
    # print(subject_words)
    # print(set(subject_words_old) - set(subject_words))
    # quit()

    if len(subject_words_old) != len(subject_words):
      print(len(subject_words_old))
      print('Different length: ' + str(len(subject_words_old)) + ' and ' + str(len(subject_words)))

    different_words_count = 0
    for i in range(len(subject_words)):
      if subject_words_old[i] != subject_words[i]:
        different_words_count += 1

    print('Number of words: ' + str(len(subject_words_old)))
    print('Number of different words: ' + str(different_words_count))
    print()
  print()

# Related words
# cnt = 0
# start = timeit.default_timer()
for grade_id in range(1, 7):
  print('Grade ' + str(grade_id))
  word_ids = get_word_ids(grade_id)

  different_words_count = 0
  for word_id in word_ids:
    offseted_word_id = word_id + word_ids_offset[grade_id - 1]
    # cnt += 1
    # if cnt % 1000 == 0:
    #   print(timeit.default_timer() - start)
    #   print(different_words_count)

    word = get_word(grade_id, word_id)
    family_id = get_family_id(grade_id, word_id)
    related_words = get_family_words(grade_id, family_id)

    related_words_new = get_related_words(grade_id, offseted_word_id)

    missing_words = list(set(related_words) - set(related_words_new))
    if len(related_words) != len(related_words_new):
      if len(missing_words) == 1 and missing_words[0] == word:
        continue
      different_words_count += 1

  print('Number of different words: ' + str(different_words_count))
  print()
