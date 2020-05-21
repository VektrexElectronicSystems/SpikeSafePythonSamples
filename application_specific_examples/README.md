# Application-Specific Examples

These sequences address specific scenarios in which SpikeSafe functionality is used in an integrated test system, or scenarios where more advanced SpikeSafe settings need to be tuned to meet specific criteria. These sequences are for users that are comfortable with the basic functionality of the SpikeSafe PRF or SMU. See individual folders' descriptions for more information on each sequence.

## Directory
- [Making Tj Measurements](making_tj_measurements)
- [Running LIV Sweeps](running_liv_sweeps)
- [Using Pulse Holds](using_pulse_holds)

## Usage

Vektrex recommends getting acquainted with basic SpikeSafe features described in any of the other folders within [SpikeSafePythonSamples](/../../) before running these sequences. If any additional explanation or insight is necessary, contact support@vektrex.com. 

Most of these sequences involve graphing measurement results. To properly graph results, the [matplotlib](https://matplotlib.org/) library is required (version 3.2.1 or greater). Use the command `python -m pip install -U matplotlib` to install the latest version of matplotlib. You may want to perform this within a [virtual environment](https://docs.python.org/3/tutorial/venv.html). Once the matplotlib library is installed, each sequence can be run as a standalone Python file.

For some of these sequences, some external instrumentation such as a spectrometer or a temperature-control device may be necessary. Read the individual sequence's description to see which settings and instrumentation need modification, and adjust settings based on your given test setup. For some of these sequences, some repetition is necessary as trial and error is the best method to achieve the desired outcome.

