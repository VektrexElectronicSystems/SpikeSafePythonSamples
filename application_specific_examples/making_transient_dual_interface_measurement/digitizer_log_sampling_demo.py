# Goal: Make a challenging Transient Dual Interface Measurement (TDIM) (JESD51-14) with the Vektrex PSMU

import sys
import time
import logging
import os

from decimal import Decimal
from spikesafe_python.MemoryTableReadData import MemoryTableReadData
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.SpikeSafeError import SpikeSafeError
from spikesafe_python.DigitizerDataFetch import fetch_voltage_data, wait_for_new_voltage_data
from matplotlib import pyplot as plt 
import numpy as np

def log_and_print_to_console(message_string):
    print(message_string)

def receive_user_input_and_log():
    inputText = input()
    return inputText

### set these before starting application

# SpikeSafe port number
port_number = 8282         

ok_string = "0, OK"
channel_ready_string = "100, Channel Ready; Channel(s) 1"
true_string = "TRUE"
slow_sampling_string = "SLOWLOG"
medium_sampling_string = "MEDIUMLOG"
fast_sampling_string = "FASTLOG"

log_and_print_to_console('\nPlease make sure the 5 minutes wait time is given between grease and non-grease test.\nPress Enter to continue.')
input()
log_and_print_to_console('\nEnter the option # for sampling mode:\n1. FASTLOG.\n2. MEDIUMLOG\n3. SLOWLOG.\nIf this is the second test, please make sure the sampling mode is the same as the first test.')
sampling_mode_input = float(receive_user_input_and_log())
log_and_print_to_console('\nEnter the option # for the 1st test:\n1. Grease.\n2. No Grease\n')
grease_input = float(receive_user_input_and_log())
log_and_print_to_console('\nEnter the IP address:')
ip_address = receive_user_input_and_log()

### setting up sequence log
log = logging.getLogger(__name__)
filename_grease_log = "digitizer_log_sampling_grease.log"
filename_no_grease_log = "digitizer_log_sampling_noGrease.log"
# the log file will be refered to current directory
if grease_input == 1:
    logging.basicConfig(filename=os.path.relpath(filename_grease_log), filemode = 'w', format=' %(message)s',datefmt='%S',level=logging.INFO)
elif grease_input == 2:
    logging.basicConfig(filename=os.path.relpath(filename_no_grease_log), filemode = 'w', format=' %(message)s',datefmt='%S',level=logging.INFO)

