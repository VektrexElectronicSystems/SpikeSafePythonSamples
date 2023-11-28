# Goal: 
# Demonstrate use of the alternate commands to adjust SpikeSafe Pulse On Time and Off Time
# Commands for Pulse Width, Duty Cycle, Pulse Period, and Pulse Hold will be demonstrated. Settings will be adjusted while running "dynamically"
#
# Expectation: 
#

import sys
import time
import logging
from spikesafe_python.MemoryTableReadData import log_memory_table_read
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

def log_and_print(message_string):
    log.info(message_string)
    print(message_string)

def verify_current_pulse_settings(spike_safe_socket):
    spike_safe_socket.send_scpi_command('SOUR1:PULS:WIDT?')
    pulse_width = spike_safe_socket.read_data()
    log_and_print('Updated Pulse Width: {}s'.format(pulse_width))

    spike_safe_socket.send_scpi_command('SOUR1:PULS:DCYC?')
    duty_cycle = spike_safe_socket.read_data()
    log_and_print('Updated Duty Cycle: {}%'.format(duty_cycle))

    spike_safe_socket.send_scpi_command('SOUR1:PULS:PER?')
    pulse_period = spike_safe_socket.read_data()
    log_and_print('Updated Pulse Period: {}s'.format(pulse_period))

    log_all_events(spike_safe_socket)

    # space out the log and terminal output for clarity
    log_and_print('')

