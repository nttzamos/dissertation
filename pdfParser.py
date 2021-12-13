from os import listdir
import tika, tika.parser as parser
import string
import re
from databaseHandler import DBHandler

class PdfParser():
  @staticmethod
  def readGradeWords(grade):
    directoryPath = "Resources/Grades/" + str(grade)
    filesInDirectory = PdfParser.getFilesInDirectory(directoryPath)
    
    allSubjectsWords = {}
    for file in filesInDirectory:
      subjectWords = PdfParser.readWordsFromFile(directoryPath, file)
      allSubjectsWords = allSubjectsWords | set(subjectWords)


    DBHandler.addMultipleWords(allSubjectsWords)

  @staticmethod
  def readWordsFromFile(directoryPath, file):
    filePath = directoryPath + "/" + file

    tika.initVM()
    raw = parser.from_file(filePath)
    pdf = raw["content"]
    words = pdf.split()
    for i in range(len(words)):
      words[i] = words[i].lower()
      words[i] = words[i].translate(str.maketrans('', '', string.punctuation))

    i = 0
    while i < len(words):
      if DBHandler.isRemovable(words[i]) or len(words[i])<3:
        del words[i]
      else:
        i += 1

  @staticmethod
  def isRemovable(inputString):
    return any(c.isdigit() for c in inputString) or re.search('[a-zA-Z]', inputString) or not(any(c.isalpha() for c in inputString))

  @staticmethod
  def getFilesInDirectory(directoryPath):
    return listdir(directoryPath)