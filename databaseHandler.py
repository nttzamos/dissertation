from os import path
from pdfParser import PdfParser

import timeit
import sqlite3
import datetime

class DBHandler():
  databasesDirectoryPath = "Databases/"
  gradeFileName = "grade_"
  commonDatabaseFile = "common.db"

  # --- Initialization code ---
  @staticmethod
  def initializeDatabases():
    DBHandler.initializeCommonDatabase()

    if DBHandler.databasesExist():
      return

    for grade in range(1, 7):
      DBHandler.initializeGradeDatabase(grade)

  @staticmethod
  def initializeCommonDatabase():
    commonDatabaseFilePath = DBHandler.databasesDirectoryPath + DBHandler.commonDatabaseFile

    if path.isfile(commonDatabaseFilePath):
      return

    con = sqlite3.connect(commonDatabaseFilePath)
    cur = con.cursor()
    gradesNames = ["Α' Δημοτικού", "Β' Δημοτικού", "Γ' Δημοτικού", "Δ' Δημοτικού", "Ε' Δημοτικού", "ΣΤ' Δημοτικού"]

    cur.execute('''CREATE TABLE grades (id INTEGER PRIMARY KEY, name TEXT)''')

    for i in range(6):
      cur.execute("INSERT INTO grades VALUES (?, ?) ON CONFLICT(id) DO NOTHING", (i + 1, gradesNames[i]))
    con.commit()
    con.close()

  @staticmethod
  def getGrades():
    con, cur = DBHandler.connectToCommonDatabase()
    cur.execute("SELECT name FROM grades ORDER BY id")
    grades = list(map(lambda grade: grade[0], cur.fetchall()))

    con.close()
    return grades

  @staticmethod
  def getGradeSubjects(grade):
    con, cur = DBHandler.connectToGradeDatabase(grade)
    cur.execute("SELECT name FROM subjects ORDER BY id")
    subjects = list(map(lambda subject: subject[0], cur.fetchall()))

    con.close()
    return subjects

  @staticmethod
  def initializeGradeDatabase(grade):
    gradeDatabaseFilePath = DBHandler.databasesDirectoryPath + DBHandler.gradeFileName + str(grade) + ".db"

    # Connecting to the database
    con = sqlite3.connect(gradeDatabaseFilePath)
    cur = con.cursor()

    # Creating the necessary tables
    cur.execute('''CREATE TABLE words (id INTEGER PRIMARY KEY, word TEXT)''')
    cur.execute('''CREATE TABLE subjectWords (id INTEGER PRIMARY KEY, subjectId INTEGER, wordId INTEGER)''')
    cur.execute('''CREATE TABLE recentSearches (id INTEGER PRIMARY KEY AUTOINCREMENT, wordId INTEGER, searchedAt TIMESTAMP)''')
    cur.execute('''CREATE TABLE starredWords (id INTEGER PRIMARY KEY AUTOINCREMENT, wordId INTEGER)''')

    # Creating the subjects table
    subjectNames = PdfParser.getGradeSubjectsNames(grade)
    DBHandler.initializeSubjectsTable(cur, subjectNames)
    con.commit()

    grade_start = timeit.default_timer()

    subjectFiles = PdfParser.getGradeSubjectsFiles(grade)
    wordsSet = set()
    wordsPerSubject = dict()
    for i in range(len(subjectFiles)):
      currentSubjectWords = list(set(PdfParser.readSubjectWords(grade, subjectFiles[i])))
      wordsPerSubject[subjectNames[i]] = currentSubjectWords
      wordsSet = wordsSet | set(currentSubjectWords)

    wordsList = DBHandler.wordsOrderedAlphabetically(list(wordsSet))
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
  def wordsOrderedAlphabetically(words):
    translationTable = {
      940: 945, 941: 949, 972: 959, 974: 969, 943: 953, 942: 951, 973: 965
    }

    normalizedWords = list(map(lambda word: word.translate(translationTable), words))

    return [word for _, word in sorted(zip(normalizedWords, words))]

  @staticmethod
  def initializeSubjectsTable(cur, subjectNames):
    cur.execute('''CREATE TABLE subjects (id INTEGER PRIMARY KEY, name TEXT)''')

    subjects = list()
    for i in range(len(subjectNames)):
      subjects.append([i + 1, subjectNames[i]])

    print(subjects)
    cur.executemany("INSERT INTO subjects VALUES (?,?) ON CONFLICT(id) DO NOTHING", subjects)

  @staticmethod
  def getWords(grade):
    con, cur = DBHandler.connectToGradeDatabase(grade)
    cur.execute('SELECT word FROM words ORDER BY word')
    words = list(map(lambda word: word[0], cur.fetchall()))

    con.close()
    return words

  # --- Recent searches code ---
  @staticmethod
  def addRecentSearch(word):
    from MainWidget.currentSearch import CurrentSearch
    grade = CurrentSearch.currentGrade

    con, cur = DBHandler.connectToGradeDatabase(grade)
    wordId = DBHandler.getWordId(cur, word)
    recentSearchExists = DBHandler.recentSearchExists(cur, wordId)
    dateTimeNow = datetime.datetime.now()

    if recentSearchExists:
      cur.execute("UPDATE recentSearches SET searchedAt = ? WHERE wordId = ?", (dateTimeNow, wordId))
    else:
      cur.execute("INSERT INTO recentSearches VALUES (null, ?, ?)", (wordId, dateTimeNow))

    con.commit()
    con.close()
    return recentSearchExists

  @staticmethod
  def recentSearchExists(cur, wordId):
    cur.execute("SELECT COUNT(*) FROM recentSearches WHERE wordId = ?", (wordId,))
    return cur.fetchone()[0] > 0

  @staticmethod
  def removeRecentSearch(word):
    from MainWidget.currentSearch import CurrentSearch
    grade = CurrentSearch.currentGrade

    con, cur = DBHandler.connectToGradeDatabase(grade)
    wordId = DBHandler.getWordId(cur, word)
    cur.execute("DELETE FROM recentSearches WHERE wordId = ?", (wordId,))
    con.commit()
    con.close()

  @staticmethod
  def getRecentSearches():
    from MainWidget.currentSearch import CurrentSearch
    grade = CurrentSearch.currentGrade

    con, cur = DBHandler.connectToGradeDatabase(grade)
    sql = '''SELECT word
        FROM words
        INNER JOIN recentSearches
        ON words.id = recentSearches.wordId
        ORDER BY recentSearches.searchedAt'''

    cur.execute(sql)
    recentSearches = list(map(lambda recentSearch: recentSearch[0], cur.fetchall()))
    con.close()
    return recentSearches

  # --- Starred words code ---
  @staticmethod
  def addStarredWord(word):
    from MainWidget.currentSearch import CurrentSearch
    grade = CurrentSearch.currentGrade

    con, cur = DBHandler.connectToGradeDatabase(grade)
    wordId = DBHandler.getWordId(cur, word)

    cur.execute("INSERT INTO starredWords VALUES (null, ?)", (wordId,))
    con.commit()
    con.close()

  @staticmethod
  def starredWordExists(word):
    from MainWidget.currentSearch import CurrentSearch
    grade = CurrentSearch.currentGrade

    con, cur = DBHandler.connectToGradeDatabase(grade)
    wordId = DBHandler.getWordId(cur, word)

    cur.execute("SELECT COUNT(*) FROM starredWords WHERE wordId = ?", (wordId,))
    return cur.fetchone()[0] > 0

  @staticmethod
  def removeStarredWord(word):
    from MainWidget.currentSearch import CurrentSearch
    grade = CurrentSearch.currentGrade

    con, cur = DBHandler.connectToGradeDatabase(grade)
    wordId = DBHandler.getWordId(cur, word)
    cur.execute("DELETE FROM starredWords WHERE wordId = ?", (wordId,))
    con.commit()
    con.close()

  @staticmethod
  def getStarredWords():
    from MainWidget.currentSearch import CurrentSearch
    grade = CurrentSearch.currentGrade

    con, cur = DBHandler.connectToGradeDatabase(grade)

    sql = '''SELECT word
        FROM words
        INNER JOIN starredWords
        ON words.id = starredWords.wordId
        ORDER BY words.id DESC'''

    cur.execute(sql)
    starredWords = list(map(lambda starredWord: starredWord[0], cur.fetchall()))
    con.close()
    return starredWords

  @staticmethod
  def getWordId(cur, word):
    cur.execute("SELECT id FROM words WHERE word = ?", (word,))
    return cur.fetchone()[0]

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
      return True
      quit()

  @staticmethod
  def updateWord(oldWord, newWord, grades):
    for grade in grades:
      con, cur = DBHandler.connectToGradeDatabase(grade)

      if DBHandler.wordExists(cur, newWord):
        DBHandler.removeWordFromGrade(cur, oldWord)
      else:
        cur.execute("UPDATE words SET word = ? WHERE word = ?", (newWord, oldWord))
        # update relevant tables as well?

      con.commit()
      con.close()

  @staticmethod
  def deleteWord(word, grades):
    for grade in grades:
      con, cur = DBHandler.connectToGradeDatabase(grade)

      DBHandler.removeWordFromGrade(cur, word)

      con.commit()
      con.close()

  @staticmethod
  def removeWordFromGrade(cur, word):
    wordId = DBHandler.getWordId(cur, word)
    cur.execute("DELETE FROM words WHERE id = ?", (wordId,))
    cur.execute("DELETE FROM subjectWords WHERE wordId = ?", (wordId,))
    cur.execute("DELETE FROM recentSearches WHERE wordId = ?", (wordId,))
    cur.execute("DELETE FROM starredWords WHERE wordId = ?", (wordId,))

  @staticmethod
  def wordExists(cur, word):
    cur.execute("SELECT id FROM words WHERE word = ?", (word,))
    return cur.fetchone()[0]

  @staticmethod
  def connectToGradeDatabase(grade):
    gradeDatabaseFilePath = DBHandler.databasesDirectoryPath + DBHandler.gradeFileName + str(grade) + ".db"
    con = sqlite3.connect(gradeDatabaseFilePath)
    cur = con.cursor()
    return con, cur

  @staticmethod
  def connectToCommonDatabase():
    con = sqlite3.connect(DBHandler.databasesDirectoryPath + DBHandler.commonDatabaseFile)
    cur = con.cursor()
    return con, cur
