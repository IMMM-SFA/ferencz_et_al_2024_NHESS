# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os 

os.chdir("Data Path")

Region_O_Irr_well_df = pd.read_csv('Wells_Region_O_Irr.csv')
Region_K_Irr_well_df = pd.read_csv('Wells_Region_K_Irr.csv')
Region_F_Irr_well_df = pd.read_csv('Wells_Region_F_Irr.csv')

Region_O_Dom_well_df = pd.read_csv('Wells_Region_O_Dom.csv')
Region_K_Dom_well_df = pd.read_csv('Wells_Region_K_Dom.csv')
Region_F_Dom_well_df = pd.read_csv('Wells_Region_F_Dom.csv')

Region_O_Ind_well_df = pd.read_csv('Wells_Region_O_Ind.csv')
Region_K_Ind_well_df = pd.read_csv('Wells_Region_K_Ind.csv')
Region_F_Ind_well_df = pd.read_csv('Wells_Region_F_Ind.csv')

Region_O_Pub_well_df = pd.read_csv('Wells_Region_O_Pub.csv')
Region_K_Pub_well_df = pd.read_csv('Wells_Region_K_Pub.csv')
Region_F_Pub_well_df = pd.read_csv('Wells_Region_F_Pub.csv')

#%% Well counts for bar plots 

Region_F_Irr_counts =  Region_F_Irr_well_df.Year.value_counts()
Region_F_Irr_counts.sort_index(inplace = True) 
Region_F_Dom_counts =  Region_F_Dom_well_df.Year.value_counts()
Region_F_Dom_counts.sort_index(inplace = True) 
Region_F_Ind_counts =  Region_F_Ind_well_df.Year.value_counts()
Region_F_Ind_counts.sort_index(inplace = True) 
Region_F_Pub_counts =  Region_F_Pub_well_df.Year.value_counts()
Region_F_Pub_counts.sort_index(inplace = True) 

Region_K_Irr_counts =  Region_K_Irr_well_df.Year.value_counts()
Region_K_Irr_counts.sort_index(inplace = True) 
Region_K_Dom_counts =  Region_K_Dom_well_df.Year.value_counts()
Region_K_Dom_counts.sort_index(inplace = True) 
Region_K_Ind_counts =  Region_K_Ind_well_df.Year.value_counts()
Region_K_Ind_counts.sort_index(inplace = True)
Region_K_Pub_counts =  Region_K_Pub_well_df.Year.value_counts()
Region_K_Pub_counts.sort_index(inplace = True)

Region_O_Irr_counts = Region_O_Irr_well_df.Year.value_counts()
Region_O_Irr_counts.sort_index(inplace = True)
Region_O_Dom_counts = Region_O_Dom_well_df.Year.value_counts()
Region_O_Dom_counts.sort_index(inplace = True)
Region_O_Ind_counts = Region_O_Ind_well_df.Year.value_counts()
Region_O_Ind_counts.sort_index(inplace = True)
Region_O_Pub_counts = Region_O_Pub_well_df.Year.value_counts()
Region_O_Pub_counts.sort_index(inplace = True)

#%% Subplots

fig, axs = plt.subplots(nrows=4, ncols=3, figsize=(8, 8))
fig.suptitle('Well Installations (2001-2021)', fontsize = 14)

# Region K 
axs[0,0].bar(Region_K_Irr_counts.index, Region_K_Irr_counts.values, color = 'tab:green')
axs[0,0].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_K_Irr_counts.values)+10,
                color = 'red', linewidth = 2)
axs[0,0].set_xlim([2000.5, 2021.5])
axs[0,0].set_ylim([0, max(Region_K_Irr_counts.values)+10])
axs[0,0].set_xticks(ticks = np.arange(21)+2001, labels = np.tile('',21), rotation = 90)

axs[1,0].bar(Region_K_Ind_counts.index, Region_K_Ind_counts.values, color = 'tab:gray')
axs[1,0].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_K_Ind_counts.values)+10,
                color = 'red', linewidth = 2)
axs[1,0].set_xlim([2000.5, 2021.5])
axs[1,0].set_ylim([0, max(Region_K_Ind_counts.values)+10])
axs[1,0].set_xticks(ticks = np.arange(21)+2001, labels = np.tile('',21), rotation = 90)


