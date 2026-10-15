# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [DigitizerVfCustomSequence](/spikesafe_python_lib_docs/DigitizerVfCustomSequence/README.md) | parse_sequence

## parse_sequence(sequence: str) -> DigitizerVfCustomSequence

### Definition
Parses comma-separated `number_of_samples@aperture_in_microseconds` steps.
Both fields are integers. Clears the previous steps and returns the same sequence
object. Entries without exactly two `@`-separated fields or with invalid integers
are skipped. Parsed steps are numbered from 1; no instrument range validation is
performed by this helper.

### Example
```python
import spikesafe_python

sequence = spikesafe_python.DigitizerVfCustomSequence().parse_sequence("2@100,3@200")
sequence.parse_sequence("2@100,3@200")
assert sequence.get_total_number_of_samples() == 5
```
