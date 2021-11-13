import sqlite3
import datetime
import tika
import string
from tika import parser
import re

class DBHandler():
  con = sqlite3.connect('new.db')
  cur = con.cursor()

  @staticmethod
  def init_db(self):
    DBHandler.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type=='table' AND name='words' ''')
    if DBHandler.cur.fetchone()[0]==1:
      print("Database exists.")
      return
    else:
      DBHandler.cur.execute('''CREATE TABLE words (word TEXT PRIMARY KEY, stem TEXT, lemma TEXT)''')
      DBHandler.cur.execute('''CREATE TABLE recentSearches (word TEXT PRIMARY KEY, time TIMESTAMP, starred INTEGER)''')
      DBHandler.cur.execute('''CREATE TABLE starredWords (id INTEGER, word TEXT)''')
      DBHandler.cur.execute('''CREATE TABLE recentActions (type TEXT, word1 TEXT, word2 TEXT, time TIMESTAMP)''')
      DBHandler.cur.execute('''CREATE TABLE subjects (subjectName TEXT, state INTEGER)''')
      # for word in words:
      #   self.addSingleWord(word)
      # self.addMultipleWords(words)
      self.addSubjectPDF()

  @staticmethod
  def dropTables(self):
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
  def addSingleWord(self, word):
    lemma = "lemma"
    stem = "stem"
    DBHandler.cur.execute("INSERT INTO words VALUES (?,?,?) ON CONFLICT(word) DO NOTHING", (word, stem, lemma))
    DBHandler.con.commit()

  @staticmethod
  def addMultipleWords(self, words):
    newList = []
    for i in range(len(words)):
      newList.append((words[i], "lemma", "stem"))
    DBHandler.cur.executemany("INSERT INTO words VALUES (?,?,?) ON CONFLICT(word) DO NOTHING", newList)
    DBHandler.con.commit()

  @staticmethod
  def getAllWords(self):
    DBHandler.cur.execute('SELECT word FROM words ORDER BY word')
    rows = DBHandler.cur.fetchall()
    words = [row[0] for row in rows]
    return words

  @staticmethod
  def addRecentSearch(self, word, starred):
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
  def deleteRecentSearch(self, word):
    DBHandler.cur.execute("DELETE FROM recentSearches WHERE word=?", (word,))
    DBHandler.con.commit()

  @staticmethod
  def getAllRecentSearches(self):
    DBHandler.cur.execute('SELECT word FROM recentSearches ORDER BY time')
    rows = DBHandler.cur.fetchall()
    words = [row[0] for row in rows]
    return words

  @staticmethod
  def addStarredWord(self, id, word):
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
  def isStarredWord(self, word):
    DBHandler.cur.execute("SELECT * FROM starredWords WHERE word=?", (word, ))
    data = DBHandler.cur.fetchall()
    if len(data)==0:
      return False
    else:
      return True

  @staticmethod
  def deleteStarredWord(self, word):
    DBHandler.cur.execute("DELETE FROM starredWords WHERE word=?", (word,))
    DBHandler.con.commit()

  @staticmethod
  def getStarredWordPosition(self, word):
    DBHandler.cur.execute("SELECT COUNT(*) FROM words WHERE word<?", (word,))
    position = DBHandler.cur.fetchone()[0]
    return position

  @staticmethod
  def getAllStarredWords(self):
    DBHandler.cur.execute('SELECT word FROM starredWords ORDER BY word')
    rows = DBHandler.cur.fetchall()
    words = [row[0] for row in rows]
    return words

  @staticmethod
  def addRecentAction(self, word):
    pass

  @staticmethod
  def deleteRecentAction(self, word):
    pass

  @staticmethod
  def addSubject(self, word):
    pass

  @staticmethod
  def deleteSubject(self, word):
    pass

  @staticmethod
  def isRemovable(self, inputString):
    return any(c.isdigit() for c in inputString) or re.search('[a-zA-Z]', inputString) or not(any(c.isalpha() for c in inputString))

  @staticmethod
  def addSubjectPDF(self):
    tika.initVM()
    # Έχω δυο επιλογές:
    # 1. να μην αφαιρέσω τα duplicates και να αφήσω την addMultipleWords να το χειριστεί
    # 2. να αφαιρέσω τα duplicates και να μην χρειαστεί να το χειριστεί η addMultipleWords
    print("Initializing Database")
    raw = parser.from_file("Subjects/Φυσική.pdf")
    pdf = raw["content"]
    words = pdf.split()
    for i in range(len(words)):
      words[i] = words[i].lower()
      words[i] = words[i].translate(str.maketrans('', '', string.punctuation))

    i = 0
    while i < len(words):
      if self.isRemovable(words[i]) or len(words[i])<3:
        del words[i]
      else:
        i += 1
    # for word in words:
    #   self.addSingleWord(word)
    self.addMultipleWords(words)

  @staticmethod
  def closeConnection(self):
    DBHandler.con.close()
    print("Connection closed successfully!")
