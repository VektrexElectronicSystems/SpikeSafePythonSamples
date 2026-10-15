# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerVfCustomSequence](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/README.md)

## DigitizerVfCustomSequence

### Definition
Stores and inspects custom digitizer sampling steps locally. Construct with
`DigitizerVfCustomSequence()`. This helper does not send commands to the instrument.

### Attributes
| Name | Type | Description |
| - | - | - |
| sequence_steps | list[DigitizerVfCustomSequenceStep] | Initially empty list of [steps](/spikesafe_python_lib_docs/DigitizerVfCustomSequenceStep/README.md). |

### Methods
| Name | Description |
| - | - |
| [parse_sequence](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/parse_sequence/README.md) | Parses comma-separated `number_of_samples@aperture_in_microseconds` steps. |
| [get_aperture_for_sample_number_in_seconds](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/get_aperture_for_sample_number_in_seconds/README.md) | Returns the aperture in seconds for a **1-based** sample number across all steps. |
| [is_first_sample_in_step](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/is_first_sample_in_step/README.md) | Returns whether the **1-based** sample number is the first sample of a step. |
| [get_total_number_of_samples](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/get_total_number_of_samples/README.md) | Returns the sum of `number_of_samples` across the steps. |
| [get_total_time_seconds](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/get_total_time_seconds/README.md) | Returns the total sampling aperture duration in seconds. |
