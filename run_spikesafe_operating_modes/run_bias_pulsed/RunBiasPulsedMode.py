# Goal: 
# Connect to a SpikeSafe and run Bias Pulsed mode on all channels into an LED, Laser, or electrical component for 10 seconds while obtaining readings
# 
# Expectation: 
# All channels will be driven with 100mA with a forward voltage of <1V during this time

import sys
import time
import logging
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.Precision import get_precise_current_command_argument
from spikesafe_python.Precision import get_precise_time_command_argument
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
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S',
    handlers=[
        logging.FileHandler("SpikeSafePythonSamples.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

### start of main program
try:
    log.info("RunBiasPulsedMode.py started.")

    log.info("Python version: {}".format(sys.version))
    
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
    tcp_socket.send_scpi_command(f'SOUR0:CURR {get_precise_current_command_argument(0.1)}')   

    # set each channel's voltage to 20 V 
    tcp_socket.send_scpi_command('SOUR0:VOLT 20') 

    # set each channel's bias current to 20 mA and check for all events
    tcp_socket.send_scpi_command(f'SOUR0:CURR:BIAS {get_precise_current_command_argument(0.02)}')   

    # In this example, we specify pulse settings using Pulse Width and Period Commands
    # Unless specifying On Time and Off Time, set pulse HOLD before any other pulse settings
    tcp_socket.send_scpi_command('SOUR0:PULS:HOLD PERIOD')   

    tcp_socket.send_scpi_command(f'SOUR0:PULS:PER {get_precise_time_command_argument(0.01)}')

    # When Pulse Width is set, Period will not be adjusted at all because we are holding period. Duty Cycle will be adjusted as a result
    tcp_socket.send_scpi_command(f'SOUR0:PULS:WIDT {get_precise_time_command_argument(0.001)}')

    # set each channel's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.send_scpi_command('SOUR0:PULS:CCOM 4')
    tcp_socket.send_scpi_command('SOUR0:PULS:RCOM 4')
    
    # set each channe's ramp mode to Fast
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')   

    # Check for any errors with initializing commands
    log_all_events(tcp_socket)

    # turn on all channels
    tcp_socket.send_scpi_command('OUTP0 1')

    # wait until the channel is fully ramped
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

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


