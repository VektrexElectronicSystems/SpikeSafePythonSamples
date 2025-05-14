import sys
import logging

from spikesafe_python.SpikeSafeError import SpikeSafeError
from spikesafe_python.SpikeSafeInfoParser import parse_spikesafe_info
from spikesafe_python.TcpSocket import TcpSocket

### set these before starting application
ip_address = '10.0.0.231'
port_number = 8282 

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
    log.info("ReadSpikeSafeInfo.py started.")
        
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    tcp_socket.send_scpi_command('*RST') # "*RST" - reset to a known state (does not affect "VOLT" commands)
    spikesafe_info = parse_spikesafe_info(tcp_socket) # parse the SpikeSafe information and print it to the log file
    
    # log the SpikeSafe information. To access an attribute, use the dot operator (e.g., spikesafe_info.idn)
    log.info(vars(spikesafe_info))

    # log the information for each digitizer. To access an attribute, use the dot operator (e.g., digitizer.version)
    for digitizer in spikesafe_info.digitizer_infos:
        log.info(vars(digitizer))

    log.info("ReadSpikeSafeInfo.py completed.") 

except SpikeSafeError as ssErr:
    # print any SpikeSafe-specific error to both the terminal and the log file, then exit the application
    error_message = 'SpikeSafe error: {}\n'.format(ssErr)
    log.error(error_message)
    print(error_message)
except Exception as err:
    # print any general exception to both the terminal and the log file, then exit the application
    error_message = 'Program error: {}\n'.format(err)
    log.error(error_message)       
    print(error_message)
