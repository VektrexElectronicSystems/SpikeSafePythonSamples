# Goal: 
# Make a junction temperature measurement on an LED using the Electrical Test Method specified by the Joint Electron Device Engineering Council
#
# Expectation:
# 1.) A K-factor will be measured by comparing voltages at two controlled temperatures
# 2.) The LED will be heated using its operational current until it reaches a stable operating temperature
# 3.) The SpikeSafe will be run in CDBC mode and the digitizer will make voltage readings at the beginning of an Off Time cycle

import sys
import time
import logging
from spikesafe_python.DigitizerDataFetch import wait_for_new_voltage_data
from spikesafe_python.DigitizerDataFetch import fetch_voltage_data
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait     
from spikesafe_python.SpikeSafeError import SpikeSafeError
from matplotlib import pyplot as plt
from tkinter import messagebox 

### set these before starting application

def log_and_print(message_string):
    log.info(message_string)
    print(message_string)

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282 

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("TjMeasurement.py started.")
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # abort digitizer in order get it into a known state. This is good practice when connecting to a SpikeSafe SMU
    tcp_socket.send_scpi_command('VOLT:ABOR')

    # set up Channel 1 for Bias Current output to determine the K-factor
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP BIAS')
    tcp_socket.send_scpi_command('SOUR0:CURR:BIAS 0.033')
    tcp_socket.send_scpi_command('SOUR1:VOLT 40')
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')  

    log_and_print('Configured SpikeSafe to Bias Current mode to obtain K-factor. Starting current output.')

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # wait until Channel 1 is ready to pulse
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    messagebox.showinfo('Bias Current Output Started','Measurement Current is currently outputting to the DUT.\n\nPress \'OK\' once temperature has been stabilized at T1, and both  V1 and T1 have been recorded')

    wait(2)

    messagebox.showinfo('Bias Current Output Started','Measurement Current is currently outputting to the DUT.\n\nChange the control temperature to T2.\n\nPress \'OK\' once temperature has been stabilized at T2, and both the V2 and T2 have been recorded')

    # turn off Channel 1 
    tcp_socket.send_scpi_command('OUTP1 0')

    log_and_print('K-factor values obtained. Stopped bias current output. Configuring to take Electrical Test Method measurement.')

    # set up Channel 1 for CDBC output to make the junction temperature measurement
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP BIASPULSEDDYNAMIC')
    tcp_socket.send_scpi_command('SOUR1:CURR 3.5')
    tcp_socket.send_scpi_command('SOUR0:CURR:BIAS 0.033')
    tcp_socket.send_scpi_command('SOUR1:VOLT 40')
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 1')
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 0.001')
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')  

    # set Digitizer settings to take a series of quick measurements during the Off Time of CDBC operation
    tcp_socket.send_scpi_command('VOLT:RANG 100')
    tcp_socket.send_scpi_command('VOLT:APER 2')
    tcp_socket.send_scpi_command('VOLT:TRIG:DEL 0')
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')
    tcp_socket.send_scpi_command('VOLT:TRIG:EDGE FALLING')
    tcp_socket.send_scpi_command('VOLT:TRIG:COUN 1')
    tcp_socket.send_scpi_command('VOLT:READ:COUN 50')

    # check all SpikeSafe event since all settings have been sent
    log_all_events(tcp_socket)

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # wait until Channel 1 is ready to pulse
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    messagebox.showinfo('Continuous Pulse Train Outputting', 'Heating Current is being outputted.\n\nWait until temperature has stabilized, then press \'OK\' to take voltage measurements.')

    # initialize the digitizer. Measurements will be taken once a current pulse is outputted
    tcp_socket.send_scpi_command('VOLT:INIT')

    # wait for the Digitizer measurements to complete 
    wait_for_new_voltage_data(tcp_socket, 0.5)

    # fetch the Digitizer voltage readings using VOLT:FETC? query
    digitizerData = []
    digitizerData = fetch_voltage_data(tcp_socket)

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # prepare digitizer voltage data to plot
    samples = []
    voltage_readings = []
    for dd in digitizerData:
        samples.append(dd.sample_number)
        voltage_readings.append(dd.voltage_reading)

    # plot the pulse shape using the fetched voltage readings
    plt.plot(samples, voltage_readings)
    plt.ylabel('Voltage (V)')
    plt.xlabel('Logarithmic time since start of Heating Current (log s)')
    plt.xscale('log')
    plt.title('Digitizer Voltage Readings - Vf(0) Extrapolation')
    plt.grid()
    plt.show()

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()

    log.info("TjMeasurement.py completed.\n")

except SpikeSafeError as ssErr:
    # print any SpikeSafe-specific error to both the terminal and the log file, then exit the application
    error_message = 'SpikeSafe error: {}\n'.format(ssErr)
    log.error(error_message)
    print(error_message)
    sys.exit(1)
except Exception as err:
    # print any general exception to both the terminal and the log file, then exit the application
    error_message = 'Program error: {}\n'.format(err)
    log.error(error_message)       
    print(error_message)   
    sys.exit(1)
