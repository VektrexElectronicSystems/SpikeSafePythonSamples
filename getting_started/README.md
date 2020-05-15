# Getting Started

These sequences are primarily intended for first-time users of Vektrex products. They contain steps to perform the basic tasks that are necessary to run the sequences within SpikeSafePythonExamples/Instrument Examples.

## Directory

- [Read All Events](read_all_events) - Reads all events from the SpikeSafe event queue
- [Read *IDN?](read_idn) - Uses the SCPI Standard "*IDN?" query to obtain the model your SpikeSafe
- [Read Memory Table Data](read_memory_table_data) - Reads the SpikeSafe status and obtains current operational information from the SpikeSafe
- [TCP Sample](tcp_socket_sample) - a more in depth example that connects to the SpikeSafe using a TCP socket. An *IDN? query is sent with more verbose Python commands.

## Usage

Simply change the line `ip_address = '10.0.0.220'` to match the IP address of you connected SpikeSafe and run the sequence (generally by pressing F5). Observe the outputs that appear in the terminal window.