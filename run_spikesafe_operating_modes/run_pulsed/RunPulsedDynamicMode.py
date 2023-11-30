# Goal: 
# Connect to a SpikeSafe and run Pulsed Dynamic mode into an LED, Laser, or electrical component for 10 seconds while obtaining readings
# Settings will be adjusted while running "dynamically" to demonstrate dynamic mode features, and then the channel will output for a few more seconds
#
# Expectation: 
# Channel 1 will be driven with 100mA with a forward voltage of <1V during this time
# While running, Set Current will be changed to 200mA, and On Time & Off Time will be changed to 100µs

import sys
import time
import logging
from spikesafe_python.Compensation import get_optimum_compensation
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.Precision import get_precise_compliance_voltage_command_argument
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
    log.info("RunPulsedDynamicMode.py started.")

    log.info("Python version: {}".format(sys.version))
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set Channel 1's pulse mode to Pulsed Dynamic
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP PULSEDDYNAMIC')

    # set Channel 1's current to 100 mA
    set_current = 0.1
    tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(set_current)}')   

    # set Channel 1's voltage to 20 V 
    tcp_socket.send_scpi_command(f'SOUR1:VOLT {get_precise_compliance_voltage_command_argument(20)}')   

    # set Channel 1's Pulse On Time to 1ms
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {get_precise_time_command_argument(0.001)}')

    # set Channel 1's Pulse Off Time to 9ms
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TOFF {get_precise_time_command_argument(0.009)}')

    # set Channel 1's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.send_scpi_command('SOUR1:CURR? MAX')
    spikesafe_model_max_current = float(tcp_socket.read_data())
    load_impedance, rise_time = get_optimum_compensation(spikesafe_model_max_current, set_current)
    tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}') 
    
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

    # set Channel 1's current to 200 mA dynamically while channel is operating. Check events and measure readings
    tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(0.2)}')
    log_all_events(tcp_socket)
    log_memory_table_read(tcp_socket)
    wait(1)

    # set Channel 1's Pulse On Time to 100µs dynamically while channel is operating. Check events and measure readings
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {get_precise_time_command_argument(0.0001)}')
    log_all_events(tcp_socket)
    log_memory_table_read(tcp_socket)
    wait(1)

    # set Channel 1's Pulse Off Time to 100µs dynamically while channel is operating. Check events and measure readings
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TOFF {get_precise_time_command_argument(0.0001)}')

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

    log.info("RunPulsedDynamicMode.py completed.\n")

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


