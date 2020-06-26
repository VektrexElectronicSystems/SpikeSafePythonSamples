# Making Integrated Voltage Measurements

These folders contain examples to make voltage measurements using the SpikeSafe SMU's integrated Digitizer. Relevant settings will be sent to both the SpikeSafe and the Digitizer, and then voltage will be measured across the DUT and displayed onscreen. Each folder contains information on the relevant settings and expected output from the given mode(s). These examples are only applicable to the SpikeSafe SMU and assume some basic knowledge of [SpikeSafe Operating Modes](../run_spikesafe_operating_modes).

## Directory
- [Measure All Pulsed Voltages](measure_all_pulsed_voltages)
- [Measure Pulsed Sweep Voltage](measure_pulsed_sweep_voltage)
- [Measure Voltage Across Pulse](measure_voltage_across_pulse)

## Usage

These sequences involve graphing measurement results, and require the [matplotlib](https://matplotlib.org/) library. See instructions on installing this library under the "Usage" section in the [SpikeSafePythonSamples markdown file](/README.md#installing-matplotlib-package).

Connect the SpikeSafe SMU's Force and Sense leads to the LED, Laser, or electrical equipment to be tested. Using the descriptions and screenshots provided, determine which mode fits your test scenario. Run the sequences provided and observe the outputted voltage measurement data onscreen. The code provided sends all the necessary commands to output current and measure voltage for a given test purpose, but sequences may be modified as necessary to fit your specific application.
