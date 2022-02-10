class Styles():
  from MenuBar.settings import Settings
  theme = Settings.get_setting('theme')

  if theme == 'light':
    menu_bar_style = """
      QPushButton:hover { background-color: grey }
      QPushButton { border: none }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: black }"""
  else:
    menu_bar_style = """
      QPushButton:hover { background-color: grey }
      QPushButton { border: none }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: white }"""

  application_icon_style = """QPushButton:hover { background-color: none }"""

  if theme == 'light':
    settings_widget_style = """
      QCheckBox { color: black }
      QRadioButton { color: black }"""
  else:
    settings_widget_style = """
      QWidget { background-color: #171010 }
      QCheckBox { color: white }
      QRadioButton { color: white }"""

  if theme == 'light':
    close_window_button_style = """
      QPushButton:hover { background-color: #D11A2A }"""
  else:
    close_window_button_style = """
      QPushButton:hover { background-color: #D11A2A }"""

  if theme == 'light':
    main_window_style = """
      QWidget { background-color: #F9CF93 }
      QPushButton { background-color: none }"""
  else:
    main_window_style = """
      QWidget { background-color: #2B2B2B }
      QPushButton { background-color: none }"""
      # QWidget { background-color: #E0C097 }

  if theme == 'light':
    main_window_background_style = """
      QWidget { background-color: #FFFAFA }\n
      QPushButton { background-color: none }"""
  else:
    main_window_background_style = """
      QWidget { background-color: #171010 }\n
      QPushButton { background-color: none }"""
      # QWidget { background-color: #5C3D2E }

  if theme == 'light':
    side_widgets_style = """
      QWidget { background-color: #DEDEDE }
      QLabel { color: black }
      QScrollBar { background-color: none }"""
  else:
    side_widgets_style = """
      QWidget { background-color: #362222 }
      QLabel { color: white }
      QScrollBar { background-color: none }"""
      # QWidget { background-color: #2D2424 }

  if theme == 'light':
    side_widgets_title_label_style = """
      QLabel { border : 1px solid black; border-bottom: 0px; padding: 10px 0px; background-color: #F9E4C8; color: #1C1C1C }"""
  else:
    side_widgets_title_label_style = """
      QLabel { border : 1px solid white; border-bottom: 0px; padding: 10px 0px; background-color: #423F3E; color: white }"""
      # QLabel { border : 1px solid black; border-bottom: 0px; padding: 10px 0px; background-color: #B85C38; color: blue }"""

  if theme == 'light':
    item_widgets_style = """
      QWidget { background-color: #FBF7F0 }
      QLabel { color: black }
      QPushButton:hover { background-color: grey }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QPushButton { background-color: none }"""
  else:
    item_widgets_style = """
      QWidget { background-color: #171010 }
      QLabel { color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border: 1px solid white }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QPushButton { background-color: white }"""

  if theme == 'light':
    searching_widget_focused_style = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid blue }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""
  else:
    searching_widget_focused_style = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid blue }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""

  if theme == 'light':
    searching_widget_unfocused_style = """
      QWidget { background-color: white; border-radius: 10px; border: none }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""
  else:
    searching_widget_unfocused_style = """
      QWidget { background-color: white; border-radius: 10px; border: none }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""

  if theme == 'light':
    searching_widget_error_style = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid red }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""
  else:
    searching_widget_error_style = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid red }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""

  if theme == 'light':
    subwidget_style = """
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }"""
  else:
    subwidget_style = """
      QPushButton { border: 1px solid white; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: white }
      QPushButton:hover { background-color: grey }"""

  if theme == 'light':
    error_message_style = """
      QLabel { color: red }
      QLabel { background-color: none }
      QLabel { border: none }"""
  else:
    error_message_style = """
      QLabel { color: red }
      QLabel { background-color: none }
      QLabel { border: none }"""

  if theme == 'light':
    words_editing_widget_style = """
      QWidget { background-color: none }
      QDialog { background-color: #FFFAFA }
      QComboBox { color: black }
      QCheckBox { color: black }
      QRadioButton { color: black }
      QLabel { color: black }"""
  else:
    words_editing_widget_style = """
      QWidget { background-color: none }
      QDialog { background-color: #171010 }
      QComboBox { color: black }
      QCheckBox { color: white }
      QRadioButton { color: white }
      QLabel { color: white }"""
      # QDialog { background-color: #5C3D2E }

  if theme == 'light':
    error_message_labelStyle = """QLabel { color: red }"""
  else:
    error_message_labelStyle = """QLabel { color: red }"""

  if theme == 'light':
    current_search_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }
      QComboBox { color: black }"""
  else:
    current_search_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }
      QComboBox { color: black }"""

  if theme == 'light':
    searched_word_style = """
      QLabel { border: 1px solid black; border-radius: 50%; padding: 0px 50px; background-color: #F9E4C8; color: black }"""
  else:
    searched_word_style = """
      QLabel { border: 1px solid white; border-radius: 50%; padding: 0px 50px; background-color: #423F3E; color: white }"""
      # QLabel { border: 1px solid black; border-radius: 50%; padding: 0px 50px; background-color: #B85C38; color: black }"""

  if theme == 'light':
    student_addition_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }"""
  else:
    student_addition_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }
      QComboBox { color: black }"""

  if theme == 'light':
    student_update_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }"""
  else:
    student_update_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }
      QComboBox { color: black }"""

  if theme == 'light':
    profile_addition_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }"""
  else:
    profile_addition_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }
      QComboBox { color: black }"""

  if theme == 'light':
    profile_update_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }"""
  else:
    profile_update_style = """
      QWidget { background-color: none }
      QPushButton { border: 1px solid black; border-radius: 10px; padding: 5px 50px }
      QPushButton { color: black }
      QPushButton:hover { background-color: grey }
      QComboBox { color: black }"""

  if theme == 'light':
    results_widget_style = """
      QWidget { background-color: #DEDEDE }
      QLabel { color: black }
      QScrollBar { background-color: none }"""
  else:
    results_widget_style = """
      QWidget { background-color: #362222 }
      QLabel { color: white }
      QScrollBar { background-color: none }"""
      # QWidget { background-color: #2D2424 }

  if theme == 'light':
    result_style = """
      QWidget { background-color: white; border-radius: 10px}
      QPushButton { background-color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border-radius: 12px }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: black }"""
  else:
    result_style = """
      QWidget { background-color: black; border-radius: 10px}
      QPushButton { background-color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border-radius: 12px }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: white }"""
