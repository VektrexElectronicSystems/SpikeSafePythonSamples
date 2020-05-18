# Reading Memory Table Data
The `*MEMory:TABLe:READings` query is a SpikeSafe-specific SCPI query to obtain status information for all SpikeSafe channels. This information includes the current bulk voltage, channel voltage, channel current, and channel state. The temperatures of each heat sink are also obtained by this query.

## Purpose
Demonstrate proper usage of the "Get SpikeSafe Status" query on the SpikeSafe. During typical operation, the `*MEMory:TABLe:READings` query should be sent periodically while the SpikeSafe is connected in order to monitor temperature and power output. This is especially useful when one or more SpikeSafe channels are enabled.

## Expected Output
A Get SpikeSafe Status query will be sent, and its response will be read. This typically looks similar to the text shown below if connected to a one-channel SpikeSafe and that channel is disabled.

`MEM:TABL:READ`

`(DIF (NAME "Output Readings" (DATA (BULK 100.1) (CH1 0.000000 0.000000 0) (T1 27.1) (T2 0.0) (T3 0.0) (T4 0.0) )))`
