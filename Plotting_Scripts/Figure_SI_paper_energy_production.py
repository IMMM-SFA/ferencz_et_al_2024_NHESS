# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 14:37:26 2021

@author: sbferen
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

os.chdir("Path to Data")
power_df = pd.read_csv("Basin_Power_Plants_EIA.csv", na_values = -999)
power_df.fillna(0, inplace = True)

 
labels = list(power_df.PrimSource.unique())
labels = ['Year'] + labels
K = pd.DataFrame(data = np.zeros((260,len(labels))), columns = labels)
F = pd.DataFrame(data = np.zeros((260,len(labels))), columns = labels)
O = pd.DataFrame(data = np.zeros((260,len(labels))), columns = labels)
Basin = pd.DataFrame(data = np.zeros((260,len(labels))), columns = labels)


for i in range(len(labels)-1):
    source = labels[i+1]
    
    data = power_df.copy()
    data = data.where(data.PrimSource == source)
    data = data.dropna()
    Basin.iloc[:,i+1] = np.sum(data.iloc[:,32:]).values
    
    data_K = data.copy()
    data_K = data_K.where(data.Region == 'K')
    data_K = data_K.dropna()
    K.iloc[:,i+1] = np.sum(data_K.iloc[:,32:]).values
    
    data_F = data.copy()
    data_F = data_F.where(data.Region == 'F')
    data_F = data_F.dropna()
    F.iloc[:,i+1] = np.sum(data_F.iloc[:,32:]).values

    data_O = data.copy()
    data_O = data_O.where(data.Region == 'O')
    data_O = data_O.dropna()
    O.iloc[:,i+1] = np.sum(data_O.iloc[:,32:]).values
    

    
Basin_summer = np.zeros((21, 10))
Basin_annual = np.zeros((21, 10))

for i in range(21):
    for j in range(9):
        Basin_summer[i,j+1] = np.sum(Basin.iloc[i*12+5:i*12+8, j+1])
        Basin_annual[i,j+1] = np.sum(Basin.iloc[i*12:(i+1)*12, j+1])
    

# Basin annual production, linear scale 
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
x = np.linspace((2001 + 1/12),(2022 + 8/12), 260, endpoint = True)
#axs.plot(x, power_df.iloc[68, 32:], label = 'Fayette')
axs.plot(np.arange(21)+2000, Basin_annual[:,6], label = 'Coal', color = 'red')
axs.plot(np.arange(21)+2000, Basin_annual[:,7], label = 'Nuclear', color = 'black')
axs.plot(np.arange(21)+2000, Basin_annual[:,2], label = 'Wind', color = 'green')
axs.plot(np.arange(21)+2000, Basin_annual[:,1], label = 'Gas', color = 'purple')
axs.plot(np.arange(21)+2000, Basin_annual[:,5], label = 'Hydro', color = 'blue')
axs.plot(np.arange(21)+2000, Basin_annual[:,3], label = 'Solar', color = 'gold')

plt.legend()
axs.set_xlim([2000, 2020])
#axs.set_ylim([0, 1.25*10**7])
#plt.yscale('log')
axs.xaxis.set_major_locator(MultipleLocator(5))
axs.xaxis.set_minor_locator(MultipleLocator(1))

# Basin annual production, log scale 
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
x = np.linspace((2001 + 1/12),(2022 + 8/12), 260, endpoint = True)
#axs.plot(x, power_df.iloc[68, 32:], label = 'Fayette')
axs.plot(np.arange(21)+2000, Basin_annual[:,6], label = 'Coal', color = 'red')
axs.plot(np.arange(21)+2000, Basin_annual[:,7], label = 'Nuclear', color = 'black')
axs.plot(np.arange(21)+2000, Basin_annual[:,2], label = 'Wind', color = 'green')
axs.plot(np.arange(21)+2000, Basin_annual[:,1], label = 'Gas', color = 'purple')
axs.plot(np.arange(21)+2000, Basin_annual[:,5], label = 'Hydro', color = 'blue')
axs.plot(np.arange(21)+2000, Basin_annual[:,3], label = 'Solar', color = 'gold')

plt.legend()
axs.set_xlim([2000, 2020])
#axs.set_ylim([0, 1.25*10**7])
plt.yscale('log')
axs.xaxis.set_major_locator(MultipleLocator(5))
axs.xaxis.set_minor_locator(MultipleLocator(1))
