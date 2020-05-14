# Goal: 
# Connect to a SpikeSafe and request module identification
# 
# SCPI Command:
# *IDN?
# 
# Example Result: 
# Vektrex, SpikeSafe Mini, Rev 2.0.3.18; Ch 1: DSP 2.0.9, CPLD C.2, Last Cal Date: 17 FEB 2020, SN: 12006, HwRev: E1, Model: MINI-PRF-10-10US\n

import socket

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### start of main program
# create socket object
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2 second socket timeout
tcp_socket.settimeout(2)                                        

try:
    # connect to SpikeSafe
    tcp_socket.connect((ip_address, port_number))

    # define SpikeSafe SCPI command with line feed \n as an argument to send from socket   
    arg_str = "*IDN?\n"

    # convert argument to type byte, which is the format required by the socket                             
    arg_byte = arg_str.encode()

    # send SpikeSafe SCPI command                     
    tcp_socket.send(arg_byte)

    # read SpikeSafe response and print it                       
    response = tcp_socket.recv(2048)               
    print(response)                                 
except socket.timeout as err:
    print(err)
except socket.error as err:
    print(err)
except Exception as err:
    print(err)
finally:
    # disconnect from SpikeSafe
    tcp_socket.close()                              