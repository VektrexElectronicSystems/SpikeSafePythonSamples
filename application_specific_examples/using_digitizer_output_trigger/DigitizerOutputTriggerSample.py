# Goal: 
# Demonstrate using the Digitizer Output Trigger as an input trigger to the SpikeSafe or an external instrument
# 
# Expectation: 
# The digitizer will output a trigger signal, the SpikeSafe will run a 3-pulse Multi Pulse sequence, and the voltages will be measured by the Digitizer and graphed

import sys
import time
import logging
from spikesafe_python.Compensation import get_optimum_compensation
from spikesafe_python.DigitizerDataFetch import wait_for_new_voltage_data
from spikesafe_python.DigitizerDataFetch import fetch_voltage_data
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.Precision import get_precise_compliance_voltage_command_argument
from spikesafe_python.Precision import get_precise_current_command_argument
from spikesafe_python.Precision import get_precise_time_command_argument
from spikesafe_python.Precision import get_precise_time_microseconds_command_argument
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.SpikeSafeEvents import SpikeSafeEvents
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait     
from spikesafe_python.SpikeSafeError import SpikeSafeError
from matplotlib import pyplot as plt

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
    log.info("DigitizerOutputTriggerSample.py started.")

    log.info("Python version: {}".format(sys.version))
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket(enable_logging=False)
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,  this will automatically abort digitizer in order get it into a known state. This is good practice when connecting to a SpikeSafe PSMU
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # set up Channel 1 for Multi Pulse output. To find more explanation, see run_spikesafe_operation_modes/run_multi_pulse
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP MULTIPULSE')
    set_current = 0.1
    tcp_socket.send_scpi_command(f'SOUR1:CURR {get_precise_current_command_argument(set_current)}')   
    tcp_socket.send_scpi_command(f'SOUR1:VOLT {get_precise_compliance_voltage_command_argument(20)}')
    pulse_on_time = 1
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {get_precise_time_command_argument(pulse_on_time)}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TOFF {get_precise_time_command_argument(1)}')
    tcp_socket.send_scpi_command('SOUR1:PULS:COUN 3')
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    tcp_socket.send_scpi_command('SOUR1:CURR? MAX')
    spikesafe_model_max_current = float(tcp_socket.read_data())
    load_impedance, rise_time = get_optimum_compensation(spikesafe_model_max_current, set_current, pulse_on_time)
    tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}')
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')  

    # set Channel 1's Input Trigger Source to External so an external trigger signal will start SpikeSafe current output
    tcp_socket.send_scpi_command('OUTP1:TRIG:SOUR EXT')  

    # set Channel 1's Input Trigger Delay to 10µs (the minimum value). The SpikeSafe will output current 10µs after receiving the input trigger signal
    tcp_socket.send_scpi_command('OUTP1:TRIG:DEL 10')  

    # set Channel 1's Input Trigger Polarity to rising. This should match the expected polarity of the trigger signal
    tcp_socket.send_scpi_command('OUTP1:TRIG:POL RISING')   

    # set typical Digitizer settings to match SpikeSafe settings. For more explanation, see making_integrated_voltage_measurements
    tcp_socket.send_scpi_command('VOLT:RANG 10')
    aperture = 400000
    tcp_socket.send_scpi_command(f'VOLT:APER {get_precise_time_microseconds_command_argument(aperture)}')
    hardware_trigger_delay = 200000
    tcp_socket.send_scpi_command(f'VOLT:TRIG:DEL {get_precise_time_microseconds_command_argument(hardware_trigger_delay)}')
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')
    tcp_socket.send_scpi_command('VOLT:TRIG:EDGE RISING')
    hardware_trigger_count = 6
    tcp_socket.send_scpi_command(f'VOLT:TRIG:COUN {hardware_trigger_count}') # two 3-pulse Multi Pulse sequences will output
    reading_count = 1
    tcp_socket.send_scpi_command(f'VOLT:READ:COUN {reading_count}') 

    # set the Digitizer Hardware Trigger polarity to rising
    tcp_socket.send_scpi_command('VOLT:OUTP:TRIG:EDGE RISING')  

    # check all SpikeSafe event since all settings have been sent
    log_all_events(tcp_socket)

    # initialize the digitizer. Measurements will be taken once a current pulse is outputted
    tcp_socket.send_scpi_command('VOLT:INIT')

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # wait until Channel 1 is ready to pulse
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # output the Digitizer hardware output trigger. 10µs after this signal is outputted, the Multi Pulse sequence will start
    tcp_socket.send_scpi_command('VOLT:OUTP:TRIG')

    # check that the Multi Pulse output has ended
    has_multi_pulse_ended = ''
    while has_multi_pulse_ended != 'TRUE':
        tcp_socket.send_scpi_command('SOUR1:PULS:END?')
        has_multi_pulse_ended =  tcp_socket.read_data()
        wait(0.5)

    # output the Digitizer hardware output trigger. As long as the SpikeSafe is ready to pulse, this can be done continuously
    tcp_socket.send_scpi_command('VOLT:OUTP:TRIG')

    # check that the Multi Pulse output has ended
    has_multi_pulse_ended = ''
    while has_multi_pulse_ended != 'TRUE':
        tcp_socket.send_scpi_command('SOUR1:PULS:END?')
        has_multi_pulse_ended =  tcp_socket.read_data()
        wait(0.5)

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

    # plot the pulse shape using the fetched voltage readings
    plt.plot(samples, voltage_readings)
    plt.ylabel('Voltage (V)')
    plt.xlabel('Sample Number (#)')
    plt.title('Digitizer Voltage Readings - two 3-pulse Multi-Pulse outputs')
    plt.axis([0, 7, min(voltage_readings) - 0.1, max(voltage_readings) + 0.1])
    plt.grid()
    plt.show()

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()

    log.info("DigitizerOutputTriggerSample.py completed.\n")

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


