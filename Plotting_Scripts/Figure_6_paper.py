# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 09:36:54 2023

@author: fere556
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os 
import matplotlib.dates as mdates


os.chdir("C:/Users/fere556/OneDrive - PNNL/Documents/ERCOT/Retrospective_analysis/Discharge_and_water_quality_data")

# Import processed daily average flow data 
San_saba_D = pd.read_csv('San_saba_daily.csv', index_col  = 0)
S_conch_D = pd.read_csv('S_concho_daily.csv', index_col  = 0)
Barton_D = pd.read_csv('Barton_flow_daily.csv', index_col  = 0)

# Import USGS daily flow data
USGS_daily_flow = pd.read_csv('USGS_Colorado_Basin_daily_flow.csv')

# Import water quality Data 
Ivie = pd.read_csv('OH_Ivie_filtered.csv')
Spense = pd.read_csv('Spense_filtered.csv')
Travis = pd.read_csv('Lake_Travis_WQ_filtered.csv')
Buchanon = pd.read_csv('Lake_Buchanon_WQ_filtered.csv')
CO_Nit = pd.read_csv('Colorado_River_Downstream_of_Austin_Nitrogen.csv')
CO_Pho = pd.read_csv('Colorado_River_Downstream_of_Austin_Phosphorus.csv')

#%% Caluclate annual flow

S_conch_annual_arr = np.zeros((len(S_conch_D.iloc[:,0]),4))
for i in range(len(S_conch_annual_arr[:,0])):
    S_conch_annual_arr[i,0] = S_conch_D.iloc[i,0].split('/')[0]
    S_conch_annual_arr[i,1] = S_conch_D.iloc[i,0].split('/')[1]
    S_conch_annual_arr[i,2] = S_conch_D.iloc[i,0].split('/')[2]
    S_conch_annual_arr[i,3] = S_conch_D.iloc[i,1]

S_conch_years = np.unique(S_conch_annual_arr[:,2])
S_conch_annual = np.zeros((len(S_conch_years),2))

for i in range(len(S_conch_years)):
    temp = np.where(S_conch_annual_arr[:,2] == S_conch_years[i])
    S_conch_annual[i,1] = np.mean(S_conch_annual_arr[temp,3])
   
San_saba_annual_arr = np.zeros((len(San_saba_D.iloc[:,0]),4))
for i in range(len(San_saba_annual_arr[:,0])):
    San_saba_annual_arr[i,0] = San_saba_D.iloc[i,0].split('/')[0]
    San_saba_annual_arr [i,1] = San_saba_D.iloc[i,0].split('/')[1]
    San_saba_annual_arr[i,2] = San_saba_D.iloc[i,0].split('/')[2]
    San_saba_annual_arr[i,3] = San_saba_D.iloc[i,1]

San_saba_years = np.unique(San_saba_annual_arr[:,2])
San_saba_annual = np.zeros((len(San_saba_years),2))

for i in range(len(San_saba_years)-1):
    temp = np.where(San_saba_annual_arr[:,2] == San_saba_years[i])
    San_saba_annual[i,1] = np.mean(San_saba_annual_arr[temp,3])

   
Barton_annual_arr = np.zeros((len(Barton_D.iloc[:,0]),4))
for i in range(len(Barton_annual_arr[:,0])):
    Barton_annual_arr[i,0] = Barton_D.iloc[i,0].split('/')[0]
    Barton_annual_arr[i,1] = Barton_D.iloc[i,0].split('/')[1]
    Barton_annual_arr[i,2] = Barton_D.iloc[i,0].split('/')[2]
    Barton_annual_arr[i,3] = Barton_D.iloc[i,1]

Barton_years = np.unique(Barton_annual_arr[:,2])
Barton_annual = np.zeros((len(Barton_years),2))

for i in range(len(Barton_years)-1):
    temp = np.where(Barton_annual_arr[:,2] == Barton_years[i])
    data = np.sort(Barton_annual_arr[temp,3])
    Barton_annual[i,1] = np.mean(data[0:len(data[0,:])-10])

#%% Flow duration plots 

# Columns for flow duration plots: 8147000 (2), 8158000 (11), 8162000 (7), 
#                                  8151500 (5), 8128000 (10), Barton (separate file)

# Produces subplots a, b, c, d, e, f in that order 

