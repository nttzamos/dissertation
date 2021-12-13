from os import listdir
import tika, tika.parser as parser
import string
import timeit
import re
import sqlite3

def isRemovable(inputString):
  return any(c.isdigit() for c in inputString) or re.search('[a-zA-Z]', inputString) or not(any(c.isalpha() for c in inputString))

def readWordsFromFile(directoryPath, file):
  filePath = directoryPath + "/" + file

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
    if isRemovable(words[i]) or len(words[i])<3:
      del words[i]
    else:
      i += 1

  return words

# ------------------------------------------------------------------------------------ #

for grade in range(1, 7):
  directoryPath = "Resources/Grades/" + str(grade)
  filesInDirectory = listdir(directoryPath)

  subjects = []

  allSubjectsWords = set()

  start = timeit.default_timer()

  for file in filesInDirectory:
    subjectWords = readWordsFromFile(directoryPath, file)
    subjects.append(subjectWords)
    allSubjectsWords = allSubjectsWords | set(subjectWords)

  print("Elapsed time: " + str(timeit.default_timer() - start))
  print("Length of full set is: " + str(len(allSubjectsWords)))

  # for subject in subjects:
  #   print(subject)
  #   print()
  #   print()

  print(len(subjects))

  start = timeit.default_timer()

  allSubjectsWords = list(allSubjectsWords)


  # print(dbWords)
  con = sqlite3.connect("Databases2/practice" + str(grade) + ".db")
  cur = con.cursor()

  cur.execute('''CREATE TABLE subject_words (id INTEGER PRIMARY KEY, subject_id INTEGER, word TEXT)''')
  cur.execute('''CREATE TABLE words (id INTEGER PRIMARY KEY, word TEXT)''')
  
  dbWords = []
  for i in range(len(allSubjectsWords)):
    dbWords.append((i + 1, allSubjectsWords[i]))

  # for i in range(len(allSubjectsWords)):
  #   cur.execute("INSERT INTO words VALUES (?,?) ON CONFLICT(id) DO NOTHING", (i + 1, allSubjectsWords[i]))
  
  cur.executemany("INSERT INTO words VALUES (?,?) ON CONFLICT(id) DO NOTHING", dbWords)
  con.commit()

  print("creating db took: " + str(timeit.default_timer() - start))
