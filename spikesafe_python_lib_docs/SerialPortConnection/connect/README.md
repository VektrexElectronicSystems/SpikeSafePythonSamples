# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [SerialPortConnection](/spikesafe_python_lib_docs/SerialPortConnection/README.md) | connect(self, com_port, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, terminator='\n')

## connect(self, com_port, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, terminator='\n')

### Definition
Opens a TCP socket for a SpikeSafe.

### Parameters
com_port [string](https://docs.python.org/3/library/string.html)  
COM port of the SpikeSafe (e.g., 'COM3')

baudrate [int](https://docs.python.org/3/library/functions.html#int) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Baud rate for the serial connection (default is 9600)

parity [string](https://docs.python.org/3/library/string.html) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Parity for the serial connection (default is serial.PARITY_NONE)

stopbits [int](https://docs.python.org/3/library/functions.html#int) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Stop bits for the serial connection (default is serial.STOPBITS_ONE)

bytesize [int](https://docs.python.org/3/library/functions.html#int) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Byte size for the serial connection (default is serial.EIGHTBITS)

terminator [string](https://docs.python.org/3/library/string.html) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Line terminator for the serial connection (default is '\n')

### Raises
[IOError](https://docs.python.org/3/library/exceptions.html#IOError)  
On any error.

### Examples

### Examples In Action