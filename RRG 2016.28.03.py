# -*- coding: utf-8 -*-

# Розрахунок показників розробки на режимі розчиненого газу і все, що необхідне для 
# формування вихідних даних.

# Функції для розрахунку фазових проникностей

from scipy import interpolate
import matplotlib.pyplot as plt
import math
from scipy.optimize import minimize
import Fluid
import Well
import GeolObject
import KoriPermeabilityModel as KoriPM
import RRGmodel
import DevelopmentObject
import HistoryMatching
import os
import Forecast
    
def Naar(x):
    m=x[0][0]
    p=x[0][1]
    q=x[0][2]
    # saturation, agent, front
    saf=x[1][0]
    skr=x[1][1]
    s=(saf-skr)/(1-skr)
    ko=(1-2*s)**m/(2-(1-2*s)**p)
    ka=s**q
    ksi=ka/ko
    return(ko,ka,ksi)
    
# Перший пункт головного меню    
    
def ShowGraphs():
    print("1.1 Графіки Царевича.")
    print("1.2 Апроксимація Корі.")
    print("1.3 Апроксимація Наара-Гендерсона.")
    choise1=input("Зробіть вибір: ")
    #choise1='1.2'
    if choise1=='1.1':
        print("Зайшов у функцію відн. прон.")
        # читаю дані з файла
        #filename=u"Дані Царьова.dat"
        filename="data.dat"
        f=open(filename,"r")
        print("відкрив файл")
        s=[]
        Fn=[]
        ksi=[]
        for line in f:
            parts=line.split('\t')
            s.append(1-float(parts[0]))
            Fn.append(float(parts[1]))
            ksi.append(float(parts[2]))
        f.close()
        plt.plot(s,Fn,s,ksi)
        plt.show()
    elif choise1=='1.2':
        # побудова графіка Корі
        sa=[]
        Fn=[]
        Fa=[]
        sakr=0.8
        sa.append(0)
        for num in range(1,17):
            sa.append(sa[0]+sakr/16*num)
            #print(num,s[num-1],s[num])
        for num in range(1,5):
            sa.append(sa[16]+(1-sakr)/4*num)
        print(sa)
        Fn=[]
        Fa=[]
        y=[[4,3],[0.2,0]]
        for num in range(len(sa)):            
            y[1][1]=1-sa[num]
            rr=Kori(y)
            Fn.append(rr[0])
            Fa.append(rr[1])
        print('sa=',sa,'Fn=',Fn,'Fa=',Fa)
        plt.plot(sa,Fn,sa,Fa)
        plt.show()
           
#        ShowTsar()
    return

def DetRelPerm():
    print("Зайшов у функцію відн. прон.")
    # читаю дані з файла
    #filename=u"Дані Царьова.dat"
    filename="data.dat"
    f=open(filename,"r")
    print("відкрив файл")
    s=[]
    Fn=[]
    ksi=[]
    for line in f:
        parts=line.split('\t')
        s.append(float(parts[0]))
        Fn.append(float(parts[1]))
        ksi.append(float(parts[2]))
    f.close()
    #print(s)
    #print(Fn)
    #print(ksi)
    # Функції для мінімізації
    def TsarMin1(x):
        #print(x[0],x[1],x[2])
        y=[[x[0],x[1]],[x[2],0]]
        #print(len(y),y[0])
        sum=0
        maxdiff=0
        for i in range(len(s)):
            #print('i=',i,'sum=',sum)
            # мінімізація по відносному відхиленню
            if ksi[i]!=0:
                y[1][1]=s[i]
                KoriModel=KoriPM.KoriPermeabilityModel(x[0],x[1],x[2])
                #print('KoriRes=',KoriRes)
                ksiKori=KoriModel.getKsi(s[i])
                diff=((ksi[i]-ksiKori)/ksi[i])**2
                if diff>maxdiff:
                    maxdiff=diff
                    maxnum=i
                    maxTsar=ksi[i]
                    maxKori=ksiKori
                sum+=diff
                #print('i=',i,'ksi=',ksi[i],"ksiKori=",ksiKori,'dSum=',((ksi[i]-ksiKori)/ksi[i])**2,'sum=',sum)
        print("sum=",sum,'maxdiff=',maxdiff,'maxnum=',maxnum,'maxTsar=',maxTsar,'maxKori=',maxKori)
        return(sum)
    
    # сама мінімізація
    # Початкові наближення у апроксимації Корі: h=4; k=3; 
    # s_в_kr - таке насичення газом (критичне витісняючим анентом), 
    # при якому припиняється рух нафти, приймаємо 0.8
    # в Царевича цієї величини немає, бо такі великі насичення газом не роглядаються
