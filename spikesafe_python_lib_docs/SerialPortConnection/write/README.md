# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [SerialPortConnection](/spikesafe_python_lib_docs/SerialPortConnection/README.md) | write(self, command, enable_logging=None)

## write(self, command, enable_logging=None)

### Definition
Writes a command to the Serial Port.

### Parameters
command [string](https://docs.python.org/3/library/string.html)  
Command to write to the Serial Port.

enable_logging [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Whether to enable logging for this command (default is None, which uses the instance's enable_logging setting).

### Raises
[IOError](https://docs.python.org/3/library/exceptions.html#IOError)  
On any error.

### Examples

### Examples In Action