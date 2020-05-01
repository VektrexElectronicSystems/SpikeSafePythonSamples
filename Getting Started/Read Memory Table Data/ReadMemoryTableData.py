# Goal: Connect to a SpikeSafe and read memory table data

import sys
from spikesafe_python.data.MemoryTableReadData import MemoryTableReadData
from spikesafe_python.utility.spikesafe_utility.TcpSocket import TcpSocket

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.246'
port_number = 8282          

### start of main program
try:
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.openSocket(ip_address, port_number)

    # request SpikeSafe memory table
    tcp_socket.sendScpiCommand('MEM:TABL:READ')

    # read SpikeSafe memory table and print SpikeSafe response to terminal
    data = tcp_socket.readData()                                            
    print(data)

    # parse SpikeSafe memory table
    memory_table_read = MemoryTableReadData().ParseMemoryTableRead(data)

    # disconnect from SpikeSafe    
    tcp_socket.closeSocket()                                                
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)
