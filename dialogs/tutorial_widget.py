from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QLabel, QGroupBox, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

from menu.settings import Settings

class TutorialWidget(QDialog):
  TITLES = [
    'Εισαγωγή στο Wordinary', 'Μαθητές', 'Προφίλ', 'Μαθήματα', 'Αποτελέσματα'
  ]

  APPLICATION_INTRODUCTION = (
    'Καλώς ήρθατε στο Wordinary! Μια εφαρμογή που βοηθά μαθητές Δημοτικού να '
    'μάθουν ευκολότερα τις συγγενικές λέξεις των λέξεων που ανήκουν στα βιβλία '
    'τους.\n\nΓια να χρησιμοποιήσετε την εφαρμογή, πρέπει να επιλέξετε έναν μαθητή, '
    'ένα προφίλ του συγκεκριμένου μαθητή και ένα ή όλα τα μαθήματα του συγκεκριμένου '
    'προφίλ.\n\nΗ εφαρμογή χρησιμοποιεί το Wiktionary (https://el.wiktionary.org/) '
    'προκειμένουν να εντοπίσει τις συγγενικές λέξεις των λέξεων που αναζητά ο χρήστης.'
    '\n\nΤα αποτελέσματα της αναζήτησης εμφανίζονται στο κάτω μέρος της εφαρμογής.'
  )

  STUDENT_EXPLANATION = (
    'Μπορείτε να δημιουργήσετε μαθητές, οι οποίοι αντιστοιχούν ουσιαστικά στους '
    'πραγματικούς σας μαθητές, έτσι ώστε να διαφοροποιήσετε δεδομένα τους, όπως '
    'τα προφίλ τους, τις αναζητήσεις αλλά και τις αγαπημένες τους λέξεις.\n\n'
    'Μπορείτε να δημιουργήσετε νέους μαθητές ή να επεξεργαστείτε τους υπάρχοντες '
    'πατώντας το κουμπί "Επεξεργασία Δεδομένων" που βρίσκεται στο δεξί μέρος της '
    'εφαρμογής.'
  )

  PROFILE_EXPLANATION = (
    'Τα προφίλ ανήκουν σε μια συγκεκριμένη τάξη και περιέχουν ένα σύνολο των '
    'μαθημάτων αυτής της τάξης.\n\nΥπάρχουν 6 προκαθορισμένα προφίλ (ένα για κάθε '
    'τάξη του δημοτικού) που περιέχουν όλα τα μαθήματα της εκάστοτε τάξης, και τα '
    'οποία δεν μπορούν να μεταβληθούν ή να διαγραφούν.\n\nΜπορείτε να δημιουργήσετε '
    'νέα προφίλ ή να επεξεργαστείτε τα υπάρχοντα πατώντας το κουμπί "Επεξεργασία '
    'Δεδομένων" που βρίσκεται στο δεξί μέρος της εφαρμογής.'
  )

  SUBJECT_EXPLANATION = (
    'Όπως έχετε καταλάβει ήδη, κάθε προφίλ αποτελείται από πολλαπλά μαθήματα.\n\n'
    'Τα μάθηματα που επιλέγετε ορίζουν το σύνολο λέξεων από το οποίο μπορείτε να '
    'αναζητήσετε μια λέξη από την μπάρα αναζήτησης που βρίσκεται στο πάνω μέρος '
    'της εφαρμογής. Επίσης, οι πρόσφατες αναζητήσεις και οι αγαπημένες λέξεις '
    'αντιστοιχούν στην εκάστοτε επιλεγμένη τάξη.\n\nΗ επιλογή μαθήματος δεν '
    'περιορίζει ωστόσο τα αποτελέσματα που θα εμφανιστούν. Τα αποτελέσματα '
    'περιορίζονται μόνο από την τάξη στην οποία ανήκει το επιλεγμένο μάθημα '
    '(ή μαθήματα).\n\nΔηλαδή, η επιλογή ενός συγκεκριμένου μαθήματος δεν '
    'περιορίζει το γεγονός, πως στα αποτελέσματα θα ανήκουν λέξεις από όλα '
    'τα μαθήματα της εκάστοτε τάξης του μαθήματος.'
  )

  RESULT_EXPLANATION = (
    'Τα αποτελέσματα της αναζήτησης του χρήστη εμφανίζονται στο κάτω μέρος της '
    'εφαρμογής.\n\nΟι συγγενικές λέξεις που ανήκουν σε κάποιο βιβλίο της τάξης '
    'του επιλεγμένου βιβλίου εμφανίζονται χωρίς πλάισιο. Λέξεις τις οποίες '
    'επιστρέφει το Wiktionary ως συγγενικές της λέξης που αναζητήθηκε μόλις, '
    'αλλά οι οποίες δεν υπάρχουν σε κάποιο βιβλίο της τάξης του επιλεγμένου '
    'μαθήματος, παρουσιάζονται μέσα σε ένα μπλε πλαίσιο.'
  )

  TEXTS = [
    APPLICATION_INTRODUCTION, STUDENT_EXPLANATION, PROFILE_EXPLANATION,
    SUBJECT_EXPLANATION, RESULT_EXPLANATION
  ]

  DIALOG_TITLE = 'Οδηγίες'
  CHECK_BOX_TEXT = 'Εμφανισή οδηγιών κατά την εκκίνηση'
  CLOSE_BUTTON_TEXT = 'Κλείσιμο'
  PREVIOUS_BUTTON_TEXT = 'Προηγούμενο'
  NEXT_BUTTON_TEXT = 'Επόμενο'

  def __init__(self):
    super().__init__()
    self.setWindowTitle(TutorialWidget.DIALOG_TITLE)
    self.setWindowIcon(QIcon('resources/window_icon.png'))

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(0)

    self.setFixedHeight(400)
    self.setFixedWidth(750)

    section_label_font = QFont(Settings.font, 20)
    text_font = QFont(Settings.font, 16)

    self.current_tutorial = 0

    self.group_box_widget = QGroupBox()
    self.group_box_widget.setFont(section_label_font)
    self.group_box_widget.layout = QHBoxLayout(self.group_box_widget)
    self.group_box_widget.layout.setContentsMargins(0, 0, 0, 0)

    self.explanation = QLabel()
    self.explanation.setWordWrap(True)
    self.explanation.setFont(text_font)

    self.group_box_widget.layout.addWidget(self.explanation, alignment=Qt.AlignmentFlag.AlignTop)

    buttons_widget = QWidget()
    buttons_widget.layout = QHBoxLayout(buttons_widget)
    buttons_widget.layout.setSpacing(5)

    self.setting_check_box = QCheckBox(TutorialWidget.CHECK_BOX_TEXT)
    self.setting_check_box.clicked.connect(self.toggle_tutorial_setting)
    if Settings.get_setting('show_tutorial_on_startup'):
      self.setting_check_box.setChecked(True)

    self.next_tutorial_button = QPushButton(TutorialWidget.NEXT_BUTTON_TEXT)
    self.next_tutorial_button.adjustSize()
    self.next_tutorial_button.pressed.connect(self.next_tutorial)

    self.previous_tutorial_button = QPushButton(TutorialWidget.PREVIOUS_BUTTON_TEXT)
    self.previous_tutorial_button.adjustSize()
    self.previous_tutorial_button.pressed.connect(self.previous_tutorial)
    self.previous_tutorial_button.setDisabled(True)

    self.close_tutorial_button = QPushButton(TutorialWidget.CLOSE_BUTTON_TEXT)
    self.close_tutorial_button.adjustSize()
    self.close_tutorial_button.pressed.connect(self.close)

    buttons_widget.layout.addWidget(self.setting_check_box, alignment=Qt.AlignmentFlag.AlignLeft)
    buttons_widget.layout.addWidget(self.close_tutorial_button, alignment=Qt.AlignmentFlag.AlignRight)
    buttons_widget.layout.addWidget(self.previous_tutorial_button)
    buttons_widget.layout.addWidget(self.next_tutorial_button)

    self.layout.addWidget(self.group_box_widget)
    self.layout.addWidget(buttons_widget, alignment=Qt.AlignmentFlag.AlignBottom)

    self.update_tutorial()

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.tutorial_widget_style)

  def next_tutorial(self):
    if self.current_tutorial < len(TutorialWidget.TEXTS) - 1:
      self.current_tutorial += 1
      self.update_tutorial()

    if self.current_tutorial == len(TutorialWidget.TEXTS) - 1:
      self.next_tutorial_button.setDisabled(True)
    elif self.current_tutorial == 1:
      self.previous_tutorial_button.setEnabled(True)

  def previous_tutorial(self):
    if self.current_tutorial > 0:
      self.current_tutorial -= 1
      self.update_tutorial()

    if self.current_tutorial == 0:
      self.previous_tutorial_button.setDisabled(True)
    elif self.current_tutorial == len(TutorialWidget.TEXTS) - 2:
      self.next_tutorial_button.setEnabled(True)

  def update_tutorial(self):
    counter_text = (' (' + str(self.current_tutorial + 1) + '/' +
      str(len(TutorialWidget.TEXTS)) + ')'
    )
    self.group_box_widget.setTitle(TutorialWidget.TITLES[self.current_tutorial] + counter_text)
    self.explanation.setText(TutorialWidget.TEXTS[self.current_tutorial])

  def toggle_tutorial_setting(self):
    Settings.set_boolean_setting('show_tutorial_on_startup', self.setting_check_box.isChecked())
