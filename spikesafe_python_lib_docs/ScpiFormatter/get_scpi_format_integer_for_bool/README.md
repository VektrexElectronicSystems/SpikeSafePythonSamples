# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [ScpiFormatter](/spikesafe_python_lib_docs/ScpiFormatter/README.md) | get_scpi_format_integer_for_bool

## get_scpi_format_integer_for_bool

### Definition
Return the SCPI formatted value for a boolean value.

### Returns
[int](https://docs.python.org/3/library/functions.html#int)  
Return the SCPI formatted value for a boolean value. 1 for True, 0 for False.

### Examples
The following example demonstrates the `get_scpi_format_integer_for_bool()` function. It sends the SpikeSafe PSMU current range auto SCPI command.
```
# set the SpikeSafe Current Range to Auto
set_current_range_auto = True
tcp_socket.send_scpi_command(f'SOUR1:CURR:RANG:AUTO {spikesafe_python.ScpiFormatter.get_scpi_format_integer_for_bool(set_current_range_auto)}') 

```

### Examples In Action