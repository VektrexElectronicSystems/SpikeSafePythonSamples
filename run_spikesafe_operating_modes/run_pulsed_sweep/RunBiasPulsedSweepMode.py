# Goal: 
# Connect to a SpikeSafe and run Bias Pulsed Sweep mode on Channel 1 into an LED, Laser, or electrical component and run two complete Pulsed Sweeps with a non-zero bias current
# 
# Expectation: 
# Channel 1 will run a sweep from 30mA to 210mA, which will take 1 second in total
# A 10mA bias current will run while the channel is running
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
    log.info("RunBiasPulsedSweepMode.py started.")

    log.info("Python version: {}".format(sys.version))
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = spikesafe_python.TcpSocket(enable_logging=False)
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    spikesafe_python.log_all_events(tcp_socket)

    # set Channel 1's pulse mode to Bias Pulsed Sweep and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP BIASPULSEDSWEEP')

    # set Channel 1's Pulsed Sweep parameters to match the test expectation
    tcp_socket.send_scpi_command(f'SOUR1:CURR:STAR {spikesafe_python.get_precise_current_command_argument(0.02)}')
    stop_current = 0.2
    tcp_socket.send_scpi_command(f'SOUR1:CURR:STOP {spikesafe_python.get_precise_current_command_argument(stop_current)}')   
    tcp_socket.send_scpi_command('SOUR1:CURR:STEP 100')   

    # set Channel 1 to output one pulse per step
    tcp_socket.send_scpi_command('SOUR1:PULS:COUN 1')

    # set Channel 1's Bias Current to 10mA
    tcp_socket.send_scpi_command(f'SOUR1:CURR:BIAS {spikesafe_python.get_precise_current_command_argument(0.01)}')   

    # set Channel 1's voltage to 20 V 
    tcp_socket.send_scpi_command(f'SOUR1:VOLT {spikesafe_python.get_precise_compliance_voltage_command_argument(20)}')   

    # set Channel 1's pulse settings for a 1% duty cycle and 1ms Period using the Pulse On Time and Pulse Off Time commands
    pulse_on_time = 0.0001
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {spikesafe_python.get_precise_time_command_argument(0.0001)}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TOFF {spikesafe_python.get_precise_time_command_argument(0.0099)}')

    # set Channel 1's compensation settings
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    tcp_socket.send_scpi_command('SOUR1:CURR? MAX')
    spikesafe_model_max_current = float(tcp_socket.read_data())
    load_impedance, rise_time = spikesafe_python.get_optimum_compensation(spikesafe_model_max_current, stop_current, pulse_on_time)
    tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}')   

    # set Channel 1's Ramp mode to Fast
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')  

    # Check for any errors with initializing commands
    spikesafe_python.log_all_events(tcp_socket)

    # turn on Channel 1. Bias current will be outputted the entire time the channel is running 
    tcp_socket.send_scpi_command('OUTP1 1')

    # Wait until Channel 1 is ready for a trigger command
    spikesafe_python.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # Output pulsed sweep for Channel 1
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # Wait for the Pulsed Sweep to be complete
    spikesafe_python.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.PULSED_SWEEP_COMPLETE) # event 109 is "Pulsed Sweep Complete"

    # Output pulsed sweep for Channel 1. Multiple sweeps can be run while the channel is enabled
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # Wait for the Pulsed Sweep to be complete
    spikesafe_python.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.PULSED_SWEEP_COMPLETE) # event 109 is "Pulsed Sweep Complete"

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    log.info("RunBiasPulsedSweepMode.py completed.\n")

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