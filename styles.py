class Styles():
  sideWidgetsStyle = """
    QWidget { background-color: black }
    QLabel { color: white }
    QScrollBar { background-color: none }"""

  titleBarStyle = """
    QPushButton:hover { background-color: grey }
    QPushButton { border: none }
    QPushButton { padding-bottom: 5px }
    QPushButton { padding-top: 5px }
    QLabel { color: white }"""

  itemWidgetsStyle = """
    QPushButton:hover { background-color: grey }
    QPushButton { border: 1px solid black }
    QPushButton { padding-bottom: 5px }
    QPushButton { padding-top: 5px }
    QLabel { color: white }
    QWidget { background-color: green }"""

  resultsWidgetStyle = """
    QWidget { background-color: blue }
    QLabel { color: white }
    QScrollBar { background-color: none }"""

  resultStyle = """
    QWidget { background-color: white; border-radius: 10px}
    QPushButton { background-color: white }
    QPushButton:hover { background-color: grey }
    QPushButton { border-radius: 12px }
    QPushButton { border: 1px solid black }
    QPushButton { padding-bottom: 5px }
    QPushButton { padding-top: 5px }
    QLabel { color: blue }"""

  currentSearchStyle = """
    QComboBox { background-color: none }
    QComboBox { color: blue }
    QWidget { background-color: none }"""

  searchingWidgetFocusedStyle = """
    QWidget { background-color: white; border-radius: 10px; border: 1px solid blue }
    QLineEdit { border: none }
    QPushButton { background-color: none }
    QPushButton { border: none }
    QPushButton { padding-bottom: 8px }
    QPushButton { padding-top: 8px }"""

  searchingWidgetUnfocusedStyle = """
    QWidget { background-color: white; border-radius: 10px; border: none }
    QLineEdit { border: none }
    QPushButton { background-color: none }
    QPushButton { border: none }
    QPushButton { padding-bottom: 8px }
    QPushButton { padding-top: 8px }"""

  searchingWidgetErrorStyle = """
    QWidget { background-color: white; border-radius: 10px; border: 1px solid red }
    QLineEdit { border: none }
    QPushButton { background-color: none }
    QPushButton { border: none }
    QPushButton { padding-bottom: 8px }
    QPushButton { padding-top: 8px }"""

  mainWindowStyle = """
    QWidget { background-color: red }
    QPushButton { background-color: none }"""
