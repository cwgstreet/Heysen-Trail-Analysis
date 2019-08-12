#!/usr/bin/env python3
# -*- coding: utf-8 -*-

  
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Module name: analysis.py
# Purpose:     analyse Heysen Trail trip data from rambl.com html
# 
# Notes:       load pandas, clense data, calc stats 
#
# Copyright:   2019, release under GPL3. See LICENSE file for details
#              Carl W Greenstreet <cwgstreet@gmail.com>
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# 1. Import standard libraries

# import standard libraries
import csv          # i/o of csv files
import datetime     # manage date time formats
import os           # access files on drive
# import re           # regular expressions to extract strings
# import time         # time to allow sleep pause for JS to catch up

# import HT-analysis modules
import config           # global variables
import debug            # debug functions - variable values/types/counts
import extract_data     # Extract Heysen Trail trip data from rambl.com html
import extract_tripidx  # extrap or load trip id's
import extract_page     # extract dynamic JS generated (inner) HTML
import file_io          # write / read csv files to local disk


#import third party libary specific imports
import pandas as pd # pandas to create dataframes
# import bs4      # beautiful soup 4 library to parse website
# import lxml     # lxml to parse website
# import requests # requests to get http


# import specific third party libaries
# from selenium import webdriver


def load_df(debug_flag, HT_DATA):
    
    """ create pandas dataframe from zipped list"""
    
    df = pd.DataFrame(zippedList, columns = ['trip_id', 'title', 'day',
                                            'date', 'start', 'stop',
                                            'council', 'total_duration',
                                            'active_duration', 
                                            'paused_duration' , 'distance',
                                            'avg_speed', 'highest_point', 
                                            'total_ascent', 'difficulty'] ) 
    
    debug.print_df

def export_df(debug_flag, FILEPATH, DATA_FILENAME, DF_FILENAME):
    """ write dataframe to csv file"""
    df.to_csv(path_or_buf='test_df.csv', encoding='utf-8')
    
    
    
    
    
if __name__ == "__main__":
  
    # # Set debugging status: on=True or off=False
    debug_flag = True
    debug.debug_status(debug_flag)

    FILEPATH = "/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/"
    TRIPID_FILENAME = "tripidx.csv"
    DATA_FILENAME = "heysen_data.csv"
    
    print("file at:" + FILEPATH + DATA_FILENAME)
    
    # load up or extract Heysen data from ramblr.com
    extract_data.get_data(debug_flag, FILEPATH, config.HT_data)  
    
    # created dataframe
    load_df(debug_flag)
              

    print("Dataframe : " , df, sep='\n')
    
    print("/n/n")
    
    print(df.head)

# print('############################################################')  #make it easier to find this section in terminal output


#print('############################################################')  #make it easier to find this section in terminal output

#print('############################################################')  #make it easier to find this section in terminal output
            
#print('\n############################################################')  #make it easier to find this section in terminal output





    

