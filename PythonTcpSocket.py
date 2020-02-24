import socket

ip_address = '10.0.0.240'   # SpikeSafe IP address
port_number = 8282          # SpikeSafe port number

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket object
tcp_socket.connect((ip_address, port_number))                   # connect to SpikeSafe
arg_str = "*IDN?\n"                                             # define SpikeSafe SCPI command as an argument to send in socket
arg_byte = arg_str.encode()                                     # convert argument to type byte, which is the format required by the socket
tcp_socket.send(arg_byte)                                       # send SpikeSafe SCPI command
response = tcp_socket.recv(2048)                                # read SpikeSafe response
print(response)                                                 # print SpikeSafe response to terminal
tcp_socket.close()                                              # disconnect from SpikeSafe