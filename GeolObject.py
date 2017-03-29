# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:02:24 2016

@author: taras
"""

# Цей клас описує геологічний об’єкт

class GeolObject(object):
    def __init__(self,fileName): 
        # Зчитує з файла властивості свердловини
        f=open(fileName,"r")
        # Загальна інформація, поки що тут тільки тиск насичення
        for line in f:
            self.pn=float(line.split('\t')[0])
            self.Qzap=float(line.split('\t')[1])
            self.QzapExtractable=float(line.split('\t')[2])
        f.close()

