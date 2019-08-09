#!/usr/bin/env python3
# -*- coding: utf-8 -*-
  
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Module name: extract_page.py
# Purpose:     use ChromeDriver to extract dynamic JS-generated 
#                 (inner) HTML
# 
# Notes:
#
# Copyright:   2019, release under GPL3. See LICENSE file for details
#              Carl W Greenstreet <cwgstreet@gmail.com>
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# 1. Import standard libraries

# import libraries
import pprint as pp # pretty print or improved print formation
import time         # time to allow sleep pause for JS to catch up

# import HT-analysis modules
import config           #global variables
import debug            #debug functions - variable values / types / counts

# import third party libary specific imports
import bs4      # beautiful soup 4 library to parse website
import lxml     # lxml to parse website

# import specific third party libaries
from selenium import webdriver


def get_dynamic_HTML(debug_flag, target_url):
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
    dynamic_page = browser.page_source  #https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
    config.JS_dynamic_HTML = bs4.BeautifulSoup(dynamic_page, "lxml")
    
    # close browser - choose appropriate:
    browser.close()  # doesn’t always stop the web driver that’s running in background
    #browser.quit()  # warning: kills all instances of Chrome and Chromedriver

    
if __name__ == "__main__":
    
    # Set debugging status: on=True or off=False
    debug_flag = True
    debug.debug_status(debug_flag)

    # set test page
    target_url = "https://www.ramblr.com/web/mymap/trip/478170/1510167/"

    get_dynamic_HTML(debug_flag, target_url) 
    
    # use beautiful soup function prettify to display page
    #pp.pprint(config.JS_dynamic_HTML)  # comment out if not needed 
    print (config.JS_dynamic_HTML.prettify()) # comment out as not needed once catured to text file
     

