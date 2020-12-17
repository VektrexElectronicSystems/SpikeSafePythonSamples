# Example for TCP Socket

## **Purpose**
Demonstrate how to use a light-weight TCP socket to communicate with a SpikeSafe PRF or PSMU.

### Overview 
In this example we cover how to create a socket, how to send encoded SCPI commands to the SpikeSafe, and read data through the TCP buffer.

This example does not use any additional libraries to show how easy it is to communicate with a SpikeSafe. All other examples in this repository are powered by [spikesafe-python](https://pypi.org/project/spikesafe-python/), Vektrex's official Python package that provides light-weight access Python helper classes and functions to easily communicate with to your SpikeSafe and parse data into easy to use objects.