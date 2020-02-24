# Goal: Connect to a SpikeSafe and request module identification
# SCPI Command: *IDN?
# Example Result: Vektrex, SpikeSafe Mini, Rev 2.0.3.18; Ch 1: DSP 2.0.9, CPLD C.2, Last Cal Date: 17 FEB 2020, SN: 12006, HwRev: E1, Model: MINI-PRF-10-10US\n
# Note: Written for simplicity

import socket

ip_address = '10.0.0.240'   # SpikeSafe IP address
port_number = 8282          # SpikeSafe port number

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket object
tcp_socket.settimeout(5)

try:
    tcp_socket.connect((ip_address, port_number))                   # connect to SpikeSafe
    arg_str = "*IDN?\n"                                             # define SpikeSafe SCPI command with line feed /n as an argument to send from socket
    arg_byte = arg_str.encode()                                     # convert argument to type byte, which is the format required by the socket
    tcp_socket.send(arg_byte)                                       # send SpikeSafe SCPI command
    response = tcp_socket.recv(2048)                                # read SpikeSafe response
    print(response)                                                 # print SpikeSafe response to terminal
except socket.timeout as err:
    print(err)
except socket.error as err:
    print(err)
finally:
    tcp_socket.close()                                              # disconnect from SpikeSafe