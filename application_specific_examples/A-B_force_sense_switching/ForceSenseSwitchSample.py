# Goal: Demonstrate the A/B switch functionality of the SpikeSafe SMU while operating in DC mode
# Expectation: Channel 1 will run in DC mode with the switch set to Primary. Afterward the Switch be set to Auxiliary mode, in which another source may operate connected to the SpikeSafe
#               After the Auxiliary source has completed operation, the switch will be set to Primary to operate the SpikeSafe in DC mode again

import sys
import time
from spikesafe_python.data.MemoryTableReadData import log_memory_table_read
from spikesafe_python.utility.spikesafe_utility.ReadAllEvents import log_all_events
from spikesafe_python.utility.spikesafe_utility.TcpSocket import TcpSocket
from spikesafe_python.utility.Threading import wait     
from tkinter import messagebox

### set these before starting application

# SpikeSafe IP address and port number
ip_address = '10.0.0.220'
port_number = 8282          

### start of main program
try:
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = TcpSocket()
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state
    tcp_socket.send_scpi_command('*RST')                  
    log_all_events(tcp_socket)

    # check that the Force Sense Selector Switch is available for this SpikeSafe. We need the switch to run this sequence
    # If switch related SCPI is sent and there is no switch configured, it will result in error "386, Output Switch is not installed"
    tcp_socket.send_scpi_command('OUTP1:CONN:AVAIL?')
    isSwitchAvailable = tcp_socket.read_data()
    if isSwitchAvailable != b'Ch:1\n':
        raise Exception('Force Sense Selector Switch is not available, and is necessary to run this sequence.')

    # set the Force Sense Selector Switch state to Primary (A) so that the SpikeSafe can output to the DUT
    # the default switch state can be manually adjusted using SCPI, so it is best to send this command even after sending a *RST
    tcp_socket.send_scpi_command('OUTP1:CONN PRI')

    # set Channel 1 settings to operate in DC mode
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP DC')    
    tcp_socket.send_scpi_command('SOUR1:CURR:PROT 50')    
    tcp_socket.send_scpi_command('SOUR1:CURR 0.1')        
    tcp_socket.send_scpi_command('SOUR1:VOLT 20')       

    # log all SpikeSafe event after settings are adjusted  
    log_all_events(tcp_socket) 

    # turn on Channel 1
    tcp_socket.send_scpi_command('OUTP1 1')                                        

    # check for all events and measure readings on Channel 1 once per second for 10 seconds
    time_end = time.time() + 10                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)                            
    
    # turn off Channel 1 and check for all events
    # When operating in DC mode, the channel must be turned off before adjusting the switch state
    tcp_socket.send_scpi_command('OUTP1 0')               
    log_all_events(tcp_socket)

    # set the Force Sense Selector Switch state to Auxiliary (B) so that the Auxiliary Source will be routed to the DUT and the SpikeSafe will be disconnected
    tcp_socket.send_scpi_command('OUTP1:CONN AUX')

    # Show a message box so any tasks using the Auxiliary source may be performed before adjusting the switch back to Primary
    # The SpikeSafe is not electrically connected to the DUT at this time
    messagebox.showinfo("Auxiliary Source Active", "Force Sense Selector Switch is in Auxiliary (B) mode. Perform any tests using the auxiliary source, then close this window to adjust the switch back to Primary (A) mode.")

    # set the Force Sense Selector Switch state to Primary (A) so that the SpikeSafe can output to the DUT
    tcp_socket.send_scpi_command('OUTP1:CONN PRI')

    # turn on Channel 1
    tcp_socket.send_scpi_command('OUTP1 1')                                        

    # check for all events and measure readings on Channel 1 once per second for 10 seconds
    time_end = time.time() + 10                         
    while time.time() < time_end:                       
        log_all_events(tcp_socket)
        log_memory_table_read(tcp_socket)
        wait(1)                            
    
    # turn off Channel 1 and check for all events
    tcp_socket.send_scpi_command('OUTP1 0')               
    log_all_events(tcp_socket)

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()                            
except Exception as err:
    # print any error to terminal and exit application
    print('Program error: {}'.format(err))          
    sys.exit(1)