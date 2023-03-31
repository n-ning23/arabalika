import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import io
import os
from settings import *

plt.rcParams['font.family'] = "Noto Serif SC"

class Character:
    __c_name:str = None
    __c_desc:str = ""
    __c_base = [0]*9
    __c_main = [0]*9
    __c_subs = [0]*7
    __c_percent = [0]*3
    __c_flat = [0]*9
    __c_stats = [0]*9
    __c_image = None
    __s = None
    def create(self, s:Settings, name:str, desc:str = ""):
        self.__c_name = name
        self.__c_desc = desc
        self.base()
        self.main()
        self.subs()
        self.percent()
        self.flat()
        self.__c_image = io.BytesIO()
        self.__s = s
        self.stats = [s.d("hp"), s.d("atk"), s.d("def"), s.d("em"), s.d("crate"), s.d("cdmg"), s.d("er"), s.d("ele"), s.d("heal")]
    def display(self):
        if (self.__c_name == None):
            raise Exception("Character not created.")
        self.__c_image = io.BytesIO()
        table = pd.DataFrame([self.stats,self.__c_stats])
        table = table.T
        table.columns = [self.__s.d("stats"), f"{self.__c_name}"]
        image, axes = plt.subplots()
        image_colors = [
            colors.hsv_to_rgb([self.__s.h,0.5,0.67]), 
            colors.hsv_to_rgb([self.__s.h,0.19,0.93]), 
            colors.hsv_to_rgb([self.__s.h,0.29,0.88])
        ]
        color = [[image_colors[0],image_colors[1]],[image_colors[2],"w"]]*4+[[image_colors[0],image_colors[1]]]
        plt_table = axes.table(cellText=table.values, 
            cellColours=color,
            cellLoc = 'center',
            colLabels=table.columns, 
            colColours=[self.__s.color(),self.__s.color()],
            loc='center'
            )
        plt_table[0,0].get_text().set_color("w")
        plt_table[0,1].get_text().set_color("w")
        plt_table.auto_set_column_width(col=[0])
        plt_table.scale(1,2)
        plt.axis("off")
        image.patch.set_visible(False)
        plt.savefig(self.__c_image,format="png", bbox_inches="tight", dpi=300)
        plt.savefig("test.png", bbox_inches="tight", dpi=300)
        plt.close()
        self.__c_image.seek(0)
    def base(self,
        b_hp:int = 0, 
        b_atk:int = 0,
        b_def:int = 0,
        b_em:int = 0,
        b_crate:float = 5,
        b_cdmg:float = 50,
        b_er:float = 100,
        b_ele:float = 0,
        b_heal:float = 0):
        if (self.__c_name == None):
            raise Exception("Character not created.")
        self.__c_base = [
            b_hp if b_hp != -1 else self.__c_base[0], 
            b_atk if b_atk != -1 else self.__c_base[1],
            b_def if b_def != -1 else self.__c_base[2],
            b_em if b_em != -1 else self.__c_base[3],
            b_crate if b_crate != -1 else self.__c_base[4],
            b_cdmg if b_cdmg != -1 else self.__c_base[5],
            b_er if b_em != -1 else self.__c_base[6],
            b_ele if b_ele != -1 else self.__c_base[7],
            b_heal if b_heal != -1 else self.__c_base[8]
        ]
    def main(self, m:[int]=[0,0,0,0,0,0,0,0,0]):
        if (self.__c_name == None):
            raise Exception("Character not created.")
        self.__c_main = [
            m[0]*46.6,
            m[1]*46.6,
            m[2]*46.6,
            m[3]*187,
            m[4]*31.1,
            m[5]*62.2,
            m[6]*51.8,
            m[7]*46.6,
            m[8]*35.9
        ]
        if (self.__c_main[7] < 0):
            self.__c_main[7] = 58.3
    def subs(self,
        s_hp:int = 0, 
        s_atk:int = 0,
        s_def:int = 0,
        s_em:int = 0,
        s_crate:float = 0,
        s_cdmg:float = 0,
        s_er:int = 0):
        if (self.__c_name == None):
            raise Exception("Character not created.")
        self.__c_subs = [
            s_hp*5 if s_hp != -1 else self.__c_subs[0], 
            s_atk*5 if s_atk != -1 else self.__c_subs[1],
            s_def*6 if s_def != -1 else self.__c_subs[2],
            s_em*19.5 if s_em != -1 else self.__c_subs[3],
            s_crate*3.3 if s_crate != -1 else self.__c_subs[4],
            s_cdmg*6.6 if s_cdmg != -1 else self.__c_subs[5],
            s_er*5.5 if s_er != -1 else self.__c_subs[6]
        ]
    def percent(self,
        p_hp:int = 0, 
        p_atk:int = 0,
        p_def:int = 0,
        ):
        if (self.__c_name == None):
            raise Exception("Character not created.")
        self.__c_percent = [
            p_hp if p_hp != -1 else self.__c_percent[0], 
            p_atk if p_atk != -1 else self.__c_percent[1], 
            p_def if p_def != -1 else self.__c_percent[2]
        ]
    def flat(self,
        f_hp:int = 0, 
        f_atk:int = 0,
        f_def:int = 0,
        f_em:int = 0,
        f_crate:float = 0,
        f_cdmg:float = 0,
        f_er:float = 0,
        f_ele:float = 0,
        f_heal:float = 0):
        if (self.__c_name == None):
            raise Exception("Character not created.")
        self.__c_flat = [
            f_hp if f_hp != -1 else self.__c_flat[0], 
            f_atk if f_atk != -1 else self.__c_flat[1],
            f_def if f_def != -1 else self.__c_flat[2],
            f_em if f_em != -1 else self.__c_flat[3],
            f_crate if f_crate != -1 else self.__c_flat[4],
            f_cdmg if f_cdmg != -1 else self.__c_flat[5],
            f_er if f_er != -1 else self.__c_flat[6],
            f_ele if f_ele != -1 else self.__c_flat[7],
            f_heal if f_heal != -1 else self.__c_flat[8]
        ]
    def calculate(self):
        if (self.__c_name == None):
            raise Exception("Character not created.")
        self.__c_stats = [
            int(self.__c_base[0]*0.01*(100+self.__c_main[0]+self.__c_subs[0]+self.__c_percent[0])+self.__c_flat[0]), #hp
            int(self.__c_base[1]*0.01*(100+self.__c_main[1]+self.__c_subs[1]+self.__c_percent[1])+self.__c_flat[1]), #atk
            int(self.__c_base[2]*0.01*(100+self.__c_main[2]+self.__c_subs[2]+self.__c_percent[2])+self.__c_flat[2]), #def
            int(self.__c_base[3]+self.__c_main[3]+self.__c_subs[3]+self.__c_flat[3]), #em
            self.__c_base[4]+self.__c_main[4]+self.__c_subs[4]+self.__c_flat[4], #crate
            self.__c_base[5]+self.__c_main[5]+self.__c_subs[5]+self.__c_flat[5], #cdmg
            self.__c_base[6]+self.__c_main[6]+self.__c_subs[6]+self.__c_flat[6], #er
            self.__c_base[7]+self.__c_main[7]+self.__c_flat[7], #ele
            self.__c_base[8]+self.__c_main[8]+self.__c_flat[8] #heal
        ]
    def optimizeCrit(self):
        if (self.__c_name == None):
            raise Exception("Character not created.")
        cv = self.__c_base[4]*2+self.__c_main[4]*2+self.__c_subs[4]*2+self.__c_flat[4]*2+self.__c_base[5]+self.__c_main[5]+self.__c_subs[5]+self.__c_flat[5]
        crate = min(min(cv/4,100),self.__c_base[4]+self.__c_main[4]+self.__c_subs[4]+self.__c_subs[5]/2+self.__c_flat[4])
        cdmg = cv-crate*2
        self.__c_subs[4] = (crate - self.__c_base[4] - self.__c_main[4] - self.__c_flat[4])
        self.__c_subs[5] = (cdmg - self.__c_base[5] - self.__c_main[5] - self.__c_flat[5])
    def energy(self, burst, 
    onSame:int = 0, offSame:int = 0,
    onDiff:int = 0, offDiff:int = 0,
    onNone:int = 0, offNone:int = 0,
    fixed:float = 0):
        if (self.__c_name == None):
            raise Exception("Character not created.")
        total_energy = 3*onSame + 1.8*offSame + onDiff + 0.6*offDiff + 2*onNone + 1.2*offNone
        temp = burst-fixed-total_energy
        if (total_energy < 0.1*temp):
            raise Exception("Not enough energy to satisfy ER needs.")
        if (total_energy == 0):
            raise Exception("Total energy generated in a rotation is 0.")
        if (temp/total_energy < -1):
            temp = -total_energy
        energy = 100+100*temp/total_energy
        return energy
    def getName(self):
        return self.__c_name
    def getDesc(self):
        return self.__c_desc
    def getSubs(self):
        subs = [
            self.__c_subs[0]/5,
            self.__c_subs[1]/5,
            self.__c_subs[2]/6,
            self.__c_subs[3]/19.5,
            self.__c_subs[4]/3.3,
            self.__c_subs[5]/6.6,
            self.__c_subs[6]/5.5
        ]
        return list(zip(self.stats, subs))
    def getStats(self):
        self.calculate()
        return self.__c_stats
    def getImage(self):
        self.calculate()
        self.display()
        return self.__c_image
    def setName(self, name:str):
        self.__c_name = name
    def setDesc(self, desc:str):
        self.__c_desc = desc
'''
s = Settings()
c = Character()
c.create(s, "Klee")
c.base(10287,311+608,615,b_ele=28.8)
c.main([0,1,0,0,1,0,0,1,0])
#c.main(m_atk=1,m_ele=1,m_crate=1)
c.subs(s_atk=4,s_crate=9,s_cdmg=9)
c.flat(f_hp=4780, f_atk=311, f_crate=33.1, f_ele=15)
print(c.getStats())
c.optimizeCrit()
print(c.getStats())
print(c.energy(burst=70,onSame=14,offNone=6))
c.display()
'''