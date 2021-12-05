from PyQt6.QtGui import QFont

from ItemWidgets.recentSearch import RecentSearch
from MainWidget.result import Result

class Settings():
  font = QFont().family()
  screenWidth = 0
  leftWidgetWidth = 0
  resultsWidgetColumns = 0
  rightWidgetWidth = 0
  singleResultWidth = 0

  def __init__(self):
    pass

  @staticmethod
  def calculateSizeSettings():
    longRecentSearch = RecentSearch("WWWWWWWWWWWWWWW", True) # 15
    Settings.leftWidgetWidth = longRecentSearch.sizeHint().width()


    longResult = Result("WWWWWWWWWW") # 10
    Settings.singleResultWidth = longResult.sizeHint().width()
    Settings.resultsWidgetColumns = (Settings.screenWidth - Settings.leftWidgetWidth) // Settings.singleResultWidth
    Settings.rightWidgetWidth = Settings.resultsWidgetColumns * Settings.singleResultWidth

    
    # Fun Experiment
    # chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # print(len(chars)); max = 0; maxChar = 'a'; sizes = []
    # for char in chars:
    #   str = ''
    #   for i in range(10): str = str + char; size = Result(str).sizeHint().width()
    #   if size > max: max = size; maxChar = char
    #   sizes.append(size)

    # print(max); print(maxChar); print(sizes)
