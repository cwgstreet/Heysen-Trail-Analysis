#!/usr/bin/env python3
# -*- coding: utf-8 -*-

  
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Module name: extract_data.py
# Purpose:     Extract Heysen Trail trip data from rambl.com html
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
import config           #global variables
import debug            #debug functions - variable values / types / counts
import extract_tripidx  #extrap or load trip id's

#import third party libary specific imports
import bs4      # beautiful soup 4 library to parse website
import lxml     # lxml to parse website
import requests # requests to get http

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
    
    # close browser - choose appropriate
    browser.close()  # doesn’t always stop the web driver that’s running in background
    #browser.quit()  # warning: kills all instances of Chrome and Chromedriver


def get_data(debug_flag):
    """Extract gstreet trip data from rambl.com html """
    
    # Avoid unecessary web scraping if trail_data list exists as csv file    
    
    if os.path.isfile('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/heysen_data.csv'):  
        debug.debug.console_msg('Importing heysen_data.csv into HT_data[] list')
        
        with open('/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/heysen_data.csv', 'r') as f:
            reader = csv.reader(f)
            config.tripidx = list(reader)
            
        debug.debug_val_type(HT_data, debug_flag)
        
    else:
        
        debug.console_msg('heysen_data.csv file does not exist. \n\tWill scrape ramblr.com for data')
    
        # Create list of URLs to scrape in format of 
        #   webpage/web/mymap/trip/user_id/trip_id
        #   target_url = "https://www.ramblr.com/web/mymap/trip/478170/tripidx/"
        
        URL_prefix = "https://www.ramblr.com/web/mymap/trip/478170/"
        
        URLs = []  #must first create empty list to append to within for loop
        
        # list comprehension to convert tripidx list to list of strings
        # for reference, same as following 3 lines below
        # ids = []
        # for tripid in tripidx[0]:
            # ids.append(str(tripid))    
        ids = [str(tripid) for tripid in config.tripidx[0]]  #list comprehension
        
        debug.debug_val_type(ids, debug_flag)
        print ("\t count =",len(ids)) 
    
        for id in ids:
            URL = (URL_prefix + id)
            URLs.append(URL)
            debug.debug_val_type(URL, debug_flag)  # debug code:  target URLs
    
        # ------------------------------------------------------------------
        # Capture web page info for each URL
        
        for URL in URLs:
            #target_url = URL
            target_url = "https://www.ramblr.com/web/mymap/trip/478170/1576327 #debug test case"
            debug.debug_val_type(target_url, debug_flag)  # debug code:  target URLs
    
            # get JS generated dynamic HTML page
            JS_dynamic_HTML = get_dynamic_HTML(target_url)
            
            # Parse  JS_dynamic_HTML  variable, and store it in Beautiful Soup format
            soup_JS_dynamic = bs4.BeautifulSoup(JS_dynamic_HTML, "lxml")
            
            # use beautiful soup function prettify to display page
            #print (soup_JS_dynamic.prettify()) # comment out as not needed once captured to text file
            
            Title = soup_JS_dynamic.h1
            Title = str(Title)
            title=Title[Title.find("h1>")+3:Title.find("</h1>")]
            print ("\nTitle =",title)
            print ("\tTitle type:",(type(title))) #debug
    
                
            
            #########################################################
            ###   FIX Code Below
            ####|||||||||||||||||||||||||||||||||||||||||||||||||||||||||
            
            
            
            # #specify the target url  URL in format of webpage/web/mymap/trip/user_id/trip_id
            # target_url = "https://www.ramblr.com/web/mymap/trip/478170/1510167/"
            
            # #Query the website and return the html to the variable 'page'
            # page = requests.get(target_url)
            
            # # 2b. Capture inner html dynamically generated by Java Script
            # options = webdriver.ChromeOptions()
            # options.headless = True
            
            # browser_path = r"/Applications/chromedriver"
            # browser = webdriver.Chrome(executable_path=browser_path,
                                    # options=options) 
            
            # browser.get(target_url) #navigate to the page
            
            # innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
            
            # # Parse  innerHTML  variable, and store it in Beautiful Soup format
            # soup_inner = bs4.BeautifulSoup(innerHTML, "lxml")
            # soup = bs4.BeautifulSoup(page.text, features = "lxml")
            # #print("soup type:", type(soup))
            # #print("soup_innerHTML type:", type(soup_inner))
            
            # #use beautiful soup function prettify to display page
            # #  Output to file did not work:   print (soup.prettify(), file=open("output.txt", "a"))
            # #print (soup.prettify()) # comment out as not needed once catured to text file
            # #print (soup_inner.prettify()) # comment out as not needed once catured to text file
            
            
            # 3. Extract data from Trail Journal web page
            
            #---------------------------------------------------------------------
            # Variables of interest:
            # Day, Date, Start location, End Location, Council, distnce, total duration,
            #   active duration, paused duration, avg speed, highest point, total ascent,
            #   difficulty, rest day?, tent, hut, bed
            
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')  #make it easier to find start of output
            
            
            #------- Day (Day)---------
            Day=[int(s) for s in re.findall(r'\b\d+\b', Title)]
            print('Day=',Day)    #debug test, returns Day= [6]
            print ("\tDay type:",(type(Day)))
            
            #------- Start Location (Start_location) ---------
            keyword = " - "
            after_keyword = Title.partition(keyword)
            keyword2 = ' to '           # split walk title into tuple at keyword
            start_stop = after_keyword[2].partition(keyword2)
            Start_location=start_stop[0]     #assigns start location to first tuple element 
            debug.debug_val_type(Start_location, debug_flag)
            
            #------- Stop Location (Stop_location) ---------
            keyword3 = '<'  #change split keyword to further seperate third tuple element
            start_stop2 = start_stop[2].partition(keyword3)
            Stop_location=start_stop2[0]
            debug.debug_val_type(Stop_location, debug_flag)
            
            #------- Title (title) ---------
            # title=Title[Title.find("h1>")+3:Title.find("</h1>")]
            # debug.debug_val_type(title, debug_flag)
            
            #-------Council (council)) ---------
            location = soup_JS_dynamic.find('div', class_ ="content_addr")
            location = str(location)     # convests location into string
            council=location[location.find(">")+1:location.find(",")]
            debug.debug_val_type(council, debug_flag)
            
            #-------Recording Date (date) ---------
            recording_date = soup_JS_dynamic.find('div', class_ ="content_recoding_time")
            recording_date = str(recording_date)     # timedate function requires string
            date_timestamp=recording_date[recording_date.find(":")+2:recording_date.find(" <")-5]
            recording_date_time_obj = datetime.datetime.strptime(date_timestamp, '%b %d, %Y %I:%M %p')
            debug.debug_datetime(recording_date_time_obj, debug_flag)
            
            
            #print('\n############################################################')  #make it easier to find this section in terminal output
            
            #------- Extract all Durations (durations) ---------
            durations = soup_JS_dynamic.find_all('li', class_ ="aft")
            durations = str(durations)
            durations = re.findall("\d+[h]\s\d+[m]\s\d+[s]", durations) 
            debug.debug_val_type(durations, debug_flag)
            
            #-------Total Duration (total_duration) ---------
            total_duration=durations[0]            
            total_duration_time_obj = datetime.datetime.strptime(total_duration, '%Hh %Mm %Ss')   
            total_duration = total_duration_time_obj   
            debug.debug_time(total_duration, debug_flag)
            
            #-------Active Duration (paused_duration) ---------
            active_duration=durations[1]
            print("\nActive Duration =",active_duration)  #debug
            print ("\tActive Duration type:",(type(active_duration)))
            
            active_duration_time_obj = datetime.datetime.strptime(active_duration, '%Hh %Mm %Ss')   
            print('Active Time:', active_duration_time_obj.time())   #debug
            
            #-------Paused Duration (paused_duration) ---------
            paused_duration=durations[2]
            print("\nPaused Duration =",paused_duration)  #debug
            print ("\tPaused Duration type:",(type(paused_duration)))
            
            paused_duration_time_obj = datetime.datetime.strptime(paused_duration, '%Hh %Mm %Ss')   
            print('Paused Time:', paused_duration_time_obj.time())   #debug
            
            #print('############################################################')  #make it easier to find this section in terminal output
            
            #------- Distance (distance) ---------
            distance = soup_JS_dynamic.find('div', class_ ="content_distance")
            #print(type(distance))        #debug
            #print("distance=",distance)  #debug
            distance = str(distance)   # convests distance into string
            #print(type(distance))        #debug
            distance=[float(s) for s in re.findall(r'\d+\.\d+', distance)]
            print('\nDistance =',distance)    #debug test, returns Distance = [30.8]
            print ("\tDistance type:",(type(distance)))
            
            #------- Total Ascent (total_ascent)---------
            total_ascent = soup_JS_dynamic.find('div', class_ ="content_total_ascent")
            #print(type(total_ascent))
            #print("Total Ascent=",total_ascent)  #debug
            total_ascent = str(total_ascent)   # convests total_ascent into string
            #print(type(total_ascent))        #debug
            total_ascent=[int(s) for s in re.findall(r'\b\d+\b', total_ascent)]
            print('\nTotal Ascent =',total_ascent)    #debug test, returns Total Ascent = [525]
            print ("\tTotal Ascent type:",(type(total_ascent)))
            
            #------- Highest Point (highest_point)---------
            highest_point = soup_JS_dynamic.find('div', class_ ="content_highest_point")
            #print(type(highest_point))
            #print("Highest Point =",highest_point)  #debug
            highest_point = str(highest_point)   # convests highest_point into string
            #print(type(highest_point))        #debug
            highest_point=[int(s) for s in re.findall(r'\b\d+\b', highest_point)]
            print('\nHighest Point =',highest_point)    #debug test, returns Highest Point = [389]
            print ("\tHighest Point type:",(type(highest_point)))
            
            #------- Average Speed (avg_spped)---------
            avg_speed = soup_JS_dynamic.find('div', class_ ="content_avg_speed")
            #print(type(avg_speed))
            #print("Average Speed =",avg_speed)  #debug
            avg_speed = str(avg_speed)   # convests avg_speed into string
            #print(type(avg_speed))        #debug
            avg_speed=[float(s) for s in re.findall(r'\d+\.\d+', avg_speed)]
            print('\nAverage Speed =',avg_speed)    #debug test, returns Average Speed = [30.8]
            print ("\tAverage Speed type:",(type(avg_speed)))
            
            break  #temporary - only perform one pass of for loop

        
if __name__ == "__main__":
  
    # Set debugging status: on=True or off=False
    debug_flag = True
    debug.debug_status(debug_flag)

    extract_tripidx.get_tripidx(debug_flag)            

    get_data(debug_flag)            




#print('############################################################')  #make it easier to find this section in terminal output






