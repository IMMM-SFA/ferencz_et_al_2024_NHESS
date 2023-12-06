# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 15:26:52 2022

@author: fere556
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os 
import seaborn as sns

os.chdir("C:/Users/fere556/OneDrive - PNNL/Documents/ERCOT/Retrospective_analysis/Data")

wms_df = pd.read_csv('WMS_costs_backup_v3.csv')

# Region_O WMS 
wms_O = wms_df.copy()
wms_O = wms_O.where(wms_O.Region[:] == 'O')
wms_O.dropna(thresh = 4, inplace = True)

# Region_K WMS 
wms_K = wms_df.copy()
wms_K = wms_K.where(wms_K.Region[:] == 'K')
wms_K.dropna(thresh = 4, inplace = True)

# Region_F WMS 
wms_F = wms_df.copy()
wms_F = wms_F.where(wms_F.Region[:] == 'F')
wms_F.dropna(thresh = 4, inplace = True)

#%% Volume supplied, Number, and Cost of strategies (in 2022 $'s)

strategies = wms_df.Type_Category.unique()

fields = strategies.tolist()
fields.insert(0, 'year')

strategies_vol = pd.DataFrame(np.zeros((3, len(strategies)+1)), columns = fields)
strategies_count =  pd.DataFrame(np.zeros((3, len(strategies)+1)), columns = fields)
strategies_cost =  pd.DataFrame(np.zeros((3, len(strategies)+1)), columns = fields)

year = [2011, 2016, 2021]

for i in range(3): # water plan year (row)
    # Filter by year 
    strategies_year = wms_df.where(wms_df.Year == year[i])
    strategies_year.dropna(thresh = 6, inplace = True)
    
    for j in range(len(strategies)): # strategy (column)
        
        # Filter by strategy type 
        strategy = strategies_year.copy()
        strategy = strategy.where(strategy.Type_Category == strategies[j]) 
        strategy.dropna(thresh = 6, inplace = True)
        
        # Volume
        strategies_vol.iloc[i,j+1] = strategy.Volume.sum()
        
        # Number
        strategies_count.iloc[i,j+1] = len(strategy.Volume)
        
        # Cost 
        strategies_cost.iloc[i,j+1] = strategy.iloc[:,9].mean()
        
        
# Box and whisker of unit cost ($ per acft for each strategy)
cost_boxplot = np.zeros((500, len(strategies)))

for i in range(len(strategies)):
    strategy = wms_df.copy()
    strategy = strategy.where(strategy.Type_Category == strategies[i]) 
    strategy.dropna(thresh = 6, inplace = True)
    numstrat = len(strategy.Volume)
    cost_boxplot[0:numstrat, i] = strategy.iloc[:,9]
    cost_boxplot[numstrat:, i] = np.nan

plt.figure(figsize = [8,6]) 
sns.boxplot(data = cost_boxplot, color = 'gray')
plt.ylim([0, 3500])
plt.xticks(np.arange(19),strategies, rotation = 'vertical')

# convert unit cost to $/m^3
wms_df.iloc[:,9] = wms_df.iloc[:,9]/1233.48

plt.figure(figsize = [8,4])       
sns.boxplot(data = wms_df, x = 'Type_Category', y = '2022_Cost',  hue = 'Region', palette = {'K': 'magenta', 'F': 'indigo', 'O': 'green'})
plt.legend([],[], frameon=False)
plt.ylim([0, 3])
plt.xlim([-0.5,18.5])
plt.xticks(np.arange(19),strategies, rotation = 'vertical')  
plt.savefig("Figure_WMS.svg", format="svg")

#%% Strategy volumes by region 
volume_F = pd.DataFrame(np.zeros((3, len(strategies)+1)), columns = fields)
volume_K = pd.DataFrame(np.zeros((3, len(strategies)+1)), columns = fields)
volume_O = pd.DataFrame(np.zeros((3, len(strategies)+1)), columns = fields)

for i in range(3): # water plan year (row)
    # Filter by year 
    strategies_year = wms_df.where(wms_df.Year == year[i])
    strategies_year.dropna(thresh = 6, inplace = True)
    
    for j in range(len(strategies)): # strategy (column)
        
        # Filter by strategy type 
        strategy = strategies_year.copy()
        strategy = strategy.where(strategy.Type_Category == strategies[j]) 
        strategy.dropna(thresh = 6, inplace = True)
        
        # Strategy Volume F
        region = strategy.copy()
        region = strategy.where(region.Region == 'F')
        region.dropna(thresh = 6, inplace = True)
        volume_F.iloc[i,j+1] = region.Volume.sum()
        
        # Strategy Volume K
        region = strategy.copy()
        region = strategy.where(region.Region == 'K')
        region.dropna(thresh = 6, inplace = True)
        volume_K.iloc[i,j+1] = region.Volume.sum()
        
        # Strategy Volume O
        region = strategy.copy()
        region = strategy.where(region.Region == 'O')
        region.dropna(thresh = 6, inplace = True)
        volume_O.iloc[i,j+1] = region.Volume.sum()


# Regional volumes for top strategies 
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(8, 3))

region_K_indx = [2,3,4,11,14,17]
region_K_labels = ['Conservation','SW Contract','Reuse', 'Return Flows', 
                   'Drought Management', 'New Reservoir']
colors = ['green','grey','black']
for i in range(len(region_K_indx)):
    axs[0].plot(volume_K.iloc[:,region_K_indx[i]])
    axs[0].set_ylim([0,210000])
    
region_F_indx = [2, 6, 8, 12, 1]
region_F_labels = ['Conservation', 'Groundwater', 'Subordination', 
                   'Treatment', 'Brush Control' ]
colors = ['green', 'blue', ]
for i in range(len(region_F_indx)):
    axs[1].plot(volume_F.iloc[:,region_F_indx[i]])
    axs[1].set_ylim([0,80000])
                
region_O_indx = [2, 6, 9, 7]
region_O_labels = ['Conservation', 'Groundwater', 'ASR', 'Infrastructure']
colors = ['green', 'blue', ]
for i in range(len(region_O_indx)):
    axs[2].plot(volume_O.iloc[:,region_O_indx[i]])
    axs[2].set_ylim([0,55000])

fig.tight_layout()

