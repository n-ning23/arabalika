from table2ascii import table2ascii, PresetStyle
import pandas as pd
import matplotlib.plt as plt

''' Class Rotation:
    __r_start:bool- whether rotation has been started
    __r_dim:tuple(int,int)- (sec,col)
    __r_ttable:[string][string]- transposed table
    __r_text:str- formatted ascii table
    __r_title:str- name of the rotation
'''
class Rotation():
    __r_start = False
    __r_dim = (0,0)
    __r_ttable = [[]]
    __r_text = ""
    __r_title = ""
    def rStart(self, sec:int, col:int=1, title:str=""):
        '''Starts a rotation with sec rows and col+1 columns'''
        if (sec < 1):
            raise Exception("Rotation cannot be less than one second.")
        if (sec > 30):
            raise Exception("Rotation should be at most 30 seconds.")
        if (col < 1):
            raise Exception("There cannot be less than one column.")
        if (col > 6):
            raise Exception("The bot does not support more than 6 columns.")
        self.__r_start = True
        self.__r_dim = (sec,col)
        self.__r_ttable = [[""]*sec for i in range(0,col+1)]
        self.__r_ttable[0] = [i for i in range(1,sec+1)]
        self.__r_title = title
        self.rCompile()
        self.rDisplay()
    def rCompile(self):
        '''Converts self.__r_ttable to text that is stored in self.__r_text'''
        if not self.__r_start:
            raise Exception("Rotation not started.")
        _,col = self.__r_dim
        header = ["C"+str(i) for i in range(0,col+1)]
        header[0] = "Seconds"
        body = zip(*self.__r_ttable)
        body = list(map(lambda r: list(r), body))
        self.__r_text = table2ascii(header=header,body=body,style=PresetStyle.thin_box)
    def rAdd(self, desc, secStart:int, secEnd:int, col:int=1):
        '''Adds an action to the table named desc from secStart to secEnd in C[col]'''
        if not self.__r_start:
            raise Exception("Rotation not started.")
        seconds, columns = self.__r_dim
        if (secEnd < secStart):
            raise Exception("Duration should be more than 0 seconds.")
        if (secStart < 1):
            raise Exception("Start cannot be less than 1.")
        if (secEnd > seconds):
            raise Exception("Cannot end after end of rotation.")
        if (col > columns) or (col < 1):
            raise Exception("Column does not exist.")
        for cell in self.__r_ttable[col][secStart-1:secEnd]:
            if (cell != ""):
                raise Exception("Cell occupied already with:"+cell)
        self.__r_ttable[col][secStart-1] = desc
        self.__r_ttable[col][secStart:secEnd] = ("\u25A0" for i in range(secStart,secEnd))
        self.rCompile()
        self.rDisplay()
    def rRemove(self, secStart:int, secEnd:int, col:int=1):
        '''Removes entries from secStart to secEnd in C[col] from table'''
        if not self.__r_start:
            raise Exception("Rotation not started.")
        seconds, columns = self.__r_dim
        if (secEnd < secStart):
            raise Exception("Duration should be more than 0 seconds.")
        if (secStart < 1):
            raise Exception("Start cannot be less than 1.")
        if (secEnd > seconds):
            raise Exception("Cannot end after end of rotation.")
        if (col > columns) or (col < 1):
            raise Exception("Column does not exist.")
        self.__r_ttable[col][secStart-1:secEnd] = ("" for i in range(secStart-1,secEnd))
        self.rCompile()
        self.rDisplay()
    def rAddColumn(self,col:int):
        '''Adds a column C[col]'''
        if not self.__r_start:
            raise Exception("Rotation not started.")
        seconds, columns = self.__r_dim
        if (columns == 6):
            raise Exception("The bot does not support more than 6 columns.")
        if (col > columns+1) or (col < 1):
            raise Exception("Column does not exist.")
        self.__r_dim = (seconds, columns+1)
        self.__r_ttable = self.__r_ttable[:col][:]+[[""]*seconds]+self.__r_ttable[col:][:]
        self.rCompile()
        self.rDisplay()
    def rRemoveColumn(self,col:int):
        '''Removes a column C[col]'''
        if not self.__r_start:
            raise Exception("Rotation not started.")
        seconds, columns = self.__r_dim
        if (columns == 1):
            raise Exception("Cannot remove when only one column exists.")
        if (col > columns) or (col < 1):
            raise Exception("Column does not exist.")
        self.__r_dim = (seconds, columns-1)
        self.__r_ttable = self.__r_ttable[:col][:] + self.__r_ttable[col+1:][:]
        self.rCompile()
        self.rDisplay()
    def rDisplay(self):
        '''Displays output of self.__r_text'''
        if not self.__r_start:
            raise Exception("Rotation not started.")
        print(self.__r_text)
    def rFinish(self):
        '''Resets self.__r_start to False after displaying'''
        if not self.__r_start:
            raise Exception("Rotation not started.")
        self.rDisplay()
        self.__r_start = False
        self.__r_dim = (0,0)
        self.__r_ttable = [[]]
        self.__r_text = ""
    def rGetDim(self):
        return self.__r_dim
    def rGetTable(self):
        return self.__r_ttable
    def rGetText(self):
        return self.__r_text
    def rGetTitle(self):
        return self.__r_title