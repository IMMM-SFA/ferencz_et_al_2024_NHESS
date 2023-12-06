# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 10:40:30 2022

@author: sbferen
"""

import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

os.chdir("C:/Users/fere556/OneDrive - PNNL/Documents/ERCOT/Retrospective_analysis/Data/Agg_Data")

Prod_F = pd.read_csv("Annual_crop_production_Region_F.csv", thousands=',') 
Prod_K = pd.read_csv("Annual_crop_production_Region_K.csv", thousands=',')
Prod_O = pd.read_csv("Annual_crop_production_Region_O.csv", thousands=',')

Acres_F =  pd.read_csv("Annual_crop_area_Region_F.csv", thousands=',')
Acres_K =  pd.read_csv("Annual_crop_area_Region_K.csv", thousands=',')
Acres_O =  pd.read_csv("Annual_crop_area_Region_O.csv", thousands=',')

Cattle_F = pd.read_csv("Cattle_region_F.csv", thousands=',')
Cattle_K = pd.read_csv("Cattle_region_K.csv", thousands=',')
Cattle_O = pd.read_csv("Cattle_region_O.csv", thousands=',')


#%% Agg impacts Figure

Fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(10,5))

# Row 1: Acres

# Cotton 
axs[0,0].plot(Prod_F.Year, Acres_F.iloc[:,2]/1000, color = 'black', linestyle = '-')
axs[0,0].plot(Prod_O.Year, Acres_O.iloc[:,1]/1000, color = 'gray', linestyle ='-')
axs[0,0].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[0,0].vlines([2008, 2015], ymin = 0, ymax = 1200,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[0,0].set_ylim([0, 1100])
axs[0,0].xaxis.set_major_locator(MultipleLocator(5))
axs[0,0].xaxis.set_minor_locator(MultipleLocator(1))
axs[0,0].set_ylabel('Harvested acres (10^3)')

# Corn
axs[0,1].plot(Prod_K.Year, Acres_K.iloc[:,1]/1000, color = 'black', linestyle = '-')
axs[0,1].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[0,1].vlines([2008, 2015], ymin = 0, ymax = 10 + max(Prod_K.iloc[:,5])/1000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[0,1].set_ylim([50, 200])
axs[0,1].xaxis.set_major_locator(MultipleLocator(5))
axs[0,1].xaxis.set_minor_locator(MultipleLocator(1))

# Wheat 
axs[0,2].plot(Prod_F.Year, Acres_F.iloc[:,1]/1000, color = 'black', linestyle = '-')
axs[0,2].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[0,2].vlines([2008, 2015], ymin = 0, ymax = 350,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[0,2].set_ylim([0, 350])
axs[0,2].xaxis.set_major_locator(MultipleLocator(5))
axs[0,2].xaxis.set_minor_locator(MultipleLocator(1))

# Rice 
axs[0,3].plot(Prod_K.Year, Acres_K.iloc[:,4]/1000, color = 'black', linestyle = '-')
axs[0,3].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[0,3].vlines([2008, 2015], ymin = 0, ymax = 110,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[0,3].set_ylim([0, 110])
axs[0,3].xaxis.set_major_locator(MultipleLocator(5))
axs[0,3].xaxis.set_minor_locator(MultipleLocator(1))

# Row 2: Yeilds 

# Cotton
axs[1,0].plot(Prod_F.Year, (Prod_F.iloc[:,3])/1000, color = 'black', linestyle = '-')
axs[1,0].plot(Prod_O.Year, (Prod_O.iloc[:,1])/1000, color = 'gray', linestyle ='-')
axs[1,0].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[1,0].vlines([2008, 2015], ymin = 0, ymax = 1700,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[1,0].set_ylim([0, 1700])
axs[1,0].xaxis.set_major_locator(MultipleLocator(5))
axs[1,0].xaxis.set_minor_locator(MultipleLocator(1))
axs[1,0].set_ylabel('Yield units (10^3)')

# Corn 
axs[1,1].plot(Prod_K.Year, Prod_K.iloc[:,2]/1000, color = 'black', linestyle = '-')
axs[1,1].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[1,1].vlines([2008, 2015], ymin = 0, ymax = 20000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[1,1].set_ylim([5000, 20000])
axs[1,1].xaxis.set_major_locator(MultipleLocator(5))
axs[1,1].xaxis.set_minor_locator(MultipleLocator(1))

# Wheat 
axs[1,2].plot(Prod_F.Year, Prod_F.iloc[:,2]/1000, color = 'black', linestyle = '-')
axs[1,2].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[1,2].vlines([2008, 2015], ymin = 0, ymax = 10500,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[1,2].set_ylim([0, 10500])
axs[1,2].xaxis.set_major_locator(MultipleLocator(5))
axs[1,2].xaxis.set_minor_locator(MultipleLocator(1))

# Rice 
axs[1,3].plot(Prod_K.Year, Prod_K.iloc[:,6]/1000, color = 'black', linestyle = '-')
axs[1,3].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[1,3].vlines([2008, 2015], ymin = 0, ymax = 10000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[1,3].set_ylim([2000, 9000])
axs[1,3].xaxis.set_major_locator(MultipleLocator(5))
axs[1,3].xaxis.set_minor_locator(MultipleLocator(1))

# Row 3: Yield/Acre

# Cotton 
axs[2,0].plot(Prod_F.Year, Prod_F.iloc[:,3]/Acres_F.iloc[:,2], color = 'black', linestyle = '-')
axs[2,0].plot(Prod_O.Year, Prod_O.iloc[:,1]/Acres_O.iloc[:,1], color = 'gray', linestyle ='-')
axs[2,0].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[2,0].vlines([2008, 2015], ymin = 0, ymax = 10 + max(Prod_K.iloc[:,5])/1000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[2,0].set_ylim([0, 2])
axs[2,0].xaxis.set_major_locator(MultipleLocator(5))
axs[2,0].xaxis.set_minor_locator(MultipleLocator(1))
axs[2,0].set_ylabel('Yield/Acre (-)')

# Corn 
axs[2,1].plot(Prod_K.Year, Prod_K.iloc[:,2]/Acres_K.iloc[:,1], color = 'black', linestyle = '-')
axs[2,1].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[2,1].vlines([2008, 2015], ymin = 0, ymax = 10 + max(Prod_K.iloc[:,5])/1000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[2,1].set_ylim([50, 130])
axs[2,1].xaxis.set_major_locator(MultipleLocator(5))
axs[2,1].xaxis.set_minor_locator(MultipleLocator(1))

# Wheat
axs[2,2].plot(Prod_F.Year, Prod_F.iloc[:,2]/Acres_F.iloc[:,1], color = 'black', linestyle = '-')
axs[2,2].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[2,2].vlines([2008, 2015], ymin = 0, ymax = 10 + max(Prod_K.iloc[:,5])/1000,
                  color = 'red', linestyle = ':', linewidth = 2)


axs[2,2].set_ylim([15, 35])
axs[2,2].xaxis.set_major_locator(MultipleLocator(5))
axs[2,2].xaxis.set_minor_locator(MultipleLocator(1))

# Rice 
axs[2,3].plot(Prod_K.Year,  Prod_K.iloc[:,6]/Acres_K.iloc[:,4], color = 'black', linestyle = '-')
axs[2,3].set_xlim([2000,2020]), axs[0,0].set_xlim([2000,2020]), axs[0,2].set_xlim([2000,2020])
axs[2,3].vlines([2008, 2015], ymin = 0, ymax = 10 + max(Prod_K.iloc[:,5])/1000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[2,3].set_ylim([60, 100])
axs[2,3].xaxis.set_major_locator(MultipleLocator(5))
axs[2,3].xaxis.set_minor_locator(MultipleLocator(1))

plt.tight_layout()

plt.savefig("Agg_impacts_ts.svg", format="svg")

# Row 4 (separate plot, cattle)
Cattle_data = np.zeros((21, 4))
Cattle_data[:,0] = np.arange(21) + 2000

years = np.arange(21) + 2000
cattle_by_year = np.zeros((years.size,2))
cattle_by_year[:,0] = years 
 
region = [Cattle_F, Cattle_K, Cattle_O]
for j in range(3):       
    for i in range(years.size):
        data = region[j].where(region[j].Year == years[i])
        data.dropna(inplace = True, how = 'all')
        Cattle_data[i,j+1] = data.Value.sum(axis = 0)
        
Fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(7,2))
axs[1].plot(years, (Cattle_data[:,1])/1000, color = 'black', linestyle ='-')#, label = 'Region F')
# axs[1].hlines(np.mean(Cattle_data[0:8,1])/1000, xmin = 2000, xmax = 2008, color = 'red')
# axs[1].hlines(np.mean(Cattle_data[8:16,1])/1000, xmin = 2008, xmax = 2015, color = 'red')
# axs[1].hlines(np.mean(Cattle_data[16:,1])/1000, xmin = 2015, xmax = 2020, color = 'red')

axs[0].plot(years, (Cattle_data[:,2])/1000, color = 'black', linestyle ='-')#, label = 'Region K')
# axs[0].hlines(np.mean(Cattle_data[0:8,2])/1000, xmin = 2000, xmax = 2008, color = 'red')
# axs[0].hlines(np.mean(Cattle_data[8:16,2])/1000, xmin = 2008, xmax = 2015, color = 'red')
# axs[0].hlines(np.mean(Cattle_data[16:,2])/1000, xmin = 2015, xmax = 2020, color = 'red')

axs[2].plot(years, (Cattle_data[:,3])/1000, color = 'black', linestyle ='-')#, label = 'Region O')
# axs[2].hlines(np.mean(Cattle_data[0:8,3])/1000, xmin = 2000, xmax = 2008, color = 'red')
# axs[2].hlines(np.mean(Cattle_data[8:16,3])/1000, xmin = 2008, xmax = 2015, color = 'red')
# axs[2].hlines(np.mean(Cattle_data[16:,3])/1000, xmin = 2015, xmax = 2020, color = 'red')

axs[1].set_xlim([2000,2020]), axs[0].set_xlim([2000,2020]), axs[2].set_xlim([2000,2020])
axs[0].vlines([2008, 2015], ymin = 0, ymax = 10+max(Cattle_data[:,2])/1000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[1].vlines([2008, 2015], ymin = 0, ymax = 30+max(Cattle_data[:,1])/1000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[2].vlines([2008, 2015], ymin = 0, ymax = 10+max(Cattle_data[:,3])/1000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[0].set_ylim([500, 800])
axs[1].set_ylim([350, 650])
axs[2].set_ylim([50, 100])
axs[0].xaxis.set_major_locator(MultipleLocator(5))
axs[0].xaxis.set_minor_locator(MultipleLocator(1))
axs[1].xaxis.set_major_locator(MultipleLocator(5))
axs[1].xaxis.set_minor_locator(MultipleLocator(1))
axs[2].xaxis.set_major_locator(MultipleLocator(5))
axs[2].xaxis.set_minor_locator(MultipleLocator(1))
# axs.xaxis.set_major_locator(MultipleLocator(5))
# axs.xaxis.set_minor_locator(MultipleLocator(1))
# axs.yaxis.set_major_locator(MultipleLocator(100))
# axs.yaxis.set_minor_locator(MultipleLocator(50))
# axs.set_ylabel('Cattle 10^3 head')
# plt.legend(bbox_to_anchor=(1.04, 0.7))
plt.tight_layout()
plt.savefig("Agg_impacts_ts_cattle.svg", format="svg")


