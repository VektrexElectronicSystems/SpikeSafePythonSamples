# Goal: 
# Connect to a SpikeSafe and run Pulsed Sweep mode on Channel 1 into an LED
# Measure the emitted light using a Spectrometer
# Graph the results of the light (L), current (I), and voltage (V) measurements
#
# Expectation: 
# Channel 1 will run a sweep from 20mA to 200mA, which will take 100ms. Expecting a low (<1V) forward voltage
# Using external

import os
import sys
import time
import logging
from spikesafe_python.DigitizerDataFetch import wait_for_new_voltage_data
from spikesafe_python.DigitizerDataFetch import fetch_voltage_data
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait     
from spikesafe_python.SpikeSafeError import SpikeSafeError
from CasSpectrometer import CasDll
from matplotlib import pyplot as plt 

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282        

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("LIVSweepExample.py started.")

    ### CAS4 Spectrometer Configuration

    # Implements the external CAS4x64.dll file provided by Instrument Systems to configure a spectrometer for LIV sweep operation

    # instantiate new CasDll to connect to the CAS Spectrometer
    cas_dll = CasDll()

    # creates a CAS4 device context to be used for all following configuration
    deviceId = cas_dll.casCreateDeviceEx(cas_dll.InterfaceTest, 0).rval

    # check for errors on the CAS4
    cas_dll.check_cas4_device_error(deviceId)

    # specify and configure the .INI configuration and .ISC calibration file to initialize the CAS4
    print('Enter .INI configuration file (in current working directory) to be used for CAS operation:')
    ini_file_string = input()
    if ini_file_string.endswith(".ini") == False:
        ini_file_string += ".ini"
    ini_file_path = os.path.join(os.getcwd(), ini_file_string)

    print('Enter .ISC calibration file (in current working directory) to be used for CAS operation:')
    isc_file_string = input()
    if isc_file_string.endswith(".isc") == False:
        isc_file_string += ".isc"
    isc_file_path = os.path.join(os.getcwd(), isc_file_string)

    cas_dll.casSetDeviceParameterString(deviceId, cas_dll.dpidConfigFileName, ini_file_path.encode())
    cas_dll.casSetDeviceParameterString(deviceId, cas_dll.dpidCalibFileName, isc_file_path.encode())

    # initialize the CAS4 using the configuration and calibration files specified by the user
    # check if any error codes result from the initializiation
    cas_dll.check_cas4_error_code(cas_dll.casInitialize(deviceId, cas_dll.InitOnce).rval)

    # set the CAS4 measurement integration time to 10ms to match the Pulsed Sweep parameters
    cas_dll.casSetMeasurementParameter(deviceId, cas_dll.mpidIntegrationTime, 10)

    # set the CAS4 trigger mode to a hardware (i.e. flip-flop) trigger
    cas_dll.casSetMeasurementParameter(deviceId, cas_dll.mpidTriggerSource, cas_dll.trgFlipFlop)

    # set the CAS4 trigger delay time to 5ms to match the Pulsed Sweep parameters
    cas_dll.casSetMeasurementParameter(deviceId, cas_dll.mpidDelayTime, 5)

    ### Start of typical sequence

    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set up Channel 1 for Pulsed Sweep output. To find more explanation, see instrument_examples/run_pulsed_sweep
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP PULSEDSWEEP')
    tcp_socket.send_scpi_command('SOUR1:CURR:STAR 0.02')
    tcp_socket.send_scpi_command('SOUR1:CURR:STOP 0.2')   
    tcp_socket.send_scpi_command('SOUR1:CURR:STEP 25')   
    tcp_socket.send_scpi_command('SOUR1:VOLT 20')   
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 0.02')
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 1') 

    # Check for any errors with SpikeSafe initialization commands
    log_all_events(tcp_socket)

    # set up Digitizer to measure Pulsed Sweep output. To find more explanation, see making_integrated_voltage_measurements/measure_pulsed_sweep_voltage
    tcp_socket.send_scpi_command('VOLT:RANG 100')
    tcp_socket.send_scpi_command('VOLT:APER 12000')
    tcp_socket.send_scpi_command('VOLT:TRIG:DEL 4000')
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')
    tcp_socket.send_scpi_command('VOLT:TRIG:EDGE RISING')
    tcp_socket.send_scpi_command('VOLT:TRIG:COUN 25')
    tcp_socket.send_scpi_command('VOLT:READ:COUN 1')

    # Check for any errors with Digitizer initialization commands
    log_all_events(tcp_socket)

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # start Digitizer measurements. We want the digitizer waiting for triggers before starting the pulsed sweep
    tcp_socket.send_scpi_command('VOLT:INIT')

    # Wait until Channel 1 is ready for a trigger command
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # Output pulsed sweep for Channel 1
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # prepare the CAS Spectrometer for measurement
    # may have to disable AutoRanging using casSetOptionsOnOff (coAutorangeMeasurement = false)

    # initialize the CAS Spectrometer for measurement - will need to perform this once per Pulsed Sweep pulse
    light_readings = []
    light_reading = 0.0
    light_unit = ''
    for measurementNumber in range(1,25):
        cas_dll.casMeasure(deviceId)
        cas_dll.casColorMetric(deviceId)
        cas_dll.casGetPhotInt(deviceId, light_reading, light_unit, 32) #arbitrarily picked 32 for AUnitMaxLen: the maximum number of characters light_unit can hold
        light_readings.append(light_reading)

    # Wait for the Pulsed Sweep to be complete
    read_until_event(tcp_socket, 109) # event 109 is "Pulsed Sweep Complete"

    # wait for the Digitizer measurements to complete. We need to wait for the data acquisition to complete before fetching the data
    wait_for_new_voltage_data(tcp_socket, 0.5)

    # fetch the Digitizer voltage readings
    digitizerData = fetch_voltage_data(tcp_socket)

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    # # Display spectrum graphically with matplotlib - for verification test purposes, not related to LIV sweep
    # plt.figure()
    # plt.title("Spectrum")
    # plt.plot([
    #     cas_dll.casGetData(deviceId, i).rval for i in range(
    #         0,
    #         int(
    #             cas_dll.casGetDeviceParameter(deviceId,
    #                                           cas_dll.dpidPixels).rval - 1))
    # ])
    # plt.show()

    # put the fetched data in a plottable data format
    voltage_readings = []
    current_steps = []
    start_current_mA = 20
    step_size_mA = 7.5 # 7.5mA = Step Size = (StopCurrent - StartCurrent)/(StepCount - 1)
    for dd in digitizerData:
        voltage_readings.append(dd.voltage_reading)
        current_steps.append(start_current_mA + step_size_mA * (dd.sample_number - 1))

    # plot the pulse shape using the fetched voltage readings and the light measurement readings overlaid
    graph, voltage_axis = plt.subplots()

    # configure the voltage data
    voltage_axis.xlabel('Set Current (mA)')
    voltage_axis.ylabel('Voltage (V)')    
    voltage_axis.plot(current_steps, voltage_readings)
    
    #configure the light measurement data
    light_axis = voltage_axis.twinx()
    light_axis.ylabel('Photometric (lm)')
    light_axis.plot(current_steps, light_readings)

    plt.title('LIV Sweep (20mA to 200mA)')
    graph.tight_layout()
    plt.grid()
    plt.show()

    log.info("LIVSweepExample.py completed.\n")

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