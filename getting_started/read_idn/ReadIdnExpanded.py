# Goal: 
# Connect to a SpikeSafe and request module identification
# 
# SCPI Commands: 
# *IDN?
# VOLT:DIGI:AVAIL?
# VOLT:VER?
# VOLT:DATA:HWRE?
# VOLT:DATA:SNUM?
# VOLT:DATA:CDAT?
# OUTP1:CONN:AVAIL?
# 
# Example Result: 
# Vektrex, SpikeSafe Mini, Rev 2.0.3.18; Ch 1: DSP 2.0.9, CPLD C.2, Last Cal Date: 17 FEB 2020, SN: 12006, HwRev: E1, Model: MINI-PRF-10-10US\n
# TRUE
# 0.9.0
# C
# 50012
# 02 DEC 2020
# ALL


import sys
import logging
from spikesafe_python.TcpSocket import TcpSocket
from spikesafe_python.SpikeSafeError import SpikeSafeError

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

    # request if Digitizer is available (This is only available on PSMU and PSMU HC depending on model)
    tcp_socket.send_scpi_command('VOLT:DIGI:AVAIL?')         

    # read Digitizer information
    data = tcp_socket.read_data()
    log.info("SpikeSafe VOLT:DIGI:AVAIL? Response: {}".format(data))
    if data == "TRUE":        
        tcp_socket.send_scpi_command('VOLT:VER?')             
        digitizer_version = tcp_socket.read_data()
        tcp_socket.send_scpi_command('VOLT:DATA:HWRE?')             
        digitizer_hardware_rev = tcp_socket.read_data()    
        tcp_socket.send_scpi_command('VOLT:DATA:SNUM?')             
        digitizer_serial_number = tcp_socket.read_data()        
        tcp_socket.send_scpi_command('VOLT:DATA:CDAT?')             
        digitizer_calibration_date = tcp_socket.read_data()                        

        log.info("Digitizer Information Response: version={}, HW Rev={}, SN={}, Cal Date={}".format(digitizer_version, digitizer_hardware_rev, digitizer_serial_number, digitizer_calibration_date))

    # request if Force Sense Selector Switch is available (This is only available on PSMU and PSMU HC depending on model)
    tcp_socket.send_scpi_command('OUTP1:CONN:AVAIL?')

    # read Force Sense Selector Switch information
    data = tcp_socket.read_data()
    log.info("SpikeSafe OUTP1:CONN:AVAIL? Response: {}".format(data))

    # disconnect from SpikeSafe
    tcp_socket.close_socket()  

    log.info("ReadIdnExpanded.py completed.\n") 

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

