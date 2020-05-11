# Example for Operating the SpikeSafe SMU's Force Sense Selector Switch as a Connect/Disconnect Switch

## **Purpose**
Demonstrate how to use the SpikeSafe SMU's Force Sense Selector Switch to deliver power to an LED, Laser, or electrical component using both the SpikeSafe current output and an auxiliary source output.

The Force Sense Selector switch `further description needed`


## Overview 
In this sequence, the SpikeSafe initially operates in Multi-Pulse mode with the Force Sense Selector Switch set to Primary. Afterward, the switch is set to Auxiliary mode, in which SpikeSafe circuitry is completed disconnected from the DUT. Once any DUT modifications are complete, the switch is set back to Primary in which the SpikeSafe is connected, and the SpikeSafe outputs Multi-Pulse current to the DUT once more.

The Force Sense Selector Switch is an optional feature for the SpikeSafe that provides the capability to quickly make adjustments to a DUT in a production setting without physically disconnecting any cables. The switch is a true mechanical switch that completely isolates the SpikeSafe circuity from the DUT while in the disconnected (Auxiliary) state. Both the force leads and the sense leads are affected during switching.

The Force Sense Selector Switch can switch from Primary to Auxiliary mode as long as current is not actively being outputted from the SpikeSafe. This means that in Multi-Pulse mode, the channel can be enabled while the Switch changes state. 

In this sequence, it is assumed that the user has basic knowledge of the SpikeSafe's Multi-Pulse mode. If you have not previously used Multi-Pulse mode, see [Run Multi-Pulse](../../run_multi_pulse).

## Key Settings 
- **Set Current:** 100mA
- **Compliance Voltage:** 20V
- **Pulse Count:** 3
- **On Time:** 1s
- **On Time:** 1s
- **Ramp Rate:** Default. Voltage will ramp as fast as 10V/sec. Current will ramp as fast as 1A/sec.
- **Switch State:** Primary initially. After running a Multi-Pulse sequence, it will be switched to Auxiliary. After the message box is closed, it will go back to Primary to once again run with SpikeSafe operation.

## Circuit Diagram
The following circuit diagram shows illustrates the basic circuitry that makes up the Force Sense Selector Switch. It is a true hardware switch that isolates a one source when the other source is active.

![](Switch_Hardware_Setup_Diagram.png)