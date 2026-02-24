# Goal: 
# Connect to a SpikeSafe and run Staircase Sweep mode on Channel 1 into an LED, Laser, or electrical component and run two complete Staircase Sweeps
#
# Expectation: 
# Channel 1 will run a sweep from 20mA to 200mA, which will take 100ms. Expecting a low (<1V) forward voltage

import sys
import logging
import spikesafe_python

### set these before starting application

# SpikeSafe IP address and port number
ip_address: str = '10.0.0.220'
port_number: int = 8282    

start_current_amps: float = 0.02
stop_current_amps: float = 0.2
current_step_count: int = 10  
compliance_voltage_volts: float = 20
step_on_time_milliseconds: int = 1

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
    log.info("RunStaircaseSweepMode.py started.")

    log.info("Python version: {}".format(sys.version))
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = spikesafe_python.TcpSocket(enable_logging=False)
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)
    
    # parse the SpikeSafe information
    spikesafe_info = spikesafe_python.SpikeSafeInfoParser.parse_spikesafe_info(tcp_socket)

    # set Channel 1's pulse mode to Staircase Sweep and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP STAIRCASESWEEP')

    # set Channel 1's Staircase Sweep parameters to match the test expectation
    tcp_socket.send_scpi_command(f'SOUR1:CURR:STA:SWE:STAR {spikesafe_python.Precision.get_precise_current_command_argument(start_current_amps)}')
    tcp_socket.send_scpi_command(f'SOUR1:CURR:STA:SWE:STOP {spikesafe_python.Precision.get_precise_current_command_argument(stop_current_amps)}')   
    tcp_socket.send_scpi_command(f'SOUR1:CURR:STA:SWE:STEP {current_step_count}')  
    tcp_socket.send_scpi_command(f'SOUR1:PULS:STA:SWE:TON {step_on_time_milliseconds}')

    # set Channel 1's voltage
    tcp_socket.send_scpi_command(f'SOUR1:VOLT {spikesafe_python.Precision.get_precise_compliance_voltage_command_argument(compliance_voltage_volts)}')   

    # set Channel 1's compensation settings
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    load_impedance, rise_time = spikesafe_python.Compensation.get_optimum_compensation(spikesafe_info.maximum_set_current, stop_current_amps, step_on_time_milliseconds)
    tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}') 
    
    # set Channel 1's Ramp mode to Fast
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')

    # set Channel 1's External Source Trigger Out to Always
    tcp_socket.send_scpi_command('SOUR1:PULS:TRIG ALWAYS')

    # set Channel 1's External Source Trigger Out to Positive
    tcp_socket.send_scpi_command('OUTP1:TRIG:SLOP POS')

    # set Channel 1's trigger source to Internal (so that the SpikeSafe triggers the Staircase Sweep when the OUTP:TRIG command is sent)
    tcp_socket.send_scpi_command('OUTP1:TRIG:SOUR INT')

    # Check for any errors with initializing commands
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # Wait until Channel 1 is ready for a trigger command
    spikesafe_python.ReadAllEvents.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # Output Staircase Sweep for Channel 1
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # Wait for the Staircase Sweep to be complete
    spikesafe_python.ReadAllEvents.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.STAIRCASE_SWEEP_IS_COMPLETED) # event 127 is "Staircase Sweep is completed"
    
    # Output Staircase Sweep for Channel 1
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # Wait for the Staircase Sweep to be complete
    spikesafe_python.ReadAllEvents.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.STAIRCASE_SWEEP_IS_COMPLETED) # event 127 is "Staircase Sweep is completed"

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')
    
    # wait until the channel is fully discharged
    spikesafe_python.Discharge.wait_for_spikesafe_channel_discharge(
        spikesafe_socket= tcp_socket,
        spikesafe_info=spikesafe_info,
        compliance_voltage=compliance_voltage_volts, 
        channel_number=1)

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    log.info("RunStaircaseSweepMode.py completed.\n")

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