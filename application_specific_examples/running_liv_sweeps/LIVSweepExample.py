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
ip_address = '10.0.0.220'
port_number = 8282      

# LIV Sweep SpikeSafe parameters
LIV_start_current_mA = 20
LIV_stop_current_mA = 200
LIV_sweep_step_count = 19

compliance_voltage_V = 20
pulse_on_time_seconds = 0.02
pulse_off_time_seconds = 0.05 # setting too small of an off time may result in missed measurements by the CAS4

# CAS4 measurement settings
CAS4_integration_time_ms = 10
CAS4_trigger_delay_ms = 5

# CAS4 interface mode
CAS4_interface_mode = 3
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
    cas_spectrometer = CasDll()

    # creates a CAS4 device context to be used for all following configuration
    deviceId = cas_spectrometer.casCreateDeviceEx(CAS4_interface_mode, 0).rval

    # connect to the CAS4 interface
    if CAS4_interface_mode != 3:
        deviceInterface = cas_spectrometer.casGetDeviceTypeOption(CAS4_interface_mode, deviceId)
        deviceId = cas_spectrometer.casCreateDeviceEx(CAS4_interface_mode, deviceInterface.rval).rval

    # check for errors on the CAS4
    cas_spectrometer.check_cas4_device_error(deviceId)

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

    cas_spectrometer.casSetDeviceParameterString(deviceId, cas_spectrometer.dpidConfigFileName, ini_file_path.encode())
    cas_spectrometer.casSetDeviceParameterString(deviceId, cas_spectrometer.dpidCalibFileName, isc_file_path.encode())

    # initialize the CAS4 using the configuration and calibration files specified by the user, and check if any errors occur
    cas_spectrometer.check_cas4_error_code(cas_spectrometer.casInitialize(deviceId, cas_spectrometer.InitForced).rval)


    ### CAS4 Configuration

    # turn off CAS4 Autoranging so we can define our own integration time
    cas_spectrometer.casSetOptionsOnOff(deviceId, cas_spectrometer.coAutorangeMeasurement, 0)
    
    # set the CAS4 measurement integration time to 10ms to match the Pulsed Sweep parameters
    cas_spectrometer.casSetMeasurementParameter(deviceId, cas_spectrometer.mpidIntegrationTime, CAS4_trigger_delay_ms)

    # set the CAS4 trigger mode to a hardware (i.e. flip-flop) trigger
    cas_spectrometer.casSetMeasurementParameter(deviceId, cas_spectrometer.mpidTriggerSource, cas_spectrometer.trgFlipFlop)

    # set the CAS4 trigger delay time to 5ms to match the Pulsed Sweep parameters
    cas_spectrometer.casSetMeasurementParameter(deviceId, cas_spectrometer.mpidTriggerDelayTime, CAS4_integration_time_ms)

    # set the CAS4 trigger delay time to 10 seconds
    cas_spectrometer.casSetMeasurementParameter(deviceId, cas_spectrometer.mpidTriggerTimeout, 10000)

    # prepare the CAS4 density filter if necessary
    cas_needs_to_set_density_filter = cas_spectrometer.casGetDeviceParameter(deviceId, cas_spectrometer.dpidNeedDensityFilterChange).rval
    if cas_needs_to_set_density_filter != 0:
        cas_spectrometer.casSetMeasurementParameter(deviceId, cas_spectrometer.mpidDensityFilter, cas_spectrometer.casGetMeasurementParameter(deviceId, cas_spectrometer.mpidNewDensityFilter).rval)

    # perform a dark current measurement on the CAS4 if necessary
    cas_needs_dark_current_measurement = cas_spectrometer.casGetDeviceParameter(deviceId, cas_spectrometer.dpidNeedDarkCurrent).rval
    if cas_needs_dark_current_measurement != 0:
        cas_spectrometer.casSetShutter(deviceId, 1)
        cas_spectrometer.casMeasureDarkCurrent(deviceId)
        cas_spectrometer.casSetShutter(deviceId, 0)
        cas_spectrometer.check_cas4_device_error(deviceId)

    # prepare the CAS4 for measurement and verify that there are no resulting errorss
    cas_spectrometer.check_cas4_error_code(cas_spectrometer.casPerformAction(deviceId, cas_spectrometer.paPrepareMeasurement).rval)


    ### SpikeSafe Connection and Configuration (Start of typical sequence)

    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,    
    tcp_socket.send_scpi_command('*RST')  
    tcp_socket.send_scpi_command('VOLT:ABOR')                
    log_all_events(tcp_socket)

    # set up SpikeSafe Channel 1 for Pulsed Sweep output. To find more explanation, see instrument_examples/run_pulsed_sweep
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP PULSEDSWEEP')
    tcp_socket.send_scpi_command('SOUR1:CURR:STAR {}'.format(float(LIV_start_current_mA) / 1000))
    tcp_socket.send_scpi_command('SOUR1:CURR:STOP {}'.format(float(LIV_stop_current_mA) / 1000))   
    tcp_socket.send_scpi_command('SOUR1:CURR:STEP {}'.format(LIV_sweep_step_count))   
    tcp_socket.send_scpi_command('SOUR1:VOLT {}'.format(compliance_voltage_V))   
    tcp_socket.send_scpi_command('SOUR1:PULS:TON {}'.format(pulse_on_time_seconds))
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF {}'.format(pulse_off_time_seconds)) 

    # Check for any errors with SpikeSafe initialization commands
    log_all_events(tcp_socket)

    # set up SpikeSafe Digitizer to measure Pulsed Sweep output. To find more explanation, see making_integrated_voltage_measurements/measure_pulsed_sweep_voltage
    tcp_socket.send_scpi_command('VOLT:RANG 100')
    tcp_socket.send_scpi_command('VOLT:APER {}'.format(pulse_on_time_seconds * 600000)) # we want to measure 60% of the pulse
    tcp_socket.send_scpi_command('VOLT:TRIG:DEL {}'.format(pulse_on_time_seconds * 200000)) # we want to skip the first 20% of the pulse
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')
    tcp_socket.send_scpi_command('VOLT:TRIG:EDGE RISING')
    tcp_socket.send_scpi_command('VOLT:TRIG:COUN {}'.format(LIV_sweep_step_count))
    tcp_socket.send_scpi_command('VOLT:READ:COUN 1')

    # Check for any errors with Digitizer initialization commands
    log_all_events(tcp_socket)


    ### LIV Sweep Operation

    # turn on SpikeSafe Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # start SpikeSafe Digitizer measurements. We want the digitizer waiting for triggers before starting the pulsed sweep
    tcp_socket.send_scpi_command('VOLT:INIT')

    # Wait until SpikeSafe Channel 1 is ready for a trigger command
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # Output pulsed sweep for Channel 1
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # prepare data objects for CAS4 measurement
    light_readings = []
    light_reading = ctypes.c_double()
    light_unit = ctypes.create_string_buffer(256)

    # obtain CAS4 measurements
    for measurementNumber in range(0, LIV_sweep_step_count):
        # reset the CAS4 trigger signal in preparation for the next measurement 
        cas_spectrometer.casSetDeviceParameter(deviceId, cas_spectrometer.dpidLine1FlipFlop, 0)

        # perform the CAS4 measurement
        cas_spectrometer.casMeasure(deviceId)
        cas_spectrometer.check_cas4_error_code(cas_spectrometer.casColorMetric(deviceId).rval)
        cas_spectrometer.casGetPhotInt(deviceId, ctypes.byref(light_reading), light_unit, ctypes.sizeof(light_unit))
        light_readings.append(light_reading.value)
        cas_spectrometer.check_cas4_device_error(deviceId)

        # Check for any SpikeSafe errors while outputting the Pulsed Sweep
        log_all_events(tcp_socket)

    # wait for the Digitizer measurements to complete. We need to wait for the data acquisition to complete before fetching the data
    wait_for_new_voltage_data(tcp_socket, 0.5)

    # fetch the SpikeSafe Digitizer voltage readings
    digitizerData = fetch_voltage_data(tcp_socket)

    # turn off SpikeSafe Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    # disconnect from the CAS4
    cas_spectrometer.casDoneDevice(deviceId)


    ### Data Graphing

    # put the fetched data in a plottable data format
    voltage_readings = []
    current_steps = []
    step_size_mA = (LIV_stop_current_mA - LIV_start_current_mA) / (LIV_sweep_step_count - 1) # Step Size [in mA] = (StopCurrent - StartCurrent)/(StepCount - 1)
    for dd in digitizerData:
        voltage_readings.append(dd.voltage_reading)
        current_steps.append(LIV_start_current_mA + step_size_mA * (dd.sample_number - 1))

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

    plt.title('LIV Sweep ({}mA to {}mA)'.format(LIV_start_current_mA, LIV_stop_current_mA))
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