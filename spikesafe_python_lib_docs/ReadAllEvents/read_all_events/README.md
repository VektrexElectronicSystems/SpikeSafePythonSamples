# spikesafe-python API Overview | ReadAllEvents | read_all_events(spike_safe_socket)

## read_all_events(spike_safe_socket)

### Definition
Returns an array of all events from the SpikeSafe event queue.

### Parameters
spike_safe_socket [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md)  
Socket object used to communicate with SpikeSafe.

### Returns
[EventData array](/spikesafe_python_lib_docs/EventData/README.md)  
All events from SpikeSafe in a list of EventData objects.

### Examples
The following example demonstrates the read_all_events function. It connects to a SpikeSafe and reads all events to empty the SpikeSafe event queue.
```
# instantiate new TcpSocket to connect to SpikeSafe
tcp_socket = TcpSocket()

# connect to SpikeSafe                        
tcp_socket.open_socket(ip_address, port_number)  

# read all events in SpikeSafe event queue, store in list, and print them to the log file
event_data = read_all_events(tcp_socket)          
for event in event_data:                        
    log.info(event.event)
    log.info(event.code)
    log.info(event.message)
    log.info(','.join(map(str, event.channel_list)))
```

### Examples In Action
[/getting_started/read_all_events//ReadAllEventsHelper.py](/getting_started/read_all_events//ReadAllEventsHelper.py)