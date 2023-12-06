# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 11:37:17 2022

@author: sbferen
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import seaborn as sns
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

os.chdir('C:/Users/fere556/OneDrive - PNNL/Documents/ERCOT/Retrospective_analysis\Data')

region_k_res = pd.read_csv('Region_K_per_capita_storage.csv')
region_F_res = pd.read_csv('Region_F_reservoir_storage.csv')

huc_1208_dm = pd.read_csv('Drought_Monitor_1208.csv')
huc_1209_dm = pd.read_csv('Drought_Monitor_1209.csv')

#%% Drought Monitor data processessing and plotting 

test_date = mdates.date2num(np.datetime64(huc_1208_dm.MapDate[0]))

# Add numeric date column to dataframes 
huc_1208_dm['num_Date'] = np.zeros(len(huc_1208_dm.iloc[:,0]))
huc_1209_dm['num_Date'] = np.zeros(len(huc_1209_dm.iloc[:,0]))

for i in range(len(huc_1208_dm.iloc[:,0])):
    huc_1208_dm.num_Date[i] = mdates.date2num(np.datetime64(huc_1208_dm.MapDate[i]))
    
for i in range(len(huc_1209_dm.iloc[:,0])):
    huc_1209_dm.num_Date[i] = mdates.date2num(np.datetime64(huc_1209_dm.MapDate[i]))
    
unique_dates_1208 = huc_1208_dm.num_Date.unique()
unique_dates_1209 = huc_1209_dm.num_Date.unique()

fields = ['Date','D0','D1','D2','D3','D4']
drought_data_1208 = pd.DataFrame(data = np.zeros((len(unique_dates_1208),6)), columns = fields)
drought_data_1209 = pd.DataFrame(data = np.zeros((len(unique_dates_1209),6)), columns = fields)

drought_data_1208.Date = unique_dates_1208
drought_data_1209.Date = unique_dates_1209

for i in range(len(drought_data_1208.Date)):
    date_filter = huc_1208_dm.where(huc_1208_dm.num_Date == drought_data_1208.Date[i])
    date_filter.dropna(thresh = 6, inplace = True)
    date_filter.reset_index(inplace = True)
    
    for j in range(len(date_filter.iloc[:,0])):
        if date_filter.USDMLevel[j].rstrip() == 'D0':
            drought_data_1208.D0[i] = date_filter.PercentCurrent[j]
        if date_filter.USDMLevel[j].rstrip() == 'D1':
            drought_data_1208.D1[i] = date_filter.PercentCurrent[j]
        if date_filter.USDMLevel[j].rstrip() == 'D2':
            drought_data_1208.D2[i] = date_filter.PercentCurrent[j]
        if date_filter.USDMLevel[j].rstrip() == 'D3':
            drought_data_1208.D3[i] = date_filter.PercentCurrent[j]
        if date_filter.USDMLevel[j].rstrip() == 'D4':
            drought_data_1208.D4[i] = date_filter.PercentCurrent[j]
            
for i in range(len(drought_data_1209.Date)):
    date_filter = huc_1209_dm.where(huc_1209_dm.num_Date == drought_data_1209.Date[i])
    date_filter.dropna(thresh = 6, inplace = True)
    date_filter.reset_index(inplace = True)
    
    for j in range(len(date_filter.iloc[:,0])):
        if date_filter.USDMLevel[j].rstrip() == 'D0':
            drought_data_1209.D0[i] = date_filter.PercentCurrent[j]
        if date_filter.USDMLevel[j].rstrip() == 'D1':
            drought_data_1209.D1[i] = date_filter.PercentCurrent[j]
        if date_filter.USDMLevel[j].rstrip() == 'D2':
            drought_data_1209.D2[i] = date_filter.PercentCurrent[j]
        if date_filter.USDMLevel[j].rstrip() == 'D3':
            drought_data_1209.D3[i] = date_filter.PercentCurrent[j]
        if date_filter.USDMLevel[j].rstrip() == 'D4':
            drought_data_1209.D4[i] = date_filter.PercentCurrent[j]

# HUC 1208
plt.figure(figsize = (6, 2))
colors = ['gold', 'gold', 'darkorange','red', 'darkred']
for i in range(4):
    plt.fill_between(mdates.num2date(drought_data_1208.Date), drought_data_1208.iloc[:,i+2], 
                     color = colors[i+1])
    plt.xlim([datetime.date(2000, 1, 1), datetime.date(2020, 12, 31)])

plt.ylabel('% basin area')
plt.xlabel('year')
# HUC 1209
plt.figure(figsize = (6, 2))
colors = ['gold', 'gold', 'darkorange','red', 'darkred']
for i in range(4):
    plt.fill_between(mdates.num2date(drought_data_1209.Date), drought_data_1209.iloc[:,i+2], 
                     color = colors[i+1])
    plt.xlim([datetime.date(2000, 1, 1), datetime.date(2020, 12, 31)])
    
