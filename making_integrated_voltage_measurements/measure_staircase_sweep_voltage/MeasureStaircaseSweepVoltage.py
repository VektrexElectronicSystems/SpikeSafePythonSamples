# Goal: 
# Connect to a SpikeSafe and run a Staircase Sweep into a 10Ω resistor. Take voltage measurements from the DC output using the SpikeSafe PSMU's integrated Digitizer
# 
# Expectation: 
# Channel 1 will be driven with 100mA with a forward voltage of ~1V during this time

import sys
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
step_on_time_milliseconds: int = 1

# Digitizer voltage range options in volts: 10, 100, 400
digitizer_voltage_range_volts: float = 10
digitizer_aperture_microseconds: int = 514
digitizer_hardware_trigger_delay_microseconds: int = 150
digitizer_hardware_trigger_count: int = current_step_count
digitizer_reading_count: int = 1

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
    log.info("MeasureStaircaseSweepVoltage.py started.")

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
    load_impedance, rise_time = spikesafe_python.Compensation.get_optimum_compensation(spikesafe_info.maximum_set_current, stop_current_amps, step_on_time_milliseconds / 1000.0)
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

    # start Digitizer measurements. We want the digitizer waiting for triggers before starting the Staircase Sweep
    tcp_socket.send_scpi_command('VOLT:INIT')

    # turn on Channel 1 
    tcp_socket.send_scpi_command('OUTP1 1')    
    
    # wait until Channel 1 is fully ramped so we can send a trigger command for a Staircase Sweep
    spikesafe_python.ReadAllEvents.read_until_event(tcp_socket, spikesafe_python.SpikeSafeEvents.CHANNEL_READY) # event 100 is "Channel Ready"

    # trigger Channel 1 to start the Staircase Sweep output
    tcp_socket.send_scpi_command('OUTP1:TRIG')

    # Get estimated completion time for Digitizer measurements to occur. Estimating completion time minimizes digitizer polling during DigitizerDataFetch
    estimated_complete_time_seconds = spikesafe_python.DigitizerDataFetch.get_new_voltage_data_estimated_complete_time(
        aperture_microseconds=digitizer_aperture_microseconds,
        hardware_trigger_count=digitizer_hardware_trigger_count,
        reading_count=digitizer_reading_count,
        hardware_trigger_delay_microseconds=digitizer_hardware_trigger_delay_microseconds)
    
    # fetch voltage data from Digitizer containing sample number and voltage reading
    digitizer_data = [spikesafe_python.DigitizerData]

    try:
        # wait for the Digitizer measurements to complete. We need to wait for the data acquisition to complete before fetching the data
        digitizer_data = spikesafe_python.DigitizerDataFetch.wait_for_new_voltage_data(
            spike_safe_socket=tcp_socket,
            wait_time=estimated_complete_time_seconds,
            timeout=10)
        
        # fetch complete data
        digitizer_data = spikesafe_python.DigitizerDataFetch.fetch_voltage_data(tcp_socket)

        log.info(f"Complete VOLT:FETC? Response returned with {len(digitizer_data)} readings")
    except Exception as err:
        log.error(f"Complete VOLT:FETC? Response error: {err}")

        try:
            # attempt to abort partial digitizer readings
            tcp_socket.send_scpi_command("VOLT:ABOR:PART")

            # wait for the Digitizer partial measurements to complete. It's expected that the wait time here will be small since we are fetching partial data after an abort.
            spikesafe_python.DigitizerDataFetch.wait_for_new_voltage_data(tcp_socket)

            # fetch whatever data is available
            digitizer_data = spikesafe_python.DigitizerDataFetch.fetch_voltage_data(tcp_socket)

            log.info(f"Partial VOLT:FETC? Response after error returned with {len(digitizer_data)} readings")

            # check if partial measurements were a result of a SpikeSafe error
            spikesafe_python.ReadAllEvents.log_all_events(tcp_socket)
        except TimeoutError as e:
            # Timeout error will occur if no partial measurements were taken
            log.error(f"Partial VOLT:FETC? Response error: {e}")

            # check if no partial measurements were a result of a SpikeSafe error
            spikesafe_python.ReadAllEvents.read_all_events(tcp_socket)
        except Exception as e:
            # All other errors, exit the script
            raise

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
            
    # split array and separate with commas
    voltage_readings = []
    current_steps = []
    step_size_amps = (stop_current_amps - start_current_amps) / (current_step_count - 1)
    for dd in digitizer_data:
        voltage_readings.append(dd.voltage_reading)
        current_steps.append(start_current_amps + step_size_amps * (dd.sample_number - 1))

    # plot the pulse shape using the fetched voltage readings
    plt.plot(current_steps, voltage_readings)
    plt.ylabel('Voltage (V)')
    plt.xlabel('Set Current (A)')
    plt.title(f'Digitizer Voltage Readings - Staircase Sweep ({start_current_amps}A to {stop_current_amps}A)')
    plt.grid()
    plt.show()

    log.info("MeasureStaircaseSweepVoltage.py completed.\n")

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