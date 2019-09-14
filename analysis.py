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


# def load_df(debug_flag, HT_DATA):
    
    # """ create pandas dataframe from zipped list"""
    
    # df = pd.DataFrame(HT_DATA, columns = ['trip_id', 'title', 'day',
                                            # 'date', 'start', 'stop',
                                            # 'council', 'total_duration',
                                            # 'active_duration', 
                                            # 'paused_duration' , 'distance',
                                            # 'avg_speed', 'highest_point', 
                                            # 'total_ascent', 'difficulty'] ) 
    
    # debug.print_df

def load_df_csv(debug_flag, FILEPATH, DF_FILENAME):
    """ create pandas dataframe from csv file"""
    
    df = pd.read_csv(FILEPATH + DF_FILENAME, index_col=0)
    #df = pd.read_csv("/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/data/heysen_df_scrubbed.csv", index_col=0)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    debug.print_df(df, debug_flag)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    return df

# def export_df(debug_flag, FILEPATH, DF_FILENAME):
    # """ write dataframe to csv file"""
    # df.to_csv(path_or_buf='test_df.csv', encoding='utf-8')
    
    
if __name__ == "__main__":
  
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    # # Set debugging status: on=True or off=False
    debug_flag = True
    debug.status_msg(debug_flag)

    FILEPATH = "/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/data/"
    # TRIPID_FILENAME = "tripidx.csv"
    DF_FILENAME = "heysen_df_scrubbed.csv"
    
    
    print("----------------------------------------------------------")

    print("file located at:" + FILEPATH + DF_FILENAME)
    
    # load df from csv file
    df = load_df_csv(debug_flag, FILEPATH, DF_FILENAME)
    print("Dataframe : " , df, sep='\n')

    print("\n----------------------------------------------------------")

    # created dataframe
    #load_df(debug_flag, config.HT_data)
              

    # print("Dataframe : " , df, sep='\n')
    
    # print("/n/n")
    
    # print(df.head)

# print('############################################################')  #make it easier to find this section in terminal output


#print('############################################################')  #make it easier to find this section in terminal output

#print('############################################################')  #make it easier to find this section in terminal output
            
#print('\n############################################################')  #make it easier to find this section in terminal output





    

