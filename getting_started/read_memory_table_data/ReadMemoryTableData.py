# Goal: 
# Connect to a SpikeSafe and read memory table data

import sys
from spikesafe_python.MemoryTableReadData import MemoryTableReadData
from spikesafe_python.TcpSocket import TcpSocket

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### start of main program
try:
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # request SpikeSafe memory table
    tcp_socket.send_scpi_command('MEM:TABL:READ')

    # read SpikeSafe memory table and print SpikeSafe response to terminal
    data = tcp_socket.read_data()                                            
    print(data)

    # parse SpikeSafe memory table
    memory_table_read = MemoryTableReadData().parse_memory_table_read(data)

    # disconnect from SpikeSafe    
    tcp_socket.close_socket()                                                
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)