Periods = [0, 2922, 5722, 8036] # indexes for pre, drought, post periods 
gauge_indexes = [2, 11, 7, 5, 10]
y_min = [0.1, 1, 1, 1, 1, 10 ]
y_max = [200, 500, 1000, 3000, 200, 200]

for k in range(6):

    
    if k != 5:
        column = gauge_indexes[k]
        data = USGS_daily_flow.iloc[:,column] 
        gauge = USGS_daily_flow.columns
        title = gauge[column]
    else: 
        data = Barton_D.iloc[:,0]
        Periods = [0, 2499, 5048, 6534]
        title = 'Barton'
        
    # temp arrays
    flow_pre = data[Periods[0]:Periods[1]]
    flow_pre = flow_pre.dropna()
    flow_drought = data[Periods[1]:Periods[2]]
    flow_drought = flow_drought.dropna()
    flow_post =  data[Periods[2]:Periods[3]]
    flow_post = flow_post.dropna()
    
    # sort
    flow_pre = flow_pre.sort_values() 
    flow_drought = flow_drought.sort_values() 
    flow_post = flow_post.sort_values() 
    
    # convert to m^3/s 
    flow_pre = 0.0283168 * flow_pre
    flow_drought = 0.0283168 * flow_drought
    flow_post = 0.02831688 * flow_post 
    
    # rank
    rank_pre = np.arange(len(flow_pre)) + 1
    rank_drought = np.arange(len(flow_drought)) + 1
    rank_post = np.arange(len(flow_post)) + 1
    
    # exceedance probability 
    exceedance_pre = np.zeros(len(rank_pre))
    exceedance_drought = np.zeros(len(rank_drought))
    exceedance_post = np.zeros(len(rank_post))
    
    for i in range(len(rank_pre)):
        exceedance_pre[i] = 100 * (rank_pre[i]/(1 + len(rank_pre)))
    
    for i in range(len(rank_drought)):  
        exceedance_drought[i] = 100 * (rank_drought[i]/(1 + len(rank_drought)))
        
    for i in range(len(rank_post)):    
        exceedance_post[i] = 100 * (rank_post[i]/(1 + len(rank_post)))
    
    # plot 
    fig, axs = plt.subplots(1, 1, figsize=(3, 2))
    axs.plot(exceedance_pre, flow_pre[::-1], color = 'k', linestyle = '--')
    axs.plot(exceedance_drought, flow_drought[::-1], color = 'red')
    axs.plot(exceedance_post, flow_post[::-1], color = 'k', linestyle = ':')
    plt.title(title)
    plt.yscale('log')
    plt.grid(which = 'both', axis = 'both')
    #axs.yaxis.set_minor_locator(MultipleLocator(100))
    axs.xaxis.set_major_locator(MultipleLocator(50))
    axs.xaxis.set_minor_locator(MultipleLocator(10))
    plt.ylim([y_min[k], y_max[k]])
    plt.savefig(title + "_flow_duration.svg", format="svg")
    
    
    fig, axs = plt.subplots(1, 1, figsize=(3, 1))
    percentiles = np.linspace(0,100,21, endpoint = True)
    percent_reduction = np.zeros(21)
    flow_pre = flow_pre.reset_index(drop = True)
    flow_drought = flow_drought.reset_index(drop = True)
    for i in range(21):
        dif_pre = np.absolute(exceedance_pre-percentiles[i]) 
        index_pre = dif_pre.argmin()
        dif_drought = np.absolute(exceedance_drought-percentiles[i])
        index_drought = dif_drought.argmin()
        
        percent_reduction[i] = 100 * (flow_pre[index_pre] - flow_drought[index_drought])/flow_pre[index_pre] 
        
    axs.plot(percentiles, percent_reduction[::-1], color = 'k', linestyle = '-')
    plt.grid(which = 'both', axis = 'both')
    plt.title(title)
    axs.yaxis.set_major_locator(MultipleLocator(20))
    axs.yaxis.set_minor_locator(MultipleLocator(10))
    axs.xaxis.set_major_locator(MultipleLocator(50))
    axs.xaxis.set_minor_locator(MultipleLocator(10))
    plt.ylim([0, 100])
    plt.xlim([0, 100])
    plt.savefig(title + "_percent_change.svg", format="svg")


