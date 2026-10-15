# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerVfCustomSequenceStep](/spikesafe_python_lib_docs/DigitizerVfCustomSequenceStep/README.md)

## DigitizerVfCustomSequenceStep

### Definition
Stores one custom sampling step. Usually created by
[`DigitizerVfCustomSequence.parse_sequence()`](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/parse_sequence/README.md).

### Constructor
`DigitizerVfCustomSequenceStep(step_number: int, number_of_samples: int, aperture_in_microseconds: int)`

### Attributes
| Name | Type | Description |
| - | - | - |
| step_number | int | Step number; the sequence parser assigns numbers starting at 1. |
| number_of_samples | int | Number of samples in the step. |
| aperture_in_microseconds | int | Aperture of each sample, in microseconds. |

The constructor stores the supplied values without instrument range validation.

### Example
```python
import spikesafe_python

step = spikesafe_python.DigitizerVfCustomSequenceStep(1, 2, 100)
assert step.aperture_in_microseconds == 100
```