plt.ylabel('% basin area')
plt.xlabel('year')

#%% Per capita storage (acre-ft/per person)

fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(8, 3))

# Region F
axs[0].plot(region_k_res.iloc[3653:29950,1], region_F_res.iloc[3653:29950,11], 
            color = 'black')
axs[0].set_xlabel('Year')
axs[0].set_ylabel('Acre-ft/person')
axs[0].set_xlim([1950, 2021])
axs[0].yaxis.set_major_locator(MultipleLocator(0.5))
axs[0].yaxis.set_minor_locator(MultipleLocator(0.25))
axs[0].xaxis.set_major_locator(MultipleLocator(20))
axs[0].xaxis.set_minor_locator(MultipleLocator(5))

# Region K
axs[1].plot(region_k_res.iloc[3653:29950,1], region_k_res.Storage_per_capita[3653:29950], 
            color = 'black')
axs[1].set_xlabel('Year')
axs[1].set_xlim([1950, 2021])
axs[1].yaxis.set_major_locator(MultipleLocator(1))
axs[1].yaxis.set_minor_locator(MultipleLocator(0.5))
axs[1].xaxis.set_major_locator(MultipleLocator(20))
axs[1].xaxis.set_minor_locator(MultipleLocator(5))

# Combined K and F
axs[2].plot(region_k_res.iloc[3653:29950,1], (region_F_res.iloc[3653:29950,7] + \
                    region_k_res.conservation_storage[3653:29950].values)/  \
                 (region_k_res.iloc[3653:29950,6]+region_F_res.iloc[3653:29950:,10]), 
                 color = 'black')
axs[2].set_xlabel('Year')
axs[2].set_xlim([1950, 2021])
axs[2].yaxis.set_major_locator(MultipleLocator(0.5))
axs[2].yaxis.set_minor_locator(MultipleLocator(0.25))
axs[2].xaxis.set_major_locator(MultipleLocator(20))
axs[2].xaxis.set_minor_locator(MultipleLocator(5))
#axs[1].ylabel('Acft/person')
plt.tight_layout()

#%% Paper Figure 1: reservoir storage and drought monitor data 

fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(4, 8))
axs[1].plot(region_F_res.iloc[:,1], 1233.48 * region_F_res.iloc[:,7].values/(10**6), 
         color = 'black')
axs[1].plot([2000,2021],[1.9 * 1233.48, 1233.48* 1.9], color = 'black', linestyle = ':')
#axs[1].set_xlabel('Year')
axs[1].set_ylabel('Storage (Million m^3)')
axs[1].set_xlim([2000, 2021])
#axs[1].set_ylim([0,2])
axs[1].yaxis.set_major_locator(MultipleLocator(500))
axs[1].yaxis.set_minor_locator(MultipleLocator(250))
axs[1].xaxis.set_major_locator(MultipleLocator(5))
axs[1].xaxis.set_minor_locator(MultipleLocator(1))
#axs[0].title('Region F Combined Storage 1940-2020')
axs[1].grid(visible = True, axis = 'y', which = 'both')


axs[2].plot(region_k_res.iloc[:,1], 1233.48 * region_k_res.conservation_storage[:].values/(10**6), 
        color = 'black')
axs[2].plot([2000,2025],[1233.48 * 2.1, 1233.48 * 2.1], color = 'black', linestyle = ':')
#axs[2].set_xlabel('Year')
#axs[2].set_ylabel('Storage (Million Acft)')
#axs[1].set_ylabel('Storage (Million Acft)')
axs[2].set_xlim([2000, 2021])
#axs[2].set_ylim([0,2.15])
axs[2].yaxis.set_major_locator(MultipleLocator(500))
axs[2].yaxis.set_minor_locator(MultipleLocator(250))
axs[2].xaxis.set_major_locator(MultipleLocator(5))
axs[2].xaxis.set_minor_locator(MultipleLocator(1))
#axs[1].title('Region K Combined Storage 1940-2020')
axs[2].grid(visible = True, axis = 'y', which = 'both')

axs[3].plot(region_k_res.iloc[21915:29950,1], 1233.48 * (region_F_res.iloc[21915:29950,7] + \
                    region_k_res.conservation_storage[21915:29950].values)/(10**6), 
         color = 'black')
axs[3].plot([2000,2021],[1233.48 * 4, 1233.48 *4], color = 'black', linestyle = ':')
axs[3].set_xlabel('Year')
axs[3].set_ylabel('Storage (Million m^3)')

axs[2].set_ylabel('Storage (Million m^3)')
axs[3].set_xticks([1940,1950,1960,1970,1980,1990,2000,2010,2020])
axs[3].set_xlim([2000, 2021])
#axs[3].set_ylim([0,4.1])
axs[3].yaxis.set_major_locator(MultipleLocator(1000))
axs[3].yaxis.set_minor_locator(MultipleLocator(500))
axs[3].xaxis.set_major_locator(MultipleLocator(5))
axs[3].xaxis.set_minor_locator(MultipleLocator(1))
axs[3].grid(visible = True, axis = 'y', which = 'both')

