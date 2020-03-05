# Goal: Create a reusable TCP socket

import socket

class TcpSocket():
    """
    A class used to represent a TCP socket for remote communication
    to a SpikeSafe.

    ...

    Methods
    -------
    openSocket(self, ip_address, port_number)
        Opens a TCP/IP socket for remote communication to a SpikeSafe
    closeSocket(self)
        Closes TCP/IP socket used for remote communication to a SpikeSafe
    sendScpiCommand(self, scpi_command)
        Sends a SCPI command via TCP/IP socket to a SpikeSafe
    readData(self)
        Reads data reply via TCP/IP socket from a SpikeSafe
    """

    # create a connection via socket
    def openSocket(self, ip_address, port_number):
        """Opens a TCP/IP socket for remote communication to a SpikeSafe

        Parameters
        ----------
        ip_address : str
            IP address of the SpikeSafe (10.0.0.220 to 10.0.0.0.251)
        port_number : str
            Port number of the SpikeSafe (8282 by default)

        Raises
        ------
        Exception
            On any error
        """
        global tcp_socket
        try:
            # create socket with 2 second timeout and connect to SpikeSafe
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          
            tcp_socket.settimeout(2)                                                
            tcp_socket.connect((ip_address, port_number))                           
        except Exception as err:
            # print any error to terminal and raise error to function caller
            print('Error connecting to socket at {}: {}'.format(ip_address, err))   
            raise                                                                   

    # close a connection via socket
    def closeSocket(self):
        try:
            # disconnect from socket
            tcp_socket.close()  
        except Exception as err:
            # print any error to terminal and raise error to function caller
            print('Error disconnecting from socket: {}'.format(err))    
            raise                                                       
        
    # send a SCPI command via socket
    def sendScpiCommand(self, scpi_command):
        try:
            # add \n termination to SCPI command
            # encode SCPI command to type byte, which is the format required by the socket
            # send byte to socket
            scpi_command_str = scpi_command + '\n'                          
            scpi_command_byte = scpi_command_str.encode()                   
            tcp_socket.send(scpi_command_byte)                              
        except Exception as err:
            # print any error to terminal and raise error to function caller
            print('Error sending SCPI command to socket: {}'.format(err))   
            raise                                                           

    # read data via socket
    def readData(self):
        try:
            # read data from socket, which is automatically converted from type byte to type string
            # return data to function calle
            data_str = tcp_socket.recv(2048)                                
            return data_str                                                 
        except Exception as err:
            # print any error to terminal and raise error to function caller
            print('Error reading data from socket: {}'.format(err))         
            raise                                                           