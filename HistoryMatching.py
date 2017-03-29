# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:15:10 2016

@author: taras
"""
import KoriPermeabilityModel as KoriPM
import MyInterp

class historyMatching(object):
    def __init__(self,RRGMod,devObj):
        self.RRGMod=RRGMod
        self.devObj=devObj
        
    def CountRRGOptimCriteriumH(xh):
        # В цій функції мінімізація відбувається по критерію співпадання газового фактора на кінець
        # фактичного періоду і мінімізації різниці накопиченого видобутку газу по факту і по моделі
#        print('Зайшов у функцію мінімізації')
        h=xh[0]
        #k=x[1]
        global k
        def CountRRGOptimCriteriumK(xk):
#            print('Зайшов у другу функцію мінімізації')
            k=xk[0]
            res=simpleRRG(PreparedProjectData,h,k,True)
            Gs=res[3]
            nuOil=res[5]
            # тут критерієм є співпадання газового фактора в останній точці
            # Остання точка з динаміки показників по об’єкту має поточний коефіцієнт вилучення
            # Потрібно знайти таку точку в РРГ, їй відповідає поточний газовий фактор
            # Цей газовий фактор і порівнюємо з фактичним
            LastPoint=len(Gs)
            # потчний коефіцієнт вилучення
#            print('ObjectRates[11]=',ObjectRates[11])
#            print('nuOil=',nuOil)
#            print('Gs=',Gs)
#            print(len(nuOil),len(Gs))
#            print('LastNuOil=',LastNuOil)
            tck = interpolate.splrep(nuOil, Gs, s=0)
            RRG_GF = interpolate.splev(LastNuOil, tck, der=0)
  #          print('RRG_GF=',RRG_GF)
            print('      ',h,k,RRG_GF,ObQg[LastPoint-1]/ObQo[LastPoint-1]*1000,abs(RRG_GF-ObQg[LastPoint-1]/ObQo[LastPoint-1]*1000))
            return (abs(RRG_GF-ObQg[LastPoint-1]/ObQo[LastPoint-1]*1000))
        res1 = minimize(CountRRGOptimCriteriumK,(2.1612), method='L-BFGS-B',bounds=[(1.0,7.0)])
#        res1 = minimize(TsarMin1,[4.0,3.0,0.2],             method='L-BFGS-B',bounds=((0,8),(0,8),(0,1))) 
#        print('res1=',res1)
        k=res1.x[0]
#        print('k=',k)
#        print('res1=',res1.x[0])
        res=simpleRRG(PreparedProjectData,h,k,False)
        Gs=res[3]
        nuOil=res[5]
        # Оптимізую по накопиченому видобутку газу
        # Треба сформувати масив, де кожній точці у РРГ відповідає накопичений видобуток газу
        # і тоді при відомому попточному коефієнті нафтовилучення знайти накопичений видобуто газу
        RRG_Qo=[]
        RRG_sumQo=[]        
        RRG_Qg=[]
        RRG_sumQg=[]
        RRG_Qo.append(0.0)
        RRG_sumQo.append(0.0)
        RRG_Qg.append(0.0)
        RRG_sumQg.append(0.0)
        for i in range(1,len(nuOil)):
            RRG_Qo.append((nuOil[i]-nuOil[i-1])*PreparedProjectData[0][1])
            RRG_sumQo.append(RRG_sumQo[i-1]+RRG_Qo[i])
            RRG_Qg.append(RRG_Qo[i]*Gs[i]/1000.0)
            RRG_sumQg.append(RRG_sumQg[i-1]+RRG_Qg[i])
#            print('i=',i,'Qg=',RRG_Qg[i],'sumQg=',RRG_sumQg[i])
#        print('nuOil=',nuOil,'RRG_sumQg=',RRG_sumQg)
        tck = interpolate.splrep(nuOil, RRG_sumQg, s=0)
        RRGLastSumQg = interpolate.splev(LastNuOil, tck, der=0)
#        for i in range(len(ObQo)):
#            print(i,Gs[i],ObQg[i]/ObQo[i]*1000)
        print('RRGLastSumQg=',RRGLastSumQg,'LastsumQg=',LastsumQg, abs(RRGLastSumQg-LastsumQg))
#        print('h=',h,'k=',k)
        return (abs(RRGLastSumQg-LastsumQg))

    def countRRGOptimCriteriumDiffYearGas(self,x):
        # В цій функції мінімізація відбувається по критерію мінімізації квадрату різниць
        # між річними видобутками газу по факту і по моделі
        permMod=KoriPM.KoriPermeabilityModel(x[0],x[1],x[2])
        self.RRGMod.makeRRGTable(permMod,False)
        self.devObj.setRatesFromRRGmodel(self.RRGMod.nuOil,self.RRGMod.ps,self.RRGMod.p2,self.RRGMod.Gs,self.RRGMod.phi)
        # Оптимізую по річному видобутку газу
        # Треба сформувати масив, де кожній точці у РРГ відповідає річний видобуток газу
        # і тоді при відомому поточному коефієнті нафтовилучення знайти накопичений видобуто газу
#        self.obj.setRatesFromRRGmodel(self.nuOil,self.ps,self.Gs,self.phi)
#        sumDiffsumQg=0
#        for i in range(self.obj.numOfPoints):
#            print('ObsumQg=',self.obj.sumQg[i],'RRGsumQg=',self.obj.RRGsumQg[i])
#            sumDiffsumQg=sumDiffsumQg+(self.obj.sumQg[i]-self.obj.RRGsumQg[i])**2.0
#        print('h=',x[0],'k=',x[1],'sor=',x[2],'sum=',sumDiffsumQg)
#        self.obj.setRatesFromRRGmodel(self.nuOil,self.ps,self.Gs)
        sumDiffsumQg=0
        for i in range(self.devObj.numOfPoints):
#            print('ObsumQg=',self.obj.sumQg[i],'RRGsumQg=',self.obj.RRGsumQg[i])
            sumDiffsumQg=sumDiffsumQg+(self.devObj.Qg[i]-self.devObj.RRGQg[i])**4
#        print('h=',x[0],'k=',x[1],'sor=',x[2],'sum=',sumDiffsumQg)
        return (sumDiffsumQg)

    def setWellProd(self,pPl,pZ,permMod):
        for i in range(len(self.devObj.wells)):
            well=self.devObj.wells[i]
            pS=(pPl+pZ)/2.0
            # тут ще треба врахувати к-сть днів у році
            lastPoint=self.devObj.numOfPoints-1
            sk=MyInterp.Interp(self.RRGMod.p2,self.RRGMod.sk,pPl)
            #       sk=self.histMatch.RRGmod.getSk(RRGPs)
#                    print('        sk=',sk)
            Fo=(permMod.getKo(sk))
            bos=self.RRGMod.fl.getBOil(pS)
            muos=self.RRGMod.fl.getMuOil(pS)
            phi=Fo/bos*muos
            #print('Fo=',Fo,'bos=',bos,'muos=',muos,'pPl=',pPl,'phi=',phi,'q=',well.qo[well.numOfPoints-1])
            well.kProd=well.qo[well.numOfPoints-1]/(phi*(pPl-pZ))
#            print(well.kProd)
            # тепер заповнюю кожну свердловину її продуктивністю
#            for well in self.ownWells:
#                well.prod=[]
#                for i in range(well.numOfPoints):
#                    well.prod.append()
