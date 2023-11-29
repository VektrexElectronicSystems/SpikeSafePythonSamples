# Goal: 
# Connect to a SpikeSafe and run a Pulsed Sweep into a 10Ω resistor. Take voltage measurements from the pulsed output using the SpikeSafe PSMU's integrated Digitizer
# 
# Expectation: 
# Channel 1 will be driven with 100mA with a forward voltage of ~1V during this time

import sys
import time
import logging
from spikesafe_python.DigitizerDataFetch import wait_for_new_voltage_data
from spikesafe_python.DigitizerDataFetch import fetch_voltage_data
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.Precision import get_precise_compliance_voltage_command_argument
from spikesafe_python.Precision import get_precise_current_command_argument
from spikesafe_python.Precision import get_precise_time_command_argument
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
    log.info("MeasurePulsedSweepVoltage.py started.")

    log.info("Python version: {}".format(sys.version))
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,  this will automatically abort digitizer in order get it into a known state. This is good practice when connecting to a SpikeSafe PSMU
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)
    
    # set up Channel 1 for pulsed sweep output. To find more explanation, see instrument_examples/run_spikesafe_operating_modes/run_pulsed
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP PULSEDSWEEP')
    tcp_socket.send_scpi_command(f'SOUR1:CURR:STAR {get_precise_current_command_argument(0.02)}')
    tcp_socket.send_scpi_command(f'SOUR1:CURR:STOP {get_precise_current_command_argument(0.2)}')   
    tcp_socket.send_scpi_command(f'SOUR1:CURR:STEP 100')    
    tcp_socket.send_scpi_command(f'SOUR1:VOLT {get_precise_compliance_voltage_command_argument(20)}')   
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {get_precise_time_command_argument(0.0001)}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TOFF {get_precise_time_command_argument(0.0099)}')
    tcp_socket.send_scpi_command('SOUR1:PULS:CCOM 4')
    tcp_socket.send_scpi_command('SOUR1:PULS:RCOM 4')  
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST') 

    # set Digitizer voltage range to 10V since we expect to measure voltages significantly less than 10V
    tcp_socket.send_scpi_command('VOLT:RANG 10')

    # set Digitizer aperture for 60µs. Aperture specifies the measurement time, and we want to measure a majority of the pulse's constant current output
    tcp_socket.send_scpi_command('VOLT:APER 60')

    # set Digitizer trigger delay to 20µs. We want to give sufficient delay to omit any overshoot the current pulse may have
    tcp_socket.send_scpi_command('VOLT:TRIG:DEL 20')

    # set Digitizer trigger source to hardware. When set to a hardware trigger, the digitizer waits for a trigger signal from the SpikeSafe to start a measurement
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')

    # set Digitizer trigger edge to rising. The Digitizer will start a measurement after the SpikeSafe's rising pulse edge occurs
    tcp_socket.send_scpi_command('VOLT:TRIG:EDGE RISING')

    # set Digitizer trigger count to 100. We want to take one voltage reading for every step in the pulsed sweep
    tcp_socket.send_scpi_command('VOLT:TRIG:COUN 100')

    # set Digitizer reading count to 1. This is the amount of readings that will be taken when the Digitizer receives its specified trigger signal
    tcp_socket.send_scpi_command('VOLT:READ:COUN 1')

    # check all SpikeSafe event since all settings have been sent
    log_all_events(tcp_socket)

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # wait until Channel 1 is fully ramped so we can send a trigger command for a pulsed sweep
    read_until_event(tcp_socket, SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # start Digitizer measurements. We want the digitizer waiting for triggers before starting the pulsed sweep
    tcp_socket.send_scpi_command('VOLT:INIT')

    # trigger Channel 1 to start the pulsed sweep output
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # wait for the Digitizer measurements to complete. We need to wait for the data acquisition to complete before fetching the data
    wait_for_new_voltage_data(tcp_socket, 0.5)

    # fetch the Digitizer voltage readings
    digitizerData = fetch_voltage_data(tcp_socket)

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # put the fetched data in a plottable data format
    voltage_readings = []
    current_steps = []
    start_current_mA = 20
    step_size_mA = 1.82 # 1.82mA = Step Size = (StopCurrent - StartCurrent)/(StepCount - 1)
    for dd in digitizerData:
        voltage_readings.append(dd.voltage_reading)
        current_steps.append(start_current_mA + step_size_mA * (dd.sample_number - 1))


    # plot the pulse shape using the fetched voltage readings
    plt.plot(current_steps, voltage_readings)
    plt.ylabel('Voltage (V)')
    plt.xlabel('Set Current (mA)')
    plt.title('Digitizer Voltage Readings - Pulsed Sweep (20mA to 200mA)')
    plt.grid()
    plt.show()

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    log.info("MeasurePulsedSweepVoltage.py completed.\n")

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


