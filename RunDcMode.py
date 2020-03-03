# Goal: Connect to a SpikeSafe and run DC mode into a shorting plug for 60 seconds
# Expectation: Channel 1 will be driven with 100mA with a forward voltage of ~100mV during this time

import sys
import time
from Data.MemoryTableReadData import MemoryTableReadData
from Utility.SpikeSafeUtility.ReadAllEvents import ReadAllEvents
from Utility.SpikeSafeUtility.TcpSocket import TcpSocket

def logAllEvents(tcp_socket):
    event_data = ReadAllEvents(tcp_socket)  # read all events in SpikeSafe event queue and store in list
    for event in event_data:                # print all SpikeSafe events to terminal
        print(event.event)

def logMemoryTableRead(tcp_socket):
    tcp_socket.sendScpiCommand('MEM:TABL:READ') # request SpikeSafe memory table
    data = tcp_socket.readData()                # read SpikeSafe memory table
    print(data)

# set these before starting application
ip_address = '10.0.0.246'   # SpikeSafe IP address
port_number = 8282          # SpikeSafe port number

# start of main program
try:
    tcp_socket = TcpSocket()                            # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket.openSocket(ip_address, port_number)      # connect to SpikeSafe
    tcp_socket.sendScpiCommand('*RST')                  # reset to default state
    logAllEvents(tcp_socket)                            # check for all events
    tcp_socket.sendScpiCommand('SOUR1:FUNC:SHAP DC')    # set Channel 1's pulse mode to DC
    logAllEvents(tcp_socket)                            # check for argument and limit errors from setting Channel 1's pulse mode. It is best practice to check for errors after sending each command
    tcp_socket.sendScpiCommand('SOUR1:CURR:PROT 50')    # set Channel 1's safety threshold for over current protection to 50%
    logAllEvents(tcp_socket)                            # check for all events
    tcp_socket.sendScpiCommand('SOUR1:CURR 0.1')        # set Channel 1's current to 100 mA
    logAllEvents(tcp_socket)                            # check for all events
    tcp_socket.sendScpiCommand('SOUR1:VOLT 10')         # set Channel 1's voltage to 10 V
    logAllEvents(tcp_socket)                            # check for all events
    tcp_socket.sendScpiCommand('OUTP1 1')               # turn on Channel 1
    logAllEvents(tcp_socket)                            # check for all events

    time_end = time.time() + 60                         # check for all events and measure readings on Channel 1 once per second for 60 seconds
    while time.time() < time_end:                       # it is best practice to do this to ensure Channel 1 is on and does not have any errors
        logAllEvents(tcp_socket)
        logMemoryTableRead(tcp_socket)
        time.sleep(1)                                   
    
    tcp_socket.sendScpiCommand('OUTP1 0')               # turn off Channel 1
    logAllEvents(tcp_socket)                            # check for all errors
    logMemoryTableRead(tcp_socket)                      # check Channel 1 is off
    tcp_socket.closeSocket()                            # disconnect from SpikeSafe
except Exception as err:
    print('Program error: {}'.format(err))              # print any error to terminal
    sys.exit(1)                                         # exit application on any error