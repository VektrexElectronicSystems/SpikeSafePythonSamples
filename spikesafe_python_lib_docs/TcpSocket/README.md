# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)

## TcpSocket

### Definition
A class used to represent a network TCP socket for remote communication to SpikeSafe.

### Attributes
| Name | Description |
| - | - |
| [default_log_level](/spikesafe_python_lib_docs/TcpSocket/default_log_level/README.md) | Default Log Level for messages when enable_logging is True |
| [enable_logging](/spikesafe_python_lib_docs/TcpSocket/enable_logging/README.md) | Enable Logging on functions called in TcpSocket class |
| [socket_ip_address](/spikesafe_python_lib_docs/TcpSocket/socket_ip_address/README.md) | IP address of for the TCP/IP socket. |
| [tcp_socket](/spikesafe_python_lib_docs/TcpSocket/tcp_socket/README.md) | TCP/IP socket for remote comuications to SpikeSafe. |

### Functions
| Name | Description |
| - | - |
| [close_socket(self)](/spikesafe_python_lib_docs/TcpSocket/close_socket/README.md) | Close a TCP socket for SpikeSafe. |
| [open_socket(self, ip_address, port_number, enable_logging = None)](/spikesafe_python_lib_docs/TcpSocket/open_socket/README.md) | Opens a TCP socket for a SpikeSafe. |
| [read_data(self)](/spikesafe_python_lib_docs/TcpSocket/read_data/README.md) | Read data from a SCPI Query sent to a remote SpikeSafe. |
| [send_scpi_command(self,scpi_command, enable_logging = None)](/spikesafe_python_lib_docs/TcpSocket/send_scpi_command/README.md) | Sent a SCPI command to a remote SpikeSafe. |