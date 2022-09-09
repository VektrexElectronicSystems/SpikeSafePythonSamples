# Goal: 
# Connect to a SpikeSafe and run Single Pulse mode on all channels into an LED, Laser, or electrical component and output to all channels
# 
# Expectation: 
# All channels will output a 100mA pulse with a pulse width of 1ms. This will happen 3 times. Expecting a low (<1V) forward voltage

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
    log.info("RunSinglePulseMode.py started.")
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set each channel's pulse mode to Single Pulse
    tcp_socket.send_scpi_command('SOUR0:FUNC:SHAP SINGLEPULSE')

    # set each channel's current to 100 mA
    tcp_socket.send_scpi_command('SOUR0:CURR 0.1')     

    # set each channel's voltage to 20 V 
    tcp_socket.send_scpi_command('SOUR0:VOLT 20')   

    # set each channel's pulse width to 1ms. Of the pulse time settings, only Pulse On Time and Pulse Width [+Offset] are relevant in Single Pulse mode
    tcp_socket.send_scpi_command('SOUR0:PULS:TON 0.001')

    # set each channel's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.send_scpi_command('SOUR0:PULS:CCOM 4')
    tcp_socket.send_scpi_command('SOUR0:PULS:RCOM 4')   
    
    # set Channel 1's Ramp mode to Fast
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')  

    # Check for any errors with initializing commands
    log_all_events(tcp_socket)

    # turn on all channels
    tcp_socket.send_scpi_command('OUTP0 1')

    # Wait until channels are ready for a trigger command
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # Output 1ms pulse for all channels
    tcp_socket.send_scpi_command('OUTP0:TRIG')

    # check for all events and measure readings on each channel once per second for 2 seconds,
    # it is best practice to do this to ensure each channel is on and does not have any errors
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)        

    # Output 1ms pulse for all channels. Multiple pulses can be outputted while the channel is enabled
    tcp_socket.send_scpi_command('OUTP0:TRIG')

    # check for all events and measure readings after the second pulse output
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1) 

    # After the pulse is complete, set each channel's current to 200 mA while the channels are enabled
    tcp_socket.send_scpi_command('SOUR0:CURR 0.2')  

    # Output 1ms pulse for all channels
    tcp_socket.send_scpi_command('OUTP0:TRIG')

    # check for all events and measure readings after the last pulse output
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1) 

    # turn off all channels after routine is complete
    tcp_socket.send_scpi_command('OUTP0 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    log.info("RunSinglePulseMode.py completed.\n")

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