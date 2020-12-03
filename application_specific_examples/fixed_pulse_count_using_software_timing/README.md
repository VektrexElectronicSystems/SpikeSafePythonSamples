# Example for Making Fixed Pulsed Count Using Software Based Timing

## Purpose
Demonstrate how to use a SpikeSafe DCP, PRF, or PSMU to make fixed pulse count using software based timing.

## Overview
Making fixed pulsed count using software based timing is simple when a rough number of fixed pulses is required. Continuous and Continuous Dynamic operation modes output a continuous current pulse train at the specified Set Current, On Time, and Off Time. Combined with using a software based timer, a fixed count of continuous current pulses can be made to a device in a simple setup.

## Key Settings

### SpikeSafe Current Output Settings
- **Pulse Mode:** Continuous Dynamic
- **Current:** 100mA
- **Set Current:** 3.5A (may modify according to DUT characteristics)
- **Compliance Voltage:** 10V
- **On Time:** 1us
- **Off Time:** 9us

### Software Settings Settings
- **Pulse Count:** 10,000
- **Time Waited to Achieve Pulse Count:** 30ms

## Considerations
- See [Run Pulsed](../../run_spikesafe_operating_modes/run_pulsed) for further descriptions of when to Continuous and Continuous Dynamic operation modes.
- SpikeSafe current pulse train starts when the SpikeSafe channel is turned on. To ensure expected current pulsing is supplied, the time to achieve pulse count is started after `Event 100, Channel Ready`, there's an expectation to in excess over the expected number of pulses.
- Due to software based timing there will be a difference between the number of actual pulses and the expected number of pulses.

## Expected Results
Taking considerations into account, there's an expectation to see over 10,000 pulses due to channel ready time and software based timing.

A frequency counters to track the number of pulses showed an output of 12,810 pulses. This implies there were ~2,810 pulses outputted before the SpikeSafe provided current pulses at a full current of 100mA, and ~10,000 pulses during the time waited to achieve the desired pulse count.

![](pulse_counter.png)