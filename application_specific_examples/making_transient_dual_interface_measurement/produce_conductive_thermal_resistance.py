# Goal: 
# Read the Grease/no Grease data files and plot the graph 

import sys
import os

from decimal import Decimal
from spikesafe_python.SpikeSafeError import SpikeSafeError
from matplotlib import pyplot as plt 
import numpy as np

def log_and_print_to_console(message_string):
    print(message_string)

def receive_user_input_and_log():
    inputText = input()
    return inputText

slow_sampling_string = "SLOWLOG"
medium_sampling_string = "MEDIUMLOG"
fast_sampling_string = "FASTLOG"
slow_sampling_mode = 3
medium_sampling_mode = 2
fast_sampling_mode = 1

# the number of samples
# use for checking wheather the plot is fast or slow log sampling   
num_of_data_fastLog = 525
num_of_data_mediumLog = 500
num_of_data_slowLog = 460

filename_grease_log = "digitizer_log_sampling_grease.log"
filename_no_grease_log = "digitizer_log_sampling_noGrease.log"

log_and_print_to_console('\nEnter the option # for sampling mode:\n1. FASTLOG.\n2. MEDIUMLOG\n3. SLOWLOG.\n')
sampling_mode_input = float(receive_user_input_and_log())

### start of main program
try:   
    # open grease data file in current directory
    grease_data = open(os.path.relpath(filename_grease_log), "r")
    
    grease_data_string = grease_data.read()
    grease_data_list = grease_data_string.split("\n")
    # put voltage data into grease_data_list 
    for i in range(0, len(grease_data_list)-2, 1):
        grease_data_list[i] = grease_data_list[i]. replace("\n", "")
        grease_data_list[i] = float(grease_data_list[i])

    # record the number of samples for grease data
    # the number of data of the 2 files should be the same
    # the data in two files should be ran with the same sampling mode
    # (the number of data of fast log = 525)
    # (the number of data of slow log = 460)    
    num_of_data_grease = i + 1

    # open no grease data file in current directory
    no_grease_data = open(os.path.relpath(filename_no_grease_log), "r")
    no_grease_data_string = no_grease_data.read()
    no_grease_data_list = no_grease_data_string.split("\n")
    # put voltage data into noGreasedDataList
    for i in range(0, len(no_grease_data_list)-2, 1):
        no_grease_data_list[i] = no_grease_data_list[i]. replace("\n", "")
        no_grease_data_list[i] = float(no_grease_data_list[i])

    # record the number of sample for no grease data
    num_of_data_noGrease = i + 1

    if num_of_data_grease != num_of_data_noGrease:
        #should show error message
        raise Exception("\nThe Grease and no Grease testing were ran with different sampling mode.")
    else:
        num_of_data = num_of_data_noGrease

    if sampling_mode_input == fast_sampling_mode:
        sampling_mode_string = fast_sampling_string
    elif sampling_mode_input == medium_sampling_mode:
        sampling_mode_string = medium_sampling_string
    elif sampling_mode_input == slow_sampling_mode:
        sampling_mode_string = slow_sampling_string

    # plot graph
    Time_us = 0
    grease_readings = []
    no_grease_readings = []
    diff_readings = []
    time_value = []
    i = 1
    for dd in range(num_of_data):
        grease_readings.append(grease_data_list[dd])
        no_grease_readings.append(no_grease_data_list[dd])
        diff_readings.append(grease_data_list[dd] - no_grease_data_list[dd])
        time_value.append(Time_us/1000000)
        if sampling_mode_string == slow_sampling_string:
            # log time scale
            if i > 0 and i <=49:
                Time_us = Time_us + 2
            elif i > 49 and i <= 139:
                Time_us = Time_us + 10
            elif i > 139 and i <= 229:
                Time_us = Time_us + 100
            elif i > 229 and i <= 319:
                Time_us = Time_us + 1000       
            elif i > 319 and i <= 364:
                Time_us = Time_us + 20000
            elif i > 364 and i <= 409:
                Time_us = Time_us + 200000
            elif i > 409 and i <= 454:
                Time_us = Time_us + 2000000   
            elif i > 454 and i <= 500:
                Time_us = Time_us + 20000000   
        elif sampling_mode_string == medium_sampling_string:    
            if i >= 0 and i <=49:
                Time_us = Time_us + 2
            elif i >= 50 and i <= 124:
                Time_us = Time_us + 12
            elif i >= 125 and i <= 199:
                Time_us = Time_us + 120
            elif i >= 200 and i <= 274:
                Time_us = Time_us + 1200       
            elif i >= 275 and i <= 349:
                Time_us = Time_us + 12000
            elif i >= 350 and i <= 424:         
                Time_us = Time_us + 120000                        
            elif i >= 425 and i <= 499:         
                Time_us = Time_us + 1200000  
        elif sampling_mode_string == fast_sampling_string:
            if i > 0 and i <=99:
                Time_us = Time_us + 2
            elif i > 99 and i <= 179:
                Time_us = Time_us + 10
            elif i > 179 and i <= 269:
                Time_us = Time_us + 100
            elif i > 269 and i <= 359:
                Time_us = Time_us + 1000       
            elif i > 359 and i <= 449:
                Time_us = Time_us + 10000
            elif i > 449 and i <= 524:         
                Time_us = Time_us + 100000
        i = i + 1   
     
    # plot the voltage graph for grease and no grease
    plot1 = plt.figure(1)
    plt.plot(time_value, grease_readings, color='tab:red')
    plt.plot(time_value, no_grease_readings, color='tab:blue')
    plt.legend(["With Grease", "With No Grease"])
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')    
    plt.grid()
    if sampling_mode_string == slow_sampling_string:
        plt.title('Digitizer Slow Log Sampling')
    elif sampling_mode_string == medium_sampling_string:
        plt.title('Digitizer Medium Log Sampling')    
    elif sampling_mode_string == fast_sampling_string:
        plt.title('Digitizer Fast Log Sampling')      
    plt.xscale('log')
    plot1.show()

    # plot the graph for grease and no grease voltage subtraction
    plot2 = plt.figure(2)
    plt.plot(time_value, diff_readings, color='tab:green')
    plt.legend(["Voltage Difference"])
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')    
    plt.grid()
    if sampling_mode_string == slow_sampling_string:
        plt.title('Voltage Subtraction (Slow Log Sampling)')
    elif sampling_mode_string == medium_sampling_string:
        plt.title('Voltage Subtraction (Medium Log Sampling)')
    elif sampling_mode_string == fast_sampling_string:
        plt.title('Voltage Subtraction (Fast Log Sampling)')      
    plt.xscale('log')
    plot2.show()

    # hold to show graph
    input("Press [enter] to end.")

except SpikeSafeError as ssErr:
    # print any SpikeSafe-specific error to both the terminal and the log file, then exit the application
    error_message = 'SpikeSafe error: {}\n'.format(ssErr)
    print(error_message)
    sys.exit(1)
except Exception as err:
    # print any general exception to both the terminal and the log file, then exit the application
    error_message = 'Program error: {}\n'.format(err)     
    print(error_message)   
    sys.exit(1)

