from shared.database_handler import get_words
from shared.pdf_parser import PdfParser
from os import listdir
import re
from models.word import destroy_word

def show_statistics(minimum_length=15, show_details=False):
  for grade in range(1, 7):
    saved_words = get_words(grade, grade, 'Όλα τα μαθήματα')
    long_words = []

    for word in saved_words:
      if len(word) > minimum_length:
        long_words.append(word)

    print(str(len(long_words)) + ' out of ' + str(len(saved_words)))
    print(100 * (len(long_words) / len(saved_words)))
    print()

    if show_details:
      print(long_words)
      print()

def destroy_long_words(minimum_length):
  valid_words = [
    'συγχρηματοδοτούμενος', 'ηλεκτροκαρδιογράφημα', 'κλειδαροαμπαρωμένες',
    'αλληλοσυμπληρώνομαι', 'καρδιοαναπνευστικός', 'κωνσταντινουπολίτης',
    'περιβαλλοντολογικός', 'συμπεριλαμβανόμενος', 'απομαγνητοφωνημένος',
    'τζιτζιμιτζιχότζιρας', 'δευτερολεπτοδείκτης','κακομεταχειρίζομαι',
    'χριστουγεννιάτικος', 'αγριοτριανταφυλλιά', 'αλληλοεξουδετερώνω',
    'αλληλοκατηγορούμαι', 'αντιπεριφερειάρχης', 'αποτελεσματικότητα',
    'διαπολιτισμικότητα', 'ευαισθητοποιημένος', 'καταστενοχωρημένος',
    'καταταλαιπωρημένος', 'κοινωνικοποιημένος', 'πρωτοεμφανιζόμενος',
    'τηλεκατευθυνόμενος', 'ηλεκτρομαγνητισμός', 'πετρελαιοπαραγωγός',
    'πρωτοδημοσιευμένος', 'ρωμαιοκαθολικισμός', 'υπερπροστατευτικός'
  ]

  for grade in range(1, 7):
    saved_words = get_words(grade, grade, 'Όλα τα μαθήματα')

    for word in saved_words:
      if len(word) > minimum_length and not word in valid_words:
        destroy_word(word, [grade])

def fix_conjoined_words(show_details=False):
  for grade in range(1, 7):
    saved_words = get_words(grade, grade, 'Όλα τα μαθήματα')

    grade_directory_path = 'processed/subjects' + str(grade) + '/'
    files_list = listdir(grade_directory_path)
    files_list.sort()
    words_set = set()
    current_subject_words = set()

    for file in files_list:
      if file == '.DS_Store' or 'processerror' in file:
        print('error' + str(file))
        continue

      file_contents = open(grade_directory_path + file, 'r')
      file_lines = file_contents.readlines()
      for i in range(len(file_lines)):
        line = file_lines[i]
        line = line.strip()
        if line.startswith('<types:Lemma'):
          result = re.search('value="(.*)"/>', line)
          current_subject_words.add(result.group(1))

          if result.group(1) == 'YOU_HAVE_REACHED_THE_END_OF_A_SUBJECT':
            current_subject_words = list(set(PdfParser.clean_words(list(current_subject_words))))
            words_set = words_set | set(current_subject_words)
            current_subject_words = set()

    words_to_remove = list(set(saved_words) - words_set)
    words_to_remove.sort()
    words_to_add = list(words_set - set(saved_words))
    words_to_add.sort()

    for word in words_to_remove:
      destroy_word(word, [grade])

    if show_details:
      print('\nWORDS TO REMOVE FOR GRADE ' + str(grade))
      print('------------------------------------------------------')
      print(words_to_remove)
      print('------------------------------------------------------\n')
      # print('\nWORDS TO ADD FOR GRADE ' + str(grade))
      # print('------------------------------------------------------')
      # print(words_to_add)
      # print('------------------------------------------------------\n')

show_statistics(15, show_details=False)
fix_conjoined_words(show_details=False)
destroy_long_words(17)
print('------------------------------------------------------\n')
show_statistics(15, show_details=False)
