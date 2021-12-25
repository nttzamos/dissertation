from os import listdir

import tika, tika.parser as parser
import string
import re

class PdfParser():
  gradesSubjectsDirectoryPath = "Resources/Grades/"

  @staticmethod
  def getGradeSubjectsNames(grade):
    return list(map(
      lambda subjectFile: subjectFile.replace('.pdf', ''), PdfParser.getGradeSubjectsFiles(grade)
    ))

  @staticmethod
  def getGradeSubjectsFiles(grade):
    return listdir(PdfParser.gradesSubjectsDirectoryPath + str(grade))

  @staticmethod
  def readSubjectWords(grade, subjectFile):
    filePath = PdfParser.gradesSubjectsDirectoryPath + str(grade) + "/" + subjectFile

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
      if PdfParser.wordIsRemovable(words[i]) or len(words[i])<3:
        del words[i]
      else:
        i += 1

    return words

  @staticmethod
  def wordIsRemovable(inputString):
    return any(c.isdigit() for c in inputString) or re.search('[a-zA-Z]', inputString) or not(any(c.isalpha() for c in inputString))
