# Example for Measuring In-Situ LED Junction Temperature using the SpikeSafe SMU

## Purpose
Demonstrate how to make in-situ junction temperature (Tj) measurements on LEDs using the SpikeSafe SMU and its integrated Voltage Digitizer.

## Overview 
The junction temperature (Tj) of an LED is the temperature in the LED's active region, which is the point at which the diode connects to its base. Tj is a vital measurement in determining the efficiency of a part to remove heat, and therefore the expected lifetime of the part. A majority of the technology in the market limits the user to making Tj measurements after removing the part from its typical housing, which is both time-consuming and does not provide an accurate comparison to the part's typical operating Tj. The SpikeSafe SMU's Continuous Dynamic Bias Current (CDBC) along with its integrated Voltage Digitizer make it possible for users to measure an LED's Tj in its typical housing (i.e. "in-situ").

This test procedure follows the Electrical Test Method specified by the Joint Electron Device Engineering Council. More information can be found at [JESD 51-51](https://www.jedec.org/sites/default/files/docs/JESD51-51.pdf) and [LEDs Magazine](https://www.ledsmagazine.com/manufacturing-services-testing/article/14173251/jedec-technique-simplifies-led-junction-temperature-measurement).

## Procedure
In this sequence, three major steps will be performed in order to determine the in-situ Tj of an LED:
1.) Determine the K-factor, the change in forward voltage corresponding to a change in temperature for the LED
2.) 
3.)

## Key Settings
- **Pulse Mode:** Continuous Dynamic Bias Current
- **Bias Current (Measurement Current):** 33mA
- **Set Current (Heating Current):** 
- **Compliance Voltage:** 20V
- **On Time:** 1ms
- **Off Time:** 10µs
- **Ramp Rate:** Fast. Voltage will ramp as fast as 1000V/sec. Current will ramp as fast as 50A/sec.


## Considerations
- This sequence assumes the user has basic knowledge of SpikeSafe CDBC Mode operation. To find more information on the basics of SpikeSafe CDBC output, see [Run Bias Pulsed](../../run_spikesafe_operating_modes/run_bias_pulsed).
- This sequence provides the layout to run Tj measurement for a specific DUT. For your testing, you may have to modify the Set Current, Bias Current, and Compliance Voltage to obtain an accurate Tj measurement.


## Expected Results
