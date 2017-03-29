# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 11:12:12 2016

@author: taras
"""
# Тут:
# so - насичення нафтою
# sor - залишкове насичення нафтою
# sa - насичення витісняючим агентом

class KoriPermeabilityModel(object):
    def __init__(self,h,k,sor):
        self.h=h
        self.k=k
        self.sor=sor

    def getAll(self,so):
        #print('Виклик Корі з параметрами h=',h,' k=',k)
        # saturation, agent, front
        sa=1-so
        s=None
        if so>self.sor:
            s=sa/(1-self.sor)
            self.ko=(1-s)**self.h
            #print('s=',s,'ko=',ko)
            self.ka=s**self.k*(2-s)
            if self.ko!=0:
                self.ksi=self.ka/self.ko
            else: self.ksi=0
        else:
            self.ko=0
            self.ka=1
            self.ksi=1000
        return(self.ko,self.ka,self.ksi)
        
    def getKo(self,s):
        return(self.getAll(s)[0])

    def getKa(self,s):
        return(self.getAll(s)[1])

    def getKsi(self,s):
        return(self.getAll(s)[2])

    def saveToFile(self,projectName):
        fileName='./'+projectName+'/PermModel.dat'
        f = open(fileName,"w")
        print('Kori',file=f)
        print(self.h,self.k,self.sor,file=f)
        f.close()

    def loadFromFile(self,projectName):
        fileName='./'+projectName+'/PermModel.dat'
        f = open(fileName,"r")
        line=f.readline()
        line=f.readline()
        parts=line.split(' ')
        self.h=float(parts[0])
        self.k=float(parts[1])
        self.sor=float(parts[2])
        f.close()
