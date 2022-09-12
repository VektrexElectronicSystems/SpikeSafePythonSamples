# Goal: 
# Use PSMU to supply current to Channel on into a resistor load in DC staircase pattern and measure voltage at each step
# Load the results of sample number, current, voltage, and calculated voltage to a table
# Graph the results of current (I), voltage (V), and calculated voltage (V) measurements. Voltage and calculated voltage can be compared

import sys
import time
import logging
import numpy as np

from decimal import Decimal
from spikesafe_python.DigitizerDataFetch import fetch_voltage_data
from spikesafe_python.DigitizerDataFetch import wait_for_new_voltage_data
from spikesafe_python.MemoryTableReadData import MemoryTableReadData
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.SpikeSafeEvents import SpikeSafeEvents
from spikesafe_python.SpikeSafeError import SpikeSafeError
from spikesafe_python.TcpSocket import TcpSocket
from matplotlib import pyplot as plt 

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282

# stair case parameters
step_count = 10
start_current_A = 0.010
stop_current_A = 0.100
step_size_A = (stop_current_A - start_current_A) / (step_count - 1)
load_ohm_value = 1

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("MeasuringDcStaircaseVoltages.py started.")
        
    # instantiate new TcpSocket to connect to PSMU
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set Channel 1's mode to DC Dynamic mode and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP DCDYNAMIC')
    log_all_events(tcp_socket)

    # set Channel 1's voltage to 10 and check for all events
    tcp_socket.send_scpi_command('SOUR1:VOLT 10')
    log_all_events(tcp_socket)

    # set Channel 1's Auto Range to On and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR:RANG:AUTO 1')
    log_all_events(tcp_socket)

    # set Channel 1's current to start current and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR {}'.format(start_current_A))
    log_all_events(tcp_socket)

    # set Channel 1's Ramp mode to Fast and check for all events
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')
    log_all_events(tcp_socket)

    # start the Channel 1
    tcp_socket.send_scpi_command('OUTP1 ON')

    # wait until Channel 1 is ready
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"
    
    # set Digitizer to abort any measurements
    tcp_socket.send_scpi_command('VOLT:ABOR')
    log_all_events(tcp_socket)

    # set Digitizer Aperture to 10us and check for all events
    tcp_socket.send_scpi_command('VOLT:APER 10')
    log_all_events(tcp_socket)

    # set Digitizer Trigger Count to step count and check for all events
    tcp_socket.send_scpi_command('VOLT:TRIG:COUN {}'.format(step_count))
    log_all_events(tcp_socket)

    # set Digitizer Read Count to 1 and check for all events
    tcp_socket.send_scpi_command('VOLT:READ:COUN 1')
    log_all_events(tcp_socket)

    # set Digitizer Range to 10V and check for all events
    tcp_socket.send_scpi_command('VOLT:RANG 10')
    log_all_events(tcp_socket)

    # set Digitizer SW Trigger and check for all events
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR SOFTWARE')
    log_all_events(tcp_socket)

    # start Digitizer software triggered measurements
    tcp_socket.send_scpi_command('VOLT:INIT:SENDMSG')
    log_all_events(tcp_socket)

    # start DC staircase current supply and voltage measurement per step
    set_current = start_current_A
    currentIncrementFloat = 0.0
    for step in range(0, step_count):
        # step up Channel 1 current to next step
        set_current = round(set_current + currentIncrementFloat, 3)
        cmdStr = "SOUR1:TRIG " + str(set_current)
        # send Set Current command for next step
        tcp_socket.send_scpi_command(cmdStr)
        currentIncrementFloat = step_size_A

        
    # check for all events
    log_all_events(tcp_socket)
    
    # wait for the Digitizer measurements to complete. We need to wait for the data acquisition to complete before fetching the data
    wait_for_new_voltage_data(tcp_socket, 0.5)

    # Fetch Data and check for all events
    digitizer_data = fetch_voltage_data(tcp_socket)
    log_all_events(tcp_socket)

    # disconnect from PSMU    
    tcp_socket.close_socket()      

    # put the fetched data in a plottable data format
    voltage_readings = []
    current_steps = []
    voltage_calculated_readings = []
    voltage_data_log_array = []
    logging.info("Sample Number  |   Current     |       Vf   |    Vf Calculated")
    logging.info("-------------  | ------------- | ---------- | ----------------")
    for dd in digitizer_data:
        voltage_readings.append(dd.voltage_reading)
        current_steps.append(start_current_A + step_size_A * (dd.sample_number - 1))
        voltage_data_log_array.append(dd.voltage_reading)
        voltage_calculated_readings.append((start_current_A + step_size_A * (dd.sample_number - 1))*load_ohm_value)
        current = start_current_A + step_size_A * (dd.sample_number - 1)
        voltage_calculated = (start_current_A + step_size_A * (dd.sample_number - 1))*load_ohm_value
        logging.info('      %s      |      %.3f    |    %.10f   |   %.3f' % (dd.sample_number, current, dd.voltage_reading, voltage_calculated))

    # plot the pulse shape using the fetched voltage readings and the light measurement readings overlaid
    graph, voltage_axis = plt.subplots()

    # configure the voltage data
    voltage_axis.set_xlabel('Set Current (A)')
    voltage_axis.set_ylabel('Voltage (V)', color='tab:red')    
    voltage_axis.plot(current_steps, voltage_readings, color='tab:red')
    
    # configure the calculated voltage data
    voltage_calculated_axis = voltage_axis.twinx()
    voltage_calculated_axis.set_ylabel('Calculated voltage (V)', color='tab:blue')
    voltage_calculated_axis.plot(current_steps, voltage_calculated_readings, color='tab:blue')

    plt.title('Sweep ({}A to {}A)'.format(start_current_A, stop_current_A))
    graph.tight_layout()
    plt.grid()
    plt.show()

    log.info("MeasuringDcStaircaseVoltages.py completed.\n")

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