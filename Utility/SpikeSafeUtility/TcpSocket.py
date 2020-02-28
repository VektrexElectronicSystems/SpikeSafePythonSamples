# Goal: Create a reusable TCP socket

import socket

class TcpSocket():

    # create a connection via socket
    def openSocket(self, ip_address, port_number):
        global tcp_socket
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          # create socket object
            tcp_socket.settimeout(2)                                                # 2 second socket timeout
            tcp_socket.connect((ip_address, port_number))                           # connect to socket
        except Exception as err:
            print('Error connecting to socket at {}: {}'.format(ip_address, err))   # print any error to terminal
            raise                                                                   # raise error to function caller

    # close a connection via socket
    def closeSocket(self):
        try:
            tcp_socket.close()  # disconnect from socket
        except Exception as err:
            print('Error disconnecting from socket: {}'.format(err))    # print any error to terminal
            raise                                                       # raise error to function caller
        
    # send a SCPI command via socket
    def sendScpiCommand(self, scpi_command):
        try:
            scpi_command_str = scpi_command + '\n'                          # add \n termination to SCPI command
            scpi_command_byte = scpi_command_str.encode()                   # encode SCPI command to type byte, which is the format required by the socket
            tcp_socket.send(scpi_command_byte)                              # send byte to socket
        except Exception as err:
            print('Error sending SCPI command to socket: {}'.format(err))   # print any error to terminal
            raise                                                           # raise error to function caller

    # read data via socket
    def readData(self):
        try:
            data_str = tcp_socket.recv(2048)                                # read data from socket, which is automatically converted from type byte to type string
            return data_str                                                 # return data to function caller
        except Exception as err:
            print('Error reading data from socket: {}'.format(err))         # print any error to terminal
            raise                                                           # raise error to function caller