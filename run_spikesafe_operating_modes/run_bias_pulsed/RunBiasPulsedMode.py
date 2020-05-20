# Goal: 
# Connect to a SpikeSafe and run Bias Pulsed mode on all channels into an LED, Laser, or electrical component for 10 seconds while obtaining readings
# 
# Expectation: 
# All channels will be driven with 100mA with a forward voltage of <1V during this time

import sys
import time
import logging
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait     

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282         

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("RunBiasPulsedMode.py started.")
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # Synchronize rising edge of all channels
    tcp_socket.send_scpi_command('SOUR0:PULS:STAG 0')   

    # set each channel's pulse mode to Pulsed Dynamic
    tcp_socket.send_scpi_command('SOUR0:FUNC:SHAP BIASPULSED')

    # set each channel's current to 100 mA
    tcp_socket.send_scpi_command('SOUR0:CURR 0.1')   

    # set each channel's voltage to 10 V 
    tcp_socket.send_scpi_command('SOUR0:VOLT 10') 

    # set each channel's bias current to 20 mA and check for all events
    tcp_socket.send_scpi_command('SOUR0:CURR:BIAS 0.02')   

    # In this example, we specify pulse settings using Pulse Width and Period Commands
    # Unless specifying On Time and Off Time, set pulse HOLD before any other pulse settings
    tcp_socket.send_scpi_command('SOUR0:PULS:HOLD PERIOD')   

    tcp_socket.send_scpi_command('SOUR0:PULS:PER 0.01')

    # When Pulse Width is set, Period will not be adjusted at all because we are holding period. Duty Cycle will be adjusted as a result
    tcp_socket.send_scpi_command('SOUR0:PULS:WIDT 0.001')

    # set each channel's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.send_scpi_command('SOUR0:PULS:CCOM 4')
    tcp_socket.send_scpi_command('SOUR0:PULS:RCOM 4')   

    # Check for any errors with initializing commands
    log_all_events(tcp_socket)

    # turn on all channels
    tcp_socket.send_scpi_command('OUTP0 1')

    # wait until the channel is fully ramped
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # check for all events and measure readings for all channels once per second for 10 seconds,
    # it is best practice to do this to ensure each channel is on and does not have any errors
    time_end = time.time() + 10                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)

    # turn off all channels after routine is complete
    tcp_socket.send_scpi_command('OUTP0 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()  

    log.info("RunBiasPulsedMode.py completed.\n")

except Exception as err:
    # print any error to the log file and exit application
    log.error('Program error: {}'.format(err))          
    sys.exit(1)


