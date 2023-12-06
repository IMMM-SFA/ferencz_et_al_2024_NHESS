# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 10:02:17 2022

@author: sbferen
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os 

#%%
os.chdir("C:/Users/fere556/OneDrive - PNNL/Documents/ERCOT/Retrospective_analysis/Data")

Region_K = pd.read_csv('GDP_region_K.csv', 
                                  thousands = ',')
Region_F = pd.read_csv('GDP_region_F.csv', 
                                  thousands = ',')
Region_O = pd.read_csv('GDP_region_O.csv', 
                                  thousands = ',')

Counties = pd.read_csv('Region_K_F_O_counties.csv')

cpi = pd.read_csv('inflation_correction.csv')

#%% Clean data 

regions = [Region_F, Region_K, Region_O]
for i in range(3):
    region = regions[i]
    for j in range(len(region.iloc[:,0])):
        for k in range(20):
            try: 
                if float(region.iloc[j,k+4]) >= 0:
                    continue 
                else:
                    region.iloc[j,k+4] = 0
                
            except ValueError:
                region.iloc[j,k+4] = 0
   
    regions[i] = region
    
#%% Subplots for Regional GDP by sector

years = np.arange(20)+2001

linecode = [1, 3, 6, 56]
categories = ['All industry', 'Agriculture', 'Oil, gas, mining', 
              'Real estate, rentals, leasing']

Fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(9,8))
for category in range(len(linecode)):
    F_data = Region_F.where(Region_F.LineCode[:] == linecode[category])
    F_data = F_data.dropna(thresh = 15)
    F_data = (np.array(F_data.iloc[:,4:])).astype('int')
    F_data_corrected = np.multiply(cpi.iloc[4:24,1],np.sum(F_data[:,:], axis = 0))/10**6
    F_data = np.sum(F_data[:,:], axis = 0)/10**6
    axs[category, 1].plot(years, F_data_corrected, color = 'k', label = 'F')
    #axs[category, 1].plot(years, F_data, color = 'k', label = 'F')
    axs[category, 1].vlines([2008, 2015], ymin = min(F_data_corrected), ymax = max(F_data_corrected), color = 'red', 
                  linestyle = ':', linewidth = 2)
    #axs[1].set_ylim([min(data_corrected), max(data_corrected)])
    axs[category, 1].xaxis.set_major_locator(MultipleLocator(10))
    axs[category, 1].xaxis.set_minor_locator(MultipleLocator(1))
    # axs[1].yaxis.set_major_locator(MultipleLocator(50))
    # axs[1].yaxis.set_minor_locator(MultipleLocator(25))
    #axs[1].set_title('Middle Basin')
    
    K_data = Region_K.where(Region_K.LineCode[:] == linecode[category])
    K_data = K_data.dropna(thresh = 15)
    K_data = (np.array(K_data.iloc[:,4:])).astype('int')
    K_data_corrected = np.multiply(cpi.iloc[4:24,1],np.sum(K_data[:,:], axis = 0))/10**6
    K_data = np.sum(K_data[:,:], axis = 0)/10**6
    #axs[category, 0].plot(years, K_data, color = 'k', label = 'K')
    axs[category, 0].plot(years, K_data_corrected, color = 'k', label = 'K')

    axs[category, 0].vlines([2008, 2015], ymin = min(K_data_corrected), ymax =  max(K_data_corrected),
                      color = 'red', linestyle = ':', linewidth = 2)
    #axs[0].set_ylim([min(data_corrected), max(data_corrected)])
    # axs[0].set_ylabel('Population (10^3)')
    axs[category, 0].xaxis.set_major_locator(MultipleLocator(10))
    axs[category, 0].xaxis.set_minor_locator(MultipleLocator(1))
    # axs[0].yaxis.set_major_locator(MultipleLocator(200))
    # axs[0].yaxis.set_minor_locator(MultipleLocator(100))
    #axs[category,0].set_title('Lower Basin')

    O_data = Region_O.where(Region_O.LineCode[:] == linecode[category])
    O_data = O_data.dropna(thresh = 15)
    O_data = (np.array(O_data.iloc[:,4:])).astype('int')
    O_data_corrected = np.multiply(cpi.iloc[4:24,1],np.sum(O_data[:,:], axis = 0))/10**6
    O_data = np.sum(O_data[:,:], axis = 0)/10**6
    #axs[category, 2].plot(years, O_data, color = 'k', label = 'O')
    axs[category, 2].plot(years, O_data_corrected, color = 'k', label = 'K')

    axs[category, 2].vlines([2008,2015], ymin = min(O_data_corrected), ymax = max(O_data_corrected),
                      color = 'red', linestyle = ':', linewidth = 2)
    #axs[2].set_ylim([min(data_corrected), max(data_corrected)])
    axs[category, 2].xaxis.set_major_locator(MultipleLocator(10))
    axs[category, 2].xaxis.set_minor_locator(MultipleLocator(1))
    # axs[2].yaxis.set_major_locator(MultipleLocator(2))
    # axs[2].yaxis.set_minor_locator(MultipleLocator(1))
    #axs[category, 2].set_title('Upper Basin')

    Basin_data = K_data + F_data + O_data
    Basin_corrected = K_data_corrected + F_data_corrected + O_data_corrected 
    #axs[category, 3].plot(years, Basin_data, color = 'k', label = 'O')
    axs[category, 3].plot(years, Basin_corrected, color = 'k', label = 'K')

    axs[category, 3].vlines([2008,2015], ymin = min(Basin_corrected), ymax = max(Basin_corrected),
                      color = 'red', linestyle = ':', linewidth = 2)
    #axs[2].set_ylim([min(data_corrected), max(data_corrected)])
    axs[category, 3].xaxis.set_major_locator(MultipleLocator(10))
    axs[category, 3].xaxis.set_minor_locator(MultipleLocator(1))
    # axs[2].yaxis.set_major_locator(MultipleLocator(2))
    # axs[2].yaxis.set_minor_locator(MultipleLocator(1))
    #axs[category, 2].set_title('Upper Basin')
        
    #plt.suptitle(categories[category])
    #plt.tight_layout()

