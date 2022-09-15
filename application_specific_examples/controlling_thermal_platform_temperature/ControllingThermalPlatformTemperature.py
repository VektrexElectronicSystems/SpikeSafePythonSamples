# Goal: 
# Use TEC to ramp up to 50°C, stabilize, and run for 10 minutes; then ramp down to 25°C, stabilize, and run for 10 minutes.

import logging
import sys
import time
from datetime import datetime, timedelta
from SerialInterface import SerialInterfaceDll
from time import sleep

### set these before starting application
set_temperature_one = 50
set_temperature_one_stability_minutes = 10
set_temperature_two = 25
set_temperature_two_stability_minutes = 10

### setting up sequence log
log = logging.getLogger(__name__)
logging.basicConfig(filename='SpikeSafePythonSamples.log',format='%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)

### start of main program
try:
    log.info("ControllingThermalPlatformTemperature.py started.")

    TEC_controller = SerialInterfaceDll()

    # Set the beep enable sound
    TEC_controller.write_command("BEEP 1")

    # Set the mount type to 284 TEC High Power LaserMount.
    # Will default sensor type, sensor coefficients, gain, fan mode, and current limit
    TEC_controller.write_command("TEC:MOUNT 284")

    # Set temperature control mode
    TEC_controller.write_command("TEC:MODE:T")

    # Set the heat/cool mode to both
    TEC_controller.write_command("TEC:HEATCOOL BOTH")

    # Set the low set temperature limit to 10°C
    TEC_controller.write_command("TEC:LIMit:TLO 10")

    # Set the high set temperature limit to 85°C
    TEC_controller.write_command("TEC:LIMit:THI 85")

    # Set platform tolerance to be within 0.5°C of set point for 30 seconds
    TEC_controller.write_command("TEC:TOLerance 0.5, 30")

    ##### Target temperature 1

    # Set set temperature to set_temperature_one
    TEC_controller.write_command("TEC:T {0}".format(set_temperature_one))

    # Set controller output to on
    TEC_controller.write_command("TEC:OUT 1")

    # Monitor until TEC is in tolerance
    while True:
        TEC_out_of_tolerance = TEC_controller.write_command("TEC:COND?")
        if TEC_controller.isKthBitSet(TEC_out_of_tolerance, 9) == True:
            break

    # Let TEC temperature stabilize while in tolerance
    TEC_stability_start_time = time.time()
    while True:
        TEC_out_of_tolerance = TEC_controller.write_command("TEC:COND?")
        if ((TEC_controller.isKthBitSet(TEC_out_of_tolerance, 9) == True) and 
            (time.time() - TEC_stability_start_time - 30 >= set_temperature_one_stability_minutes * 60)):
                break
        else:
            break

    # Set set temperature to set_temperature_two
    TEC_controller.write_command("TEC:T {0}".format(set_temperature_two))

    ##### Target temperature 2

    # Monitor until TEC is in tolerance
    while True:
        TEC_out_of_tolerance = TEC_controller.write_command("TEC:COND?")
        if TEC_controller.isKthBitSet(TEC_out_of_tolerance, 9) == True:
            break

    # Let TEC temperature stabilize while in tolerance
    TEC_stability_start_time = time.time()
    while True:
        TEC_out_of_tolerance = TEC_controller.write_command("TEC:COND?")
        if ((TEC_controller.isKthBitSet(TEC_out_of_tolerance, 9) == True) and 
            (time.time() - TEC_stability_start_time - 30 >= set_temperature_two_stability_minutes * 60 * 60)):
                break
        else:
            break

    ##### Disconnect
    TEC_controller.close()

    log.info("ControllingThermalPlatformTemperature.py completed.\n")

except Exception as err:
    # print any general exception to both the terminal and the log file, then exit the application
    error_message = 'Program error: {}\n'.format(err)
    log.error(error_message)       
    print(error_message)   
    sys.exit(1)