#!/usr/bin/env python3
# -*- coding: utf-8 -*-

  
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Module name: file_io.py
# Purpose:     write / read csv files
# 
# Notes:
#
# Copyright:   2019, release under GPL3. See LICENSE file for details
#              Carl W Greenstreet <cwgstreet@gmail.com>
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# import libraries
import csv          # i/o of csv files
import os           # access files on drive
#import inspect      # to get variable names

# import HT-analysis modules
import config       # global variables
import debug        # debug functions - variable values / types / counts


def csv_read(PATH, NAME):
    """reads a csv file into list called contents"""
    with open(PATH + NAME, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        contents = list(reader)
    flat_list = [item for sublist in contents for item in sublist] #https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
    return flat_list


def csv_write(PATH, NAME, contents):
    """writes list called contents into a csv file"""
    with open(PATH + NAME, 'a') as csvFile:  #note: 'a' means open for writing - append
            writer = csv.writer(csvFile)
            writer.writerows([contents])  # https://stackoverflow.com/questions/15129567/csv-writer-writing-each-character-of-word-in-separate-column-cell
            # writerow vs writerows: https://stackoverflow.com/questions/33091980/difference-between-writerow-and-writerows-methods-of-python-csv-module
    csvFile.close()



# test code follows:          
if __name__ == "__main__":
    
    # Set debugging status: on=True or off=False
    debug_flag = True
    debug.status_msg(debug_flag)
    
    
    # ---------------- Test CSV Read -----------------------------------
    PATH = "/Users/carlwgreenstreet/Documents/Git/Heysen-Trail-Analysis/"
    NAME = "tripidx.csv"
    
    config.tripidx = csv_read(PATH, NAME)
    
    debug.val_type(config.tripidx, debug_flag)  # debug code:  page numbers
    debug.list_count(config.tripidx, debug_flag)
    
    
    # ---------------- Test CSV Write -----------------------------------
    NAME = "delete_test.csv"
    
    csv_write(PATH, NAME, config.tripidx)
    
    
