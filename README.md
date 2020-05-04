# SpikeSafe Python Samples

Use these code samples to start learning how to communicate with your SpikeSafe via TCP/IP using Python. Sequences can be run with the following Vektrex products:
 - [SpikeSafe SMU](https://www.vektrex.com/products/spikesafe-source-measure-unit/)
 - [SpikeSafe Performance Series ("PRF")](https://www.vektrex.com/products/spikesafe-performance-series-precision-pulsed-current-sources/)

## Directory

- [Getting Started](/getting_started) - These sequences are primarily intended for first-time users of Vektrex products. They contain steps to perform the basic tasks that are necessary to run the sequences within [Instrument Examples](/instrument_examples).
- [Instrument Examples](/instrument_examples) - These folders contain examples to run specific SpikeSafe modes. Basic settings will be sent to the SpikeSafe, and then one or more channels will be enabled to demonstrate the operation of each mode.
  - [Run Bias Pulsed](/instrument_examples/run_bias_pulsed)
  - [Run Bias](/instrument_examples/run_bias)
  - [Run DC](/instrument_examples/run_dc)
  - [Run Modulated DC](/instrument_examples/run_modulated_dc)
  - [Run Multi Pulse](/instrument_examples/run_multi_pulse)
  - [Run Pulsed Sweep](/instrument_examples/run_pulsed_sweep)
  - [Run Pulsed](/instrument_examples/run_pulsed)
  - [Run Single Pulse](/instrument_examples/run_single_pulse)
- [Application Specific Examples](/application_specific_examples) - These folders consist of more advanced sequences to address specific test scenarios, as well as some demonstrations to fine-tune your SpikeSafe current output.

## Usage

Each script can be run independently as a standalone Python file. Run a file  in its current state and verify that the expected outputs are obtained, as specified by the file's markdown description.

For most examples, you may need to modify the specified IP address within a sequence to match the IP address that is physically set on your SpikeSafe's DIP switch. In each sequence, the default IP address is set to 10.0.0.220 in the line `ip_address = '10.0.0.220'`.

Each file can be modified to include additional settings and commands to fit individual needs. Refer to SpikeSafe documentation for more information on the SpikeSafe API.

## Downloading Files

On this page, press "Clone or download" to download all files in this repository. We recommend saving this repository to your working directory for all other GitHub repositories.

If only a specific sequence or folder is needed, right-click the desired file/folder and select "Save link as...".

## Where Do I Start?

First start with [read_idn.py](/getting_started/read_idn) sample to learn how setup a simple socket to communicate with your SpikeSafe. Then check out the rest of the samples under [Getting Started](/getting_started).

## Built With

* [Visual Studio Code](https://code.visualstudio.com/)
* [Python for Windows](https://www.python.org/downloads/windows/)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Support/Feedback

If any further assistance is needed beyond the information provided within this repository, email support@vektrex.com.

Feature requests and bug reports can be submitted to the [Issues Page](/issues) of this repository. This page is regularly monitored and maintained by Vektrex engineers.

## Authors

* **Bill Thompson** - [BillThomp](https://github.com/BillThomp)
* **Eljay Gemoto** - [eljayg](https://github.com/eljayg)

## License

Licensed under the Vektrex Sample License.
