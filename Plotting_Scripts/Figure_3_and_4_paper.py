# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 12:57:31 2022

@author: sbferen
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os 

os.chdir("C:/Users/fere556/OneDrive - PNNL/Documents/ERCOT/Retrospective_analysis/Data")

County_water_use = pd.read_csv('SumFinal_CountyReport_2000_2020.csv', 
                                  thousands = ',')

Counties = pd.read_csv('Region_K_F_O_counties.csv')

plt.rcParams['font.size'] = 14

#%% Processing county data 
# Convert county names to all lowercase 
for i in range(len(Counties.iloc[:,0])):
    Counties.County[i] = Counties.County[i].lower()
    
for i in range(len(County_water_use.iloc[:,0])):
    County_water_use.CountyName[i] = County_water_use.CountyName[i].lower()
    
# Label counties in Region K, F, and O
County_water_use['Region'] = ['Other']*5334

for i in range(len(County_water_use.iloc[:,0])):
    for j in range(len(Counties.iloc[:,0])):
        if County_water_use.CountyName[i] == Counties.County[j] \
            and Counties.In_Colorado_Watershed[j] == 'Y':
            County_water_use.Region[i] = Counties.Region[j]

# Construct dataframes for sectoral use in each region 
labels = list(County_water_use.columns.values)
labels  = labels + ['Tot_Gw','Tot_Sw']

Region_K = pd.DataFrame(data = np.zeros((21,24)), columns = labels) 
Region_F = pd.DataFrame(data = np.zeros((21,24)), columns = labels) 
Region_O = pd.DataFrame(data = np.zeros((21,24)), columns = labels) 

Region_K.Year[:] = np.arange(21)+2000
Region_F.Year[:] = np.arange(21)+2000
Region_O.Year[:] = np.arange(21)+2000

years = np.arange(21) + 2000
for i in range(21): # number of rows (years)
    temp = County_water_use.copy()
    temp = temp.where(temp.Region == 'K')
    temp = temp.where(temp.Year == years[i])
    temp.dropna(inplace = True)
    Region_K.iloc[i,2:21] = temp.iloc[:,2:21].sum() 
    temp = County_water_use.copy()
    temp = temp.where(temp.Region == 'F')
    temp = temp.where(temp.Year == years[i])
    temp.dropna(inplace = True)
    Region_F.iloc[i,2:21] = temp.iloc[:,2:21].sum() 
    temp = County_water_use.copy()
    temp = temp.where(temp.Region == 'O')
    temp = temp.where(temp.Year == years[i])
    temp.dropna(inplace = True)
    Region_O.iloc[i,2:21] = temp.iloc[:,2:21].sum()


Region_F.Tot_Gw = Region_F.Muni_GW + Region_F.Mining_GW + Region_F.MFG_Gw + \
                  Region_F.Power_GW + Region_F.Livestock_GW + Region_F.Irrig_GW

Region_F.Tot_Sw = Region_F.Muni_SW + Region_F.Mining_SW + Region_F.MFG_SW + \
                  Region_F.Power_SW + Region_F.Livestock_SW + Region_F.Irrig_SW

Region_K.Tot_Gw = Region_K.Muni_GW + Region_K.Mining_GW + Region_K.MFG_Gw + \
                  Region_K.Power_GW + Region_K.Livestock_GW + Region_K.Irrig_GW

Region_K.Tot_Sw = Region_K.Muni_SW + Region_K.Mining_SW + Region_K.MFG_SW + \
                  Region_K.Power_SW + Region_K.Livestock_SW + Region_K.Irrig_SW
                  
Region_O.Tot_Gw = Region_O.Muni_GW + Region_O.Mining_GW + Region_O.MFG_Gw + \
                  Region_O.Power_GW + Region_O.Livestock_GW + Region_O.Irrig_GW 

Region_O.Tot_Sw = Region_O.Muni_SW + Region_O.Mining_SW + Region_O.MFG_SW + \
                  Region_O.Power_SW + Region_O.Livestock_SW + Region_O.Irrig_SW  
                  
#%% Convert from acre-ft to m^3

Region_F.iloc[:,3:] = Region_F.iloc[:,3:] * 1233.48 
Region_K.iloc[:,3:] = Region_K.iloc[:,3:] * 1233.48 
Region_O.iloc[:,3:] = Region_O.iloc[:,3:] * 1233.48 

#%% Population in each region - subplots

Fig, axs = plt.subplots(nrows=4, ncols=3, figsize=(12,10))
axs[0,1].plot(Region_F.Year, (Region_F.Population)/1000,
         color = 'black', label = 'Pop')
