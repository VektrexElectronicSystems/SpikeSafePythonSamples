# Goal:
# Tune the pulse shape of a SpikeSafe PSMU or PRF by varying the compensation settings (Load Impedance and Rise Time)
#
# Expectation:
# A single 100µs pulse will be outputted sixteen separate times, demonstrating each combination of pulse tuning settings

import sys
import time
import logging
from enum import Enum
from matplotlib import pyplot as plt
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.Precision import get_precise_current_command_argument
from spikesafe_python.Precision import get_precise_time_command_argument
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.SpikeSafeEvents import SpikeSafeEvents
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait 
from tkinter import messagebox     

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

### defining the action to take per test session
def run_single_pulse_tuning_test(load_impedance, rise_time):
    
    log.info('Running single pulse tuning test iteration with {} and {}'.format(load_impedance, rise_time))

    # set the load impedance and rise time according to the input parameters
    tcp_socket.send_scpi_command('SOUR1:PULS:CCOM {}'.format(LoadImpedance(load_impedance).value))
    tcp_socket.send_scpi_command('SOUR1:PULS:RCOM {}'.format(RiseTime(rise_time).value)) 

    # Check for any errors with initializing commands
    log_all_events(tcp_socket)

    # turn on all channels
    tcp_socket.send_scpi_command('OUTP1 1')

    # Wait until channels are ready for a trigger command
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # Output 1ms pulse for all channels
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    is_pulse_complete = ''                
    while is_pulse_complete != 'TRUE':                       
        tcp_socket.send_scpi_command('SOUR1:PULS:END?')
        is_pulse_complete = tcp_socket.read_data()
        log_all_events(tcp_socket)

    messagebox.showinfo("Single Pulse Outputted", "Observe the current pulse shape using an oscilloscope or DMM, and note the current compensation settings.\n\nPress \"OK\" to move to the next combination of Pulse Tuning settings.\n\nLoad Impedance: {}\nRise Time: {}".format(LoadImpedance(load_impedance).name, RiseTime(rise_time).name))

    tcp_socket.send_scpi_command('OUTP1 0')

    # wait one second to account for any electrical transients before starting the next session
    wait(1)

    log.info('Single pulse tuning test iteration completed successfully.')

    return

### classes to express the compensation settings being tested
class LoadImpedance(Enum):
    VERY_LOW = 4
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class RiseTime(Enum):
    VERY_SLOW = 4
    SLOW = 3
    MEDIUM = 2
    FAST = 1

### start of main program
try:
    log.info("PulseTuningExample.py started.")

    log.info("Python version: {}".format(sys.version))
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set channel 1's pulse mode to Single Pulse
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP SINGLEPULSE')

    # set channel 1's current to 100 mA
    tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(0.1)}')     

    # set channel 1's voltage to 20 V 
    tcp_socket.send_scpi_command('SOUR1:VOLT 20')   

    # set channel 1's pulse width to 100µs. Of the pulse time settings, only Pulse On Time and Pulse Width [+Offset] are relevant in Single Pulse mode
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {get_precise_time_command_argument(0.0001)}')

    # set channel 1's output ramp to fast
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')

    # Check for any errors with initializing commands
    log_all_events(tcp_socket)

    # run each combination of Pulse Tuning settings to determine the settings that output the best pulse shape
    # per Vektrex recommendation, Load Impedance is tuned prior to Rise Time
    # once a pattern has been established, it may be useful to comment out ineffective or redundant test cases
    run_single_pulse_tuning_test(LoadImpedance.VERY_LOW, RiseTime.VERY_SLOW)    
    run_single_pulse_tuning_test(LoadImpedance.LOW, RiseTime.VERY_SLOW)    
    run_single_pulse_tuning_test(LoadImpedance.MEDIUM, RiseTime.VERY_SLOW)    
    run_single_pulse_tuning_test(LoadImpedance.HIGH, RiseTime.VERY_SLOW)    

    run_single_pulse_tuning_test(LoadImpedance.VERY_LOW, RiseTime.SLOW)    
    run_single_pulse_tuning_test(LoadImpedance.LOW, RiseTime.SLOW)    
    run_single_pulse_tuning_test(LoadImpedance.MEDIUM, RiseTime.SLOW)    
    run_single_pulse_tuning_test(LoadImpedance.HIGH, RiseTime.SLOW)    

    run_single_pulse_tuning_test(LoadImpedance.VERY_LOW, RiseTime.MEDIUM)    
    run_single_pulse_tuning_test(LoadImpedance.LOW, RiseTime.MEDIUM)    
    run_single_pulse_tuning_test(LoadImpedance.MEDIUM, RiseTime.MEDIUM)    
    run_single_pulse_tuning_test(LoadImpedance.HIGH, RiseTime.MEDIUM)    

    run_single_pulse_tuning_test(LoadImpedance.VERY_LOW, RiseTime.FAST)    
    run_single_pulse_tuning_test(LoadImpedance.LOW, RiseTime.FAST)    
    run_single_pulse_tuning_test(LoadImpedance.MEDIUM, RiseTime.FAST)    
    run_single_pulse_tuning_test(LoadImpedance.HIGH, RiseTime.FAST)    

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    log.info("PulseTuningExample.py completed.\n")

except Exception as err:
    # print any error to the log file and exit application
    log.error('Program error: {}'.format(err))          
    sys.exit(1)