axs[2,0].bar(Region_K_Pub_counts.index, Region_K_Pub_counts.values, color = 'tab:blue')
axs[2,0].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_K_Pub_counts.values)+10,
                color = 'red', linewidth = 2)
axs[2,0].set_xlim([2000.5, 2021.5])
axs[2,0].set_ylim([0, 30])
axs[2,0].set_xticks(ticks = np.arange(21)+2001, labels = np.tile('',21), rotation = 90)

axs[3,0].bar(Region_K_Dom_counts.index, Region_K_Dom_counts.values, color = 'black')
axs[3,0].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_K_Dom_counts.values)+10,
                color = 'red', linewidth = 2)
axs[3,0].set_xlim([2000.5, 2021.5])
axs[3,0].set_ylim([0, max(Region_K_Dom_counts.values)+10])
axs[3,0].xaxis.set_major_locator(MultipleLocator(5))
axs[3,0].xaxis.set_minor_locator(MultipleLocator(1))

# Region F
axs[0,1].bar(Region_F_Irr_counts.index, Region_F_Irr_counts.values, color = 'tab:green')
axs[0,1].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_F_Irr_counts.values)+10,
                color = 'red', linewidth = 2)
axs[0,1].set_xlim([2000.5, 2021.5])
axs[0,1].set_ylim([0, max(Region_F_Irr_counts.values)+10])
axs[0,1].set_xticks(ticks = np.arange(21)+2001, labels = np.tile('',21), rotation = 90)

axs[1,1].bar(Region_F_Ind_counts.index, Region_F_Ind_counts.values, color = 'tab:gray')
axs[1,1].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_F_Ind_counts.values)+10,
                color = 'red', linewidth = 2)
axs[1,1].set_xlim([2000.5, 2021.5])
axs[1,1].set_ylim([0, max(Region_F_Ind_counts.values)+10])
axs[1,1].set_xticks(ticks = np.arange(21)+2001, labels = np.tile('',21), rotation = 90)


axs[2,1].bar(Region_F_Pub_counts.index, Region_F_Pub_counts.values, color = 'tab:blue')
axs[2,1].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_F_Pub_counts.values)+10,
                color = 'red', linewidth = 2)
axs[2,1].set_xlim([2000.5, 2021.5])
axs[2,1].set_ylim([0, 30])
axs[2,1].set_xticks(ticks = np.arange(21)+2001, labels = np.tile('',21), rotation = 90)

axs[3,1].bar(Region_F_Dom_counts.index, Region_F_Dom_counts.values, color = 'black')
axs[3,1].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_F_Dom_counts.values)+10,
                color = 'red', linewidth = 2)
axs[3,1].set_xlim([2000.5, 2021.5])
axs[3,1].set_ylim([0, max(Region_F_Dom_counts.values)+10])
axs[3,1].xaxis.set_major_locator(MultipleLocator(5))
axs[3,1].xaxis.set_minor_locator(MultipleLocator(1))

# Region O
axs[0,2].bar(Region_O_Irr_counts.index, Region_O_Irr_counts.values, color = 'tab:green')
axs[0,2].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_O_Irr_counts.values)+10,
                color = 'red', linewidth = 2)
axs[0,2].set_xlim([2000.5, 2021.5])
axs[0,2].set_ylim([0, max(Region_O_Irr_counts.values)+10])
axs[0,2].set_xticks(ticks = np.arange(21)+2001, labels = np.tile('',21), rotation = 90)

axs[1,2].bar(Region_O_Ind_counts.index, Region_O_Ind_counts.values, color = 'tab:gray')
axs[1,2].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_O_Ind_counts.values)+10,
                color = 'red', linewidth = 2)
axs[1,2].set_xlim([2000.5, 2021.5])
axs[1,2].set_ylim([0, max(Region_O_Ind_counts.values)+10])
axs[1,2].set_xticks(ticks = np.arange(21)+2001, labels = np.tile('',21), rotation = 90)


axs[2,2].bar(Region_O_Pub_counts.index, Region_O_Pub_counts.values, color = 'tab:blue')
axs[2,2].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_O_Pub_counts.values)+10,
                color = 'red', linewidth = 2)
axs[2,2].set_xlim([2000.5, 2021.5])
axs[2,2].set_ylim([0, 10])
axs[2,2].set_xticks(ticks = np.arange(21)+2001, labels = np.tile('',21), rotation = 90)