axs[0,1].vlines([2008, 2015], ymin = 0, ymax = 10+max(Region_F.Population[:])/1000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[0,1].set_ylim([-10+min(Region_F.Population[:])/1000, 10+max(Region_F.Population[:])/1000])
#axs[0,1].xaxis.set_major_locator(MultipleLocator(5))
axs[0,1].xaxis.set_minor_locator(MultipleLocator(1))
axs[0,1].yaxis.set_major_locator(MultipleLocator(50))
axs[0,1].yaxis.set_minor_locator(MultipleLocator(25))

axs[0,0].plot(Region_K.Year, (Region_K.Population)/1000,
         color = 'black', label = 'Pop')
axs[0,0].vlines([2008, 2015], ymin = 0, ymax = 50+max(Region_K.Population[:])/1000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[0,0].set_ylim([-50+(min(Region_K.Population[:]))/1000, 50+max(Region_K.Population[:])/1000])
axs[0,0].set_ylabel('Population 10\u00b3')
#axs[0,0].xaxis.set_major_locator(MultipleLocator(5))
axs[0,0].xaxis.set_minor_locator(MultipleLocator(1))
axs[0,0].yaxis.set_major_locator(MultipleLocator(200))
axs[0,0].yaxis.set_minor_locator(MultipleLocator(100))

axs[0,2].plot(Region_O.Year, (Region_O.Population)/1000,
         color = 'black', label = 'Pop')
axs[0,2].vlines([2008,2015], ymin = 0, ymax = (max(Region_O.Population[:])+10)/1000,
                  color = 'red', linestyle = ':', linewidth = 2)
axs[0,2].set_ylim([(min(Region_O.Population[:])-10)/1000, (max(Region_O.Population[:])+10)/1000])
#axs[0,2].xaxis.set_major_locator(MultipleLocator(5))
axs[0,2].xaxis.set_minor_locator(MultipleLocator(1))
axs[0,2].yaxis.set_major_locator(MultipleLocator(2))
axs[0,2].yaxis.set_minor_locator(MultipleLocator(1))

# total_pop = Region_F.Population + Region_K.Population + Region_O.Population
# axs[0,3].plot(Region_F.Year, total_pop/1000, color = 'k')
# axs[0,3].vlines([2008,2015], ymin = 0, ymax = (max(total_pop))/1000,
#                   color = 'red', linestyle = ':', linewidth = 2)
# axs[0,3].set_ylim([1700, 2600])

# # axs[0,3].xaxis.set_major_locator(MultipleLocator(5))
# axs[0,3].xaxis.set_minor_locator(MultipleLocator(1))
# # axs[0,3].yaxis.set_major_locator(MultipleLocator(2))
# # axs[0,3].yaxis.set_minor_locator(MultipleLocator(1))


# Total, SW, and GW use in each region  

#fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(8,2.5))
axs[1,1].plot(Region_F.Year, Region_F.Tot_Gw[:]/10**6, color = 'black', linestyle = '--', label = 'Gw')
axs[1,1].plot(Region_F.Year, Region_F.Tot_Sw[:]/10**6, color = 'black', label = 'Sw')
axs[1,1].scatter(Region_F.Year, Region_F.Tot_Sw[:]/10**6+Region_F.Tot_Gw[:]/10**6, 
               color = 'black', marker = 'o', s = 14, label = 'Tot')
axs[1,1].vlines([2008,2015], ymin = 0, ymax = 10+max(Region_F.Tot_Sw[:]/10**6+Region_F.Tot_Gw[:]/10**6),
                  color = 'red', linestyle = ':', linewidth = 2)
axs[1,1].set_ylim([45, 10+max(Region_F.Tot_Sw[:]/10**6+Region_F.Tot_Gw[:]/10**6)])
axs[1,1].xaxis.set_major_locator(MultipleLocator(5))
axs[1,1].xaxis.set_minor_locator(MultipleLocator(1))
axs[1,1].yaxis.set_major_locator(MultipleLocator(100))
axs[1,1].yaxis.set_minor_locator(MultipleLocator(25))


axs[1,0].plot(Region_K.Year, Region_K.Tot_Gw[:]/10**6, color = 'black', linestyle = '--', label = 'Gw')
axs[1,0].plot(Region_K.Year, Region_K.Tot_Sw[:]/10**6, color = 'black', label = 'Sw')
axs[1,0].scatter(Region_K.Year, Region_K.Tot_Sw[:]/10**6+Region_K.Tot_Gw[:]/10**6, 
               color = 'black', marker = 'o', s = 14, label = 'Tot')
axs[1,0].vlines([2008,2015], ymin = 0, ymax = 50+max(Region_K.Tot_Sw[:]/1000+Region_K.Tot_Gw[:]/1000),
                  color = 'red', linestyle = ':', linewidth = 2)
axs[1,0].set_ylim([0, 50+max(Region_K.Tot_Sw[:]/10**6+Region_K.Tot_Gw[:]/10**6)])
axs[1,0].set_ylabel('Water use 10\u00b3 acre-ft')
axs[1,0].xaxis.set_major_locator(MultipleLocator(5))
axs[1,0].xaxis.set_minor_locator(MultipleLocator(1))
axs[1,0].yaxis.set_major_locator(MultipleLocator(200))
axs[1,0].yaxis.set_minor_locator(MultipleLocator(100))

# axs_right = axs[1,2].twinx()
# axs_right.plot(Region_O.Year, Region_O.Tot_Sw[:]/1000, color = 'black', label = 'Sw')
# axs_right.set_ylabel('SW', color = 'black') #, fontsize = 14)
#axs[1,2].set_ylabel('GW, Tot')
axs[1,2].plot(Region_O.Year, Region_O.Tot_Gw[:]/10**6, color = 'black', linestyle = '--', label = 'Gw')
axs[1,2].plot(Region_O.Year, Region_O.Tot_Sw[:]/10**6, color = 'black', label = 'Sw')
axs[1,2].scatter(Region_O.Year, Region_O.Tot_Sw[:]/10**6+Region_O.Tot_Gw[:]/10**6,  
            color = 'black', marker = 'o', s = 14, label = 'Tot')
axs[1,2].vlines([2008,2015], ymin = 0, ymax = 50+max(Region_O.Tot_Sw[:]/10**6+Region_O.Tot_Gw[:]/10**6),
                  color = 'red', linestyle = ':', linewidth = 2)
axs[1,2].set_ylim([0, 50+max(Region_O.Tot_Sw[:]/10**6+Region_O.Tot_Gw[:]/10**6)])
axs[1,2].xaxis.set_major_locator(MultipleLocator(5))
axs[1,2].xaxis.set_minor_locator(MultipleLocator(1))
axs[1,2].yaxis.set_major_locator(MultipleLocator(200))
axs[1,2].yaxis.set_minor_locator(MultipleLocator(100))


# basin_SW = Region_K.Tot_Sw[:] + Region_F.Tot_Sw[:] + Region_O.Tot_Sw[:]
# basin_GW = Region_K.Tot_Gw[:] + Region_F.Tot_Gw[:] + Region_O.Tot_Gw[:]
# basin_tot = basin_SW + basin_GW
# axs[1,3].plot(Region_O.Year, basin_GW/1000, color = 'black', linestyle = '--', label = 'Gw')
# axs[1,3].plot(Region_O.Year, basin_SW/1000, color = 'black', label = 'Sw')
# axs[1,3].scatter(Region_O.Year, basin_tot/1000,  
#            color = 'black', marker = 'o', s = 14, label = 'Tot')
# axs[1,3].vlines([2008,2015], ymin = 0, ymax = 50+max(Region_O.Tot_Sw[:]/1000+Region_O.Tot_Gw[:]/1000),
#                   color = 'red', linestyle = ':', linewidth = 2)
# #axs[1,3].set_ylim([0, 50+max(Region_O.Tot_Sw[:]/1000+Region_O.Tot_Gw[:]/1000)])
# #axs[1,3].xaxis.set_major_locator(MultipleLocator(5))
# axs[1,3].xaxis.set_minor_locator(MultipleLocator(1))
# axs[1,3].yaxis.set_major_locator(MultipleLocator(500))
# axs[1,3].yaxis.set_minor_locator(MultipleLocator(250))


# Sectoral Water Use 

#fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(8,2.5))
axs[2,1].plot(Region_F.Year, Region_F.Irrigation[:]/10**6, color = 'tab:green', linewidth = 2, label = 'Irr')
axs[2,1].plot(Region_F.Year, Region_F.Municipal[:]/10**6, color = 'tab:blue', linewidth = 2, label = 'Mun')
axs[2,1].plot(Region_F.Year, Region_F.SteamElectric[:]/10**6, color = 'gray', linewidth = 2, label = 'Pow')
axs[2,1].plot(Region_F.Year, (Region_F.Mining[:]+Region_F.Manufactoring[:])/10**6,
         color = 'gold', linewidth = 2, label = 'Ind')
axs[2,1].vlines([2008, 2015], ymin = 0, ymax = 10+max(Region_F.Irrigation[:])/10**6,
                 color = 'red',  linestyle = ':', linewidth = 2)
axs[2,1].set_ylim([0, 10+max(Region_F.Irrigation[:])/10**6])
axs[2,1].xaxis.set_major_locator(MultipleLocator(5))
axs[2,1].xaxis.set_minor_locator(MultipleLocator(1))
axs[2,1].yaxis.set_major_locator(MultipleLocator(100))
axs[2,1].yaxis.set_minor_locator(MultipleLocator(25))

axs[2,0].plot(Region_K.Year, Region_K.Irrigation[:]/10**6, color = 'tab:green', linewidth = 2, label = 'Irr')
axs[2,0].plot(Region_K.Year, Region_K.Municipal[:]/10**6, color = 'tab:blue', linewidth = 2, label = 'Mun')
axs[2,0].plot(Region_K.Year, Region_K.SteamElectric[:]/10**6, color = 'gray', linewidth = 2, label = 'Pow')
axs[2,0].plot(Region_K.Year, (Region_K.Mining[:]+Region_K.Manufactoring[:])/10**6,
         color = 'gold', linewidth = 2, label = 'Ind')
axs[2,0].vlines([2008, 2015], ymin = 0, ymax = 50+max(Region_K.Irrigation[:])/10**6,
                 color = 'red',  linestyle = ':', linewidth = 2)
axs[2,0].set_ylim([0, 50 +max(Region_K.Irrigation[:])/10**6])
axs[2,0].set_ylabel('Sectoral use 10\u00b3 acre-ft')
axs[2,0].xaxis.set_major_locator(MultipleLocator(5))
axs[2,0].xaxis.set_minor_locator(MultipleLocator(1))
axs[2,0].yaxis.set_major_locator(MultipleLocator(200))
axs[2,0].yaxis.set_minor_locator(MultipleLocator(100))

axs[2,2].plot(Region_O.Year, Region_O.Irrigation[:]/10**6, color = 'tab:green', linewidth = 2, label = 'Irr')
axs[2,2].plot(Region_O.Year, Region_O.Municipal[:]/10**6, color = 'tab:blue', linewidth = 2, label = 'Mun')
axs[2,2].plot(Region_O.Year, Region_O.SteamElectric[:]/10**6, color = 'gray', linewidth = 2, label = 'Pow')
axs[2,2].plot(Region_O.Year, (Region_O.Mining[:]+Region_O.Manufactoring[:])/10**6,
         color = 'gold', linewidth = 2, label = 'Ind')
axs[2,2].vlines([2008, 2015], ymin = 0, ymax = 50 +max(Region_O.Irrigation[:])/10**6,
                 color = 'red',  linestyle = ':', linewidth = 2)
axs[2,2].set_ylim([0, 50+max(Region_O.Irrigation[:])/10**6])
axs[2,2].xaxis.set_major_locator(MultipleLocator(5))
axs[2,2].xaxis.set_minor_locator(MultipleLocator(1))
axs[2,2].yaxis.set_major_locator(MultipleLocator(200))
axs[2,2].yaxis.set_minor_locator(MultipleLocator(100))



#plt.tight_layout()

# Sectoral GW Use

#fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(8,2.5))
axs[3,1].plot(Region_F.Year, Region_F.Irrig_GW[:]/10**6, color = 'tab:green', linewidth = 2, label = 'Irr')
axs[3,1].plot(Region_F.Year, Region_F.Muni_GW[:]/10**6, color = 'tab:blue', linewidth = 2, label = 'Mun')
axs[3,1].plot(Region_F.Year, Region_F.Power_GW[:]/10**6, color = 'gray', linewidth = 2, label = 'Pow')
axs[3,1].plot(Region_F.Year, (Region_F.Mining_GW[:]+Region_F.MFG_Gw[:])/10**6,
         color = 'gold', linewidth = 2, label = 'Ind')
axs[3,1].vlines([2008, 2015], ymin = 0, ymax = 10 +max(Region_F.Irrig_GW[:])/10**6,
                 color = 'red', linestyle = ':', linewidth = 2)
axs[3,1].set_ylim([0, 10+ max(Region_F.Irrig_GW[:])/10**6])
axs[3,1].xaxis.set_major_locator(MultipleLocator(5))
axs[3,1].xaxis.set_minor_locator(MultipleLocator(1))
axs[3,1].yaxis.set_major_locator(MultipleLocator(50))
axs[3,1].yaxis.set_minor_locator(MultipleLocator(25))

axs[3,0].plot(Region_K.Year, Region_K.Irrig_GW[:]/10**6, color = 'tab:green', linewidth = 2, label = 'Irr')
axs[3,0].plot(Region_K.Year, Region_K.Muni_GW[:]/10**6, color = 'tab:blue', linewidth = 2, label = 'Mun')
axs[3,0].plot(Region_K.Year, Region_K.Power_GW[:]/10**6, color = 'gray', linewidth = 2, label = 'Pow')
axs[3,0].plot(Region_K.Year, (Region_K.Mining_GW[:]+Region_K.MFG_Gw[:])/10**6,
         color = 'gold', linewidth = 2, label = 'Ind')
axs[3,0].vlines([2008, 2015], ymin = 0, ymax = 25+ max(Region_K.Irrig_GW[:])/10**6,
                 color = 'red', linestyle = ':', linewidth = 2)
axs[3,0].set_ylim([0, 25+ max(Region_K.Irrig_GW[:])/10**6])
axs[3,0].set_ylabel('Sectoral GW 10\u00b3 acre-ft')
axs[3,0].xaxis.set_major_locator(MultipleLocator(5))
axs[3,0].xaxis.set_minor_locator(MultipleLocator(1))
axs[3,0].yaxis.set_major_locator(MultipleLocator(50))
axs[3,0].yaxis.set_minor_locator(MultipleLocator(25))

axs[3,2].plot(Region_O.Year, Region_O.Irrig_GW[:]/10**6, color = 'tab:green', linewidth = 2, label = 'Irr')
axs[3,2].plot(Region_O.Year, Region_O.Muni_GW[:]/10**6, color = 'tab:blue', linewidth = 2, label = 'Mun')
axs[3,2].plot(Region_O.Year, Region_O.Power_GW[:]/10**6, color = 'gray', label = 'Pow')
axs[3,2].plot(Region_O.Year, (Region_O.Mining_GW[:]+Region_O.MFG_Gw[:])/10**6,
         color = 'gold', linewidth = 2, label = 'Ind')
axs[3,2].vlines([2008, 2015], ymin = 0, ymax = 25+ max(Region_O.Irrig_GW[:])/10**6,
                 color = 'red', linestyle = ':', linewidth = 2)
axs[3,2].set_ylim([0, 25+ max(Region_O.Irrig_GW[:])/10**6])
axs[3,2].xaxis.set_major_locator(MultipleLocator(5))
axs[3,2].xaxis.set_minor_locator(MultipleLocator(1))
axs[3,2].yaxis.set_major_locator(MultipleLocator(200))
axs[3,2].yaxis.set_minor_locator(MultipleLocator(100))

plt.tight_layout()

plt.savefig("Figure_4b_municipal_use_change.svg", format="svg")

#%% Ratio of GW to total 

fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(8,2.5))
axs[1].plot(Region_F.Year, Region_F.Irrig_GW[:]/Region_F.Irrigation[:], color = 'tab:green', label = 'Irr')
axs[1].plot(Region_F.Year, Region_F.Muni_GW[:]/Region_F.Municipal[:], color = 'tab:blue', label = 'Mun')
axs[1].plot(Region_F.Year, Region_F.Power_GW[:]/Region_F.SteamElectric[:], color = 'gray', label = 'Pow')
axs[1].plot(Region_F.Year, (Region_F.Mining_GW[:]+Region_F.MFG_Gw[:])/(Region_F.Mining[:]+Region_F.Manufactoring[:]),
         color = 'gold', label = 'Ind')
axs[1].vlines([2008, 2015], ymin = 0, ymax = 1,
                 color = 'red', linestyle = ':', linewidth = 2)
axs[1].set_ylim([0, 1])
axs[1].xaxis.set_major_locator(MultipleLocator(5))
axs[1].xaxis.set_minor_locator(MultipleLocator(1))
axs[1].yaxis.set_major_locator(MultipleLocator(.2))
axs[1].yaxis.set_minor_locator(MultipleLocator(.1))

axs[0].plot(Region_K.Year, Region_K.Irrig_GW[:]/Region_K.Irrigation[:], color = 'tab:green', label = 'Irr')
axs[0].plot(Region_K.Year, Region_K.Muni_GW[:]/Region_K.Municipal[:], color = 'tab:blue', label = 'Mun')
axs[0].plot(Region_K.Year, Region_K.Power_GW[:]/Region_K.SteamElectric[:], color = 'gray', label = 'Pow')
axs[0].plot(Region_K.Year, (Region_K.Mining_GW[:]+Region_K.MFG_Gw[:])/(Region_K.Mining[:]+Region_K.Manufactoring[:]),
         color = 'gold', label = 'Ind')
axs[0].vlines([2008, 2015], ymin = 0, ymax = 1,
                 color = 'red', linestyle = ':', linewidth = 2)
axs[0].set_ylim([0, 1])
axs[0].set_ylabel('Fraction GW')
axs[0].xaxis.set_major_locator(MultipleLocator(5))
axs[0].xaxis.set_minor_locator(MultipleLocator(1))
axs[0].yaxis.set_major_locator(MultipleLocator(0.2))
axs[0].yaxis.set_minor_locator(MultipleLocator(0.1))

axs[2].plot(Region_O.Year, Region_O.Irrig_GW[:]/Region_O.Irrigation[:], color = 'tab:green', label = 'Irr')
axs[2].plot(Region_O.Year, Region_O.Muni_GW[:]/Region_O.Municipal[:], color = 'tab:blue', label = 'Mun')
axs[2].plot(Region_O.Year, Region_O.Power_GW[:]/Region_O.SteamElectric[:], color = 'grey', label = 'Pow')
axs[2].plot(Region_O.Year, Region_O.Irrig_GW[:]/Region_O.Irrigation[:], color = 'tab:green', label = 'Irr')
axs[2].plot(Region_O.Year, (Region_O.Mining_GW[:]+Region_O.MFG_Gw[:])/(Region_O.Mining[:]+Region_O.Manufactoring[:]),
         color = 'gold', label = 'Ind')
axs[2].vlines([2008, 2015], ymin = 0, ymax = 1.05,
                 color = 'red', linestyle = ':', linewidth = 2)
axs[2].set_ylim([-0.02, 1.05])
axs[2].xaxis.set_major_locator(MultipleLocator(5))
axs[2].xaxis.set_minor_locator(MultipleLocator(1))
axs[2].yaxis.set_major_locator(MultipleLocator(0.2))
axs[2].yaxis.set_minor_locator(MultipleLocator(0.1))

plt.tight_layout()


#%% Population in each region 
Fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(4,3))
axs.plot(Region_F.Year, (Region_F.Population)/1000,
         color = 'black', label = 'Pop')
