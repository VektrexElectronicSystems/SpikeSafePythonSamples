import serial
import serial.tools.list_ports as port_list
from time import sleep 

class SerialInterfaceDll(object):

    def __init__(self, port=None, baudrate=38400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0, write_timeout=0, command_delay=0.1):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.command_delay = command_delay

        if port == None:
            ports = list(port_list.comports())
            for p in ports:
                print (p)
                # Choosing COM port from list of available connections 
                if "USB Serial Port" in p[1]:
                    try:
                        self.port = p[0]
                        # Setting up and connecting to device
                        self.ser = serial.Serial(port =     self.port,
                                                baudrate = self.baudrate,
                                                parity =   self.parity,
                                                stopbits = self.stopbits,
                                                bytesize = self.bytesize,
                                                timeout =  self.timeout,
                                                write_timeout = self.write_timeout)
                        if self.ser.is_open:
                            print("\n" + self.port + " has been opened.\n")
                            self.ser.write(b'*IDN? \r\n')
                            sleep(0.1)
                            print(bytes.decode(self.ser.read(256)))
                        else:
                            print("\nDid not connect to " + self.port + "\n")
                        return
                    except:
                        print("Failed to connect to " + p[0])
        else:
            self.ser = serial.Serial(port =     self.port,
                                                baudrate = self.baudrate,
                                                parity =   self.parity,
                                                stopbits = self.stopbits,
                                                bytesize = self.bytesize,
                                                timeout =  self.timeout,
                                                write_timeout = self.write_timeout)
    

    def close(self):
        self.ser.close()
        sleep(self.command_delay)
        if not self.ser.is_open:
            print("\n" + self.port + " has been closed.\n")
        return

    def write_command(self,command):
        response = None
        self.ser.write(str.encode(command) + b'\r\n')
        sleep(self.command_delay)
        response = bytes.decode(self.ser.read(256))
        return(response)

    def isKthBitSet(self, n, k): 
        if n & (1 << (k - 1)): 
            return True
        else: 
            return False 