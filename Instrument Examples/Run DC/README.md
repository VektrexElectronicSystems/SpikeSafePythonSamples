# Examples for Operating a SpikeSafe PRF or SMU in DC modes

##Purpose
How to use a SpikeSafe PRF or SMU to deliver high precision DC current to an LED or Laser.  These operation modes output constant current at the specified Set Current. Current is outputted with configurable current ramp and automated power reduction to protect devices under test.

## RunDCMode Overview
Operates SpikeSafe as DC current source with single output current.

## RunDCMode Key Settings
- **Set Current:** 100mA
- **Compliance Voltage:** 10V
- **Ramp Rate:** Default. Voltage will ramp as fast as 10V/sec. Current will ramp as fast as 1A/sec.


## RunDCMode Current Output
- When running either sequence, one can expect to see the following current ramp. This image was acquired by measuring output current using a TCPA300 Current Probe into a MDO3024 Mixed Domain Oscilloscope

![](DC_Ramp.png)

##RunDCDynamicMode Overview
Operates SpikeSafe as DC current source with multiple output current. In DC Dynamic mode, the Set Current can be modified while the SpikeSafe is outputting current.  This example can be used to generate a software controlled stair case ramp. 

##RunDCDynamicMode Key Settings
-Steps 10mA, 20mA, 30mA, 40mA
- **Set Current:** 100mA
- **Compliance Voltage:** 10V
- **Ramp Rate:** Default. Voltage will ramp as fast as 10V/sec. Current will ramp as fast as 1A/sec.

## RunDCMode Current Output
- When running either sequence, one can expect to see the following current ramp. This image was acquired by measuring output current using a TCPA300 Current Probe into a MDO3024 Mixed Domain Oscilloscope

![](DC_Ramp.png)
