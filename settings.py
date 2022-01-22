from PyQt6.QtGui import QFont

from ItemWidgets.recentSearch import RecentSearch
from MainWidget.result import Result

import pickledb

class Settings():
  settingsDatabaseFile = "settings.json"

  font = QFont().family()
  screenWidth = 0
  screenHeight = 0
  leftWidgetWidth = 0
  resultsWidgetColumns = 0
  rightWidgetWidth = 0
  singleResultWidth = 0

  @staticmethod
  def initializeSettingsDatabase(screenWidth, screenHeight):
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)
    if not settingsDatabase.get('lastGradePicked'):
      settingsDatabase.set('lastGradePicked', 1)

    if isinstance(settingsDatabase.get('rememberLastGradePicked'), bool):
      settingsDatabase.set('rememberLastGradePicked', 0)

    if isinstance(settingsDatabase.get('askBeforeActions'), bool):
      settingsDatabase.set('askBeforeActions', 1)

    if isinstance(settingsDatabase.get('showEditDictWordsButton'), bool):
      settingsDatabase.set('showEditDictWordsButton', 1)

    settingsDatabase.dump()

    Settings.calculateSizeSettings(screenWidth, screenHeight)

  @staticmethod
  def modifyLastGradePicked(grade):
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)
    settingsDatabase.set('lastGradePicked', grade)
    settingsDatabase.dump()

  @staticmethod
  def calculateSizeSettings(screenWidth, screenHeight):
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)
    if not settingsDatabase.get('screenWidth') == screenWidth:
      settingsDatabase.set('screenWidth', screenWidth)
      settingsDatabase.set('screenHeight', screenHeight)

      longRecentSearch = RecentSearch("WWWWWWWWWWWWWWW", True) # 15
      leftWidgetWidth = longRecentSearch.sizeHint().width()
      settingsDatabase.set('leftWidgetWidth', leftWidgetWidth)

      rightWidgetWidth = screenWidth - leftWidgetWidth - 2
      settingsDatabase.set('rightWidgetWidth', rightWidgetWidth)

      longResult = Result("WWWWWWWWWW") # 10
      singleResultWidth = longResult.sizeHint().width()
      settingsDatabase.set('singleResultWidth', singleResultWidth)

      settingsDatabase.dump()

  @staticmethod
  def getLeftWidgetWidth():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get('leftWidgetWidth')

  @staticmethod
  def getRightWidgetWidth():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get('rightWidgetWidth')

  @staticmethod
  def getResultsWidgetColumns():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)
    resultsWidgetColumns = settingsDatabase.get('rightWidgetWidth') // settingsDatabase.get('singleResultWidth')

    return resultsWidgetColumns

  @staticmethod
  def setBooleanSetting(settingName, newValue):
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)
    settingsDatabase.set(settingName, 1 if newValue else 0)
    settingsDatabase.dump()

  @staticmethod
  def getBooleanSetting(settingName):
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get(settingName) == 1

    # Fun Experiment
    # chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # print(len(chars)); max = 0; maxChar = 'a'; sizes = []
    # for char in chars:
    #   str = ''
    #   for i in range(10): str = str + char; size = Result(str).sizeHint().width()
    #   if size > max: max = size; maxChar = char
    #   sizes.append(size)

    # print(max); print(maxChar); print(sizes)
