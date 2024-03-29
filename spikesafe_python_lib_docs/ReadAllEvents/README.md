# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [ReadAllEvents](/spikesafe_python_lib_docs/ReadAllEvents/README.md)

## ReadAllEvents

### Definition
Provides a collection of helper functions you can use to check the SpikeSafe event queue.

### Functions
| Name | Description |
| - | - |
| [log_all_events(spike_safe_socket)](/spikesafe_python_lib_docs/ReadAllEvents/log_all_events/README.md) | Reads all SpikeSafe events from event queue and prints them to the log file. |
| [read_all_events(spike_safe_socket, enable_logging = None)](/spikesafe_python_lib_docs/ReadAllEvents/read_all_events/README.md) | Returns an array of all events from the SpikeSafe event queue. |
| [read_until_event(spike_safe_socket, code, enable_logging = None)](/spikesafe_python_lib_docs/ReadAllEvents/read_until_event/README.md) | Returns an array of all events from the SpikeSafe event queue until a specific event is read. |