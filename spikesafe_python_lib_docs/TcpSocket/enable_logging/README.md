# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md) | enable_logging

## enable_logging

### Definition
Enable Logging on functions called in TcpSocket class.

### Attribute Value
[bool](https://docs.python.org/3/library/stdtypes.html#boolean-values) 

### Examples
The following example demonstrates the enable_logging attribute. It creates a new TcpSocket object, sets the socket to log all SCPI as info messages, connects to a SpikeSafe, and logs all socket and helper function socket activity to the SpikeSafePythonSamples file.
```
### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S',
    handlers=[
        logging.FileHandler("SpikeSafePythonSamples.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

### start of main program
try:
    log.info("LogAllTcpSocketScpi.py started.")
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket(enable_logging=False)

    # set TcpSocket to log all SCPI
    tcp_socket.enable_logging = True

    # set TcpSocket to log all SCPI as info level messages
    tcp_socket.default_log_level = 20

    # connect to SpikeSafe
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')

    # request SpikeSafe memory table
    tcp_socket.send_scpi_command('MEM:TABL:READ')

    # read SpikeSafe memory table and print SpikeSafe response to the log file
    data = tcp_socket.read_data()   

    # read all events in SpikeSafe event queue, store in list, and print them to the log file
    # here it's expected to receive 1 event: 102, External Pause Signal Ended
    event_data = read_all_events(tcp_socket)
```

### Examples In Action
[/getting_started/scpi_logging/LogAllTcpSocketScpi.py](/getting_started/scpi_logging/LogAllTcpSocketScpi.py)