### start of main program
try:
    log.info("UsingPulseHolds.py started.")

    log.info("Python version: {}".format(sys.version))
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and configure settings to run in Continuous Dynamic mode
    tcp_socket.send_scpi_command('*RST')                  
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP PULSEDDYNAMIC')
    tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(0.1)}')   
    tcp_socket.send_scpi_command('SOUR1:VOLT 20')   
    tcp_socket.send_scpi_command('SOUR1:PULS:CCOM 4')
    tcp_socket.send_scpi_command('SOUR1:PULS:RCOM 4')   
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')

    # initially setting the On and Off Time to their default values using the standard commands 
    # Although not recommended, it is possible to use On Time, Off Time, Pulse Width, Period, and Duty Cycle commands in the same test session
    # If On or Off Time is specified using these standard commands, the Pulse Hold will be ignored
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 0.001')
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 0.009')

    # Check for any errors with initializing commands
    log_all_events(tcp_socket)

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # wait until the channel is fully ramped
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # check for all events and measure readings on Channel 1 once per second for 5 seconds,
    # it is best practice to do this to ensure Channel 1 is on and does not have any errors
    time_end = time.time() + 5                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)

    # set Channel 1's Pulse Hold to Period. Setting any pulse-related setting will not re-calculate Pulse Period
    tcp_socket.send_scpi_command('SOUR1:PULS:HOLD PER')
    log_and_print('Held Pulse Period')

    # set Channel 1's Pulse Width to 8ms. Since Period is being held, the Period will remain at 10ms
    pulse_width_seconds = 0.008
    tcp_socket.send_scpi_command('SOUR1:PULS:WIDT {}'.format(pulse_width_seconds))
    log_and_print('Set Pulse Width to {}s'.format(pulse_width_seconds))

    # verify that the expected updates are made to the pulse settings
    verify_current_pulse_settings(tcp_socket)
    
    # wait two seconds while running with the newly updated settings
    wait(2)

    # set Channel 1's Duty Cycle to 50%. Since Period is being held, the Period will remain at 10ms
    duty_cycle = 50
    tcp_socket.send_scpi_command('SOUR1:PULS:DCYC {}'.format(duty_cycle))
    log_and_print('Set Duty Cycle to {}%'.format(duty_cycle))

    # verify that the expected updates are made to the pulse settings
    verify_current_pulse_settings(tcp_socket)
    
    # wait two seconds while running with the newly updated settings
    wait(2)

    # set Channel 1's Duty Cycle to 0%. Using this alternate command set, the Duty Cycle is able to be set to 0% and 100%
    # Duty Cycle of 0% corresponds to an always-off output, similar to a disabled channel
    duty_cycle = 0
    tcp_socket.send_scpi_command('SOUR1:PULS:DCYC {}'.format(duty_cycle))
    log_and_print('Set Duty Cycle to {}%'.format(duty_cycle))

    # verify that the expected updates are made to the pulse settings
    verify_current_pulse_settings(tcp_socket)
    
    # wait two seconds while running with the newly updated settings
    wait(2)

    # set Channel 1's Duty Cycle to 100%. Using this alternate command set, the Duty Cycle is able to be set to 0% and 100%
    # Duty Cycle of 100% corresponds to an always-on output, similar to a DC mode
    duty_cycle = 100
    tcp_socket.send_scpi_command('SOUR1:PULS:DCYC {}'.format(duty_cycle))
    log_and_print('Set Duty Cycle to {}%'.format(duty_cycle))

    # verify that the expected updates are made to the pulse settings
    verify_current_pulse_settings(tcp_socket)
    
    # wait two seconds while running with the newly updated settings
    wait(2)

    # set Channel 1's Pulse Hold to Pulse Width. Setting any pulse-related setting will not re-calculate Pulse Width
    tcp_socket.send_scpi_command('SOUR1:PULS:HOLD WIDT')
    log_and_print('Held Pulse Width')

    # set Channel 1's Pulse Period to 20ms. Since Pulse Width is being held, the Pulse Width will remain at 10ms
    pulse_period_seconds = 0.02
    tcp_socket.send_scpi_command('SOUR1:PULS:PER {}'.format(pulse_period_seconds))
    log_and_print('Set Pulse Period to {}s'.format(pulse_period_seconds))

    # verify that the expected updates are made to the pulse settings
    verify_current_pulse_settings(tcp_socket)
    
    # wait two seconds while running with the newly updated settings
    wait(2)

    # set Channel 1's Duty Cycle to 25%. Since Pulse Width is being held, the Pulse Width will remain at 10ms
    duty_cycle = 25
    tcp_socket.send_scpi_command('SOUR1:PULS:DCYC {}'.format(duty_cycle))
    log_and_print('Set Duty Cycle to {}%'.format(duty_cycle))

    # verify that the expected updates are made to the pulse settings
    verify_current_pulse_settings(tcp_socket)
    
    # wait two seconds while running with the newly updated settings
    wait(2)

    # set Channel 1's Pulse Hold to Duty Cycle. Setting any pulse-related setting will not re-calculate Duty Cycle
    tcp_socket.send_scpi_command('SOUR1:PULS:HOLD DCYC')
    log_and_print('Held Duty Cycle')

    # set Channel 1's Pulse Period to 200ms. Since Duty Cycle is being held, the Duty Cycle will remain at 25%
    pulse_period_seconds = 0.2
    tcp_socket.send_scpi_command('SOUR1:PULS:PER {}'.format(pulse_period_seconds))
    log_and_print('Set Pulse Period to {}s'.format(pulse_period_seconds))

    # verify that the expected updates are made to the pulse settings
    verify_current_pulse_settings(tcp_socket)
    
    # wait two seconds while running with the newly updated settings
    wait(2)

    # set Channel 1's Pulse Width to 1ms. Since Duty Cycle is being held, the Duty Cycle will remain at 25%
    pulse_width_seconds = 0.001
    tcp_socket.send_scpi_command('SOUR1:PULS:WIDT {}'.format(pulse_width_seconds))
    log_and_print('Set Pulse Width to {}s'.format(pulse_width_seconds))

    # verify that the expected updates are made to the pulse settings
    verify_current_pulse_settings(tcp_socket)
    
    # wait two seconds while running with the newly updated settings
    wait(2)

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    log.info("UsingPulseHolds.py completed.\n")

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