colors = ['gold', 'gold', 'darkorange','red', 'darkred']
for i in range(4):
    axs[0].fill_between(mdates.num2date(drought_data_1209.Date), drought_data_1209.iloc[:,i+2], 
                     color = colors[i+1])
    #axs[0].set_ylabel('% Area')
    axs[0].set_xlim([datetime.date(2000, 1, 1), datetime.date(2020, 12, 31)])
    # axs[0].set_xticks([datetime.date(2000, 1, 1), datetime.date(2005, 1, 1), 
    #                   datetime.date(2010, 1, 1), datetime.date(2015, 1, 1), 
    #                   datetime.date(2020, 1, 1)], labels = [2000, 2005, 2010, 
    #                                                         2015, 2020])
    axs[0].set_xticks([datetime.date(2005, 1, 1), 
                      datetime.date(2010, 1, 1), datetime.date(2015, 1, 1), 
                      datetime.date(2020, 1, 1)], labels = [2005, 2010, 
                                                            2015, 2020])                                                        
plt.tight_layout()

plt.savefig("Figure_1_Drought_index_and_Res_storage.svg", format="svg")


#%% Alternative figure with reservoir storage as % of total storage and drought monitor data 

fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(3, 6))
axs[1].plot(region_F_res.iloc[:,1], region_F_res.iloc[:,7].values/(1.9*10**6), 
         color = 'black')
axs[1].plot([2000,2021],[1.9,1.9], color = 'black', linestyle = ':')
#axs[1].set_xlabel('Year')
#axs[1].set_ylabel('Storage (Million Acft)')
axs[1].set_xlim([2000, 2021])
axs[1].set_ylim([0,1])
axs[1].yaxis.set_major_locator(MultipleLocator(0.5))
axs[1].yaxis.set_minor_locator(MultipleLocator(0.1))
axs[1].xaxis.set_major_locator(MultipleLocator(5))
axs[1].xaxis.set_minor_locator(MultipleLocator(1))
#axs[0].title('Region F Combined Storage 1940-2020')
axs[1].grid(visible = True, axis = 'y', which = 'both')


axs[2].plot(region_k_res.iloc[:,1], region_k_res.conservation_storage[:].values/(2.1*10**6), 
        color = 'black')
axs[2].plot([2000,2021],[2.1,2.1], color = 'black', linestyle = ':')
#axs[2].set_xlabel('Year')
#axs[2].set_ylabel('Storage (Million Acft)')
#axs[1].set_ylabel('Storage (Million Acft)')
axs[2].set_xlim([2000, 2021])
axs[2].set_ylim([0,1])
axs[2].yaxis.set_major_locator(MultipleLocator(0.5))
axs[2].yaxis.set_minor_locator(MultipleLocator(0.1))
axs[2].xaxis.set_major_locator(MultipleLocator(5))
axs[2].xaxis.set_minor_locator(MultipleLocator(1))
#axs[1].title('Region K Combined Storage 1940-2020')
axs[2].grid(visible = True, axis = 'y', which = 'both')


axs[3].plot(region_k_res.iloc[21915:29950,1], (region_F_res.iloc[21915:29950,7] + \
                    region_k_res.conservation_storage[21915:29950].values)/(4.1*10**6), 
         color = 'black')
axs[3].plot([2000,2021],[4,4], color = 'black', linestyle = ':')
axs[3].set_xlabel('Year')
#axs[3].set_ylabel('Storage (Million Acft)')

#axs[2].set_ylabel('Storage (Million Acft)')
axs[3].set_xticks([1940,1950,1960,1970,1980,1990,2000,2010,2020])
axs[3].set_xlim([2000, 2021])
axs[3].set_ylim([0,1])
axs[3].yaxis.set_major_locator(MultipleLocator(0.5))
axs[3].yaxis.set_minor_locator(MultipleLocator(0.1))
axs[3].xaxis.set_major_locator(MultipleLocator(5))
axs[3].xaxis.set_minor_locator(MultipleLocator(1))
axs[3].grid(visible = True, axis = 'y', which = 'both')

colors = ['gold', 'gold', 'darkorange','red', 'darkred']
for i in range(4):
    axs[0].fill_between(mdates.num2date(drought_data_1209.Date), drought_data_1209.iloc[:,i+2], 
                     color = colors[i+1])
    #axs[0].set_ylabel('% Area')
    axs[0].set_xlim([datetime.date(2000, 1, 1), datetime.date(2020, 12, 31)])
    axs[0].set_xticks([datetime.date(2000, 1, 1), datetime.date(2005, 1, 1), 
                      datetime.date(2010, 1, 1), datetime.date(2015, 1, 1), 
                      datetime.date(2020, 1, 1)], labels = [2000, 2005, 2010, 
                                                            2015, 2020])

plt.tight_layout()




