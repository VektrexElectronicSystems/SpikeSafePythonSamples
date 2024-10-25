# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Compensation](/spikesafe_python_lib_docs/Compensation/README.md) | custom_compensation_table_schema

## custom_compensation_table_schema

### Definition
This schema defines the structure of the data required for custom compensation in the system. It is a list of objects, where each object contains details about compensation settings for a specific device. Below are the fields and their descriptions.

### Schema Overview
- Type: [list([])](https://docs.python.org/3/library/stdtypes.html#list) of objects
- Minimum items: 1 (at least one compensation setting is required)

### Object Fields
Each object in the array must contain the following fields:

spikesafe_model_max_current_amps [number](https://json-schema.org/understanding-json-schema/reference/numeric#number)  
- The maximum current supported by the SpikeSafe model in amps.  
- Constraints: The value must be a number greater than or equal to 0.

device_type [string](https://docs.python.org/3/library/string.html)  
- The type of device the compensation setting applies to.

is_default [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values)  
- Indicates whether this is the default compensation setting for the device_type.  
- Constraints: The value must be true for one object per spikesafe_model_max_current_amps and device_type combination.

set_current_amps_start_range [number](https://json-schema.org/understanding-json-schema/reference/numeric#number)  
- The starting range of the current set point in amps.  
- Constraints:
  - The value must be a number greater than or equal to 0.
  - The value must be less than set_current_amps_end_range.

set_current_amps_end_range [number](https://json-schema.org/understanding-json-schema/reference/numeric#number)  
- The ending range of the current set point in amps.  
- Constraints:
  - The value must be a number greater than or equal to 0.
  - The value must be greater than set_current_amps_start_range.

load_impedance [string](https://docs.python.org/3/library/string.html)  
- The impedance load setting for the compensation configuration.  
- Constraints: Must be equal to the name of an enum in [LoadImpedance](/spikesafe_python_lib_docs/SpikeSafeEnums/LoadImpedance/README.md).

rise_time [string](https://docs.python.org/3/library/string.html)  
- The rise time setting for the compensation configuration.  
- Constraints: Must be equal to the name of an enum in [RiseTime](/spikesafe_python_lib_docs/SpikeSafeEnums/RiseTime/README.md).

### Example JSON
Here is an example of a valid JSON object that conforms to the schema:

```
[
  {
    "spikesafe_model_max_current_amps": 0.5,
    "device_type": "laser_red",
    "is_default": true,
    "set_current_amps_start_range": 0,
    "set_current_amps_end_range": 0.0075,
    "load_impedance": "HIGH",
    "rise_time": "FAST"
  },
  {
    "spikesafe_model_max_current_amps": 0.5,
    "device_type": "laser_red",
    "is_default": false,
    "set_current_amps_start_range": 0.0075,
    "set_current_amps_end_range": 0.125,
    "load_impedance": "MEDIUM",
    "rise_time": "FAST"
  } 
  {
    "spikesafe_model_max_current_amps": 0.5,
    "device_type": "laser_red",
    "is_default": false,
    "set_current_amps_start_range": 0.375,
    "set_current_amps_end_range": 0.5,
    "load_impedance": "MEDIUM",
    "rise_time": "FAST"
  }
]
```