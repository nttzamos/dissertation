from PyQt6.QtGui import QFont

from ItemWidgets.recentSearch import RecentSearch
from MainWidget.result import Result

import pickledb

class Settings():
  settings_database_file = 'MenuBar/settings.json'
  font = QFont().family()

  @staticmethod
  def initialize_settings_database(screen_width, screen_height):
    settings_database = pickledb.load(Settings.settings_database_file, False)

    if not settings_database.get('maximum_results'):
      settings_database.set('maximum_results', 20)

    if not settings_database.get('_last_grade_picked'):
      settings_database.set('_last_grade_picked', 1)

    if not settings_database.get('theme'):
      settings_database.set('theme', 'light')

    if not settings_database.get('default_editing_action'):
      settings_database.set('default_editing_action', 'update')

    if isinstance(settings_database.get('remember_last_grade_picked'), bool):
      settings_database.set('remember_last_grade_picked', 0)

    if isinstance(settings_database.get('ask_before_actions'), bool):
      settings_database.set('ask_before_actions', 1)

    if isinstance(settings_database.get('show_edit_dict_words_button'), bool):
      settings_database.set('show_edit_dict_words_button', 1)

    settings_database.dump()

    Settings.calculate_size_settings(screen_width, screen_height)

  @staticmethod
  def calculate_size_settings(screen_width, screen_height):
    settings_database = pickledb.load(Settings.settings_database_file, False)
    if not settings_database.get('screen_width') == screen_width:
      settings_database.set('screen_width', screen_width)
      settings_database.set('screen_height', screen_height)

      long_recent_search = RecentSearch('WWWWWWWWWWWWWWW', True) # 15
      left_widget_width = long_recent_search.sizeHint().width()
      settings_database.set('left_widget_width', left_widget_width)

      right_widget_width = screen_width - left_widget_width - 2
      settings_database.set('right_widget_width', right_widget_width)

      long_result = Result('WWWWWWWWWW', initial=True) # 10
      single_result_width = long_result.sizeHint().width()
      settings_database.set('single_result_width', single_result_width)

      settings_database.dump()

  @staticmethod
  def get_screen_width():
    settings_database = pickledb.load(Settings.settings_database_file, False)

    return settings_database.get('screen_width')

  @staticmethod
  def get_screen_height():
    settings_database = pickledb.load(Settings.settings_database_file, False)

    return settings_database.get('screen_height')

  @staticmethod
  def get_left_widget_width():
    settings_database = pickledb.load(Settings.settings_database_file, False)

    return settings_database.get('left_widget_width')

  @staticmethod
  def get_right_widget_width():
    settings_database = pickledb.load(Settings.settings_database_file, False)

    return settings_database.get('right_widget_width')

  @staticmethod
  def get_single_result_width():
    settings_database = pickledb.load(Settings.settings_database_file, False)

    return settings_database.get('single_result_width')

  @staticmethod
  def get_results_widget_columns():
    settings_database = pickledb.load(Settings.settings_database_file, False)
    results_widget_columns = settings_database.get('right_widget_width') // (settings_database.get('single_result_width') + 10)

    return results_widget_columns

  @staticmethod
  def set_maximum_results(maximum_results):
    settings_database = pickledb.load(Settings.settings_database_file, False)
    settings_database.set('maximum_results', maximum_results)
    settings_database.dump()

  @staticmethod
  def get_maximum_results():
    settings_database = pickledb.load(Settings.settings_database_file, False)

    return settings_database.get('maximum_results')

  @staticmethod
  def set_boolean_setting(setting_name, new_value):
    settings_database = pickledb.load(Settings.settings_database_file, False)
    settings_database.set(setting_name, 1 if new_value else 0)
    settings_database.dump()

  @staticmethod
  def get_boolean_setting(setting_name):
    settings_database = pickledb.load(Settings.settings_database_file, False)

    return settings_database.get(setting_name) == 1

  @staticmethod
  def set_theme(theme):
    settings_database = pickledb.load(Settings.settings_database_file, False)
    settings_database.set('theme', theme)
    settings_database.dump()

  @staticmethod
  def get_theme():
    settings_database = pickledb.load(Settings.settings_database_file, False)

    return settings_database.get('theme')

  @staticmethod
  def set_default_editing_action(default_editing_action):
    settings_database = pickledb.load(Settings.settings_database_file, False)
    settings_database.set('default_editing_action', default_editing_action)
    settings_database.dump()

  @staticmethod
  def get_default_editing_action():
    settings_database = pickledb.load(Settings.settings_database_file, False)

    return settings_database.get('default_editing_action')

    # Fun Experiment
    # chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # print(len(chars)); max = 0; max_char = 'a'; sizes = []
    # for char in chars:
    #   str = ''
    #   for i in range(10): str = str + char; size = Result(str).sizeHint().width()
    #   if size > max: max = size; max_char = char
    #   sizes.append(size)

    # print(max); print(max_char); print(sizes)
