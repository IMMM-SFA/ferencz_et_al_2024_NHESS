# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 11:42:29 2022

@author: sbferen
"""

import os 
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


os.chdir("Path to Data")
wms_data = pd.read_csv('Planned_supply_and_needs_bar_plot_data_final.csv')

#%% Water use restrictions 
labels = ['2011', '2016', '2021']

width = 0.5       # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots(nrows = 3, ncols = 4, figsize = (8,7))
colors = ['tab:green', 'tab:blue', 'gold', 'gray']
for j in range(3):
    for i in range(4):
        ax[j,i].bar(labels, 1233.48 * wms_data.iloc[j*4+i,1:4]/10**6, width, color = colors[i])
        ax[j,i].bar(labels, 1233.48 * wms_data.iloc[j*4+i,4:7]/10**6, width, fill = False, edgecolor = 'red', linewidth = 2)

plt.tight_layout()

plt.savefig("Figure_10_Planned_Supply.svg", format="svg")
