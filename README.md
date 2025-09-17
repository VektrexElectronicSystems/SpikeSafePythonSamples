# SpikeSafe Python Samples

Use these code samples to start learning how to communicate with your SpikeSafe via TCP/IP using Python. Sequences can be run with the following Vektrex products:
 - [SpikeSafe PSMU](https://www.vektrex.com/products/spikesafe-source-measure-unit/)
 - [SpikeSafe Performance Series ("PRF")](https://www.vektrex.com/products/spikesafe-performance-series-precision-pulsed-current-sources/)

## Directory

- [Getting Started](getting_started) - These sequences are primarily intended for first-time users of Vektrex products. They contain steps to perform the basic tasks that are necessary to run the sequences within the run_spikesafe_operating_modes folder.
- [Run SpikeSafe Operating Modes](run_spikesafe_operating_modes) - These folders contain examples to run specific SpikeSafe modes designed to test LEDs, Lasers, and electrical equipment. Basic settings will be sent to the SpikeSafe, and then one or more channels will be enabled to demonstrate the operation of each mode.
- [Making Integrated Voltage Measurements](making_integrated_voltage_measurements) - These folders contain examples to measure voltage using the SpikeSafe PSMU's integrated voltage Digitizer. The SpikeSafe outputs current to an LED, Laser, or electrical equipment, and then voltage measurements are read and displayed onscreen.
- [Using the Force Sense Selector Switch](using_force_sense_selector_switch) - These folders contain examples to operate the optional integrated switch within the SpikeSafe PSMU. The SpikeSafe outputs to an LED, Laser, or electrical equipment as in the previous examples, and the switch is used to either disconnect the SpikeSafe from the test circuit or to operate an auxiliary source to power the DUT.
- [Application-Specific Examples](application_specific_examples) - These folders consist of more advanced sequences to address specific test scenarios, as well as some demonstrations to fine-tune your SpikeSafe current output. These sequences explain how to make light measurements using a SpikeSafe and a spectrometer, how to make in-situ junction temperature measurements on LEDs, and how to take full advantage of all SpikeSafe features.
- [spikesafe-python API Overview](spikesafe_python_lib_docs). These folders contain complete class documentation for the spikesafe-python package used to power all of the aforementioned example directories.

## Downloading Files

On this page, press **Clone or download** to download all files in this repository. We recommend saving this repository to your working directory with all other GitHub repositories.

If only a specific sequence or folder is needed, right-click the desired file/folder and select **Save link as...**.

## Project Setup

### Setup Steps

1. **Install Python 3.10+**
   - Download Python from [python.org](https://www.python.org/downloads/).
   - During installation check **Add Python to PATH**.

2. **Verify Python**
   - Open a terminal and run:
      | OS | Command |
      | - | - |
      | Windows | `py --version` |
      | macOS | `python3 --version` |

3. **Install [pip](https://pypi.org/project/pip/)**
   - Run:
      | OS | Command |
      | - | - |
      | Windows | `py -m pip install --upgrade pip` |
      | macOS | `python3 -m pip install --upgrade pip` |

4. **Install Dependencies**
   - Set terminal to the directory containing `requirements.txt`, run:
     ```bash
     cd <path to directory containing requirements.txt>
     ```
   - Run:
      | OS | Command |
      | - | - |
      | Windows | `py -m pip install --force-reinstall -r requirements.txt` |
      | macOS | `python3 -m pip install --force-reinstall -r requirements.txt` |

### IDEs

#### Visual Studio Code
To run these sequences a light-weight IDE, or to target cross-platform development, use the free [Visual Studio Code](https://code.visualstudio.com/). See [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial) to simply setup your IDE with Python. Optionally, using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) is recommended to successfully meet the installation requirements to run these sequences.

#### Visual Studio Community
To run these sequences in a more feature rich IDE, use the free [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/). See [Python In Visual Studio](https://docs.microsoft.com/en-us/visualstudio/python/tutorial-working-with-python-in-visual-studio-step-00-installation?view=vs-2022) to simply setup your IDE with Python. Optionally, using a [virtual environment](https://docs.microsoft.com/en-us/visualstudio/python/managing-python-environments-in-visual-studio?view=vs-2022) is recommended.

## Where Do I Start?

Start with [TCP Socket Sample](getting_started/tcp_socket_sample) to learn how setup a simple socket to communicate with your SpikeSafe. Then check out the rest of the samples under [Getting Started](getting_started).

You will need to modify the specified IP address within a sequence to match the IP address that is physically set on your SpikeSafe's DIP switch. In each sequence, the default IP address of 10.0.0.220 is set in the line `ip_address = '10.0.0.220'`.

Each file can be modified to include additional settings and commands to fit individual needs. Complete class documentation is available in [spikesafe-python API Overview](spikesafe_python_lib_docs).

Most examples will log messages to the SpikeSafePythonSamples.log file under your local SpikeSafePythonSamples\ directory. Please refer to this file to ensure your sequence is running correctly.

## Built With

* [Visual Studio Code](https://code.visualstudio.com/)
* [Python for Windows](https://www.python.org/downloads/windows/)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/VektrexElectronicSystems/SpikeSafePythonSamples/tags). 

## FAQ

I'm developing an application using NI-VISA, what is the recommended practice for handling termination characters?  
See [Termination Characters in NI-VISA](https://www.ni.com/en-us/support/documentation/supplemental/06/termination-characters-in-ni-visa.html)

I'm developing an application using MATLAB, how do I get started?  
See [System Requirements for MATLAB Engine API for Python](https://www.mathworks.com/help/matlab/matlab_external/system-requirements-for-matlab-engine-for-python.html) to ensure your system can support Python. Then see [Call Python from MATLAB](https://www.mathworks.com/help/matlab/call-python-libraries.html) on how to access Python libraries in MATLAB.

Why does my script's performance vary between different operating systems and machines?  
See [Remarks](/spikesafe_python_lib_docs/Threading/wait/README.md#remarks) describing resolution of system timers between operating systems.

How does Python handle locale?  
The [locale](https://docs.python.org/3/library/locale.html#module-locale) module is implemented on top of the _locale module, which in turn uses an ANSI [C locale](https://docs.oracle.com/cd/E19253-01/817-2521/overview-1002/index.html) (also called the "POSIX locale") implementation if available. The C locale is often described as "culture-neutral" because it doesn't apply any regional or language-specific rules for formatting data. It is a basic, system-independent locale that follows standardized rules for formatting data such as numbers, dates, and currency. The C locale uses U.S.-style conventions by default, such as:
- Period (.) as the decimal point for numbers
- Simple ASCII character classification and sorting
- English-style date and time formats

## Support/Feedback

If any further assistance is needed beyond the information provided within this repository, email support@vektrex.com.

Feature requests and bug reports can be submitted to [the Vektrex website's support page](https://www.vektrex.com/request-support/). Select **Other** as the Product/System and enter **SpikeSafePythonSamples GitHub Repository** as the Subject.

## Contributors

* **Andy Fung** - [andyfung](https://github.com/andyfung)
* **Bill Thompson** - [BillThomp](https://github.com/BillThomp)
* **Brad Wise** - [BradWise](https://github.com/bradwise)
* **Eljay Gemoto** - [eljayg](https://github.com/eljayg)

## License

SpikeSafePythonSamples is licensed under the MIT license, which allows for non-commercial and commercial use.
