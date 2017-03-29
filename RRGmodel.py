# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 11:11:03 2016

@author: taras
"""
import KoriPermeabilityModel as KoriPM
from scipy import interpolate

class RRGmodel(object):
        
    def __init__(self,deposit,fluid):
        self.obj=deposit
        self.fl=fluid
        
    def setStepOfPressureChange(self,dP):
        self.dP=dP
        
    def makeRRGTable(self,permeabilityModel,printTable):
        # Ця процедура розраховує РРГ для об’єкту, без оптимізацій і всяких прибамбасів
        self.numOfRRGPoints=int((self.obj.pn-1)/self.dP)+1
        self.p1=[]
        self.p2=[]
        self.ps=[]
        self.p1.append(self.obj.pn)
        self.p2.append(self.obj.pn)
        self.ps.append(self.obj.pn)
        for i in range(1,self.numOfRRGPoints):
            if i==1:
                self.p1.append(self.obj.pn)
            else:
                self.p1.append(self.p1[i-1]-self.dP)
            self.p2.append(self.p1[i]-self.dP)
            self.ps.append((self.p1[i]+self.p2[i])/2.0)
        self.muos = self.fl.getMuOil(self.ps)
        self.bo=self.fl.getBOil(self.p2)
        self.bos = self.fl.getBOil(self.ps)
        self.Go=self.fl.getGOil(self.p2)
        self.Gos = self.fl.getGOil(self.ps)
        self.mugs = self.fl.getMuGas(self.ps)
        self.Gs=[]
        self.sk=[]
        self.ksi=[]
        self.Fo=[]
        self.Fg=[]
        self.nuOil=[]
        # Це для розрахунку дебітів свердловин
        self.phi=[]
        # Step 0
        #print('step 0')
        self.sk.append(1.0)
        
#        koriModel=KoriPM(permeabilityModel)
        self.ksi.append(permeabilityModel.getKsi(self.sk[0]))
        self.Fo.append(permeabilityModel.getKo(self.sk[0]))
        self.Fg.append(permeabilityModel.getKa(self.sk[0]))
        #    tck = interpolate.splrep(presTab, muoTab, s=0)
        #print('tck=',tck)
        self.Gs.append(self.ksi[0]*self.muos[0]/self.mugs[0]*self.bos[0]*self.ps[0]/1e5+self.Gos[0])
        self.nuOil.append(0.0)
        self.phi.append(self.Fo[0]/(self.bos[0]*self.muos[0]))
        if printTable==True:
            print(' i','|','p1[i-1]','p2[i-1]','ps[i-1]','sk[i-1]','ksi[i-1]','muos[i-1]',' mugs[i-1]','bos[i-1]','Gos[i-1]','Gs[i-1]','Go[i-1]','bo[i-1]','Go[i]',' bo[i]',' sk[i]',' nu[i]')
            print('-'*137)
        for i in range(1,self.numOfRRGPoints):
            self.ksi.append(permeabilityModel.getKsi(self.sk[i-1]))
            self.Fo.append(permeabilityModel.getKo(self.sk[i-1]))
            self.Fg.append(permeabilityModel.getKa(self.sk[i-1]))
            self.Gs.append(self.ksi[i]*self.muos[i]/self.mugs[i]*self.bos[i]*self.ps[i]*10+self.Gos[i])
            #print('Чисельник=',((Gs[i]-Go[i-1])/bo[i-1]*sk[i-1]-(1-sk[i-1])*p1[i-1]*10+p1[i]*10))
            #print('Знаменник=',((Gs[i]-Go[i])/bo[i]+p1[i]*10))
            self.sk.append(((self.Gs[i]-self.Go[i-1])/self.bo[i-1]*self.sk[i-1]-(1-self.sk[i-1])*self.p1[i-1]*10+self.p1[i]*10)/((self.Gs[i]-self.Go[i])/self.bo[i]+self.p1[i]*10))
            self.nuOil.append(1-self.sk[i]/self.sk[0]*self.bo[0]/self.bo[i])
            self.phi.append(self.Fo[i]/(self.bos[i]*self.muos[i]))
#            print(self.ps[i],self.phi[i])
            if printTable==True:
                print("%2d | %5.1f %7.1f %7.1f %8.3f %8.4f %6.2f %11.3f %9.3f %8.1f %7.1f %7.1f %7.3f %7.1f %6.3f %6.3f %6.3f" % (i,self.p1[i-1],self.p2[i-1],self.ps[i-1],self.sk[i-1],self.ksi[i-1],self.muos[i-1],self.mugs[i-1],self.bos[i-1],self.Gos[i-1],self.Gs[i-1],self.Go[i-1],self.bo[i-1],self.Go[i],self.bo[i],self.sk[i],self.nuOil[i]))
            # Ще визначаю phi, яке потрібне для розрахунку дебітів свердловин
            # Середній тиск для свердловини
#        pz=2 # Цей тиск треба буде ввести з файла
#        pWell=[]
#        for i in range(NumOfIntervals):
#            pWell.append((p2[i]-pz)/2.0)
            # Необхідні властивості флюїдів при середніх тисках у свердловині
#        muosWellP = fluid.getMuOil(pWell)
        #print('muo=',muo)
#        phi=[]
#        bosWellP = fluid.getBOil(pWell)
        #        print(len(Fo),len(bosWellP),len(muosWellP))
#        for i in range(NumOfIntervals):
#            phi.append(Fo[i]/(bosWellP[i]*muosWellP[i]))
    
        #print('Gs[i]=',Gs[i],'Go[i]=',Go[i],'bo[i]=',bo[i])
        #print('y=',y)
#        return (p1,p2,ps,Gs,sk,nu,phi)

    def getControlSum1():
        pass
        


        
    def optimizeRRGModel():
        # ця процедура має оптимізувати параметри проекту, самі дані проекту мають бути вхідними даними
        # що зробити:
        # 1. Вибрати проект і прочитати з нього дані.
        # 2. Підібрати параметри РРГ.
        print('Заходжу в PrepareData')
        PreparedProjectData=prepareData()
        #    print('Запаси нафти=',PreparedProjectData[0][1])
        ObjectRates=PreparedProjectData[3]
        ObQo=ObjectRates[1]
        #    print('Qo=',ObQo)
        ObQg=ObjectRates[7]
        ObsumQg=ObjectRates[8]
        ObNuOil=ObjectRates[11]
        LastPoint=len(ObQg)
        LastNuOil=ObjectRates[11][LastPoint-1]
        LastsumQg=ObjectRates[8][LastPoint-1]
        #CountRRGOptimCriteriumH([2.685,2.161])
        # 
        print('Хочу зайти у функцію мінімізації')
        #    res=minimize(CountRRGOptimCriteriumH,[2.685],method='L-BFGS-B')
        res=minimize(CountRRGOptimCriteriumDiffYearGas,[2.685,2.1612],method='L-BFGS-B',bounds=[(1.0,7.0),(1.0,7.0)])
        print('Це я вже після функції мінімізації')
        h=res.x[0]
        k=res.x[1]
        # Дуже добре, отримав h і k, тепер дивлюся, що з того вийшло
        # Роблю розрахунок РРГ при отриманих h і k
        res=simpleRRG(PreparedProjectData,h,k,True)
        # Доповнюю розрахунок по РРГ видобутками нафти і газу
        p2=res[1]
        Gs=res[3]
        sk=res[4]
        nuOil=res[5]
        phi=res[6]
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
            print(' i','|','p2[i]','  sk[i]',' Gs[i]',' nu[i]','   Qo[i]','sumQo[i]',' Qg[i]','sumQG[i]')
            print('-'*99)
            for i in range(len(Gs)):
                #        print(i,p2[i],sk[i],Gs[i],nuOil[i],RRG_Qo[i],RRG_sumQo[i],RRG_Qg[i],RRG_sumQg[i])
                print("%2d | %4.1f %7.3f %7.1f %6.3f %7.1f %7.1f %7.1f %7.1f" % (i,p2[i],sk[i],Gs[i],nuOil[i],RRG_Qo[i],RRG_sumQo[i],RRG_Qg[i],RRG_sumQg[i]))
        # Ніби вийшло гарно, тепер треба фактичні дані доповнити тиском, річним і накопиченим видобутками газу
        tck = interpolate.splrep(nuOil, p2, s=0)
        ObP = interpolate.splev(ObNuOil, tck, der=0)
        #    print(ObP)
        tck = interpolate.splrep(nuOil, RRG_Qg, s=0)
        ObRRGQg = interpolate.splev(ObNuOil, tck, der=0)
        #    print(ObRRGQg)
        tck = interpolate.splrep(nuOil, RRG_sumQg, s=0)
        ObRRGsumQg = interpolate.splev(ObNuOil, tck, der=0)
        for i in range(len(ObsumQg)):
            print(ObRRGQg[i],ObQg[i],ObRRGsumQg[i],ObsumQg[i])
        # Тут можна доробити ще кілька варіантів оптимізації
        
        
        # прогнозування роботи свердловин
        # Приймаю, що мені відомий вибійний тиск, оскільки насос спущений на певну глибину
        tck = interpolate.splrep(nuOil, phi, s=0)
        ObPhi = interpolate.splev(ObNuOil, tck, der=0)
        pz=2
        LastPoint=len(ObQo)
        #    print(len(ObQo),len(ObPhi),len(ObP))
        kProd=ObQo[LastPoint-1]/(ObPhi[LastPoint-1]*(ObP[LastPoint-1]-pz))
        # Д
        #    print(kProd)

    def setWellRates(self,wellList):
        # тут wellList є списком із попарними величинами:
        # назва св., коеф.прод., вибійний тиск
        self.qWells=[]
        for well in wellList:
            name=well[0]
            kp=well[1]
            pc=well[2]
            qWell=[]
            for i in range(self.numOfRRGPoints):
                qWell.append(kp*(self.ps[i]-pc)*self.phi[i])
        self.qWells.append(qWell)
        self.sumQWell=[]
        for i in range(self.numOfRRGPoints):
            sum=0
            for q in self.qWells[i]:
                sum=sum+q
            self.sumQWell.append(sum)
     
    def getSk(self,p):
        print(self.sk,self.ps)
        tck = interpolate.splrep(self.sk, self.ps, s=0)
        
        return interpolate.splev(p, tck, der=0)

    def getPk(self,nuOil):
        tck = interpolate.splrep(self.nuOil, self.p2, s=0)
        return interpolate.splev(nuOil, tck, der=0)
         
        