# Goal: 
# Connect to a SpikeSafe and request module identification
# 
# SCPI Command:
# *IDN?
# 
# Example Result: 
# Vektrex, SpikeSafe Mini, Rev 2.0.3.18; Ch 1: DSP 2.0.9, CPLD C.2, Last Cal Date: 17 FEB 2020, SN: 12006, HwRev: E1, Model: MINI-PRF-10-10US\n

import sys
import socket
import logging

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S',
    handlers=[
        logging.FileHandler("SpikeSafePythonSamples.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

### start of main program
# create socket object
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2 second socket timeout
tcp_socket.settimeout(2)                                        

try:
    log.info("TcpSample.py started.")
    
    # connect to SpikeSafe
    tcp_socket.connect((ip_address, port_number))

    # define SpikeSafe SCPI command with line feed \n as an argument to send from socket   
    arg_str = "*IDN?\n"

    # convert argument to type byte, which is the format required by the socket                             
    arg_byte = arg_str.encode()

    # send SpikeSafe SCPI command                     
    tcp_socket.send(arg_byte)

    # read SpikeSafe response and print it to the log file                       
    response = tcp_socket.recv(2048)               
    log.info(response)                                 
except socket.timeout as err:
    log.error(err)
except socket.error as err:
    log.error(err)
except Exception as err:
    log.error(err)
finally:
    # disconnect from SpikeSafe
    tcp_socket.close()   

    log.info("TcpSample.py completed.\n")
