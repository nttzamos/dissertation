from item.recent_search import RecentSearch

import pickledb

class Settings():
  SETTINGS_DATABASE_FILE = 'resources/settings.json'
  LANGUAGES = {
    'Ελληνικά': 'el',
    'English': 'en'
  } # If you wish to add more languages, modify this dictionary accordingly

  @staticmethod
  def initialize_settings_database(screen_width, screen_height):
    settings_default_values = {
      'maximum_results': 30,
      'last_student_picked': 1,
      'theme': 'light',
      'updated_language': 'el',
      'updated_selected_font': 'medium'
    }

    boolean_settings_default_values = {
      'remember_last_student_picked': 0,
      'ask_before_actions': 1,
      'show_edit_dict_words_button': 1,
      'only_show_words_with_family': 0,
      'show_tutorial_on_startup': 1,
      'use_wiktionary': 1,
      'show_unsaved_changes_message': 1
    }

    boolean_settings_about_hiding_messages = [
      'hide_no_internet_message', 'hide_theme_change_effect_message',
      'hide_delete_profile_message', 'hide_delete_student_message',
      'hide_delete_word_message', 'hide_language_change_effect_message',
      'hide_remove_word_from_family_message',
      'hide_font_size_change_effect_message'
    ]

    for key, value in settings_default_values.items():
      if not Settings.get_setting(key):
        Settings.set_setting(key, value)

    for key, value in boolean_settings_default_values.items():
      if isinstance(Settings.get_setting(key), bool):
        Settings.set_setting(key, value)

    for key in boolean_settings_about_hiding_messages:
      Settings.set_setting(key, 0)

    Settings.set_setting('language', Settings.get_setting('updated_language'))
    Settings.set_setting('selected_font', Settings.get_setting('updated_selected_font'))

    from shared.font_settings import FontSettings
    FontSettings.set_selected_font(Settings.get_setting('selected_font'))

    Settings.calculate_size_settings(screen_width, screen_height)

  @staticmethod
  def calculate_size_settings(screen_width, screen_height):
    settings_database = pickledb.load(Settings.SETTINGS_DATABASE_FILE, False)
    if not settings_database.get('screen_width') == screen_width:
      settings_database.set('screen_width', screen_width)
      settings_database.set('screen_height', screen_height)

      long_recent_search = RecentSearch('ωωωωωωωωωωωωωωω', True) # 15
      left_widget_width = long_recent_search.sizeHint().width()
      settings_database.set('left_widget_width', left_widget_width)

      settings_database.dump()

  @staticmethod
  def set_boolean_setting(setting_name, setting_value):
    Settings.set_setting(setting_name, 1 if setting_value else 0)

  @staticmethod
  def get_boolean_setting(setting_name):
    return Settings.get_setting(setting_name) == 1

  @staticmethod
  def set_setting(setting_name, setting_value):
    settings_database = pickledb.load(Settings.SETTINGS_DATABASE_FILE, False)
    settings_database.set(setting_name, setting_value)
    settings_database.dump()

  @staticmethod
  def get_setting(setting_name):
    settings_database = pickledb.load(Settings.SETTINGS_DATABASE_FILE, False)

    return settings_database.get(setting_name)

  @staticmethod
  def get_available_languages():
    return list(Settings.LANGUAGES.keys())

  @staticmethod
  def set_language(language):
    Settings.set_setting('updated_language', Settings.LANGUAGES[language])

  @staticmethod
  def get_language():
    selected_language_code = Settings.get_setting('language')
    for language_name, language_code in Settings.LANGUAGES.items():
      if language_code == selected_language_code:
        return language_name

