# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 12:34:26 2015

@author: Dudz
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

#Specify file path where data is contained
#Get list of file names
path = 'C:\Users\Dudz\Documents\Money\Scripts\AirlinesOnTime\\2015'

def define_files(path):
    files = [ f for f in listdir(path) if isfile(join(path,f)) ]
    
    csvs = []
    
    x = 0
    while x < len(files):
        csvs.append(str(path + '\\' + files[x]))
    
        x = x + 1
    
    return csvs
    
files = define_files(path)


#Function to load CSV and format it
def load_data(csv):
    data = pd.read_csv(csv)
    
    data = pd.DataFrame(data)
    
    data = data [ data['ORIGIN_AIRPORT_ID'] == 12266]
    
    data['YEAR'] = pd.to_datetime(data.FL_DATE).dt.year
    data['MONTH'] = pd.to_datetime(data.FL_DATE).dt.month
    data['DAY'] = pd.to_datetime(data.FL_DATE).dt.day
    data = data.drop('FL_DATE', axis=1)
    data = data.drop('Unnamed: 14', axis=1)    
    
    min_delay = (-15,15)
    
    data.loc[ data.DEP_DELAY.isin(min_delay), 'DEP_DELAY' ] = 0
    data.loc[ data.DEP_DELAY.isnull(), 'DEP_DELAY' ] = 0
    data.loc[ data.ARR_DELAY.isnull(), 'ARR_DELAY' ] = 0
    data.loc[ data.CARRIER_DELAY.isnull(), 'CARRIER_DELAY'] = 0
    data.loc[ data.WEATHER_DELAY.isnull(), 'WEATHER_DELAY'] = 0
    data.loc[ data.NAS_DELAY.isnull(), 'NAS_DELAY'] = 0
    data.loc[ data.SECURITY_DELAY.isnull(), 'SECURITY_DELAY'] = 0
    data.loc[ data.LATE_AIRCRAFT_DELAY.isnull(), 'LATE_AIRCRAFT_DELAY'] = 0
    
    return data
    
#Function to generate monthly stats
def gen_month_stats(data):
    month = data.groupby('MONTH')['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']

    return month

#Function to generate airline based stats
def gen_airline_stats(data):
    airline = data.groupby('AIRLINE_ID')['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']
    
    return airline

#Function to generate destination airport based stats
def gen_des_airport_stats(data):
    des_airport = data_df.groupby('DEST_AIRPORT_ID')['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']

    return des_airport

#Function to generate time of date based stats
def gen_hr_stats(data):
    bins = range(0,2400,100)
    
    hr_bins = pd.cut(data_df.CRS_DEP_TIME, bins)
    
    hr = data_df.groupby(hr_bins)['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']
    
    return hr
    
    
#Function to 
def try_stats(func):
    try:
        var
    except NameError:
        var = func
        var_count = var.count()
        var_median = var.median()
        var_mean = var.mean()
        var_max = var.max()
        var_min = var.min()
    else:
        var = func
        var_count = var_count.append(var.count(), ignore_index=True)
        var_median = var_median.append(var.median(), ignore_index=True)
        var_mean = var_mean.append(var.mean(), ignore_index=True)
        var_max = var_max.append(var.max(), ignore_index=True)
        var_min = var_min.append(var.min(), ignore_index=True)
        
    return var_count, var_median, var_mean, var_max, var_min

#Sequence to load each CSV file individually, convert to DataFrame
#Then calculate stats on each file individually and then delete them from memory

counts = []
data_df = pd.DataFrame()
   
for i in files:
    data = load_data(i)
    print i
    
    counts.append(len(data))
 
    #month_count, month_median, month_mean, month_max, month_min = try_stats(gen_month_stats(data))    
    
    data_df = data_df.append(data, ignore_index=True)
    
    month_stats = gen_month_stats(data_df)
    
    airine_stats = gen_airline_stats(data_df)
    
    des_airport = gen_des_airport_stats(data_df)
    
    hr_stats = gen_hr_stats(data_df)