# Goal: 
# Connect to a SpikeSafe and run Multi Pulse mode on Channel 1 into an LED, Laser, or electrical component
#
# Expectation: 
# All channels will output a 100mA pulse with a pulse width of 1ms and a Bias Current of 10mA. This will happen 3 times
# After outputting one Multi-Pulse train at 100mA, change the Set Current to 200mA while the channel is enabled and trigger another Multi-Pulse train
# Expecting a low (<1V) forward voltage

import sys
import time
import logging
import spikesafe_python 

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
    log.info("RunMultiPulseMode.py started.")

    log.info("Python version: {}".format(sys.version))
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = spikesafe_python.TcpSocket(enable_logging=False)
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    spikesafe_python.log_all_events(tcp_socket)

    # set Channel 1's pulse mode to Multi Pulse
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP MULTIPULSE')

    # set Channel 1's current to 100 mA
    set_current = 0.1
    tcp_socket.send_scpi_command(f'SOUR1:CURR {spikesafe_python.get_precise_current_command_argument(set_current)}') 

    # set Channel 1's voltage to 20 V 
    tcp_socket.send_scpi_command(f'SOUR1:VOLT {spikesafe_python.get_precise_compliance_voltage_command_argument(20)}')   

    # set Channel 1's Pulse On Time and Pulse Off Time to 1s each
    pulse_on_time = 1
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {spikesafe_python.get_precise_time_command_argument(pulse_on_time)}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TOFF {spikesafe_python.get_precise_time_command_argument(1)}')

    # set Channel 1's Pulse Count to 3. Every trigger will output 3 pulses
    tcp_socket.send_scpi_command('SOUR1:PULS:COUN 3')

    # set Channel 1's compensation settings to their default values
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.send_scpi_command('SOUR1:CURR? MAX')
    spikesafe_model_max_current = float(tcp_socket.read_data())
    load_impedance, rise_time = spikesafe_python.get_optimum_compensation(spikesafe_model_max_current, set_current, pulse_on_time)
    tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}')
       
    # set Channel 1's Ramp mode to Fast
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')  

    # Check for any errors with initializing commands
    spikesafe_python.log_all_events(tcp_socket)

    # turn on Channel 1
    tcp_socket.send_scpi_command('OUTP1 1')

    # Wait until channel is ready for a trigger command
    spikesafe_python.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # Output 1ms pulse for Channel 1
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # check for all events and measure readings on the channel once per second for 2 seconds,
    # it is best practice to do this to ensure the channel is on and does not have any errors
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        spikesafe_python.log_all_events(tcp_socket)
        spikesafe_python.log_memory_table_read(tcp_socket)
        spikesafe_python.wait(1)        

    # check that the Multi Pulse output has ended
    has_multi_pulse_ended = ''
    while has_multi_pulse_ended != 'TRUE':
        tcp_socket.send_scpi_command('SOUR1:PULS:END?')
        has_multi_pulse_ended =  tcp_socket.read_data()
        spikesafe_python.wait(0.5)

    # After the pulsing has ended, set Channel 1's current to 200 mA while the channel is enabled
    tcp_socket.send_scpi_command(f'SOUR1:CURR {spikesafe_python.get_precise_current_command_argument(0.2)}')

    # Output 1ms pulse for Channel 1. Multiple pulses can be outputted while the channel is enabled
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # check for all events and measure readings after the second pulse output
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        spikesafe_python.log_all_events(tcp_socket)
        spikesafe_python.log_memory_table_read(tcp_socket)
        spikesafe_python.wait(1) 

    # check that the Multi Pulse output has ended
    hasMultiPulseEndedString = ''
    while hasMultiPulseEndedString != 'TRUE':
        tcp_socket.send_scpi_command('SOUR1:PULS:END?')
        hasMultiPulseEndedString =  tcp_socket.read_data()
        spikesafe_python.wait(0.5)

    # turn off all Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    log.info("RunMultiPulseMode.py completed.\n")

except spikesafe_python.SpikeSafeError as ssErr:
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