axs.plot(Region_O.Year, (Region_O.Population)/1000,
         color = 'black', label = 'Pop')
axs.plot(Region_K.Year, (Region_K.Population)/1000,
         color = 'black', label = 'Pop')

axs.vlines([2008, 2015], ymin = 0, ymax = 50+max(Region_K.Population[:])/1000,
                  color = 'red', linestyle = ':', linewidth = 2)
#axs.set_ylim([0, 50+max(Region_K.Population[:])/1000])
axs.set_ylabel('Population (10^3)')
#plt.yscale('log')
# axs.xaxis.set_major_locator(MultipleLocator(5))
# axs.xaxis.set_minor_locator(MultipleLocator(1))
# axs.yaxis.set_major_locator(MultipleLocator(2))
# axs.yaxis.set_minor_locator(MultipleLocator(1))

plt.tight_layout()

#%% Dataframes for agricultural and municipal change in GW and SW use 

sns.set_theme(style="whitegrid")


rows = ['Lower drought','Middle drought', 'Upper drought', 'Lower post', 'Middle post',
        'Upper post']

columns = ['Agg','Mun'] #,'Ind','Therm']

data = np.zeros((len(rows),2))

avg_gw = pd.DataFrame(data = data.copy(), index = rows, columns = columns)
avg_sw = pd.DataFrame(data = data.copy(), index = rows, columns = columns)