#    res1 = minimize(TsarMin1,[4.0,3.0,0.2],options={'xtol': 1e-8, 'disp': False}) 
    res1 = minimize(TsarMin1,[4.0,3.0,0.2], method='L-BFGS-B',bounds=((0,8),(0,8),(0,1))) 

    print(res1)
    y=[[2.685,2.161],[0,0]]
#    for num in range(len(s)):
#        y[1][1]=s[num]
#        ksiKori=Kori(y)[2]
        # print('ksiTzar=',ksi[num],'ksiKori=',ksiKori)
    return res1

def InputDataAboutReservoir():
    name=input('введіть назву проекта: ')
    
    pn=input('Тиск насичення, МПа:')
    #mug=
    return

def OpenProject(prname):
    # Завантажує з файла і формує структуру даних проекту
    # Властивості флюїдів
    filename='./'+prname+'/'+'pvt.dat'
    fluid=Fluid.Fluid(filename)
    # Дані по видобутках свердловин
    wellfiles = os.listdir('./'+prname+'/wells') 
    wells = filter(lambda x: x.endswith('.rates'), wellfiles) 
#    print('Знайдено наступні свердловини:')
    # тут потрібно прочитати дані про видобутки і сформувати список
    WellRates=[]
    for name in wells:
        print(name)
#        print('зайшов у цикл')
        filename=prname+'/wells/'+name
        WellRates.append(Well.Well(name,filename))
#        print(len(WellRates))
    filename='./'+prname+'/'+'general.dat'
    # Створюю об’єкт розробки
    obj=GeolObject.GeolObject(filename)
    return(obj,fluid,WellRates)

def prepareData():
    # Тут я створюю список проектів, вибираю з них, читаю і підготовлюю дані
    files = os.listdir() 
    projects = filter(lambda x: x.endswith('.rrg'), files) 
    print('Знайдено наступні проекти, виберіть з них:')
    for name in projects:
        print(name)
    # prname=input('Введіть назву проекту без розширення .rrg (exit, щоб вийти: ')
    prname='Rudavets.rrg'
    (obj,fluid,WellRates)=OpenProject(prname)
    return (obj,fluid,WellRates,prname)


def RRGadvanced():
    # ця процедура має оптимізувати параметри проекту, самі дані проекту мають бути вхідними даними
    # що зробити:
    # 1. Вибрати проект і прочитати з нього дані.
    # 2. Підібрати параметри РРГ.
    (geolObj,fluid,wellRates,prname)=prepareData()
    RRGMod=RRGmodel.RRGmodel(geolObj,fluid)
    RRGMod.setStepOfPressureChange(0.2)
    devObj=DevelopmentObject.DevelopmentObject(geolObj,wellRates)
    histMatch=HistoryMatching.historyMatching(RRGMod,devObj)
    # Підбираю модель фазових проникностей
#    res=minimize(CountRRGOptimCriteriumH,[2.685],method='L-BFGS-B')
    res=minimize(histMatch.countRRGOptimCriteriumDiffYearGas,[2.685,2.1612,0.0],method='L-BFGS-B',bounds=[(1.0,7.0),(1.0,7.0),(0.0,1.0)])
    print('Це я вже після функції мінімізації')
    h=res.x[0]
    k=res.x[1]
    sor=res.x[2]
    permMod=KoriPM.KoriPermeabilityModel(h,k,sor)
    RRGMod.makeRRGTable(permMod,True)
    permMod.saveToFile(prname)
    print('Річний видобуток газу')
    plt.plot(devObj.years,devObj.Qg,devObj.years,devObj.RRGQg)
    plt.show()
#    for i in range(obj.numOfPoints):
#        print(obj.years[i],obj.Gf[i],obj.RRGGf[i])
    plt.plot(devObj.years,devObj.Gf,devObj.years,devObj.RRGGf)
    plt.show()

    # прогнозування роботи свердловин
    # Приймаю, що мені відомий вибійний тиск, оскільки насос спущений на певну глибину
    pz=2
    print('# Розраховую продуктивності існуючих свердловин')
    # Середній тиск в останньому році
    pPlS=(histMatch.devObj.RRGP2[histMatch.devObj.numOfPoints-1]+histMatch.devObj.RRGP2[histMatch.devObj.numOfPoints-2])/2.0
    histMatch.setWellProd(pPlS,pz,permMod)
    for well in devObj.wells:
        print(well.kProd)
    devObj.saveWellProdToFile(prname)
    
    # Тут потрібно розглядати варіанти розробки
    
    # Роблю перелік файлів з варіантами розробки
    varFiles = os.listdir('./'+prname+'/variants') 
    varFiles = filter(lambda x: x.endswith('.variant'), varFiles) 
