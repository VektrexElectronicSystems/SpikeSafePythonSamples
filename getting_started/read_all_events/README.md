# Reading All SpikeSafe Events
While operating the SpikeSafe, it is necessary to be aware of any events that may occur that may affect SpikeSafe behavior. The SpikeSafe event queue outputs all events and errors that occur during SpikeSafe operation. The event queue is queried using the SPCI standard `SYSTem:ERRor?` query. The event queue is FIFO, meaning that the first event or error to occur will be the first to be outputted when the queue is queried. Once the SpikeSafe returns `0, OK`, there are no new events or errors.

## Purpose
Demonstrate proper usage of the "Check Event Queue" query on the SpikeSafe. During typical operation, the `SYSTem:ERRor?` query should be sent repeatedly until `0, OK` is received. It is good practice to send this query after any other SCPI command is sent to verify that the SpikeSafe is in the correct state. It is also recommended to send the query periodicall while a SpikeSafe channel is running to determine if any events or errors occurs that require action.

When the SpikeSafe returns an event, it will be in the format `<code>, <event_message>`. Each specific event message has an associated event code.

## Expected Output
The SpikeSafe will be repeatedly queried until a `0, OK` response is received. The amount of querying will vary based upon the state of the SpikeSafe prior to running this sequence.

A typical output is shown below:

`SYST:ERR?`

`102, External Paused Signal Stopped`

`SYST:ERR?`

`0, OK`