from PyQt6.QtGui import QFont

from ItemWidgets.recentSearch import RecentSearch
from MainWidget.result import Result

import pickledb

class Settings():
  settingsDatabaseFile = "MenuBar/settings.json"
  font = QFont().family()

  @staticmethod
  def initializeSettingsDatabase(screenWidth, screenHeight):
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    if not settingsDatabase.get('maximumResults'):
      settingsDatabase.set('maximumResults', 20)

    if not settingsDatabase.get('lastGradePicked'):
      settingsDatabase.set('lastGradePicked', 1)

    if not settingsDatabase.get('theme'):
      settingsDatabase.set('theme', 'light')

    if not settingsDatabase.get('defaultEditingAction'):
      settingsDatabase.set('defaultEditingAction', 'update')

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
  def getScreenWidth():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get('screenWidth')

  @staticmethod
  def getScreenHeight():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get('screenHeight')

  @staticmethod
  def getLeftWidgetWidth():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get('leftWidgetWidth')

  @staticmethod
  def getRightWidgetWidth():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get('rightWidgetWidth')

  @staticmethod
  def getSingleResultWidth():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get('singleResultWidth')

  @staticmethod
  def getResultsWidgetColumns():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)
    resultsWidgetColumns = settingsDatabase.get('rightWidgetWidth') // (settingsDatabase.get('singleResultWidth') + 10)

    return resultsWidgetColumns

  @staticmethod
  def setMaximumResults(maximumResults):
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)
    settingsDatabase.set('maximumResults', maximumResults)
    settingsDatabase.dump()

  @staticmethod
  def getMaximumResults():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get('maximumResults')

  @staticmethod
  def setBooleanSetting(settingName, newValue):
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)
    settingsDatabase.set(settingName, 1 if newValue else 0)
    settingsDatabase.dump()

  @staticmethod
  def getBooleanSetting(settingName):
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get(settingName) == 1

  @staticmethod
  def setTheme(theme):
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)
    settingsDatabase.set('theme', theme)
    settingsDatabase.dump()

  @staticmethod
  def getTheme():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get('theme')

  @staticmethod
  def setDefaultEditingAction(defaultEditingAction):
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)
    settingsDatabase.set('defaultEditingAction', defaultEditingAction)
    settingsDatabase.dump()

  @staticmethod
  def getDefaultEditingAction():
    settingsDatabase = pickledb.load(Settings.settingsDatabaseFile, False)

    return settingsDatabase.get('defaultEditingAction')

    # Fun Experiment
    # chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # print(len(chars)); max = 0; maxChar = 'a'; sizes = []
    # for char in chars:
    #   str = ''
    #   for i in range(10): str = str + char; size = Result(str).sizeHint().width()
    #   if size > max: max = size; maxChar = char
    #   sizes.append(size)

    # print(max); print(maxChar); print(sizes)
