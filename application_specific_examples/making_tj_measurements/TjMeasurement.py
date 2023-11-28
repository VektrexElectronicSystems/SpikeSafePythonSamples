# Goal: 
# Make a junction temperature measurement on an LED using the Electrical Test Method specified by the Joint Electron Device Engineering Council
#
# Expectation:
# 1.) A K-factor will be measured by comparing voltages at two controlled temperatures
# 2.) The LED will be heated using its operational current until it reaches a stable operating temperature
# 3.) The SpikeSafe will be run in CDBC mode and the digitizer will make voltage readings at the beginning of an Off Time cycle
# after step 3, readings will be graphed with a logarithmic x-axis

import sys
import time
import logging
import math
import statistics
from spikesafe_python.DigitizerDataFetch import wait_for_new_voltage_data
from spikesafe_python.DigitizerDataFetch import fetch_voltage_data
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.Precision import get_precise_current_command_argument
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.SpikeSafeEvents import SpikeSafeEvents
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait     
from spikesafe_python.SpikeSafeError import SpikeSafeError
from matplotlib import pyplot as plt

def log_and_print_to_console(message_string):
    log.info(message_string.replace('\n',''))
    print(message_string)

def receive_user_input_and_log():
    inputText = input()
    log.info(inputText)
    return inputText

def calculate_Vf0(start_point, end_point, digitizer_data_list):
    # only want to reference the data within the straight line
    straight_line_digitizer_data = []
    for index in range(start_point, end_point):
        straight_line_digitizer_data.append(digitizer_data_list[index])

    sample_list = []
    sqrt_sample_list = []
    voltage_list = []
    for dd in straight_line_digitizer_data:
        sample_list.append(dd.sample_number)
        sqrt_sample_list.append(math.sqrt(dd.sample_number))
        voltage_list.append(dd.voltage_reading)

    # this method uses data from the time square root axis to extrapolate to T=0    
    number_of_data_points = len(straight_line_digitizer_data)
    sqrt_sample_average = statistics.mean(sqrt_sample_list)
    voltage_average = statistics.mean(voltage_list)

    sum_of_samples = sum(sample_list)
    sum_of_point_products = 0.0
    for index in range(0, number_of_data_points):
        sum_of_point_products += sqrt_sample_list[index] * voltage_list[index]

    # We extrapolate Vf0 by using a line-of-best fit 
    line_of_best_fit_slope = (sum_of_point_products / number_of_data_points - sqrt_sample_average * voltage_average) / (sum_of_samples / number_of_data_points - sqrt_sample_average * sqrt_sample_average)
    Vf0 = -1 * (line_of_best_fit_slope * sqrt_sample_average - voltage_average)
    return Vf0

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282 

