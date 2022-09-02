# spikesafe-python API Overview | SpikeSafeError

## SpikeSafeError

### Definition
Exception raised for SpikeSafe errors returned by the `SYSTem:ERRor?` query

Inheritance [Exception](https://docs.python.org/3/library/exceptions.html#Exception) -> SpikeSafeError

### Attributes
| Name | Description |
| - | - |
| [channel_list](/spikesafe_python_lib_docs/SpikeSafeError/channel_list/README.md) | The full error query response text. |
| [code](/spikesafe_python_lib_docs/SpikeSafeError/code/README.md) | Numerical code representing the specific SpikeSafe error. |
| [message](/spikesafe_python_lib_docs/SpikeSafeError/message/README.md) | Explanation of the SpikeSafe error. |
| [full_error](/spikesafe_python_lib_docs/SpikeSafeError/full_error/README.md) | The full error query response text. |

### Constructors
| Name | Description |
| - | - |
| [SpikeSafeError(self, code, message, channel_list, full_error)](/spikesafe_python_lib_docs/SpikeSafeError/SpikeSafeError%20Constructors/README.md) | Initializes a new instance of the SpikeSafeError class with a specified code, message, channel list, and full error that causes this exception. |