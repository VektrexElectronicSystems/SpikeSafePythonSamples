# SpikeSafe Python Samples

Use these code samples to start learning how to communicate with your SpikeSafe via TCP/IP using Python. Sequences can be run with the following Vektrex products:
 - [SpikeSafe SMU](https://www.vektrex.com/products/spikesafe-source-measure-unit/)
 - [SpikeSafe Performance Series ("PRF")](https://www.vektrex.com/products/spikesafe-performance-series-precision-pulsed-current-sources/)

## Directory

- [Getting Started](getting_started) - These sequences are primarily intended for first-time users of Vektrex products. They contain steps to perform the basic tasks that are necessary to run the sequences within the instrument_examples folder.
- [Run SpikeSafe Operating Modes](run_spikesafe_operating_modes) - These folders contain examples to run specific SpikeSafe modes designed to test LEDs, Lasers, and electrical equipment. Basic settings will be sent to the SpikeSafe, and then one or more channels will be enabled to demonstrate the operation of each mode.
- [Making Integrated Voltage Measurements](making_integrated_voltage_measurements) - These folders contain examples to measure voltage using the SpikeSafe SMU's integrated voltage Digitizer. The SpikeSafe outputs current to an LED, Laser, or electrical equipment, and then voltage measurements are read and displayed onscreen.
- [Application Specific Examples](application_specific_examples) - These folders consist of more advanced sequences to address specific test scenarios, as well as some demonstrations to fine-tune your SpikeSafe current output. These sequences explain how to make light measurements using a SpikeSafe and a spectrometer, how to make in-situ junction temperature measurements on LEDs, and how to take full advantage of all SpikeSafe features.

## Usage

Each script can be run independently as a standalone Python file. Run a file  in its current state and verify that the expected outputs are obtained, as specified by the file's markdown description.

For most examples, you may need to modify the specified IP address within a sequence to match the IP address that is physically set on your SpikeSafe's DIP switch. In each sequence, the default IP address is set to 10.0.0.220 in the line `ip_address = '10.0.0.220'`.

Each file can be modified to include additional settings and commands to fit individual needs. Refer to SpikeSafe documentation for more information on the SpikeSafe API.

## Downloading Files

On this page, press "Clone or download" to download all files in this repository. We recommend saving this repository to your working directory for all other GitHub repositories.

If only a specific sequence or folder is needed, right-click the desired file/folder and select "Save link as...".

## Where Do I Start?

First start with [TCP Socket Sample](getting_started/tcp_socket_sample) to learn how setup a simple socket to communicate with your SpikeSafe. Then check out the rest of the samples under [Getting Started](getting_started).

## Built With

* [Visual Studio Code](https://code.visualstudio.com/)
* [Python for Windows](https://www.python.org/downloads/windows/)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Support/Feedback

If any further assistance is needed beyond the information provided within this repository, email support@vektrex.com.

Feature requests and bug reports can be submitted to the [Issues Page](issues) of this repository. This page is regularly monitored and maintained by Vektrex engineers.

## Authors

* **Bill Thompson** - [BillThomp](https://github.com/BillThomp)
* **Eljay Gemoto** - [eljayg](https://github.com/eljayg)

## License

Licensed under the Vektrex Sample License.
