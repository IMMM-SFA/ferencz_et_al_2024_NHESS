# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

os.chdir("Data Path")
cpi_data = pd.read_csv('inflation_correction.csv') # inflation correction 

# Import raw USDA annual survey data 
regional_crop_data = ['Crops_region_K_annual_survey.csv', 
                      'Crops_region_F_annual_survey.csv', 
                      'Crops_region_O_annual_survey.csv']

output_folders = ['Region_K_crop_data', 'Region_F_crop_data', 'Region_O_crop_data' ] # processed raw USDA data will be output to new folders 

regions = ['K','F','O']

#%% Crop area (Acres) data filtering for 'Acres Harvested' data by county 

for region in range(3):
    # import regional data 
    if region > 0:
        os.chdir('..')
        
    crop_data = pd.read_csv(regional_crop_data[region], thousands=',')  
    os.mkdir(output_folders[region])
    os.chdir(output_folders[region])
    
    crop_data_area_filtered = crop_data.copy()
    crop_data_area_filtered.drop(columns = ['CV (%)'], inplace = True)
    
    crop_data_area_filtered['flag'] = np.zeros(crop_data_area_filtered.iloc[:,0].size)*np.nan
    for i in range(crop_data_area_filtered.iloc[:,0].size):
        if crop_data_area_filtered.iloc[i,11] == 'NOT SPECIFIED': # 'Domain_category' field 
             crop_data_area_filtered.iloc[i,13] = 1
             
    crop_data_area_filtered.dropna(inplace = True)
    
    crop_data_area_filtered['flag'] = np.zeros(crop_data_area_filtered.iloc[:,0].size)*np.nan
    for i in range(crop_data_area_filtered.iloc[:,0].size):
        temp = crop_data_area_filtered.iloc[i,9].split() # 'Data_item' field
        if any(temp in 'ACRES' for temp in temp) == 1 and any(temp in 'HARVESTED' for temp in temp) == 1:
            crop_data_area_filtered.iloc[i,13] = 1
    
    crop_data_area_filtered.dropna(inplace = True)
    
    counties = crop_data.County.unique()
    crops = crop_data_area_filtered.iloc[:,9].unique() # 'Data_item' column 
    
    
    crop_data_area_filtered_tot = crop_data_area_filtered.copy()
    
    
    for i in range(crop_data_area_filtered_tot.iloc[:,0].size):
        try:
            crop_data_area_filtered_tot.iloc[i,12] = int(crop_data_area_filtered_tot.iloc[i,12].replace(',',''))
        
        except ValueError:
            crop_data_area_filtered_tot.iloc[i,12] = 0
            
        except AttributeError:
            continue

    # Crop area (Acres) for entire region by year 

    Region_crop_area = np.zeros((crops.size, 1))
     
    for i in range(len(crops)):
        data = crop_data_area_filtered_tot
        data = data.where(crop_data_area_filtered_tot.iloc[:,9] == crops[i])
        data.dropna(inplace = True)
        data.sort_values(by = ['Year'], inplace = True)
        years = data.Year.unique()
        arr = np.zeros((years.size, 2))
        arr[:,0] = years
        for j in range(years.size):
            year_data = data.where(data.iloc[:,1] == arr[j,0])
            year_data.dropna(inplace = True)
            arr[j,1] = np.sum(year_data.Value[:])
        Region_crop_area[i] = np.sum(year_data.Value[:])
    
    
    crop_type_indexes = np.where(Region_crop_area[:] > 5000)
    crop_indexes = crop_type_indexes[0] # crop type with more than 5,000 acres in 2017
    
    year_ts = np.arange(62)+1960
    annual_crop_areas = pd.DataFrame(data = np.zeros((len(year_ts),len(crop_indexes))), 
                                                              columns = crops[crop_indexes])
    annual_crop_areas['Year'] = year_ts
    annual_crop_areas.set_index('Year', inplace = True)
    

    for i in range(len(crop_indexes)):
        plt.clf()
        fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(4,3))
        crop_indx = crop_indexes[i]
        data = crop_data_area_filtered_tot
        data = data.where(crop_data_area_filtered_tot.iloc[:,9] == crops[crop_indx])
        data.dropna(inplace = True)
        data.sort_values(by = ['Year'], inplace = True)
        years = data.Year.unique()
        arr = np.zeros((years.size, 2))
        arr[:,0] = years
        for j in range(years.size):
            year_data = data.where(data.iloc[:,1] == arr[j,0])
            year_data.dropna(inplace = True)
            arr[j,1] = np.sum(year_data.Value[:])   
            crop_area_row = np.where(year_ts == years[j])
            annual_crop_areas.iloc[crop_area_row[0][0],i] = np.sum(year_data.Value[:]) 
        annual_crop_areas.iloc[:,i]
        axs.plot(arr[:,0], arr[:,1]/1000) 
        axs.set_xlim([2000,2022])
        axs.vlines([2008,2015], ymin = 0, ymax = max(arr[:,1])/1000+10,
                      color = 'red', linewidth = 2)
        axs.set_ylim([0,max(arr[:,1])/1000+10])
        axs.set_ylabel('Acres [10^3]')
        axs.set_title(crops[crop_indx], fontsize = 8)
        plt.tight_layout()
        plt.savefig('acreage_'+crops[crop_indx]+'.png')
    
    annual_crop_areas.to_csv('Annual_crop_area_Region_' + regions[region] + '.csv')
    
    # Crop sales 
    crop_data_sales_filtered = crop_data.copy()
    crop_data_sales_filtered.drop(columns = ['CV (%)'], inplace = True)
    
    crop_data_sales_filtered['flag'] = np.zeros(crop_data_sales_filtered.iloc[:,0].size)*np.nan
    for i in range(crop_data_sales_filtered.iloc[:,0].size):
        if crop_data_sales_filtered.iloc[i,11] == 'NOT SPECIFIED': # 'Domain_category' field 
             crop_data_sales_filtered.iloc[i,13] = 1
             
    crop_data_sales_filtered.dropna(inplace = True)
    
    crop_data_sales_filtered['flag'] = np.zeros(crop_data_sales_filtered.iloc[:,0].size)*np.nan
    for i in range(crop_data_sales_filtered.iloc[:,0].size):
        temp = crop_data_sales_filtered.iloc[i,9].split() # 'Data_item' field
        if any(temp in 'SALES,' for temp in temp) == 1:
            crop_data_sales_filtered.iloc[i,13] = 1
    
    crop_data_sales_filtered.dropna(inplace = True)
    
    for i in range(crop_data_sales_filtered.iloc[:,0].size):
        try:
            crop_data_sales_filtered.iloc[i,12] = int(crop_data_sales_filtered.iloc[i,12].replace(',',''))
        
        except ValueError:
            crop_data_sales_filtered.iloc[i,12] = 0
            
        except AttributeError:
            continue
    
    crop_data_sales_filtered['cpi_corrected'] = np.zeros(crop_data_sales_filtered.iloc[:,0].size) 
    for i in range(crop_data_sales_filtered.iloc[:,0].size):
        year = crop_data_sales_filtered.iloc[i,1]
        cpi = cpi_data.where(cpi_data.year == year)
        cpi.dropna(inplace = True)
        crop_data_sales_filtered.iloc[i,14] = crop_data_sales_filtered.iloc[i,12]*cpi.iloc[0,1]
        
    Region_crop_sales = np.zeros((crops.size, 1))
    
    crops = np.unique(crop_data_sales_filtered.iloc[:,9])
    
    for i in range(len(crops)):
        data = crop_data_sales_filtered
        data = data.where(crop_data_sales_filtered.iloc[:,9] == crops[i])
        data.dropna(inplace = True)
        data.sort_values(by = ['Year'], inplace = True)
        years = data.Year.unique()
        arr = np.zeros((years.size, 2))
        arr[:,0] = years
        for j in range(years.size):
            year_data = data.where(data.iloc[:,1] == arr[j,0])
            year_data.dropna(inplace = True)
            arr[j,1] = np.sum(year_data.Value[:])
        Region_crop_sales[i] = np.sum(year_data.Value[:])
    
    
    crop_type_indexes = np.where(Region_crop_sales[:] > 5000)
    crop_indexes = crop_type_indexes[0]
    
    for i in range(len(crop_indexes)):
        plt.clf()
        i = crop_indexes[i]
        data = crop_data_sales_filtered
        data = data.where(crop_data_sales_filtered.iloc[:,9] == crops[i])
        data.dropna(inplace = True)
        data.sort_values(by = ['Year'], inplace = True)
        years = data.Year.unique()
        arr = np.zeros((years.size, 3))
        arr[:,0] = years
        for j in range(years.size):
            year_data = data.where(data.iloc[:,1] == arr[j,0])
            year_data.dropna(inplace = True)
            arr[j,1] = np.sum(year_data.Value[:])
            arr[j,2] = np.sum(year_data.cpi_corrected[:])
        plt.scatter(arr[:,0], arr[:,1]/10**6, marker = 'o') 
        plt.plot(arr[:,0], arr[:,1]/10**6, linestyle = '-') 
        plt.scatter(arr[:,0], arr[:,2]/10**6, marker = 'o') 
        plt.plot(arr[:,0], arr[:,2]/10**6, linestyle = ':') 
        plt.ylabel('Sales (million $)')
        plt.title(crops[i])
        plt.tight_layout()
        plt.savefig('sales'+crops[i]+'.png')
        
    # Crop production data filtering by county 
    print('production block ' + regions[region])
    crop_data_production_filtered = crop_data.copy()
    crop_data_production_filtered.drop(columns = ['CV (%)'], inplace = True)
    crop_data_production_filtered = crop_data_production_filtered.dropna()
    
    
    crop_data_production_filtered['flag'] = np.zeros(crop_data_production_filtered.iloc[:,0].size)*np.nan
    for i in range(crop_data_production_filtered.iloc[:,0].size):
        temp = crop_data_production_filtered.iloc[i,9].split()
        if any(temp in 'PRODUCTION,' for temp in temp) == 1:
            crop_data_production_filtered.iloc[i,13] = 1
    
    crop_data_production_filtered.dropna(inplace = True)
    
    
    counties = crop_data.County.unique()
    crops = crop_data_production_filtered.iloc[:,9].unique()
    
    
    crop_data_production_filtered.drop(columns = ['flag'], inplace = True)
    crop_data_production_filtered_tot = crop_data_production_filtered.copy()
    
    for i in range(crop_data_production_filtered_tot.iloc[:,0].size):
        try:
            crop_data_production_filtered_tot.iloc[i,12] = int(crop_data_production_filtered_tot.iloc[i,12].replace(',',''))
        
        except ValueError:
            crop_data_production_filtered_tot.iloc[i,12] = 0
            
        except AttributeError:
            continue

    Region_crop_production = np.zeros((crops.size, 1))
     
    for i in range(len(crops)):
        data = crop_data_production_filtered_tot
        data = data.where(crop_data_production_filtered_tot.iloc[:,9] == crops[i])
        data.dropna(inplace = True)
        data.sort_values(by = ['Year'], inplace = True)
        years = data.Year.unique()
        arr = np.zeros((years.size, 2))
        arr[:,0] = years
        for j in range(years.size):
            year_data = data.where(data.iloc[:,1] == arr[j,0])
            year_data.dropna(inplace = True)
            arr[j,1] = np.sum(year_data.Value[:])
        Region_crop_production[i] = np.sum(year_data.Value[:])
    
    year_ts = np.arange(62)+1960
    annual_crop_production = pd.DataFrame(data = np.zeros((len(year_ts),len(crops))), 
                                                              columns = crops)
    annual_crop_production['Year'] = year_ts
    annual_crop_production.set_index('Year', inplace = True)
    
    for i in range(len(crops)):
        plt.clf()
        fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(4,3))
        data = crop_data_production_filtered_tot
        data = data.where(data.iloc[:,9] == crops[i])
        data.dropna(inplace = True)
        data.sort_values(by = ['Year'], inplace = True)
        years = data.Year.unique()
        arr = np.zeros((years.size, 2))
        arr[:,0] = years
        for j in range(years.size):
            year_data = data.where(data.iloc[:,1] == arr[j,0])
            year_data.dropna(inplace = True)
            arr[j,1] = np.sum(year_data.Value[:])
            crop_prod_row = np.where(year_ts == years[j])
            annual_crop_production.iloc[crop_prod_row[0][0],i] = np.sum(year_data.Value[:])
        axs.plot(arr[:,0], arr[:,1]/1000) 
        axs.set_xlim([2000,2022])
        axs.vlines([2008,2015], ymin = 0, ymax = max(arr[:,1])/1000+10,
                      color = 'red', linewidth = 2)
        axs.set_ylim([0,max(arr[:,1])/1000+10])
        axs.set_ylabel('Production [10^3]')
        axs.set_title(crops[i], fontsize = 8)
        plt.tight_layout()
        plt.savefig('production_'+crops[i]+'.png')
    
    annual_crop_production.to_csv('Annual_crop_production_Region_' + regions[region] + '.csv')



