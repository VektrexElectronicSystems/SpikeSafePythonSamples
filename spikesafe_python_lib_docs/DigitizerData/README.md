# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerData](/spikesafe_python_lib_docs/DigitizerData/README.md)

## DigitizerData

### Definition
A class used to store data in a simple accessible object from a digitizer fetch response. 

### Attributes
| Name | Description |
| - | - |
| [sample_number](/spikesafe_python_lib_docs/DigitizerData/sample_number/README.md) | Sample number of the voltage reading. |
| [time_since_start_seconds](/spikesafe_python_lib_docs/DigitizerData/time_since_start_seconds/README.md) | Time since the start of the sampling in seconds. |
| [voltage_reading](/spikesafe_python_lib_docs/DigitizerData/voltage_reading/README.md) | Digitizer voltage reading. |

### Functions
| Name | Description |
| - | - |
| [voltage_reading_volts_formatted_float(self)](/spikesafe_python_lib_docs/DigitizerData/voltage_reading_formatted_float/README.md) | Return the voltage reading formatted to matching hardware decimal places. |
| [voltage_reading_volts_formatted_string(self)](/spikesafe_python_lib_docs/DigitizerData/voltage_reading_formatted_string/README.md) | Return the voltage reading formatted to matching hardware decimal places. |