# Total industry minus oil and gas 

#Fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(8,3))
F_data_OG = Region_F.where(Region_F.LineCode[:] == 6)
F_data_OG = F_data_OG.dropna(thresh = 15)
F_data_OG = (np.array(F_data_OG.iloc[:,4:])).astype('int')
F_data_all = Region_F.where(Region_F.LineCode[:] == 1)
F_data_all = F_data_all.dropna(thresh = 15)
F_data_all = (np.array(F_data_all.iloc[:,4:])).astype('int')
F_og_removed = F_data_all - F_data_OG
F_data_corrected = np.multiply(cpi.iloc[4:24,1],np.sum(F_og_removed[:,:], axis = 0))/10**6

F_data = np.sum(F_og_removed[:,:], axis = 0)/10**6
#axs[4,1].plot(years, F_data, color = 'black', label = 'F')
axs[4,1].plot(years, F_data_corrected, color = 'k', label = 'F')
axs[4,1].vlines([2008, 2015], ymin = min(F_data_corrected), ymax = max(F_data_corrected), color = 'red', 
              linestyle = ':', linewidth = 2)
axs[4,1].set_ylim([20, 42])
axs[4,1].xaxis.set_major_locator(MultipleLocator(10))
axs[4,1].xaxis.set_minor_locator(MultipleLocator(1))
# axs[1].yaxis.set_major_locator(MultipleLocator(50))
# axs[1].yaxis.set_minor_locator(MultipleLocator(25))
#axs[1].set_title('Middle Basin')

K_data_OG = Region_K.where(Region_K.LineCode[:] == 6)
K_data_OG = K_data_OG.dropna(thresh = 15)
K_data_OG = (np.array(K_data_OG.iloc[:,4:])).astype('int')
K_data_all = Region_K.where(Region_K.LineCode[:] == 1)
K_data_all = K_data_all.dropna(thresh = 15)
K_data_all = (np.array(K_data_all.iloc[:,4:])).astype('int')
K_og_removed = K_data_all - K_data_OG
K_data_corrected = np.multiply(cpi.iloc[4:24,1],np.sum(K_og_removed[:,:], axis = 0))/10**6

K_data= np.sum(K_og_removed[:,:], axis = 0)/10**6
#axs[4,0].plot(years, K_data, color = 'black', label = 'K')
axs[4,0].plot(years, K_data_corrected, color = 'k', label = 'K')
axs[4,0].vlines([2008, 2015], ymin = 0, ymax =  10+max(K_data_corrected),
                  color = 'red', linestyle = ':', linewidth = 2)
axs[4,0].set_ylim([75, 180])
# axs[0].set_ylabel('Population (10^3)')
axs[4,0].xaxis.set_major_locator(MultipleLocator(10))
axs[4,0].xaxis.set_minor_locator(MultipleLocator(1))
# axs[0].yaxis.set_major_locator(MultipleLocator(200))
# axs[0].yaxis.set_minor_locator(MultipleLocator(100))
#axs[4,0].set_title('Lower Basin')

O_data_OG = Region_O.where(Region_O.LineCode[:] == 6)
O_data_OG = O_data_OG.dropna(thresh = 15)
O_data_OG = (np.array(O_data_OG.iloc[:,4:])).astype('int')
O_data_all = Region_O.where(Region_O.LineCode[:] == 1)
O_data_all = O_data_all.dropna(thresh = 15)
O_data_all = (np.array(O_data_all.iloc[:,4:])).astype('int')
O_og_removed = O_data_all - O_data_OG
O_data_corrected = np.multiply(cpi.iloc[4:24,1],np.sum(O_og_removed[:,:], axis = 0))/10**6

O_data = np.sum(O_og_removed[:,:], axis = 0)/10**6
#axs[4,2].plot(years, O_data, color = 'black', label = 'O')
axs[4,2].plot(years, O_data_corrected, color = 'k', label = 'O')
axs[4,2].vlines([2008,2015], ymin = 0, ymax = 1+max(O_data_corrected),
                  color = 'red', linestyle = ':', linewidth = 2)
axs[4,2].set_ylim([1, 3])
axs[4,2].xaxis.set_major_locator(MultipleLocator(10))
axs[4,2].xaxis.set_minor_locator(MultipleLocator(1))
# axs[2].yaxis.set_major_locator(MultipleLocator(2))
# axs[2].yaxis.set_minor_locator(MultipleLocator(1))
#axs[2].set_title('Upper Basin')

all_data = K_data + O_data + F_data
Basin_corrected = K_data_corrected + F_data_corrected + O_data_corrected 

#axs[4,3].plot(years, all_data, color = 'black', label = 'K')
axs[4,3].plot(years, Basin_corrected, color = 'k')
axs[4,3].vlines([2008,2015], ymin = 0, ymax = 1+max(Basin_corrected),
                  color = 'red', linestyle = ':', linewidth = 2)
axs[4,3].set_ylim([100, 220])
axs[4,3].xaxis.set_major_locator(MultipleLocator(10))
axs[4,3].xaxis.set_minor_locator(MultipleLocator(1))
# axs[2].yaxis.set_major_locator(MultipleLocator(2))
# axs[2].yaxis.set_minor_locator(MultipleLocator(1))
#axs[2].set_title('Upper Basin')

#plt.suptitle('All industry minus oil, gas, mining')
plt.tight_layout()

plt.savefig("GDP_Figure.svg", format="svg")






