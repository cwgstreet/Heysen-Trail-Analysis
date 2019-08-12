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

# import standard libraries
import csv          # i/o of csv files
import datetime     # manage date time formats
import itertools    # use chain tool used to flatten list of list
import os           # access files on drive
import re           # regular expressions to extract strings
import time         # time to allow sleep pause for JS to catch up

# import HT-analysis modules
import config           # global variables
import debug            # debug functions - variable values/types/counts
import extract_tripidx  # extrap or load trip id's
import extract_page     # extract dynamic JS generated (inner) HTML
import file_io          # write / read csv files to local disk


#import third party libary specific imports
import bs4      # beautiful soup 4 library to parse website
import lxml     # lxml to parse website
import requests # requests to get http

# import specific third party libaries
from selenium import webdriver


def get_data(debug_flag, FILEPATH, DATA_FILENAME = "heysen_data.csv"):
    """Extract gstreet trip data from rambl.com html """
    

    # Avoid unecessary web scraping if HT_data list exists as csv file    
    if os.path.isfile(FILEPATH + DATA_FILENAME):  
        debug.console_msg('\t heysen_data.csv file exists! \n\tImporting heysen_data.csv into HT_data[] list')
        
        config.HT_data = file_io.csv_read(FILEPATH, DATA_FILENAME)
        debug.debug_val_type(config.HT_data, debug_flag)
        
    else:
        
        debug.console_msg('heysen_data.csv file does not exist \n\t  Will scrape ramblr.com for data')
    
        # get trip ids
        extract_tripidx.get_tripidx(debug_flag, FILEPATH, TRIPID_FILENAME) 
        # Create list of URLs to scrape in format of webpage/web/mymap/trip/user_id/trip_id
        #   target_url = "https://www.ramblr.com/web/mymap/trip/478170/tripidx/"
        
        URL_prefix = "https://www.ramblr.com/web/mymap/trip/478170/"
        
        URLs = []  #must first create empty list to append to within for loop
        
        # list comprehension to convert tripidx list to list of strings
        # for reference, same as following 3 lines below
        # ids = []
        # for tripid in tripidx[0]:
        #     ids.append(str(tripid))    
        ids = [str(tripid) for tripid in config.tripidx]  #list comprehension
        
        debug.debug_val_type(ids, debug_flag)
        debug.debug_count(ids, debug_flag)
    
        #initialise empty lists to append extracted data into later
        heysen_row = []   
        id_list = []
        tit_list = []
        day_list = []
        date_list = []
        start_list = []
        stop_list = []
        council_list = []
        tot_dur_list = []
        act_dur_list = []
        pause_dur_list = []
        dist_list = []
        speed_list = []
        height_list = []
        ascent_list = []
        dif_list = []
        
        # create list of URLs to extract data from
        for id in ids:
            URL = (URL_prefix + id)
            URLs.append(URL)
            debug.debug_val_type(URL, debug_flag)  # debug code:  target URLs
    
        # Capture web page info for each URL
        for index, URL in enumerate(URLs):
            target_url = URL  #work through full list of URLs
            #target_url =  "https://www.ramblr.com/web/mymap/trip/478170/1576327" #debug test case - contains log data
            #target_url = "https://www.ramblr.com/web/mymap/trip/478170/1443174"   #debug test case - no log data

            debug.console_msg('extracted data follows:')                        
            debug.debug_val_type(target_url, debug_flag)  # debug code:  target URLs
        
            # get JS generated dynamic HTML page
            extract_page.get_dynamic_HTML(debug_flag, target_url)
            
            # Parse JS_dynamic_HTML string, and store it as Beautiful Soup object
            soup_JS_dynamic = bs4.BeautifulSoup(config.JS_dynamic_HTML, "lxml")
            
            # if required for debugging, use beautiful soup function prettify to display parsed html page
            #print (soup_JS_dynamic.prettify()) # comment out as not needed once captured to text file

            # Extract data from Trail Journal web page
            #---------------------------------------------------------------------
            # Variables of interest:
            # tripid, day, date, start_location, end_location, council, distance, total_duration,
            #   active_duration, paused_duration, avg_speed, highest_point, total_ascent,
            #   difficulty, rest day?, tent, hut, bed
            #---------------------------------------------------------------------
            
            #------- extract title string ---------
            Title = soup_JS_dynamic.h1
            Title = str(Title)  #must be string for next operation
            Title = Title.replace("&amp;", "&")  #fix string as special character "&" isn't rendered (escaped)
            title = Title[Title.find("h1>")+3:Title.find("</h1>")]
            title = str(title)
            debug.debug_val_type(title, debug_flag)
            title = [title]
            if not title:        #check for empty list; add null (None) placeholder if empty
                title = [None]
            debug.debug_val_type(title, debug_flag)
            
            #------- Day (day)---------
            day = [int(s) for s in re.findall(r'\b\d+\b', Title)]
            if not day:        #check for empty list; add null (None) placeholder if empty
                day = [None]
            debug.debug_val_type(day, debug_flag)
              
            #------- Start Location (start_location) ---------
            keyword = " - "
            after_keyword = Title.partition(keyword)
            keyword2 = ' to '           # split walk title into tuple at keyword
            start_stop = after_keyword[2].partition(keyword2)
            start = start_stop[0]     #assigns start location to first tuple element 
            start = [start]
            if not start:        #check for empty list; add null (None) placeholder if empty
                start = [None]
            debug.debug_val_type(start, debug_flag)
            
            #------- Stop Location (stop_location) ---------
            keyword3 = '<'  #change split keyword to further seperate third tuple element
            start_stop2 = start_stop[2].partition(keyword3)
            stop = start_stop2[0]
            stop = [stop]
            if not stop:        #check for empty list; add null (None) placeholder if empty
                stop = [None]
            debug.debug_val_type(stop, debug_flag)
            
            #------- Title (title) ---------
            # title=Title[Title.find("h1>")+3:Title.find("</h1>")]
            # title = [title]
            # debug.debug_val_type(title, debug_flag)
            
            #-------Council (council)) ---------
            location = soup_JS_dynamic.find('div', class_ ="content_addr")
            location = str(location)     # convests location into string
            council = location[location.find(">")+1:location.find(",")]
            council = [council]
            if not council:        #check for empty list; add null (None) placeholder if empty
                council = [None]
            debug.debug_val_type(council, debug_flag)

            #-------Recording Date (date) ---------
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
            except ValueError:
                # unknown format
                recording_date_time_obj = None
                print("cannot parse recording date - unhknown format")
            
            date = recording_date_time_obj
            debug.debug_datetime(date, debug_flag)
            date = [date]
            if not date:        #check for empty list; add null (None) placeholder if empty
                date = [None]
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
            #difficulty = [difficulty]
            if not difficulty:        #check for empty list; add null (None) placeholder if empty
                difficulty = [None]
            debug.debug_val_type(difficulty, debug_flag)

            #-------Total Duration (total_duration) ---------
            try:
                total_duration = durations[0] 
                total_duration_time_obj = datetime.datetime.strptime(total_duration, '%Hh %Mm %Ss')   
                total_duration = total_duration_time_obj   
                debug.debug_time(total_duration, debug_flag)
                total_duration = [total_duration]
                if not total_duration:        #check for empty list; add null (None) placeholder if empty
                    total_duration = [None]
                debug.debug_val_type(total_duration, debug_flag)  
            except:    # trap any error 
                total_duration = [None] 
                debug.debug_val_type(total_duration, debug_flag)  

            #-------Active Duration (active_duration) ---------
            try:
                active_duration = durations[1]
                active_duration_time_obj = datetime.datetime.strptime(active_duration, '%Hh %Mm %Ss')   
                active_duration = active_duration_time_obj
                debug.debug_time(active_duration, debug_flag)
                active_duration = [active_duration]
                if not tactive_duration:        #check for empty list; add null (None) placeholder if empty
                    active_duration = [None]
                debug.debug_val_type(active_duration, debug_flag)
            except:    # trap any error 
                active_duration = [None] 
                debug.debug_val_type(active_duration, debug_flag)  

            #-------Paused Duration (paused_duration) ---------
            try:
                paused_duration = durations[2]
                paused_duration_time_obj = datetime.datetime.strptime(paused_duration, '%Hh %Mm %Ss')   
                paused_duration = paused_duration_time_obj
                debug.debug_time(paused_duration, debug_flag)
                paused_duration = [paused_duration]
                if not paused_duration:        #check for empty list; add null (None) placeholder if empty
                    paused_duration = [None]
                debug.debug_val_type(paused_duration, debug_flag)
            except:    # trap any error 
                paused_duration = [None] 
                debug.debug_val_type(paused_duration, debug_flag)  
   
            #------- Distance (distance) ---------
            distance = soup_JS_dynamic.find('div', class_ ="content_distance")
            distance = str(distance)   # convests distance into string
            distance = [float(s) for s in re.findall(r'\d+\.\d+', distance)]
            if not distance:        #check for empty list; add null (None) placeholder if empty
                distance = [None]
            debug.debug_val_type(distance, debug_flag)
            
            #------- Total Ascent (total_ascent)---------
            total_ascent = soup_JS_dynamic.find('div', class_ ="content_total_ascent")
            total_ascent = str(total_ascent)   # convests total_ascent into string
            total_ascent = [int(s) for s in re.findall(r'\b\d+\b', total_ascent)]
            if not total_ascent:        #check for empty list; add null (None) placeholder if empty
                total_ascent = [None]
            debug.debug_val_type(total_ascent, debug_flag)
            
            #------- Highest Point (highest_point)---------
            highest_point = soup_JS_dynamic.find('div', class_ ="content_highest_point")
            highest_point = str(highest_point)   # convests highest_point into string
            highest_point = [int(s) for s in re.findall(r'\b\d+\b', highest_point)]
            if not highest_point:        #check for empty list; add null (None) placeholder if empty
                highest_point = [None]
            debug.debug_val_type(highest_point, debug_flag)
            
            #------- Average Speed (avg_spped)---------
            avg_speed = soup_JS_dynamic.find('div', class_ ="content_avg_speed")
            avg_speed = str(avg_speed)   # convests avg_speed into string
            avg_speed = [float(s) for s in re.findall(r'\d+\.\d+', avg_speed)]
            if not avg_speed:        #check for empty list; add null (None) placeholder if empty
                avg_speed = [None]
            debug.debug_val_type(avg_speed, debug_flag)
            
            tempidlist = []
            tempidlist.append(config.tripidx[index])
           
            # now add data into list
            id_list.append(tempidlist)           
            tit_list.append(title)
            day_list.append(day) 
            date_list.append(date)
            start_list.append(start) 
            stop_list.append(stop)
            council_list.append(council)
            tot_dur_list.append(total_duration)
            act_dur_list.append(active_duration)
            pause_dur_list.append(paused_duration)
            dist_list.append(distance)
            speed_list.append(avg_speed)
            height_list.append(highest_point) 
            ascent_list.append(total_ascent)
            dif_list.append(difficulty)

        # flatten lists (list of lists into flat list)
        #   ref: https://coderwall.com/p/rcmaea/flatten-a-list-of-lists-in-one-line-in-python
        id_list  = list(itertools.chain(*id_list))  
        tit_list  = list(itertools.chain(*tit_list))  
        day_list  = list(itertools.chain(*day_list))  
        date_list  = list(itertools.chain(*date_list))  
        start_list  = list(itertools.chain(*start_list))  
        stop_list  = list(itertools.chain(*stop_list))  
        council_list  = list(itertools.chain(*council_list))  
        tot_dur_list  = list(itertools.chain(*tot_dur_list))  
        act_dur_list  = list(itertools.chain(*act_dur_list))  
        pause_dur_list  = list(itertools.chain(*pause_dur_list))  
        dist_list  = list(itertools.chain(*dist_list))  
        speed_list  = list(itertools.chain(*speed_list))  
        height_list  = list(itertools.chain(*height_list))  
        ascent_list  = list(itertools.chain(*ascent_list))  
        dif_list  = list(itertools.chain(*dif_list))  

        debug.debug_val_type(id_list, debug_flag)
        debug.debug_val_type(tit_list, debug_flag)
        debug.debug_val_type(speed_list, debug_flag)

        HT_zipdata = list(zip(id_list, tit_list, day_list, date_list, 
                                start_list, stop_list, council_list, 
                                tot_dur_list, act_dur_list, 
                                pause_dur_list, dist_list, speed_list, 
                                height_list, ascent_list, dif_list) )
        
        debug.debug_val_type(HT_zipdata, debug_flag)
        
        print("\n\n")  #two blank lines
        
        # debugging:  print rows of HT_zipdate
        for index, value in enumerate(HT_zipdata):
            print(f'{index}: {value}')

        #file_io.csv_write(FILEPATH, DATA_FILENAME, heysen_row)  #testing when single target_URL iteration
        file_io.csv_write(FILEPATH, DATA_FILENAME, HT_zipdata)
        
        config.HT_data = HT_zipdata  # write to global so data can pass between modules
        
        

        
if __name__ == "__main__":
  
    # Set debugging status: on=True or off=False
    debug_flag = True
    debug.debug_status(debug_flag)

    FILEPATH = "/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/"
    TRIPID_FILENAME = "tripidx.csv"
    DATA_FILENAME = "heysen_data.csv"

    get_data(debug_flag, FILEPATH, DATA_FILENAME)            


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





