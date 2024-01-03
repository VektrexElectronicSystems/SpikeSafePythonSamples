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

## Usage

### Python
Download from the official [Python](https://www.python.org/downloads/) website.

During Python installation check the box Add Python to PATH when prompted.
- Confirm Python PATH is set in **Command Prompt** by typing `py --version` to verify the Python version

Installing Python will install:
- IDLE  
- Python Launcher  
- Python3 Interpreter

After Python installation is complete, restart the computer to ensure packages under the [Packages](#packages) Section can be successfully installed.

It is recommended to use a version of Python with the status key of bugfix or higher, see [Python Release Cycle](https://devguide.python.org/versions/#versions).

#### Windows Setup

##### Use the Standard Console Command Prompt
To open Command Prompt press the key combination Windows + R to open a Run dialog, and then type cmd and hit Enter or click Ok.

##### Add Python to PATH
It is recommended that the path of Python Interpreter is added for easy usage. If this was not done in as part of the [Python](#python) section, it can be manually done afterwards.

Manually add Python to Windows Path:
- Press the key combination **Windows + R** to open a Run dialog
- Type `sysdm.cpl` to open the System Properties
- Press **Advanced** tab and then press on **Environment Variables…** to open Environment Variables dialog
- Under the **User variables** box, press on **New…** to add the `Path` variable (if your **Path** variable already exists, then press on **Edit…** instead):
- Set the Path **Variable value** to the 1) `Python application path` and 2) `Python Scripts path`. To find these paths and set the value:
   - Type `Python` in the Windows Search Bar
   - Right-click on the **Python App**, and then press **Open file location**
   - Right-click on the **Python shortcut**, and then press **Open file location** (this is the `Python application path`)
   - Navigate to the **scripts** folder (this is the `Python Scripts path`)
   - Set the Path **Variable value** to `Python application path;Python Scripts path` (paths are separated by a semicolon)
- Press **OK**
- Confirm Python PATH is set in **Command Prompt** by typing `py --version` to verify the Python version

#### Mac OS X Setup

##### Use the Standard Console Terminal
To open Terminal navigate to Applications, then Utilities, then double-click the Terminal program.

##### Add Python to PATH 
It is recommended that the path of Python Interpreter is added for easy usage. To do this:

- The path for Python interpreter can be found by opening **Python Launcher application** (this is the `Python install directory`)
- Open **Terminal**
- Type `sudo nano /etc/paths`  
- Enter path of the `Python install directory` here  
- Press `Control + X` to exit  
- Press `Y` to save  
- Confirm Python PATH is set in **Terminal** by typing `python3 --version` to verify the Python version

### IDEs

#### Visual Studio Code and Using a Virtual Environment
To run these sequences a light-weight IDE, or to target cross-platform development, use the free [Visual Studio Code](https://code.visualstudio.com/). See [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial) to simply setup your IDE with Python. Optionally, using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) is recommended to successfully meet the installation requirements to run these sequences. To setup your virtual environment run the follow commands and then continue to install the remaining Python packages later in this document:

| OS | Command |
| - | - |
| Windows | `py -m venv .venv` followed by `.venv\scripts\activate` |
| macOS | `python3 -m venv .venv` followed by `.venv\scripts\activate` |

#### Visual Studio Community
To run these sequences in a more feature rich IDE, use the free [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/). See [Python In Visual Studio](https://docs.microsoft.com/en-us/visualstudio/python/tutorial-working-with-python-in-visual-studio-step-00-installation?view=vs-2022) to simply setup your IDE with Python. Optionall, using a [virtual environment](https://docs.microsoft.com/en-us/visualstudio/python/managing-python-environments-in-visual-studio?view=vs-2022) is recommended to successfully meet the installation requirements to run these sequences.

### Packages
SpikeSafePythonSamples requires packages to run all scripts.

There are two ways to install these packages:
1. See Section [Automatically Install Packages](#automatically-install-packages)
2. See Section [Manually Install Packages](#manually-install-packages)

After all packages are installed, refer to section [Package Helpers](#package-helpers) to verify package details.

#### Automatically Install Packages
All necessary SpikeSafePythonSamples packages may be installed automatically. See [Install SpikeSafePythonSamples Packages](/getting_started/install_spikesafe_python_samples_packages/) and run the python .py script in this directory.

#### Manually Install Packages
All necessary SpikeSafePythonSamples packages may be installed manually. Perform all of the subsections below.

##### Installing pip Package
Installing packages use [pip](https://pypi.org/project/pip/). It is recommended that pip be updated to latest version.

First, check if your environment has pip installed, run command:
| OS | Command |
| - | - |
| Windows | `py -m pip --version` |
| macOS | `python3 -m pip --version` |

If your environment does not have pip installed, run command:
| OS | Command |
| - | - |
| Windows | `py -m ensurepip --upgrade` |
| macOS | `python3 -m ensurepip --upgrade` |

To install/upgrade pip, run command: 
| OS | Command |
| - | - |
| Windows | `py -m pip install --upgrade pip` |
| macOS | `python3 -m pip install --upgrade pip` |

##### Installing spikesafe-python Package
The [spikesafe-python](https://pypi.org/project/spikesafe-python/) library will need to be installed. Vektrex recommends always having the latest version of spikesafe-python when running these sequences; the current version is 1.5.15.

To install this package, run command:
| OS | Command |
| - | - |
| Windows | `py -m pip install spikesafe-python` |
| macOS | `python3 -m pip install spikesafe-python` |

Once the spikesafe-python package is installed, each script in this repository can be run independently as a standalone Python file. Run a file in its current state and verify that the expected outputs are obtained, as specified by the file's markdown description.

Complete class documentation is available for spikesafe-python in [spikesafe-python API Overview](spikesafe_python_lib_docs).

##### Installing matplotlib Package
Some sequences involve graphing measurement results. To properly graph results, the [matplotlib](https://matplotlib.org/) library is required (version 3.2.1 or greater). Once the matplotlib library is installed, each sequence that involves graphing can be run as a standalone Python file.

To install this package, run command:
| OS | Command |
| - | - |
| Windows | `py -m pip install matplotlib` |
| macOS | `python3 -m pip install matplotlib` |

##### Installing PyCLibrary Package
Some sequences require external C resources, and requires the [PyCLibrary](https://pyclibrary.readthedocs.io/en/latest/) library. Once the PyCLibrary library is installed, each sequence that involves external C resources can be run as a standalone Python file.

To install this package, run command:
| OS | Command |
| - | - |
| Windows | `py -m pip install pyclibrary` |
| macOS | `python3 -m pip install pyclibrary` |

##### Installing pyserial Package
Some sequences involve connecting to a serial interface instrument and requires the [pyserial](https://pypi.org/project/pyserial/) library (version 3.5 or greater). Once the pyserial library is installed, each sequence that involves a serial interface can be run as a standalone Python file.

To install this package, run command:
| OS | Command |
| - | - |
| Windows | `py -m pip install pyserial` |
| macOS | `python3 -m pip install pyserial` |

#### Package Helpers

##### How to View All Installed Packages
A list of all installed packages can be displayed.

To view all installed packages, run command:
| OS | Command |
| - | - |
| Windows | `pip freeze` |
| macOS | `pip3 freeze` |

##### How to View Details of an Installed Package
After a package is installed the details of a package can be displayed.

To view details of a package, run command: 
| OS | Command |
| - | - |
| Windows | `pip show <package name>` |
| macOS | `pip3 show <package name>` |

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

## FAQ

I'm developing an application using NI-VISA, what is the recommended practice for handling termination characters?<br />
See [Termination Characters in NI-VISA](https://www.ni.com/en-us/support/documentation/supplemental/06/termination-characters-in-ni-visa.html)

I'm developing an application using MATLAB, how do I get started?<br />
See [System Requirements for MATLAB Engine API for Python](https://www.mathworks.com/help/matlab/matlab_external/system-requirements-for-matlab-engine-for-python.html) to ensure your system can support Python. Then see [Call Python from MATLAB](https://www.mathworks.com/help/matlab/call-python-libraries.html) on how to access Python libraries in MATLAB.

## Support/Feedback

If any further assistance is needed beyond the information provided within this repository, email support@vektrex.com.

Feature requests and bug reports can be submitted to [the Vektrex website's support page](https://www.vektrex.com/request-support/). Select "Other" as the Product/System and enter "SpikeSafePythonSamples GitHub Repository" as the Subject.

## Contributors

* **Andy Fung** - [andyfung](https://github.com/andyfung)
* **Bill Thompson** - [BillThomp](https://github.com/BillThomp)
* **Brad Wise** - [BradWise](https://github.com/bradwise)
* **Eljay Gemoto** - [eljayg](https://github.com/eljayg)

## License

SpikeSafePythonSamples is licensed under the MIT license, which allows for non-commercial and commercial use.
