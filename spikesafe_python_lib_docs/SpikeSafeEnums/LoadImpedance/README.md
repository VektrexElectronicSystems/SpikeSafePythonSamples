# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [SpikeSafeEnums](/spikesafe_python_lib_docs/SpikeSafeEnums/README.md) | [LoadImpedance](/spikesafe_python_lib_docs/SpikeSafeEnums/LoadImpedance/README.md)

## LoadImpedance [IntEnum](https://docs.python.org/3/library/enum.html#enum.IntEnum)

### Definition
Defines the Load Impedance acceptable values as enumerations.

### Enumerations
| Name | Code |
| - | - |
| VERY_LOW | 4
| LOW | 3
| MEDIUM | 2
| HIGH | 1

### Examples
The following example demonstrates the `LoadImpedance` IntEnum. It sets the compensation settings on the SpikeSafe.
```
# set the load impedance and rise time
tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {LoadImpedance.MEDIUM}')
tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {RiseTime.FAST}') 
```

### Examples In Action
[/application_specific_examples/pulse_tuning/PulseTuningExample.py](/application_specific_examples/pulse_tuning/PulseTuningExample.py)