#%% Plot Water Quality Data - produces subplot g, h, i in that order

years_df = pd.DataFrame({'year': np.arange(21)+2000,
                   'month': 6*np.ones(21),
                   'day': 15*np.ones(21)})
years_df = pd.to_datetime(years_df)

periods_df = pd.DataFrame({'year': [2000, 2007, 2016, 2020, 2002, 2005],
                   'month': [1, 12, 1, 12, 1, 1],
                   'day': [1, 31, 1, 31, 1, 1]})

periods_df = pd.to_datetime(periods_df)

# Ivie ans Spense Reservoirs: Specific Conductance
fig, axs = plt.subplots(1, 1, figsize=(4, 2))
dates_Ivie = pd.to_datetime(Ivie.iloc[:,6], format='%m/%d/%Y')
dates_Spense = pd.to_datetime(Spense.iloc[:,6], format='%m/%d/%Y')
plt.scatter(dates_Ivie, Ivie.Value[:], marker = '.', color = 'black', zorder = 1)
plt.scatter(dates_Spense, Spense.Value[:], facecolors = 'none', edgecolors = 'grey', zorder = 1)
axs.vlines(x = periods_df[1], ymin = 0, ymax = 5000, color = 'red')
axs.vlines(x = periods_df[2], ymin = 0, ymax = 5000, color = 'red')
plt.ylim([1000, 5000])
plt.xlim([(periods_df[0]),periods_df[3]])
#plt.xticks(rotation=90)
plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))
plt.gca().xaxis.set_minor_locator(mdates.YearLocator(1))
plt.savefig("WQ_Ivie_Spense.svg", format="svg")

# Travis and Buchanon: Specific Conductance
fig, axs = plt.subplots(1, 1, figsize=(4, 2))
dates_Travis = pd.to_datetime(Travis.iloc[:,3], format='%m/%d/%Y')
dates_Buchanon = pd.to_datetime(Buchanon.iloc[:,4], format='%m/%d/%Y')
plt.scatter(dates_Travis, Travis.Value[:], marker = '.', color = 'black', zorder = 1)
plt.scatter(dates_Buchanon, Buchanon.Value[:], facecolors = 'none', edgecolors = 'grey', zorder = 1)
axs.vlines(x = periods_df[1], ymin = 0, ymax = 1000, color = 'red')
axs.vlines(x = periods_df[2], ymin = 0, ymax = 1000, color = 'red')
plt.ylim([350, 650])
plt.xlim([(periods_df[0]),periods_df[3]])
#plt.xticks(rotation=90)
plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))
plt.gca().xaxis.set_minor_locator(mdates.YearLocator(1))
plt.savefig("WQ_Buc_Travis.svg", format="svg")


# Colorado River downstream of Austin: Nitrogen and Phosphorus 
fig, ax_left = plt.subplots(nrows=1, ncols=1, figsize=(4,2))
ax_right = ax_left.twinx()

dates = pd.to_datetime(CO_Nit.iloc[:,6], format='%m/%d/%Y')
ax_left.scatter(dates, CO_Nit.iloc[:,17], marker = '.', color = 'black', zorder = 1)
ax_left.set_ylabel('Nitrogen (mg/L)', fontsize = 14)
ax_left.set_ylim([0, 10])
ax_left.set_xlim([(periods_df[0]),periods_df[3]])
ax_left.vlines(x = periods_df[1], ymin = 0, ymax = 1000, color = 'red')
ax_left.vlines(x = periods_df[2], ymin = 0, ymax = 1000, color = 'red')

dates = pd.to_datetime(CO_Pho.iloc[:,6], format='%m/%d/%Y')
ax_right.scatter(dates, CO_Pho.iloc[:,17], facecolors = 'none', edgecolors = 'grey')
ax_right.set_ylabel('Phosphorus (mg/L)', color = 'grey', fontsize = 14)
ax_right.tick_params(axis = 'y', colors = 'gray')
ax_right.set_ylim([0, 2.2])
ax_right.set_xlim([(periods_df[0]),periods_df[3]])

ax_left.xaxis.set_major_locator(mdates.YearLocator(5))
ax_left.xaxis.set_minor_locator(mdates.YearLocator(1))

plt.savefig("WQ_Colorado_River.svg", format="svg")







