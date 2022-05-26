from PyQt6.QtWidgets import QToolTip
from PyQt6.QtGui import QFont

class FontSettings():
  FONT = QFont().family()
  FONT_SIZES_SCALE = [
    6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 21, 24, 30, 36, 48, 60, 72
  ]

  DEFAULT_FONT_INDEXES = {
    'heading': 9,
    'result': 8,
    'single_word': 7,
    'text': 7,
    'button': 7,
    'tooltip': 5,
    'error': 4
  }

  SELECTED_FONT_MAPPING = {
    'very_small': -2,
    'small': -1,
    'medium': 0,
    'big': 1,
    'very_big': 2
  }

  @staticmethod
  def get_font(font_name):
    default_index_difference = FontSettings.SELECTED_FONT_MAPPING[FontSettings.SELECTED_FONT]
    font_index = FontSettings.DEFAULT_FONT_INDEXES[font_name] + default_index_difference
    return QFont(FontSettings.FONT, FontSettings.FONT_SIZES_SCALE[font_index])

  @staticmethod
  def initialize_font_settings(selected_font):
    FontSettings.SELECTED_FONT = selected_font
    QToolTip.setFont(FontSettings.get_font('tooltip'))
