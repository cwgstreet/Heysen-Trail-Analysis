#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Module name:  HT-analysis.py
# Purpose:      Extact and analyse Heysen Trail thru-hike data
# 
# Notes:        Main module
#
# Copyright:    2019, release under GPL3. See LICENSE file for details
#               Carl W Greenstreet <cwgstreet@gmail.com>
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#  
# PURPOSE:
# 
# My overarching purpose is to begin to learn Python so apologies for  
#   the kludgy structure & code.  We all have to start somewhere!  
#
#  Main script: 
#       HT-analysis.py
#
#  Modules:
#       config.py - global variables
#       debug.py - debug nd console message functions
#       extract_tripidx.py - extrap or load trip id's
#       extract_data.py - extract or load trail journal data
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
import datetime   # manage date time formats
import os      # access files on drive
import re      # regulr expression to find strings
import time    # time to allow sleep pause for JS to catch up

# import HT-analysis modules
#import extract_data  :TODO  uncomment once module is working
import config           #global variables
import debug            #debug functions - variable values / types / counts
import extract_tripidx  #extrap or load trip id's

# import third party libraries
#import bs4      # beautiful soup 4 library to parse website
#import lxml     # lxml best html parser to use with beautiful soup
#import requests # 3rd party Requests library to querry website

# import specific third party libaries
from selenium import webdriver

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_dynamic_HTML(target_url):
    """uses ChromeDriver to extract dynamic JS generated (inner) HTML"""
    
    # run headless mode; runs faster & consumes less resources
    #  see https://masterwebscrapingwithpython.com/book/download-html.html
    options = webdriver.ChromeOptions()
    options.headless = True

    
    browser_path = r"/Applications/chromedriver"   #local path
    
    
    browser = webdriver.Chrome(executable_path=browser_path,
                                options=options) 
    
    browser.get(target_url) #navigate to the page

    time.sleep(5)  #give Java Script time to catch up otherwise fails
    JS_dynamic_HTML = browser.page_source  #https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python

    return JS_dynamic_HTML
    
    # close browser - choose appropriate
    browser.close()  # doesn’t always stop the web driver that’s running in background
    #browser.quit()  # warning: kills all instances of Chrome and Chromedriver

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    # Set debugging status: on=True or off=False
    debug_flag = True
    debug.status_msg(debug_flag)
    
    # Extract gstreet trip ids (tripidx) from rambl.com html
    extract_tripidx.get_tripidx(debug_flag)    
    
            
    
    # # 4. Scrape ramblr.com to obtain trail journal data
    # # ----------------------------------------------------------------------
    
    # if os.path.isfile('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/heysen_data.csv'):  
        # debug.debug.console_msg('Importing heysen_data.csv into tripidx[] list')
        
        # with open('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/heysen_data.csv', 'r') as f:
            # reader = csv.reader(f)
            # tripidx = list(reader)
            
        # debug.val_type(tripidx, debug_flag)
        
    # else:
        
        # debug.console_msg('heysen_data.csv file does not exist. \n\tWill scrape ramblr.com for data')
    
        # # ------------------------------------------------------------------
        # # Create list of URLs to scrape in format of 
        # #   webpage/web/mymap/trip/user_id/trip_id
        # #   target_url = "https://www.ramblr.com/web/mymap/trip/478170/tripidx/"
        
        # URL_prefix = "https://www.ramblr.com/web/mymap/trip/478170/"
        
        # URLs = []  #must first create empty list to append to within for loop
        
        
        # #list comprehension to convert tripidx list to list of strings
        # # for reference, same as following 3 lines below
        # # ids = []
        # # for tripid in tripidx[0]:
            # # ids.append(str(tripid))    
        
        # ids = [str(tripid) for tripid in tripidx[0]]  #list comprehension
        
        # debug.val_type(ids, debug_flag)
        # print ("\t count =",len(ids)) 
    
        # for id in ids:
            # URL = (URL_prefix + id)
            # URLs.append(URL)
            # debug.val_type(URL, debug_flag)  # debug code:  target URLs
    
        # # ------------------------------------------------------------------
        # # Capture web page info for each URL
        
        # for URL in URLs:
            # #target_url = URL
            # target_url = "https://www.ramblr.com/web/mymap/trip/478170/1576327 #debug test case"
            # debug.val_type(target_url, debug_flag)  # debug code:  target URLs
    
            # # get JS generated dynamic HTML page
            # JS_dynamic_HTML = get_dynamic_HTML(target_url)
            
            # # Parse  JS_dynamic_HTML  variable, and store it in Beautiful Soup format
            # soup_JS_dynamic = bs4.BeautifulSoup(JS_dynamic_HTML, "lxml")
            
            # # use beautiful soup function prettify to display page
            # #print (soup_JS_dynamic.prettify()) # comment out as not needed once captured to text file
            
            # Title = soup_JS_dynamic.h1
            # Title = str(Title)
            # title=Title[Title.find("h1>")+3:Title.find("</h1>")]
            # print ("\nTitle =",title)
            # print ("\tTitle type:",(type(title))) #debug
    
                
            # break  #temporary - only perform one pass of for loop
            
    
