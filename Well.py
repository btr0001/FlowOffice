# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 16:22:42 2016

@author: taras
"""

# Цей клас описує свердловину

class Well(object):
    def __init__(self,wellName,fileName): 
        # Зчитує з файла властивості свердловини
        f=open(fileName,"r")
        self.name=wellName
        self.year=[]
        self.Qo=[]
        self.sumQo=[]
        self.Qw=[]
        self.sumQw=[]
        self.Ql=[]
        self.sumQl=[]
        self.Qg=[]
        self.sumQg=[]
        self.nw=[]
        self.Gf=[]
        self.days=[]
        self.method=[]
        self.qo=[]
        self.ql=[]
        for line in f:
            parts=line.split('\t')
            self.year.append(float(parts[0]))
            self.Qo.append(float(parts[1]))
            self.sumQo.append(float(parts[2]))
            self.Qw.append(float(parts[3]))
            self.sumQw.append(float(parts[4]))
            self.Ql.append(float(parts[5]))
            self.sumQl.append(float(parts[6]))
            self.Qg.append(float(parts[7]))
            self.sumQg.append(float(parts[8]))
            self.nw.append(float(parts[9]))
            self.Gf.append(float(parts[10]))
            self.days.append(float(parts[11]))
            self.method.append(parts[12])
            self.qo.append(float(parts[13]))
            self.ql.append(float(parts[14]))
        self.numOfPoints=len(self.year)
        self.minYear=self.year[0]
        self.maxYear=self.year[self.numOfPoints-1]
#        print(self.name,self.minYear,self.maxYear,self.numOfPoints)

