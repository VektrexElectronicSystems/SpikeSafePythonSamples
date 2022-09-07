# spikesafe-python API Overview

## Introduction

The official Python driver supporting Vektrex SpikeSafe products:
- [SpikeSafe SMU](https://www.vektrex.com/products/spikesafe-source-measure-unit/)
- [SpikeSafe Performance Series ("PRF")](https://www.vektrex.com/products/spikesafe-performance-series-precision-pulsed-current-sources/)

Vektrex SpikeSafe Python API used for automation of custom instrument control sequences for testing LED, laser, and electronic equipment.

The Vektrex SpikeSafe Python API powers the Python examples published on Github.

Instructions to download and setup **spikesafe-python** can be found [here](https://pypi.org/project/spikesafe-python/) on pypi.org.

## Classes

| Class Name | Description |
| - | - |
| [ChannelData](/spikesafe_python_lib_docs/ChannelData/README.md) | A class used to store data in a simple accessible object from a channel in SpikeSafe's event response. | 
| [DigitizerData](/spikesafe_python_lib_docs/DigitizerData/README.md) | A class used to store data in a simple accessible object from a digitizer fetch response. |
| [DigitizerDataFetch](/spikesafe_python_lib_docs/DigitizerDataFetch/README.md) | A helper class used to simplify collecting data from a PSMU Digitizer. |
| [EventData](/spikesafe_python_lib_docs/EventData/README.md) | A class used to store data in a simple accessible object from a SpikeSafe's event response. |
| [MemoryTableReadData](/spikesafe_python_lib_docs/MemoryTableReadData/README.md) | A class used to store data in a simple accessible object from a SpikeSafe's Memory Table Read response. |
| [ReadAllEvents](/spikesafe_python_lib_docs/ReadAllEvents/README.md) | A helper class used to simplify reading events from a SpikeSafe. |
| [SpikeSafeError](/spikesafe_python_lib_docs/SpikeSafeError/README.md) | Exception raised for SpikeSafe errors returned by the System Error query. |
| [SpikeSafeEvents Enum](/spikesafe_python_lib_docs/SpikeSafeEvents/README.md) | Defines the SpikeSafe events as enumerations. |
| [TcpSocket](/spikesafe_python_lib_docs/TcpSocket/README.md) | A class used to represent a TCP socket for remote communication to a SpikeSafe. |
| [TemperatureData](/spikesafe_python_lib_docs/TemperatureData/README.md) | A class used to store data in a simple accessible object from a heat sink in SpikeSafe's event response. |
| [Threading](/spikesafe_python_lib_docs/Threading/README.md) | A helper class used to simplify threading behavior. |