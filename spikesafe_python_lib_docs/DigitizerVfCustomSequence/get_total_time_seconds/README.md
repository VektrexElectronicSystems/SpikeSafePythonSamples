# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerVfCustomSequence](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/README.md) | get_total_time_seconds

## get_total_time_seconds() -> float

### Definition
Returns the sum of each step's sample count multiplied by its aperture, converted
from microseconds to seconds. This is the total sampling aperture duration;
trigger delays, idle time, and communication overhead are not included.

### Example
```python
import spikesafe_python

sequence = spikesafe_python.DigitizerVfCustomSequence().parse_sequence("2@100,3@200")
assert sequence.get_total_time_seconds() == 0.0008
```
