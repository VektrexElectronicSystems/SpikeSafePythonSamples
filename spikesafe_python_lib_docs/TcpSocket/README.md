# spikesafe-python API Overview | TcpSocket

## TcpSocket

### Definition
A class used to represent a network TCP socket for remote communication to SpikeSafe

### Attributes
| Name | Description |
| - | - |
| [tcp_socket](/spikesafe_python_lib_docs/TcpSocket/tcp_socket/README.md) | TCP/IP socket for remote comuications to SpikeSafe |

### Functions
| Name | Description |
| - | - |
| [close_socket(self)](/spikesafe_python_lib_docs/TcpSocket/close_socket/README.md) | Close a TCP socket for SpikeSafe |
| [open_socket(self, ip_address, port_number)](/spikesafe_python_lib_docs/TcpSocket/open_socket/README.md) | Opens a TCP socket for a SpikeSafe |
| [read_data(self)](/spikesafe_python_lib_docs/TcpSocket/read_data/README.md) | Read data from a SCPI Query sent to a remote SpikeSafe |
| [send_scpi_command(self,scpi_command)](/spikesafe_python_lib_docs/TcpSocket/send_scpi_command/README.md) | Sent a SCPI command to a remote SpikeSafe |