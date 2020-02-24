# This is an example program of how to connect to a SpikeSafe, read its information, and read data from it

import socket
import sys

# create a connection via socket
def openSocket(ip_address, port_number):
    global tcp_socket
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket object
        tcp_socket.settimeout(2)                                        # 2 second socket timeout
        tcp_socket.connect((ip_address, port_number))                   # connect to socket
    except Exception as e:
        print('Error connecting to socket at {}: {}'.format(ip_address, e))
        raise

# close a connection via socket
def closeSocket():
    try:
        tcp_socket.close()  # disconnect from socket
    except Exception as e:
        print('Error disconnecting from socket: {}'.format(e))
        raise
    

# send a SCPI command via socket
def sendScpiCommand(scpi_command):
    try:
        scpi_command_str = scpi_command + '\n'           # add \n termination to SCPI command
        scpi_command_byte = scpi_command_str.encode()    # encode SCPI command to byte
        tcp_socket.send(scpi_command_byte)               # send byte to socket
    except Exception as e:
        print('Error sending SCPI command to socket: {}'.format(e))
        raise

# read data via socket
def readData():
    try:
        data_str = tcp_socket.recv(2048)
        return data_str
    except Exception as e:
        print('Error reading data from socket: {}'.format(e))
        raise

# start of main program
try:
    openSocket('10.0.0.240', 8282)  # connect to SpikeSafe
    sendScpiCommand('*IDN?')        # request SpikeSafe information
    data = readData()               # read SpikeSafe information
    print(data)                     # print SpikeSafe response to terminal

    sendScpiCommand('MEM:TABL:READ')
    data = readData()
    print(data)

    closeSocket()                   # disconnect from SpikeSafe
except Exception as e:
    print('Program error: {}'.format(e))
    sys.exit(1)                     # exit application on any error