# Gigabyte K85 Backend
This project is part of a larger project to control RGB keyboards from
Python with a unified interface, check [python-rgb-keyboards](https://github.com/RedFantom/python-rgb-keyboards).

## Interface Description
For the Gigabyte K85 interface description, check `/INTERFACE.md`. The
Gigabyte K85 is a relatively simple single-color RGB keyboard with 
support for the full 8-bit RGB spectrum.

## Disclaimer
Nothing in this repository was created or developed with the support of 
Gigabyte or any of its affiliates. They have explicitly refused to 
provide any help to this project. Please post any and all questions or
issues on the issues page of this GitHub repository.

## Usage
To use this backend with the `rgbkeyboards` package, simply import this
module. The backend must be registered with `rgbkeyboards` before 
usage with the `register(path=None)` function.

Note that this module depends on `pyusb` with an available backend. On
Windows, the backend `libusb1` is enforced and requires a DLL file of 
which the path must be passed to the `register(path=full_dll_path)`
function.

The required binary file is located in a 7z-archive that can be 
downloaded from [here](https://github.com/libusb/libusb/releases). The
actual DLL-files for 32-bit and 64-bit architectures are located in 
`/MS32/dll/libusb-1.0.dll` and `/MS64/dll/libusb-1.0.dll` respectively.

This backend is not included with the base `rgbkeyboards` installation
because the DLL files are packaged in a 7z-archive for Windows, and 
unpacking those files with Python is impossible in a cross-platform
implementation.

## License
```
Gigabyte K85 rgbkeyboards backend and interface description
Copyright (C) 2018 RedFantom

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the license.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```

## Firmware
The Gigabyte software to control the RGB LEDs on the K85 may prompt to
execute a firmware update. This may execute fine, but if you find 
yourself with a seemingly bricked keyboard after a mysterious error
occurs, please check `/FIRMWARE.md`.
 
