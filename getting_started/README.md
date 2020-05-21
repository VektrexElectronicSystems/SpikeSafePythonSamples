# Getting Started

These sequences are primarily intended for first-time users of Vektrex products. They contain steps to perform the basic tasks that are necessary to run the sequences within SpikeSafePythonExamples/[Run SpikeSafe Operating Modes](../run_spikesafe_operating_modes).

## Directory
For first-time users, Vektrex recommends running the sequences in the order shown below:

1. [TCP Sample](tcp_socket_sample) - a more in depth example that connects to the SpikeSafe using a TCP socket. An *IDN? query is sent with more verbose Python commands.
2. [Read *IDN?](read_idn) - Uses the SCPI Standard "*IDN?" query to obtain the model your SpikeSafe
3. [Read All Events](read_all_events) - Reads all events from the SpikeSafe event queue 
4. [Read Memory Table Data](read_memory_table_data) - Reads the SpikeSafe status and obtains current operational information from the SpikeSafe

## Usage
To run these sequences, an IDE such as [Visual Studio Code](https://code.visualstudio.com/) is required. The [spikesafe-python](https://pypi.org/project/spikesafe-python/) repository will need to be installed as a package using the command `python -m pip install spikesafe-python`. Vektrex recommends always having the latest version of spikesafe-python when running these sequences; the current version is 1.1.0. It may help to run these sequences in a [virtual environment](https://docs.python.org/3/tutorial/venv.html).


Simply change the line `ip_address = '10.0.0.220'` to match the IP address of you connected SpikeSafe and run the sequence (generally by pressing F5). Observe the outputs that appear in the terminal window.