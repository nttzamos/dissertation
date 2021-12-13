from os import listdir
from os import path

import tika, tika.parser as parser
import string
import timeit
import re

import sqlite3
import datetime

class DBHandler():
  con = sqlite3.connect('new.db')
  cur = con.cursor()

  gradesSubjectsDirectoryPath = "Resources/Grades/"
  databasesDirectoryPath = "Databases/"
  gradeFileName = "grade_"
  commonDatabaseFile = "common.db"

  @staticmethod
  def initializeDatabases():
    DBHandler.initializeCommonDatabase()

    if DBHandler.databasesExist():
      return

    for grade in range(1, 7):
      DBHandler.initializeGradeDatabase(grade)

  @staticmethod
  def initializeCommonDatabase():
    if path.isfile(DBHandler.databasesDirectoryPath + DBHandler.commonDatabaseFile):
      return
    
    con = sqlite3.connect(DBHandler.databasesDirectoryPath + DBHandler.commonDatabaseFile)
    cur = con.cursor()
    gradesNames = ["Α' Δημοτικού", "Β' Δημοτικού", "Γ' Δημοτικού", "Δ' Δημοτικού", "Ε' Δημοτικού", "ΣΤ' Δημοτικού"]

    cur.execute('''CREATE TABLE grades (id INTEGER PRIMARY KEY, name TEXT)''')
    cur.execute('''CREATE TABLE recentSearches (word TEXT PRIMARY KEY, time TIMESTAMP, starred INTEGER)''')
    cur.execute('''CREATE TABLE starredWords (id INTEGER, wordId INTEGER)''')
    
    for i in range(6):
      cur.execute("INSERT INTO grades VALUES (?, ?) ON CONFLICT(id) DO NOTHING", (i + 1, gradesNames[i]))
    con.commit()
    con.close()
  
  @staticmethod
  def databasesExist():
    base = DBHandler.databasesDirectoryPath + DBHandler.gradeFileName
    extension = ".db"
    existingDatabasesCount = 0
    for grade in range(1, 7):
      if path.isfile(base + str(grade) + extension):
        existingDatabasesCount += 1
    
    if existingDatabasesCount == 0:
      return False
    elif existingDatabasesCount == 6:
      return True
    else:
      print("Databases are more than 0 and less than 6.")
      quit()

  @staticmethod
  def initializeGradeDatabase(grade):
    con = sqlite3.connect(DBHandler.databasesDirectoryPath + DBHandler.gradeFileName + str(grade) + ".db")
    cur = con.cursor()

    cur.execute('''CREATE TABLE words (id INTEGER PRIMARY KEY, word TEXT)''')
    cur.execute('''CREATE TABLE subjectWords (id INTEGER PRIMARY KEY, subjectId INTEGER, wordId INTEGER)''')

    subjectFiles = DBHandler.getGradeSubjectsFiles(grade)
    subjectNames = DBHandler.getGradeSubjectsNames(grade)
    
    DBHandler.initializeSubjectsTable(cur, subjectNames)
    con.commit()

    grade_start = timeit.default_timer()

    wordsSet = set()
    wordsPerSubject = dict()
    for i in range(len(subjectFiles)):
      currentSubjectWords = list(set(DBHandler.readSubjectWords(grade, subjectFiles[i])))
      wordsPerSubject[subjectNames[i]] = currentSubjectWords
      wordsSet = wordsSet | set(currentSubjectWords)

    wordsList = list(wordsSet)
    print()
    print("Grade: " + str(grade))
    grade_middle_1 = timeit.default_timer()
    print("Creating lists: " + str(grade_middle_1 - grade_start))

    words = list(zip(list(range(1, len(wordsList) + 1)), wordsList))
    cur.executemany("INSERT INTO words VALUES (?, ?) ON CONFLICT(id) DO NOTHING", words)
    con.commit()

    grade_middle_2 = timeit.default_timer()
    print("Creating words table: " + str(grade_middle_2 - grade_middle_1))

    globalIndex = 0
    for i in range(len(subjectNames)):
      # Implementation 1
      # for j in range(len(wordsPerSubject[subjectNames[i]])):
      #   globalIndex += 1
      #   currentWord = wordsPerSubject[subjectNames[i]][j]
      #   wordsListIndex = wordsList.index(currentWord)
      #   cur.execute("INSERT INTO subjectWords VALUES (?, ?, ?) ON CONFLICT(id) DO NOTHING", (globalIndex, i + 1, wordsListIndex))
      # con.commit()

      # Implementation 2
      wordsListIndeces = list()

      n = len(wordsPerSubject[subjectNames[i]])
      globalIndex += 1

      for j in range(n):
        wordsListIndeces.append(wordsList.index(wordsPerSubject[subjectNames[i]][j]))
      subjectsWords = list(zip(list(range(globalIndex, globalIndex + n)), [i + 1] * n, wordsListIndeces))
      cur.executemany("INSERT INTO subjectWords VALUES (?, ?, ?) ON CONFLICT(id) DO NOTHING", subjectsWords)
      con.commit()

      globalIndex += n

    grade_end = timeit.default_timer()
    print("Creating subjects_words table: " + str(grade_end - grade_middle_2))
    print("Total: " + str(grade_end - grade_start))

    con.close()

  @staticmethod
  def readSubjectWords(grade, subjectFile):
    filePath = DBHandler.gradesSubjectsDirectoryPath + str(grade) + "/" + subjectFile

    tika.initVM()
    raw = parser.from_file(filePath)
    pdf = raw["content"]
    words = pdf.split()
    for i in range(len(words)):
      words[i] = words[i].lower()
      words[i] = re.sub(r'[^\w\s]', '', words[i])
      # words[i] = words[i].translate(str.maketrans('', '', string.punctuation))
    
    i = 0
    while i < len(words):
      if DBHandler.wordIsRemovable(words[i]) or len(words[i])<3:
        del words[i]
      else:
        i += 1

    return words

  @staticmethod
  def wordIsRemovable(inputString):
    return any(c.isdigit() for c in inputString) or re.search('[a-zA-Z]', inputString) or not(any(c.isalpha() for c in inputString))

  @staticmethod
  def initializeSubjectsTable(cur, subjectNames):
    cur.execute('''CREATE TABLE subjects (id INTEGER PRIMARY KEY, name TEXT)''')

    subjects = list()
    for i in range(len(subjectNames)):
      subjects.append([i + 1, subjectNames[i]])

    print(subjects)
    cur.executemany("INSERT INTO subjects VALUES (?,?) ON CONFLICT(id) DO NOTHING", subjects)

  @staticmethod
  def getGradeSubjectsNames(grade):
    return list(map(
      lambda subjectFile: subjectFile.replace('.pdf', ''), DBHandler.getGradeSubjectsFiles(grade)
    ))
    

  @staticmethod
  def getGradeSubjectsFiles(grade):
    return listdir(DBHandler.gradesSubjectsDirectoryPath + str(grade))

  @staticmethod
  def init_db():
    DBHandler.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type=='table' AND name='words' ''')
    if DBHandler.cur.fetchone()[0]==1:
      print("Database exists.")
      return
    else:
      print("Database will be created.")
      DBHandler.cur.execute('''CREATE TABLE words (word TEXT PRIMARY KEY, stem TEXT, lemma TEXT)''')
      DBHandler.cur.execute('''CREATE TABLE recentSearches (word TEXT PRIMARY KEY, time TIMESTAMP, starred INTEGER)''')
      DBHandler.cur.execute('''CREATE TABLE starredWords (id INTEGER, word TEXT)''')
      DBHandler.cur.execute('''CREATE TABLE recentActions (type TEXT, word1 TEXT, word2 TEXT, time TIMESTAMP)''')
      DBHandler.cur.execute('''CREATE TABLE subjects (subjectName TEXT, state INTEGER)''')

  @staticmethod
  def dropTables():
    DBHandler.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type=='table' AND name='words' ''')
    if DBHandler.cur.fetchone()[0]==0:
      print("Database does not exist.")
      return
    else:
      DBHandler.cur.execute('''DROP TABLE words''')
      DBHandler.cur.execute('''DROP TABLE recentSearches''')
      DBHandler.cur.execute('''DROP TABLE starredWords''')
      DBHandler.cur.execute('''DROP TABLE recentActions''')
      DBHandler.cur.execute('''DROP TABLE subjects''')

  @staticmethod
  def getAllWords():
    DBHandler.cur.execute('SELECT word FROM words ORDER BY word')
    rows = DBHandler.cur.fetchall()
    words = [row[0] for row in rows]
    return words

  @staticmethod
  def addRecentSearch(word, starred):
    DBHandler.cur.execute("SELECT * FROM recentSearches WHERE word=?", (word, ))
    data = DBHandler.cur.fetchall()
    if len(data)==0:
      now = datetime.datetime.now()
      # DBHandler.cur.execute("INSERT INTO recentSearches VALUES (?,?) ON CONFLICT(word) DO NOTHING", (word, now))
      DBHandler.cur.execute("INSERT INTO recentSearches VALUES (?,?,?)", (word, now, starred))
      DBHandler.con.commit()
      return True
    else:
      now = datetime.datetime.now()
      DBHandler.cur.execute("UPDATE recentSearches SET time=? WHERE word=?", (now, word))
      DBHandler.con.commit()
      return False

  @staticmethod
  def deleteRecentSearch(word):
    DBHandler.cur.execute("DELETE FROM recentSearches WHERE word=?", (word,))
    DBHandler.con.commit()

  @staticmethod
  def getAllRecentSearches():
    DBHandler.cur.execute('SELECT word FROM recentSearches ORDER BY time')
    rows = DBHandler.cur.fetchall()
    words = [row[0] for row in rows]
    return words

  @staticmethod
  def addStarredWord(id, word):
    DBHandler.cur.execute("SELECT * FROM starredWords WHERE word=?", (word, ))
    data = DBHandler.cur.fetchall()
    if len(data)==0:
      # DBHandler.cur.execute("INSERT INTO starredWords VALUES (?,?) ON CONFLICT(word) DO NOTHING", (id, word))
      DBHandler.cur.execute("INSERT INTO starredWords VALUES (?,?)", (id, word))
      DBHandler.con.commit()
      return True
    else:
      return False

  @staticmethod
  def isStarredWord(word):
    DBHandler.cur.execute("SELECT * FROM starredWords WHERE word=?", (word, ))
    data = DBHandler.cur.fetchall()
    if len(data)==0:
      return False
    else:
      return True

  @staticmethod
  def deleteStarredWord(word):
    DBHandler.cur.execute("DELETE FROM starredWords WHERE word=?", (word,))
    DBHandler.con.commit()

  @staticmethod
  def getStarredWordPosition(word):
    DBHandler.cur.execute("SELECT COUNT(*) FROM starredWords WHERE word < ?", (word,))
    position = DBHandler.cur.fetchone()[0]
    return position

  @staticmethod
  def getAllStarredWords():
    DBHandler.cur.execute('SELECT word FROM starredWords ORDER BY word DESC')
    rows = DBHandler.cur.fetchall()
    words = [row[0] for row in rows]
    return words

  @staticmethod
  def closeConnection():
    DBHandler.con.close()
    print("Connection closed successfully!")
