#!/usr/bin/env python3
# -*- coding: utf-8 -*-
  
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Module name: extract_tripidx.py
# Purpose:     Extract gstreet trip ids (tripidx) from rambl.com html
# 
# Notes:
#
# Copyright:   2019, release under GPL3. See LICENSE file for details
#              Carl W Greenstreet <cwgstreet@gmail.com>
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# 1. Import standard libraries

#import libraries
import csv          # i/o of csv files
import datetime     # manage date time formats
import os           # access files on drive
import re           # regular expressions to extract strings
import time         # time to allow sleep pause for JS to catch up

# import HT-analysis modules
import config       #global variables
import debug        #debug functions - variable values / types / counts

#import third party libary specific imports
import bs4          # beautiful soup 4 library to parse website
import lxml         # lxml to parse website
import requests     # requests to get http

# import specific third party libaries
from selenium import webdriver


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
    
    # close browser - choose appropriate:
    browser.close()  # doesn’t always stop the web driver that’s running in background
    #browser.quit()  # warning: kills all instances of Chrome and Chromedriver

def get_tripidx(debug_flag):
    """Extract gstreet trip ids (tripidx) from rambl.com html """
   
    # Avoid unecessary web scraping if tripidx list exists as csv file    
    if os.path.isfile('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/tripidx.csv'):  
        debug.console_msg('Importing tripidx.csv into tripidx[] list')
        
        with open('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/tripidx.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            config.tripidx = list(reader)
            
        debug.debug_val_type(config.tripidx, debug_flag)  # debug code:  page numbers
        debug.debug_count(config.tripidx, debug_flag)

        print(config.tripidx[0][1])
        #print ("\t count =", len(tripidx))
        debug.debug_count(config.tripidx, debug_flag)

 
    else:
        
        debug.console_msg('tripidx.csv file does not exist. \n\tWill scrape ramblr.com for data')
        
        page_numbers = [str(x) for x in range(1,5)]  #list comprehension; create list of strings
        debug.debug_val_type(page_numbers, debug_flag)  # debug code:  page numbers
    
        URL_prefix = "https://www.ramblr.com/web/mymap/trip/478170#h=1&u_uid=478170&type=1&unit=1&page="
        URL_suffix = "&stext=&active=0&sort=10&receivegid="
        
        URLs = []  #must first create empty list to append to within for loop
        
        for page in page_numbers:
            URL = (URL_prefix + page + URL_suffix)
            URLs.append(URL)
            debug.debug_val_type(URL, debug_flag)  # debug code:  page numbers
            
        # Capture tripidx data from target web pages and load into a list
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
            
            tripidx_extract =[str(s) for s in re.findall(r'data-tripidx="(\d+)', tripidx_string)]
                
            config.tripidx.extend(tripidx_extract)
                    
        config.tripidx.sort()    
        debug.debug_val_type(tripidx, debug_flag)  # debug code:  target_url
        debug.debug_count(tripidx, debug_flag)
                    
        # write and save scraped tripidx data to csv file
        with open('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/tripidx.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows([config.tripidx])  #https://stackoverflow.com/questions/15129567/csv-writer-writing-each-character-of-word-in-separate-column-cell
                
        csvFile.close()


if __name__ == "__main__":
    
    # Set debugging status: on=True or off=False
    debug_flag = True
    debug.debug_status(debug_flag)

    get_tripidx(debug_flag)            
    
