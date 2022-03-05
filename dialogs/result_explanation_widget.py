from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QLabel, QGroupBox, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

from menu.settings import Settings

class ResultExplanationWidget(QDialog):
  DIALOG_TITLE = 'Αποτελέσματα'
  CLOSE_BUTTON_TEXT = 'Κλείσιμο'
  RESULT_EXPLANATION_TITLE = 'Επεξήγηση Αποτελεσμάτων'
  RESULT_EXPLANATION_TEXT = (
    'Οι συγγενικές λέξεις που ανήκουν σε κάποιο βιβλίο της τάξης '
    'του επιλεγμένου προφίλ εμφανίζονται μέσα σε ένα μαύρο πλάισιο.\n\nΛέξεις '
    'τις οποίες επιστρέφει το Wiktionary ως συγγενικές, της λέξης που αναζητήθηκε '
    'μόλις, αλλά οι οποίες δεν υπάρχουν σε κάποιο βιβλίο της τάξης του '
    'επιλεγμένου προφίλ, παρουσιάζονται μέσα σε ένα μπλε πλαίσιο.\n\n Σε '
    'αυτές τις λέξεις, το κουμπί με το σύμβολο της πρόσθεσης έχει ως '
    'αποτέλεσμα την προσθήκη της εκάστοτε λέξης στο λεξιλόγιο των επιλεγμένων '
    'βιβλίων.'
  )

  def __init__(self):
    super().__init__()
    self.setWindowTitle(ResultExplanationWidget.DIALOG_TITLE)
    self.setWindowIcon(QIcon('resources/window_icon.png'))

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(20, 10, 20, 10)
    self.layout.setSpacing(10)

    self.setFixedHeight(300)
    self.setFixedWidth(750)

    section_label_font = QFont(Settings.font, 20)
    text_font = QFont(Settings.font, 16)

    self.group_box_widget = QGroupBox(ResultExplanationWidget.RESULT_EXPLANATION_TITLE)
    self.group_box_widget.setFont(section_label_font)
    self.group_box_widget.layout = QHBoxLayout(self.group_box_widget)
    self.group_box_widget.layout.setContentsMargins(0, 0, 0, 0)

    explanation = QLabel(ResultExplanationWidget.RESULT_EXPLANATION_TEXT)
    explanation.setWordWrap(True)
    explanation.setFont(text_font)

    self.group_box_widget.layout.addWidget(explanation, alignment=Qt.AlignmentFlag.AlignTop)

    self.close_tutorial_button = QPushButton(ResultExplanationWidget.CLOSE_BUTTON_TEXT)
    self.close_tutorial_button.adjustSize()
    self.close_tutorial_button.pressed.connect(self.close)
    self.close_tutorial_button.setAutoDefault(False)

    self.layout.addWidget(self.group_box_widget)
    self.layout.addWidget(self.close_tutorial_button, alignment=Qt.AlignmentFlag.AlignRight)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.tutorial_widget_style)
