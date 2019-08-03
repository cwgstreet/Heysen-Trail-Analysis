#!/usr/bin/env python3
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
# My overarching purpose is to begin to learn Python so apologies for  
#   the kludgy structure & code.  We all have to start somewhere!  
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
from pprint import pprint


# 2. functions
# ----------------------------------------------------------------------

def console_msg(msg):
    """Display a message on console window"""
    clear = "\n" * 2
    print(clear)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++\
          \n\t" +msg +"\
          \n+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
  
def retrieve_name(var):
    """
    Gets the name of var. Does it from the out-most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    #https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string/18425523
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]

def debug_val_type(debug_target):
    """Prints variable name, value and type to console window
        when switch debug_on = true"""
    if debug_on:
        var_name = str(debug_target)
        print("\n"+retrieve_name(debug_target)+" = ",debug_target)
        print("\t"+retrieve_name(debug_target)+" type:",type(debug_target))
    

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
# Debugging
#   turn debugging on (True) or off (False)

debug_on = True

if debug_on:
    console_msg('Debugging is ON')
else:
    console_msg('Debugging is OFF')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# 3. Create list of search page strings (list URLs)
# ----------------------------------------------------------------------

# Check if tripidx[] list exists as csv file to avoid unecessary
#   web scraping  
#   if true, load csv file
#   if false, scrape web and generate list

if os.path.isfile('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/tripidx.csv'):  
    console_msg('Importing tripidx.csv into tripidx[] list')
    
    with open('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/tripidx.csv', 'r') as f:
        tripidx=[]
        reader = csv.reader(f, delimiter=',')
        tripidx = list(reader)
        
    debug_val_type(tripidx)  # debug code:  page numbers
    print(tripidx[0][1])
    print ("\t count =",len(tripidx)) 

    
    
else:
    
    console_msg('tripidx.csv file does not exist. \n\tWill scrape ramblr.com for data')
    
    page_numbers = [str(x) for x in range(1,5)]  #list comprehension; create list of strings
    debug_val_type(page_numbers)  # debug code:  page numbers

    URL_prefix = "https://www.ramblr.com/web/mymap/trip/478170#h=1&u_uid=478170&type=1&unit=1&page="
    URL_suffix = "&stext=&active=0&sort=10&receivegid="
    
    URLs = []  #must first create empty list to append to within for loop
    
    for page in page_numbers:
        URL = (URL_prefix + page + URL_suffix)
        URLs.append(URL)
        debug_val_type(URL)  # debug code:  page numbers
        
        
    # Capture tripidx data from target web pages and load into a list
    tripidx=[]	#create empty list to extend data into within for loop
    
    for URL in URLs:
    
        # specify the target url URL in format of 
        #   webpage/web/mymap/trip/user_id/trip_id
        target_url = URL
        # Example URL for testing:
        #target_url = "https://www.ramblr.com/web/mymap/trip/478170#h=1&u_uid=478170&type=1&unit=1&page=1&stext=&active=0&sort=10&receivegid="

        # get JS generated dynamic HTML page
        JS_dynamic_HTML = get_dynamic_HTML(target_url)
        
        # Parse  JS_dynamic_HTML  variable, and store it in Beautiful Soup format
        soup_JS_dynamic = bs4.BeautifulSoup(JS_dynamic_HTML, "lxml")
        
        # use beautiful soup function prettify to display page
        #print (soup_JS_dynamic.prettify()) # comment out as not needed once captured to text file
        
        # Extract tripidx values from Trail Journal web page
            
        tripidx_string = str(soup_JS_dynamic.find_all('div', class_ = "lists pr nomysession") )	# note: class_ uses trailing "_" to avoid conflict
        #                                                                                          between html "class" with Python keyword "class"
        # debug code follows
        #print("\n-------------")
        #print("\nTrip ID=",tripidx_string)  #debug
        #print(type(tripidx_string))       #debug
        #print("-------------")
        
        tripidx_extract =[str(s) for s in re.findall(r'data-tripidx="(\d+)', tripidx_string)]
        # debug code follows
        # print("\n-------------")
        # print ("\ntripidx =",tripidx)
        # print ("\ttripidx type:",(type(tripidx))) #debug
        # print("-------------")
            
        tripidx.extend(tripidx_extract)
                
    tripidx.sort()    
    debug_val_type(tripidx)  # debug code:  target_url
    tripid_range = len(tripidx) + 1  #use later for range where end=n+1
    print ("\t count =",len(tripidx)) 
        
    with open('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/tripidx.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows([tripidx])  #https://stackoverflow.com/questions/15129567/csv-writer-writing-each-character-of-word-in-separate-column-cell
            
    csvFile.close()
            

# 4. Scrape ramblr.com to obtain trail journal data
# ----------------------------------------------------------------------

if os.path.isfile('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/heysen_data.csv'):  
    console_msg('Importing heysen_data.csv into tripidx[] list')
    
    with open('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/heysen_data.csv', 'r') as f:
        reader = csv.reader(f)
        tripidx = list(reader)
        
    debug_val_type(tripidx)
    
else:
    
    console_msg('heysen_data.csv file does not exist. \n\tWill scrape ramblr.com for data')

    # ------------------------------------------------------------------
    # Create list of URLs to scrape in format of 
    #   webpage/web/mymap/trip/user_id/trip_id
    #   target_url = "https://www.ramblr.com/web/mymap/trip/478170/tripidx/"
    
    URL_prefix = "https://www.ramblr.com/web/mymap/trip/478170/"
    
    URLs = []  #must first create empty list to append to within for loop
    
    
    #list comprehension to convert tripidx list to list of strings
    # for reference, same as following 3 lines below
    # ids = []
    # for tripid in tripidx[0]:
        # ids.append(str(tripid))    
    
    ids = [str(tripid) for tripid in tripidx[0]]  #list comprehension
    
    debug_val_type(ids)
    print ("\t count =",len(ids)) 

    for id in ids:
        URL = (URL_prefix + id)
        URLs.append(URL)
        debug_val_type(URL)  # debug code:  target URLs



    # ------------------------------------------------------------------
    # Capture web page info for each URL
    
    

    
    # for URL in URLs:
        # target_url = URL


