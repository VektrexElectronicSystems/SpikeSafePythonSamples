# Application-Specific Examples

These sequences address specific scenarios in which SpikeSafe functionality is used in an integrated test system, or scenarios where more advanced SpikeSafe settings need to be tuned to meet specific criteria. These sequences are for users that are comfortable with the basic functionality of the SpikeSafe PRF or SMU. See individual folders' descriptions for more information on each sequence.

## Directory
- [Fixed Pulse Count Using Software Timing](fixed_pulse_count_using_software_timing)
- [Making Tj Measurements](making_tj_measurements)
- [Measuring DC Staircase Voltages](measuring_dc_staircase_voltages)
- [Measuring Wavelength Spectrum](measuring_wavelength_spectrum)
- [Pulse Tuning](pulse_tuning)
- [Running LIV Sweeps](running_liv_sweeps)
- [Using Digitizer Output Trigger](using_digitizer_output_trigger)
- [Using Pulse Holds](using_pulse_holds)

## Usage

Vektrex recommends getting acquainted with basic SpikeSafe features described in any of the other folders within [SpikeSafePythonSamples](/../../) before running these sequences. If any additional explanation or insight is necessary, contact support@vektrex.com. 

Some of these sequences involve graphing measurement results, and require the [matplotlib](https://matplotlib.org/) library. See instructions on installing this library under the "Usage" section in the [SpikeSafePythonSamples markdown file](/README.md#installing-matplotlib-package).

Some of these sequences employ external C resources, and require the [PyCLibrary](https://pyclibrary.readthedocs.io/en/latest/) library. See instructions on installing this library under the "Usage" section in the [SpikeSafePythonSamples markdown file](/README.md#installing-pyclibrary-package).

For some of these sequences, some external instrumentation such as a spectrometer or a temperature-control device may be necessary. Read the individual sequence's description to see which settings and instrumentation need modification, and adjust settings based on your given test setup. For some of these sequences, some repetition is necessary as trial and error is the best method to achieve the desired outcome.

