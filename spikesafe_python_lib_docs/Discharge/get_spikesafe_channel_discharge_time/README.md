# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md) | [Discharge](/spikesafe_python_lib_docs/Discharge/README.md) | def spikesafe_python.get_spikesafe_channel_discharge_time(compliance_voltage)

## spikesafe_python.get_spikesafe_channel_discharge_time(compliance_voltage)

### Definition
Returns the time to fully discharge the SpikeSafe channel based on the compliance voltage.

### Parameters
compliance_voltage [float](https://docs.python.org/3/library/functions.html#float)  
Compliance voltage to factor in discharge time

### Returns
[float](https://docs.python.org/3/library/functions.html#float)    
Discharge time in seconds

### Examples
The following example demonstrates the `spikesafe_python.get_spikesafe_channel_discharge_time()` function. It checks for the time to fully discharge the SpikeSafe channel based on the compliance voltage, and waits for that period until restarting the channel.
```
# set Channel 1's pulse mode to Modulated DC
tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP MODULATED')    

# set Channel 1's current to 200 mA. This will be the output current when a sequence step specifies "@100"
tcp_socket.send_scpi_command(f'SOUR1:CURR {spikesafe_python.get_precise_current_command_argument(0.2)}')       

# set Channel 1's voltage to 20 V
compliance_voltage = 20
tcp_socket.send_scpi_command(f'SOUR1:VOLT {spikesafe_python.get_precise_compliance_voltage_command_argument(compliance_voltage)}') 

# set Channel 1's modulated sequence to a DC staircase with 5 steps
# There are 5 current steps that each last for 1 second: 40mA, 80mA, 120mA, 160mA, and 200mA
tcp_socket.send_scpi_command('SOUR1:SEQ 1(1@20,1@40,1@60,1@80,1@100)') 

# Log all events since all settings are sent
spikesafe_python.log_all_events(tcp_socket) 

# turn on Channel 1
tcp_socket.send_scpi_command('OUTP1 1')                                         

# Wait until channel is ready for a trigger command
spikesafe_python.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

# Output modulated sequence
tcp_socket.send_scpi_command('OUTP1:TRIG')

# Wait until channel has completed it modulated sequence
spikesafe_python.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.MODULATED_SEQ_IS_COMPLETED) # event 105 is "Modulated SEQ completed"

# turn off Channel 1
tcp_socket.send_scpi_command('OUTP1 0')
wait_time = spikesafe_python.get_spikesafe_channel_discharge_time(compliance_voltage)
spikesafe_python.wait(wait_time)      

# set Channel 1's modulated sequence to an infinite pulsing pattern. This pulsing pattern will repeatedly perform 3 steps:
# 1.) it will pulse Off for 250ms, then On for 250ms at 120mA. This will happen twice
# 2.) it will pulse Off for 500ms, then On for 500ms at 60mA. This will also happen twice 
# 3.) for one second, 180mA will be outputted
tcp_socket.send_scpi_command('SOUR1:SEQ *(2(.25@0,.25@60),2(.5@0,.5@30),1@90)')          

# turn on Channel 1
tcp_socket.send_scpi_command('OUTP1 1') 
```

### Examples In Action
[/run_spikesafe_operating_modes/run_modulated_dc/RunModulatedMode.py](/run_spikesafe_operating_modes/run_modulated_dc/RunModulatedMode.py)