# -*- coding: utf-8 -*-
"""
Created on Wed May 14 09:54:55 2014

@author: taras
"""

# Розрахунок режиму розчиненого газу на прикладі Рудавецького родовища
# методика взята з Справочного руководства
# Розрахунок при заданому дебіті
# Вихідні дані
pn=7.5 # тиск насичення в МПа
dp=0.1 # крок зміни тиску в МПа
# 1. Задаємося рядом значень тиску на контурі з кроком dp
pk=[]
pp=pn
while pp>dp:
     pk.append(pp)
     pp-=dp
if pk[-1]>dp: pk.append(0)
print(pk)