### start of main program
try:   
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,  this will automatically abort digitizer in order get it into a known state. This is good practice when connecting to a SpikeSafe PSMU  
    tcp_socket.send_scpi_command('*RST')    

    # Set digitizer range to 10V
    tcp_socket.send_scpi_command('VOLT:RANG 10')

    tcp_socket.send_scpi_command('SYST:ERR?')
    syst_err_string = tcp_socket.read_data()  

    # Set digitizer sampling mode 
    if sampling_mode_input == 1:
        tcp_socket.send_scpi_command('VOLT:SAMPMODE FASTLOG')
    elif sampling_mode_input == 2:
        tcp_socket.send_scpi_command('VOLT:SAMPMODE MEDIUMLOG')
    elif sampling_mode_input == 3:
        tcp_socket.send_scpi_command('VOLT:SAMPMODE SLOWLOG')

    # Query the digitizer sampling mode
    tcp_socket.send_scpi_command('VOLT:SAMPMODE?')
    sampling_mode_string = tcp_socket.read_data()      
    
    tcp_socket.send_scpi_command('SYST:ERR?')
    syst_err_string = tcp_socket.read_data()

    # Set digitizer trigger source to HARDWARE  
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')  

    # Set digitier trigger edge to rising
    tcp_socket.send_scpi_command('VOLT:TRIG:EDGE RISING')    

    # Set digitizer trigger delay to 50us
    tcp_socket.send_scpi_command('VOLT:TRIG:DEL 50')

    tcp_socket.send_scpi_command('SYST:ERR?')
    syst_err_string = tcp_socket.read_data()  

    # PSMU setting
    # set DC Dynamic mode
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP DCDYNAMIC')
    
    # set MCV to 25
    tcp_socket.send_scpi_command('SOUR1:VOLT 25')

    # set Auto Range
    tcp_socket.send_scpi_command('SOUR1:CURR:RANG:AUTO 1')

    # set current to 1A
    tcp_socket.send_scpi_command('SOUR1:CURR 1')

    # set Ramp mode to Fast
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')

    # wait for OK
    while True:
        tcp_socket.send_scpi_command('SYST:ERR?')
        syst_err_string = tcp_socket.read_data()    
        if syst_err_string == ok_string:
            break

    # the trigger signal come from the voltage start up
    tcp_socket.send_scpi_command('VOLT:INIT')

    # Start the channel
    tcp_socket.send_scpi_command('OUTP1 ON')
    # wait for channel ready
    while True:
        tcp_socket.send_scpi_command('SYST:ERR?')
        syst_err_string = tcp_socket.read_data()    
        if syst_err_string == channel_ready_string:
            break

    start_data_ready_time = time.time()
    while True:
        time.sleep(1)
        tcp_socket.send_scpi_command('VOLT:NDAT?')
        ndataStr = tcp_socket.read_data()    
        if ndataStr == true_string:
            break  

    # Fetch Data    
    digitizer_data = fetch_voltage_data(tcp_socket)

    # time stamp record the approximate timing between the trigger signal and the data output 
    end_data_ready_time = time.time()

    # wait for OK
    while True:
        tcp_socket.send_scpi_command('SYST:ERR?')
        syst_err_string = tcp_socket.read_data()    
        if syst_err_string == ok_string:
            break

    # disconnect from SpikeSafe    
    tcp_socket.close_socket()      

    # plot graph
    voltage_readings = []
    current_steps = []
    if sampling_mode_string == slow_sampling_string:
        Time_us = 1000
    elif sampling_mode_string == medium_sampling_string:
        Time_us = 2
    elif sampling_mode_string == fast_sampling_string:
        Time_us = 2

    i = 0
    for dd in digitizer_data:
        if sampling_mode_string == slow_sampling_string:
            # log time scale
            if i > 0 and i <=99:
                Time_us = Time_us + 1000
            elif i > 99 and i <= 189:
                Time_us = Time_us + 10000
            elif i > 189 and i <= 279:
                Time_us = Time_us + 100000
            elif i > 279 and i <= 369:
                Time_us = Time_us + 1000000       
            elif i > 369 and i <= 459:
                Time_us = Time_us + 10000000
        elif sampling_mode_string == medium_sampling_string:    
            if i > 0 and i <=49:
                Time_us = Time_us + 2
            elif i > 49 and i <= 124:
                Time_us = Time_us + 12
            elif i > 124 and i <= 199:
                Time_us = Time_us + 120
            elif i > 199 and i <= 274:
                Time_us = Time_us + 1200       
            elif i > 274 and i <= 349:
                Time_us = Time_us + 12000
            elif i > 349 and i <= 424:         
                Time_us = Time_us + 120000                        
            elif i > 424 and i <= 499:         
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
        voltage_readings.append(dd.voltage_reading)   
        current_steps.append(Time_us/1000000)
        i = i + 1   
        logging.info('%.10f' % (dd.voltage_reading))
    
    logging.info("Data Ready time:  {}".format(end_data_ready_time-start_data_ready_time))

    graph, voltage_axis = plt.subplots()
    voltage_axis.plot(current_steps, voltage_readings, color='tab:red')
    plt.xscale('log')
    voltage_axis.set_xlabel('Time (s)')
    voltage_axis.set_ylabel('Voltage (V)')    

    if sampling_mode_string == slow_sampling_string:
        plt.title('Digitizer Slow Log Sampling')
    elif sampling_mode_string == medium_sampling_string:
        plt.title('Digitizer Medium Log Sampling')
    elif sampling_mode_string == fast_sampling_string:
        plt.title('Digitizer Fast Log Sampling')

    graph.tight_layout()
    plt.grid()
    plt.show()

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