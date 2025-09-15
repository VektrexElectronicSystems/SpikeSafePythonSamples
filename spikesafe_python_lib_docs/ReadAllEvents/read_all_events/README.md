# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [ReadAllEvents](/spikesafe_python_lib_docs/ReadAllEvents/README.md) | spikesafe_python.read_all_events(spike_safe_socket, enable_logging = None)

## spikesafe_python.read_all_events(spike_safe_socket, enable_logging = None)

### Definition
Returns an array of all events from the SpikeSafe event queue.

### Parameters
spike_safe_socket [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)  
Socket object used to communicate with SpikeSafe.

enable_logging [bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) [optional](https://docs.python.org/3/library/typing.html#typing.Optional)  
Overrides spike_safe_socket.enable_logging attribute (None by default, will use spike_safe_socket.enable_logging value).

### Returns
[EventData array](/spikesafe_python_lib_docs/EventData/README.md)  
All events from SpikeSafe in a list of EventData objects.

### Examples
The following example demonstrates the spikesafe_python.read_all_events function. It connects to a SpikeSafe and reads all events to empty the SpikeSafe event queue.
```
# instantiate new TcpSocket to connect to SpikeSafe
tcp_socket = spikesafe_python.TcpSocket(enable_logging=False)

# connect to SpikeSafe                        
tcp_socket.open_socket(ip_address, port_number)  

# read all events in SpikeSafe event queue, store in list, and print them to the log file
event_data = spikesafe_python.read_all_events(tcp_socket)          
for event in event_data:                        
    log.info(event.event)
    log.info(event.code)
    log.info(event.message)
    log.info(','.join(map(str, event.channel_list)))
```

### Examples In Action
[/getting_started/spikesafe_python.read_all_events//ReadAllEventsHelper.py](/getting_started/spikesafe_python.read_all_events//ReadAllEventsHelper.py)