# [spikesafe-python API Overview](/spikesafe_python_lib_docs/README.md)

## Introduction

The official Python driver supporting Vektrex SpikeSafe products:
- [SpikeSafe PSMU](https://www.vektrex.com/products/spikesafe-source-measure-unit/)
- [SpikeSafe Performance Series ("PRF")](https://www.vektrex.com/products/spikesafe-performance-series-precision-pulsed-current-sources/)

Vektrex SpikeSafe Python API used for automation of custom instrument control sequences for testing LED, laser, and electronic equipment.

The Vektrex SpikeSafe Python API powers the Python examples published on Github.

Instructions to download and setup **spikesafe-python** can be found [here](https://pypi.org/project/spikesafe-python/) on pypi.org.

## Classes

| Class Name | Description |
| - | - |
| [ChannelData](/spikesafe_python_lib_docs/ChannelData/README.md) | A class used to store data in a simple accessible object from a channel in SpikeSafe's event response. | 
| [Compensation](/spikesafe_python_lib_docs/Compensation/README.md) | A helper class that provides a collection of helper functions you can use to help with SpikeSafe compensation settings. 
| [DigitizerData](/spikesafe_python_lib_docs/DigitizerData/README.md) | A class used to store data in a simple accessible object from a digitizer fetch response. |
| [DigitizerDataFetch](/spikesafe_python_lib_docs/DigitizerDataFetch/README.md) | A helper class used to simplify collecting data from a PSMU Digitizer. |
| [DigitizerEnums](/spikesafe_python_lib_docs/DigitizerEnums/README.md) | Defines the Digitizer acceptable values as enumerations. |
| [Discharge](/spikesafe_python_lib_docs/Discharge/README.md) | A helper class that provides a collection of helper functions you can use to properly discharge the SpikeSafe channel. |
| [EventData](/spikesafe_python_lib_docs/EventData/README.md) | A class used to store data in a simple accessible object from a SpikeSafe's event response. |
| [MemoryTableReadData](/spikesafe_python_lib_docs/MemoryTableReadData/README.md) | A class used to store data in a simple accessible object from a SpikeSafe's Memory Table Read response. |
| [Precision](/spikesafe_python_lib_docs/Precision/README.md) | A helper class that provides a collection of helper functions to get the precise number of decimal places for a SpikeSafe SCPI command argument. |
| [ReadAllEvents](/spikesafe_python_lib_docs/ReadAllEvents/README.md) | A helper class used to simplify reading events from a SpikeSafe. |
| [SpikeSafeEnums](/spikesafe_python_lib_docs/SpikeSafeEnums/README.md) | Defines the SpikeSafe acceptable values as enumerations. |
| [SpikeSafeError](/spikesafe_python_lib_docs/SpikeSafeError/README.md) | Exception raised for SpikeSafe errors returned by the System Error query. |
| [SpikeSafeEvents](/spikesafe_python_lib_docs/SpikeSafeEvents/README.md) | Defines the SpikeSafe events as enumerations. |
| [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md) | A class used to represent a TCP socket for remote communication to a SpikeSafe. |
| [TemperatureData](/spikesafe_python_lib_docs/TemperatureData/README.md) | A class used to store data in a simple accessible object from a heat sink in SpikeSafe's event response. |
| [Threading](/spikesafe_python_lib_docs/Threading/README.md) | A helper class used to simplify threading behavior. |