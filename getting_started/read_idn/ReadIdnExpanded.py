# Goal: 
# Connect to a SpikeSafe and request module identification
# 
# SCPI Command: 
# *IDN?
# 
# Example Result: 
# Vektrex, SpikeSafe Mini, Rev 2.0.3.18; Ch 1: DSP 2.0.9, CPLD C.2, Last Cal Date: 17 FEB 2020, SN: 12006, HwRev: E1, Model: MINI-PRF-10-10US\n

import sys
import logging
from spikesafe_python.TcpSocket import TcpSocket

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### start of main program
try:
    log.info("ReadIdnExpanded.py started.")
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()

    # connect to SpikeSafe
    tcp_socket.open_socket(ip_address, port_number)  
    
    # request SpikeSafe information
    tcp_socket.send_scpi_command('*IDN?')             
    
    # read SpikeSafe information
    data = tcp_socket.read_data()                    
    log.info("SpikeSafe *IDN? Response: {}".format(data))

    # disconnect from SpikeSafe
    tcp_socket.close_socket()  

    log.info("ReadIdnExpanded.py completed.\n") 

except Exception as err:
    # print any error to the log file and exit application
    log.error('Program error: {}'.format(err))          
    sys.exit(1)

