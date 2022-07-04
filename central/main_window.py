from PyQt6.QtWidgets import QSplitter, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from central.main_widget import MainWidget
from menu.settings import Settings
from models.profile import get_profile_name
from side.recent_searches_widget import RecentSearchesWidget
from side.starred_words_widget import StarredWordsWidget

import gettext

language_code = Settings.get_setting('language')
language = gettext.translation('search', localedir='resources/locale', languages=[language_code])
language.install()
_ = language.gettext

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()

    self.setWindowIcon(QIcon('resources/window_icon.png'))
    self.setWindowTitle('Wordinary')

    self.layout = QVBoxLayout(self)
    self.layout.setSpacing(0)
    self.layout.setContentsMargins(0, 0, 0, 0)

    vertical_splitter = QSplitter()
    vertical_splitter.setOrientation(Qt.Orientation.Vertical)
    vertical_splitter.setChildrenCollapsible(True)

    MainWindow.recent_searches_widget = RecentSearchesWidget()
    MainWindow.starred_words_widget = StarredWordsWidget()

    MainWindow.recent_searches_widget.initialize()
    MainWindow.starred_words_widget.initialize()

    vertical_splitter.addWidget(MainWindow.recent_searches_widget)
    vertical_splitter.addWidget(MainWindow.starred_words_widget)

    horizontal_splitter = QSplitter()
    horizontal_splitter.setOrientation(Qt.Orientation.Horizontal)
    horizontal_splitter.setChildrenCollapsible(True)

    MainWindow.main_widget = MainWidget()

    horizontal_splitter.addWidget(vertical_splitter)
    horizontal_splitter.addWidget(MainWindow.main_widget)
    horizontal_splitter.setCollapsible(1, False)

    self.main_window_widget = QWidget(self)
    self.main_window_widget.layout = QHBoxLayout(self.main_window_widget)
    self.main_window_widget.layout.setContentsMargins(0, 0, 0, 0)
    self.main_window_widget.layout.setSpacing(0)
    self.main_window_widget.layout.addWidget(horizontal_splitter)

    self.layout.addWidget(self.main_window_widget)

    self.style()

  def style(self):
    from shared.styles import Styles
    self.main_window_widget.setStyleSheet(Styles.main_window_background_style)
    self.setStyleSheet(Styles.main_window_style)

  @staticmethod
  def update_widgets(profile_id, subject_name):
    from search.searching_widget import SearchingWidget
    from central.results_widget import ResultsWidget

    # Ορισμός του μηνύματος σφάλματος της μπάρας ανάλογα με το αν έχει
    # επιλεχτεί ένα συγκεκριμένο μάθημα ή όλα τα μαθήματα ενός προφίλ.
    if subject_name == _('ALL_SUBJECTS_TEXT'):
      SearchingWidget.modify_error_message(get_profile_name(profile_id), False)
    else:
      SearchingWidget.modify_error_message(subject_name, True)

    # Ανανέωση του συνόλου των λέξεων από τις οποίες ο χρήστης μπορεί να
    # επιλέξει κάποια για να αναζητήσει την οικογένεια της.
    SearchingWidget.update_selected_dictionary()

    # Εμφάνιση του λεκτικού του πάνελ των αποτελεσμάτων που ενημερώνει για
    # για την λειτουργικότητα του.
    ResultsWidget.show_placeholder()

    # Αρχικοποίηση των λιστών των πρόσφατων αναζητήσεων και των αγαπημένων
    # λέξεων με βάση τα επιλεγμένα φίλτρα.
    RecentSearchesWidget.populate()
    StarredWordsWidget.populate()

    # Ανανέωση του λεκτικού του πλαισίου της τωρινής αναζήτησης.
    MainWidget.current_search.searched_word_label.setText(_('ENTER_WORD_TEXT'))

  @staticmethod
  def clear_previous_filters_details():
    # Τερματισμός της μεθόδοου στην περίπτωση που προηγουμένως δεν ήταν
    # επιλεγμένο κάποιο μάθημα καθώς αυτό σημαίνει πως τα εκάστοτε widgets
    # δεν περιείχαν κάποια πληροφορία μιας και δεν είχαν επιλεχτεί τιμές για
    # όλα τα φίλτρα αναζήτησης (αφού η τιμή του μαθήματος επιλέγεται τελευταία).
    from search.current_search import CurrentSearch
    if not CurrentSearch.subject_selector_active: return

    from search.searching_widget import SearchingWidget
    from central.results_widget import ResultsWidget

    CurrentSearch.subject_selector_active = False

    # Καθαρισμός του συνόλου των λέξεων που μπορούν να αναζητηθούν στην μπάρα.
    SearchingWidget.dictionary_words = []
    SearchingWidget.completer.setModel(None)

    # Αρχικοποίηση του μηνύματος σφάλματος της μπάρας αναζήτησης.
    SearchingWidget.set_initial_error_message()

    # Εμφάνιση του λεκτικού του πάνελ των αποτελεσμάτων που ενημερώνει για
    # για την λειτουργικότητα του.
    ResultsWidget.show_placeholder()

    # Καθαρισμός των δεδομένων των λιστών των πρόσφατων αναζητήσεων και των
    # αγαπημένων λέξεων.
    RecentSearchesWidget.clear_previous_recent_searches()
    StarredWordsWidget.clear_previous_starred_words()
