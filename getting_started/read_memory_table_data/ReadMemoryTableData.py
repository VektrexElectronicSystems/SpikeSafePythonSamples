# Goal: 
# Connect to a SpikeSafe and read memory table data

import sys
import logging
from spikesafe_python.MemoryTableReadData import MemoryTableReadData
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.SpikeSafeError import SpikeSafeError

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282         

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("ReadMemoryTableData.py started.")
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # request SpikeSafe memory table
    tcp_socket.send_scpi_command('MEM:TABL:READ')

    # read SpikeSafe memory table and print SpikeSafe response to the log file
    data = tcp_socket.read_data()                                            
    log.info(data)

    # parse SpikeSafe memory table
    memory_table_read = MemoryTableReadData().parse_memory_table_read(data)

    # disconnect from SpikeSafe    
    tcp_socket.close_socket()      

    log.info("ReadMemoryTableData.py completed.\n")

except SpikeSafeError as ssErr:
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

