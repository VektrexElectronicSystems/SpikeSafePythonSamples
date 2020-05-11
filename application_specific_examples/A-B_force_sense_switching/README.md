# Example for Operating the SpikeSafe SMU's Force Sense Selector Switch to Control Two SMUs

## **Purpose**
Demonstrate how to use the SpikeSafe SMU's Force Sense Selector Switch to deliver power to an LED, Laser, or electrical component using both the SpikeSafe current output and an auxiliary source output.

The Force Sense Selector switch `further description needed`


## Overview 
In this sequence, the SpikeSafe initially operates in DC mode with the Force Sense Selector Switch set to Primary. Afterward, the switch is set to Auxiliary mode, in which the test circuit is routed from an Auxiliary source to the DUT. Once auxiliary testing is complete, the switch is set back to Primary and the SpikeSafe outputs DC current to the DUT once more.

The Force Sense Selector Switch is an optional feature for the SpikeSafe that provides the capability to switch between two SMUs (one being the SpikeSafe) for a given electrical test. This switching between the two sources does not require making any hardware or wiring modifications mid-test. Both the force leads and the sense leads are affected during switching.

The Force Sense Selector Switch can switch from Primary to Auxiliary mode as long as current is not actively being outputted from the SpikeSafe. Vektrex strongly recommends turning off any auxiliary source output before changing the switch state from Auxiliary to Primary to avoid damaging the DUT.

## Key Settings 
- **Set Current:** 100mA
- **Compliance Voltage:** 20V
- **Ramp Rate:** Default. Voltage will ramp as fast as 10V/sec. Current will ramp as fast as 1A/sec.
- **Switch State:** Primary initially. After running in the SpikeSafe's DC mode for 10 seconds, it will be switched to Auxiliary. After running any testing with an Auxiliary source, it will go back to Primary to once again run with SpikeSafe operation.

## Circuit Diagram
The following circuit diagram shows illustrates the basic circuitry that makes up the Force Sense Selector Switch. It is a true hardware switch that isolates a one source when the other source is active.

![](Switch_Hardware_Setup_Diagram.png)



