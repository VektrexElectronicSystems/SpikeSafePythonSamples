import sys
import time
import logging
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.Precision import get_precise_compliance_voltage_command_argument
from spikesafe_python.Precision import get_precise_current_command_argument
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.SpikeSafeEvents import SpikeSafeEvents
from spikesafe_python.SpikeSafeError import SpikeSafeError
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait

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
    log.info("discharge_channel_using_delay.py started.")

    log.info("Python version: {}".format(sys.version))
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket(enable_logging=False)
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set Channel 1's pulse mode to DC and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP DC')    
    log_all_events(tcp_socket)

    # set Channel 1's safety threshold for over current protection to 50% and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    log_all_events(tcp_socket) 

    # set Channel 1's current to 100 mA and check for all events
    tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(0.1)}')        
    log_all_events(tcp_socket)  

    # set Channel 1's voltage to 20 V and check for all events
    compliance_voltage = 20
    tcp_socket.send_scpi_command(f'SOUR1:VOLT {get_precise_compliance_voltage_command_argument(compliance_voltage)}')         
    log_all_events(tcp_socket) 

    # start test #1 by turning on Channel 1 and check for all events
    tcp_socket.send_scpi_command('OUTP1 1')               
    log_all_events(tcp_socket)
    
    # wait until the channel is fully ramped to 10mA
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # check for all events and measure readings on Channel 1 once per second for 5 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 5                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)                            
    
    # turn off Channel 1 and check for all events
    tcp_socket.send_scpi_command('OUTP1 0', enable_logging=True)               
    log_all_events(tcp_socket)

    # wait until the channel is fully discharged before starting test #2
    log.info('Waiting for Channel 1 to fully discharge after test #1...')
    is_discharge_complete = ''                
    while is_discharge_complete != 'TRUE':                       
        tcp_socket.send_scpi_command('OUTP1:DISC:COMP?', enable_logging=True)
        is_discharge_complete = tcp_socket.read_data(enable_logging=True)

    # start test #2 by turning on Channel 1 and check for all events
    tcp_socket.send_scpi_command('OUTP1 1', enable_logging=True)               
    log_all_events(tcp_socket)
    
    # wait until the channel is fully ramped to 10mA
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # check for all events and measure readings on Channel 1 once per second for 5 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 5                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)                            
    
    # turn off Channel 1 and check for all events
    tcp_socket.send_scpi_command('OUTP1 0', enable_logging=True)               
    log_all_events(tcp_socket)

    # wait until the channel is fully discharged before disconnecting the load
    log.info('Waiting for Channel 1 to fully discharge after test #2...')
    is_discharge_complete = ''                
    while is_discharge_complete != 'TRUE':                
        tcp_socket.send_scpi_command('OUTP1:DISC:COMP?', enable_logging=True)
        is_discharge_complete = tcp_socket.read_data(enable_logging=True)

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()                  

    log.info("discharge_channel_using_delay.py completed.\n")

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