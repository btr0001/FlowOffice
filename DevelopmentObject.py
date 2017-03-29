# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 16:18:52 2016

@author: taras
"""

from scipy import interpolate

# Цей клас описує об’єкт розробки
# Він включає показники розробки, отримані з даних по свердловинах, а також
# відповідники річного видобутку газу, накопиченого видобутку газу, газового фактора,
# перераховані з РРГ-моделі (можливо, додасться ще щось).
# Назви цих показників починаються з RRG

class DevelopmentObject(object):
    def __init__(self,geolObject,wells):
        self.obj=geolObject
        self.wells=wells
        # Зчитує з файла властивості свердловини
        well=self.wells[0]
        self.minYear=well.minYear
        self.maxYear=well.maxYear
        for well in wells:
            if well.minYear<self.minYear:
                self.minYear=well.minYear
            if well.maxYear>self.maxYear:
                self.maxYear=well.maxYear
        self.numOfPoints=int(self.maxYear-self.minYear+1)
#        print('Об’єкт',self.minYear,self.maxYear,self.points)
        # показники по родовищу
        # Шаблони показників по об’єкту
        self.years=[]
        self.Qo=[]
        self.sumQo=[]
        self.Qw=[]
        self.sumQw=[]
        self.Ql=[]
        self.sumQl=[]
        self.Qg=[]
        self.sumQg=[]
        self.days=[]
        self.numOfWells=[]
        # Створюю списки з показниками, заповнюю їх нулями
#        print('Заповнення нулями')
        for i in range(int(self.minYear),int(self.maxYear)+1):
            self.years.append(i)
            self.Qo.append(0)
            self.sumQo.append(0)
            self.Qw.append(0)
            self.sumQw.append(0)
            self.Ql.append(0)
            self.sumQl.append(0)
            self.Qg.append(0)
            self.sumQg.append(0)
            self.days.append(0)
            self.numOfWells.append(0)
#        print(self.years)
        # Заповнюю показники по родовищу
        # Цикл по свердловинах
        for well in wells: # Вибираю свердловину і отримую масиви даних по них
            # Цикл по роках свердловини і додавання їх у об’єкт
            # Різниця між роком свердловини і роком об’єкта
            diff=int(well.minYear-self.minYear)
#            print(well.name,well.minYear,self.minYear,diff)
            for i in range(well.numOfPoints):
                # індекс в масиві по об’єкту
                j=i+diff
#                print(i,well.year[i],j,self.years[j])
                self.Qo[j]=self.Qo[j]+well.Qo[i]
                self.sumQo[j]=self.sumQo[j]+well.sumQo[i]
                self.Qw[j]=self.Qw[j]+well.Qw[i]
                self.sumQw[j]=self.sumQw[j]+well.sumQw[i]
                self.Ql[j]=self.Ql[j]+well.Ql[i]
                self.sumQl[j]=self.sumQl[j]+well.sumQl[i]
                self.Qg[j]=self.Qg[j]+well.Qg[i]
                self.sumQg[j]=self.sumQg[j]+well.sumQg[i]
                self.days[j]=self.days[j]+well.days[i]
                self.numOfWells[j]=self.numOfWells[j]+1
        # Додаю коефіцієнт вилучення нафти і ГФ
        self.nuOil=[]
        self.Gf=[]
            #    print('OilZap=',OilZap)
            #    print('lenYears=',len(ObYears))
        for i in range(self.numOfPoints):
            self.nuOil.append(self.sumQo[i]/self.obj.Qzap)
            self.Gf.append(self.Qg[i]/self.Qo[i]*1000)
#        print('ObsumQo=',ObsumQo[i],'Nuoil=',ObNuOil[i])

    def setRatesFromRRGmodel(self,nuOil,ps,p2,Gs,phi):
        # тут nuOil - коефіцієнт вилучення нафти
        # ps - середній тиск у покладі
        # Gs - середній газовий фактор
        tck = interpolate.splrep(nuOil, Gs, s=0)
        self.RRGGf = interpolate.splev(self.nuOil, tck, der=0)
        print(nuOil,ps,self.nuOil)
        tck = interpolate.splrep(nuOil, p2, s=0)
        interpolatedRRGP2 = interpolate.splev(self.nuOil, tck, der=0)
        self.RRGP2=[]
        for a in interpolatedRRGP2:
            self.RRGP2.append(a)
        tck = interpolate.splrep(nuOil, phi, s=0)
        self.RRGphi = interpolate.splev(self.nuOil, tck, der=0)
        self.RRGQg=[]
        self.RRGsumQg=[]
#        print(' рік','|','p2[i]',' Gs[i]',' nu[i]','   Qg[i]','RRGQg[i]',' sumQg[i]','sumRRGQg[i]')
#        print('-'*99)
        for i in range(self.numOfPoints):
            self.RRGQg.append(self.Qo[i]*self.RRGGf[i]/1000.0)
            if i==0:
                self.RRGsumQg.append(self.RRGQg[i])
            else:
                self.RRGsumQg.append(self.RRGsumQg[i-1]+self.RRGQg[i])
#            print("%2d | %4.1f %7.1f %7.3f %7.3f %7.3f %7.3f %7.3f" % (self.years[i],self.RRGPs[i],self.RRGGf[i],self.nuOil[i],self.Qg[i],self.RRGQg[i],self.sumQg[i],self.RRGsumQg[i]))
        

    def setWellProdHistory(self,pz):
        for well in self.ownWells:
            well.kProdHistory=[]
            
    def saveWellProdToFile(self,projectName):
        fileName='./'+projectName+'/kProd.dat'
        print(fileName)
        f = open(fileName,"w")
        kProd=[]
        for i in range(len(self.wells)):
            well=self.wells[i]
            kProd.append(well.kProd)
        print(kProd,file=f)
        f.close()
        
