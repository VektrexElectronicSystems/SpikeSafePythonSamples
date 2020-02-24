import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('10.0.0.223', 8282))
argSt = "*IDN?\n"
argByte = argSt.encode()
sock.send(argByte)
idn = sock.recv(2048)
print(idn)
sock.close()