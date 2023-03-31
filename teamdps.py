from rotation import Rotation
from character import Character

class Team:
    __name:str = ""
    __desc:str = ""
    __characters = {}
    __rotation:Rotation = None
    __dps:float = 0
    def create(self, name:str, desc:str):
        self.__name = name
        self.__desc = desc