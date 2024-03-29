# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [SpikeSafeError](/spikesafe_python_lib_docs/SpikeSafeError/README.md) | code

## code

### Definition
Numerical code representing the specific SpikeSafe error

### Attribute Value
[int](https://docs.python.org/3/library/functions.html#int)  

### Examples
The following example demonstrates the code attribute. It sends an invalid command to the SpikeSafe to induce the event `304, Invalid Voltage Setting; SOUR1:VOLT 1`, sends `SYST:ERR?` to empty the SpikeSafe event queue, and extracts the event info from a EventData object to raise a SpikeSafeError.
```
# event queue list
event_queue = []

# initialize flag to check if event queue is empty 
is_event_queue_empty = False                                                                                                                      

# set Channel 1's voltage to an invalid 1 V and check for all events
tcp_socket.send_scpi_command(f'SOUR1:VOLT {get_precise_compliance_voltage_command_argument(40)}')

# initialize flag to check if event queue is empty 
is_event_queue_empty = False                                                                                                                      

# run as long as there is an event in the SpikeSafe queue
# here it's expected to receive 1 event: 304, Invalid Voltage Setting; SOUR1:VOLT 1
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

# convert all events in the SpikeSafe event queue to EventData objects in a new list
for event in event_queue:
    event_data_response = EventData().parse_event_data(event)

    # raise a SpikeSafeError for any event codes 200 and greater that correspond to SpikeSafe Errors. In general, operation should stop for these
    # here it's expected to raise a SpikeSafeError for event: 304, Invalid Voltage Setting; SOUR1:VOLT 1
    if (event_data_response.code > 200):
        raise SpikeSafeError(event_data_response.code, event_data_response.message, event_data_response.channel_list, event_data_response.event)
```

### Examples In Action
[/getting_started/read_all_events/ReadAllEventsManual.py](/getting_started/read_all_events/ReadAllEventsManual.py)