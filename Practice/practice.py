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

def hello(tmp):
  print(tmp)

hello(5 > 0)
