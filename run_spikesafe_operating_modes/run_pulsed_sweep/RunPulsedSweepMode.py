# Goal: 
# Connect to a SpikeSafe and run Pulsed Sweep mode on Channel 1 into an LED, Laser, or electrical component and run two complete Pulsed Sweeps
#
# Expectation: 
# Channel 1 will run a sweep from 20mA to 200mA, which will take 100ms. Expecting a low (<1V) forward voltage

import sys
import time
import logging
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait     
from spikesafe_python.SpikeSafeError import SpikeSafeError

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282        

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("RunPulsedSweepMode.py started.")
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set Channel 1's pulse mode to Pulsed Sweep and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP PULSEDSWEEP')

    # set Channel 1's Pulsed Sweep parameters to match the test expectation
    tcp_socket.send_scpi_command('SOUR1:CURR:STAR 0.02')
    tcp_socket.send_scpi_command('SOUR1:CURR:STOP 0.2')   
    tcp_socket.send_scpi_command('SOUR1:CURR:STEP 100')   

    # set Channel 1 to output one pulse per step
    tcp_socket.send_scpi_command('SOUR1:PULS:COUN 1')

    # set Channel 1's voltage to 20 V 
    tcp_socket.send_scpi_command('SOUR1:VOLT 20')   

    # set Channel 1's pulse settings for a 1% duty cycle and 1ms Period using the Pulse On Time and Pulse Off Time commands
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 0.0001')
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 0.0099')

    # set Channel 1's compensation settings to High/Fast
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.send_scpi_command('SOUR1:PULS:CCOM 1')
    tcp_socket.send_scpi_command('SOUR1:PULS:RCOM 1')   

    # Check for any errors with initializing commands
    log_all_events(tcp_socket)

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # Wait until Channel 1 is ready for a trigger command
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # Output pulsed sweep for Channel 1
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # Wait for the Pulsed Sweep to be complete
    read_until_event(tcp_socket, 109) # event 109 is "Pulsed Sweep Complete"

    # Output pulsed sweep for Channel 1. Multiple sweeps can be run while the channel is enabled
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # Wait for the Pulsed Sweep to be complete
    read_until_event(tcp_socket, 109) # event 109 is "Pulsed Sweep Complete"

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    log.info("RunPulsedSweepMode.py completed.\n")

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