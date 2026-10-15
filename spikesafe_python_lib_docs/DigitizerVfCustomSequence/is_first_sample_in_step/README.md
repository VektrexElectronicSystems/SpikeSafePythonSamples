# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerVfCustomSequence](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/README.md) | is_first_sample_in_step

## is_first_sample_in_step(sample_number: int) -> bool

### Definition
Returns whether the **1-based** sample number is the first sample of a step.
For ordinary positive-length steps, sample 1 starts the first step and subsequent
steps start after the preceding steps' sample counts.

### Example
```python
import spikesafe_python

sequence = spikesafe_python.DigitizerVfCustomSequence().parse_sequence("2@100,3@200")
assert sequence.is_first_sample_in_step(3) is True
assert sequence.is_first_sample_in_step(4) is False
```
