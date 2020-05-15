# Goal: Connect to a SpikeSafe and output a Single Pulse into a 10Ω resistor
#       Take voltage measurements throughout that pulse using the SpikeSafe SMU's integrated Digitizer to determine the pulse shape
# Expectation: Channel 1 will be driven with 100mA with a forward voltage of ~1V during this time

import sys
import time
from spikesafe_python.MemoryTableReadData import log_memory_table_read
from spikesafe_python.ReadAllEvents import log_all_events
from spikesafe_python.ReadAllEvents import read_until_event
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.Threading import wait     
from matplotlib import pyplot as plotter

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
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP SINGLEPULSE')
    tcp_socket.send_scpi_command('SOUR1:PULS:TON 0.001')
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    tcp_socket.send_scpi_command('SOUR1:PULS:CCOM 4')
    tcp_socket.send_scpi_command('SOUR1:PULS:RCOM 4')
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST')  
    tcp_socket.send_scpi_command('SOUR1:CURR 0.1')   
    tcp_socket.send_scpi_command('SOUR1:VOLT 20')

    # set Digitizer voltage range to 10V since we expect to measure voltages significantly less than 10V
    tcp_socket.send_scpi_command('VOLT:RANG 10')

    # set Digitizer aperture for 2µs, the minimum value. Aperture specifies the measurement time, and we want to measure incrementally across the current pulse
    tcp_socket.send_scpi_command('VOLT:APER 2')

    # set Digitizer trigger delay to 0µs. We want to take measurements as fast as possible
    tcp_socket.send_scpi_command('VOLT:TRIG:DEL 0')

    # set Digitizer trigger source to hardware. When set to a hardware trigger, the digitizer waits for a trigger signal from the SpikeSafe to start a measurement
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')

    # set Digitizer trigger edge to rising. The Digitizer will start a measurement after the SpikeSafe's rising pulse edge occurs
    tcp_socket.send_scpi_command('VOLT:TRIG:EDGE RISING')

    # set Digitizer trigger count to 1. We are measuring the output of one current pulse
    tcp_socket.send_scpi_command('VOLT:TRIG:COUN 1')

    # set Digitizer reading count to 525, the maximum value. We are measuring a 1ms pulse, and will take 525 measurements 2µs apart from each other
    tcp_socket.send_scpi_command('VOLT:READ:COUN 525')

    # check all SpikeSafe event since all settings have been sent
    log_all_events(tcp_socket)

    # initialize the digitizer. Measurements will be taken once a current pulse is outputted
    tcp_socket.send_scpi_command('VOLT:INIT')

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')

    # wait until Channel 1 is ready to pulse
    read_until_event(tcp_socket, 100) # event 100 is "Channel Ready"

    # output a current pulse for Channel 1
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # wait for the Digitizer measurements to complete 
    # once "TRUE" is returned, it means the Digitizer is ready to fetch new data
    # given the settings, this loop should only iterate once
    digitizerHasNewData = ''                       
    while digitizerHasNewData != b'TRUE\n':                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)

        tcp_socket.send_scpi_command('VOLT:NDAT?')
        digitizerHasNewData = tcp_socket.read_data()
        wait(0.5)

    # fetch the Digitizer voltage readings
    tcp_socket.send_scpi_command('VOLT:FETC?')
    digitizerData = tcp_socket.read_data()

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')

    # put the fetched data in a plottable data format
    voltageReadingStrings = digitizerData.decode(sys.stdout.encoding).split(",")
    voltageReadings = []
    sampleNumbers = []
    sample = 1
    for v in voltageReadingStrings:
        voltageReadings.append(float(v))
        sampleNumbers.append(sample)
        sample += 1

    # plot the pulse shape using the fetched voltage readings
    plotter.plot(sampleNumbers, voltageReadings)
    plotter.ylabel('Voltage (V)')
    plotter.xlabel('Sample Number')
    plotter.title('Digitizer Voltage Readings - 1ms 100mA Pulse')
    plotter.grid()
    plotter.show()

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)