max_gw = pd.DataFrame(data = data.copy(), index = rows, columns = columns)
max_sw = pd.DataFrame(data = data.copy(), index = rows, columns = columns)

# Agg GW
avg_gw.iloc[0,0] = 100*(np.mean(Region_K.Irrig_GW[8:16]) - np.mean(Region_K.Irrig_GW[0:8]))/np.mean(Region_K.Irrig_GW[0:8])
avg_gw.iloc[1,0] = 100*(np.mean(Region_F.Irrig_GW[8:16]) - np.mean(Region_F.Irrig_GW[0:8]))/np.mean(Region_F.Irrig_GW[0:8])
avg_gw.iloc[2,0] = 100*(np.mean(Region_O.Irrig_GW[8:16]) - np.mean(Region_O.Irrig_GW[0:8]))/np.mean(Region_O.Irrig_GW[0:8])
avg_gw.iloc[3,0] = 100*(np.mean(Region_K.Irrig_GW[16:])  - np.mean(Region_K.Irrig_GW[0:8]))/np.mean(Region_K.Irrig_GW[0:8])
avg_gw.iloc[4,0] = 100*(np.mean(Region_F.Irrig_GW[16:])  - np.mean(Region_F.Irrig_GW[0:8]))/np.mean(Region_F.Irrig_GW[0:8])
avg_gw.iloc[5,0] = 100*(np.mean(Region_O.Irrig_GW[16:])  - np.mean(Region_O.Irrig_GW[0:8]))/np.mean(Region_O.Irrig_GW[0:8])

max_gw.iloc[0,0] = 100*(np.max(Region_K.Irrig_GW[8:16]) - np.max(Region_K.Irrig_GW[0:8]))/np.max(Region_K.Irrig_GW[0:8])
max_gw.iloc[1,0] = 100*(np.max(Region_F.Irrig_GW[8:16]) - np.max(Region_F.Irrig_GW[0:8]))/np.max(Region_F.Irrig_GW[0:8])
max_gw.iloc[2,0] = 100*(np.max(Region_O.Irrig_GW[8:16]) - np.max(Region_O.Irrig_GW[0:8]))/np.max(Region_O.Irrig_GW[0:8])
max_gw.iloc[3,0] = 100*(np.max(Region_K.Irrig_GW[16:])  - np.max(Region_K.Irrig_GW[0:8]))/np.max(Region_K.Irrig_GW[0:8])
max_gw.iloc[4,0] = 100*(np.max(Region_F.Irrig_GW[16:])  - np.max(Region_F.Irrig_GW[0:8]))/np.max(Region_F.Irrig_GW[0:8])
max_gw.iloc[5,0] = 100*(np.max(Region_O.Irrig_GW[16:])  - np.max(Region_O.Irrig_GW[0:8]))/np.max(Region_O.Irrig_GW[0:8])

# Mun GW 
avg_gw.iloc[0,1] = 100*(np.mean(Region_K.Muni_GW[8:16]) - np.mean(Region_K.Muni_GW[0:8]))/np.mean(Region_K.Muni_GW[0:8])
avg_gw.iloc[1,1] = 100*(np.mean(Region_F.Muni_GW[8:16]) - np.mean(Region_F.Muni_GW[0:8]))/np.mean(Region_F.Muni_GW[0:8])
avg_gw.iloc[2,1] = 100*(np.mean(Region_O.Muni_GW[8:16]) - np.mean(Region_O.Muni_GW[0:8]))/np.mean(Region_O.Muni_GW[0:8])
avg_gw.iloc[3,1] = 100*(np.mean(Region_K.Muni_GW[16:])  - np.mean(Region_K.Muni_GW[0:8]))/np.mean(Region_K.Muni_GW[0:8])
avg_gw.iloc[4,1] = 100*(np.mean(Region_F.Muni_GW[16:])  - np.mean(Region_F.Muni_GW[0:8]))/np.mean(Region_F.Muni_GW[0:8])
avg_gw.iloc[5,1] = 100*(np.mean(Region_O.Muni_GW[16:])  - np.mean(Region_O.Muni_GW[0:8]))/np.mean(Region_O.Muni_GW[0:8])

max_gw.iloc[0,1] = 100*(np.max(Region_K.Muni_GW[8:16]) - np.max(Region_K.Muni_GW[0:8]))/np.max(Region_K.Muni_GW[0:8])
max_gw.iloc[1,1] = 100*(np.max(Region_F.Muni_GW[8:16]) - np.max(Region_F.Muni_GW[0:8]))/np.max(Region_F.Muni_GW[0:8])
max_gw.iloc[2,1] = 100*(np.max(Region_O.Muni_GW[8:16]) - np.max(Region_O.Muni_GW[0:8]))/np.max(Region_O.Muni_GW[0:8])
max_gw.iloc[3,1] = 100*(np.max(Region_K.Muni_GW[16:])  - np.max(Region_K.Muni_GW[0:8]))/np.max(Region_K.Muni_GW[0:8])
max_gw.iloc[4,1] = 100*(np.max(Region_F.Muni_GW[16:])  - np.max(Region_F.Muni_GW[0:8]))/np.max(Region_F.Muni_GW[0:8])
max_gw.iloc[5,1] = 100*(np.max(Region_O.Muni_GW[16:])  - np.max(Region_O.Muni_GW[0:8]))/np.max(Region_O.Muni_GW[0:8])

