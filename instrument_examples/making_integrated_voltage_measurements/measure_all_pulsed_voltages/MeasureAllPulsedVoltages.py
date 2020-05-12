# Goal: Connect to a SpikeSafe and run Pulsed mode into a 10Ω resistor. Take voltage measurements from the pulsed output using the SpikeSafe SMU's integrated Digitizer
# Expectation: Channel 1 will be driven with 100mA with a forward voltage of ~1V during this time

import sys
import time
from spikesafe_python.data.MemoryTableReadData import log_memory_table_read
from spikesafe_python.utility.spikesafe_utility.ReadAllEvents import log_all_events
from spikesafe_python.utility.spikesafe_utility.ReadAllEvents import read_until_event
from spikesafe_python.utility.spikesafe_utility.TcpSocket import TcpSocket
from spikesafe_python.utility.Threading import wait   

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### start of main program
try:
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # abort digitizer in order get it into a known state. This is good practice when connecting to a SpikeSafe SMU
    tcp_socket.send_scpi_command('VOLT:ABOR')

    # set up Channel 1 for pulsed output. To find more explanation, see instrument_examples/run_pulsed
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP PULSED')
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 0.001')
    tcp_socket.send_scpi_command('SOUR1:PULS:TOFF 0.009')
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    tcp_socket.send_scpi_command('SOUR1:PULS:CCOM 4')
    tcp_socket.send_scpi_command('SOUR1:PULS:RCOM 4')
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')  
    tcp_socket.send_scpi_command('SOUR1:CURR 0.1')   
    tcp_socket.send_scpi_command('SOUR1:VOLT 20')

    # set Digitizer voltage range to 10V since we expect to measure voltages significantly less than 10V
    tcp_socket.send_scpi_command('VOLT:RANG 10')

    # set Digitizer aperture for 600µs. Aperture specifies the measurement time, and we want to measure a majority of the pulse's constant current output
    tcp_socket.send_scpi_command('VOLT:APER 600')

    # set Digitizer trigger delay to 200µs. We want to give sufficient delay to omit any overshoot the current pulse may have
    tcp_socket.send_scpi_command('VOLT:TRIG:DEL 200')

    # set Digitizer trigger source to hardware. When set to a hardware trigger, the digitizer waits for a trigger signal from the SpikeSafe to start a measurement
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')

    # set Digitizer trigger edge to rising. The Digitizer will start a measurement after the SpikeSafe's rising pulse edge occurs
    tcp_socket.send_scpi_command('VOLT:TRIG:EDGE RISING')

    # set Digitizer trigger count to 525, the maximum value. 525 rising edges of current pulses will correspond to 525 voltage readings
    tcp_socket.send_scpi_command('VOLT:TRIG:COUN 525')

    # set Digitizer reading count to 1. This is the amount of readings that will be taken when the Digitizer receives its specified trigger signal
    tcp_socket.send_scpi_command('VOLT:READ:COUN 1')

    # check all SpikeSafe event since all settings have been sent
    log_all_events(tcp_socket)

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # wait until Channel 1 is fully ramped before we take any digitizer measurements. We are looking to measure consistent voltage values
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # start Digitizer measurements
    tcp_socket.send_scpi_command('VOLT:INIT')

    # wait for the Digitizer measurements to complete. 
    # We need to wait for the data acquisition to complete before fetching the data. Once "TRUE" is returned, it means the Digitizer is ready to fetch new data
    digitizerHasNewData = ''                       
    while digitizerHasNewData != b'TRUE\n':                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)

        tcp_socket.send_scpi_command('VOLT:NDAT?')
        digitizerHasNewData = tcp_socket.read_data()
        wait(0.5)

    # fetch and print the Digitizer voltage readings
    tcp_socket.send_scpi_command('VOLT:FETC?')
    digitizerData = tcp_socket.read_data()
    print("Digitizer readings: {}".format(digitizerData))

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)


