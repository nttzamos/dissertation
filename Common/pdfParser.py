from os import listdir

import tika, tika.parser as parser
import re

class PdfParser():
  gradesSubjectsDirectoryPath = "Resources/Grades/"

  validCharacters = [
    912, 940, 941, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955,
    956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970,
    971, 972, 974, 943, 942, 973,
    7936, 7937, 7940, 7941, 7952, 7953, 7956, 7957, 7968, 7969, 7972, 7973,
    7974, 7984, 7985, 7988, 7989, 7990, 7991, 8000, 8001, 8004, 8005, 8016,
    8017, 8020, 8021, 8023, 8032, 8033, 8038, 8048, 8049, 8050, 8051, 8052,
    8053, 8054, 8055, 8056, 8057, 8058, 8059, 8060, 8061, 8115, 8118, 8131,
    8134, 8135, 8147, 8150, 8164, 8165, 8166, 8179, 8182, 8183
  ]

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

    return PdfParser.cleanWords(pdf.split())

  @staticmethod
  def cleanWords(words):
    for i in range(len(words)):
      words[i] = words[i].lower()
      words[i] = re.sub(r'[^\w\s]', '', words[i])

    words = PdfParser.fixLetterAsciiValue(words)

    i = 0
    while i < len(words):
      if PdfParser.wordIsRemovable(words[i]):
        del words[i]
      else:
        i += 1

    return words

  @staticmethod
  def fixLetterAsciiValue(words):
    table = { 181: 956 }

    return list(map(lambda word: word.translate(table), words))

  @staticmethod
  def wordIsRemovable(word):
    if len(word) < 3:
      return True

    for character in word:
      if not ord(character) in PdfParser.validCharacters:
        return True

    return False
