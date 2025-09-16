# Goal: 
# Make 10,000 pulses using software based timing and then shutoff pulsing

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
    log.info("FixedPulseCountUsingSoftwareTimingExample.py started.")

    log.info("Python version: {}".format(sys.version))
        
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = spikesafe_python.TcpSocket(enable_logging=False)
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # set Channel 1's mode to DC Dynamic and check for all events
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP PULSEDDYNAMIC')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # set Channel 1's Trigger Output to Positive and check for all events
    tcp_socket.send_scpi_command('OUTP1:TRIG:SLOP POS')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # set Channel 1's Trigger Output Always and check for all events
    tcp_socket.send_scpi_command('SOUR0:PULS:TRIG ALWAYS')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # set Channel 1's Pulse On Time to 1us and check for all events
    pulse_on_time = 0.000001
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {spikesafe_python.Precision.get_precise_time_command_argument(pulse_on_time)}')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # set Channel 1's Pulse Off Time 9us and check for all events
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TOFF {spikesafe_python.Precision.get_precise_time_command_argument(0.000009)}')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # set Channel 1's Pulse Width adjustment to disabled and check for all events
    tcp_socket.send_scpi_command('SOUR1:PULS:AADJ 0')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # set Channel 1's current to 100mA and check for all events
    set_current = 0.1
    tcp_socket.send_scpi_command(f'SOUR1:CURR {spikesafe_python.Precision.get_precise_current_command_argument(set_current)}')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # set Channel 1's voltage to 20V and check for all events
    tcp_socket.send_scpi_command(f'SOUR1:VOLT {spikesafe_python.Precision.get_precise_compliance_voltage_command_argument(20)}')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # set Channel 1's Auto Range to On and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR:RANG:AUTO 1')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # set Channel 1's Load Impedance and Rise Time, and check for all events
    tcp_socket.send_scpi_command('SOUR1:CURR? MAX')
    spikesafe_model_max_current = float(tcp_socket.read_data())
    load_impedance, rise_time = spikesafe_python.Compensation.get_optimum_compensation(spikesafe_model_max_current, set_current, pulse_on_time)
    tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)
    tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # set Channel 1's Ramp mode to Fast and check for all events
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # Start the channel
    tcp_socket.send_scpi_command('OUTP1 ON')

    # wait until Channel 1 is ready
    spikesafe_python.ReadAllEvents.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # pulsing starts before before getting Channel Ready message
    # wait 30ms for getting ~10000 pulses
    time.sleep(0.030)
    
    # disable Channel
    tcp_socket.send_scpi_command('OUTP1 OFF')
        
    # disconnect from SpikeSafe    
    tcp_socket.close_socket()      

    log.info("FixedPulseCountUsingSoftwareTimingExample.py completed.\n")

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