# # Industrial GW 
# Region_K_indust_GW = Region_K.Mining_GW[:]+Region_K.MFG_Gw[:]
# Region_F_indust_GW = Region_F.Mining_GW[:]+Region_F.MFG_Gw[:]
# Region_O_indust_GW = Region_O.Mining_GW[:]+Region_O.MFG_Gw[:]

# avg_gw.iloc[0,2] = 100*(np.mean(Region_K_indust_GW[8:16]) - np.mean(Region_K_indust_GW[0:8]))/np.mean(Region_K_indust_GW[0:8])
# avg_gw.iloc[1,2] = 100*(np.mean(Region_F_indust_GW[8:16]) - np.mean(Region_F_indust_GW[0:8]))/np.mean(Region_F_indust_GW[0:8])
# avg_gw.iloc[2,2] = 100*(np.mean(Region_O_indust_GW[8:16]) - np.mean(Region_O_indust_GW[0:8]))/np.mean(Region_O_indust_GW[0:8])
# avg_gw.iloc[3,2] = 100*(np.mean(Region_K_indust_GW[16:])  - np.mean(Region_K_indust_GW[0:8]))/np.mean(Region_K_indust_GW[0:8])
# avg_gw.iloc[4,2] = 100*(np.mean(Region_F_indust_GW[16:])  - np.mean(Region_F_indust_GW[0:8]))/np.mean(Region_F_indust_GW[0:8])
# avg_gw.iloc[5,2] = 100*(np.mean(Region_O_indust_GW[16:])  - np.mean(Region_O_indust_GW[0:8]))/np.mean(Region_O_indust_GW[0:8])

# # Power GW 
# avg_gw.iloc[0,3] = 100*(np.mean(Region_K.Power_GW[8:16]) - np.mean(Region_K.Power_GW[0:8]))/np.mean(Region_K.Power_GW[0:8])
# avg_gw.iloc[1,3] = 100*(np.mean(Region_F.Power_GW[8:16]) - np.mean(Region_F.Power_GW[0:8]))/np.mean(Region_F.Power_GW[0:8])
# avg_gw.iloc[2,3] = 100*(np.mean(Region_O.Power_GW[8:16]) - np.mean(Region_O.Power_GW[0:8]))/np.mean(Region_O.Power_GW[0:8])
# avg_gw.iloc[3,3] = 100*(np.mean(Region_K.Power_GW[16:])  - np.mean(Region_K.Power_GW[0:8]))/np.mean(Region_K.Power_GW[0:8])
# avg_gw.iloc[4,3] = 100*(np.mean(Region_F.Power_GW[16:])  - np.mean(Region_F.Power_GW[0:8]))/np.mean(Region_F.Power_GW[0:8])
# avg_gw.iloc[5,3] = 100*(np.mean(Region_O.Power_GW[16:])  - np.mean(Region_O.Power_GW[0:8]))/np.mean(Region_O.Power_GW[0:8])

# Agg SW
avg_sw.iloc[0,0] = 100*(np.mean(Region_K.Irrig_SW[8:16]) - np.mean(Region_K.Irrig_SW[0:8]))/np.mean(Region_K.Irrig_SW[0:8])
avg_sw.iloc[1,0] = 100*(np.mean(Region_F.Irrig_SW[8:16]) - np.mean(Region_F.Irrig_SW[0:8]))/np.mean(Region_F.Irrig_SW[0:8])
avg_sw.iloc[2,0] = np.nan # 100*(np.mean(Region_O.Irrig_SW[8:16]) - np.mean(Region_O.Irrig_SW[0:8]))/np.mean(Region_O.Irrig_SW[0:8])
avg_sw.iloc[3,0] = 100*(np.mean(Region_K.Irrig_SW[16:])  - np.mean(Region_K.Irrig_SW[0:8]))/np.mean(Region_K.Irrig_SW[0:8])
avg_sw.iloc[4,0] = 100*(np.mean(Region_F.Irrig_SW[16:])  - np.mean(Region_F.Irrig_SW[0:8]))/np.mean(Region_F.Irrig_SW[0:8])
avg_sw.iloc[5,0] = np.nan #100*(np.mean(Region_O.Irrig_SW[16:])  - np.mean(Region_O.Irrig_SW[0:8]))/np.mean(Region_O.Irrig_SW[0:8])

max_sw.iloc[0,0] = 100*(np.max(Region_K.Irrig_SW[8:16]) - np.max(Region_K.Irrig_SW[0:8]))/np.max(Region_K.Irrig_SW[0:8])
max_sw.iloc[1,0] = 100*(np.max(Region_F.Irrig_SW[8:16]) - np.max(Region_F.Irrig_SW[0:8]))/np.max(Region_F.Irrig_SW[0:8])
max_sw.iloc[2,0] = np.nan # 100*(np.mean(Region_O.Irrig_SW[8:16]) - np.mean(Region_O.Irrig_SW[0:8]))/np.mean(Region_O.Irrig_SW[0:8])
max_sw.iloc[3,0] = 100*(np.max(Region_K.Irrig_SW[16:])  - np.max(Region_K.Irrig_SW[0:8]))/np.max(Region_K.Irrig_SW[0:8])
max_sw.iloc[4,0] = 100*(np.max(Region_F.Irrig_SW[16:])  - np.max(Region_F.Irrig_SW[0:8]))/np.max(Region_F.Irrig_SW[0:8])
max_sw.iloc[5,0] = np.nan #100*(np.mean(Region_O.Irrig_SW[16:])  - np.mean(Region_O.Irrig_SW[0:8]))/np.mean(Region_O.Irrig_SW[0:8])

# Mun SW 
avg_sw.iloc[0,1] = 100*(np.mean(Region_K.Muni_SW[8:16]) - np.mean(Region_K.Muni_SW[0:8]))/np.mean(Region_K.Muni_SW[0:8])
avg_sw.iloc[1,1] = 100*(np.mean(Region_F.Muni_SW[8:16]) - np.mean(Region_F.Muni_SW[0:8]))/np.mean(Region_F.Muni_SW[0:8])
avg_sw.iloc[2,1] = 100*(np.mean(Region_O.Muni_SW[8:16]) - np.mean(Region_O.Muni_SW[0:8]))/np.mean(Region_O.Muni_SW[0:8])
avg_sw.iloc[3,1] = 100*(np.mean(Region_K.Muni_SW[16:])  - np.mean(Region_K.Muni_SW[0:8]))/np.mean(Region_K.Muni_SW[0:8])
avg_sw.iloc[4,1] = 100*(np.mean(Region_F.Muni_SW[16:])  - np.mean(Region_F.Muni_SW[0:8]))/np.mean(Region_F.Muni_SW[0:8])
avg_sw.iloc[5,1] = 100*(np.mean(Region_O.Muni_SW[16:])  - np.mean(Region_O.Muni_SW[0:8]))/np.mean(Region_O.Muni_SW[0:8])

max_sw.iloc[0,1] = 100*(np.max(Region_K.Muni_SW[8:16]) - np.max(Region_K.Muni_SW[0:8]))/np.max(Region_K.Muni_SW[0:8])
max_sw.iloc[1,1] = 100*(np.max(Region_F.Muni_SW[8:16]) - np.max(Region_F.Muni_SW[0:8]))/np.max(Region_F.Muni_SW[0:8])
max_sw.iloc[2,1] = 100*(np.max(Region_O.Muni_SW[8:16]) - np.max(Region_O.Muni_SW[0:8]))/np.max(Region_O.Muni_SW[0:8])
max_sw.iloc[3,1] = 100*(np.max(Region_K.Muni_SW[16:])  - np.max(Region_K.Muni_SW[0:8]))/np.max(Region_K.Muni_SW[0:8])
max_sw.iloc[4,1] = 100*(np.max(Region_F.Muni_SW[16:])  - np.max(Region_F.Muni_SW[0:8]))/np.max(Region_F.Muni_SW[0:8])
max_sw.iloc[5,1] = 100*(np.max(Region_O.Muni_SW[16:])  - np.max(Region_O.Muni_SW[0:8]))/np.max(Region_O.Muni_SW[0:8])

