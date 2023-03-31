import matplotlib.colors as colors
from consts import *

class Settings:
    language = COMMAND_LANGUAGE
    def __init__(self):
        self.language = COMMAND_LANGUAGE
        self.h = 0.5
        self.s = 0.86
        self.v = 0.33
        self.__description = DESCRIPTION[self.language]
        self.__color = colors.hsv_to_rgb([self.h, self.s, self.v])
    def updateSettings(self):
        self.__description = DESCRIPTION[self.language]
        self.__color = colors.hsv_to_rgb([self.h, self.s, self.v])
    def d(self, phrase:str):
        return self.__description[phrase]
    def color(self):
        return colors.to_hex(self.__color)