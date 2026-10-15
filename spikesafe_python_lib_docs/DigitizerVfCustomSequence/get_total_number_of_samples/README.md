# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerVfCustomSequence](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/README.md) | get_total_number_of_samples

## get_total_number_of_samples() -> int

### Definition
Returns the sum of `number_of_samples` across the steps. An empty sequence returns `0`.

### Example
```python
import spikesafe_python

sequence = spikesafe_python.DigitizerVfCustomSequence().parse_sequence("2@100,3@200")
assert sequence.get_total_number_of_samples() == 5
```
