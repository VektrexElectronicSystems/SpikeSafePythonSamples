# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerVfCustomSequence](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/README.md) | get_aperture_for_sample_number_in_seconds

## get_aperture_for_sample_number_in_seconds(sample_number: int) -> float

### Definition
Returns the aperture in seconds for a **1-based** sample number across all steps.
Raises `IndexError` when the sample number does not correspond to a sample in the
sequence.

### Example
```python
import spikesafe_python

sequence = spikesafe_python.DigitizerVfCustomSequence().parse_sequence("2@100,3@200")
assert sequence.get_aperture_for_sample_number_in_seconds(3) == 0.0002
```
