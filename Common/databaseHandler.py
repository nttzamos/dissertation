from os import path
from Common.pdfParser import PdfParser

import timeit
import sqlite3
import datetime

class DBHandler():
  databasesDirectoryPath = "Databases/"
  databaseFile = "database.db"

  @staticmethod
  def initializeDatabases():
    if path.isfile(DBHandler.databasesDirectoryPath + DBHandler.databaseFile):
      return

    DBHandler.initializeCommonDatabase()
    for grade in range(1, 7):
      DBHandler.initializeGradeDatabase(grade)

  @staticmethod
  def initializeCommonDatabase():
    databaseFilePath = DBHandler.databasesDirectoryPath + DBHandler.databaseFile

    if path.isfile(databaseFilePath):
      return

    con = sqlite3.connect(databaseFilePath)
    cur = con.cursor()
    gradesNames = ["Α' Δημοτικού", "Β' Δημοτικού", "Γ' Δημοτικού", "Δ' Δημοτικού", "Ε' Δημοτικού", "ΣΤ' Δημοτικού"]

    cur.execute('''CREATE TABLE grade (id INTEGER PRIMARY KEY, name TEXT)''')
    cur.execute('''CREATE TABLE subject (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, grade_id INTEGER)''')
    cur.execute('''CREATE TABLE student (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
    cur.execute('''CREATE TABLE profile (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, grade_id INTEGER)''')
    cur.execute('''CREATE TABLE student_profile (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, profile_id INTEGER)''')
    cur.execute('''CREATE TABLE profile_subject (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER, subject_id INTEGER)''')
    cur.execute('''CREATE TABLE candidate (id INTEGER PRIMARY KEY AUTOINCREMENT, grade_id INTEGER, word_id INTEGER)''')

    # Should we maybe remove profile_id?
    cur.execute('''CREATE TABLE recent_search (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER, profile_id INTEGER, student_id INTEGER, subject_id INTEGER, searched_at TIMESTAMP)''')
    cur.execute('''CREATE TABLE starred_word (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER, profile_id INTEGER, student_id INTEGER, subject_id INTEGER)''')

    for i in range(6):
      cur.execute("INSERT INTO grade VALUES (?, ?) ON CONFLICT(id) DO NOTHING", (i + 1, gradesNames[i]))
    con.commit()
    con.close()

  @staticmethod
  def addStudent(name, profiles):
    con, cur = DBHandler.connectToDatabase()

    cur.execute("INSERT INTO student VALUES (null, ?)", (name,))
    con.commit()
    con.close()

    DBHandler.addStudentProfiles(cur.lastrowid, profiles)

  @staticmethod
  def updateStudentName(studentId, newStudentName):
    con, cur = DBHandler.connectToDatabase()

    cur.execute("UPDATE student SET name = ? WHERE id = ?", (newStudentName, studentId))
    con.commit()
    con.close()

  @staticmethod
  def removeStudent(id):
    con, cur = DBHandler.connectToDatabase()

    cur.execute("DELETE FROM student WHERE id = ?", (id,))
    cur.execute("DELETE FROM student_profile WHERE student_id = ?", (id,))
    con.commit()
    con.close()

  @staticmethod
  def getStudents():
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT name FROM student ORDER BY name")
    students = list(map(lambda student: student[0], cur.fetchall()))

    con.close()
    return students

  @staticmethod
  def getStudentId(studentName):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT id FROM student WHERE name = ?", (studentName,))
    studentId = cur.fetchone()[0]
    con.close()
    return studentId

  @staticmethod
  def getStudentDetails(studentName):
    studentId = DBHandler.getStudentId(studentName)
    return studentId, DBHandler.getStudentProfiles(studentId)

  @staticmethod
  def studentNameExists(studentName):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT COUNT(*) FROM student WHERE name = ?", (studentName,))
    studentNameExists = cur.fetchone()[0] > 0
    con.close()

    return studentNameExists

  @staticmethod
  def addStudentProfiles(studentId, profiles):
    con, cur = DBHandler.connectToDatabase()
    for profile in profiles:
      profileId = DBHandler.getProfileId(profile)
      cur.execute("INSERT INTO student_profile VALUES (null, ?, ?)", (studentId, profileId))

    con.commit()
    con.close()

  @staticmethod
  def removeStudentProfiles(studentId, profiles):
    con, cur = DBHandler.connectToDatabase()

    # query = "DELETE FROM profileSubjects WHERE id IN ({})".format(", ".join("?" * len(subjects)))
    # cur.execute(query, subjects)

    for profile in profiles:
      profileId = DBHandler.getProfileId(profile)
      cur.execute("DELETE FROM student_profile WHERE student_id = ? AND profile_id = ?", (studentId, profileId))

    con.commit()
    con.close()

  @staticmethod
  def getStudentProfiles(studentId):
    con, cur = DBHandler.connectToDatabase()

    query = ('SELECT profile.name '
        'FROM student_profile '
        'INNER JOIN profile '
        'ON student_profile.profile_id = profile.id '
        'WHERE student_profile.student_id = ?')

    cur.execute(query, (studentId,))
    profileNames = list(map(lambda profileName: profileName[0], cur.fetchall()))

    con.close()

    return profileNames

  @staticmethod
  def addProfile(name, grade, subjects):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT name, id FROM subject WHERE grade_id = ?", (grade,))
    subjectDictionary = dict(cur.fetchall())
    con.close()

    subjectIds = []
    for subject in subjects:
      subjectIds.append(subjectDictionary[subject])

    con, cur = DBHandler.connectToDatabase()
    cur.execute("INSERT INTO profile VALUES (null, ?, ?)", (name, grade))
    profileSubjects = list(zip([cur.lastrowid] * len(subjectIds), subjectIds))
    cur.executemany("INSERT INTO profile_subject VALUES (null, ?, ?)", profileSubjects)

    con.commit()
    con.close()

  @staticmethod
  def updateProfileName(profileId, newProfileName):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("UPDATE profile SET name = ? WHERE id = ?", (newProfileName, profileId))

    con.commit()
    con.close()

  @staticmethod
  def removeProfile(id):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("DELETE FROM profile WHERE id = ?", (id,))
    cur.execute("DELETE FROM profile_subject WHERE profile_id = ?", (id,))
    cur.execute("DELETE FROM student_profile WHERE profile_id = ?", (id,))

    con.commit()
    con.close()

  @staticmethod
  def getProfiles():
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT name FROM profile ORDER BY id")
    profiles = list(map(lambda profile: profile[0], cur.fetchall()))

    con.close()
    return profiles

  @staticmethod
  def getProfileId(profileName):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT id FROM profile WHERE name = ?", (profileName,))
    profileId = cur.fetchone()[0]
    con.close()

    return profileId

  @staticmethod
  def getProfileName(profileId):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT name FROM profile WHERE id = ?", (profileId,))
    profileName = cur.fetchone()[0]
    con.close()

    return profileName

  @staticmethod
  def getProfileGrade(profileId):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT grade_id FROM profile WHERE id = ?", (profileId,))
    profileGrade = cur.fetchone()[0]
    con.close()

    return profileGrade

  @staticmethod
  def getProfileDetails(profileName):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT id, grade_id FROM profile WHERE name = ?", (profileName,))
    profileId, gradeId = cur.fetchone()

    cur.execute("SELECT name FROM grade WHERE id = ?", (gradeId,))
    gradeName = cur.fetchone()[0]

    query = ('SELECT name '
        'FROM subject '
        'INNER JOIN profile_subject '
        'ON subject.id = profile_subject.subject_id '
        'WHERE profile_subject.profile_id = ?')

    cur.execute(query, (profileId,))
    profileSubjects = list(map(lambda word: word[0], cur.fetchall()))

    con.close()
    return profileId, gradeId, gradeName, profileSubjects

  @staticmethod
  def profileNameExists(profileName):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT COUNT(*) FROM profile WHERE name = ?", (profileName,))
    profileNameExists = cur.fetchone()[0] > 0
    con.close()

    return profileNameExists

  @staticmethod
  def addProfileSubjects(gradeId, profileId, subjects):
    con, cur = DBHandler.connectToDatabase()

    subjectsIds = []
    for subject in subjects:
      subjectsIds.append(DBHandler.getSubjectId(gradeId, subject))

    profileSubjects = list(zip([profileId] * len(subjectsIds), subjectsIds))
    cur.executemany("INSERT INTO profile_subject VALUES (null, ?, ?)", profileSubjects)

    con.commit()
    con.close()

  @staticmethod
  def removeProfileSubjects(gradeId, profileId, subjects):
    con, cur = DBHandler.connectToDatabase()

    # query = "DELETE FROM profileSubjects WHERE id IN ({})".format(", ".join("?" * len(subjects)))
    # cur.execute(query, subjects)

    for subject in subjects:
      cur.execute("DELETE FROM profile_subject WHERE profile_id = ? AND subject_id = ?", (profileId, DBHandler.getSubjectId(gradeId, subject)))

    con.commit()
    con.close()

  @staticmethod
  def getProfileSubjects(profileId):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT subject_id FROM profile_subject WHERE profile_id = ?", (profileId,))

    profileSubjects = list(map(lambda subject: subject[0], cur.fetchall()))

    con.close()
    return profileSubjects

  @staticmethod
  def getGrades():
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT name FROM grade ORDER BY id")
    grades = list(map(lambda grade: grade[0], cur.fetchall()))

    con.close()
    return grades

  @staticmethod
  def initializeGradeDatabase(grade):
    databaseFilePath = DBHandler.databasesDirectoryPath + DBHandler.databaseFile

    gradeTableName = DBHandler.getGradeTableName(grade)
    subjectTableName = DBHandler.getSubjectTableName(grade)

    con = sqlite3.connect(databaseFilePath)
    cur = con.cursor()

    cur.execute('CREATE TABLE ' + gradeTableName + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)')
    cur.execute('CREATE TABLE ' + subjectTableName + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, subject_id INTEGER, word_id INTEGER)')

    subjectNames = PdfParser.getGradeSubjectsNames(grade)
    DBHandler.initializeSubjectsTable(cur, grade, subjectNames)
    con.commit()

    # grade_start = timeit.default_timer()

    # subjectFiles = PdfParser.getGradeSubjectsFiles(grade)
    wordsSet = set()
    wordsPerSubject = dict()
    for i in range(len(subjectNames)):
      # currentSubjectWords = list(set(PdfParser.readSubjectWords(grade, subjectFiles[i])))
      currentSubjectWords = ['Νίκος1', 'Νίκος2', 'Νίκος3']
      for j in range(len(currentSubjectWords)):
        currentSubjectWords[j] = 'subject' + str(i) + str(grade) + currentSubjectWords[j]
      wordsPerSubject[subjectNames[i]] = currentSubjectWords
      wordsSet = wordsSet | set(currentSubjectWords)

    wordsList = DBHandler.sortWordsAlphabetically(list(wordsSet))
    # print()
    # print("Grade: " + str(grade))
    # grade_middle_1 = timeit.default_timer()
    # print("Creating lists: " + str(grade_middle_1 - grade_start))

    words = list(zip(list(range(1, len(wordsList) + 1)), wordsList))
    cur.executemany('INSERT INTO ' + gradeTableName + ' VALUES (?, ?)', words)
    con.commit()

    # grade_middle_2 = timeit.default_timer()
    # print("Creating words table: " + str(grade_middle_2 - grade_middle_1))

    for i in range(len(subjectNames)):
      # Implementation 1
      # for j in range(len(wordsPerSubject[subjectNames[i]])):
      #   currentWord = wordsPerSubject[subjectNames[i]][j]
      #   wordsListIndex = wordsList.index(currentWord)
      #   cur.execute("INSERT INTO subject_words VALUES (null, ?, ?) ON CONFLICT(id) DO NOTHING", (i + 1, wordsListIndex))
      # con.commit()

      # Implementation 2
      wordsListIndeces = list()

      n = len(wordsPerSubject[subjectNames[i]])

      for j in range(n):
        wordsListIndeces.append(wordsList.index(wordsPerSubject[subjectNames[i]][j]))

      subjectId = DBHandler.getSubjectId(grade, subjectNames[i])
      subjectsWords = list(zip([subjectId] * n, wordsListIndeces))
      cur.executemany('INSERT INTO ' + subjectTableName + ' VALUES (null, ?, ?) ON CONFLICT(id) DO NOTHING', subjectsWords)
      con.commit()

    # grade_end = timeit.default_timer()
    # print("Creating subject_word table: " + str(grade_end - grade_middle_2))
    # print("Total: " + str(grade_end - grade_start))

    con.close()

  @staticmethod
  def sortWordsAlphabetically(words):
    translationTable = {
      940: 945, 941: 949, 972: 959, 974: 969, 943: 953, 942: 951, 973: 965
    }

    normalizedWords = list(map(lambda word: word.translate(translationTable), words))

    return [word for _, word in sorted(zip(normalizedWords, words))]

  @staticmethod
  def initializeSubjectsTable(cur, grade, subjectNames):
    subjects = list(zip(subjectNames, [grade] * len(subjectNames)))

    cur.executemany("INSERT INTO subject VALUES (null, ?, ?) ON CONFLICT(id) DO NOTHING", subjects)

  @staticmethod
  def getWords(profileId, gradeId, subjectName):
    if subjectName == 'All Subjects':
      subjectIds = DBHandler.getProfileSubjects(profileId)
    else:
      subjectIds = [DBHandler.getSubjectId(gradeId, subjectName)]

    con, cur = DBHandler.connectToDatabase()

    wordsSet = set()
    for subjectId in subjectIds:
      query = ('SELECT word '
        'FROM ' + DBHandler.getGradeTableName(gradeId) + ' ' +
        'INNER JOIN ' + DBHandler.getSubjectTableName(gradeId) + ' ' +
        'ON ' + DBHandler.getGradeTableName(gradeId) + '.id = ' + DBHandler.getSubjectTableName(gradeId) + '.word_id '
        'WHERE ' + DBHandler.getSubjectTableName(gradeId) + '.subject_id = ?')

      cur.execute(query, (subjectId,))
      subjectWords = list(map(lambda word: word[0], cur.fetchall()))
      wordsSet = wordsSet | set(subjectWords)

    con.close()
    words = list(wordsSet)
    words.sort()

    return words

  @staticmethod
  def getGradeWords(gradeId):
    con, cur = DBHandler.connectToDatabase()
    cur.execute('SELECT word FROM ' + DBHandler.getGradeTableName(gradeId) + ' ORDER BY word')
    words = list(map(lambda word: word[0], cur.fetchall()))

    con.close()
    return words

  @staticmethod
  def getCandidateWords(gradeId):
    con, cur = DBHandler.connectToDatabase()
    query = ('SELECT word '
        'FROM ' + DBHandler.getGradeTableName(gradeId) + ' ' +
        'INNER JOIN candidate '
        'ON ' + DBHandler.getGradeTableName(gradeId) + '.id = candidate.word_id '
        'WHERE candidate.grade_id = ?')

    cur.execute(query, (gradeId,))
    words = list(map(lambda word: word[0], cur.fetchall()))

    con.close()
    return words

  @staticmethod
  def addRecentSearch(word):
    from MainWidget.currentSearch import CurrentSearch
    studentId, profileId, grade, subjectName = CurrentSearch.getCurrentSelectionDetails()
    if subjectName == -1:
      return # got to change

    subjectId = DBHandler.getSubjectId(grade, subjectName)

    wordId = DBHandler.getWordId(grade, word)
    recentSearchExists = DBHandler.recentSearchExists(wordId, profileId)
    dateTimeNow = datetime.datetime.now()
    con, cur = DBHandler.connectToDatabase()

    if recentSearchExists:
      cur.execute("UPDATE recent_search SET searched_at = ? WHERE word_id = ? AND profile_id = ? AND student_id = ?", (dateTimeNow, wordId, profileId, studentId))
    else:
      cur.execute("INSERT INTO recent_search VALUES (null, ?, ?, ?, ?, ?)", (wordId, profileId, studentId, subjectId, dateTimeNow))

    con.commit()
    con.close()
    return recentSearchExists

  @staticmethod
  def recentSearchExists(wordId, profileId):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT COUNT(*) FROM recent_search WHERE word_id = ? AND profile_id = ?", (wordId, profileId))
    recentSearchExists = cur.fetchone()[0] > 0
    con.close()
    return recentSearchExists

  @staticmethod
  def removeRecentSearch(word):
    from MainWidget.currentSearch import CurrentSearch
    studentId, profileId, grade, subjectName = CurrentSearch.getCurrentSelectionDetails()

    con, cur = DBHandler.connectToDatabase()
    wordId = DBHandler.getWordId(grade, word)
    cur.execute("DELETE FROM recent_search WHERE word_id = ? AND profile_id = ? AND student_id = ?", (wordId, profileId, studentId))
    con.commit()
    con.close()

  @staticmethod
  def getRecentSearches():
    from MainWidget.currentSearch import CurrentSearch
    studentId, profileId, grade, subjectName = CurrentSearch.getCurrentSelectionDetails()
    if subjectName == -1:
      extraInfo = (profileId, studentId)
      query = ('SELECT word '
        'FROM ' + DBHandler.getGradeTableName(grade) + ' ' +
        'INNER JOIN recent_search '
        'ON ' + DBHandler.getGradeTableName(grade) + '.id = recent_search.word_id '
        'WHERE recent_search.profile_id = ? '
        'AND recent_search.student_id = ? '
        'ORDER BY recent_search.searched_at ')
    else:
      extraInfo = (DBHandler.getSubjectId(grade, subjectName), profileId, studentId)
      query = ('SELECT word '
        'FROM ' + DBHandler.getGradeTableName(grade) + ' ' +
        'INNER JOIN recent_search '
        'ON ' + DBHandler.getGradeTableName(grade) + '.id = recent_search.word_id '
        'WHERE recent_search.subject_id = ? '
        'AND recent_search.profile_id = ? '
        'AND recent_search.student_id = ? '
        'ORDER BY recent_search.searched_at ')

    con, cur = DBHandler.connectToDatabase()

    cur.execute(query, extraInfo)
    recentSearches = list(map(lambda recentSearch: recentSearch[0], cur.fetchall()))
    con.close()
    return recentSearches

  @staticmethod
  def addStarredWord(word):
    from MainWidget.currentSearch import CurrentSearch
    studentId, profileId, grade, subjectName = CurrentSearch.getCurrentSelectionDetails()
    if subjectName == -1:
      return # got to change

    subjectId = DBHandler.getSubjectId(grade, subjectName)

    con, cur = DBHandler.connectToDatabase()
    wordId = DBHandler.getWordId(grade, word)

    cur.execute("INSERT INTO starred_word VALUES (null, ?, ?, ?, ?)", (wordId, profileId, studentId, subjectId))
    con.commit()
    con.close()

  @staticmethod
  def starredWordExists(word):
    from MainWidget.currentSearch import CurrentSearch
    studentId, profileId, grade, subjectName = CurrentSearch.getCurrentSelectionDetails()

    wordId = DBHandler.getWordId(grade, word)
    con, cur = DBHandler.connectToDatabase()

    cur.execute("SELECT COUNT(*) FROM starred_word WHERE word_id = ? AND profile_id = ? AND student_id = ?", (wordId, profileId, studentId))
    return cur.fetchone()[0] > 0

  @staticmethod
  def removeStarredWord(word):
    from MainWidget.currentSearch import CurrentSearch
    studentId, profileId, grade, subjectName = CurrentSearch.getCurrentSelectionDetails()

    con, cur = DBHandler.connectToDatabase()
    wordId = DBHandler.getWordId(grade, word)
    cur.execute("DELETE FROM starred_word WHERE word_id = ? AND profile_id = ? AND student_id = ?", (wordId, profileId, studentId))
    con.commit()
    con.close()

  @staticmethod
  def getStarredWords():
    from MainWidget.currentSearch import CurrentSearch
    studentId, profileId, grade, subjectName = CurrentSearch.getCurrentSelectionDetails()

    con, cur = DBHandler.connectToDatabase()

    if subjectName == -1:
      extraInfo = (profileId, studentId)
      query = ('SELECT word '
          'FROM ' + DBHandler.getGradeTableName(grade) + ' ' +
          'INNER JOIN starred_word '
          'ON ' + DBHandler.getGradeTableName(grade) + '.id = starred_word.word_id '
          'WHERE starred_word.profile_id = ? '
          'AND starred_word.student_id = ? '
          'ORDER BY ' + DBHandler.getGradeTableName(grade) + '.id DESC')
    else:
      extraInfo = (DBHandler.getSubjectId(grade, subjectName), profileId, studentId)
      query = ('SELECT word '
          'FROM ' + DBHandler.getGradeTableName(grade) + ' ' +
          'INNER JOIN starred_word '
          'ON ' + DBHandler.getGradeTableName(grade) + '.id = starred_word.word_id '
          'WHERE starred_word.subject_id = ? '
          'AND starred_word.profile_id = ? '
          'AND starred_word.student_id = ? '
          'ORDER BY ' + DBHandler.getGradeTableName(grade) + '.id DESC')

    cur.execute(query, extraInfo)
    starredWords = list(map(lambda starredWord: starredWord[0], cur.fetchall()))
    con.close()
    return starredWords

  @staticmethod
  def getSubjectId(grade, subject):
    con, cur = DBHandler.connectToDatabase()
    cur.execute('SELECT id FROM subject WHERE grade_id = ? AND name = ?', (grade, subject))
    subjectId = cur.fetchone()[0]
    cur.close()
    con.close()
    return subjectId

  @staticmethod
  def getSubjectName(subjectId):
    con, cur = DBHandler.connectToDatabase()
    cur.execute('SELECT name FROM subject WHERE id = ?', (subjectId,))
    subjectName = cur.fetchone()[0]
    cur.close()
    con.close()
    return subjectName

  @staticmethod
  def getWordId(grade, word):
    con, cur = DBHandler.connectToDatabase()
    cur.execute('SELECT id FROM ' + DBHandler.getGradeTableName(grade) + ' WHERE word = ?', (word,))
    wordId = cur.fetchone()[0]
    cur.close()
    con.close()
    return wordId

  @staticmethod
  def updateWord(oldWord, newWord, grades):
    for grade in grades:
      con, cur = DBHandler.connectToDatabase()

      if DBHandler.wordExists(cur, grade, newWord):
        DBHandler.removeWordFromGrade(cur, oldWord)
      else:
        cur.execute('UPDATE ' + DBHandler.getGradeTableName(grade) + ' SET word = ? WHERE word = ?', (newWord , oldWord))

      con.commit()
      con.close()

  @staticmethod
  def deleteWord(word, grades):
    for grade in grades:
      con, cur = DBHandler.connectToDatabase()

      DBHandler.removeWordFromGrade(cur, grade, word)

      con.commit()
      con.close()

  @staticmethod
  def removeWordFromGrade(cur, grade, word):
    if DBHandler.wordExists(cur, grade, word):
      wordId = DBHandler.getWordId(cur, word)
      cur.execute('DELETE FROM ' + DBHandler.getGradeTableName(grade) + ' WHERE id = ?', (wordId,))
      cur.execute('DELETE FROM subject_word WHERE word_id = ?', (wordId,))
      cur.execute('DELETE FROM recent_search WHERE word_id = ?', (wordId,))
      cur.execute('DELETE FROM starred_word WHERE word_id = ?', (wordId,))

  @staticmethod
  def wordExists(cur, grade, word):
    cur.execute('SELECT COUNT(*) FROM ' + DBHandler.getGradeTableName(grade) + ' WHERE word = ?', (word,))
    return cur.fetchone()[0] > 0

  @staticmethod
  def getGradeSubjects(grade):
    con, cur = DBHandler.connectToDatabase()
    cur.execute("SELECT name FROM subject WHERE grade_id = ? ORDER BY name", (grade,))
    subjects = list(map(lambda subject: subject[0], cur.fetchall()))
    con.close()
    return subjects

  @staticmethod
  def getGradeTableName(grade):
    return 'grade_' + str(grade) + '_word'

  @staticmethod
  def getSubjectTableName(grade):
    return 'subject_' + str(grade) + '_word'

  @staticmethod
  def connectToDatabase():
    con = sqlite3.connect(DBHandler.databasesDirectoryPath + DBHandler.databaseFile)
    cur = con.cursor()
    return con, cur
