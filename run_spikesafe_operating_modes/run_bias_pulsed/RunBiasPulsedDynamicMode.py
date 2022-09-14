# Goal:
# Connect to a SpikeSafe and run Bias Pulsed Dynamic mode into an LED, Laser, or electrical component for over 10 seconds while obtaining readings
# Settings will be adjusted while running "dynamically" to demonstrate dynamic mode features. Channel will run for 5 more seconds afterwards
#
# Expectation: 
# Channel 1 will be driven constant with 20mA, and increase by 100mA during On Times
# While running, the On and Off Times will be adjusted to 100µs, and the pulsed Set Current will be adjusted to 200mA
# We expect a forward voltage of ~100mV while runing this sequence

import sys
import time
import logging
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.SpikeSafeEvents import SpikeSafeEvents
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait     
from spikesafe_python.SpikeSafeError import SpikeSafeError

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("RunBiasPulsedDynamicMode.py started.")
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # Synchronize rising edge of all channels
    tcp_socket.send_scpi_command('SOUR1:PULS:STAG 0')   

    # set Channel 1's pulse mode to Pulsed Dynamic and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP BIASPULSEDDYNAMIC')

    # set Channel 1's current to 100 mA
    tcp_socket.send_scpi_command('SOUR1:CURR 0.1')   

    # set Channel 1's voltage to 10 V 
    tcp_socket.send_scpi_command('SOUR1:VOLT 20') 

    # set Channel 1's bias current to 20 mA and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR:BIAS 0.02')   

    # set Channel 1's Pulse On Time to 1ms
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 0.001')

    # set Channel 1's Pulse Off Time to 9ms
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 0.009')

    # set Channel 1's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.send_scpi_command('SOUR1:PULS:CCOM 4')
    tcp_socket.send_scpi_command('SOUR1:PULS:RCOM 4')

    # set Channel 1's Ramp mode to Fast
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')  

    # Check for any errors with initializing commands
    log_all_events(tcp_socket)

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # wait until the channel is fully ramped
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # check for all events and measure readings on Channel 1 once per second for 10 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 10                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)

    # set Channel 1's current to 200 mA while running
    tcp_socket.send_scpi_command('SOUR1:CURR 0.2')      

    # set Channel 1's Pulse On Time to 100µs dynamically while channel is operating. Check events and measure readings
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 0.0001')
    log_all_events(tcp_socket)
    log_memory_table_read(tcp_socket)
    wait(1)

    # set Channel 1's Pulse Off Time to 100µs dynamically while channel is operating. Check events and measure readings
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 0.0001')

    # after dynamically applying all new settings, check for all events and measure readings on Channel 1 once per second for 5 seconds
    time_end = time.time() + 5                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    log.info("RunBiasPulsedDynamicMode.py completed.\n")

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


