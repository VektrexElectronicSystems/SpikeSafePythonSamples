# Reading Memory Table Data
The `MEM:TABL:READ` query is a SpikeSafe-specific SCPI query to obtain status information for all SpikeSafe channels. This information includes the current bulk voltage, channel voltage, channel current, and channel state. The temperatures of each heat sink are also obtained by this query.

## Purpose
Demonstrate proper usage of the "Get SpikeSafe Status" query on the SpikeSafe. During typical operation, the `MEM:TABL:READ` query should be sent periodically while the SpikeSafe is connected in order to monitor temperature and power output. This is especially useful when one or more SpikeSafe channels are enabled.

## Expected Output
A Get SpikeSafe Status query will be sent, and its response will be read. This typically looks similar to the text shown below if connected to a one-channel SpikeSafe and that channel is enabled. Here the 1 channel SpikeSafe bulk voltage is 100.1V; Channel 1 displays 10.024510V, 10.001mA, and is enabled; and Heat Sink Temperature 1 measures 27.1°C.

`MEM:TABL:READ`

`(DIF (NAME "Output Readings" (DATA (BULK 100.1) (CH1 10.024510 0.010001 1) (T1 27.1) (T2 0.0) (T3 0.0) (T4 0.0) )))`

## MEM:TABL:READ Output Data Format
Data format used for the readings is described below.

```
(DIF (NAME "Output Readings”  
  (DATA  
    (BULK <vread>)  
    (CH1 <vread> <iread> <on/off>)  
    (CH2 <vread> <iread> <on/off>)  
    (CH3 <vread> <iread> <on/off>)  
    (CH4 <vread> <iread> <on/off>)  
    (CH5 <vread> <iread> <on/off>)  
    (CH6 <vread> <iread> <on/off>)  
    (CH7 <vread> <iread> <on/off>)  
    (CH8 <vread> <iread> <on/off>)  
    (T1 <tread>)  
    (T2 <tread>)  
    (T3 <tread>)  
    (T4 <tread>)  
  )  
)) 
```

| Property | Description |
| - | - |
| BULK <vread> | Float in volts, up to 1 decimal place |
| CH<#> <vread> | Float in volts, up to 6 decimal places |
| CH<#> <iread> | Float in amps, up to 6 decimal places |
| CH<#> <on/off> | Boolean, 1 or 0 |
| T<#> <tread> | Float in Celsius, up to 1 decimal place |

NOTE: SS400 model varies between 1 to 8 channels but will always report 4 heat sink temperatures. PSMU is always 1 channel and will always report 1 heat sink temperature.