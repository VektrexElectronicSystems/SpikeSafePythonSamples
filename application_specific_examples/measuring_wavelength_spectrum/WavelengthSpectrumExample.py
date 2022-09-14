# Goal: 
# Connect to a SpikeSafe and run DC Dynamic mode on Channel 1 into an LED
# Measure the emitted light using a Spectrometer
#
# Expectation: 
# Channel 1 will output 100mA DC current. Expecting a low (<1V) forward voltage
# Using external CAS DLL, control the spectrometer to make light measurements and then graph the wavelength spectrum

import sys
import time
import logging
import os
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.SpikeSafeEvents import SpikeSafeEvents
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait     
from spikesafe_python.SpikeSafeError import SpikeSafeError
from CasSpectrometer import CasDll
from matplotlib import pyplot as plt 

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282         

# SpikeSafe Single Pulse current settings
set_current_amps = 0.1
compliance_voltage_V = 20

# CAS4 measurement settings
CAS4_integration_time_ms = 20
CAS4_trigger_delay_ms = 5 # needs to be set to a non-zero value for the spectrometer to correctly output data

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
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("WavelengthSpectrumExample.py started.")
    
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

    # reset the CAS4 trigger signal in preparation for the measurement 
    cas_spectrometer.casSetDeviceParameter(deviceId, cas_spectrometer.dpidLine1FlipFlop, 0)

    ### SpikeSafe Connection and Configuration (Start of typical sequence)

    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset SpikeSafe to default state and check for all events    
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set SpikeSafe Channel 1's pulse mode to Single Pulse and set all relevant settings. For more information, see run_spikesafe_operating_modes/run_dc
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP SINGLEPULSE')
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 1')    
    tcp_socket.send_scpi_command('SOUR1:CURR {}'.format(set_current_amps))        
    tcp_socket.send_scpi_command('SOUR1:VOLT {}'.format(compliance_voltage_V))         
    log_all_events(tcp_socket) 

    # turn on SpikeSafe Channel 1 and check for all events
    tcp_socket.send_scpi_command('OUTP1 1')               
    log_all_events(tcp_socket)                            

    # wait until the channel is fully ramped and output a single pulse
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"
    tcp_socket.send_scpi_command('OUTP1:TRIG')   

    # take a CAS4 measurement
    cas_spectrometer.casMeasure(deviceId)
    cas_spectrometer.check_cas4_device_error(deviceId)

    # determine the number of visible pixels to be measured by the CAS4
    visible_pixels = int(cas_spectrometer.casGetDeviceParameter(deviceId, cas_spectrometer.dpidVisiblePixels).rval)
    cas_spectrometer.check_cas4_error_code(visible_pixels)

    # prepare data objects for CAS4 measurement
    spectrum = []
    wavelengths = []

    # determine the number of dead pixels to be ignored by the CAS4
    dead_pixels = int(cas_spectrometer.casGetDeviceParameter(deviceId, cas_spectrometer.dpidDeadPixels).rval)
    cas_spectrometer.check_cas4_error_code(dead_pixels)

    # measure the spectrum and associate wavelengths using the CAS4. Ignore dead pixels
    for pixel in range(0, visible_pixels):
        spectrum.append(cas_spectrometer.casGetData(deviceId, pixel + dead_pixels).rval)
        wavelengths.append(cas_spectrometer.casGetXArray(deviceId, pixel + dead_pixels).rval)

    # turn off SpikeSafe Channel 1 and check for all events
    tcp_socket.send_scpi_command('OUTP1 0')               
    log_all_events(tcp_socket)

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()     

    # disconnect from the CAS4
    cas_spectrometer.casDoneDevice(deviceId)


    ### Plot the wavelength spectrum
    spectral_intensity = []
    spectrum_max = max(spectrum)

    if spectrum_max == 0:
        raise Exception("Full spectrum was measured as 0.0 mW/nm")

    for point in spectrum:
        spectral_intensity.append((point/spectrum_max) * 100)
    
    plt.plot(wavelengths, spectral_intensity)
    plt.ylabel('Spectral Intensity (%)')
    plt.xlabel('Wavelength (nm)')
    plt.axis([min(wavelengths), max(wavelengths), min(spectral_intensity), 100])
    plt.grid()
    plt.show()

    log.info("WavelengthSpectrumExample.py completed.\n")

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