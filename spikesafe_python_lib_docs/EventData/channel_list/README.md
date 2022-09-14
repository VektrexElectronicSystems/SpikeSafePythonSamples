# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [EventData](/spikesafe_python_lib_docs/EventData/README.md) | channel_list

## channel_list

### Definition
Channels affected by event as list of integers.

### Attribute Value
[integer array](https://docs.python.org/3/library/array.html)

### Remarks
Errors that affect the entire source may return an empty array.

### Examples
The following example demonstrates the channel_list attribute. It connects to a recently power-cycled SpikeSafe, initiates the request for SpikeSafe Memory Table Read to induce the event `102, External Pause Signal Ended`, sends `SYST:ERR?` to empty the SpikeSafe event queue, and extracts the event info from a EventData object.
```
# instantiate new TcpSocket to connect to SpikeSafe
tcp_socket = TcpSocket()

# connect to SpikeSafe                        
tcp_socket.open_socket(ip_address, port_number)  

# reset to default state and check for all events,
# it is best practice to check for errors after sending each command      
tcp_socket.send_scpi_command('*RST') 

# request SpikeSafe memory table
tcp_socket.send_scpi_command('MEM:TABL:READ')

# read SpikeSafe memory table and print SpikeSafe response to the log file
data = tcp_socket.read_data()   

# event queue list
event_queue = []

# initialize flag to check if event queue is empty 
is_event_queue_empty = False                                                                                                                      

# run as long as there is an event in the SpikeSafe queue
# here it's expected to receive 1 event: 102, External Pause Signal Ended
while is_event_queue_empty == False:
    # request SpikeSafe events and read data 
    tcp_socket.send_scpi_command('SYST:ERR?')                                        
    event_response = tcp_socket.read_data()

    # event queue is empty
    if event_response.startswith('0'):
        is_event_queue_empty = True
    else:
        # add event to event queue
        event_queue.append(event_response)

event_data = []

# convert all events in the SpikeSafe event queue to EventData objects in a new list and print them to the log file
for event in event_queue:
    event_data_response = EventData().parse_event_data(event)
    event_data.append(event_data_response)
    log.info(event_data_response.event)
    log.info(event_data_response.code)
    log.info(event_data_response.message)
    log.info(','.join(map(str, event_data_response.channel_list)))
```

### Examples In Action
[/getting_started/read_all_events/ReadAllEventsManual.py](/getting_started/read_all_events/ReadAllEventsManual.py)