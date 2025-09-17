# Goal: 
# Demonstrate the connect/disconnect switch functionality of the SpikeSafe PSMU while operating in Multi-Pulse mode
# 
# Expectation: 
# Channel 1 will run in Multi-Pulse mode with the switch set to Primary
# While the channel is enabled but not outputting, the switch be set to Auxiliary mode to isolate the source from the DUT
# Once any modifications to the DUTs have completed in Auxiliary mode, the switch will be set to Primary in which the SpikeSafe will output another Multi-Pulse train

import sys
import time
import logging
import spikesafe_python
from tkinter import messagebox     

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
    log.info("ConnectDisconnectSwitchSample.py started.")

    log.info("Python version: {}".format(sys.version))

    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = spikesafe_python.TcpSocket(enable_logging=False)
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state    
    tcp_socket.send_scpi_command('*RST')                  

    # check that the Force Sense Selector Switch is available for this SpikeSafe. We need the switch to run this sequence
    # If switch related SCPI is sent and there is no switch configured, it will result in error "386, Output Switch is not installed"
    tcp_socket.send_scpi_command('OUTP1:CONN:AVAIL?')
    isSwitchAvailable = tcp_socket.read_data()
    if isSwitchAvailable != 'Ch:1':
        raise Exception('Force Sense Selector Switch is not available, and is necessary to run this sequence.')

    # set the Force Sense Selector Switch state to Primary (A) so that the SpikeSafe can output to the DUT
    # the default switch state can be manually adjusted using SCPI, so it is best to send this command even after sending a *RST
    tcp_socket.send_scpi_command('OUTP1:CONN PRI')

    # set Channel 1's settings to operate in Multi-Pulse mode
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP MULTIPULSE')
    set_current = 0.1
    tcp_socket.send_scpi_command(f'SOUR1:CURR {spikesafe_python.Precision.get_precise_current_command_argument(set_current)}')   
    tcp_socket.send_scpi_command(f'SOUR1:VOLT {spikesafe_python.Precision.get_precise_compliance_voltage_command_argument(20)}')
    pulse_on_time = 1   
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TON {spikesafe_python.Precision.get_precise_time_command_argument(pulse_on_time)}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:TOFF {spikesafe_python.Precision.get_precise_time_command_argument(1)}')
    tcp_socket.send_scpi_command('SOUR1:PULS:COUN 3')
    tcp_socket.send_scpi_command('SOUR1:CURR? MAX')
    spikesafe_model_max_current = float(tcp_socket.read_data())
    load_impedance, rise_time = spikesafe_python.Compensation.get_optimum_compensation(spikesafe_model_max_current, set_current, pulse_on_time)
    tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}')
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')   

    # Check for any errors with initializing commands
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # turn on Channel 1
    tcp_socket.send_scpi_command('OUTP1 1')

    # Wait until channel is ready for a trigger command
    spikesafe_python.ReadAllEvents.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # Output 1ms pulse for Channel 1
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # check for all events and measure readings on the channel once per second for 2 seconds,
    # it is best practice to do this to ensure the channel is on and does not have any errors
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)
        spikesafe_python.MemoryTableReadData.log_memory_table_read(tcp_socket)
        spikesafe_python.Threading.wait(1)        

    # check that the Multi Pulse output has ended
    hasMultiPulseEndedString = ''
    while hasMultiPulseEndedString != 'TRUE':
        tcp_socket.send_scpi_command('SOUR1:PULS:END?')
        hasMultiPulseEndedString =  tcp_socket.read_data()
        spikesafe_python.Threading.wait(0.5)

    # set the Force Sense Selector Switch state to Auxiliary to disconnect the SpikeSafe output from the DUT
    # this action can be performed as long as no pulses are actively being outputted from the SpikeSafe. The channel may be enabled
    tcp_socket.send_scpi_command('OUTP1:CONN AUX')

    # Show a message box so any tasks using the Auxiliary source may be performed before adjusting the switch back to Primary
    # The SpikeSafe is not electrically connected to the DUT at this time
    messagebox.showinfo("SpikeSafe Output Disconnected", "Force Sense Selector Switch is in Auxiliary mode, so SpikeSafe is isolated from the DUT. Once DUT modifications are complete, close this window to adjust the switch back to Primary mode and re-connect the SpikeSafe.")

    # set the Force Sense Selector Switch state to Primary (A) so that the SpikeSafe can output to the DUT
    tcp_socket.send_scpi_command('OUTP1:CONN PRI')

    # Output 1ms pulse for Channel 1. Multiple pulses can be outputted while the channel is enabled
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # check for all events and measure readings after the second pulse output
    time_end = time.time() + 2                         
    while time.time() < time_end:                       
        spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)
        spikesafe_python.MemoryTableReadData.log_memory_table_read(tcp_socket)
        spikesafe_python.Threading.wait(1) 

    # check that the Multi Pulse output has ended
    hasMultiPulseEndedString = ''
    while hasMultiPulseEndedString != 'TRUE':
        tcp_socket.send_scpi_command('SOUR1:PULS:END?')
        hasMultiPulseEndedString =  tcp_socket.read_data()
        spikesafe_python.Threading.wait(0.5)

    # turn off all Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    log.info("ConnectDisconnectSwitchSample.py completed.\n")

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