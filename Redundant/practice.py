from Common.pdfParser import PdfParser
from os import listdir
import re
import sqlite3
import requests
from bs4 import BeautifulSoup
import timeit

def fetchWord(word):
  url = 'https://el.wiktionary.org/wiki/{}'
  session = requests.Session()
  session.mount('http://', requests.adapters.HTTPAdapter(max_retries = 2))
  session.mount('https://', requests.adapters.HTTPAdapter(max_retries = 2))

  response = session.get(url.format(word))
  soup = BeautifulSoup(response.text.replace('>\n<', '><'), 'html.parser')

  compound_words = []
  relative_words = []

  compound_words_header = soup.find(id='Σύνθετα')
  if compound_words_header != None:
    compound_words_list = compound_words_header.find_next('ul')
    for item in compound_words_list.find_all():
      if item.name == 'li':
        compound_words.append(item.text)

  relative_words_header = soup.find(id='Συγγενικές_λέξεις')
  if relative_words_header != None:
    relative_words_list = relative_words_header.find_next('ul')
    for item in relative_words_list.find_all():
      if item.name == 'li':
        relative_words.append(item.text)

  return compound_words, relative_words, len(soup.find_all('div', class_='noarticletext')) > 0

def countTime():
  databases_directory_path = 'Databases/'
  database_file = 'database_clarin.db'
  con = sqlite3.connect(databases_directory_path + database_file)
  cur = con.cursor()

  total_count = 0
  total_time = 0
  seconds_per_hundred = 40

  for grade in range(1, 7):
    grade_table_name = 'grade_' + str(grade) + '_word'
    cur.execute('SELECT COUNT(*) FROM ' + grade_table_name)
    count = cur.fetchone()[0]
    time = ((count / 100) * seconds_per_hundred) / 60
    total_count += count; total_time += time
    print(count); print(time); print(time/60); print()

  print(total_count); print(total_time); print(total_time/60); con.close(); print()

def get_words(grade, cur):
  grade_table_name = 'grade_' + str(grade) + '_word'
  cur.execute('SELECT word FROM ' + grade_table_name)
  return list(map(lambda word: word[0], cur.fetchall()))

def get_word_id(word, cur, grade_table_name):
  cur.execute('SELECT id FROM ' + grade_table_name + ' WHERE word = ?', (word,))
  object = cur.fetchone()
  if object == None:
    return -1
  else:
    return object[0]

def get_family_id(word_id, cur, family_table_name):
  cur.execute('SELECT family_id FROM ' + family_table_name + ' WHERE word_id = ?', (word_id,))
  object = cur.fetchone()
  if object == None:
    return -1
  else:
    return object[0]

initial = False
database_created = True
families_created = False

if initial:
  for grade in range(1, 7):
    subject_names = PdfParser.get_grade_subjects_names(grade)
    subject_files = PdfParser.get_grade_subjects_files(grade)

    file_name = 'LemmaTesting/Grades/subjects' + str(grade) + '.txt'
    f = open(file_name, 'w')

    for i in range(len(subject_names)):
      text = PdfParser.readsubject_words(grade, subject_files[i], rawText=True)
      f.write(text)

    f.close()

    print('Grade ' + str(grade) + ' done!')

else:
  countTime()
  directoryPath = '../Grades/subjects'

  databases_directory_path = 'Databases/'
  database_file = 'database_clarin.db'

  con = sqlite3.connect(databases_directory_path + database_file)
  cur = con.cursor()

  # cur.execute('CREATE TABLE candidate (id INTEGER PRIMARY KEY AUTOINCREMENT, grade_id INTEGER, word_id INTEGER, word TEXT)')

  for grade in range(2, 7):
    grade_directory_path = directoryPath + str(grade) + '/'
    grade_table_name = 'grade_' + str(grade) + '_word'
    family_table_name = 'grade_' + str(grade) + '_family'

    if not database_created:
      files_list = listdir(grade_directory_path)

      cur.execute('CREATE TABLE ' + grade_table_name + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)')

      words_set = set()
      for file in files_list:
        if file == '.DS_Store' or 'processerror' in file:
          continue

        file_contents = open(grade_directory_path + file, 'r')
        file_lines = file_contents.readlines()
        for line in file_lines:
          line = line.strip()
          if line.startswith('<types:Lemma'):
            result = re.search('value="(.*)"/>', line)
            words_set.add(result.group(1))

      words_list = PdfParser.clean_words(list(words_set))

      from Common.databaseHandler import DBHandler
      words_list = DBHandler.sort_words_alphabetically(words_list)
      words = list(zip(list(range(1, len(words_list) + 1)), words_list))
      cur.executemany('INSERT INTO ' + grade_table_name + ' VALUES (?, ?)', words)
      con.commit()

    if not families_created:
      # cur.execute('DROP TABLE ' + family_table_name)
      cur.execute('CREATE TABLE ' + family_table_name + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER, family_id INTEGER)')
      con.commit()

      words_list = get_words(grade, cur)

      family_counter = 0
      compound_present = 0
      relative_present = 0
      both_present = 0

      grade_start = timeit.default_timer()

      for i in range(len(words_list)):
        if i % 100 == 0:
          print(str(i))
          print('Compound only present: ' + str(compound_present))
          print('Relative only present: ' + str(relative_present))
          print('Both Compound and Relative present: ' + str(both_present))
          print(timeit.default_timer() - grade_start)
          print()

        get_word_id(words_list[i], cur, grade_table_name)

        compound_words, relative_words, is_candidate = fetchWord(words_list[i])

        if len(compound_words) > 0 and len(relative_words) > 0:
          if is_candidate:
            print(words_list[i])
            quit()

          both_present += 1
        elif len(compound_words) > 0:
          if is_candidate:
            print(words_list[i])
            quit()

          compound_present += 1
        elif len(relative_words) > 0:
          if is_candidate:
            print(words_list[i])
            quit()

          relative_present += 1
        elif is_candidate:
          cur.execute('INSERT INTO candidate VALUES (null, ?, ?, ?)', (grade, words_list[i], i + 1))

        family_words = set(); family_words.update(compound_words); family_words.update(relative_words)
        words_in_dict = []
        for word in family_words:
          word_id = get_word_id(word, cur, grade_table_name)
          if word_id != -1:
            words_in_dict.append(word_id)

        if len(words_in_dict) == 0:
          continue

        added = False
        for word_id in words_in_dict:
          family_id = get_family_id(word_id, cur, family_table_name)
          if family_id != -1:
            cur.execute('INSERT INTO ' + family_table_name + ' VALUES (null, ?, ?)', (i + 1, family_id))
            added = True

        if not added:
          family_counter += 1
          cur.execute('INSERT INTO ' + family_table_name + ' VALUES (null, ?, ?)', (i + 1, family_counter))
          for word_id in words_in_dict:
            cur.execute('INSERT INTO ' + family_table_name + ' VALUES (null, ?, ?)', (word_id, family_counter))

        con.commit()

      print('Compound only present: ' + str(compound_present))
      print('Relative only present: ' + str(relative_present))
      print('Both Compound and Relative present: ' + str(both_present))
      print('Total Words: ' + str(len(words_list)))
      print('Grade ' + str(grade) + ' done!')

  con.close()
