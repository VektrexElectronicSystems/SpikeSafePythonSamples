# Goal: 
# Connect to a SpikeSafe and run Modulated DC mode into an LED, Laser, or electrical component with a custom pulse sequence
#
# Expectation: 
# Channel 1 will be driven with varying current levels up to 150mA, specified within SCPI commands

import sys
import time
import logging
from spikesafe_python.Discharge import get_spikesafe_channel_discharge_time
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.Precision import get_precise_compliance_voltage_command_argument
from spikesafe_python.Precision import get_precise_current_command_argument
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
    log.info("RunModulatedMode.py started.")

    log.info("Python version: {}".format(sys.version))
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set Channel 1's pulse mode to Modulated DC
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP MODULATED')    

    # set Channel 1's current to 200 mA. This will be the output current when a sequence step specifies "@100"
    tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(0.2)}')       

    # set Channel 1's voltage to 20 V
    compliance_voltage = 20
    tcp_socket.send_scpi_command(f'SOUR1:VOLT {get_precise_compliance_voltage_command_argument(compliance_voltage)}') 

    # set Channel 1's modulated sequence to a DC staircase with 5 steps
    # There are 5 current steps that each last for 1 second: 40mA, 80mA, 120mA, 160mA, and 200mA
    tcp_socket.send_scpi_command('SOUR1:SEQ 1(1@20,1@40,1@60,1@80,1@100)') 

    # Log all events since all settings are sent
    log_all_events(tcp_socket) 

    # turn on Channel 1
    tcp_socket.send_scpi_command('OUTP1 1')                                         

    # Wait until channel is ready for a trigger command
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # Output modulated sequence
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # Wait until channel has completed it modulated sequence
    read_until_event(tcp_socket, SpikeSafeEvents.MODULATED_SEQ_IS_COMPLETED) # event 105 is "Modulated SEQ completed"

    # turn off Channel 1
    tcp_socket.send_scpi_command('OUTP1 0')
    wait_time = get_spikesafe_channel_discharge_time(compliance_voltage)
    wait(wait_time)      

    # set Channel 1's modulated sequence to an infinite pulsing pattern. This pulsing pattern will repeatedly perform 3 steps:
    #       1.) it will pulse Off for 250ms, then On for 250ms at 120mA. This will happen twice
    #       2.) it will pulse Off for 500ms, then On for 500ms at 60mA. This will also happen twice 
    #       3.) for one second, 180mA will be outputted
    tcp_socket.send_scpi_command('SOUR1:SEQ *(2(.25@0,.25@60),2(.5@0,.5@30),1@90)')          

    # turn on Channel 1
    tcp_socket.send_scpi_command('OUTP1 1')                                         

    # Wait until channel is ready for a trigger command
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # Output modulated sequence
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # check for all events and measure readings on Channel 1 once per second for 10 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 10                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)                            
    
    # turn off Channel 1. Since the sequence runs indefinitely, we do not wait for a "Modulated SEQ completed" message
    tcp_socket.send_scpi_command('OUTP1 0')      

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()   

    log.info("RunModulatedMode.py completed.\n")

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