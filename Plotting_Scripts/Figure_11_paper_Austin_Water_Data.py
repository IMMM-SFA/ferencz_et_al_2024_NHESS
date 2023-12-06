# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 09:51:46 2022

@author: sbferen
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np 
import os

os.chdir("Path to data")


AW_df = pd.read_csv('Austin_Water_supply_data.csv', header = 'infer')

plt.rcParams['font.size'] = 14

fig, ax_left = plt.subplots(nrows=1, ncols=1, figsize=(6,4))
ax_right = ax_left.twinx()
ax_right_2 = ax_left.twinx()
ax_right_2.spines.right.set_position(("axes", 1.2))

ax_left.plot(AW_df.iloc[:,0], 3.78541 * AW_df.iloc[:,1]/10**9, color = 'k', label = 'Supply', 
             linewidth = 3)
ax_left.set_ylabel('Annual Supply (billion L)', fontsize = 14)

ax_right.plot(AW_df.iloc[:,0], AW_df.iloc[:,2]/10**6, color = 'gray', label = 'Population', 
              linewidth = 3)
ax_right.set_ylabel('Population (million)', color = 'gray', fontsize = 14)
ax_right.tick_params(axis = 'y', colors = 'gray')

ax_right_2.plot(AW_df.iloc[:,0], AW_df.iloc[:,3]*3.78541, color = 'tab:blue', label = 'Per capita use', 
                linewidth = 3)
ax_right_2.set_ylabel('Per capita use (L/day)', color = 'tab:blue', fontsize = 14)
ax_right_2.tick_params(axis = 'y', colors = 'tab:blue')

plt.savefig("Figure_11.svg", format="svg")
#plt.tight_layout()

#%% Map figure 
AW_df = pd.read_csv('Water_supply_data.csv', header = 'infer')

plt.rcParams['font.size'] = 14

fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(4,3))

plt.plot(AW_df.iloc[:,0], AW_df.iloc[:,3], color = 'tab:blue', label = 'Per capita use', 
                linewidth = 3)
axs.vlines([2008,2015], ymin = 0, ymax = 200,
                  color = 'red', linewidth = 2, linestyle = '--')
plt.ylabel('Per capita use (gal/day)', fontsize = 14)
plt.ylim([120, 200])
plt.xlim([2000, 2020])
axs.yaxis.set_minor_locator(MultipleLocator(10))
#axs.xaxis.set_minor_locator(MultipleLocator(1))
axs.xaxis.set_major_locator(MultipleLocator(5))
plt.tight_layout()
plt.savefig("Map_Figure_Austin_Water_Use.svg", format="svg")
