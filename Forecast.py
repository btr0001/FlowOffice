# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 14:55:25 2016

@author: taras
"""
import MyInterp
from scipy import interpolate

class Forecast(object):
    # newWells - список нових свердловин, назва, рік вводу, продуктивність
    def __init__(self,histMatch,permModel,newWells,name,pz,period,prname):
        # Для кожної точки моделі РРГ я маю пластовий тиск, вибійнй тиск у
        # кожній свердловині, коефіцієнт продуктивності, тоді я можу також 
        # знати і сумарний дебіт свердловин
        self.histMatch=histMatch
        self.permMod=permModel
        self.period=period
        self.varName=name
        self.pz=pz
        self.newWells=newWells
        self.prName=prname
        
    def makeForecast(self,fromYear,toYear):
        return
        
        
    def doForecast(self):
        # Власне розраховую тут прогноз
        # Розбиваю прогноз на інтервали, де є різна кількість свердловин
        # формую список років
        print('Розглядаю варіант',self.varName)
        fileName='./'+self.prName+'/variants/'+self.varName+'.prrates'
        print('filename=',fileName)
        f = open(fileName,"w")

        years=[]
        years.append(self.histMatch.devObj.maxYear+1)
        if self.varName!='base':
            for data in self.newWells:
#                print(data)
                if data[0]>years[len(years)-1]:
                    years.append(data[0])
        years.append(years[0]+self.period)
#        print(years)
        # формую список свердловин для кожного періоду
        periods=[]
        for i in range(len(years)-1):
            startYear=years[i]
            finishYear=years[i+1]-1
            wellsInPeriod=[]
            # базові свердловини
            for well in self.histMatch.devObj.wells:
                wellsInPeriod.append([well.name,well.kProd])
            # вибійний тиск
            # нові свердловини
            # проходжу масив вводу нових свердловин, додаю ті, де
            # рік вводу менший чи рівний за кінець періоду
            if self.varName!='base':
                for well in self.newWells:
                    if well[0]<=startYear:
                        wellsInPeriod.append([well[1],well[2]])
            periods.append([startYear,finishYear,wellsInPeriod])
#        print(periods)
        # тепер сам прогноз
        # index - це останній елемент масивів з історії розхробки
        startIndex=self.histMatch.devObj.numOfPoints-1
        print('Це має бути останній рік з історії:',self.histMatch.devObj.years[startIndex])
        
        
        # Тут власне починається розрахунок прогнозу по роках
        # Роблю перший рядок з даними з останнього прогнозного року
        self.year=[self.histMatch.devObj.years[startIndex]]
        self.pPl2=[self.histMatch.devObj.RRGP2[startIndex]]
        self.pPlS=[(self.histMatch.devObj.RRGP2[startIndex]+self.histMatch.devObj.RRGP2[startIndex-1])/2.0]
        self.Qo=[self.histMatch.devObj.Qo[startIndex]]
        self.sumQo=[self.histMatch.devObj.sumQo[startIndex]]
        self.Gf=[self.histMatch.devObj.Gf[startIndex]]
        self.Qg=[self.Qo[0]*self.Gf[0]/1000]
        self.sumQg=[self.histMatch.devObj.sumQg[startIndex]]
        
        index=0
        print('Дані з останнього фактичного року:')
        print('рік=',self.year[index],'Q=',self.Qo[index],'sumQ=',self.sumQo[index],'Gf=',self.Gf[index],'Ppl=',self.pPl2[index])
        print(self.year[index],self.Qo[index],self.sumQo[index],self.Gf[index],self.pPl2[index],file=f)
        # Цикл по періодах
        for period in periods:
            startYear=period[0]
            finishYear=period[1]
            print('Зайшов у період ',startYear,'-',finishYear)
            # Цикл по роках всередині періода
            for year in range(int(startYear),int(finishYear)):
                #print('    Розглядаю рік: ',year)
                index=index+1
                # перше наближення - пластовий тиск приймаю рівним на 
                # попередній рік
                temporaryRRGP2=self.pPl2[index-1]
                temporaryRRGPS=(self.pPlS[index-1]+temporaryRRGP2)/2.0
                temporarySumQOil=self.sumQo[index-1]
                #print('    temporarySumQOil=',temporarySumQOil)
                while True:
                    p2Previous=temporaryRRGP2
                    # визначаю дебіти свердловин
                    #  цикл по свердловинах
                    wells=period[2]
                    QOilFromAllWells=0
                    for well in wells:
#                        print('        Розглядаю свердловину',well[0])
                        kProd=well[1]
#                        print('        kProd=',kProd)
                        pWells=(temporaryRRGPS+self.pz)/2.0
#                        print('        pWells=',pWells,'RRGPs=',RRGPs)
                        pW=[]
                        pW.append(pWells)
                        sk=MyInterp.Interp(self.histMatch.RRGMod.p2,self.histMatch.RRGMod.sk,temporaryRRGP2)
                 #       sk=self.histMatch.RRGmod.getSk(RRGPs)
#                        print('        sk=',sk)
                        Fo=(self.permMod.getKo(sk))
                        bos=self.histMatch.RRGMod.fl.getBOil(pWells)
                        muos=self.histMatch.RRGMod.fl.getMuOil(pWells)
                        phi=Fo/bos*muos
                        q=kProd*(temporaryRRGPS-self.pz)*phi
              #          print('Fo=',Fo,'bos=',bos,'muos=',muos,'phi=',phi,'pPl=',temporaryRRGPs,'q=',q)
                        Q=q*365.25*0.9
                        #print('        Q=',Q)
                        QOilFromAllWells+=Q
#                        print('        QOilFromAllWells=',QOilFromAllWells)
#                    print('index=',index)
                    temporarySumQOil=self.sumQo[index-1]+QOilFromAllWells/1000
                    #print('temporarySumQOil=',temporarySumQOil,'Qzap=',self.histMatch.devObj.obj.Qzap)
                    temporaryNuOil=temporarySumQOil/self.histMatch.devObj.obj.Qzap
#                    print('temporaryNuOil=',temporaryNuOil)
                    # уточнюю величину пластового тиску
                    trend1=self.histMatch.RRGMod.nuOil
                    trend2=self.histMatch.RRGMod.p2
                    temporaryRRGP2=MyInterp.Interp(trend1,trend2,temporaryNuOil)
                    #print('temporaryRRGPs=',temporaryRRGPs,'різниця тисків=',psPrevious-temporaryRRGPs)
                    if abs(p2Previous-temporaryRRGP2)<0.001:
                        #print(type())
                        self.year.append(year)
                        self.pPl2.append(temporaryRRGP2)
                        self.pPlS.append(temporaryRRGPS)
                        self.Qo.append(QOilFromAllWells/1000)
                        self.sumQo.append(temporarySumQOil)
                        trend1=self.histMatch.RRGMod.p2
                        trend2=self.histMatch.RRGMod.Gs
                        self.Gf = MyInterp.Interp(trend1,trend2,self.pPlS)
                        col3=self.Qo[index]/self.histMatch.devObj.obj.Qzap*100
                        print(self.histMatch.devObj.obj.QzapExtractable,self.Qo[index])
                        col4=self.Qo[index]/(self.histMatch.devObj.obj.QzapExtractable-self.sumQo[index])*100
                        col6=self.Qo[index]/self.histMatch.devObj.obj.QzapExtractable*100
                        col7=self.sumQo[index]/self.histMatch.devObj.obj.Qzap
                        self.Qg.append(self.Qo[index]*self.Gf[index]/1000)
                        self.sumQg.append(self.sumQg[index-1]+self.Qg[index])
                        print('рік=',self.year[index],'Q=',self.Qo[index],'sumQ=',self.sumQo[index],'Gf=',self.Gf[index],'Ppl2=',self.pPl2[index])
                        print(self.year[index],self.Qo[index],col3,col4,self.sumQo[index],col6,col7,self.Qg[index],self.sumQg[index],file=f)
                        break;
        f.close()            
            
#        wellList=[]
        # базові свердловини
#        for well in self.wells:
#            wellList.append(well.name,well.kProd)
        # нові свердловини
#        for well in self.newWells:
#            wellList.append(well[0],)
#        self.RRGMod.setWellRates(wellList)
        