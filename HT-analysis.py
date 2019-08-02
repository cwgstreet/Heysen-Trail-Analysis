#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  HT-analysis.py
#  
#  Copyright 2019 Carl W Greenstreet <cwgstreet@gmal.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# PURPOSE:
# 
# Overarching purpose is to begin to learn Python so apologies for poor
#   structure & code.  We all have to start somewhere!  
#
# Workflow for this python program: 
#  1) Scrape ramblr.com website and extract list of tripidx values 
#      (trip IDs) from my Heysen Trail multi-day thru-hike journals
#  2) Use tripidx list to scrape trail journal data (58 days x 15 
#       data items)
#  3) Load data into pandas dataframes, 
#  4) clean-up dataframes 
#  5) write csv file(s) to minimise need to scrape web
#  6) Analyse data 
#  7) create plots
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# 1. Import libraries
# ----------------------------------------------------------------------

# import standard libraries
import csv     # i/o of csv files
import inspect # to get variable names
import os      # access files on drive
import re      # regulr expression to find strings
import time    # time to allow sleep pause for JS to catch up

# import third party libraries
import bs4      # beautiful soup 4 library to parse website
import lxml     # lxml best html parser to use with beautiful soup
import requests # 3rd party Requests library to querry website

# import specific third party libaries
from selenium import webdriver

# 2. functions
# ----------------------------------------------------------------------

def console_msg(msg):
    """Display a message on console window"""
    clear = "\n" * 2
    print(clear)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++\
                # \n\t" +msg +"\
          \n+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(clear)
  
def retrieve_name(var):
    """
    Gets the name of var. Does it from the out-most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]

def debug_val_type(debug_target):
    """Prints variable name, value and type to console window"""
    var_name = str(debug_target)
    print("\n"+retrieve_name(debug_target)+" = ",debug_target)
    print("\t"+retrieve_name(debug_target)+" type:",type(debug_target))
    


# 3. Create list of search page strings (list URLs)
# ----------------------------------------------------------------------

# Check if tripidx[] list exists as csv file to avoid unecessary
#   web scraping  
#   if true, load csv file
#   if false, scrape web and generate list

if os.path.isfile('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/tripidx.csv'):  
    console_msg('Importing tripidx.csv into tripidx[] list')
    
    with open('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/tripidx.csv', 'r') as f:
        reader = csv.reader(f)
        tripidx = list(reader)
        
    debug_val_type(tripidx)
    
else:
    page_numbers = [str(x) for x in range(1,5)]  #list comprehension; create list of strings
    debug_val_type(page_numbers)  # debug code:  page numbers

    URL_prefix = "https://www.ramblr.com/web/mymap/trip/478170#h=1&u_uid=478170&type=1&unit=1&page="
    URL_suffix = "&stext=&active=0&sort=10&receivegid="
    
    URLs = []  #must first create empty list to append to within for loop
    
    for page in page_numbers:
        URL = (URL_prefix + page + URL_suffix)
        URLs.append(URL)
        debug_val_type(URL)  # debug code:  page numbers
        
        

# debug code: check list contents
# print(URLs)
# print("\n-------------")
# print("URLs[0]=]", URLs[0])
# print("\tURLs[0] type:", type(URLs[0]))
# # print(URLs[1])
# # print(URLs[2])
# # print(URLs[3])
# print("-------------")