avg_gw['Region'] = rows
max_gw['Region'] = rows
avg_sw['Region'] = rows
max_sw['Region'] = rows



#%%

columns = ['Lower','Middle', 'Upper']

data = np.zeros((13, len(columns),))

ag_gw = pd.DataFrame(data = data.copy(), columns = columns)
mun_gw = pd.DataFrame(data = data.copy(), columns = columns)
pow_gw = pd.DataFrame(data = data.copy(), columns = columns)

ag_sw = pd.DataFrame(data = data.copy(), columns = columns)
mun_sw = pd.DataFrame(data = data.copy(), columns = columns)
pow_sw = pd.DataFrame(data = data.copy(), columns = columns)

# Ag GW
for i in range(13):
    ag_gw.iloc[i,0] = 100*(Region_K.Irrig_GW[i+8] - np.mean(Region_K.Irrig_GW[0:8]))/np.mean(Region_K.Irrig_GW[0:8])
    ag_gw.iloc[i,1] = 100*(Region_F.Irrig_GW[i+8] - np.mean(Region_F.Irrig_GW[0:8]))/np.mean(Region_F.Irrig_GW[0:8])
    ag_gw.iloc[i,2] = 100*(Region_O.Irrig_GW[i+8] - np.mean(Region_O.Irrig_GW[0:8]))/np.mean(Region_O.Irrig_GW[0:8])

# Ag SW
for i in range(13):
    ag_sw.iloc[i,0] = 100*(Region_K.Irrig_SW[i+8] - np.mean(Region_K.Irrig_SW[0:8]))/np.mean(Region_K.Irrig_SW[0:8])
    ag_sw.iloc[i,1] = 100*(Region_F.Irrig_SW[i+8] - np.mean(Region_F.Irrig_SW[0:8]))/np.mean(Region_F.Irrig_SW[0:8])
    ag_sw.iloc[i,2] = 100*(Region_O.Irrig_SW[i+8] - np.mean(Region_O.Irrig_SW[0:8]))/np.mean(Region_O.Irrig_SW[0:8])
    
# max_gw.iloc[0,0] = 100*(np.max(Region_K.Irrig_GW[8:16]) - np.max(Region_K.Irrig_GW[0:8]))/np.max(Region_K.Irrig_GW[0:8])
# max_gw.iloc[1,0] = 100*(np.max(Region_F.Irrig_GW[8:16]) - np.max(Region_F.Irrig_GW[0:8]))/np.max(Region_F.Irrig_GW[0:8])
# max_gw.iloc[2,0] = 100*(np.max(Region_O.Irrig_GW[8:16]) - np.max(Region_O.Irrig_GW[0:8]))/np.max(Region_O.Irrig_GW[0:8])
# max_gw.iloc[3,0] = 100*(np.max(Region_K.Irrig_GW[16:])  - np.max(Region_K.Irrig_GW[0:8]))/np.max(Region_K.Irrig_GW[0:8])
# max_gw.iloc[4,0] = 100*(np.max(Region_F.Irrig_GW[16:])  - np.max(Region_F.Irrig_GW[0:8]))/np.max(Region_F.Irrig_GW[0:8])
# max_gw.iloc[5,0] = 100*(np.max(Region_O.Irrig_GW[16:])  - np.max(Region_O.Irrig_GW[0:8]))/np.max(Region_O.Irrig_GW[0:8])

# Mun GW 
for i in range(13):
    mun_gw.iloc[i,0] = 100*(Region_K.Muni_GW[i+8] - np.mean(Region_K.Muni_GW[0:8]))/np.mean(Region_K.Muni_GW[0:8])
    mun_gw.iloc[i,1] = 100*(Region_F.Muni_GW[i+8] - np.mean(Region_F.Muni_GW[0:8]))/np.mean(Region_F.Muni_GW[0:8])
    mun_gw.iloc[i,2] = 100*(Region_O.Muni_GW[i+8] - np.mean(Region_O.Muni_GW[0:8]))/np.mean(Region_O.Muni_GW[0:8])

# Mun SW
for i in range(13):
    mun_sw.iloc[i,0] = 100*(Region_K.Muni_SW[i+8] - np.mean(Region_K.Muni_SW[0:8]))/np.mean(Region_K.Muni_SW[0:8])
    mun_sw.iloc[i,1] = 100*(Region_F.Muni_SW[i+8] - np.mean(Region_F.Muni_SW[0:8]))/np.mean(Region_F.Muni_SW[0:8])
    mun_sw.iloc[i,2] = 100*(Region_O.Muni_SW[i+8] - np.mean(Region_O.Muni_SW[0:8]))/np.mean(Region_O.Muni_SW[0:8])


# Pow GW 
for i in range(13):
    pow_gw.iloc[i,0] = 100*(Region_K.Power_GW[i+8] - np.mean(Region_K.Power_GW[0:8]))/np.mean(Region_K.Power_GW[0:8])
    pow_gw.iloc[i,1] = 100*(Region_F.Power_GW[i+8] - np.mean(Region_F.Power_GW[0:8]))/np.mean(Region_F.Power_GW[0:8])
    pow_gw.iloc[i,2] = 100*(Region_O.Power_GW[i+8] - np.mean(Region_O.Power_GW[0:8]))/np.mean(Region_O.Power_GW[0:8])
    
# Pow SW 
for i in range(13):
    pow_sw.iloc[i,0] = 100*(Region_K.Power_SW[i+8] - np.mean(Region_K.Power_SW[0:8]))/np.mean(Region_K.Power_SW[0:8])
    pow_sw.iloc[i,1] = 100*(Region_F.Power_SW[i+8] - np.mean(Region_F.Power_SW[0:8]))/np.mean(Region_F.Power_SW[0:8])
    pow_sw.iloc[i,2] = 100*(Region_O.Power_SW[i+8] - np.mean(Region_O.Power_SW[0:8]))/np.mean(Region_O.Power_SW[0:8])
    
# max_gw.iloc[0,1] = 100*(np.max(Region_K.Muni_GW[8:16]) - np.max(Region_K.Muni_GW[0:8]))/np.max(Region_K.Muni_GW[0:8])
# max_gw.iloc[1,1] = 100*(np.max(Region_F.Muni_GW[8:16]) - np.max(Region_F.Muni_GW[0:8]))/np.max(Region_F.Muni_GW[0:8])
# max_gw.iloc[2,1] = 100*(np.max(Region_O.Muni_GW[8:16]) - np.max(Region_O.Muni_GW[0:8]))/np.max(Region_O.Muni_GW[0:8])
# max_gw.iloc[3,1] = 100*(np.max(Region_K.Muni_GW[16:])  - np.max(Region_K.Muni_GW[0:8]))/np.max(Region_K.Muni_GW[0:8])
# max_gw.iloc[4,1] = 100*(np.max(Region_F.Muni_GW[16:])  - np.max(Region_F.Muni_GW[0:8]))/np.max(Region_F.Muni_GW[0:8])
# max_gw.iloc[5,1] = 100*(np.max(Region_O.Muni_GW[16:])  - np.max(Region_O.Muni_GW[0:8]))/np.max(Region_O.Muni_GW[0:8])

