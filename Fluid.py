# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 10:52:17 2016

@author: taras
"""
# Цей клас описує об’єкти, який містить табульовані дані про властивості флюїдів
# і повертає їх значення при заданих тисках

# presTab - перелік тисків, для яких табульовані властивості флюїдів
# muoTab - перелік табульованих величин в’язкості нафти
# boTab - перелік табульованих величин об’ємного коефіцієнта нафти
# GoTab - перелік табульованих величин газовмісту нафти
# mugTab - перелік табульованих величин в’язкості газу

from scipy import interpolate

class Fluid(object):
    def __init__(self,fileName): 
        # Зчитує з файла властивості флюїдів
        f=open(fileName,"r")
        self.presTab=[]
        self.muoTab=[]
        self.boTab=[]
        self.GoTab=[]
        self.mugTab=[]
        for line in f:
            parts=line.split(' ')
            self.presTab.append(float(parts[0]))
            self.muoTab.append(float(parts[1]))
            self.boTab.append(float(parts[2]))
            self.GoTab.append(float(parts[3]))
            self.mugTab.append(float(parts[4]))
        self.numOfPoints=len(self.presTab)
        f.close()
        self.tckMuOil=interpolate.splrep(self.presTab, self.muoTab, s=0)
        self.tckBOil = interpolate.splrep(self.presTab, self.boTab, s=0)
        self.tckGOil = interpolate.splrep(self.presTab, self.GoTab, s=0)
        self.tckMuGas = interpolate.splrep(self.presTab, self.mugTab, s=0)
        
        
    def getMuOil(self,listOfPresses):
        return (interpolate.splev(listOfPresses, self.tckMuOil, der=0))

    def getBOil(self,listOfPresses):
        return (interpolate.splev(listOfPresses, self.tckBOil, der=0))

    def getGOil(self,listOfPresses):
        return (interpolate.splev(listOfPresses, self.tckGOil, der=0))

    def getMuGas(self,listOfPresses):
        return (interpolate.splev(listOfPresses, self.tckMuGas, der=0))
