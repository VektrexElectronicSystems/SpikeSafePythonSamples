# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Discharge](/spikesafe_python_lib_docs/Discharge/README.md)

## Discharge

### Definition
Provides a collection of helper functions you can use to properly discharge the SpikeSafe channel.

### Functions
| Name | Description |
| - | - |
| [Discharge.get_spikesafe_channel_discharge_time(compliance_voltage)](/spikesafe_python_lib_docs/Discharge/Discharge.get_spikesafe_channel_discharge_time/README.md) | Returns the time in seconds to fully discharge the SpikeSafe channel based on the compliance voltage. |
| [Discharge.wait_for_spikesafe_channel_discharge(spike_safe_socket: TcpSocket, spikesafe_info: SpikeSafeInfo, compliance_voltage: float, channel_number: int = 1, enable_logging: bool \| None = None) -> None](/spikesafe_python_lib_docs/Discharge/wait_for_spikesafe_channel_discharge/README.md) | Automatically waits for the SpikeSafe channel to fully discharge based on SpikeSafe capabilities. If the SpikeSafe supports the Discharge Complete query, it will poll the channel until discharge is complete. If not, it will wait for a calculated time based on the compliance voltage. |