# # Industrial GW 
# Region_K_indust_GW = Region_K.Mining_GW[:]+Region_K.MFG_Gw[:]
# Region_F_indust_GW = Region_F.Mining_GW[:]+Region_F.MFG_Gw[:]
# Region_O_indust_GW = Region_O.Mining_GW[:]+Region_O.MFG_Gw[:]

# avg_gw.iloc[0,2] = 100*(np.mean(Region_K_indust_GW[8:16]) - np.mean(Region_K_indust_GW[0:8]))/np.mean(Region_K_indust_GW[0:8])
# avg_gw.iloc[1,2] = 100*(np.mean(Region_F_indust_GW[8:16]) - np.mean(Region_F_indust_GW[0:8]))/np.mean(Region_F_indust_GW[0:8])
# avg_gw.iloc[2,2] = 100*(np.mean(Region_O_indust_GW[8:16]) - np.mean(Region_O_indust_GW[0:8]))/np.mean(Region_O_indust_GW[0:8])
# avg_gw.iloc[3,2] = 100*(np.mean(Region_K_indust_GW[16:])  - np.mean(Region_K_indust_GW[0:8]))/np.mean(Region_K_indust_GW[0:8])
# avg_gw.iloc[4,2] = 100*(np.mean(Region_F_indust_GW[16:])  - np.mean(Region_F_indust_GW[0:8]))/np.mean(Region_F_indust_GW[0:8])
# avg_gw.iloc[5,2] = 100*(np.mean(Region_O_indust_GW[16:])  - np.mean(Region_O_indust_GW[0:8]))/np.mean(Region_O_indust_GW[0:8])

# # Power GW 
# avg_gw.iloc[0,3] = 100*(np.mean(Region_K.Power_GW[8:16]) - np.mean(Region_K.Power_GW[0:8]))/np.mean(Region_K.Power_GW[0:8])
# avg_gw.iloc[1,3] = 100*(np.mean(Region_F.Power_GW[8:16]) - np.mean(Region_F.Power_GW[0:8]))/np.mean(Region_F.Power_GW[0:8])
# avg_gw.iloc[2,3] = 100*(np.mean(Region_O.Power_GW[8:16]) - np.mean(Region_O.Power_GW[0:8]))/np.mean(Region_O.Power_GW[0:8])
# avg_gw.iloc[3,3] = 100*(np.mean(Region_K.Power_GW[16:])  - np.mean(Region_K.Power_GW[0:8]))/np.mean(Region_K.Power_GW[0:8])
# avg_gw.iloc[4,3] = 100*(np.mean(Region_F.Power_GW[16:])  - np.mean(Region_F.Power_GW[0:8]))/np.mean(Region_F.Power_GW[0:8])
# avg_gw.iloc[5,3] = 100*(np.mean(Region_O.Power_GW[16:])  - np.mean(Region_O.Power_GW[0:8]))/np.mean(Region_O.Power_GW[0:8])

# max_sw.iloc[0,0] = 100*(np.max(Region_K.Irrig_SW[8:16]) - np.max(Region_K.Irrig_SW[0:8]))/np.max(Region_K.Irrig_SW[0:8])
# max_sw.iloc[1,0] = 100*(np.max(Region_F.Irrig_SW[8:16]) - np.max(Region_F.Irrig_SW[0:8]))/np.max(Region_F.Irrig_SW[0:8])
# max_sw.iloc[2,0] = np.nan # 100*(np.mean(Region_O.Irrig_SW[8:16]) - np.mean(Region_O.Irrig_SW[0:8]))/np.mean(Region_O.Irrig_SW[0:8])
# max_sw.iloc[3,0] = 100*(np.max(Region_K.Irrig_SW[16:])  - np.max(Region_K.Irrig_SW[0:8]))/np.max(Region_K.Irrig_SW[0:8])
# max_sw.iloc[4,0] = 100*(np.max(Region_F.Irrig_SW[16:])  - np.max(Region_F.Irrig_SW[0:8]))/np.max(Region_F.Irrig_SW[0:8])
# max_sw.iloc[5,0] = np.nan #100*(np.mean(Region_O.Irrig_SW[16:])  - np.mean(Region_O.Irrig_SW[0:8]))/np.mean(Region_O.Irrig_SW[0:8])

# # Mun SW 

# max_sw.iloc[0,1] = 100*(np.max(Region_K.Muni_SW[8:16]) - np.max(Region_K.Muni_SW[0:8]))/np.max(Region_K.Muni_SW[0:8])
# max_sw.iloc[1,1] = 100*(np.max(Region_F.Muni_SW[8:16]) - np.max(Region_F.Muni_SW[0:8]))/np.max(Region_F.Muni_SW[0:8])
# max_sw.iloc[2,1] = 100*(np.max(Region_O.Muni_SW[8:16]) - np.max(Region_O.Muni_SW[0:8]))/np.max(Region_O.Muni_SW[0:8])
# max_sw.iloc[3,1] = 100*(np.max(Region_K.Muni_SW[16:])  - np.max(Region_K.Muni_SW[0:8]))/np.max(Region_K.Muni_SW[0:8])
# max_sw.iloc[4,1] = 100*(np.max(Region_F.Muni_SW[16:])  - np.max(Region_F.Muni_SW[0:8]))/np.max(Region_F.Muni_SW[0:8])
# max_sw.iloc[5,1] = 100*(np.max(Region_O.Muni_SW[16:])  - np.max(Region_O.Muni_SW[0:8]))/np.max(Region_O.Muni_SW[0:8])

############### Plot annual % 

################################## Agriculture Summary 

Fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(8,5))
# K SW ag 
axs.scatter(0.5*np.ones(8), ag_sw.iloc[0:8,0], facecolors='magenta', edgecolor = 'magenta')
axs.scatter(0.5, 100*(np.mean(Region_K.Irrig_SW[8:16]) - np.mean(Region_K.Irrig_SW[0:8]))/np.mean(Region_K.Irrig_SW[0:8]), s = 125, facecolors='none', edgecolor = 'magenta', 
               marker = 's')
axs.scatter(0.7*np.ones(5), ag_sw.iloc[8:,0], facecolors='magenta', edgecolor = 'magenta')
axs.scatter(0.7, 100*(np.mean(Region_K.Irrig_SW[16:]) - np.mean(Region_K.Irrig_SW[0:8]))/np.mean(Region_K.Irrig_SW[0:8]), s = 125, facecolors='none', edgecolor = 'magenta',  
               marker = 's')
# F SW ag
axs.scatter(1*np.ones(8), ag_sw.iloc[0:8,1], facecolors='indigo', edgecolor = 'indigo')
axs.scatter(1, 100*(np.mean(Region_F.Irrig_SW[8:16]) - np.mean(Region_F.Irrig_SW[0:8]))/np.mean(Region_F.Irrig_SW[0:8]), s = 125, facecolors='none', edgecolor = 'indigo', 
               marker = 's')
axs.scatter(1.2*np.ones(5), ag_sw.iloc[8:,1], facecolors='indigo', edgecolor = 'indigo')
axs.scatter(1.2, 100*(np.mean(Region_F.Irrig_SW[16:]) - np.mean(Region_F.Irrig_SW[0:8]))/np.mean(Region_F.Irrig_SW[0:8]), s = 125, facecolors='none', edgecolor = 'indigo', 
               marker = 's')

