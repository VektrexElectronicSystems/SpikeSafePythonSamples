# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [EventData](/spikesafe_python_lib_docs/EventData/README.md)

## EventData

### Definition
A class used to store data in a simple accessible object from a SpikeSafe's event response.

### Attributes
| Name | Description |
| - | - |
| [channel_list](/spikesafe_python_lib_docs/EventData/channel_list/README.md) | Channels affected by event as list of integers. |
| [code](/spikesafe_python_lib_docs/EventData/code/README.md) | Event code. |
| [event](/spikesafe_python_lib_docs/EventData/event/README.md) | Event response. |
| [message](/spikesafe_python_lib_docs/EventData/message/README.md) | Event message. |

### Functions
| Name | Description |
| - | - |
| [parse_event_data(self, event_data)](/spikesafe_python_lib_docs/EventData/parse_event_data/README.md) | Parses SpikeSafe's event response into a simple accessible object. |