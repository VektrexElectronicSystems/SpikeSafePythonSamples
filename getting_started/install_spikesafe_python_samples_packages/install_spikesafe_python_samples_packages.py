import sys
import subprocess

def install_pip():
    try:
        # Construct the command to install or upgrade pip
        command = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]

        # Run the command
        subprocess.check_call(command)
        print("Successfully installed/upgraded pip.")
    except subprocess.CalledProcessError:
        # If pip is not installed, install it
        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
            print("Successfully installed pip.")
        except subprocess.CalledProcessError:
            print("Error installing or upgrading pip.")
            sys.exit(1)

def install_packages(packages):
    try:
        # Construct the command to install or upgrade the packages
        command = [sys.executable, "-m", "pip", "install", "--upgrade"] + packages

        # Run the command
        subprocess.check_call(command)
        print("Successfully installed or upgraded packages.")
    except subprocess.CalledProcessError:
        print("Error installing or upgrading packages.")

# Check and install or upgrade pip if necessary
install_pip()

# Specify the packages to install or upgrade
packages_to_install = ["spikesafe-python", "matplotlib", "PyCLibrary", "pyserial"]

# Install or upgrade the packages
install_packages(packages_to_install)
