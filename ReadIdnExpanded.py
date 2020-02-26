# Goal: Connect to a SpikeSafe and request module identification
# SCPI Command: *IDN?
# Example Result: Vektrex, SpikeSafe Mini, Rev 2.0.3.18; Ch 1: DSP 2.0.9, CPLD C.2, Last Cal Date: 17 FEB 2020, SN: 12006, HwRev: E1, Model: MINI-PRF-10-10US\n
# Note: Written for expansion to add future commands

import sys
import ReadAllEvents.EventData
from ReadAllEvents.ReadAllEvents import ReadAllEvents
import GetStatus.MemoryTableRead
from GetStatus.MemoryTableReadUtility import ParseMemoryTableRead
import TcpSocket

# set these before starting application
ip_address = '10.0.0.246'   # SpikeSafe IP address
port_number = 8282          # SpikeSafe port number

# start of main program
try:
    tcp_socket = TcpSocket.TcpSocket()              # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket.openSocket(ip_address, port_number)  # connect to SpikeSafe
    tcp_socket.sendScpiCommand('*IDN?')             # request SpikeSafe information
    data = tcp_socket.readData()                    # read SpikeSafe information
    print(data)                                     # print SpikeSafe response to terminal
    event_data = ReadAllEvents(tcp_socket)        # empty SpikeSafe event queue
    for event in event_data:                        # print all SpikeSafe events to terminal
        print(event.event_text)
    tcp_socket.sendScpiCommand('MEM:TABL:READ')     # request SpikeSafe status
    data = tcp_socket.readData()                    # read SpikeSafe status
    print(data)                                     # print SpikeSafe response to terminal
    memory_table_read = ParseMemoryTableRead(data)  # parse SpikeSafe status
    tcp_socket.closeSocket()                        # disconnect from SpikeSafe
except Exception as err:
    print('Program error: {}'.format(err))          # print any error to terminal
    sys.exit(1)                                     # exit application on any error