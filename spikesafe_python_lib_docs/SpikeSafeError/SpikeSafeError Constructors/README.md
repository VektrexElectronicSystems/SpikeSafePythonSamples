# spikesafe-python API Overview | SpikeSafeError | SpikeSafe Error Constructors

## message

### Definition
Initializes a new instance of the SpikeSafeError class.

### Overloads
| Name | Description |
| - | - |
| SpikeSafeError(self, code, message, channel_list, full_error) | Initializes a new instance of the SpikeSafeError class with a specified code, message, channel list, and full error that causes this exception. |

### SpikeSafeError(self, code, message, channel_list, full_error)

#### Remarks
This constructor initializes the Message property of the new instance to a system-supplied message that describes the error, such as "An invalid argument was specified." This message takes into account the current system culture.

The following table shows the initial property values for an instance of SpikeSafeError.

| Attribute | Value |
| - | - |
| channel_list | The localized channel list as an array of integers. Initially set to an empty array. | 
| code | The localized error code integer. |
| full_error  | The localized full error message string. Initially set to None. |
| message | The localized error message string. |

### Examples
TODO. Need to do new getting_started sample showing SYST:ERR? parsed into EventData
```
```

### Examples In Action
TODO. Need to do new getting_started sample showing SYST:ERR? parsed into EventData