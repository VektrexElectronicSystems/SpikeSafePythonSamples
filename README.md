# SpikeSafe Python Samples

Use these code samples to start learning how to communicate with your SpikeSafe via TCP/IP using Python. Sequences can be run with the following Vektrex products:
 - [SpikeSafe SMU](https://www.vektrex.com/products/spikesafe-source-measure-unit/)
 - [SpikeSafe Performance Series ("PRF")](https://www.vektrex.com/products/spikesafe-performance-series-precision-pulsed-current-sources/)

## Directory

- [Getting Started](getting_started) - These sequences are primarily intended for first-time users of Vektrex products. They contain steps to perform the basic tasks that are necessary to run the sequences within the run_spikesafe_operating_modes folder.
- [Run SpikeSafe Operating Modes](run_spikesafe_operating_modes) - These folders contain examples to run specific SpikeSafe modes designed to test LEDs, Lasers, and electrical equipment. Basic settings will be sent to the SpikeSafe, and then one or more channels will be enabled to demonstrate the operation of each mode.
- [Making Integrated Voltage Measurements](making_integrated_voltage_measurements) - These folders contain examples to measure voltage using the SpikeSafe SMU's integrated voltage Digitizer. The SpikeSafe outputs current to an LED, Laser, or electrical equipment, and then voltage measurements are read and displayed onscreen.
- [Using the Force Sense Selector Switch](using_force_sense_selector_switch) - These folders contain examples to operate the optional integrated switch within the SpikeSafe SMU. The SpikeSafe outputs to an LED, Laser, or electrical equipment as in the previous examples, and the switch is used to either disconnect the SpikeSafe from the test circuit or to operate an auxiliary source to power the DUT.
- [Application-Specific Examples](application_specific_examples) - These folders consist of more advanced sequences to address specific test scenarios, as well as some demonstrations to fine-tune your SpikeSafe current output. These sequences explain how to make light measurements using a SpikeSafe and a spectrometer, how to make in-situ junction temperature measurements on LEDs, and how to take full advantage of all SpikeSafe features.

## Usage

### IDE and Using a Virtual Environment
To run these sequences, an IDE such as [Visual Studio Code](https://code.visualstudio.com/) is required. Optionally, using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) is recommended to successfully meet the installation requirements to run these sequences. After your virtual environment is setup, continue to install the remaining Python packages below.

### Installing spikesafe-python Package
The [spikesafe-python](https://pypi.org/project/spikesafe-python/) repository will need to be installed as a package using the command `python -m pip install spikesafe-python`. Vektrex recommends always having the latest version of spikesafe-python when running these sequences; the current version is 1.1.0.

Once the spikesafe-python package is installed, each script in this repository can be run independently as a standalone Python file. Run a file in its current state and verify that the expected outputs are obtained, as specified by the file's markdown description.

### Installing matplotlib Package
Some sequences involve graphing measurement results. To properly graph results, the [matplotlib](https://matplotlib.org/) library is required (version 3.2.1 or greater). Use the command `python -m pip install matplotlib` to install the latest version of matplotlib. Once the matplotlib library is installed, each sequence that involves graphing can be run as a standalone Python file.

### Installing PyCLibrary Package
Some sequences require external C resources, and requires the [PyCLibrary](https://pyclibrary.readthedocs.io/en/latest/) library. To install this library, enter the command `python -m pip install pyclibrary`. Once the PyCLibrary library is installed, each sequence that involves external C resources can be run as a standalone Python file.

### General Usage
For most examples, you may need to modify the specified IP address within a sequence to match the IP address that is physically set on your SpikeSafe's DIP switch. In each sequence, the default IP address of 10.0.0.220 is set in the line `ip_address = '10.0.0.220'`.

Each file can be modified to include additional settings and commands to fit individual needs. Refer to SpikeSafe documentation for more information on the SpikeSafe API.

Most examples will log messages to the SpikeSafePythonSamples.log file under your local SpikeSafePythonSamples\ directory. Please refer to this file to ensure your sequence is running correctly.

## Downloading Files

On this page, press "Clone or download" to download all files in this repository. We recommend saving this repository to your working directory for all other GitHub repositories.

If only a specific sequence or folder is needed, right-click the desired file/folder and select "Save link as...".

## Where Do I Start?

First start with [TCP Socket Sample](getting_started/tcp_socket_sample) to learn how setup a simple socket to communicate with your SpikeSafe. Then check out the rest of the samples under [Getting Started](getting_started).

## Built With

* [Visual Studio Code](https://code.visualstudio.com/)
* [Python for Windows](https://www.python.org/downloads/windows/)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/VektrexElectronicSystems/SpikeSafePythonSamples/tags). 

## Support/Feedback

If any further assistance is needed beyond the information provided within this repository, email support@vektrex.com.

Feature requests and bug reports can be submitted to [the Vektrex website's support page](https://www.vektrex.com/request-support/). Select "Other" as the Product/System and enter "GitHub Repository" as the Subject.

## Contributors

* **Bill Thompson** - [BillThomp](https://github.com/BillThomp)
* **Eljay Gemoto** - [eljayg](https://github.com/eljayg)

## License

SpikeSafePythonSamples is licensed under the MIT license, which allows for non-commercial and commercial use.
