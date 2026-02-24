# Goal: 
# Connect to a SpikeSafe and run a Pulsed Sweep into a 10Ω resistor. Take voltage measurements from the pulsed output using the SpikeSafe PSMU's integrated Digitizer, and current measurements with a Keithley 7510 DMM
# 
# Expectation: 
# Channel 1 will be driven with 100mA with a forward voltage of ~1V during this time

from datetime import datetime
import sys
import time
import logging
import spikesafe_python
from matplotlib import pyplot as plt   

### set these before starting application

# SpikeSafe IP address and port number
ip_address: str = '10.0.0.220'
port_number: int = 8282

start_current_amps: float = 0.02
stop_current_amps: float = 0.2
current_step_count: int = 10
compliance_voltage_volts: float = 20
step_on_time_milliseconds: int = 2

# Digitizer voltage range options in volts: 10, 100, 400
digitizer_voltage_range_volts: float = 10
digitizer_aperture_microseconds: int = 500
digitizer_hardware_trigger_delay_microseconds: int = 1000
digitizer_hardware_trigger_count: int = current_step_count
digitizer_reading_count: int = 1

# Keithley 7510 DMM IP address and port number
dmm_ip_address: str = '10.0.0.240'
dmm_port_number: int = 5025

# DMM trigger timeout in seconds with added 10% margin to expected DMM trigger time. This is the maximum time to wait for the DMM to complete its triggered measurements
dmm_trigger_timeout_seconds: float = (step_on_time_milliseconds * current_step_count) + step_on_time_milliseconds * current_step_count * 0.1

# DMM current range setting based on the largest test current, matching SpikeSafe's Stop Current
dmm_current_range: float = 1
if stop_current_amps < 0.00001:
    dmm_current_range = 0.00001
elif stop_current_amps < 0.0001:
    dmm_current_range = 0.0001   
elif stop_current_amps < 0.001:
    dmm_current_range = 0.001   
elif stop_current_amps < 0.01:
    dmm_current_range = 0.01               
elif stop_current_amps < 0.1:
    dmm_current_range = 0.1
else:
    dmm_current_range = 1

# DMM aperture in seconds
dmm_aperture_seconds: float = digitizer_aperture_microseconds / 1_000_000

# DMM hardware trigger delay in seconds, matching Digitizer's hardware trigger delay
dmm_hardware_trigger_delay_seconds: float = digitizer_hardware_trigger_delay_microseconds / 1_000_000

# Dmm trigger count, matching Digitizer's Trigger Count
dmm_hardware_trigger_count: int = digitizer_hardware_trigger_count

