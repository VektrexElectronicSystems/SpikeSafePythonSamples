# Goal: Connect to a SpikeSafe and request module identification
# SCPI Command: *IDN?
# Example Result: Vektrex, SpikeSafe Mini, Rev 2.0.3.18; Ch 1: DSP 2.0.9, CPLD C.2, Last Cal Date: 17 FEB 2020, SN: 12006, HwRev: E1, Model: MINI-PRF-10-10US\n

import sys
from Utility.SpikeSafeUtility.TcpSocket import TcpSocket

### set these before starting application

# SpikeSafe IP address
ip_address = '10.0.0.246'

# SpikeSafe port number   
port_number = 8282          

### start of main program
try:
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()

    # connect to SpikeSafe
    tcp_socket.openSocket(ip_address, port_number)  
    
    # request SpikeSafe information
    tcp_socket.sendScpiCommand('*IDN?')             
    
    # read SpikeSafe information
    data = tcp_socket.readData()                    
    
    # disconnect from SpikeSafe
    tcp_socket.closeSocket()                        
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)

