# Reading SpikeSafe Information

## **Read SpikeSafe Information Manually with Queries**
Corresponds to running [ReadIdnExpanded.py](/ReadIdnExpanded.py).

### *IDN? Query
The `*IDN?` query is a SCPI standard query to determine the identity of a given instrument. It generally provides information such as the instrument's model, serial number, and firmware version. For the SpikeSafe, the `*IDN?` query also provides the hardware version, number of channels, and most recent calibration date.

### Reading Digitizer Information
Digitizer is available on PSMU and PSMU HC select models. If the Digitizer is available (`VOLT:DIGI:AVAIL?`), its complete information ecompassing firmware version (`VOLT:VER?`), hardware revision (`VOLT:DATA:HWRE?`), serial number (`VOLT:DATA:SNUM?`), and calibration date (`VOLT:DATA:CDAT?`) can be read using a series of commands.

### Reading Force Sense Selector Switch Information
Force Sense Selector Switch is available on select models. The `OUTP1:CONN:AVAIL?` query is used to determine if the Force Sense Selector Switch is available.

### Purpose
Demonstrate proper usage of the "Identify SpikeSafe" queries on the SpikeSafe. During typical operation, the `*IDN?` and following queries should be sent upon connecting to determine vital information about the SpikeSafe. If a model is not configured with either a Digitizer or Force Sense Selector Switch, the queries for these can be omitted.

### Expected Output
An Identify SpikeSafe query will be sent, and its response will be read. This typically looks similar to the text shown below. Individual versions, models, and dates will vary per SpikeSafe. This output assumes a PSMU model configured with a Digitizer and Force Sense Selector Switch.

`*IDN?`

`Vektrex, SpikeSafe Mini, Rev 2.0.3.18; Ch 1: DSP 2.0.9, CPLD C.2, Last Cal Date: 10 OCT 2019, SN: 10004, HwRev: E, Model: MINI-PRF-5-01US`

`VOLT:DIGI:AVAIL?`

`TRUE`

`VOLT:VER?`

`0.9.0`

`VOLT:DATA:HWRE?`

`C`

`VOLT:DATA:SNUM?`

`50012`

`VOLT:DATA:CDAT?`

`02 DEC 2020`

`OUTP1:CONN:AVAIL?`

`ALL`

## **Read SpikeSafe Information using SpikeSafeInfoParser**
Corresponds to running [ReadSpikeSafeInfo.py](/ReadSpikeSafeInfo.py).

### Purpose
Demonstrate using [SpikeSafeInfoParser](/spikesafe_python_lib_docs/SpikeSafeInfoParser/README.md) to seamlessly gather all important SpikeSafe Information with a single function call. This parser automatically handles sending all of the necessary SCPI queries so that you can keep your python script clean.

### Expected Output
An Identify SpikeSafe query will automatically be sent, responses will be read, and a [SpikeSafeInfo](/spikesafe_python_lib_docs//SpikeSafeInfo/README.md) object returned with easily accessible attributes.