# Dmm reading count, matching Digitizer's Reading Count
dmm_reading_count: int = digitizer_reading_count

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
    log.info("MeasuringDcStaircaseIVSweep.py started.")

    log.info("Python version: {}".format(sys.version))
    
    # instantiate new TcpSocket to connect to SpikeSafe
    tcp_socket = spikesafe_python.TcpSocket(enable_logging=False)
    tcp_socket.open_socket(ip_address, port_number)

    # reset to default state and check for all events,  this will automatically abort digitizer in order get it into a known state. This is good practice when connecting to a SpikeSafe PSMU
    # it is best practice to check for errors after sending each command      
    tcp_socket.send_scpi_command('*RST')                  
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)
    
    # parse the SpikeSafe information
    spikesafe_info = spikesafe_python.SpikeSafeInfoParser.parse_spikesafe_info(tcp_socket)
    log.info(f'SpikeSafe *IDN?: {spikesafe_info.idn}')
    
    # set up Channel 1 for pulsed sweep output. To find more explanation, see instrument_examples/run_spikesafe_operating_modes/run_pulsed
    tcp_socket.send_scpi_command('SOUR1:FUNC:SHAP STAIRCASESWEEP')

    # set Channel 1's Staircase Sweep parameters to match the test expectation
    tcp_socket.send_scpi_command(f'SOUR1:CURR:STA:SWE:STAR {spikesafe_python.Precision.get_precise_current_command_argument(start_current_amps)}')
    tcp_socket.send_scpi_command(f'SOUR1:CURR:STA:SWE:STOP {spikesafe_python.Precision.get_precise_current_command_argument(stop_current_amps)}')   
    tcp_socket.send_scpi_command(f'SOUR1:CURR:STA:SWE:STEP {current_step_count}')  
    tcp_socket.send_scpi_command(f'SOUR1:PULS:STA:SWE:TON {step_on_time_milliseconds}')
    tcp_socket.send_scpi_command(f'SOUR1:VOLT {spikesafe_python.Precision.get_precise_compliance_voltage_command_argument(compliance_voltage_volts)}')
    
    # set Channel 1's compensation settings
    # For higher power loads or shorter pulses, these settings may have to be adjusted to obtain ideal pulse shape
    load_impedance, rise_time = spikesafe_python.Compensation.get_optimum_compensation(spikesafe_info.maximum_set_current, stop_current_amps, step_on_time_milliseconds)
    tcp_socket.send_scpi_command(f'SOUR1:PULS:CCOM {load_impedance}')
    tcp_socket.send_scpi_command(f'SOUR1:PULS:RCOM {rise_time}') 

    # set Channel 1's Ramp mode to Fast
    tcp_socket.send_scpi_command('OUTP1:RAMP FAST') 
    
    # set Channel 1's External Source Trigger Out to Always
    tcp_socket.send_scpi_command('SOUR1:PULS:TRIG ALWAYS')

    # set Channel 1's External Source Trigger Out to Positive
    tcp_socket.send_scpi_command('OUTP1:TRIG:SLOP POS')

    # set Channel 1's trigger source to Internal (so that the SpikeSafe triggers the Staircase Sweep when the OUTP:TRIG command is sent)
    tcp_socket.send_scpi_command('OUTP1:TRIG:SOUR INT')

    # set Digitizer voltage range to 10V since we expect to measure voltages significantly less than 10V
    tcp_socket.send_scpi_command(f'VOLT:RANG {digitizer_voltage_range_volts}')

    # set Digitizer aperture. Aperture specifies the measurement time, and we want to measure a majority of the pulse's constant current output
    tcp_socket.send_scpi_command(f'VOLT:APER {spikesafe_python.Precision.get_precise_time_microseconds_command_argument(digitizer_aperture_microseconds)}')

    # set Digitizer trigger delay. We want to give sufficient delay to omit any overshoot the current pulse may have
    tcp_socket.send_scpi_command(f'VOLT:TRIG:DEL {spikesafe_python.Precision.get_precise_time_microseconds_command_argument(digitizer_hardware_trigger_delay_microseconds)}')

    # set Digitizer trigger source to hardware. When set to a hardware trigger, the digitizer waits for a trigger signal from the SpikeSafe to start a measurement
    tcp_socket.send_scpi_command('VOLT:TRIG:SOUR HARDWARE')

    # set Digitizer trigger edge to rising. The Digitizer will start a measurement after the SpikeSafe's rising pulse edge occurs
    tcp_socket.send_scpi_command('VOLT:TRIG:EDGE RISING')

    # set Digitizer trigger count. We want to setup to measure voltage for every step in the Staircase Sweep
    tcp_socket.send_scpi_command(f'VOLT:TRIG:COUN {digitizer_hardware_trigger_count}')

    # set Digitizer reading count to 1. This is the amount of readings that will be taken when the Digitizer receives its specified trigger signal
    tcp_socket.send_scpi_command(f'VOLT:READ:COUN {digitizer_reading_count}')

    # check all SpikeSafe event since all settings have been sent
    spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)

    # instantiate new TcpSocket to connect to DMM
    dmm_tcp_socket = spikesafe_python.TcpSocket(enable_logging=False)
    dmm_tcp_socket.open_socket(dmm_ip_address, dmm_port_number)

    # DMM may require a few seconds to process commands, extend the timeout to avoid unintentional connection errors
    dmm_tcp_socket.tcp_socket.settimeout(10)

    # Log DMM information
    dmm_tcp_socket.send_scpi_command('*IDN?')
    dmm_idn = dmm_tcp_socket.read_data()
    log.info(f'DMM *IDN?: {dmm_idn}')
    dmm_tcp_socket.send_scpi_command('*LANG SCPI')
    
    # Set time on DMM to match computer's
    DateTime = time.localtime()
    dmm_tcp_socket.send_scpi_command(f'SYST:TIME {DateTime.tm_hour}, {DateTime.tm_min}, {DateTime.tm_sec}')
    dmm_tcp_socket.send_scpi_command('*RST')
    dmm_tcp_socket.send_scpi_command('*CLS')

    # Set sense function
    dmm_tcp_socket.send_scpi_command('FUNC "CURR:DC"')

    # Set aperture
    dmm_tcp_socket.send_scpi_command(f'CURR:APER {dmm_aperture_seconds}')

    # Set auto-zero
    dmm_tcp_socket.send_scpi_command('CURR:AZER OFF')

    # Set auto-delay
    dmm_tcp_socket.send_scpi_command('CURR:DEL:AUTO OFF')

    # Set range (either SENS:CURR:RANG:AUTO ON, or CURR:RANG <0.00001, 0.0001,.001, .01, .1, 1, 3, or 10>)
    dmm_tcp_socket.send_scpi_command(f'CURR:RANG {dmm_current_range}')

    # Set relative offset state (controls relative offset value to the measurement, if ON send CURR:REL: <value in amps>)
    dmm_tcp_socket.send_scpi_command('CURR:REL:STAT OFF')

    # Clear existing trigger model
    dmm_tcp_socket.send_scpi_command('TRIG:LOAD "Empty"')

    # Set Trigger Block 1, clears defbuffer1 at beginning of execution
    dmm_tcp_socket.send_scpi_command('TRIG:BLOC:BUFF:CLE 1')

    # Set Trigger Block 2, wait for EXT trigger event, and clear previously detected trigger events when entering wait block (ENT)
    dmm_tcp_socket.send_scpi_command('TRIG:BLOC:WAIT 2, EXT, ENT')

    # Set EXT trigger to rising edge (or Trigger Slope)
    dmm_tcp_socket.send_scpi_command('TRIG:EXT:IN:EDGE RIS')

    # Set Trigger Block 3, delay for n seconds (or Trigger Delay)
    dmm_tcp_socket.send_scpi_command(f'TRIG:BLOC:DEL:CONS 3, {dmm_hardware_trigger_delay_seconds}')

    # Set Trigger Block 4, use buffer defbuffer1 to store readings, and take n readings (or Reading count)
    dmm_tcp_socket.send_scpi_command(f'TRIG:BLOC:MEAS 4, "defbuffer1", {dmm_reading_count}')

    # Set Trigger Block 5, loop n more time (or number of Triggers) back to block 2
    dmm_tcp_socket.send_scpi_command(f'TRIG:BLOC:BRAN:COUN 5, {dmm_hardware_trigger_count}, 2')

    # check for DMM errors
    # initialize flag to check if DMM event queue is empty 
    is_dmm_event_queue_empty = False                                                                                                                      
    # run as long as there is an event in the DMM queue
    while is_dmm_event_queue_empty == False:
        # request DMM events and read data 
        dmm_tcp_socket.send_scpi_command('SYST:ERR?')                                        
        event_response = dmm_tcp_socket.read_data()

        # event queue is empty
        if event_response.startswith('0'):
            is_dmm_event_queue_empty = True
        else:
            # add event to event queue
            raise Exception('DMM exception: {}'.format(event_response))

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')    
    
    # wait until Channel 1 is fully ramped so we can send a trigger command for a Staircase Sweep
    spikesafe_python.ReadAllEvents.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # start Digitizer measurements. We want the digitizer waiting for triggers before starting the Staircase Sweep
    tcp_socket.send_scpi_command('VOLT:INIT')

    # start DMM measurements. We want the DMM waiting for triggers before starting the Staircase Sweep
    dmm_tcp_socket.send_scpi_command('INIT')

    # trigger Channel 1 to start the Staircase Sweep output
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # wait for the Digitizer measurements to complete. We need to wait for the data acquisition to complete before fetching the data
    spikesafe_python.DigitizerDataFetch.wait_for_new_voltage_data(tcp_socket, 0.5)

    # fetch the Digitizer voltage readings
    digitizerData = spikesafe_python.DigitizerDataFetch.fetch_voltage_data(tcp_socket)

    # initialize flag to check if DMM trigger state is idle
    is_dmm_idle_state = False

    start_time = datetime.now()

    # monitor DMM trigger state machine and check for errors until all readings are taken
    while is_dmm_idle_state == False:

        # Calculate the elapsed time
        elapsed_time = datetime.now() - start_time

        # Check if the elapsed time DMM trigger timeout
        if elapsed_time.total_seconds() > dmm_trigger_timeout_seconds:
            raise Exception('DMM exception: DMM triggered measurement has not completed in {} seconds. Check if DMM trigger cable is functioning properly'.format(dmm_trigger_timeout_seconds))

        # request DMM trigger state and read data 
        dmm_tcp_socket.send_scpi_command('TRIG:STAT?')
        trigger_state_response = dmm_tcp_socket.read_data()

        # DMM trigger state is idle
        if trigger_state_response.startswith('IDLE'):
            is_dmm_idle_state = True

        # initialize flag to check if DMM event queue is empty 
        is_dmm_event_queue_empty = False
                                                                                                                    
        # run as long as there is an event in the DMM queue
        while is_dmm_event_queue_empty == False:
            # request DMM events and read data 
            dmm_tcp_socket.send_scpi_command('SYST:ERR?')                                        
            event_response = dmm_tcp_socket.read_data()

            # event queue is empty
            if event_response.startswith('0'):
                is_dmm_event_queue_empty = True
            else:
                # add event to event queue
                raise Exception('DMM exception: {}'.format(event_response))

        # Read DMM data
        log.info('Reading DMM measurement...')

        # return the number of readings in buffer
        dmm_tcp_socket.send_scpi_command('TRAC:ACT?') 
        dmm_data_point_total_count = dmm_tcp_socket.read_data()

        # return the starting index
        dmm_tcp_socket.send_scpi_command('TRAC:ACT:STAR?')
        dmm_data_point_start_index = dmm_tcp_socket.read_data()

        # return the end index
        dmm_tcp_socket.send_scpi_command('TRAC:ACT:END?')
        dmm_data_point_end_index = dmm_tcp_socket.read_data()

        # return the array of data
        dmm_tcp_socket.send_scpi_command('TRAC:DATA? {}, {}, "defbuffer1", READ'.format(dmm_data_point_start_index, dmm_data_point_end_index))
        dmm_data_points = dmm_tcp_socket.read_data()

        # split array and separate with commas
        dmm_readings = []
        dmm_data_points_split = dmm_data_points.split(',')
        for dmm_data_point in dmm_data_points_split:
            dmm_current_reading = float(dmm_data_point)
            dmm_readings.append(dmm_current_reading)

        # Wait for the Staircase Sweep to be complete
        spikesafe_python.ReadAllEvents.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.STAIRCASE_SWEEP_IS_COMPLETED) # event 127 is "Staircase Sweep is completed"

    # turn off Channel 1 after routine is complete
    tcp_socket.send_scpi_command('OUTP1 0')
    
    # wait until the channel is fully discharged
    spikesafe_python.Discharge.wait_for_spikesafe_channel_discharge(
        spikesafe_socket= tcp_socket,
        spikesafe_info=spikesafe_info,
        compliance_voltage=compliance_voltage_volts, 
        channel_number=1)

    # disconnect from SpikeSafe                      
    tcp_socket.close_socket()    

    # put the fetched data in a plottable data format
    voltage_readings = []
    current_steps = []
    sweep_step_size_amps = (stop_current_amps - start_current_amps) / (current_step_count - 1)
    current_readings = dmm_readings
    for dd in digitizerData:
        voltage_readings.append(dd.voltage_reading)
        current_steps.append(start_current_amps + sweep_step_size_amps * (dd.sample_number - 1))

    # create figure and first axis
    fig, ax1 = plt.subplots()

    # left Y axis: DMM readings
    ax1.plot(current_steps, dmm_readings, color='blue')
    ax1.set_xlabel('Set Current (A)')
    ax1.set_ylabel('DMM Current (A)', color='blue')
    ax1.grid(True)

    # right Y axis: digitizer readings
    ax2 = ax1.twinx()
    ax2.plot(current_steps, voltage_readings, color='red')
    ax2.set_ylabel('Digitizer Voltage (V)', color='red')

    plt.title(
        f'2 ms Staircase L-I-V'
        f'({start_current_amps}A to {stop_current_amps}A)'
    )
    fig.tight_layout()
    plt.show()

    log.info("MeasuringDcStaircaseIVSweep.py completed.\n")

except spikesafe_python.SpikeSafeError as ssErr:
    # print any SpikeSafe-specific error to both the terminal and the log file, then exit the application
    error_message = 'SpikeSafe error: {}\n'.format(ssErr)
    log.error(error_message)
    print(error_message)
    sys.exit(1)
except Exception as err:
    # print any general exception to both the terminal and the log file, then exit the application
    error_message = 'Program error: {}\n'.format(err)
    log.error(error_message)       
    print(error_message)   
    sys.exit(1)