# K GW ag
axs.scatter(2*np.ones(8), ag_gw.iloc[0:8,0], facecolors='magenta', edgecolor = 'magenta')
axs.scatter(2, 100*(np.mean(Region_K.Irrig_GW[8:16]) - np.mean(Region_K.Irrig_GW[0:8]))/np.mean(Region_K.Irrig_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'magenta', 
               marker = 's')
axs.scatter(2.2*np.ones(5), ag_gw.iloc[8:,0], facecolors='magenta', edgecolor = 'magenta')
axs.scatter(2.2, 100*(np.mean(Region_K.Irrig_GW[16:]) - np.mean(Region_K.Irrig_GW[0:8]))/np.mean(Region_K.Irrig_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'magenta', 
               marker = 's')

# F GW ag
axs.scatter(2.5*np.ones(8), ag_gw.iloc[0:8,1], facecolors='indigo', edgecolor = 'indigo')
axs.scatter(2.5, 100*(np.mean(Region_F.Irrig_GW[8:16]) - np.mean(Region_F.Irrig_GW[0:8]))/np.mean(Region_F.Irrig_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'indigo', 
               marker = 's')
axs.scatter(2.7*np.ones(5), ag_gw.iloc[8:,1], facecolors='indigo', edgecolor = 'indigo')
axs.scatter(2.7, 100*(np.mean(Region_F.Irrig_GW[16:]) - np.mean(Region_F.Irrig_GW[0:8]))/np.mean(Region_F.Irrig_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'indigo', 
               marker = 's')

# O GW ag
axs.scatter(3*np.ones(8), ag_gw.iloc[0:8,2], facecolors='green', edgecolor = 'green')
axs.scatter(3, 100*(np.mean(Region_O.Irrig_GW[8:16]) - np.mean(Region_O.Irrig_GW[0:8]))/np.mean(Region_O.Irrig_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'green', 
               marker = 's')
axs.scatter(3.2*np.ones(5), ag_gw.iloc[8:,2], facecolors='green', edgecolor = 'green')
axs.scatter(3.2, 100*(np.mean(Region_O.Irrig_GW[16:]) - np.mean(Region_O.Irrig_GW[0:8]))/np.mean(Region_O.Irrig_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'green', 
               marker = 's')

axs.yaxis.set_major_locator(MultipleLocator(20))
axs.yaxis.set_minor_locator(MultipleLocator(10))
axs.set_xticks([0.5, 0.7, 1, 1.2, 2, 2.2, 2.5, 2.7, 3, 3.2], ['drought','post','drought','post','drought','post','drought','post','drought','post'], rotation = 90)
axs.hlines(0, xmin = 0, xmax = 4, color = 'grey')
axs.set_xlim([0,3.5])
axs.set_ylabel('% change in annual use')
axs.set_title('Agriculture')
plt.savefig("Figure_4a_Ag_use_change.svg", format="svg")


################################## Municipal Summary 

Fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(8,5))
# K SW mun 
axs.scatter(0.3*np.ones(8), mun_sw.iloc[0:8,0], facecolors='magenta', edgecolor = 'magenta')
axs.scatter(0.3, 100*(np.mean(Region_K.Muni_SW[8:16]) - np.mean(Region_K.Muni_SW[0:8]))/np.mean(Region_K.Muni_SW[0:8]),  s = 125, facecolors='none', edgecolor = 'magenta', 
               marker = 's')
axs.scatter(0.5*np.ones(5), mun_sw.iloc[8:,0], facecolors='magenta', edgecolor = 'magenta')
axs.scatter(0.5, 100*(np.mean(Region_K.Muni_SW[16:]) - np.mean(Region_K.Muni_SW[0:8]))/np.mean(Region_K.Muni_SW[0:8]),  s = 125, facecolors='none', edgecolor = 'magenta', 
               marker = 's')
# F SW mun
axs.scatter(0.8*np.ones(8), mun_sw.iloc[0:8,1], facecolors='indigo', edgecolor = 'indigo')
axs.scatter(0.8, 100*(np.mean(Region_F.Muni_SW[8:16]) - np.mean(Region_F.Muni_SW[0:8]))/np.mean(Region_F.Muni_SW[0:8]),  s = 125, facecolors='none', edgecolor = 'indigo', 
               marker = 's')
axs.scatter(1*np.ones(5), mun_sw.iloc[8:,1], facecolors='indigo', edgecolor = 'indigo')
axs.scatter(1, 100*(np.mean(Region_F.Muni_SW[16:]) - np.mean(Region_F.Muni_SW[0:8]))/np.mean(Region_F.Muni_SW[0:8]),  s = 125, facecolors='none', edgecolor = 'indigo', 
               marker = 's')
# O SW mun
axs.scatter(1.3*np.ones(8), mun_sw.iloc[0:8,2], facecolors='green', edgecolor = 'green')
axs.scatter(1.3, 100*(np.mean(Region_O.Muni_SW[8:16]) - np.mean(Region_O.Muni_SW[0:8]))/np.mean(Region_O.Muni_SW[0:8]),  s = 125, facecolors='none', edgecolor = 'green', 
               marker = 's')
axs.scatter(1.5*np.ones(5), mun_sw.iloc[8:,2], facecolors='green', edgecolor = 'green')
axs.scatter(1.5, 100*(np.mean(Region_O.Muni_SW[16:]) - np.mean(Region_O.Muni_SW[0:8]))/np.mean(Region_O.Muni_SW[0:8]),  s = 125, facecolors='none', edgecolor = 'green', 
               marker = 's')


# K GW mun
axs.scatter(2*np.ones(8), mun_gw.iloc[0:8,0], facecolors='magenta', edgecolor = 'magenta')
axs.scatter(2, 100*(np.mean(Region_K.Muni_GW[8:16]) - np.mean(Region_K.Muni_GW[0:8]))/np.mean(Region_K.Muni_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'magenta', 
               marker = 's')
axs.scatter(2.2*np.ones(5), mun_gw.iloc[8:,0], facecolors='magenta', edgecolor = 'magenta')
axs.scatter(2.2, 100*(np.mean(Region_K.Muni_GW[16:]) - np.mean(Region_K.Muni_GW[0:8]))/np.mean(Region_K.Muni_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'magenta', 
               marker = 's')

# F GW mun
axs.scatter(2.5*np.ones(8), mun_gw.iloc[0:8,1], facecolors='indigo', edgecolor = 'indigo')
axs.scatter(2.5, 100*(np.mean(Region_F.Muni_GW[8:16]) - np.mean(Region_F.Muni_GW[0:8]))/np.mean(Region_F.Muni_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'indigo', 
               marker = 's')
axs.scatter(2.7*np.ones(5), mun_gw.iloc[8:,1], facecolors='indigo', edgecolor = 'indigo')
axs.scatter(2.7, 100*(np.mean(Region_F.Muni_GW[16:]) - np.mean(Region_F.Muni_GW[0:8]))/np.mean(Region_F.Muni_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'indigo', 
               marker = 's')

# O GW mun
axs.scatter(3*np.ones(8), mun_gw.iloc[0:8,2], facecolors='green', edgecolor = 'green')
axs.scatter(3, 100*(np.mean(Region_O.Muni_GW[8:16]) - np.mean(Region_O.Muni_GW[0:8]))/np.mean(Region_O.Muni_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'green', 
               marker = 's')
axs.scatter(3.2*np.ones(5), mun_gw.iloc[8:,2], facecolors='green', edgecolor = 'green')
axs.scatter(3.2, 100*(np.mean(Region_O.Muni_GW[16:]) - np.mean(Region_O.Muni_GW[0:8]))/np.mean(Region_O.Muni_GW[0:8]),  s = 125, facecolors='none', edgecolor = 'green', 
               marker = 's')

axs.yaxis.set_major_locator(MultipleLocator(10))
axs.set_xticks([0.3, 0.5, 0.8, 1, 1.3, 1.5, 2, 2.2, 2.5, 2.7, 3, 3.2], ['drought','post','drought','post','drought','post','drought','post','drought','post', 'drought','post'], rotation = 90)
axs.hlines(0, xmin = 0, xmax = 4, color = 'grey')
axs.set_xlim([0,3.5])
axs.set_ylabel('% change in annual use')
axs.set_title('Municipal')
plt.savefig("Figure_4b_municipal_use_change.svg", format="svg")

