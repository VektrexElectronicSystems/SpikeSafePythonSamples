# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Compensation](/spikesafe_python_lib_docs/Compensation/README.md)

## Compensation

### Definition
Provides a collection of helper functions you can use to help with SpikeSafe compensation settings.

### Functions
| Name | Description |
| - | - |
| [get_custom_compensation(spikesafe_model_max_current_amps, set_current_amps, device_type, custom_compensation_table, pulse_on_time_seconds=None)](/spikesafe_python_lib_docs/Compensation/get_custom_compensation/README.md) | Returns the custom compensation values for a given set_current_amps and device_type based on a custom_compensation_table, and optionally a given pulse on time. |
| [get_optimum_compensation(spikesafe_model_max_current_amps, set_current_amps, pulse_on_time_seconds: None)](/spikesafe_python_lib_docs/Compensation/get_optimum_compensation/README.md) | Returns the optimum compensation for a given set current, and optionally a given pulse on time. |
| [load_custom_compensation_table(file_path)](/spikesafe_python_lib_docs/Compensation/load_custom_compensation_table/README.md) | Returns a custom compensation table from a JSON file. |
| [load_custom_compensation_unique_device_types(custom_compensation_table)](/spikesafe_python_lib_docs/Compensation/load_custom_compensation_unique_device_types/README.md) | Returns the unique device types from a custom compensation table. |

### Schemas
| Name | Description |
| - | - |
| [custom_compensation_table_schema](/spikesafe_python_lib_docs/Compensation/custom_compensation_table_schema/README.md) | This schema defines the structure of the data required for custom compensation in the system. It is a list of objects, where each object contains details about compensation settings for a specific device. Below are the fields and their descriptions. |