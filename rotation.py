import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import io
import os
from consts import *
from settings import *

plt.rcParams['font.family'] = "Noto Serif SC"

''' Class Rotation:
    __r_start:bool- whether rotation has been started
    __r_dim:tuple(int,int)- (sec,col)
    __r_table:[string][string]- transposed table
    __r_colors:pd.DataFrame - colors of respective cells
    __r_image:str- image
'''
class Rotation():
    __r_start = False
    __r_dim = (0,0)
    __r_table = [[]]
    __r_colors = [[]]
    __r_image = None
    __s = None
    def create(self, s:Settings, sec:int, col:int=1):
        '''Starts a rotation with sec rows and col+1 columns'''
        if (sec < 1):
            raise Exception("Rotation cannot be less than one second.")
        if (sec > MAX_SEC):
            raise Exception(f"Rotation should be at most {MAX_SEC} seconds.")
        if (col < 1):
            raise Exception("There cannot be less than one column.")
        if (col > MAX_COL):
            raise Exception(f"The bot does not support more than {MAX_COL} columns.")
        self.__r_start = True
        self.__r_dim = (sec,col)
        self.__r_table = [["                    "]*sec for i in range (0,col+1)]
        self.__r_colors = [["w"]*sec for i in range(0,col+1)]
        self.__r_table[0] = [i for i in range(1,sec+1)]
        self.__s = s
    def display(self):
        '''Converts self.__r_table to image that is stored in self.__r_image'''
        if not self.__r_start:
            raise Exception("Rotation not started.")
        seconds, columns = self.__r_dim
        self.__r_image = io.BytesIO()
        table = pd.DataFrame(self.__r_table)
        table = table.T
        table.columns = [f"   {self.__s.d('sec')}   "]+["" for i in range(1,columns+1)]
        image, axes = plt.subplots()
        colors = list(map(list,zip(*self.__r_colors)))
        plt_table = axes.table(cellText=table.values, 
            cellColours=colors,
            cellLoc = 'center',
            colLabels=table.columns, 
            loc='center'
            )
        plt_table.auto_set_column_width(col=[i for i in range(0,columns+1)])
        plt_table.scale(1,2)
        plt.axis("off")
        image.patch.set_visible(False)
        plt.savefig(self.__r_image,format="png", bbox_inches="tight", dpi=300)
        #plt.savefig("test.png", bbox_inches="tight", dpi=300)
        plt.close()
        self.__r_image.seek(0)
    def add(self, desc, secStart:int, secEnd:int, col:int=1):
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
        #COLOR
        h = self.__s.h+0.1*(secStart%3-1)
        if (h < 0):
            h = 1+h
        s = 0.25+0.25*(secStart//3%3)
        v = 0.75+0.25*(col%2)
        color = colors.hsv_to_rgb([h,s,v])
        self.__r_table[col][secStart-1] = desc
        self.__r_table[col][secStart:secEnd] = ["                    "]*(secEnd-secStart)
        self.__r_colors[col][secStart-1:secEnd] = [color]*(secEnd-secStart+1)
    def remove(self, secStart:int, secEnd:int, col:int=1):
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
        self.__r_table[col][secStart-1:secEnd] = ("                 " for i in range(secStart-1,secEnd))
        self.__r_colors[col][secStart-1:secEnd] = ["w"]*(secEnd-secStart+1)
    def addColumn(self,col:int):
        '''Adds a column C[col]'''
        if not self.__r_start:
            raise Exception("Rotation not started.")
        seconds, columns = self.__r_dim
        if (columns == MAX_COL):
            raise Exception("The bot does not support more than 6 columns.")
        if (col > columns+1) or (col < 1):
            raise Exception("Column does not exist.")
        self.__r_dim = (seconds, columns+1)
        self.__r_table = self.__r_table[:col][:]+[["                    "]*seconds]+self.__r_table[col:][:]
        self.__r_colors = self.__r_colors[:col][:]+[["w"]*seconds]+self.__r_colors[col:][:]
    def removeColumn(self,col:int):
        '''Removes a column C[col]'''
        if not self.__r_start:
            raise Exception("Rotation not started.")
        seconds, columns = self.__r_dim
        if (columns == 1):
            raise Exception("Cannot remove when only one column exists.")
        if (col > columns) or (col < 1):
            raise Exception("Column does not exist.")
        self.__r_dim = (seconds, columns-1)
        self.__r_table = self.__r_table[:col][:] + self.__r_table[col+1:][:]
        self.__r_colors = self.__r_colors[:col][:] + self.__r_colors[col+1:][:]
    def clear(self):
        '''Resets self.__r_start to False'''
        if not self.__r_start:
            raise Exception("Rotation not started.")
        self.__r_start = False
        self.__r_dim = (0,0)
        self.__r_table = [[]]
        self.__r_colors = [[]]
        self.__r_image = None
    def getDim(self):
        return self.__r_dim
    def getTable(self):
        return self.__r_table
    def getColors(self):
        return self.__r_colors
    def getImage(self):
        self.display()
        return self.__r_image
'''
s = Settings()
r = Rotation()
r.start(10,2)
r.add("测试",1,1)
r.add("test",2,2)
r.add("balabala",3,3)
r.add("试试超级长的袖看看怎么样",1,10,2)
'''