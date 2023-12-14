# Python using TAM API

[![TAM - API](https://img.shields.io/static/v1?label=TAM&message=API&color=b51839)](https://www.triamec.com/en/tam-api.html)

This example demonstrates the use of the TAM API with Python.
With the installation of the [Python.NET package](https://pypi.org/project/pythonnet/), Python programmers have an almost seamless integration with the .NET Common Language Runtime (CLR).
It allows Python code to interact with the CLR respectivelly with the TAM API.

## Hardware Prerequisites
- Connection to the drive by *Tria-Link* (via PCI adapter), *USB* or *Ethernet*

## Software Prerequisites
- Windows OS
- TAM API available (comes along with the *TAM System Explorer*)
- Make sure that Python is installed on your system
- [Python.NET](https://pypi.org/project/pythonnet/) installed

## Getting Started
The example shows how the TAM API can be integrated into Python and reading a register or recording data.
Before you run the example code, the following parameters may need to be adapted to your application:
- Path and version of the TAM Software `TAM_SOFTWARE_PATH = path.join(environ['ProgramFiles'], 'Triamec', 'Tam', '7.24.1', 'SDK')`
- Name of the axis `axis_name = 'Axis 0'`

## Tested with
- Windows 11
- Python **3.11.4**
- TAM SDK **7.24.1**
- pythonnet **3.0.3**
