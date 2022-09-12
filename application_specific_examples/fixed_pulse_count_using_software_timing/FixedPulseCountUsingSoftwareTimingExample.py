# Goal: 
# Make 10,000 pulses using software based timing and then shutoff pulsing

import sys
import time
import logging
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.SpikeSafeEvents import SpikeSafeEvents
from spikesafe_python.SpikeSafeError import SpikeSafeError
from spikesafe_python.TcpSocket import TcpSocket

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282 

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("FixedPulseCountUsingSoftwareTimingExample.py started.")
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set Channel 1's mode to DC Dynamic and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP PULSEDDYNAMIC')
    log_all_events(tcp_socket)

    # set Channel 1's Trigger Output to Positive and check for all events
    tcp_socket.send_scpi_command('OUTP1:TRIG:SLOP POS')
    log_all_events(tcp_socket)

    # set Channel 1's Trigger Output Always and check for all events
    tcp_socket.send_scpi_command('SOUR0:PULS:TRIG ALWAYS')
    log_all_events(tcp_socket)

    # set Channel 1's Pulse On Time to 1us and check for all events
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 0.000001')
    log_all_events(tcp_socket)

    # set Channel 1's Pulse Off Time 9us and check for all events
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 0.000009')
    log_all_events(tcp_socket)

    # set Channel 1's Pulse Width adjustment to disabled and check for all events
    tcp_socket.send_scpi_command('SOUR1:PULS:AADJ 0')
    log_all_events(tcp_socket)

    # set Channel 1's current to 100mA and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR 0.1')
    log_all_events(tcp_socket)

    # set Channel 1's voltage to 20V and check for all events
    tcp_socket.send_scpi_command('SOUR1:VOLT 20')
    log_all_events(tcp_socket)

    # set Channel 1's Auto Range to On and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR:RANG:AUTO 1')
    log_all_events(tcp_socket)

    # set Channel 1's Load Impedance to High and check for all events
    tcp_socket.send_scpi_command('SOUR1:PULS:CCOM 1')
    log_all_events(tcp_socket)

    # set Channel 1's Rise Time to Fast and check for all events
    tcp_socket.send_scpi_command('SOUR1:PULS:RCOM 1')
    log_all_events(tcp_socket)

    # set Channel 1's Ramp mode to Fast and check for all events
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')
    log_all_events(tcp_socket)

    # Start the channel
    tcp_socket.send_scpi_command('OUTP1 ON')

    # wait until Channel 1 is ready
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # pulsing starts before before getting Channel Ready message
    # wait 30ms for getting ~10000 pulses
    time.sleep(0.030)
    
    # disable Channel
    tcp_socket.send_scpi_command('OUTP1 OFF')
        
    # disconnect from SpikeSafe    
    tcp_socket.close_socket()      

    log.info("FixedPulseCountUsingSoftwareTimingExample.py completed.\n")

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