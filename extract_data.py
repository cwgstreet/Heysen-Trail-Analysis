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
    #browser.quit()  # warning: kills all instances of Chrome and Chromedriver
    browser.close()  # doesn’t always stop the web driver that’s running in background


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
    
        heysen_row = []   #need empty list to append Heysen data
        
        for id in ids:
            URL = (URL_prefix + id)
            URLs.append(URL)
            debug.debug_val_type(URL, debug_flag)  # debug code:  target URLs
    
        # ------------------------------------------------------------------
        # Capture web page info for each URL
        
        
        
        for URL in URLs:
            #target_url = URL
            # target_url = "https://www.ramblr.com/web/mymap/trip/478170/1576327" #debug test case
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')  #make it easier to find start of output
            target_url = "https://www.ramblr.com/web/mymap/trip/478170/1443174"   #debug test case - no log data
            debug.debug_val_type(target_url, debug_flag)  # debug code:  target URLs
    
            # get JS generated dynamic HTML page
            JS_dynamic_HTML = get_dynamic_HTML(target_url)
            
            # Parse  JS_dynamic_HTML  variable, and store it in Beautiful Soup format
            soup_JS_dynamic = bs4.BeautifulSoup(JS_dynamic_HTML, "lxml")
            
            # use beautiful soup function prettify to display page
            #print (soup_JS_dynamic.prettify()) # comment out as not needed once captured to text file
            
            
            # 3. Extract data from Trail Journal web page
            
            #---------------------------------------------------------------------
            # Variables of interest:
            # Day, Date, Start location, End Location, Council, distnce, total duration,
            #   active duration, paused duration, avg speed, highest point, total ascent,
            #   difficulty, rest day?, tent, hut, bed
            #---------------------------------------------------------------------
            
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')  #make it easier to find start of output
            
            #------- extract title string ---------
            Title = soup_JS_dynamic.h1
            Title = str(Title)
            title = Title[Title.find("h1>")+3:Title.find("</h1>")]
            debug.debug_val_type(title, debug_flag)
            
            #------- Day (day)---------
            day = [int(s) for s in re.findall(r'\b\d+\b', Title)]
            debug.debug_val_type(day, debug_flag)
              
            #------- Start Location (start_location) ---------
            keyword = " - "
            after_keyword = Title.partition(keyword)
            keyword2 = ' to '           # split walk title into tuple at keyword
            start_stop = after_keyword[2].partition(keyword2)
            start = start_stop[0]     #assigns start location to first tuple element 
            start = [start]
            debug.debug_val_type(start, debug_flag)
            
            #------- Stop Location (stop_location) ---------
            keyword3 = '<'  #change split keyword to further seperate third tuple element
            start_stop2 = start_stop[2].partition(keyword3)
            stop = start_stop2[0]
            stop = [stop]
            debug.debug_val_type(stop, debug_flag)
            
            #------- Title (title) ---------
            title=Title[Title.find("h1>")+3:Title.find("</h1>")]
            title = [title]
            debug.debug_val_type(title, debug_flag)
            
            #-------Council (council)) ---------
            location = soup_JS_dynamic.find('div', class_ ="content_addr")
            location = str(location)     # convests location into string
            council = location[location.find(">")+1:location.find(",")]
            council = [council]
            debug.debug_val_type(council, debug_flag)

            #-------Recording Date (date) ---------
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')  #make it easier to find start of output
            recording_date = soup_JS_dynamic.find('div', class_ ="content_recoding_time")
            recording_date = str(recording_date)     # timedate function requires string
            recording_date = recording_date.strip()   # importnt to strio leading / trailing whitespace to avoid strptime format problems

            date_timestamp = recording_date[recording_date.find(":")+2:recording_date.find(" <")-5]
            debug.debug_val_type(date_timestamp, debug_flag)

            try:
                # normal strptime format below
                recording_date_time_obj = datetime.datetime.strptime(date_timestamp, '%b %d, %Y %I:%M %p')
            except ValueError:
                # try alternative strptime format to match time data 'Apr 7, 2019'
                recording_date_time_obj = datetime.datetime.strptime(date_timestamp, '%b %d, %Y')  
                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')  #make it easier to find start of output
            except ValueError:
                # unknown format
                recording_date_time_obj = None
                print("cannot parse recording date - unhknown format")
                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')  #make it easier to find start of output
            
            
            
            date = recording_date_time_obj
            debug.debug_datetime(date, debug_flag)
            date = [date]
            debug.debug_val_type(date, debug_flag)

            
            #------- Extract all Durations (durations) ---------
            durations = soup_JS_dynamic.find_all('li', class_ ="aft")
            durations = str(durations)
            durations = re.findall("\d+[h]\s\d+[m]\s\d+[s]", durations) 
            debug.debug_val_type(durations, debug_flag)
            
            #------- Difficulty (difficulty)---------
            difficulty = soup_JS_dynamic.find_all('li', class_ ="aft")
            difficulty = str(difficulty)
            difficulty = re.findall("Easy|Moderate|Hard|Extreme", difficulty) 
            # difficulty = [difficulty]
            debug.debug_val_type(difficulty, debug_flag)

            #-------Total Duration (total_duration) ---------
            total_duration = durations[0]            
            total_duration_time_obj = datetime.datetime.strptime(total_duration, '%Hh %Mm %Ss')   
            total_duration = total_duration_time_obj   
            debug.debug_time(total_duration, debug_flag)
            total_duration = [total_duration]
            debug.debug_val_type(total_duration, debug_flag)
            
            #-------Active Duration (active_duration) ---------
            active_duration = durations[1]
            active_duration_time_obj = datetime.datetime.strptime(active_duration, '%Hh %Mm %Ss')   
            active_duration = active_duration_time_obj
            debug.debug_time(active_duration, debug_flag)
            active_duration = [active_duration]
            debug.debug_val_type(active_duration, debug_flag)

            #-------Paused Duration (paused_duration) ---------
            paused_duration = durations[2]
            paused_duration_time_obj = datetime.datetime.strptime(paused_duration, '%Hh %Mm %Ss')   
            paused_duration = paused_duration_time_obj
            debug.debug_time(paused_duration, debug_flag)
            paused_duration = [paused_duration]
            debug.debug_val_type(paused_duration, debug_flag)
            
            #------- Distance (distance) ---------
            distance = soup_JS_dynamic.find('div', class_ ="content_distance")
            distance = str(distance)   # convests distance into string
            distance = [float(s) for s in re.findall(r'\d+\.\d+', distance)]
            debug.debug_val_type(distance, debug_flag)
            
            #------- Total Ascent (total_ascent)---------
            total_ascent = soup_JS_dynamic.find('div', class_ ="content_total_ascent")
            total_ascent = str(total_ascent)   # convests total_ascent into string
            total_ascent = [int(s) for s in re.findall(r'\b\d+\b', total_ascent)]
            debug.debug_val_type(total_ascent, debug_flag)
            
            #------- Highest Point (highest_point)---------
            highest_point = soup_JS_dynamic.find('div', class_ ="content_highest_point")
            highest_point = str(highest_point)   # convests highest_point into string
            highest_point = [int(s) for s in re.findall(r'\b\d+\b', highest_point)]
            debug.debug_val_type(highest_point, debug_flag)
            
            #------- Average Speed (avg_spped)---------
            avg_speed = soup_JS_dynamic.find('div', class_ ="content_avg_speed")
            avg_speed = str(avg_speed)   # convests avg_speed into string
            avg_speed = [float(s) for s in re.findall(r'\d+\.\d+', avg_speed)]
            debug.debug_val_type(avg_speed, debug_flag)
            
            
            # concatenate trail data into a list (row) in desired order
            heysen_row.append(title)
            heysen_row.append(day) 
            heysen_row.append(date)
            heysen_row.append(start) 
            heysen_row.append(stop)
            heysen_row.append(council)
            heysen_row.append(total_duration)
            heysen_row.append(active_duration)
            heysen_row.append(paused_duration)
            heysen_row.append(distance)
            heysen_row.append(avg_speed)
            heysen_row.append(highest_point) 
            heysen_row.append(total_ascent)
            heysen_row.append(difficulty)
            
            debug.debug_val_type(heysen_row, debug_flag)


            # zippedList = list(zip(title, day, date, start, 
                                    # stop, council, total_duration, 
                                    # active_duration, paused_duration, 
                                    # distance, avg_speed, highest_point, 
                                    # total_ascent, difficulty ))
            
            # debug.debug_val_type(zippedList, debug_flag)
        
            
            break  #temporary - only perform one pass of for loop

        
if __name__ == "__main__":
  
    # Set debugging status: on=True or off=False
    debug_flag = True
    debug.debug_status(debug_flag)

    extract_tripidx.get_tripidx(debug_flag)            

    get_data(debug_flag)            


# print('############################################################')  #make it easier to find this section in terminal output

# # create dataframe from zipped list
# df = pd.DataFrame(zippedList, columns = ['trip_id', 'title', 'day',
                                            # 'date', 'start', 'stop',
                                            # 'council', 'total_duration',
                                            # 'active_duration', 
                                            # 'paused_duration' , 'distance',
                                            # 'avg_speed', 'highest_point', 
                                            # 'total_ascent', 'difficulty'] ) 
                                            
# print("Dataframe : " , df, sep='\n')
# df.to_csv(path_or_buf='test_df.csv', encoding='utf-8')

##################################################################################################################


#print('############################################################')  #make it easier to find this section in terminal output

#print('############################################################')  #make it easier to find this section in terminal output
            
#print('\n############################################################')  #make it easier to find this section in terminal output





