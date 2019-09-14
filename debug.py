#!/usr/bin/env python3
# -*- coding: utf-8 -*-

  
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Module name: debug.py
# Purpose:     debugging functions
# 
# Notes:
#
# Copyright:   2019, release under GPL3. See LICENSE file for details
#              Carl W Greenstreet <cwgstreet@gmail.com>
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# import libraries
import datetime     # manage date time formats
import inspect      # to get variable names
import re           # regular expressions to extract strings
import time         # time to allow sleep pause for JS to catch up

# import third party libary specific imports
import bs4          # beautiful soup 4 library to parse website
import lxml         # lxml to parse website
import requests     # requests to get http


def debug_status(debug_flag=True):
    """Displays a debugging status message to console"""
    if debug_flag:  #when true
        console_msg('Debugging is ON')
    else:
        console_msg('Debugging is OFF')


def retrieve_name(var):
    """ Gets the name of var. Does it from the out-most frame inner-wards.
    :param var: variable to get name from.
    :return: string """
    #https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string/18425523
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]


def console_msg(msg):
    """Display a message on console window"""
    clear = "\n" * 2
    print(clear)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++\
          \n\t" +msg +"\
          \n+++++++++++++++++++++++++++++++++++++++++++++++++++++++")


def val_type(debug_target, debug_flag):
    """Prints variable name, value and type to console window
        when switch debug_flag = True"""
    if debug_flag:
        var_name = str(debug_target)
        print("\n" + retrieve_name(debug_target) + " = ", debug_target)
        print("\t" + retrieve_name(debug_target) + " type:", type(debug_target))


def list_count(debug_target, debug_flag):
    """Prints element count of list to console window
        when switch debug_flag = True"""
    if debug_flag:
        var_name = str(debug_target)
        print("\n" + retrieve_name(debug_target) + " count: ", len(debug_target))
 
  
def date_value(debug_target, debug_flag):
    """Prints date value to console when switch debug_flag = True"""
    if debug_flag:
        var_name = str(debug_target)
        print('\nDate:', debug_target.date())   


def time_value(debug_target, debug_flag):
    """Prints time value to console when switch debug_flag = True"""
    if debug_flag:
        var_name = str(debug_target)
        print('Time:', debug_target.time())   
   
        
def date_time_value(debug_target, debug_flag):
    """Prints date, time and date-time values to console when switch debug_flag = True"""
    if debug_flag:
        var_name = str(debug_target)
        print('\nDate:', debug_target.date())   
        print('Time:', debug_target.time())   
        print('Date-time:', debug_target)     

def print_df(debug_target, debug_flag):
    """prints dataframe and df stats when switch debug_flag = True"""
    if debug_flag:
        var_name = str(debug_target)
        print("\n" + retrieve_name(debug_target) + " dataframe ", debug_target, sep='\n')
        print("\t" + retrieve_name(debug_target) + " dataframe ", debug_target, sep='\n')
        print("\t" + retrieve_name(debug_target) + " dataframe ", debug_target, sep='\n')
        
