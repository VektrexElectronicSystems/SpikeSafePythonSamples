# Goal: Connect to a SpikeSafe and request module identification
# SCPI Command: *IDN?
# Example Result: Vektrex, SpikeSafe Mini, Rev 2.0.3.18; Ch 1: DSP 2.0.9, CPLD C.2, Last Cal Date: 17 FEB 2020, SN: 12006, HwRev: E1, Model: MINI-PRF-10-10US\n

import sys
from Utility.SpikeSafeUtility.TcpSocket import TcpSocket

# set these before starting application
ip_address = '10.0.0.246'   # SpikeSafe IP address
port_number = 8282          # SpikeSafe port number

# start of main program
try:
    tcp_socket = TcpSocket()                        # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket.openSocket(ip_address, port_number)  # connect to SpikeSafe
    tcp_socket.sendScpiCommand('*IDN?')             # request SpikeSafe information
    data = tcp_socket.readData()                    # read SpikeSafe information
    tcp_socket.closeSocket()                        # disconnect from SpikeSafe
except Exception as err:
    print('Program error: {}'.format(err))          # print any error to terminal
    sys.exit(1)                                     # exit application on any error

