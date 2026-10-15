# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [MemoryTableReadData](/spikesafe_python_lib_docs/MemoryTableReadData/README.md) | log_memory_table_read

## MemoryTableReadData.log_memory_table_read(spike_safe_socket: TcpSocket) -> None

### Definition
Sends `MEM:TABL:READ`, reads the response, and writes the raw response to this
module's logger at INFO level. It does not parse or return a `MemoryTableReadData` object.

### Parameters
`spike_safe_socket`: an open [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)
connection. Returns `None`.

### Remarks
Configure logging to receive INFO messages. To avoid duplicate response logging,
the implementation recommends calling this with the socket's `enable_logging`
set to `False`. The older module-level `log_memory_table_read()` wrapper is deprecated.

### Example
```python
import spikesafe_python

# tcp_socket is an open SpikeSafe TCP connection.
spikesafe_python.MemoryTableReadData.log_memory_table_read(tcp_socket)
```
