# Reading *IDN? Query
The `*IDN?` query is a SCPI standard query to determine the identity of a given instrument. It generally provides information such as the instrument's model, serial number, and firmware version. For the SpikeSafe, the `*IDN?` query also provides the hardware version, number of channels, and most recent calibration date.

## Purpose
Demonstrate proper usage of the "Identify SpikeSafe" query on the SpikeSafe. During typical operation, the `*IDN?` query should be sent upon connecting to determine vital information about the SpikeSafe. 

## Expected Output
An Identify SpikeSafe query will be sent, and its response will be read. This typically looks similar to the text shown below. Individual versions, models, and dates will vary per SpikeSafe.

`*IDN?`

`Vektrex, SpikeSafe Mini, Rev 2.0.3.18; Ch 1: DSP 2.0.9, CPLD C.2, Last Cal Date: 10 OCT 2019, SN: 10004, HwRev: E, Model: MINI-PRF-5-01US`
