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
import os           # access files on drive
import re           # regular expressions to extract strings

# import HT-analysis modules
import config       # global variables
import debug        # debug functions - variable values / types / counts
import extract_page # extract dynamic JS generated (inner) HTML
import file_io      # write / read csv files to local disk

#import third party libary specific imports
import bs4      # beautiful soup 4 library to parse website
import lxml     # lxml to parse website

# import specific third party libaries
#from selenium import webdriver


def get_tripidx(debug_flag, FILEPATH, TRIPID_FILENAME="tripidx.csv"):
    """Extract gstreet trip ids (tripidx) from rambl.com html """
          
    # Avoid unecessary web scraping if tripidx list exists as csv file    
    if os.path.isfile(FILEPATH + TRIPID_FILENAME):  #confirms file exists
        debug.console_msg('\ttripidx.csv file exists! \n\tImporting tripidx.csv into tripidx[] list')
        
        config.tripidx = file_io.csv_read(FILEPATH, TRIPID_FILENAME)
            
        debug.val_type(config.tripidx, debug_flag)  # debug code:  page numbers
        debug.list_count(config.tripidx, debug_flag)

    else:
        debug.console_msg('tripidx.csv file does not exist! \n\tWill scrape ramblr.com for data')
        
        page_numbers = [str(x) for x in range(1,5)]  #list comprehension; create list of strings
        debug.val_type(page_numbers, debug_flag)  # debug code:  page numbers
    
        URL_prefix = "https://www.ramblr.com/web/mymap/trip/478170#h=1&u_uid=478170&type=1&unit=1&page="
        URL_suffix = "&stext=&active=0&sort=10&receivegid="
        
        URLs = []  #must first create empty list to append to within for loop
        
        for page in page_numbers:
            URL = (URL_prefix + page + URL_suffix)
            URLs.append(URL)
            debug.val_type(URL, debug_flag)  # debug code:  page numbers
            
        # Capture tripidx data from target web pages and load into a list
        for URL in URLs:
        
            # specify the target url URL in format of 
            #   webpage/web/mymap/trip/user_id/trip_id
            target_url = URL
            
            # Example URL for testing:
            #target_url = "https://www.ramblr.com/web/mymap/trip/478170#h=1&u_uid=478170&type=1&unit=1&page=1&stext=&active=0&sort=10&receivegid="
    
            # get JS generated dynamic HTML page
            extract_page.get_dynamic_HTML(debug_flag, target_url)
            
            # Extract tripidx values from Trail Journal web page
            
            soup_dynamic = bs4.BeautifulSoup(config.JS_dynamic_HTML, "lxml")
            tripidx_string = str(soup_dynamic.find_all('div', class_ = "lists pr nomysession") )	# note: class_ uses trailing "_" to avoid conflict

            tripidx_extract =[str(s) for s in re.findall(r'data-tripidx="(\d+)', tripidx_string)]
                
            config.tripidx.extend(tripidx_extract)
                    
        config.tripidx.sort()    
        debug.val_type(config.tripidx, debug_flag)  # debug code:  target_url
        debug.list_count(config.tripidx, debug_flag)
                    
        # write and save scraped tripidx data to csv file        
        file_io.csv_write(FILEPATH, TRIPID_FILENAME, config.tripidx)


if __name__ == "__main__":
    
    # Set debugging status: on=True or off=False
    debug_flag = True
    debug.status_msg(debug_flag)

    FILEPATH = "/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/"
    TRIPID_FILENAME = "tripidx.csv"

    get_tripidx(debug_flag, FILEPATH, TRIPID_FILENAME)            
    
