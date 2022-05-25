from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from shared.font_settings import FontSettings

import gettext

class RecentSearch(QWidget):
  def __init__(self, word, is_starred):
    super().__init__()

    from menu.settings import Settings
    language_code = Settings.get_setting('language')
    language = gettext.translation('item', localedir='resources/locale', languages=[language_code])
    language.install()
    _ = language.gettext

    self.setFixedHeight(50)

    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    font = FontSettings.get_font('single_word')

    data_widget = QWidget()
    data_widget.layout = QHBoxLayout(data_widget)
    data_widget.layout.setContentsMargins(0, 0, 0, 0)
    data_widget.layout.setSpacing(5)

    self.word = QLabel(word)
    self.word.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    self.word.setFont(font)

    edit_button = QPushButton()
    edit_button.setIcon(QIcon('resources/edit.svg'))
    edit_button.setToolTip(_('EDIT_TEXT'))
    edit_button.clicked.connect(self.edit_word)
    edit_button.setFixedWidth(30)

    reload_button = QPushButton()
    reload_button.setIcon(QIcon('resources/search.png'))
    reload_button.setToolTip(_('RELOAD_TEXT'))
    reload_button.clicked.connect(self.reload_word)
    reload_button.setFixedWidth(30)

    self.star_button = QPushButton()
    self.star_button.setToolTip(_('STAR_TEXT'))
    self.star_button.clicked.connect(self.toggle_starred_state)
    self.star_button.setFixedWidth(30)

    self.is_starred = is_starred
    if self.is_starred:
      self.star_button.setIcon(QIcon('resources/starred.svg'))
    else:
      self.star_button.setIcon(QIcon('resources/unstarred.svg'))

    delete_button = QPushButton()
    delete_button.setIcon(QIcon('resources/delete.svg'))
    delete_button.setToolTip(_('DELETE_TEXT'))
    delete_button.clicked.connect(self.remove_word)
    delete_button.setFixedWidth(30)

    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Plain)

    data_widget.layout.addSpacing(5)
    data_widget.layout.addWidget(self.word)
    data_widget.layout.addWidget(edit_button)
    data_widget.layout.addWidget(reload_button)
    data_widget.layout.addWidget(self.star_button)
    data_widget.layout.addWidget(delete_button)
    data_widget.layout.addSpacing(10)

    self.layout.addWidget(data_widget)
    self.layout.addWidget(line)

    self.set_texts()
    self.style()

  def set_texts(self):
    pass

  def style(self):
    from shared.styles import Styles
    self.setStyleSheet(Styles.item_widgets_style)

  def edit_word(self):
    from dialogs.word_editing_widget import WordEditingWidget
    from search.current_search import CurrentSearch

    word_editing_dialog = WordEditingWidget()
    word_editing_dialog.set_current_tab_index(1)
    word_editing_dialog.set_word_to_update(self.word.text(), CurrentSearch.grade_id)
    word_editing_dialog.exec()

  def reload_word(self):
    word = self.word.text()

    from central.main_widget import MainWidget
    from side.recent_searches_widget import RecentSearchesWidget
    MainWidget.search_word(word)
    RecentSearchesWidget.remove_and_add_recent_search(word)

    from models.recent_search import create_recent_search
    create_recent_search(word)

  def toggle_starred_state(self):
    from side.starred_words_widget import StarredWordsWidget
    word = self.word.text()

    from models.starred_word import create_starred_word, destroy_starred_word
    if self.is_starred:
      destroy_starred_word(word)
      StarredWordsWidget.toggle_starred_word_starred_state(word)
    else:
      create_starred_word(word)
      StarredWordsWidget.add_starred_word(word)

    self.toggle_starred_icon()

  def toggle_starred_icon(self):
    if self.is_starred:
      self.is_starred = False
      self.star_button.setIcon(QIcon('resources/unstarred.svg'))
    else:
      self.is_starred = True
      self.star_button.setIcon(QIcon('resources/starred.svg'))

  def remove_word(self):
    from side.recent_searches_widget import RecentSearchesWidget
    RecentSearchesWidget.remove_recent_search(self)

    from models.recent_search import destroy_recent_search
    destroy_recent_search(self.word.text())

    self.hide()
    self.deleteLater()

  def update_word(self, new_word):
    self.word.setText(new_word)
