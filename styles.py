class Styles():
  from settings import Settings
  theme = Settings.getTheme()
  if theme == 'light':
    sideWidgetsStyle = """
      QWidget { background-color: #DEDEDE }
      QLabel { color: black }
      QScrollBar { background-color: none }"""
  else:
    sideWidgetsStyle = """
      QWidget { background-color: black }
      QLabel { color: white }
      QScrollBar { background-color: none }"""

  if theme == 'light':
    sideWidgetsTitleLabelStyle = """
      QLabel { border : 1px solid black; border-bottom: 0px; padding: 10px 0px; background-color: #F9E4C8; color: #1C1C1C }"""
  else:
    sideWidgetsTitleLabelStyle = """
      QLabel { border : 1px solid black; border-bottom: 0px; padding: 10px 0px; background-color: white; color: blue }"""

  if theme == 'light':
    itemWidgetsStyle = """
      QPushButton:hover { background-color: grey }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: black }
      QWidget { background-color: #FBF7F0 }"""
  else:
    itemWidgetsStyle = """
      QPushButton:hover { background-color: grey }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: white }
      QWidget { background-color: green }"""

  if theme == 'light':
    titleBarStyle = """
      QPushButton:hover { background-color: grey }
      QPushButton { border: none }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: black }"""
  else:
    titleBarStyle = """
      QPushButton:hover { background-color: grey }
      QPushButton { border: none }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: white }"""

  if theme == 'light':
    resultsWidgetStyle = """
      QWidget { background-color: #DEDEDE }
      QLabel { color: black }
      QScrollBar { background-color: none }"""
  else:
    resultsWidgetStyle = """
      QWidget { background-color: blue }
      QLabel { color: white }
      QScrollBar { background-color: none }"""

  if theme == 'light':
    resultStyle = """
      QWidget { background-color: white; border-radius: 10px}
      QPushButton { background-color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border-radius: 12px }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: black }"""
  else:
    resultStyle = """
      QWidget { background-color: white; border-radius: 10px}
      QPushButton { background-color: white }
      QPushButton:hover { background-color: grey }
      QPushButton { border-radius: 12px }
      QPushButton { border: 1px solid black }
      QPushButton { padding-bottom: 5px }
      QPushButton { padding-top: 5px }
      QLabel { color: blue }"""

  if theme == 'light':
    currentSearchStyle = """
      QWidget { background-color: none }
      QComboBox { color: black }"""
  else:
    currentSearchStyle = """
      QWidget { background-color: none }
      QComboBox { color: blue }"""

  if theme == 'light':
    searchingWidgetFocusedStyle = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid blue }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""
  else:
    searchingWidgetFocusedStyle = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid blue }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""

  if theme == 'light':
    searchingWidgetUnfocusedStyle = """
      QWidget { background-color: white; border-radius: 10px; border: none }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""
  else:
    searchingWidgetUnfocusedStyle = """
      QWidget { background-color: white; border-radius: 10px; border: none }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""

  if theme == 'light':
    searchingWidgetErrorStyle = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid red }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""
  else:
    searchingWidgetErrorStyle = """
      QWidget { background-color: white; border-radius: 10px; border: 1px solid red }
      QLineEdit { border: none }
      QPushButton { background-color: none }
      QPushButton { border: none }
      QPushButton { padding-bottom: 8px }
      QPushButton { padding-top: 8px }"""

  if theme == 'light':
    mainWindowStyle = """
      QWidget { background-color: #F9CF93 }
      QPushButton { background-color: none }"""
  else:
    mainWindowStyle = """
      QWidget { background-color: red }
      QPushButton { background-color: none }"""

  if theme == 'light':
    wordsEditingWidgetStyle = """
      QWidget { background-color: none }
      QDialog { background-color: #FFFAFA }
      QComboBox { color: black }
      QLabel { color: black }"""
  else:
    wordsEditingWidgetStyle = """
      QWidget { background-color: none }
      QDialog { background-color: yellow }
      QComboBox { color: blue }
      QLabel { color: red }"""
