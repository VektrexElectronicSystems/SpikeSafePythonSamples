# Examples for Measuring Software Based DC Staircase Voltages Using the SpikeSafe PSMU Digitizer in DC Dynamic Mode

## Purpose
Measuring DC staircase voltages is essential in comparing the actual versus expected I/V results of a DUT. This example demonstrates how to use a SpikeSafe PSMU to provide a DUT DC current in a staircase pattern and take both a voltage and current measurement at each step. This is an addition to [Measure Staircase Sweep Voltage](../../making_integrated_voltage_measurements/measure_staircase_sweep_voltage/) when presented with any of the following cases:
1. Hardware triggering is available on external device
1. Trigger timing is greater than or equal to 1ms
1. Current readings are needed

The SpikeSafe PSMU's integrated Digitizer is used to make high precision voltage measurements and the Keithley 7510 DMM is used to make current measurements while outputting a DC current steps to the DUT. The Digitizer and DMM are taking triggered readings using a hardware trigger initiated by a SCPI command. In this case a 1 ohm resistor is used as the DUT.

## Overview 
Operates SpikeSafe as both DC current source and a high precision voltage measurement device. A DC output is demonstrated in [Run Staircase Sweep](../../run_spikesafe_operating_modes/run_staircase_sweep/). While current is outputted, voltage measurements are being taken across the flattest portion of each current pulse. After all measurements are taken and read, the results are plotted in an I-V graph.

Note the use of the New Data query while the SpikeSafe is operating. While the Digitizer is still acquiring voltage data, it can be unobtrusively queried to determine if the buffer is full yet. This information can be used to determine whether the user would ideally want to fetch data, as the data fetch will only return fresh data if the specified measurements have occurred. In this case, the New Data query will return `TRUE` once the Digitizer has taken measurements equal to its Trigger Count.

### Key Settings

### SpikeSafe Current Output Settings
- **Pulse Mode**: Staircase Sweep
- **Start Current**: 10mA
- **Stop Current**: 200mA
- **Step Count**: 10
- **On Time**: 2ms
- **Compliance Voltage**: 30V

### Digitizer Voltage Measurement Settings
- **Voltage Range**: 10V
- **Aperture**: 500us
- **Trigger Delay**: 1000us
- **Trigger Source**: Hardware
- **Trigger Count**: 10
- **Reading Count**: 1 (per trigger)

### DMM Current Measurement Settings
- **Current Range**: 1A
- **Aperture**: 500us
- **Trigger Delay**: 1000us
- **Trigger Source**: Hardware
- **Trigger Count**: 10
- **Reading Count**: 1 (per trigger)

## Expected Results
When running a DC staircase using this sequence, one can expect to see the following output.

**I/V Graph**

Once all 10 steps are measured, a graph will appear like below:

![](dc_staircase_graph.png)

**DC Staircase Current Output**

This image was acquired by measuring output current using a TCPA300 Current Probe into a MDO3024 Mixed Domain Oscilloscope

![](dc_staircase_output.png)