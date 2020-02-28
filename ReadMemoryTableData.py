# Goal: Connect to a SpikeSafe and read memory table data
# SCPI Command: *IDN?
# Example Result: Vektrex, SpikeSafe Mini, Rev 2.0.3.18; Ch 1: DSP 2.0.9, CPLD C.2, Last Cal Date: 17 FEB 2020, SN: 12006, HwRev: E1, Model: MINI-PRF-10-10US\n
# Note: Written for expansion to add future commands

import sys
from Data.MemoryTableReadData import MemoryTableReadData
from Utility.SpikeSafeUtility.TcpSocket import TcpSocket

# set these before starting application
ip_address = '10.0.0.246'   # SpikeSafe IP address
port_number = 8282          # SpikeSafe port number

# start of main program
try:
    tcp_socket = TcpSocket()                                        # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket.openSocket(ip_address, port_number)                  # connect to SpikeSafe
    tcp_socket.sendScpiCommand('MEM:TABL:READ')                     # request SpikeSafe memory table
    data = tcp_socket.readData()                                    # read SpikeSafe memory table
    print(data)                                                     # print SpikeSafe response to terminal
    memory_table_read = MemoryTableReadData().ParseGetStatus(data)  # parse SpikeSafe memory table
    tcp_socket.closeSocket()                                        # disconnect from SpikeSafe
except Exception as err:
    print('Program error: {}'.format(err))                          # print any error to terminal
    sys.exit(1)                                                     # exit application on any error

