# Using the Force Sense Selector Switch

These folders contain examples to use the optional integrated switch in the SpikeSafe PSMU. The Force Sense Selector Switch is a true mechanical switch that controls both the Force leads and the Sense leads from the SpikeSafe PSMU. In these examples, the SpikeSafe outputs currents similar to the examples in [Run SpikeSafe Operating Modes](../run_spikesafe_operating_modes) and then the switch is implemented to either disconnect the SpikeSafe from the test circuit, or to implement an auxiliary power source into the test circuit. 

## Directory
- [A/B Force/Sense Switching](A-B_force_sense_switching)
- [Connect/Disconnect Switching](connect_disconnect_switching)

## Usage

These sequences require no cabling modifications once started. The SpikeSafe should be connected to the DUT at the "To Load" output, and if applicable the auxiliary source should be connected to the SpikeSafe at the "From Aux" output.

Modify the IP address to match your SpikeSafe, and then run the sequence. The output will match the description for the given sequence. These sequences assume the user has some basic knowledge of the relevant SpikeSafe operating mode. For more information on these modes, see [Run SpikeSafe Operating Modes](../run_spikesafe_operating_modes).