#    for name in varFiles:
#        print(name)
    variantList=[]
    for name in varFiles:
        fileName=prname+'/variants/'+name
        print('Назва файла=',fileName)
        f=open(fileName,"r")
        newWells=[]
        for line in f:
            print(line)
            parts=line.split(' ')
            year=int(parts[0])
            wellName=parts[1]
            wellProd=float(parts[2])
            newWells.append([year,wellName,wellProd])
        variantList.append([name,newWells])
#    print(variantList)
    # тепер проходжуся по варіантах, створюю об’єкти і розраховую прогноз
    forecastObjects=[]
    # базовий варіант
    fObj=Forecast.Forecast(histMatch,permMod,[],'base',pz,20,prname)
    fObj.doForecast()
    forecastObjects.append(fObj)
    print('Завершив базовий')
    print(variantList)
    for variant in variantList:
        print(variant)
        fObj=Forecast.Forecast(histMatch,permMod,variant[1],variant[0],pz,20,prname)
        fObj.doForecast()
        forecastObjects.append(fObj)
    
    
    
    # Для кожної точки в режимі РРГ додаю сумарний дебіт свердловин
#    RRGMod.sumQWells=[]
#    for i in range(RRGMod.numOfRRGPoints):
#        sumQWells=0
#        for well in RRGMod.obj.ownWells:
#            sumQWells=sumQWells+well.kProd*(RRGMod.ps[i]-pz)
#        RRGMod.sumQWells.append(sumQWells)
#        print(RRGMod.ps[i],RRGMod.sumQWells[i])
    # Між дебітом свердловин і коеф. вилучення встановлено зв’язок
#    print(kProd)
    
#    print('h=',h)
#    print(res)
#    for i in range(len(ps)):
#        print(i,p1[i],p2[i],ps[i],Gs[i],sk[i],nu[i])
    return prname
    
def choozeForecastVar(prname):
    print('Виберіть варіант розробки родовища:')
    print
    print('1. Базовий.')
    WellList=[]
    
    
def MakeForecast(prname):
    # Відтворюю стан проекта із збережених файлів
    # 1. Поклад, флюїд, дані по свердловинах
    (obj,fluid,WellRates)=OpenProject(prname+'.rrg')
    # 2. Результати відтворення історії, у даній версії - модель фазових проникностей
    permMod=KoriPM.KoriPermeabilityModel(0,0,0)
    permMod.loadFromFile(prname)
    # 3. Розрахункова модель РРГ
    RRGMod=RRGmodel.RRGmodel(obj,fluid)
    RRGMod.setStepOfPressureChange(0.2)
    RRGMod.makeRRGTable(permMod,True)
    # 4. Коефіцієнти продуктивності свердловин поточні
    Pz=2.0
    obj.setWellProd(Pz)
    # 5. Заповнюю свердловини пластовими тисками і phi
    for well in WellRates:
        tck = interpolate.splrep(obj.years, obj.RRGPs, s=0)
        well.ps = interpolate.splev(well.year, tck, der=0)
        print(well.ps)

    # 5. Динаміка коефіцієнта продуктивності свердловин
    
    period=20
    newWells=[]
    var1=Forecast.Forecast(RRGMod,period,WellRates,newWells)
    var1.doForecast
    
    
    return
    
print("Зробіть вибір:")
print("1. Візуалізація даних про фазові прониконості.")
print("2. Підбір моделі фазових проникностей відповідно до таблиць Царевича.")
print("3. Ввід даних про об’єкт, що розробляється на РРГ.")
print("4. Відтворення розробки по РРГ.")
print("5. Проектні показники.")
#choise=input("Зробіть вибір: ")
choise='4'
print(choise)
if choise=='1':
    ShowGraphs()
elif choise=='2':
    DetRelPerm()
elif choise=='3':
    InputDataAboutReservoir()
elif choise=='4':
    prname=RRGadvanced()
elif choise=='5':
    MakeForecast(prname)
    
else: print("Нікуди не заходжу")
