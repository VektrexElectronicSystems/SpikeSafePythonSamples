# Goal: 
# Connect to a SpikeSafe and run Pulsed Sweep mode on Channel 1 into an LED
# Measure the emitted light using a Spectrometer
# Graph the results of the light (L), current (I), and voltage (V) measurements
#
# Expectation: 
# Channel 1 will run a sweep from 20mA to 200mA, which will take 100ms. Expecting a low (<1V) forward voltage
# Using external CAS DLL, control the spectrometer to make light measurements throughout the Pulsed Sweep

import os
import sys
import time
import logging
import ctypes
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
ip_address = '10.0.0.221'
port_number = 8282      

# number of steps in the LIV Sweep
LIV_sweep_step_count = 4

# CAS4 interface mode
CAS4_interface_mode = 5
"""
    CAS4_interface_mode: int
    - 1: PCI
    - 3: Demo (No hardware)
    - 5: USB
    - 10: PCIe
    - 11: Ethernet
"""

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("LIVSweepExample.py started.")

    ### CAS4 Spectrometer Connection/Initialization

    # Implements the external CAS4x64.dll file provided by Instrument Systems to configure a spectrometer for LIV sweep operation

    # instantiate new CasDll to connect to the CAS Spectrometer
    cas_dll = CasDll()

    # creates a CAS4 device context to be used for all following configuration
    deviceId = cas_dll.casCreateDeviceEx(cas_dll.InterfaceUSB, 0).rval
    deviceInterface = cas_dll.casGetDeviceTypeOption(cas_dll.InterfaceUSB, deviceId)
    deviceId = cas_dll.casCreateDeviceEx(cas_dll.InterfaceUSB, deviceInterface.rval).rval

    # check for errors on the CAS4
    cas_dll.check_cas4_device_error(deviceId)

    liv_sweeps_folder = "application_specific_examples\\running_liv_sweeps"

    # specify and configure the .INI configuration and .ISC calibration file to initialize the CAS4
    print('Enter .INI configuration file (must be located in SpikeSafePythonSamples\\application_specific_examples\\running_liv_sweeps) to be used for CAS operation:')
    ini_file_string = input()
    if ini_file_string.endswith(".ini") == False:
        ini_file_string += ".ini"
    ini_file_path = os.path.join(os.getcwd(), liv_sweeps_folder, ini_file_string)

    print('Enter .ISC calibration file (must be located in SpikeSafePythonSamples\\application_specific_examples\\running_liv_sweeps) to be used for CAS operation:')
    isc_file_string = input()
    if isc_file_string.endswith(".isc") == False:
        isc_file_string += ".isc"
    isc_file_path = os.path.join(os.getcwd(), liv_sweeps_folder, isc_file_string)

    cas_dll.casSetDeviceParameterString(deviceId, cas_dll.dpidConfigFileName, ini_file_path.encode())
    cas_dll.casSetDeviceParameterString(deviceId, cas_dll.dpidCalibFileName, isc_file_path.encode())

    # initialize the CAS4 using the configuration and calibration files specified by the user, and check if any errors occur
    cas_dll.check_cas4_error_code(cas_dll.casInitialize(deviceId, cas_dll.InitForced).rval)


    ### CAS4 Configuration

    # set the CAS4 measurement integration time to 10ms to match the Pulsed Sweep parameters
    cas_dll.casSetMeasurementParameter(deviceId, cas_dll.mpidIntegrationTime, 10)

    # set the CAS4 trigger mode to a hardware (i.e. flip-flop) trigger
    cas_dll.casSetMeasurementParameter(deviceId, cas_dll.mpidTriggerSource, cas_dll.trgFlipFlop)

    # set the CAS4 trigger delay time to 5ms to match the Pulsed Sweep parameters
    cas_dll.casSetMeasurementParameter(deviceId, cas_dll.mpidTriggerDelayTime, 5)

    # set the CAS4 trigger delay time to 10 seconds
    cas_dll.casSetMeasurementParameter(deviceId, cas_dll.mpidTriggerTimeout, 10000)

    # prepare the CAS Spectrometer for measurement
    cas_dll.casSetOptionsOnOff(deviceId, cas_dll.coAutorangeMeasurement, 0)
    
    cas_needs_to_set_density_filter = cas_dll.casGetDeviceParameter(deviceId, cas_dll.dpidNeedDensityFilterChange).rval
    if cas_needs_to_set_density_filter != 0:
        cas_dll.casSetMeasurementParameter(deviceId, cas_dll.mpidDensityFilter, cas_dll.casGetMeasurementParameter(deviceId, cas_dll.mpidNewDensityFilter))

    cas_needs_dark_current_measurement = cas_dll.casGetDeviceParameter(deviceId, cas_dll.dpidNeedDarkCurrent).rval
    if cas_needs_dark_current_measurement != 0:
        cas_dll.casSetShutter(deviceId, 1)
        cas_dll.casMeasureDarkCurrent(deviceId)
        cas_dll.casSetShutter(deviceId, 0)
        cas_dll.check_cas4_device_error(deviceId)

    cas_dll.check_cas4_error_code(cas_dll.casPerformAction(deviceId, cas_dll.paPrepareMeasurement).rval)


    ### SpikeSafe Connection and Configuration (Start of typical sequence)

    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')  
    tcp_socket.send_scpi_command('VOLT:ABOR')                
    log_all_events(tcp_socket)

    # set up Channel 1 for Pulsed Sweep output. To find more explanation, see instrument_examples/run_pulsed_sweep
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP PULSEDSWEEP')
    tcp_socket.send_scpi_command('SOUR1:CURR:STAR 0.01')
    tcp_socket.send_scpi_command('SOUR1:CURR:STOP 0.1')   
    tcp_socket.send_scpi_command('SOUR1:CURR:STEP {}'.format(LIV_sweep_step_count))   
    tcp_socket.send_scpi_command('SOUR1:VOLT 20')   
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 0.02')
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 8') 

    # Check for any errors with SpikeSafe initialization commands
    log_all_events(tcp_socket)

    # set up Digitizer to measure Pulsed Sweep output. To find more explanation, see making_integrated_voltage_measurements/measure_pulsed_sweep_voltage
    tcp_socket.send_scpi_command('VOLT:RANG 100')
    tcp_socket.send_scpi_command('VOLT:APER 12000')
    tcp_socket.send_scpi_command('VOLT:TRIG:DEL 4000')
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')
    tcp_socket.send_scpi_command('VOLT:TRIG:EDGE RISING')
    tcp_socket.send_scpi_command('VOLT:TRIG:COUN {}'.format(LIV_sweep_step_count))
    tcp_socket.send_scpi_command('VOLT:READ:COUN 1')

    # Check for any errors with Digitizer initialization commands
    log_all_events(tcp_socket)


    ### LIV Sweep Operation

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # start Digitizer measurements. We want the digitizer waiting for triggers before starting the pulsed sweep
    tcp_socket.send_scpi_command('VOLT:INIT')

    # Wait until Channel 1 is ready for a trigger command
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # Output pulsed sweep for Channel 1
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # prepare data objects for CAS Spectrometer measurement
    light_readings = []
    light_reading = ctypes.c_double()
    light_unit = ctypes.create_string_buffer(256)

    # obtain CAS Spectrometer measurements
    for measurementNumber in range(0,LIV_sweep_step_count):
        start_time = time.time()

        # reset the CAS4 trigger signal in preparation for the next measurement 
        cas_dll.casSetDeviceParameter(deviceId, cas_dll.dpidLine1FlipFlop, 0)

        # perform the CAS4 measurement
        cas_dll.casMeasure(deviceId)
        cas_dll.check_cas4_error_code(cas_dll.casColorMetric(deviceId).rval)
        cas_dll.casGetPhotInt(deviceId, ctypes.byref(light_reading), light_unit, ctypes.sizeof(light_unit))
        light_readings.append(light_reading.value)
        cas_dll.check_cas4_device_error(deviceId)

        # Check for any SpikeSafe errors while outputting the Pulsed Sweep
        log_all_events(tcp_socket)

        measurement_duration = time.time() - start_time
        duration_string = "measurement time: {}".format(measurement_duration)
        print(duration_string)
        log.info(duration_string)
        # wait(0.5)

    # wait for the Digitizer measurements to complete. We need to wait for the data acquisition to complete before fetching the data
    wait_for_new_voltage_data(tcp_socket, 0.5)

    # fetch the Digitizer voltage readings
    digitizerData = fetch_voltage_data(tcp_socket)

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    # disconnect from the CAS4
    cas_dll.casDoneDevice(deviceId)


    ### Data Graphing

    # put the fetched data in a plottable data format
    voltage_readings = []
    current_steps = []
    start_current_mA = 20
    step_size_mA = 180 / (LIV_sweep_step_count - 1) # Step Size [in mA] = (StopCurrent - StartCurrent)/(StepCount - 1)
    for dd in digitizerData:
        voltage_readings.append(dd.voltage_reading)
        current_steps.append(start_current_mA + step_size_mA * (dd.sample_number - 1))

    # plot the pulse shape using the fetched voltage readings and the light measurement readings overlaid
    graph, voltage_axis = plt.subplots()

    # configure the voltage data
    voltage_axis.set_xlabel('Set Current (mA)')
    voltage_axis.set_ylabel('Voltage (V)', color='tab:red')    
    voltage_axis.plot(current_steps, voltage_readings, color='tab:red')
    
    #configure the light measurement data
    light_axis = voltage_axis.twinx()
    light_axis.set_ylabel('Photometric (lm)', color='tab:blue')
    light_axis.plot(current_steps, light_readings, color='tab:blue')

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