axs[3,2].bar(Region_O_Dom_counts.index, Region_O_Dom_counts.values, color = 'black')
axs[3,2].vlines([2008.5,2015.5], ymin = 0, ymax = max(Region_O_Dom_counts.values)+10,
                color = 'red', linewidth = 2)
axs[3,2].set_xlim([2000.5, 2021.5])
axs[3,2].set_ylim([0, max(Region_O_Dom_counts.values)+10])
axs[3,2].xaxis.set_major_locator(MultipleLocator(5))
axs[3,2].xaxis.set_minor_locator(MultipleLocator(1))

plt.tight_layout()

#%% Map figure summary plots 

Public_supply_summary = np.zeros((3,3))
K_indx = [1,8,16,21]
F_indx = [0,6,13,18]
O_indx = [0,7,13,16]
for i in range(3):
   Public_supply_summary[0,i] = np.mean(Region_K_Pub_counts[K_indx[i]:K_indx[i+1]])
   Public_supply_summary[1,i] = np.mean(Region_F_Pub_counts[F_indx[i]:F_indx[i+1]])
   Public_supply_summary[2,i] = np.mean(Region_O_Pub_counts[O_indx[i]:O_indx[i+1]])

PS_df = pd.DataFrame(data = Public_supply_summary.copy())
PS_df.columns = ['2000_2007','2008_2015','2015_2020']
for i in range(3):
    PS_df.iloc[i,:] = PS_df.iloc[i,:]/PS_df.iloc[i,0]
    PS_df.iloc[i,:] =  PS_df.iloc[i,:]*100 - 100
    

Irrigation_summary = np.zeros((3,3))
K_indx = [1,9,17,22]
F_indx = [0,6,15,20]
O_indx = [1,9,17,22]
for i in range(3):
   Irrigation_summary[0,i] = np.mean(Region_K_Irr_counts[K_indx[i]:K_indx[i+1]])
   Irrigation_summary[1,i] = np.mean(Region_F_Irr_counts[F_indx[i]:F_indx[i+1]])
   Irrigation_summary[2,i] = np.mean(Region_O_Irr_counts[O_indx[i]:O_indx[i+1]])

Irr_df = pd.DataFrame(data = Irrigation_summary.copy())
Irr_df.columns = ['2000_2007','2008_2015','2015_2020']
for i in range(3):
    Irr_df.iloc[i,:] = Irr_df.iloc[i,:]/Irr_df.iloc[i,0]
    Irr_df.iloc[i,:] =  Irr_df.iloc[i,:]*100 - 100
    


X = ['2008-2015','2015-2020']
K = Irr_df.iloc[0,1:]
F = Irr_df.iloc[1,1:]
O = Irr_df.iloc[2,1:]

X_axis = np.arange(len(X))
Fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(3,2))    
plt.bar(X_axis - 0.2, K, 0.2, label = 'K', color = 'red')
plt.bar(X_axis, F, 0.2, label = 'F', color = 'yellow')
plt.bar(X_axis + 0.2, O, 0.2, label = 'O', color = 'orange')
axs.yaxis.set_minor_locator(MultipleLocator(50))
axs.yaxis.set_major_locator(MultipleLocator(100))
plt.xticks(X_axis, X)
plt.ylabel('% change in well installation')
#plt.legend()
plt.tight_layout()
plt.savefig("Map_Figure_Public_Supply_Wells.svg", format="svg")
plt.show()

X = ['2008_2015','2015_2020']
K = PS_df.iloc[0,1:]
F = PS_df.iloc[1,1:]
O = PS_df.iloc[2,1:]

X_axis = np.arange(len(X))
Fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(3,2))  
plt.bar(X_axis - 0.2, K, 0.2, label = 'K', color = 'red')
plt.bar(X_axis, F, 0.2, label = 'F', color = 'yellow')
plt.bar(X_axis+ 0.2, O, 0.2, label = 'O', color = 'orange')
axs.yaxis.set_minor_locator(MultipleLocator(25))
axs.yaxis.set_major_locator(MultipleLocator(50))
plt.xticks(X_axis, X)
plt.ylabel('% change in well installation')
#plt.legend()
plt.tight_layout()
plt.savefig("Map_Figure_Irrigation_Wells.svg", format="svg")
plt.show()
