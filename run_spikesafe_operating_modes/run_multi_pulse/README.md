# Examples for Operating a SpikeSafe PRF or SMU in Multi Pulse mode

## **Purpose**
Demonstrate how to use a SpikeSafe PRF or SMU to deliver a high precision current pulse train with a specified pulse count to an LED, Laser, or electrical component. This operation mode consists of a user-specified pulse settings to output a specified amount of pulses. A trigger command or signal is used to start current output.

## **Run Multi Pulse Mode**

### Overview 
Operates SpikeSafe as pulsed current source outputting a current pulse train with user-specified pulse count. Typical pulse settings such as Set Current, On Time, and Off Time also apply to this mode. When default trigger settings are used, pulses are outputted when the "Output Trigger" SCPI command is received. 

A channel that is operating in Multi Pulse mode can output as many pulses as specified while enabled. A pulse will only be outputted if the command is received after the previous pulse is complete. When a channel is enabled but no pulses are outputting, the user is able to change the Set Current.

Note the use of the Pulse End Query in this sequence. The Pulse End Query is a useful tool in Single Pulse and Multi Pulse modes to determine whether the SpikeSafe has completed its specified pulse output.

### Key Settings 
- **Set Current:** 100mA initially. After the first Multi-Pulse train is outputted, the Set Current is changed to 200mA while running.
- **Compliance Voltage:** 20V
- **Pulse Count:** 3
- **On Time:** 1s
- **On Time:** 1s

### Current Output
When running this sequence, one can expect to see the following pulse output from the first of the two Multi-Pulse trains. This image was acquired by measuring output current using a TCPA300 Current Probe into a MDO3024 Mixed Domain Oscilloscope

![](Multi_Pulse_Output.png)
