# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [SerialPortConnection](/spikesafe_python_lib_docs/SerialPortConnection/README.md)

## SerialPortConnection

### Definition
Class to manage a Serial Port connection to a device.

### Attributes
| Name | Description |
| - | - |
| [default_log_level](/spikesafe_python_lib_docs/SerialPortConnection/default_log_level/README.md) | Default Log Level for messages when enable_logging is True. |
| [enable_logging](/spikesafe_python_lib_docs/SerialPortConnection/enable_logging/README.md) | Flag to enable logging. |
| [port](/spikesafe_python_lib_docs/SerialPortConnection/port/README.md) | The serial port object. |
| [port_name](/spikesafe_python_lib_docs/SerialPortConnection/port_name/README.md) | The name of the serial port (e.g., 'COM3'). |
| [terminator](/spikesafe_python_lib_docs/SerialPortConnection/terminator/README.md) | The line terminator for the serial connection. |
| [timeout_milliseconds](/spikesafe_python_lib_docs/SerialPortConnection/enable_logging/README.md) | Timeout in milliseconds for serial port operations. |

### Functions
| Name | Description |
| - | - |
| [connect(self, com_port, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, terminator='\n')](/spikesafe_python_lib_docs/SerialPortConnection/connect//README.md) | Connects to the specified serial port with given parameters. |
| [disconnect(self)](/spikesafe_python_lib_docs/SerialPortConnection//disconnect/README.md) | Disconnects from the serial port. |
| [read_data(self, enable_logging=None)](/spikesafe_python_lib_docs/SerialPortConnection/read_data/README.md) | Reads data from the serial port. |
| [write(self, command, enable_logging=None)](/spikesafe_python_lib_docs/SerialPortConnection/write/README.md) | Writes a command to the serial port. |