# Examples for Operating a SpikeSafe PRF or PSMU in Pulsed modes

## **Purpose**
Demonstrate how to use a SpikeSafe PRF or PSMU to deliver high precision pulsed current to an LED or Laser. Continuous and Continuous Dynamic operation modes output a continuous current pulse train at the specified Set Current, On Time, and Off Time. These two modes differ in the way they start up, and the way they regulate current after startup.

Vektrex recommends using Continuous Dynamic for testing low currents below a few amps.  Continuous Dynamic starts with no ramp; the current transitions from zero to the programmed value in microseconds. Continuous Dynamic does not make adjustments to decrease internal power dissipation.

For long term testing over a few amps Continuous mode is recommended. Continuous Mode makes internal adjustments to decrease power dissipation. For long term reliability testing this reduction in power will save energy and generate less heat. The small adjustments can introduce a very small current variation, usually less than 0.1% of programmed set current.

## **Run Pulsed Mode**

### Overview 
Operates SpikeSafe as a pulsed current source with single output current and user-specified Pulse On Time and Pulse Off Time.

### Key Settings 
- **Set Current:** 100mA
- **Compliance Voltage:** 20V
- **On Time:** 1ms
- **Off Time:** 9ms
- **Ramp Rate:** Default. Voltage will ramp as fast as 10V/sec. Current will ramp as fast as 1A/sec.

### Considerations
- On Time and Off Time can be set using an alternative command set that consists of setting Duty Cycle, Period, and/or Pulse Width. A tutorial describing use of these alternative commands can be found in the [Using Pulse Holds](../../application_specific_examples/using_pulse_holds) folder.
- These sequences are run with the default compensation settings. This may not result in the ideal pulse shape for all test loads, in which case [Pulse Tuning](../../application_specific_examples/pulse_tuning) may be required. Pulse tuning is especially applicable during shorter Pulse On Times in the microsecond scale.

### Current Output
When running either sequence, one can expect to see the following current output and pulse shape. This image was acquired by measuring output current using a TCPA300 Current Probe into a MDO3024 Mixed Domain Oscilloscope

**Pulse Shape**

![](continuous_pulse_shape.png)

**Continuous Pulse Train**

![](continuous_pulse_train.png)


## **Run Pulsed Dynamic Mode**

### Overview
Operates SpikeSafe as a pulsed current source with multiple output currents. In Continuous Dynamic mode, the Set Current, On Time, and Off Time can be modified while the SpikeSafe is outputting current.  

Set the Maximum Compliance Voltage (MCV) to the expected load voltage +5V. Reduce MCV if an internal over power error occurs. 

### Key Settings
- **Set Current:** 100mA initially. While the channel is operating, the Set Current will be dynamically changed to 200mA.
- **On Time:** 1ms initially. While the channel is operating, the On Time will be dynamically changed to 100µs.
- **Off Time:** 9ms initially. While the channel is operating, the Off Time will be dynamically changed to 100µs.
- **Compliance Voltage:** 20V
- **Ramp Rate:** Default. Voltage will ramp as fast as 10V/sec. Current will ramp as fast as 1A/sec.

### Current Output
One can expect to see the following current pulse train when running this Pulsed Dynamic sequence. Note the changes in Set Current, On Time, and Off Time. This image was acquired by measuring output current using a TCPA300 Current Probe into a MDO3024 Mixed Domain Oscilloscope

![](pulsed_dynamic_adjustments.png)
