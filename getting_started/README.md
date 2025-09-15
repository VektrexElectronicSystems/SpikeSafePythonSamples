# Getting Started

These sequences are primarily intended for first-time users of Vektrex products. They contain steps to perform the basic tasks that are necessary to run the sequences within SpikeSafePythonSamples/[Run SpikeSafe Operating Modes](../run_spikesafe_operating_modes).

## Directory
For first-time users, Vektrex recommends running the sequences in the order shown below:

1. [Importing SpikeSafePythonSamples packages](install_spikesafe_python_samples_packages) - Automatically installs all necessary packages to run all SpikeSafePythonSamples scripts
1. [TCP Sample](tcp_socket_sample) - A more in depth example that connects to the SpikeSafe using a TCP socket. An *IDN? query is sent with more verbose Python commands
1. [Read *IDN?](read_idn) - Uses the SCPI Standard "*IDN?" query and following information queries to obtain the model of your SpikeSafe
1. [Read All Events](spikesafe_python.read_all_events) - Reads all events from the SpikeSafe event queue 
1. [Read Memory Table Data](read_memory_table_data) - Reads the SpikeSafe status and obtains current operational information from the SpikeSafe
1. [Discharge Channel](discharge_channel) - Shows how to properly shut down the SpikeSafe channel and wait for the load voltage to discharge before taking further action
1. [SCPI Logging](scpi_logging) - Shows how to log SpikeSafe SCPI messages sent over the TCP socket to a file

## Usage
To run these sequences, an IDE such as [Visual Studio Code](https://code.visualstudio.com/) is required. The [spikesafe-python](https://pypi.org/project/spikesafe-python/) repository will need to be installed as a package using the command `python -m pip install spikesafe-python`. Vektrex recommends always having the latest version of spikesafe-python when running these sequences; the current version is 1.1.0. It may help to run these sequences in a [virtual environment](https://docs.python.org/3/tutorial/venv.html).

Simply change the line `ip_address = '10.0.0.220'` to match the IP address of you connected SpikeSafe and run the sequence (generally by pressing F5). Observe the outputs that appear in both the terminal window and SpikeSafePythonSamples.log, which will output wherever you have saved the SpikeSafePythonSamples repository.