# The graph zoom offset is used to zoom in or out to better visualize data in the final graph to make it easier to determine Vf(0). Value is in volts
# A value of zero corresponds to a completely zoomed in graph. Increase the value to zoom out. Recommended values are between 0.001 and 0.100
graph_zoom_offset = 0.01

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
    log.info("TjMeasurement.py started.")

    log.info("Python version: {}".format(sys.version))
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events, this will automatically abort digitizer in order get it into a known state. This is good practice when connecting to a SpikeSafe PSMU
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)
    
    # set up Channel 1 for Bias Current output to determine the K-factor
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP BIAS')
    tcp_socket.send_scpi_command(f'SOUR0:CURR:BIAS {get_precise_current_command_argument(0.033)}')
    tcp_socket.send_scpi_command('SOUR1:VOLT 40')
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')  

    log_and_print_to_console('\nConfigured SpikeSafe to Bias Current mode to obtain K-factor. Starting current output.')

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # wait until Channel 1 is ready to pulse
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    log_and_print_to_console('\nMeasurement Current is currently outputting to the DUT.\n\nPress \'Enter\' in the console once temperature has been stabilized at T1, then record V1 and T1.')
    input()
    log_and_print_to_console('Enter T1 (in °C):')
    temperature_one = float(receive_user_input_and_log())
    log_and_print_to_console('Enter V1 (in V):')
    voltage_one = float(receive_user_input_and_log())

    wait(2)

    log_and_print_to_console('\nMeasurement Current is currently outputting to the DUT.\n\nChange the control temperature to T2.\n\nPress \'Enter\' in the console once temperature has been stabilized at T2, then record V2 and T2.')
    input()
    log_and_print_to_console('Enter T2 (in °C):')
    temperature_two = float(receive_user_input_and_log())
    log_and_print_to_console('Enter V2 (in V):')
    voltage_two = float(receive_user_input_and_log())

    k_factor = (voltage_two - voltage_one)/(temperature_two - temperature_one)
    log_and_print_to_console('K-factor: {} V/°C'.format(k_factor))

    # turn off Channel 1 
    tcp_socket.send_scpi_command('OUTP1 0')

    log_and_print_to_console('\nK-factor values obtained. Stopped bias current output. Configuring to perform Electrical Test Method measurement.')

    # set up Channel 1 for CDBC output to make the junction temperature measurement
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP BIASPULSEDDYNAMIC')
    tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(3.5)}')
    tcp_socket.send_scpi_command(f'SOUR0:CURR:BIAS {get_precise_current_command_argument(0.033)}')
    tcp_socket.send_scpi_command('SOUR1:VOLT 40')
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 1')
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 0.001')
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')  

    # set Digitizer settings to take a series of quick measurements during the Off Time of CDBC operation
    tcp_socket.send_scpi_command('VOLT:RANG 100')
    tcp_socket.send_scpi_command('VOLT:APER 2')
    tcp_socket.send_scpi_command('VOLT:TRIG:DEL 0')
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')
    tcp_socket.send_scpi_command('VOLT:TRIG:EDGE FALLING')
    tcp_socket.send_scpi_command('VOLT:TRIG:COUN 1')
    tcp_socket.send_scpi_command('VOLT:READ:COUN 500')

    # check all SpikeSafe event since all settings have been sent
    log_all_events(tcp_socket)

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # wait until Channel 1 is ready to pulse
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    log_and_print_to_console('\nHeating Current is being outputted.\n\nWait until temperature has stabilized, then press \'Enter\' in the console to take voltage measurements.')
    input()

    # initialize the digitizer. Measurements will be taken once a current pulse is outputted
    tcp_socket.send_scpi_command('VOLT:INIT')

    # wait for the Digitizer measurements to complete 
    wait_for_new_voltage_data(tcp_socket, 0.5)

    # fetch the Digitizer voltage readings using VOLT:FETC? query
    digitizerData = []
    digitizerData = fetch_voltage_data(tcp_socket)

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # prepare digitizer voltage data to plot
    samples = []
    voltage_readings = []
    for dd in digitizerData:
        samples.append(dd.sample_number)
        voltage_readings.append(dd.voltage_reading)

    log_and_print_to_console('Voltage readings are graphed above. Determine the x-values at which the graph is linear by hovering the mouse over graph and noting the \'x=\' in the bottom right.\n\nTake note of the starting x-value and the last x-value (maximum = 500) at which the graph is linear. Once these values are written down, close the graph and enter those values in the console.\n')

    # plot the pulse shape using the fetched voltage readings
    plt.plot(samples, voltage_readings)
    plt.ylabel('Voltage (V)')
    plt.xlabel('Sample number after Heating Current output [logarithmic] (#)')
    plt.xscale('log')
    plt.title('Digitizer Voltage Readings - Vf(0) Extrapolation')

    # Setting the axes so all data can be effectively visualized. For the y-axis, graph_zoom_offset = 0.01 by default. 
    # Modify as necessary at the top of this sequence so that Vf(0) can effectively be estimated using this graph
    plt.axis([1, 500, min(voltage_readings) - graph_zoom_offset, digitizerData[-1].voltage_reading + graph_zoom_offset])  

    plt.grid()
    plt.show()

    log_and_print_to_console('Enter the Start sample (of the linear portion of the graph):')
    first_linear_sample = int(float(receive_user_input_and_log()))
    log_and_print_to_console('Enter the End sample (of the linear portion of the graph) [max=500]:')
    last_linear_sample = int(float(receive_user_input_and_log()))

    Vf0 = calculate_Vf0(first_linear_sample, last_linear_sample, digitizerData)
    junction_temperature = temperature_one + ((Vf0 - voltage_one) / k_factor)

    log_and_print_to_console('\nExtrapolated Vf(0) value: {} V'.format(round(Vf0, 4)))
    log_and_print_to_console('Calculated junction temperature (Tj): {} °C\n'.format(round(junction_temperature, 4)))

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()

    log.info("TjMeasurement.py completed.\n")

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
