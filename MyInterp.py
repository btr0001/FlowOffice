# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 10:22:46 2016

@author: taras
"""
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy

#class MyInterp(object):
    
def Interp(trendData1,trendData2,data1):
    f = interpolate.interp1d(trendData1,trendData2)
    y = f(data1)  
    return y
    
